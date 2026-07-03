---
name: "shopify-asset-curator"
description: "Generate a brand-grade, category-diverse image asset library from any Shopify storefront — no API key required. Activates when users want to curate product images, build an asset library, download Shopify product photos, gather competitor imagery, extract high-res images, or generate image manifests. Includes Luxe Score ranking, adaptive re-scraping, multi-store comparison, and AEO-optimized alt-text generation."
license: MIT
metadata:
  tier: "STANDARD"
  category: "E-commerce / Asset Management"
  cert: "sigil-pass-with-concerns"
  cert_expires: "2026-09-28"
---

# Shopify Luxury Product Asset Curator

Generate a brand-grade, category-diverse image asset library from any Shopify storefront — no API key required.

## Purpose
Extract, curate, and organize high-resolution product images from any Shopify store into a taxonomically structured, marketplace-ready asset pack. Bypasses search-engine noise, watermark risk, and stale thumbnails by pulling directly from the Shopify CDN.

## When to Use

**Activation phrases:**
- "curate product images from {store}"
- "build an asset library for {store}"
- "download Shopify product photos for {category}"
- "gather competitor product imagery"
- "extract high-res images from {domain}"
- "generate image manifest for {store}"

**Good for:**
- Building brand-consistent image banks for marketing and social content
- Generating competitor analysis visual decks (multi-store comparison mode)
- Feeding AI image-generation pipelines with reference-grade product photography
- Creating localized asset packs for Xiaohongshu / RedNote / Instagram / TikTok Shop
- Prepping product imagery before a store redesign or replatforming

## Process

### Step 1: Discovery — Map the Store Catalog

Extract product handles and CDN image URLs from the storefront. Two strategies, tried in order:

**Strategy A — API-backed (preferred):**
If the store has Shopify Admin API access available (OAuth client credentials or existing token), use `GET /admin/api/2026-04/products.json?fields=id,title,handle,images` — returns structured JSON with all CDN URLs, multi-angle variants, and timestamp metadata. Supports `since_id` pagination for stores >250 SKUs.

**Strategy B — Read-only scrape (fallback):**
No API key available. Scrape public collection pages and product pages:
```
GET /collections/all
GET /collections/{category-handle}
GET /products/{product-handle}
```
Parse embedded `featured_image` and `images` JSON arrays from Shopify liquid templates:
```
"featured_image":"//cdn.shopify.com/s/files/..._{SIZE}.jpg?v={TIMESTAMP}"
"images":["//cdn.shopify.com/s/files/..._{SIZE}.jpg?v={TIMESTAMP}"]
```

**Adaptive mode (`adaptive=True`):**
On re-run, compare `?v=` timestamps against the previous manifest. Only fetch products with newer timestamps — skips unchanged items entirely. Pass `baseline_manifest` to enable.

**Output:** `{store-slug}-raw-manifest.json` — full product list with handles, titles, image arrays, and timestamp metadata.

### Step 2: Curation — Filter & Rank by Luxe Score

Apply a 5-factor scoring heuristic to surface the most brand-representative assets. Each factor is independently scored 0–1, then composited by weight:

| Factor | Weight | Detection method |
|--------|--------|-----------------|
| Resolution | 0.30 | Available size suffixes present (`grande` > `large` > `medium`) |
| Category diversity | 0.25 | Unique collection/category tags across the selected set |
| Rarity | 0.20 | Title keywords: "Reserve", "Limited", "Private Collection", "Aged", "Vintage" |
| Visual quality | 0.15 | Badge detection: skip images with overlay text ("NEW ARRIVAL", "SOLD OUT") unless explicitly requested; prefer clean hero shots |
| Freshness | 0.10 | Timestamp recency: `?v=` within last 90d = 1.0, within 1y = 0.5, older = 0.0 |

**Implementation:**
```python
def luxe_score(product: dict, baseline_ts: int = None) -> float:
    scores = {
        "resolution": score_resolution(product["sizes"]),
        "diversity": score_diversity(product.get("categories", [])),
        "rarity": score_rarity(product["title"]),
        "visual_quality": score_visual_quality(product.get("badges", [])),
        "freshness": score_freshness(product.get("timestamp"), baseline_ts),
    }
    return sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
```

