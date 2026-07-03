#!/usr/bin/env python3
"""Shopify Asset Curator — extract product images from any Shopify storefront.

Usage:
  python3 curate.py redblossomtea.com --output ./rbt-luxe-assets/
  python3 curate.py origin-9949.myshopify.com --category teas --size grande
  python3 curate.py --stores "store-a.com, store-b.com" --output ./competitor-audit/

No API key required for read-only mode. Optional Admin API token for Strategy A.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.parse
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.request import urlopen, Request

# ── Constants ──────────────────────────────────────────────────────

CDN_PATTERN = re.compile(
    r'(?:https?:)?//cdn\.shopify\.com/s/files/1/\d+/'
    r'(?:products|files|collections)/'
    r'([^"\'?]+?)(?:_\w+)?\.(jpg|jpeg|png|gif|webp)(?:\?v=\d+)?'
)

LIQUID_IMAGE_PATTERN = re.compile(
    r'"featured_image"\s*:\s*"((?:https?:)?//cdn\.shopify\.com[^"]+)"'
)
LIQUID_IMAGES_PATTERN = re.compile(
    r'"images"\s*:\s*\[(.*?)\]'
)
LIQUID_TITLE_PATTERN = re.compile(
    r'"title"\s*:\s*"((?:[^"\\]|\\.)*)"'
)
LIQUID_HANDLE_PATTERN = re.compile(
    r'"handle"\s*:\s*"((?:[^"\\]|\\.)*)"'
)
LIQUID_PRICE_PATTERN = re.compile(
    r'"price"\s*:\s*"((?:[^"\\]|\\.)*)"'
)
LIQUID_VENDOR_PATTERN = re.compile(
    r'"vendor"\s*:\s*"((?:[^"\\]|\\.)*)"'
)
LIQUID_TYPE_PATTERN = re.compile(
    r'"type"\s*:\s*"((?:[^"\\]|\\.)*)"'
)

SIZE_ORDER = {
    "grande": 1200,
    "1024x1024": 1024,
    "large": 600,
    "medium": 300,
    "small": 200,
    "compact": 160,
    "icon": 100,
}
SIZE_KEYS = sorted(SIZE_ORDER, key=lambda k: -SIZE_ORDER[k])

LUXE_WEIGHTS = {
    "resolution": 0.30,
    "diversity": 0.25,
    "rarity": 0.20,
    "visual_quality": 0.15,
    "freshness": 0.10,
}

RARITY_KEYWORDS = [
    "reserve", "limited", "private collection", "aged",
    "vintage", "exclusive", "special edition", "rare",
]

BADGE_OVERLAY_KEYWORDS = [
    "new arrival", "sold out", "coming soon", "sale",
    "best seller", "limited edition", "back in stock",
]

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/json,*/*",
    "Accept-Language": "en-US,en;q=0.9",
}


# ── Data Models ─────────────────────────────────────────────────────


@dataclass
class Product:
    """A Shopify product with image metadata extracted from the storefront."""
    handle: str
    title: str
    price: str = ""
    vendor: str = ""
    product_type: str = ""
    categories: list[str] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    timestamp: int = 0

    @property
    def available_sizes(self) -> set[str]:
        sizes: set[str] = set()
        for img in self.images:
            for suffix in SIZE_KEYS:
                if img.get("url", "").endswith(f"_{suffix}.jpg") or \
                   f"_{suffix}." in img.get("url", ""):
                    sizes.add(suffix)
        return sizes

    @property
    def has_overlay_badge(self) -> bool:
        title_lower = self.title.lower()
        return any(kw in title_lower for kw in BADGE_OVERLAY_KEYWORDS)


@dataclass
class Asset:
    """A single downloaded image asset with metadata."""
    local_path: str
    cdn_url: str
    size: str
    product_title: str
    product_handle: str
    category: str
    alt_text: str
    timestamp: int
    luxe_score: float
    checksum: str = ""


@dataclass
class CurationManifest:
    """Full curation result — product list + scored assets + metadata."""
    store_domain: str
    products: list[Product] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
    category_groups: dict[str, list] = field(default_factory=dict)
    generated_at: str = ""
    total_cdn_urls_found: int = 0
    total_downloaded: int = 0
    errors: list[str] = field(default_factory=list)


# ── Scoring ──────────────────────────────────────────────────────────


def score_resolution(available_sizes: set[str]) -> float:
    """Score 0-1 based on the largest available size suffix."""
    if not available_sizes:
        return 0.0
    for i, sz in enumerate(SIZE_KEYS):
        if sz in available_sizes:
            # grande=1.0, 1024x1024=0.85, large=0.6, medium=0.3, etc.
            return max(0.0, 1.0 - (i * 0.15))
    return 0.1


def score_diversity(categories: list[str]) -> float:
    """Score 0-1 based on number of unique categories."""
    unique = len(set(categories))
    if unique >= 6:
        return 1.0
    return unique / 6.0


def score_rarity(title: str) -> float:
    """Score 0-1 based on rarity keywords in product title."""
    title_lower = title.lower()
    matches = sum(1 for kw in RARITY_KEYWORDS if kw in title_lower)
    return min(1.0, matches * 0.33)


def score_visual_quality(product: Product) -> float:
    """Score 0-1. Penalize overlay badges, prefer clean hero shots."""
    if product.has_overlay_badge:
        return 0.3
    if not product.images:
        return 0.0
    return 0.9  # default for clean images


def score_freshness(timestamp: int, baseline_ts: int | None = None) -> float:
    """Score 0-1 based on recency of the ?v= timestamp."""
    if not timestamp:
        return 0.5  # unknown = neutral
    now = int(time.time())
    ninety_days = 90 * 86400
    one_year = 365 * 86400
    age = now - timestamp
    if baseline_ts:
        age = now - baseline_ts  # freshness relative to baseline
    if age <= ninety_days:
        return 1.0
    elif age <= one_year:
        return 0.5
    return 0.0


def compute_luxe_score(product: Product, baseline_ts: int | None = None) -> float:
    """Compute the composite Luxe Score for a product."""
    scores = {
        "resolution": score_resolution(product.available_sizes),
        "diversity": score_diversity(product.categories),
        "rarity": score_rarity(product.title),
        "visual_quality": score_visual_quality(product),
        "freshness": score_freshness(product.timestamp, baseline_ts),
    }
    return sum(scores[k] * LUXE_WEIGHTS[k] for k in LUXE_WEIGHTS)


# ── Storefront Discovery ─────────────────────────────────────────────


def _http_get(url: str, headers: dict | None = None) -> str:
    """Fetch a URL with error handling."""
    req = Request(url, headers=headers or DEFAULT_HEADERS)
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        raise RuntimeError(f"HTTP {url}: {e}")


async def discover_products_strategy_b(
    domain: str,
    category: str = "all",
) -> list[Product]:
    """Discover products via public storefront scraping (Strategy B).

    Scrapes collection pages, parses embedded Liquid JSON for product
    handles, titles, and CDN image URLs.
    """
    products: dict[str, Product] = {}
    base_url = f"https://{domain}"

    # Build collection URLs to try
    collections = _get_collection_urls(base_url, category)
    seen_handles: set[str] = set()

    for col_url in collections:
        try:
            html = _http_get(col_url)
        except RuntimeError:
            continue

        # Extract product handles from collection page
        handles = _extract_handles(html)
        if not handles:
            # Try product grid selectors
            handles = _extract_handles_fallback(html, base_url)

        for handle in handles:
            if handle in seen_handles:
                continue
            seen_handles.add(handle)

            # Scrape individual product page for full details
            product = await _scrape_product_page(base_url, handle)
            if product and product.images:
                products[handle] = product

        # Check pagination
        next_url = _get_next_page(html, base_url)
        if next_url and len(products) < 500:
            try:
                next_html = _http_get(next_url)
                more_handles = _extract_handles(next_html)
                for handle in more_handles:
                    if handle not in seen_handles:
                        seen_handles.add(handle)
                        product = await _scrape_product_page(base_url, handle)
                        if product and product.images:
                            products[handle] = product
            except RuntimeError:
                pass

    return list(products.values())


def _get_collection_urls(base_url: str, category: str) -> list[str]:
    """Determine which collection URLs to scrape."""
    if category and category != "all":
        return [f"{base_url}/collections/{category}"]
    # Try common collection handles
    candidates = ["all", "all-products", "products", "shop"]
    return [f"{base_url}/collections/{c}" for c in candidates]


def _extract_handles(html: str) -> list[str]:
    """Extract product handles from collection page HTML."""
    handles: list[str] = []

    # Try embedded JSON
    for m in LIQUID_HANDLE_PATTERN.finditer(html):
        h = m.group(1)
        if h and h not in handles:
            handles.append(h)

    # Try /products/ URL patterns
    url_pattern = re.findall(
        r'/products/([a-zA-Z0-9_-]+)',
        html,
    )
    for u in url_pattern:
        if u not in handles:
            handles.append(u)

    return handles


def _extract_handles_fallback(html: str, base_url: str) -> list[str]:
    """Fallback: extract handles from link elements and product-grid classes."""
    handles: list[str] = []
    # product-card / product-item links
    for m in re.finditer(
        r'href=["\']/products/([a-zA-Z0-9_-]+)["\']',
        html,
    ):
        h = m.group(1)
        if h not in handles:
            handles.append(h)
    return handles


def _get_next_page(html: str, base_url: str) -> str | None:
    """Check for pagination and return the next page URL."""
    # Shopify uses ?page=N
    current = re.search(r'page=(\d+)', html)
    if current:
        next_page = int(current.group(1)) + 1
        return f"{base_url}/collections/all?page={next_page}"
    # Check for "next" link
    if "Next" in html or "next" in html:
        # Common pattern: data-page="1" data-next-url
        next_url_match = re.search(r'data-next-url=["\']([^"\']+)', html)
        if next_url_match:
            url = next_url_match.group(1)
            if url.startswith("/"):
                return base_url + url
            return url
    return None


async def _scrape_product_page(base_url: str, handle: str) -> Product | None:
    """Scrape a single product page for full image info."""
    url = f"{base_url}/products/{handle}"
    try:
        html = _http_get(url)
    except RuntimeError:
        return None

    title = _first_match(LIQUID_TITLE_PATTERN, html) or handle.replace("-", " ").title()

    # Extract CDN image URLs
    images: list[dict] = []
    seen_urls: set[str] = set()

    # Primary: featured_image
    for m in CDN_PATTERN.finditer(html):
        full_url = m.group(0)
        if full_url not in seen_urls:
            seen_urls.add(full_url)
            images.append({"url": full_url})

    # Secondary: parse ["images"] JSON array
    for m in LIQUID_IMAGES_PATTERN.finditer(html):
        raw = m.group(1)
        # Extract individual quoted URLs
        for url_m in re.finditer(r'"((?:https?:)?//cdn\.shopify\.com[^"]+)"', raw):
            img_url = url_m.group(1)
            if img_url not in seen_urls and CDN_PATTERN.match(img_url):
                seen_urls.add(img_url)
                images.append({"url": img_url})

    if not images:
        return None

    # Extract timestamps from URLs
    timestamp = 0
    for img in images:
        ts_match = re.search(r'v=(\d+)', img["url"])
        if ts_match:
            ts = int(ts_match.group(1))
            if ts > timestamp:
                timestamp = ts

    price = _first_match(LIQUID_PRICE_PATTERN, html) or ""
    vendor = _first_match(LIQUID_VENDOR_PATTERN, html) or ""
    ptype = _first_match(LIQUID_TYPE_PATTERN, html) or ""

    return Product(
        handle=handle,
        title=title,
        price=price,
        vendor=vendor,
        product_type=ptype,
        images=images,
        timestamp=timestamp,
    )


def _first_match(pattern: re.Pattern, text: str) -> str | None:
    m = pattern.search(text)
    return m.group(1) if m else None


# ── Adaptive Mode: Compare manifests ─────────────────────────────────


def load_manifest(path: str) -> list[Asset]:
    """Load a prior manifest for adaptive/timestamp comparison."""
    with open(path) as f:
        data = json.load(f)
    return [Asset(**a) for a in data]


def filter_updated_products(
    products: list[Product],
    baseline_assets: list[Asset],
) -> list[Product]:
    """Return only products with newer timestamps than baseline."""
    baseline_ts: dict[str, int] = {}
    for a in baseline_assets:
        existing = baseline_ts.get(a.product_handle, 0)
        if a.timestamp > existing:
            baseline_ts[a.product_handle] = a.timestamp

    updated: list[Product] = []
    for p in products:
        prev_ts = baseline_ts.get(p.handle, 0)
        if p.timestamp > prev_ts:
            updated.append(p)
    return updated


# ── Curation ─────────────────────────────────────────────────────────


def curate_products(
    products: list[Product],
    min_score: float = 0.50,
    top_n: int = 40,
    include_all: bool = False,
    category_focus: str | None = None,
) -> list[Product]:
    """Score and rank products by Luxe Score, return curated subset."""
    if not products:
        return []

    scored: list[tuple[float, Product]] = []
    for p in products:
        score = compute_luxe_score(p)
        # Boost diversity weight if category focus is set
        if category_focus and _in_category(p, category_focus):
            score += 0.10
        scored.append((score, p))

    scored.sort(key=lambda x: -x[0])

    if include_all:
        return [p for _, p in scored]

    # Filter by min_score
    candidates = [(s, p) for s, p in scored if s >= min_score]
    if not candidates:
        # Fallback: return top N even if below min_score
        candidates = scored[:top_n]

    # Ensure category diversity (max N per category to avoid monoculture)
    per_category: dict[str, int] = defaultdict(int)
    max_per_category = max(2, top_n // 6)
    result: list[Product] = []

    for score, product in candidates:
        if len(result) >= top_n:
            break
        cat = _infer_category(product)
        if per_category[cat] >= max_per_category:
            continue
        # Tag score for later reference
        product.categories = list(set(product.categories + [cat]))
        result.append(product)
        per_category[cat] += 1

    return result


def _infer_category(product: Product) -> str:
    """Infer category from product type, vendor, or title."""
    pt = product.product_type.lower()
    vendor = product.vendor.lower()
    title = product.title.lower()

    # Type-based
    if "tea" in pt:
        for kw in ["green", "white", "oolong", "black", "pu-erh", "pu'er",
                     "herbal", "tisane", "jasmine", "matcha", "chai"]:
            if kw in pt:
                return f"teas-{kw}"
        return "teas"
    if "teaware" in pt or "pot" in pt or "cup" in pt or "gaiwan" in pt:
        for kw in ["glass", "porcelain", "yixing", "ceramic", "clay"]:
            if kw in pt or kw in title:
                return f"teaware-{kw}"
        return "teaware"
    if "gift" in pt or "set" in pt or "collection" in pt:
        return "gifts-collections"
    if "banner" in pt or "homepage" in pt:
        return "banners"
    if "logo" in pt or "brand" in pt:
        return "brand"

    # Title-based fallback
    for kw in ["green", "white", "oolong", "black", "pu-erh", "pu'er",
                 "herbal", "tisane", "jasmine", "matcha", "chai"]:
        if kw in title:
            return f"teas-{kw}"
    return "miscellaneous"


def _in_category(product: Product, category_focus: str) -> bool:
    """Check if a product belongs to the focused category."""
    cat = _infer_category(product)
    return category_focus.lower() in cat


# ── Download & Build ──────────────────────────────────────────────────


def build_asset_list(
    products: list[Product],
    store_domain: str,
    size: str = "grande",
    min_resolution: int = 0,
) -> list[Asset]:
    """Build the full list of assets to download (before download)."""
    assets: list[Asset] = []
    domain_slug = store_domain.replace("https://", "").replace("/", "").split(".")[0]

    for product in products:
        cat = _infer_category(product)
        score = compute_luxe_score(product)
        target_size = size if size in SIZE_ORDER else "grande"
        selected_images = _select_images(product, target_size, min_resolution)

        for img in selected_images:
            alt_text = _generate_alt_text(product, store_domain)
            assets.append(Asset(
                local_path=f"{cat}/{product.handle}_{img['size']}.jpg",
                cdn_url=img["url"],
                size=img["size"],
                product_title=product.title,
                product_handle=product.handle,
                category=cat,
                alt_text=alt_text,
                timestamp=product.timestamp,
                luxe_score=round(score, 2),
            ))
    return assets


def _select_images(
    product: Product,
    target_size: str,
    min_resolution: int,
) -> list[dict]:
    """Select best-resolution images for download."""
    selected: list[dict] = []
    target_idx = SIZE_KEYS.index(target_size) if target_size in SIZE_KEYS else 0

    for img in product.images:
        url = img["url"]
        # Try exact target size first, then fall back to smaller
        chosen_url = url
        chosen_size = "unknown"
        for sz in SIZE_KEYS:
            suffix = f"_{sz}."
            if suffix in url or url.endswith(f"_{sz}.jpg"):
                sz_idx = SIZE_KEYS.index(sz)
                if sz_idx <= target_idx:  # allowed by min_resolution
                    chosen_url = url
                    chosen_size = sz
                    break

        if min_resolution > 0:
            known_px = SIZE_ORDER.get(chosen_size, 0)
            if known_px and known_px < min_resolution:
                continue

        selected.append({"url": chosen_url, "size": chosen_size})

    return selected[:3]  # max 3 images per product (hero + 2 alternate)


def _generate_alt_text(product: Product, domain: str) -> str:
    """Generate AEO-optimized alt text."""
    brand = domain.replace("https://", "").replace("www.", "").split(".")[0]
    brand_title = brand.replace("-", " ").title()
    return f"{product.title} | {brand_title}"


def _size_from_url(url: str) -> str:
    """Extract size suffix from CDN URL."""
    for sz in SIZE_KEYS:
        if f"_{sz}." in url:
            return sz
    return "unknown"


async def download_asset(
    asset: Asset,
    output_dir: Path,
    existing_checksums: set[str] | None = None,
) -> bool:
    """Download a single asset. Returns True on success."""
    dest = output_dir / asset.local_path
    if dest.exists():
        return True  # already downloaded

    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        req = Request(asset.cdn_url, headers=DEFAULT_HEADERS)
        with urlopen(req, timeout=30) as resp:
            data = resp.read()

        # Compute checksum for dedup
        checksum = hashlib.sha256(data).hexdigest()
        if existing_checksums and checksum in existing_checksums:
            return False  # duplicate content, skip

        dest.write_bytes(data)
        asset.checksum = checksum
        return True
    except Exception as e:
        return False


def _generate_download_script(
    assets: list[Asset],
    output_dir: str,
) -> str:
    """Generate a standalone bash script for reproducible re-download."""
    lines = [
        "#!/usr/bin/env bash",
        "# Reproducible download script — generated by Shopify Asset Curator",
        f"# {len(assets)} assets",
        f"# Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "set -euo pipefail",
        "mkdir -p {category_dir}",
        "",
    ]
    seen_categories: set[str] = set()
    for asset in assets:
        if asset.category not in seen_categories:
            lines.append(f'mkdir -p "${{OUTDIR:-.}}/{asset.category}"')
            seen_categories.add(asset.category)

    for asset in assets:
        escaped_url = asset.cdn_url.replace('"', '\\"')
        lines.append(
            f'curl -sfL "{escaped_url}" -o "${{OUTDIR:-.}}/{asset.local_path}"'
        )

    lines.extend([
        "",
        'echo "Downloaded {len(assets)} assets to ${OUTDIR:-.}"',
    ])
    return "\n".join(lines)


def _write_manifest(assets: list[Asset], output_dir: Path) -> None:
    """Write manifest.json with all asset metadata."""
    manifest_data = []
    for a in assets:
        manifest_data.append(asdict(a))
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=2, default=str)


def _write_csv(assets: list[Asset], output_dir: Path) -> None:
    """Write CSV import file for CMS/PIM bulk upload."""
    csv_path = output_dir / "assets.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "local_path", "cdn_url", "size", "product_title",
            "product_handle", "category", "alt_text", "luxe_score",
        ])
        for a in assets:
            writer.writerow([
                a.local_path, a.cdn_url, a.size, a.product_title,
                a.product_handle, a.category, a.alt_text, a.luxe_score,
            ])


def _build_zip(output_dir: Path, archive_name: str) -> str:
    """Create ZIP archive of the output directory."""
    archive_path = shutil.make_archive(
        archive_name.replace(".zip", ""),
        "zip",
        output_dir,
    )
    return archive_path


# ── Multi-Store Comparison ───────────────────────────────────────────


def compare_stores(store_results: dict[str, CurationManifest]) -> dict:
    """Compare multiple store curations for competitive intelligence."""
    report: dict = {
        "stores": {},
        "coverage_gaps": {},
        "shared_checksums": [],
        "asset_density": {},
    }

    all_checksums: dict[str, str] = {}  # checksum -> store
    for domain, manifest in store_results.items():
        store_slug = domain.replace("https://", "").split(".")[0]
        category_counts: dict[str, int] = defaultdict(int)
        for a in manifest.assets:
            category_counts[a.category] += 1

            # Track checksums for shared-supplier detection
            if a.checksum:
                if a.checksum in all_checksums:
                    report["shared_checksums"].append({
                        "checksum": a.checksum,
                        "stores": [all_checksums[a.checksum], store_slug],
                        "product": a.product_title,
                    })
                else:
                    all_checksums[a.checksum] = store_slug

        avg_luxe = (
            sum(a.luxe_score for a in manifest.assets) / len(manifest.assets)
            if manifest.assets else 0
        )

        report["stores"][store_slug] = {
            "total_assets": len(manifest.assets),
            "categories": list(category_counts.keys()),
            "category_counts": dict(category_counts),
            "avg_luxe_score": round(avg_luxe, 2),
            "products_discovered": len(manifest.products),
        }
        report["asset_density"][store_slug] = {
            "images_per_product": round(
                len(manifest.assets) / max(len(manifest.products), 1), 1
            ),
        }

    return report


def _format_compare_report(report: dict) -> str:
    """Format comparison report as markdown."""
    lines = ["# Store Comparison Report", ""]
    for slug, data in report.get("stores", {}).items():
        lines.extend([
            f"## {slug}",
            f"- Assets: {data['total_assets']}",
            f"- Categories: {', '.join(data['categories'])}",
            f"- Avg Luxe Score: {data['avg_luxe_score']}",
            f"- Products discovered: {data['products_discovered']}",
            "",
        ])
    if report.get("shared_checksums"):
        lines.extend([
            "## Shared Suppliers Detected",
            f"- {len(report['shared_checksums'])} matching checksums across stores",
            "",
        ])
    return "\n".join(lines)


# ── Main Orchestration ────────────────────────────────────────────────


async def curate_store(
    domain: str,
    category: str = "all",
    size: str = "grande",
    output_dir: str | None = None,
    min_score: float = 0.50,
    top_n: int = 40,
    include_all: bool = False,
    depth: str = "shallow",
    min_resolution: int = 0,
    adaptive: bool = False,
    baseline_manifest: str | None = None,
    category_focus: str | None = None,
    admin_token: str | None = None,
) -> CurationManifest:
    """Run the full curation pipeline for a single store."""
    domain = domain.replace("https://", "").replace("http://", "").strip("/")
    domain_slug = domain.split(".")[0]
    out_dir = Path(output_dir or f"./{domain_slug}-luxe-assets")

    manifest = CurationManifest(
        store_domain=domain,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    print(f"[discover] {domain} (category: {category})")

    # Step 1: Discover
    if admin_token:
        print(f"[discover] Using Strategy A (Admin API)")
        products = await _discover_via_api(domain, admin_token, category)
    else:
        print(f"[discover] Using Strategy B (scrape)")
        products = await discover_products_strategy_b(domain, category)

    if not products:
        print("[discover] No products found")
        manifest.errors.append("No products discovered")
        return manifest

    manifest.products = products
    print(f"[discover] {len(products)} products, " +
          f"{sum(len(p.images) for p in products)} CDN URLs")

    # Adaptive: filter to updated only
    if adaptive and baseline_manifest:
        baseline = load_manifest(baseline_manifest)
        products = filter_updated_products(products, baseline)
        print(f"[adaptive] {len(products)} products updated since baseline")

    # Step 2: Curate
    curated = curate_products(
        products,
        min_score=min_score,
        top_n=top_n,
        include_all=include_all,
        category_focus=category_focus,
    )
    print(f"[curate] {len(curated)} products pass luxe score >= {min_score}")

    # Step 3: Build asset list
    assets = build_asset_list(curated, domain, size=size, min_resolution=min_resolution)
    manifest.category_groups = _group_by_category(assets)
    manifest.total_cdn_urls_found = len(assets)

    # Step 4: Download
    out_dir.mkdir(parents=True, exist_ok=True)
    existing_checksums: set[str] = set()
    if baseline_manifest:
        baseline = load_manifest(baseline_manifest)
        existing_checksums = {a.checksum for a in baseline if a.checksum}

    download_count = 0
    for asset in assets:
        success = await download_asset(asset, out_dir, existing_checksums)
        if success:
            download_count += 1

    manifest.total_downloaded = download_count
    print(f"[download] {download_count}/{len(assets)} assets OK")

    # Step 5: Write outputs
    manifest.assets = assets
    _write_manifest(assets, out_dir)
    _write_csv(assets, out_dir)

    script = _generate_download_script(assets, str(out_dir))
    script_path = out_dir / "download.sh"
    script_path.write_text(script)
    script_path.chmod(0o755)

    # ZIP
    archive_path = _build_zip(out_dir, str(out_dir))
    print(f"[output] {archive_path}")
    print(f"[output] {out_dir / 'manifest.json'}")
    print(f"[output] {out_dir / 'download.sh'}")
    print(f"[output] {out_dir / 'assets.csv'}")

    return manifest


async def _discover_via_api(
    domain: str,
    token: str,
    category: str = "all",
) -> list[Product]:
    """Discover products via Shopify Admin API (Strategy A)."""
    base_url = f"https://{domain}/admin/api/2026-04"
    headers = {
        **DEFAULT_HEADERS,
        "X-Shopify-Access-Token": token,
    }
    products: list[Product] = []
    url = f"{base_url}/products.json?fields=id,title,handle,images,product_type,vendor&limit=250"
    if category and category != "all":
        url += f"&collection_id={category}"

    while url:
        try:
            html = _http_get(url, headers)
            data = json.loads(html)
        except (RuntimeError, json.JSONDecodeError) as e:
            break

        for item in data.get("products", []):
            images = []
            for img in item.get("images", []):
                src = img.get("src", "")
                if src and CDN_PATTERN.match(src):
                    images.append({"url": src})

            products.append(Product(
                handle=item.get("handle", ""),
                title=item.get("title", ""),
                product_type=item.get("product_type", ""),
                vendor=item.get("vendor", ""),
                images=images,
            ))

        # Paginate
        link_header = ""  # would come from response headers in real HTTP
        next_url_match = re.search(r'<([^>]+)>;\s*rel="next"', html)
        url = next_url_match.group(1) if next_url_match else None

    return products


def _group_by_category(assets: list[Asset]) -> dict[str, list]:
    groups: dict[str, list] = defaultdict(list)
    for a in assets:
        groups[a.category].append(a.product_title)
    return dict(groups)


# ── CLI ──────────────────────────────────────────────────────────────


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Shopify Asset Curator — extract product images from any Shopify storefront",
    )
    parser.add_argument(
        "store", nargs="?",
        help="Shopify store domain (e.g. redblossomtea.com)",
    )
    parser.add_argument("--category", default="all", help="Category focus")
    parser.add_argument("--size", default="grande", choices=list(SIZE_ORDER.keys()),
                       help="Target image resolution")
    parser.add_argument("--depth", default="shallow", choices=["shallow", "deep"],
                       help="Image depth: shallow (hero) vs deep (all variants)")
    parser.add_argument("--min-score", type=float, default=0.50,
                       help="Minimum Luxe Score (0-1)")
    parser.add_argument("--top-products", type=int, default=40,
                       help="Maximum curated products")
    parser.add_argument("--include-all", action="store_true",
                       help="Bypass scoring, include everything")
    parser.add_argument("--min-resolution", type=int, default=0,
                       help="Minimum image dimension in pixels")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--adaptive", action="store_true",
                       help="Incremental mode: only fetch updated items")
    parser.add_argument("--baseline-manifest",
                       help="Prior manifest for adaptive mode / dedup")
    parser.add_argument("--category-focus",
                       help="Boost diversity weight for a specific category")
    parser.add_argument("--admin-token",
                       help="Shopify Admin API token (Strategy A)")
    parser.add_argument("--stores",
                       help="Comma-separated domains for multi-store comparison")
    parser.add_argument("--no-download", action="store_true",
                       help="Generate manifest without downloading")
    return parser.parse_args(argv)


async def main() -> None:
    args = parse_args()
    start = time.time()

    if args.stores:
        # Multi-store comparison mode
        domains = [d.strip() for d in args.stores.split(",")]
        results: dict[str, CurationManifest] = {}
        for domain in domains:
            manifest = await curate_store(
                domain,
                category=args.category,
                size=args.size,
                output_dir=args.output,
                min_score=args.min_score,
                top_n=args.top_products,
                include_all=args.include_all,
                min_resolution=args.min_resolution,
                adaptive=args.adaptive,
                baseline_manifest=args.baseline_manifest,
                category_focus=args.category_focus,
                admin_token=args.admin_token,
            )
            results[domain] = manifest

        report = compare_stores(results)
        report_md = _format_compare_report(report)
        out_path = Path(args.output or ".") / "comparison-report.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report_md)
        print(f"[compare] Report: {out_path}")
        return

    if not args.store:
        print("Error: either --stores or a store domain argument is required")
        sys.exit(1)

    manifest = await curate_store(
        args.store,
        category=args.category,
        size=args.size,
        output_dir=args.output,
        min_score=args.min_score,
        top_n=args.top_products,
        include_all=args.include_all,
        min_resolution=args.min_resolution,
        adaptive=args.adaptive,
        baseline_manifest=args.baseline_manifest,
        category_focus=args.category_focus,
        admin_token=args.admin_token,
    )

    elapsed = time.time() - start
    print(f"\n[done] {elapsed:.1f}s — {manifest.total_downloaded} assets")

    if manifest.errors:
        print(f"[errors] {len(manifest.errors)}")
        for err in manifest.errors:
            print(f"  ! {err}")


if __name__ == "__main__":
    asyncio.run(main())
