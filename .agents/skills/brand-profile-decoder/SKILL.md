---
name: "brand-profile-decoder"
description: "Decode any Shopify store into a structured Brand Profile using multi-agent analysis. Activates when users want to analyze a store, understand brand voice, decode a brand, generate a brand profile, or audit a Shopify store."
license: MIT
metadata:
  tier: "STANDARD"
  category: "E-commerce / Brand Intelligence"
---

# Brand Profile Decoder

Decode any Shopify store into a structured, evidence-anchored Brand Profile. Core loop of the CHORUS commerce intelligence brain.

## Purpose

Take ANY Shopify store URL and produce a structured Brand Profile covering voice token, value system, and product logic. Every claim is anchored to verbatim evidence from the storefront. The output is a structured JSON payload plus a readable Markdown report that a merchant could review and correct in under 5 minutes.

This is the keystone skill of the CHORUS pipeline. Downstream skills (campaign designer, copywriter, competitor matrix, audience builder) all read the Brand Profile as their primary input.

## When to Use

**Activation phrases:**
- "decode {store URL}" — full profile decode
- "analyze brand voice of {store URL}" — voice-only pass (faster)
- "generate brand profile for {store URL}" — full profile
- "audit {store URL}" — includes Skeptic validation pass
- "what is {store}'s brand" — quick profile (shallow depth)
- "break down the brand of {store}" — full decode

**Skip when:** The user wants pricing data or a simple product catalog dump. Route to `seo-audit` or a shopping-comparison skill instead.

## Process

### 5-Step Pipeline

**Step 1: FETCH** -- Pull store metadata.

Use `WebFetch` or `playwright` (Playwright for JS-rendered stores, WebFetch for static) to collect:
1. Store root page -- tagline, hero text, nav structure, footer
2. `/about` or `/pages/about-us` -- brand story, founder bio, mission
3. 10 sampled product pages -- title, description, price, category tags, image alt text, variant names
4. 5 product reviews if available (check `/products/{handle}}?view=reviews` or review app snippet in DOM)
5. `/pages/faq` -- shipping, returns, sizing policy (reveals customer pain points brand is addressing)
6. Collection/category pages -- how products are organized, what the brand considers related

**Fetch strategy:** Sample broadly first (storefront + 3 categories), then drill into products if depth=deep. For shallow depth, skip individual product pages and use collection page listings only.

**Step 2: PARALLEL MAKER** -- Run three agents concurrently using the `agent()` tool. Each receives the same fetched store data as context.

