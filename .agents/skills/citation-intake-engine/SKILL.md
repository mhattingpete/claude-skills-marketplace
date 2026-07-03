---
name: "citation-intake-engine"
description: "Extract structured brand intelligence from unstructured web sources. Activates when users want to research a brand, extract intelligence, scrape brand copy, gather brand data, or build a brand dossier."
license: MIT
metadata:
  tier: "STANDARD"
  category: "Market Intelligence / Data Extraction"
---

# Citation Intake Engine

## Purpose

Extract structured brand intelligence from unstructured web sources. Feeds the brand-profile-decoder by gathering raw material from:

- **llms.txt** (structured brand data, if available)
- **About page** (brand story, founder narrative, mission/values)
- **10-20 product descriptions** (sampled across price tiers low/medium/high)
- **5-10 customer reviews** (sourced from product pages, testimonial sections, or third-party review sites)
- **Social media bios** (LinkedIn, Instagram, X/Twitter)
- **FAQ section** (common questions reveal customer pain points and brand positioning)

Every extracted claim is tagged with its source URL for evidence anchoring. No claim leaves this engine without a verifiable source.

## When to Use

This skill activates when the user says anything like:

- "research {store}"
- "extract intelligence on {brand}"
- "gather brand data for {domain}"
- "build a brand dossier on redblossomtea.com"
- "scrape brand copy from {url}"
- "analyze {competitor} for market intelligence"
- "what does {brand}'s website tell us about their positioning"
- "intake {domain} for brand profile"
- "pull reviews and product data from {store}"

It does NOT handle brand voice analysis or persona generation -- that is the brand-profile-decoder's job. This skill only gathers raw material.

## Process

### Security: URL Validation (MANDATORY pre-flight)

Before ANY WebFetch call, validate the domain:

```python
import re, ipaddress, urllib.parse

def validate_domain(domain: str) -> str:
    """Validate domain is a public web hostname. Reject internal/private targets."""
    # Strip protocol if present
    domain = domain.strip().lstrip("https://").lstrip("http://").split("/")[0].split(":")[0]
    
    # Reject bare IP addresses (including localhost, 127.0.0.1, 192.168.*, 10.*)
    try:
        ip = ipaddress.ip_address(domain)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError(f"SSRF guard: rejected private IP address: {domain}")
        raise ValueError(f"SSRF guard: rejected bare IP address (use domain name): {domain}")
    except ValueError:
        raise  # re-raise our own errors
    except Exception:
        pass  # not an IP, continue
    
    # Reject internal hostnames
    internal_patterns = [r"^localhost", r"^127\.", r"^0\.0\.0\.0$", r"^::1$", r"^10\.", r"^172\.1[6-9]\.", r"^172\.2[0-9]\.", r"^172\.3[0-1]\.", r"^192\.168\."]
    for pat in internal_patterns:
        if re.match(pat, domain):
            raise ValueError(f"SSRF guard: rejected internal address: {domain}")
    
    # Reject non-http(s) targets
    parsed = urllib.parse.urlparse(f"https://{domain}")
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"SSRF guard: rejected non-http(s) scheme: {parsed.scheme}")
    
    return domain
```

**Use `validate_domain(domain)` before every WebFetch or HTTP fetch call.** This prevents CWE-918 SSRF attacks where a malicious domain like `localhost:8001` or `192.168.1.1` could probe internal services (Postgres on :5432, FastAPI dev on :8001, proxy on :8082).

### Phase 1: Discover

1. **Validate domain first.** Call `validate_domain(domain)` — reject internal/private addresses before any network call.
2. **Try llms.txt first.** Fetch `https://{domain}/llms.txt`. If it returns structured content (brand description, product list, pricing), extract everything and mark as high-confidence.
3. **Fall back to llms.txt fallback variants** if bare llms.txt is 404: `https://{domain}/llms-full.txt`, `https://{domain}/.well-known/llms.txt`.
4. **Try sitemap.xml** if llms.txt variants all 404. Fetch `https://{domain}/sitemap.xml` to discover page layout (About, product pages, FAQ paths).
5. **Fetch the homepage** as the last discovery step. Extract all internal links, categorize them (about, products, blog, FAQ, reviews, contact).
6. **Rate limiting:** Insert `time.sleep(1)` between each sequential fetch (1 second minimum delay). For parallel batched fetches (product pages), limit concurrency to 3 simultaneous requests.
7. **If all discovery fails**, report the domain as unreachable and recommend the user supply known page paths.

