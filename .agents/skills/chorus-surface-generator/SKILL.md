---
name: "chorus-surface-generator"
description: "Generate 3 adaptive commerce surfaces (Concierge, Product Finder, Smart Compare) from a Brand Profile. Activates when users want to generate store surfaces, build a product finder, create a concierge recommendation engine, or make a comparison tool."
license: MIT
metadata:
  tier: "STANDARD"
  category: "E-commerce / Surface Generation"
---

# CHORUS Surface Generator

## Purpose

Take a Brand Profile (from brand-profile-decoder or manually specified) and generate 3 adaptive commerce surfaces, each checked by Skeptic for brand authenticity. Every surface must feel brand-authentic and be merchant-ready — copy-paste deployable into Shopify, a widget, or a landing page.

The three surfaces form the customer-facing layer of the CHORUS commerce brain:
- **Concierge** — adaptive recommendation engine that talks like the brand
- **Product Finder** — guided quiz logic that learns what the shopper needs
- **Smart Compare** — comparison matrix that surfaces real tradeoffs

A surface that passes Skeptic is one the merchant can ship today. A surface that fails Skeptic is one that sounds like a generic SaaS template with the brand name swapped in.

## When to Use

- "generate surfaces for {store}"
- "build concierge for {brand}"
- "create product finder for my store"
- "make a comparison tool"
- "set up the full CHORUS stack for {brand}"
- "I have a brand profile, give me the surfaces"

## Process

### 1. INPUT: Brand Profile

Accepts a Brand Profile JSON (output of brand-profile-decoder, or manually specified). Minimal viable profile requires:

```json
{
  "brand_name": "Red Blossom Tea Company",
  "tagline": "San Francisco's oldest purveyor of fine Chinese teas since 1985",
  "voice_profile": {
    "register": "warm_authority",
    "tone_adjectives": ["knowledgeable", "inviting", "unhurried", "reverent"],
    "linguistic_markers": ["sensory-first descriptions", "short paragraphs", "no hype language", "occasional Chinese terms with gloss"]
  },
  "customer_personas": [
    {"name": "Curious Novice", "needs": "guidance without judgment, approachable entry points"},
    {"name": "Devoted Connoisseur", "needs": "depth, provenance details, seasonal offerings"},
    {"name": "Gift Shopper", "needs": "beautiful packaging, clear gifting cues, reliable quality"}
  ],
  "product_categories": [
    {"name": "Oolong", "count": 15, "signature": "Dragon Pearl Jasmine"},
    {"name": "Green", "count": 10, "signature": "Cloud Forest Green"},
    {"name": "Black", "count": 8, "signature": "Keemun Hao Ya A"},
    {"name": "Pu-erh", "count": 6, "signature": "1990 Vintage Pu-erh"},
    {"name": "Herbal & Tisane", "count": 5, "signature": "Chrysanthemum Buds"}
  ],
  "price_range": {"min": 8, "max": 120, "sweet_spot": "18-35"},
  "brand_values": ["tradition", "quality", "education", "community"],
  "aesthetic_keywords": ["minimal", "earthy", "calligraphic", "warm neutrals"]
}
```

Accepts both JSON file paths and inline JSON strings. If no brand_profile is provided, the skill prompts for one or asks the user to run brand-profile-decoder first.

### 2. PARALLEL GENERATION

All three surfaces generate in parallel using `agent()` sub-agents. Each sub-agent receives the full Brand Profile plus surface-specific instructions.

#### Concierge Surface

An adaptive product recommendation engine that speaks in the brand's voice. Output structure:

