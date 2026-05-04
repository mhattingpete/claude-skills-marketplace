"""macOS native read-only adapters."""

from __future__ import annotations

import platform
import plistlib
import re
import sqlite3
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

from agentfeeds_runtime.adapters.common import envelope, stable_hash


def _require_macos(stream: dict) -> None:
    if platform.system() != "Darwin":
        raise RuntimeError(f"{stream['id']}: this template requires macOS")


def _osascript(stream: dict, script: str) -> str:
    _require_macos(stream)
    timeout_seconds = int(stream.get("adapter", {}).get("timeout_seconds") or 30)
    result = subprocess.run(["osascript", "-e", script], check=False, text=True, capture_output=True, timeout=timeout_seconds)
    if result.returncode:
        raise RuntimeError(f"{stream['id']}: osascript failed: {result.stderr.strip()}")
    return result.stdout


def _rows(output: str, min_parts: int) -> list[list[str]]:
    rows = []
    pending = ""
    for line in output.splitlines():
        candidate = f"{pending}\n{line}" if pending else line
        parts = candidate.split("\t")
        if len(parts) >= min_parts:
            rows.append(parts)
            pending = ""
        else:
            pending = candidate
    return rows


def _convert(value: object, value_type: str | None) -> object:
    if value == "":
        return None
    if value_type == "boolean":
        return str(value).lower() == "true"
    if value_type == "integer":
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    if value_type == "number":
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
    return value


def _column_name(column: object) -> str:
    return column["name"] if isinstance(column, dict) else str(column)


def _column_type(column: object) -> str | None:
    return column.get("type") if isinstance(column, dict) else None


def _row_data(columns: list[object], values: list[object], static: dict | None = None) -> dict:
    data = dict(static or {})
    for column, value in zip(columns, values, strict=False):
        data[_column_name(column)] = _convert(value, _column_type(column))
    return data


def fetch_apple_automation(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    columns = adapter.get("columns") or []
    if not columns:
        raise ValueError(f"{stream['id']}: adapter.columns is required for apple_automation")
    script = adapter["script"]
    rows = _rows(_osascript(stream, script), len(columns))
    id_column = adapter.get("id_column")
    time_column = adapter.get("time_column")
    static = adapter.get("static") or {}
    events = []
    for row in rows:
        data = _row_data(columns, row, static)
        if stream.get("id") == "mac/notes-recent":
            for key in ("id", "title", "snippet", "modified_at"):
                if key in data and data.get(key) is None:
                    data[key] = ""
        elif stream.get("id") == "mac/mail-unread":
            for key in ("id", "subject", "sender", "received_at"):
                if key in data and data.get(key) is None:
                    data[key] = ""
        event_id = data.get(id_column) if id_column else None
        event_time = data.get(time_column) if time_column else None
        events.append(envelope(stream, stream_uri, event_id or stable_hash(data), data, event_time))
    return events


def _mac_absolute_epoch(value: float) -> str:
    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    dt = datetime(2001, 1, 1, tzinfo=UTC) + timedelta(seconds=float(value))
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _walk_reading_list(node: object) -> list[dict]:
    items = []
    if isinstance(node, dict):
        uri = node.get("URLString")
        extra = node.get("ReadingList") or {}
        if uri and extra:
            items.append(
                {
                    "title": node.get("URIDictionary", {}).get("title") or uri,
                    "url": uri,
                    "added_at": _mac_absolute_epoch(extra["DateAdded"]) if extra.get("DateAdded") else None,
                    "preview_text": extra.get("PreviewText"),
                }
            )
        for value in node.values():
            items.extend(_walk_reading_list(value))
    elif isinstance(node, list):
        for value in node:
            items.extend(_walk_reading_list(value))
    return items


def fetch_plist_reading_list(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    path = Path(adapter["path"]).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"{stream['id']}: Safari bookmarks file not found: {path}")
    payload = plistlib.loads(path.read_bytes())
    items = _walk_reading_list(payload)
    items.sort(key=lambda item: item.get("added_at") or "", reverse=True)
    limit = int(adapter.get("limit") or 50)
    return [envelope(stream, stream_uri, item["url"], item, item.get("added_at")) for item in items[:limit]]


def _convert_sqlite_row(adapter: dict, columns: list[object], row: tuple) -> dict:
    data = _row_data(columns, list(row), adapter.get("static") or {})
    for column, encoding in (adapter.get("timestamp_columns") or {}).items():
        if encoding == "mac_absolute_ns" and data.get(column) is not None:
            data[column] = _mac_absolute_epoch(float(data[column]) / 1_000_000_000)
        elif encoding == "mac_absolute_seconds" and data.get(column) is not None:
            data[column] = _mac_absolute_epoch(float(data[column]))
    return data


def _decode_imessage_attributed_body(value: object) -> str:
    if not isinstance(value, (bytes, bytearray)):
        return ""
    # Messages.app stores many SMS/RCS bodies as NSAttributedString streamtyped
    # blobs, leaving message.text NULL. The readable string is usually embedded
    # as UTF-8 alongside class/archive metadata. Extract candidate printable
    # strings and ignore known archive/class markers.
    ignored = {
        "streamtyped",
        "NSMutableAttributedString",
        "NSAttributedString",
        "NSObject",
        "NSMutableString",
        "NSString",
        "NSDictionary",
        "NSNumber",
        "NSValue",
        "NSMutableData",
        "NSData",
        "NSKeyedArchiver",
    }
    candidates = []
    for match in re.finditer(rb"[\x09\x0a\x0d\x20-\x7e\xc2-\xf4]{4,}", bytes(value)):
        text = match.group(0).decode("utf-8", errors="ignore")
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]+", "", text).strip()
        if not text or text in ignored or text.startswith("__kIM"):
            continue
        candidates.append(text)
    if not candidates:
        return ""
    # Prefer the longest human-readable candidate; archive metadata tends to be
    # short or marker-like, while the message body is usually the longest string.
    return max(candidates, key=len)


def _normalize_imessage_row(data: dict) -> dict:
    if data.get("display_name") is None:
        data["display_name"] = ""
    sender = str(data.get("sender") or "")
    if not data.get("display_name"):
        data["display_name"] = sender
    snippet = data.get("snippet") or _decode_imessage_attributed_body(data.get("attributed_body"))
    data["snippet"] = str(snippet or "")
    data.pop("attributed_body", None)
    if data.get("participants") is None:
        data["participants"] = [sender] if sender else []
    if data.get("unread_count") is None:
        data["unread_count"] = 1
    return data


def fetch_sqlite_query(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    if adapter.get("tcc_permission"):
        _require_macos(stream)
    path = Path(adapter["database"]).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"{stream['id']}: SQLite database not found: {path}")
    columns = adapter.get("columns") or []
    if not columns:
        raise ValueError(f"{stream['id']}: adapter.columns is required for sqlite_query")
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        rows = connection.execute(adapter["query"], adapter.get("params") or []).fetchall()
    finally:
        connection.close()
    id_column = adapter.get("id_column")
    time_column = adapter.get("time_column")
    events = []
    for row in rows:
        data = _convert_sqlite_row(adapter, columns, row)
        if stream.get("id") == "mac/imessage-unread":
            data = _normalize_imessage_row(data)
        if id_column and data.get(id_column) is not None:
            data[id_column] = str(data[id_column])
        event_id = data.get(id_column) if id_column else None
        event_time = data.get(time_column) if time_column else None
        events.append(envelope(stream, stream_uri, event_id or stable_hash(data), data, event_time))
    return events