**User overrides:**
- `--min-score N`: only include products with luxe_score >= N/100 (default 50)
- `--top-products N`: limit output to top N by score
- `--include-all`: bypass scoring, include every product at least one size
- `--category-focus <type>`: boost diversity weight for a specific category

Default: top 40–60 assets spanning ≥6 category groups.

### Step 3: Extraction — Build CDN URL Manifest

Shopify CDN URL anatomy:
```
https://cdn.shopify.com/s/files/1/{STORE_ID}/
  products/{FILENAME}_{SIZE}.jpg?v={TIMESTAMP}     # Product images
  files/{FILENAME}_{SIZE}.jpg?v={TIMESTAMP}         # Uploaded files (newer stores)
  collections/{FILENAME}_{SIZE}.jpg?v={TIMESTAMP}   # Collection banners
  t/{THEME_ID}/assets/{FILENAME}.png?v={TIMESTAMP}  # Theme assets (logos, banners)
```

**Size suffixes** (priority-ordered for download): `_grande` (1200x1200) > `_1024x1024` > `_large` > `_medium` > `_small` > `_compact` > `_icon`

When `min_resolution` is specified, compare known size suffixes against the threshold:
- `grande` → 1200px (default, best quality)
- `1024x1024` → 1024px
- `large` → 600px
- `medium` → 300px
- `small` → 200px
- `compact` → 160px
- `icon` → 100px

**Category depth:**
- `shallow` (default): hero shot only (`featured_image` or first image)
- `deep`: all image variants per product (multi-angle, lifestyle, detail shots)

### Step 4: Organization — Taxonomic Folder Structure

```
{store-slug}-luxe-assets/
├── brand/
│   └── logo.{png,svg}                             # Store logo/wordmark
├── {category-1}/
│   ├── {product-handle}_grande.jpg
│   ├── {product-handle}_large.jpg
│   └── {product-handle}_alt-1_grande.jpg          # Deep mode: alternate angles
├── {category-2}/
│   └── ...
├── banners/                                        # Collection/homepage banners
│   └── {collection-handle}_1920x.jpg
├── manifest.json                                   # Full metadata (see below)
└── download.sh                                     # Reproducible re-download script
```

**Category auto-detection:**
When product collection data is available, group by collection name.
When unavailable, infer category from product type (tea, teaware, apparel) or first path segment in handle.

**manifest.json schema:**
```json
[
  {
    "local_path": "teas/silver-needle-reserve_grande.jpg",
    "cdn_url": "https://cdn.shopify.com/s/files/1/.../silver-needle-reserve_grande.jpg?v=1234567890",
    "size": "grande",
    "product_title": "Silver Needle Reserve",
    "product_handle": "silver-needle-reserve",
    "category": "teas-white",
    "alt_text": "Silver Needle Reserve — Fuding County air-dried White Tea | Red Blossom Tea",
    "timestamp": 1234567890,
    "luxe_score": 0.88,
    "checksum": "sha256:abc123..."
  }
]
```

### Step 5: Validation — Verify & Deduplicate

```bash
# URL integrity: each CDN URL must return HTTP 200 + Content-Type: image/*
curl -sI "$cdn_url" | grep -q "200\|Content-Type: image/"

# Checksum deduplication: skip if file checksum matches an existing asset
sha256sum "$local_path" | cut -d' ' -f1

# Resolution check: verify downloaded dimensions exceed min_resolution
python3 -c "from PIL import Image; i=Image.open('$path'); print(i.size)"
```

**Deduplication:**
- By `?v=` timestamp: same URL + same timestamp = identical image, skip download
- By SHA-256 checksum: same pixel content even if URL differs (catches supplier-shared imagery)
- By `exclude_existing`: pass a prior manifest to skip all previously-hashed entries

**Outputs:**
1. **ZIP archive**: `{store-slug}-luxe-assets.zip` organized into taxonomic folders
2. **manifest.json**: maps local paths → CDN URLs → product metadata (for AI pipelines / CMS import)
3. **download.sh**: standalone bash script for one-command reproducible re-download without Python
4. **CSV import**: `{store-slug}-luxe-assets.csv` for PIM/CMS bulk upload

### Optional: Multi-Store Comparison Mode

Pass 2–3 Shopify domains to generate competitive intelligence:

```bash
python3 shopify-asset-curator.py \
  --stores "redblossomtea.com, competitor-tea.com, another-tea-shop.com" \
  --output competitor-asset-audit/
```

