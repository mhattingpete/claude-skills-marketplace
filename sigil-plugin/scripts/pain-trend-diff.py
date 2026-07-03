#!/usr/bin/env python3
"""pain-trend-diff.py — Trend differ for Reddit Pain Researcher state files.

Compares consecutive runs in reddit-pain-state.json and outputs structured
diff: persistent pains, new pains, resolved pains, and readiness changes.

Usage:
  python3 pain-trend-diff.py <state-file> [--markdown] [--json]

Examples:
  python3 pain-trend-diff.py reddit-pain-state.json --markdown
  python3 pain-trend-diff.py reddit-pain-state.json --json
"""
import json
import sys
import os
from datetime import datetime


def load_state(path):
    with open(path) as f:
        return json.load(f)


def find_pain(pains_dict, pain_id):
    return pains_dict.get(pain_id)


def compute_diff(state, run_range=None):
    """Compare consecutive runs and return structured diff.

    Args:
        state: The loaded state dict.
        run_range: Optional tuple (start_run_id, end_run_id) to diff specific runs.
                   If None, diffs the last two runs.
    """
    runs = state.get("runs", [])
    if len(runs) < 2:
        return {
            "status": "single_run",
            "total_runs": len(runs),
            "message": "Only one run available. No trends to compute yet."
        }

    # Get pains from state
    all_pains = {p["id"]: p for p in state.get("pains", [])}

    # Use state's trend tracking as authoritative
    trends = state.get("trends", {})

    persistent = trends.get("persistent_pains", [])
    new_pains = trends.get("new_pains", [])
    resolved = trends.get("resolved_pains", [])
    readiness_changes = trends.get("automation_readiness_changes", [])

    # Enrich with full pain data
    enriched_persistent = []
    for p in persistent:
        full = find_pain(all_pains, p["id"])
        if full:
            enriched_persistent.append({**p, **full})
        else:
            enriched_persistent.append(p)

    enriched_new = []
    for p in new_pains:
        full = find_pain(all_pains, p["id"])
        if full:
            enriched_new.append({**p, **full})
        else:
            enriched_new.append(p)

    enriched_resolved = []
    for p in resolved:
        enriched_resolved.append(p)

    # Compute aggregate stats
    total_pains = len(all_pains)
    persistent_count = len(enriched_persistent)
    new_count = len(enriched_new)
    resolved_count = len(enriched_resolved)

    # Count changes in automation potential
    readiness_summary = {}
    for c in readiness_changes:
        label = c.get("label", "unknown")
        change = c.get("change", 0)
        readiness_summary[label] = readiness_summary.get(label, 0) + change

    # Generate trend signals
    signals = []
    if persistent_count > 0:
        unaddressed = [p["name"] for p in enriched_persistent if p.get("automation_potential", "").startswith("VERY")]
        if unaddressed:
            signals.append(f"{len(unaddressed)} high-value pains persist across runs: {', '.join(unaddressed[:3])}")

    if new_count > 0:
        high_value_new = [p["name"] for p in enriched_new if p.get("automation_potential", "").startswith("HIGH") or p.get("automation_potential", "").startswith("VERY")]
        if high_value_new:
            signals.append(f"{len(high_value_new)} new high-value opportunities: {', '.join(high_value_new[:3])}")

    if resolved_count > 0:
        signals.append(f"{resolved_count} pains no longer trending (possibly solved or fading)")

    return {
        "status": "trends_available",
        "total_runs": len(runs),
        "last_run": runs[-1]["date"],
        "previous_run": runs[-2]["date"] if len(runs) >= 2 else None,
        "total_pains": total_pains,
        "persistent": {
            "count": persistent_count,
            "pains": enriched_persistent
        },
        "new": {
            "count": new_count,
            "pains": enriched_new
        },
        "resolved": {
            "count": resolved_count,
            "pains": enriched_resolved
        },
        "readiness_changes": readiness_summary,
        "signals": signals
    }


def format_markdown(diff):
    """Format diff as markdown report."""
    if diff["status"] == "single_run":
        return f"""# Pain Trends — {diff['total_runs']} Run(s)

Only {diff['total_runs']} run{'s' if diff['total_runs'] > 1 else ''} available. Run the research at least twice to see trends.

```json
{diff['message']}
```
"""
    total = diff["total_pains"]
    persistent = diff["persistent"]["count"]
    new_count = diff["new"]["count"]
    resolved_count = diff["resolved"]["count"]
    last = diff["last_run"]
    prev = diff["previous_run"]

    lines = [
        f"# Pain Trends — {prev} to {last}",
        "",
        f"**Total tracked pains:** {total}",
        f"**Runs so far:** {diff['total_runs']}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Persistent pains (seen 2+ runs) | {persistent} |",
        f"| New pains (first seen this run) | {new_count} |",
        f"| Resolved/vanished pains | {resolved_count} |",
        f"| **Net change** | **+{new_count - resolved_count}** |",
        "",
    ]

    if diff["signals"]:
        lines.append("### Signals")
        lines.append("")
        for s in diff["signals"]:
            lines.append(f"- {s}")
        lines.append("")

    if persistent > 0:
        lines.append("## Persistent Pains")
        lines.append("")
        lines.append("| Pain | Last Seen | Automation Potential |")
        lines.append("|------|-----------|---------------------|")
        for p in diff["persistent"]["pains"]:
            lines.append(f"| {p['name']} | {p.get('last_seen', '?')} | {p.get('automation_potential', '?')} |")
        lines.append("")

    if new_count > 0:
        lines.append("## New Pains (Emerging)")
        lines.append("")
        lines.append("| Pain | Automation Potential | Approach |")
        lines.append("|------|---------------------|----------|")
        for p in diff["new"]["pains"]:
            pot = p.get("automation_potential", "?")
            approach = p.get("automation_approach", "")
            if len(approach) > 80:
                approach = approach[:77] + "..."
            lines.append(f"| {p['name']} | {pot} | {approach} |")
        lines.append("")

    if resolved_count > 0:
        lines.append("## Resolved / Vanished Pains")
        lines.append("")
        for p in diff["resolved"]["pains"]:
            lines.append(f"- {p.get('name', p.get('id', '?'))}")
        lines.append("")

    if diff["readiness_changes"]:
        lines.append("## Automation Readiness Shifts")
        lines.append("")
        for label, change in diff["readiness_changes"].items():
            direction = "increased" if change > 0 else "decreased"
            lines.append(f"- **{label}**: readiness {direction} by {abs(change)}")
        lines.append("")

    lines.append("---")
    lines.append(f"*Generated by pain-trend-diff.py on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    return "\n".join(lines)


def format_json(diff):
    """Format diff as JSON."""
    return json.dumps(diff, indent=2)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <state-file> [--markdown] [--json]", file=sys.stderr)
        sys.exit(2)

    state_path = sys.argv[1]
    output_format = "markdown"  # default

    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--markdown":
            output_format = "markdown"
        elif arg == "--json":
            output_format = "json"

    if not os.path.exists(state_path):
        print(f"Error: state file not found: {state_path}", file=sys.stderr)
        sys.exit(1)

    state = load_state(state_path)
    diff = compute_diff(state)

    if output_format == "json":
        print(format_json(diff))
    else:
        print(format_markdown(diff))


if __name__ == "__main__":
    main()