### Phase 2: Extract Pages

For each discovered or inferred page type:

| Source Type | Min Count | Sampling Strategy |
|-------------|-----------|-------------------|
| About page | 1 | The primary `/pages/about` or `/about` URL |
| Product pages | 10-20 | Sample across low/medium/high price tiers. Use sitemap if available, or collection pages. |
| Reviews | 5-10 | Product page review sections, `/pages/reviews`, `/testimonials`, or third-party (Trustpilot, Google) via web search |
| FAQ | 1 | `/pages/faq`, `/faq`, or `/support` |
| Social bios | 1-3 per platform | LinkedIn, Instagram, X/Twitter via web search with site:linkedin.com + brand name |

Extraction rules:
- For product pages: extract title, price, description, key features/selling points, ingredients/materials, dimensions.
- For reviews: extract the review text, rating, reviewer name (if public), date (if available), and which product it's for.
- For About pages: extract founding story, mission statement, team size, location, year founded.
- For FAQs: extract question + answer pairs verbatim.

### Phase 3: Structure Output

Aggregate all extracted intelligence into a structured JSON document. Tag every claim with `source` (the exact URL it came from). Run the output through the structured schema validator (Python3 script).

Validation checks:
- Every `claims[].source` is a non-empty string starting with `http` or `https`.
- Product sampling covers at least 3 distinct price tiers within the store's range.
- At least 3 source types are represented (About + Products + one more).
- If llms.txt was available, flag it in `sources_checked` with a `"fast_path": true` marker.

### Phase 4: Handoff

Pass the structured output directly to brand-profile-decoder if it's the next step in the pipeline. Otherwise, save to a temporary file and present the summary to the user.

## Output Schema

```json
{
  "domain": "redblossomtea.com",
  "sources_checked": ["llms.txt", "/pages/about", "/products/*", "/pages/faq"],
  "sources_found": ["/pages/about", "/products/*", "/pages/faq"],
  "fast_path_via_llms": false,
  "intelligence": {
    "brand_voice": {
      "claims": [
        {"text": "family-owned since 1985", "source": "https://redblossomtea.com/pages/about"},
        {"text": "specializes in premium Chinese and Taiwanese teas", "source": "https://redblossomtea.com/pages/about"},
        {"text": "second-generation, woman-owned business in San Francisco", "source": "https://redblossomtea.com/pages/about"}
      ],
      "confidence": "HIGH",
      "notes": "Consistent voice across About page and product descriptions"
    },
    "product_taxonomy": {
      "categories": ["oolong", "green", "black", "puerh", "white", "gift-sets"],
      "pricing_logic": "premium",
      "price_range": {"low": 8.00, "mid": 24.00, "high": 120.00},
      "source_products": 14,
      "top_selling_signals": ["Dragon Pearl Jasmine Supreme appears first on multiple collection pages"]
    },
    "customer_sentiment": {
      "positive_ratio": 0.88,
      "common_phrases": ["high quality", "beautiful packaging", "authentic", "arrived fresh", "great for gifting"],
      "common_complaints": ["pricey", "limited selection", "shipping is slow to east coast"],
      "source_reviews": 8,
      "avg_rating": 4.6
    },
    "competition_signals": [
      {"text": "positions against generic tea brands with 'direct from source' narrative", "source": "https://redblossomtea.com/pages/about"},
      {"text": "FAQ compares freshness window to grocery store tea", "source": "https://redblossomtea.com/pages/faq"}
    ],
    "faq_insights": {
      "question_count": 12,
      "top_pain_points_addressed": ["How long does tea stay fresh?", "Do you ship internationally?", "What is the return policy?"],
      "source": "https://redblossomtea.com/pages/faq"
    },
    "social_presence": {
      "linkedin": {"bio": "San Francisco's premier Chinese tea company since 1985", "found": true, "source": "https://linkedin.com/company/redblossomtea"},
      "instagram": null,
      "twitter": null
    },
    "gaps": [
      "No Instagram bio found",
      "No X/Twitter bio found",
      "Only 8 reviews extracted (target was 10); supplement via web search next pass"
    ]
  }
}
```