**Output includes:**
- Side-by-side category coverage gap analysis (heatmap)
- Price-tier visual positioning map (image quality vs. price point)
- Shared supplier detection (identical image checksums across stores)
- Asset density comparison (images per product, average resolution)

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `store` | yes | — | Shopify store domain (e.g. `redblossomtea.com`) |
| `category` | no | `all` | Focus on specific categories: `teas`, `teaware`, `gifts`, `banners`, `logo`, or comma-separated list |
| `size` | no | `grande` | Target resolution: `grande` (1200px), `1024x1024`, `large` (600px), `medium` (300px) |
| `depth` | no | `shallow` | `shallow` (hero shots only) vs `deep` (all variants + alt angles) |
| `min_score` | no | `50` | Minimum luxe score threshold (0–100). Only surfaces brand-representative assets |
| `top_products` | no | `40` | Maximum output count (0 = unlimited) |
| `include_all` | no | `false` | Bypass scoring, include every product (ignores min_score/top_products) |
| `min_resolution` | no | `0` | Minimum image dimension in pixels (e.g. `800` = skip anything under 800px) |
| `exclude_existing` | no | — | Path to prior manifest for checksum dedup |
| `adaptive` | no | `false` | Re-run with timestamp-based incremental updates |
| `baseline_manifest` | no | — | Path to prior manifest for `adaptive` mode |
| `stores` | no | — | Comma-separated domains for multi-store comparison mode |
| `output` | no | `./{store-slug}-luxe-assets/` | Output directory |

## AEO-Optimized Alt-Text Generation

For every asset, auto-generates search-engine-friendly alt text using this template:

```
"{Product Name} — {Origin} {Craft} {Tea Type} | {Brand}"
# Example: "Silver Needle Reserve — Fuding County air-dried White Tea | Red Blossom Tea"
```

When product metadata includes origin, craft, flavor, or material fields, those are interpolated into the alt-text template. Falls back to just `"{Product Name} | {Brand}"` when structured data is unavailable.

The alt text is written into:
- `manifest.json` (for AI pipeline consumption)
- `{store-slug}-luxe-assets.csv` (for CMS bulk import)
- HTML template preview (for human review before publish)

## Constraints & Notes

- **Respect robots.txt**: Shopify stores generally allow product image indexing. If a store explicitly disallows scraping via robots.txt, fall back to API-only mode.
- **CDN URLs are public**: Tied to Shopify's global CDN cache layer. The `?v=` parameter is required for cache invalidation.
- **No API key needed**: Strategy B (read-only scrape) works for any store. Strategy A (Admin API) requires OAuth client credentials or an existing `shpat_`/`shpss_` token.
- **Large stores (>1000 SKUs)**: Strategy A is strongly recommended for performance and pagination. Strategy B may hit rate limits or timeout on collection pages with hundreds of products.
- **File sizes**: `grande` images are typically 1200×1200px, ~200–500KB each. A 40-image pack is ~8–20MB zipped.
- **Licensing**: Only use for stores you own or have explicit permission to audit. The `manifest.json` included in every asset pack records the source CDN URL for provenance.

## Known Limitations & Certification

**Certified: Sigil PASS_WITH_CONCERNS** (evaluated 2026-06-30, valid through 2026-09-28)
- Repository: `BlueBoobyAI/skills-god.git` at `docs/sigil/shopify-asset-curator-sigil.json`
- Score: 72/100 (engineering PASS, security PASS, UX PASS_WITH_CONCERNS, CEO/strategy PASS)

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Luxe score rarity detection is keyword-based (title scanning) | False positives on products with "Reserve" not actually being limited | Override with `--include-all` for complete but unranked output |
| Visual quality scoring only checks text overlay badges | Does not detect blur, poor lighting, or composite images | Human review recommended for final selection; the score filters obvious junk only |
| No Shopify Admin API auth flow | Strategy A requires pre-configured credentials; not wizard-guided | Strategy B (scrape) works without auth; Admin API guidance is documented for implementers |
| Scraping depends on current Shopify liquid template structure | DOM changes by theme developers can break extraction | Adaptive mode detects structural changes and warns; Strategy A (API) is structure-invariant |
| Output is a one-time snapshot, not a live sync | Assets go stale when stores update imagery | `adaptive=True` re-run compares timestamps; automation wrapper manages scheduled runs |

## Installation