```json
{
  "surface_type": "concierge",
  "brand": "Red Blossom Tea Company",
  "voice_instructions": {
    "persona": "A knowledgeable but approachable tea educator in a San Francisco Chinatown shop",
    "sensory_first": true,
    "greeting_templates": [
      "Welcome in. Let me help you find your next cup."
    ],
    "max_words_per_response": 60
  },
  "recommendation_rules": [
    {
      "trigger": "shopper signals interest in floral teas",
      "logic": "surface Jasmine offerings first (Dragon Pearl, Jasmine Silver Needle), then bridge to lighter oolongs (Oriental Beauty), never jump straight to pu-erh",
      "weight": 0.4
    },
    {
      "trigger": "shopper mentions gifting",
      "logic": "prioritize gift-ready packaging, curated sets, and tear-resistant shipping boxes",
      "weight": 0.3
    },
    {
      "trigger": "shopper on product page for pu-erh",
      "logic": "suggest brewing vessels (Yixing, gaiwan), related aged teas, never suggest herbal blends",
      "weight": 0.3
    }
  ],
  "context_aware_behaviors": {
    "page_context": "read product page metadata to inform recommendations",
    "cart_context": "fill gaps — if only oolongs in cart, suggest complementary green or pu-erh",
    "time_context": "morning → black tea or roasted oolong, afternoon → greener oolongs or white, evening → herbal or aged pu-erh"
  },
  "output_channels": ["popup widget", "inline carousel", "chat bar"]
}
```

#### Product Finder Surface

A guided quiz that learns what the shopper needs. Output structure:

```json
{
  "surface_type": "product_finder",
  "brand": "Red Blossom Tea Company",
  "quiz_logic": {
    "entry_points": [
      {"trigger": "landing page", "question": "What kind of tea experience are you looking for today?"},
      {"trigger": "category browse", "question": "You're browsing {category}. What do you want to know more about?"}
    ],
    "question_tree": {
      "id": "root",
      "question": "What kind of tea experience are you looking for today?",
      "options": [
        {"label": "Something calming and floral", "next": "floral_path", "weight": 0.3},
        {"label": "Bold and energizing", "next": "bold_path", "weight": 0.25},
        {"label": "I don't know, help me explore", "next": "novice_path", "weight": 0.35},
        {"label": "A gift for someone", "next": "gift_path", "weight": 0.1}
      ],
      "children": {
        "floral_path": {
          "question": "How floral?",
          "options": [
            {"label": "Subtle floral aroma", "result_filter": {"categories": ["oolong"], "tags": ["light_floral"]}},
            {"label": "Full jasmine-scented", "result_filter": {"product_ids": ["dragon-pearl-jasmine", "jasmine-silver-needle"]}}
          ]
        },
        "bold_path": {
          "question": "How do you take your tea?",
          "options": [
            {"label": "Strong, standalone", "result_filter": {"categories": ["black", "pu-erh"]}},
            {"label": "Smooth but complex", "result_filter": {"categories": ["oolong"], "tags": ["roasted", "dark_roast"]}}
          ]
        },
        "novice_path": {
          "question": "What flavors do you normally enjoy in drinks?",
          "options": [
            {"label": "Fruity or floral", "result_filter": {"recommend": "jasmine_green_starter"}},
            {"label": "Rich or toasty", "result_filter": {"recommend": "roasted_oolong_starter"}},
            {"label": "Clean or refreshing", "result_filter": {"recommend": "green_tea_starter"}}
          ]
        },
        "gift_path": {
          "question": "What's your budget?",
          "options": [
            {"label": "Under $30", "result_filter": {"price_max": 30, "tags": ["gift_ready"]}},
            {"label": "$30-$60", "result_filter": {"price_min": 30, "price_max": 60, "tags": ["gift_ready", "premium"]}},
            {"label": "Over $60", "result_filter": {"price_min": 60, "tags": ["gift_ready", "luxury"]}}
          ]
        }
      }
    },
    "fallback": "Always offer to speak with a real tea expert if the quiz isn't narrowing down"
  }
}
```

#### Smart Compare Surface

A comparison matrix that surfaces real tradeoffs. Output structure:

```json
{
  "surface_type": "smart_compare",
  "brand": "Red Blossom Tea Company",
  "default_comparison": {
    "title": "How do our oolongs compare?",
    "trigger": "shopper viewing 2+ oolong products",
    "dimensions": ["roast_level", "flavor_profile", "caffeine", "price_per_cup", "brewing_difficulty", "best_for"],
    "example_matrix": {
      "columns": ["Dragon Pearl Jasmine", "Tieguanyin", "Oriental Beauty", "Da Hong Pao"],
      "rows": [
        {"dimension": "Roast Level", "values": ["Unroasted", "Light roast", "Medium roast", "Dark roast"]},
        {"dimension": "Flavor Profile", "values": ["Jasmine, cream", "Orchid, buttery", "Honey, fruity", "Stone fruit, cocoa"]},
        {"dimension": "Caffeine", "values": ["Low", "Low-Med", "Med", "Med-High"]},
        {"dimension": "Brewing Difficulty", "values": ["Easy (3-5 steepings)", "Medium (gongfu recommended)", "Easy (5+ steepings)", "Advanced (precise temp needed)"]},
        {"dimension": "Best For", "values": ["Morning or afternoon", "Afternoon contemplation", "Afternoon tea session", "Evening with dessert"]}
      ]
    }
  },
  "dynamic_comparison_rules": [
    {
      "trigger": "shopper compares across categories (e.g. oolong vs pu-erh)",
      "dimensions": ["fermentation", "aging_potential", "price_range", "session_length", "storage_needs"]
    },
    {
      "trigger": "shopper compares within price tier (e.g. under $20)",
      "dimensions": ["flavor_intensity", "cup_count", "value_score", "reorder_popularity"]
    },
    {
      "trigger": "shopper compares gift sets",
      "dimensions": ["number_of_teas", "packaging_quality", "variety_score", "recipient_suitability"]
    }
  ],
  "visual_preferences": {
    "layout": "horizontal scrolling table on mobile, full table on desktop",
    "highlight": "best-in-class cell per row gets a subtle background tint",
    "call_to_action": "Click a tea name to see full product details"
  }
}
```

### 3. PARALLEL CHECKER

Skeptic reviews each surface independently and in parallel. Each review checks three dimensions:

| Dimension | What Skeptic checks | Pass condition |
|-----------|-------------------|---------------|
| **Voice authenticity** | Would the brand's founder say this? No generic e-commerce copy. Sensory language present where expected. Register consistent. | Score >= 7/10 |
| **Merchant readiness** | Can this be deployed without editing? Are all references valid (product handles, category names, price tiers)? | All references resolvable |
| **Cross-surface consistency** | Do all three surfaces describe the same brand? Same voice register, same product names, same price expectations, same customer personas? | No contradictions |

Skeptic verdict format:

```json
{
  "surface": "concierge",
  "verdict": "PASS",
  "score": 8.5,
  "findings": [
    {"severity": "info", "message": "Greeting template could be more sensory — consider adding a scent note"},
    {"severity": "pass", "message": "Recommendation rules correctly avoid suggesting pu-erh to floral seekers"},
    {"severity": "pass", "message": "Context-aware behaviors match brand values (tradition, education, quality)"}
  ]
}
```

### 4. EXIT CONDITIONS

| Condition | Action |
|-----------|--------|
| **All PASS** | Show merchant-ready output with all 3 surface JSONs + Skeptic verdicts. Ready to deploy. |
| **One FAIL** | Show the 2 passing surfaces as merchant-ready. Show the failing surface with Skeptic's findings. Append: "Tuning [surface] — contact support." |
| **Multiple FAIL** | Escalate to human with full Brand Profile + all 3 Skeptic verdicts + generation logs. Do NOT surface partial output — surfaces must work together. |

### 5. GUARDRAILS

- **Max 3 retries per surface**: If a surface fails Skeptic, regenerate up to 2 more times with Skeptic's findings as additional context. On the 3rd failure, mark as FAIL.
- **30s timeout per generation**: Each `agent()` sub-agent call must complete within 30 seconds. Hung generation = FAIL.
- **$0.50 budget governor**: Track cumulative token spend across all 3 generators + 3 checkers. If budget exceeded mid-generation, stop all in-flight generations and escalate to human.

**Budget governor — concrete enforcement mechanism:**

Use this Python function as the budget tracker (copy into session context before starting generation):

```python
import json, os, time

BUDGET_FILE = "/tmp/chorus-budget.json"
MAX_BUDGET = 0.50  # USD, configurable

def budget_ok(cost_estimate_usd: float = 0.0) -> bool:
    """Check budget before each agent() call. Returns False if exceeded."""
    budget = {"spent": 0.0, "max": MAX_BUDGET, "started": time.time()}
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE) as f:
            budget = json.load(f)
    budget["spent"] += cost_estimate_usd
    budget["last_call"] = time.time()
    with open(BUDGET_FILE, "w") as f:
        json.dump(budget, f)
    return budget["spent"] <= budget["max"]

# Pre-flight check — call before each generation:
# if not budget_ok(0.08):  # ~$0.08 per agent() call estimate
#     return {"error": "BUDGET_EXCEEDED", "budget": budget}
```