| Agent | Role | Output |
|-------|------|--------|
| **Empath** | "What shopper does this brand speak to?" | Target audience profile (demographic + psychographic), 3+ verbatim phrases that prove audience targeting, emotional hooks used |
| **Architect** | "What's the product taxonomy? Pricing logic? Category structure?" | Category tree, pricing tiers ($/unit if measurable), product logic (bundling, upsells, exclusivity signals), SKU range breadth |
| **Analyst** | "What words repeat? Emotional tone? What's the unstated value system?" | Top-10 keyword frequency, tone vector (formal/casual, warm/clinical, authoritative/peer), implied values (sustainability, luxury, convenience, craftsmanship, community), gap analysis (what the store doesn't say) |

**Every output must cite evidence.** Each claim in an agent's report links back to a source phrase from Step 1 data. A claim without evidence is discarded.

`agent()` invocation pattern:

```
agent(name="empath", prompt=format_empath_prompt(store_data), model="sonnet")
agent(name="architect", prompt=format_architect_prompt(store_data), model="sonnet")
agent(name="analyst", prompt=format_analyst_prompt(store_data), model="sonnet")
```

Run all three in parallel. If your runtime does not support parallel agent dispatch, run them sequentially but merge the outputs into a single synthesis.

**Step 3: SYNTHESIS** -- Combine the three agent outputs into a unified Brand Profile.

The synthesis produces two artifacts:

**A. Voice Token** -- A 3-5 word brand voice identifier. Examples: "Warm authority with a wink" or "Minimalist precision, no filler" or "Craft narrative, direct close". This is the brand's "descriptive fingerprint" -- used downstream for copy generation voice consistency checks.

**B. Structured Profile** (JSON + Markdown):

```json
{
  "brand_name": "",
  "voice_token": "",
  "target_audience": { "demographic": "", "psychographic": "" },
  "tone_vector": { "formality": 0.0, "warmth": 0.0, "complexity": 0.0 },
  "value_system": ["value1", "value2", "value3"],
  "product_taxonomy": { "categories": [], "pricing_tiers": {} },
  "evidence_anchors": [
    { "claim": "", "source_phrase": "", "source_url": "" }
  ],
  "confidence_scores": {
    "empath": 0.0,
    "architect": 0.0,
    "analyst": 0.0
  },
  "gaps": ["what we could not determine"]
}
```

**Evidence anchors are non-negotiable.** Every claim must point to a specific phrase scraped from the store, not an inference about what the store "probably" says. If the store is thin (few pages, no About, no reviews), surface that as a gap, not a hallucination.

**Step 4: PROFILE VALIDATION** -- Skeptic checks the Brand Profile itself.

The Skeptic agent receives the synthesized Brand Profile + 5 randomly sampled product descriptions from the raw store data (re-sampled, not the same 10 from Step 1 -- unless the store has fewer than 12 products, in which case reuse is forced).

Skeptic prompt:

> You are a Skeptic reviewer. The following Brand Profile claims to describe this store. Your job: verify that the Voice Token and value system are CONSISTENT with the actual product descriptions below. For each of the 5 product descriptions, answer: does this product's language match the claimed voice? Yes/No and why. If 2+ of 5 mismatch, the profile is INVALID -- flag it and explain the gap. If 4+ of 5 match, the profile is VALID.

**Validation outcomes:**
- **VALID** (4+ of 5 match) -- profile passes, include Skeptic sign-off in output
- **PARTIAL** (2-3 match) -- flag as PARTIAL with mismatch details, rerun Synthesis with corrections
- **INVALID** (0-1 match) -- reject, note root cause (wrong audience? wrong voice?), rerun from Step 1 with a different fetch strategy (more products, deeper scraping)

**Step 5: OUTPUT** -- Produce final deliverables.

1. **Markdown Report** -- Human-readable brand profile with section headers, verbatim quote blocks, evidence callouts, Skeptic verdict, and confidence annotations
2. **Structured JSON** -- Parsable by downstream CHORUS skills. Write to a file in the workspace named `brand-profile-{store-slug}.json` for reference.
   - **Security: Sanitize store slug before file write.** Derive slug from the store URL using `re.sub(r'[^a-z0-9-]', '', domain.lower())` — this prevents path traversal (CWE-22) where a malicious URL like `https://evil.com/../etc/passwd` could overwrite files outside the workspace.
3. **Summary** -- 3-5 sentence takeaway the merchant would agree with (designed for quick shareability)

### Error Handling

- **Store not found / 404:** Report "Store unreachable. Verify the URL is a valid Shopify storefront." Do not hallucinate profile.
- **Password wall:** Report "Store is password-protected. Cannot access without credentials." If credentials are available (via env vars or user), use Playwright with login.
  - **⚠️ Credential safety:** When using stored credentials for password wall bypass, (a) explicitly log which env var is being used, (b) NEVER log the credential value itself, (c) distinguish dev vs staging vs prod credentials in the log message. This prevents accidental credential exposure in session transcripts.
- **Thin store** (<5 products, no About page, no reviews): Produce a THIN profile with all confidence scores at 0.3 or below and gaps filled. Do not fabricate.
- **Rate limited or blocked:** Wait 5 seconds and retry with a different User-Agent. On second failure, report "Could not fetch store data -- the site may be blocking automated access."

## Input Parameters

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `store_url` | Yes | string | -- | Full Shopify store URL (e.g. `https://redblossomtea.com`) |
| `depth` | No | string | `standard` | `shallow` (3 pages, no reviews), `standard` (full pipeline), `deep` (+ competitors, 20 products) |
| `category_focus` | No | string | -- | Optional category to analyze specifically (e.g. "green tea", "accessories") |
| `skip_skeptic` | No | boolean | `false` | Set to `true` to skip Step 4 validation for speed |
| `output_format` | No | string | `both` | `json`, `markdown`, or `both` |

## Tools Used

- **WebFetch**: Primary tool for fetching storefront pages. Use for collection pages, About page, FAQ. Falls back to Playwright if JS rendering is required (e.g., infinite-scroll product grids, client-rendered review widgets).
- **Browser (Playwright)**: Fallback for JS-heavy storefronts. Navigate to root, collect rendered DOM snapshot. Use `browser_snapshot` for structure, `browser_evaluate` for extracting product list from storefront JS globals if available (`window.Shopify`, `__STORE__`, etc.).
- **Python3**: Format and deduplicate scraped text, compute keyword frequencies (simple count, no NLP library needed), run tone vector estimation (word-list-based sentiment/formality scoring, not ML inference), assemble JSON output.
- **agent()**: Dispatch the three parallel agents (Empath, Architect, Analyst) and the Skeptic verification agent. Each gets the same source data but different role-specific prompts.
- **Write**: Write the final Brand Profile JSON to `brand-profile-{store-slug}.json` in the workspace.

## Integration Contract

**Role in CHORUS flywheel:** Stage 2 (Brand) — keystone skill. Every other stage reads or writes the BrandProfile.

This skill's INPUT comes from `citation-intake-engine` (Stage 1: Monitor) or `reddit-community-monitor`. Its OUTPUT feeds `chorus-surface-generator` (Stage 3: Generate), and both the INPUT and OUTPUT conform to the shared BrandProfile schema at `src/aeo/schemas/brand_profile.py`.

**Input contract (from citation-intake-engine):**
```json
{
  "domain": "...",
  "intelligence": {"brand_voice": {...}, "product_taxonomy": {...}, ...},
  "sources_found": ["/pages/about", "/products/*"],
  "gaps": ["no Instagram bio found"]
}
```

**Output contract (to chorus-surface-generator):**
```json
{
  "brand_name": "",
  "voice_token": "",
  "target_audience": {"demographic": "", "psychographic": ""},
  "tone_vector": {"formality": 0.0, "warmth": 0.0, "complexity": 0.0},
  "value_system": ["value1", "value2"],
  "product_taxonomy": {"categories": [], "pricing_tiers": {}},
  "evidence_anchors": [{"claim": "", "source_phrase": "", "source_url": ""}],
  "confidence_scores": {"empath": 0.0, "architect": 0.0, "analyst": 0.0},
  "gaps": ["what could not be determined"]
}
```

**Contract rules:**
- Every claim must have an evidence anchor (source_phrase + source_url)
- Skeptic verification must pass (4+ of 5 product descriptions match the Voice Token)
- No fabrications for sections the store doesn't have (About, reviews, FAQ)
- The output must be machine-parseable by all downstream CHORUS skills
- A store owner could correct the profile in under 5 minutes

## Installation

```bash
skills-god.sh ensure brand-profile-decoder
```

Or manually:
```bash
mkdir -p ~/.claude/plugins/custom/skills/brand-profile-decoder
cp -r claude-skills-marketplace/.agents/skills/brand-profile-decoder/* \
  ~/.claude/plugins/custom/skills/brand-profile-decoder/
```

No external dependencies. All analysis is prompt-driven -- no ML models, no API keys beyond the Claude session.

## Related Skills

- **Competitor Matrix** (planned): Takes two Brand Profiles, produces head-to-head comparison
- **Campaign Designer** (planned): Reads Brand Profile to generate audience-specific ad campaigns
- **Copywriting Assistant** (planned): Uses Voice Token to enforce brand voice consistency
- **SEO Content Brief**: Shares storefront fetch infrastructure; use the raw catalog data from Step 1 as SEO brief input

## Success Criteria

1. **Evidence anchoring**: Every claim in the profile has a `source_phrase` and `source_url`. A profile with unsupported claims is incomplete.
2. **Skeptic verified**: The Skeptic agent confirms 4+ of 5 sampled product descriptions are consistent with the Voice Token.
3. **Merchant-correctable**: A store owner could read the profile and make corrections in under 5 minutes. If the profile is too abstract or wrong to edit quickly, the decode has failed.
4. **Machine-parseable**: The JSON output conforms to the schema above. Downstream skills can read and merge it without manual reformatting.
5. **Gap-honest**: If the store lacks an About page, reviews, or a clear FAQ, the profile says "Not available" for those sections -- not "neutral brand story" or similar fabrication.
6. **Store-agnostic**: The pipeline works for any Shopify store. No hardcoded brand names, product handles, or category names. The skill does not assume any particular industry or market position.