This skill is packaged for the claude-skills-marketplace ecosystem. Install via skills-god:

```bash
scripts/skills-god.sh ensure shopify-asset-curator
```

Or clone directly:
```bash
mkdir -p ~/skills/shopify-asset-curator
# Copy this SKILL.md into the directory
# The companion script lives at scripts/shopify-asset-curator.py
```

## Success Criteria

This skill succeeds when:
- ✅ A taxonomically organized image folder exists for the target store
- ✅ manifest.json is valid JSON and every CDN URL returns HTTP 200
- ✅ At least one asset from each major category present in the store
- ✅ All images are at the requested size suffix (no degraded resolution)
- ✅ download.sh is self-contained, executable, and reproduces the same output
- ✅ Multi-store comparison mode (when used) produces a gap analysis heatmap

## Tools Used

- **WebFetch / Browser**: Scrape Shopify collection and product pages (Strategy B)
- **Python3 + urllib**: Download images, verify checksums, build manifest
- **Python3 + json**: Parse embedded Shopify JSON data, write manifest
- **Bash + curl**: URL validation, reproducible download script, deduplication
- **Python3 + hashlib**: SHA-256 checksum for dedup across runs
- **Python3 + PIL/Pillow**: Optional — resolution verification on downloaded images

## Example Execution

**Input:**
```
Store: https://redblossomtea.com
Focus: teas, teaware, gifts, brand, banners
Size: grande / large
Depth: shallow
Exclude: previous-manifest.json (batch 1)
```

**Process:**
1. Scraped 4 collection pages → discovered 160 products
2. Extracted 665 unique CDN URLs across all products and sizes
3. Filtered to 262 unique items via size/handle dedup
4. Scored by luxe ranking → top 42 assets (≥0.65 score) across 12 category groups
5. Downloaded 42 images at `grande` resolution (~14MB)
6. Generated manifest.json, download.sh, and CSV import
7. Validated all 42 URLs: 42/42 HTTP 200, 42/42 Content-Type: image/jpeg

**Output:**
```
rbt-luxe-assets/
├── brand/rbt-logo.png
├── teas-green/          (3 items: pre-rain dragonwell, finest dragonwell, cloud mist)
├── teas-white/          (2 items: silver needle reserve, bai mu dan)
├── teas-oolong/         (11 items: da yu lin, alishan, fu shou shan, jin xuan, ...)
├── teas-black/          (5 items: gold thread reserve, golden monkey, ...)
├── teas-pu-erh-aged/    (3 items: aged wenshan baozhong 1970, ...)
├── teas-tisane/         (3 items: american ginseng, dragon pearl jasmine)
├── teaware-glass/       (4 items: glass infuser cup, blossom glass teapot, ...)
├── teaware-porcelain/   (6 items: snow tea bowl, spring gaiwan, ming server, ...)
├── teaware-yixing/      (2 items: artisan yixing teapot, yixing tasting cup)
├── teaware-accessories/ (7 items: matcha whisk, matcha scoop, bamboo tongs, ...)
├── gifts-collections/   (4 items: pinnacle collection, 40th anniversary, ...)
├── homepage-banners/    (5 items: cold brew, pinnacle, gift of tea, ...)
├── manifest.json
└── download.sh
```

## Multi-Store Comparison Output Example

```
competitor-asset-audit/
├── redblossomtea/       (42 assets, 12 categories, avg luxe 0.72)
├── competitor-tea/      (28 assets, 7 categories, avg luxe 0.58)
├── another-tea-shop/    (35 assets, 9 categories, avg luxe 0.65)
├── coverage-gap-heatmap.png
├── price-positioning-map.png
├── shared-suppliers.csv   (6 matching checksums across stores)
└── comparison-report.md
```

## Integration

This skill produces outputs consumable by:
- **Content Studio**: Manifest feeds the image library picker for blog post illustration
- **5000-Surfaces Flywheel**: Assets distributed across social platforms via cross-platform relay
- **AI image pipelines**: manifest.json feeds reference imagery into AI generation workflows
- **CMS/PIM platforms**: CSV import file for bulk upload to Shopify, WordPress, or Contentful
- **Xiaohongshu / Instagram**: Taxonomic folder structure maps directly to social post scheduling

For cross-platform publish integration, pair with a social-publish skill that consumes the manifest and uploads assets to target platforms' APIs.