This creates a durable check file that survives across sequential agent calls and provides a hard stop rather than a prose recommendation.

## Input Parameters

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `brand_profile` | Yes | JSON path or inline JSON string | — | Full Brand Profile from brand-profile-decoder or manual specification |
| `surfaces` | No | string | `all` | Which surfaces to generate: `concierge`, `product-finder`, `smart-compare`, or `all` |
| `budget` | No | number | `0.50` | Maximum USD spend for this generation. Hard stop at limit. |
| `timeout` | No | number | `30` | Seconds per sub-agent generation call |
| `max_retries` | No | integer | `3` | Max Skeptic review cycles per surface before FAIL |

## Output

Returns a structured JSON object:

```json
{
  "status": "ALL_PASS",
  "brand": "Red Blossom Tea Company",
  "generated_at": "2026-06-30T14:30:00Z",
  "surfaces": {
    "concierge": { "...": "full surface definition" },
    "product_finder": { "...": "full surface definition" },
    "smart_compare": { "...": "full surface definition" }
  },
  "skeptic_verdicts": {
    "concierge": { "verdict": "PASS", "score": 8.5, "findings": [] },
    "product_finder": { "verdict": "PASS", "score": 9.0, "findings": [] },
    "smart_compare": { "verdict": "PASS", "score": 7.5, "findings": [] }
  },
  "budget_used": 0.42,
  "total_time_seconds": 18.3
}
```

Three possible status values: `ALL_PASS`, `PARTIAL_PASS` (one surface failed), `ESCALATED` (multiple failures).

## Tools Used

- `agent()` — parallel sub-agent calls for each surface generation and each Skeptic review (up to 6 concurrent sub-agents)
- `Python3` — JSON validation, budget tracking, timeout enforcement
- `Read` — reading Brand Profile from file path if provided

## Integration Contract

**Role in CHORUS flywheel:** Stage 3 (Generate) — produces customer-facing surfaces from the BrandProfile.

This skill's INPUT is the BrandProfile JSON from `brand-profile-decoder` (Stage 2: Brand). Its OUTPUT is reviewed by `scorecard-auditor` (Stage 5: Score) using the shared contract schema.

**Input contract (from brand-profile-decoder):**
```json
{
  "brand_name": "...",
  "voice_profile": {"register": "...", "tone_adjectives": [...], "linguistic_markers": [...]},
  "customer_personas": [{"name": "...", "needs": "..."}],
  "product_categories": [{"name": "...", "count": N, "signature": "..."}],
  "price_range": {"min": N, "max": N, "sweet_spot": "..."},
  "brand_values": ["..."],
  "aesthetic_keywords": ["..."],
  "evidence_anchors": [{"claim": "...", "source_phrase": "...", "source_url": "..."}]
}
```

**Output contract (to scorecard-auditor):**
```json
{
  "status": "ALL_PASS|PARTIAL_PASS|ESCALATED",
  "brand": "...",
  "surfaces": {"concierge": {...}, "product_finder": {...}, "smart_compare": {...}},
  "skeptic_verdicts": {...},
  "budget_used": 0.0,
  "total_time_seconds": 0.0
}
```

**Contract rules:**
- Input must come from a validated brand-profile-decoder output (Skeptic-verified)
- The budget governor provides a hard enforcement stop
- Output surfaces must be Skeptic-verified (score >= 7/10)
- All product references must be resolvable against the brand's actual catalog
- Schema conforms to `src/aeo/schemas/brand_profile.py` when it exists

## Installation

```bash
bash ~/.claude/skills/skills-god.sh ensure chorus-surface-generator
```

Or symlink manually:
```bash
ln -sf /Users/cl/aeo/claude-skills-marketplace/.agents/skills/chorus-surface-generator \
       ~/.claude/skills/chorus-surface-generator
```

## Success Criteria

- All generated surfaces pass Skeptic brand authenticity check (score >= 7/10 each)
- Each surface is self-consistent (no voice drift within a single surface)
- Cross-surface consistency verified (same product names, same price expectations, same register)
- All product references resolvable against the brand's actual catalog
- Merchant-ready output requires zero editing before deployment
