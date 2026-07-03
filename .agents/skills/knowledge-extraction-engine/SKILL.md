---
name: "knowledge-extraction-engine"
description: "Distill raw community data into actionable patterns, skill requirements, and market signals. Turns observed discussions into new skill specs for the CHORUS brain's self-improvement loop."
license: MIT
metadata:
  tier: "STANDARD"
  category: "Market Intelligence / Pattern Extraction"
---

# Knowledge Extraction Engine

## Purpose

The CHORUS brain's observational learning faculty. Raw community data comes in (Reddit posts, forum threads, customer reviews, competitor analysis). This skill extracts the signal: What patterns emerge? What skills would fill the observed needs? What markets are underserved? This is the flywheel's "research and learn new skills" faculty.

## When to Use

- After reddit-community-monitor returns findings (distill into intelligence)
- When analyzing customer reviews for product/feature gaps
- When researching competitors to identify underserved markets
- When the self-assessment meta-loop identifies a faculty gap to research
- "What patterns do you see in these forum posts?"
- "Extract actionable insights from this customer feedback"

## Process

### Step 1 -- Classify Input Source

Identify the source type to apply the right extraction lens:
- **Community discussion** (Reddit, HN, forums) -> Pattern extraction + sentiment
- **Customer reviews** -> Pain point clustering + feature requests
- **Competitor analysis** -> Feature gap + positioning signals
- **Technical discussions** -> Emerging tech patterns + skill opportunities
- **Market data** -> Underserved segments + demand signals

### Step 2 -- Extract Structured Patterns

For each source, extract:

```json
{
  "source": "r/shopify",
  "patterns": [
    {
      "pattern": "merchants frustrated with PDP image loading",
      "frequency": "HIGH (12 unique posts in last 7 days)",
      "evidence": [
        "Post: 'My product images take 4s to load on mobile'",
        "Post: 'Anyone else losing sales to slow PDP?'"
      ],
      "implied_skill": "pdp-performance-optimizer",
      "urgency": "HIGH"
    }
  ],
  "skill_recommendations": [
    {
      "skill_name": "pdp-performance-optimizer",
      "what_it_would_do": "Audit a Shopify PDP for image loading, CLS, LCP -- generate fix list",
      "category": "E-commerce / Performance",
      "market_size": "Likely large -- core Shopify pain point"
    }
  ],
  "market_signals": {
    "competitors_mentioned": ["Shopify Image CDN", "Cloudinary"],
    "gaps": ["No one offers an AI-driven PDP optimizer as a skill"],
    "trending_terms": ["core web vitals", "mobile conversion", "image optimization"]
  }
}
```

### Step 3 -- Cross-Reference With Existing Skills

Check skills-god manifest. If a skill already exists that covers this recommendation, mark as DUPLICATE and provide the existing skill name.

### Step 4 -- Generate Skill Spec

For novel recommendations, produce a skill spec draft:
- Name (kebab-case)
- Purpose (one sentence)
- Category (from marketplace taxonomy)
- Tier (QUICK/STANDARD/DEEP)
- Key process steps (3-5 bullets)
- Urgency (NOW/SOON/LATER)

### Step 5 -- Collect Into Report

Output structured as:
1. **Executive Summary** -- 2-3 sentence overview of what was learned
2. **Pattern Table** -- All extracted patterns with evidence and frequency
3. **Skill Recommendations** -- Build-ready skill specs
4. **Market Signals** -- Competitor mentions, gaps, trending terms
5. **Data Quality** -- Notes on what couldn't be extracted (gaps in input data)

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `source_data` | yes | -- | Raw text, file path, or reference to previous monitor output |
| `source_type` | yes | -- | community|reviews|competitor|technical|market |
| `depth` | no | standard | quick|standard|deep -- deep spawns per-pattern research agents |
| `cross_reference` | no | true | Whether to check existing skills-god manifest for duplicates |

## Output

Structured report with:
- Extracted patterns with evidence
- Build-ready skill specs
- Market gap analysis
- Duplicate detection
- Priority ranking

## Integration

- **Input from**: reddit-community-monitor, citation-intake-engine, manual market research
- **Output to**: self-assessment-meta-loop (for build decisions), STICKY.md priority queue
- **Triggered by**: Weekly community audit, user request, or after N community monitor runs

## Tools Used

- Read (for input data)
- File operations (for report output)
- Python3 (for text analysis, clustering)
- agent() (for per-pattern deep research in DEEP mode)

## Success Criteria

- Every extracted pattern has at least 1 evidence citation
- Skill recommendations are distinct from existing skills (0 duplicates ideally)
- Market signals include at least competitor names and gap descriptions
- Report is structured and consumable by self-assessment-meta-loop