## Success Criteria

1. **At least 3 source types are found** (About + Products + at least one of: Reviews, FAQ, Social, llms.txt).
2. **Every claim has a source URL** -- no orphaned intelligence.
3. **Product sampling covers low/medium/high price tiers** -- verify by comparing extracted prices against the full catalog price range.
4. **llms.txt is checked first** -- record whether it was found (fast path) or not.
5. **Output is directly consumable by brand-profile-decoder** -- same JSON contract, no reformatting needed.
6. **If fewer than 3 source types found**, list the missing ones in `gaps` and recommend manual research to fill them.

## Tools Used

- **WebFetch**: Primary extraction tool. Fetch each page individually (About, product pages, FAQ, reviews). For product pages, batch fetch in parallel across price tiers. For llms.txt, single fast fetch.
- **web_search (Tavily)**: Find social media profiles (site:linkedin.com "Red Blossom Tea Company"), third-party review pages (site:trustpilot.com "Red Blossom Tea"), and alternative sources when primary pages 404.
- **Playwright**: When WebFetch fails due to JavaScript rendering (single-page apps, dynamic content stores). Navigate to the page, wait for content to render, extract text. Use for social media profile pages.
- **Python3**: Output validation -- run the structured JSON through a schema checker that verifies source coverage, price tier distribution, and required fields.

## Integration Contract

**Role in CHORUS flywheel:** Stage 1 (Monitor) — raw brand intelligence gathering.

This skill's OUTPUT feeds directly into `brand-profile-decoder` (Stage 2: Brand). The shared contract is defined by the BrandProfile schema at `src/aeo/schemas/brand_profile.py`.

**Output contract requirements:**
```json
{
  "domain": "store-domain.com",
  "sources_checked": ["llms.txt", "/pages/about", "..."],
  "sources_found": ["..."],
  "fast_path_via_llms": false,
  "intelligence": {
    "brand_voice": {"claims": [...], "confidence": "HIGH"},
    "product_taxonomy": {"categories": [...], "pricing_logic": "...", "price_range": {...}},
    "customer_sentiment": {"positive_ratio": 0.0, "common_phrases": [...]},
    "faq_insights": {"question_count": 0, "top_pain_points_addressed": [...]},
    "gaps": ["missing sources"]
  }
}
```

**Contract rules:**
- Every `claims[].source` is a non-empty URL starting with `http` or `https`
- Product sampling covers at least 3 distinct price tiers
- At least 3 source types must be represented (About + Products + one more)
- All claims carry evidence anchors — no orphaned intelligence
- Output must be directly consumable by brand-profile-decoder without reformatting

## Example Interaction

```
User: "research harney.com for a brand dossier"

Skill:
1. Fetch https://harney.com/llms.txt -- 404, fallback variants also 404. Mark llms as not found, note as gap.
2. Fetch https://harney.com/sitemap.xml -- discover pages: /pages/about-us, /collections/black-tea, /collections/green-tea, /collections/gift-sets, /pages/faq, /pages/reviews
3. Fetch About page: extract founding year (1983), founder (John Harney), location (Millerton, NY), mission ("fine teas for everyone").
4. Fetch 12 products across tiers:
   - Low ($8-12): English Breakfast, Earl Grey Supreme
   - Medium ($15-25): Paris, Hot Cinnamon Spice
   - High ($30+): Aged Puerh, Dragon Pearl gift set
5. Fetch FAQ: 15 Q&A pairs about shipping, steeping, storage.
6. Fetch reviews page: 10 customer reviews, avg rating 4.5.
7. Search web for social: LinkedIn bio "family-owned tea company since 1983". X bio "Tea company. Est. 1983."
8. Validate output with Python3 schema checker -- passes (4 source types, 12 products across 3 tiers, all claims sourced).
9. Present structured JSON and offer to feed it to brand-profile-decoder.

User: "yes, feed it to brand-profile-decoder"

10. Pass the JSON directly to brand-profile-decoder with a note that llms.txt was missing (gap for next pass).
```

## Installation

```bash
skills-god.sh ensure citation-intake-engine
```
