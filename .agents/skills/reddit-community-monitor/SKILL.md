---
name: "reddit-community-monitor"
description: "Monitor Reddit, Chinese forums (Xiaohongshu, Zhihu, Douban), and global community platforms for trending posts and brand mentions. Activates when users want to monitor communities, find trending posts, explore subreddits, run social listening, or track brand mentions across platforms."
license: MIT
metadata:
  tier: "STANDARD"
  category: "Market Intelligence / Social Listening"
triggers:
  - monitor subreddit {name}
  - find trending posts about {topic}
  - what's hot on {platform}
  - track mentions of {brand}
  - explore {subreddit}
  - find highly upvoted posts in {community}
  - social listening for {brand}
  - community monitoring for {topic}
  - what are people saying about {product}
  - competitor mentions on Reddit
  - trending discussions about {industry}
  - Xiaohongshu brand mentions
  - Hacker News top posts
  - forum monitoring
---

# Reddit Community Monitor

Cross-platform social listening and community intelligence tool for monitoring Reddit, Chinese forums (Xiaohongshu/RedNote, Zhihu, Douban), and global platforms (Hacker News, Lobsters) for trending posts, brand mentions, and competitor activity. Part of the CHORUS commerce intelligence brain.

---

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Process](#process)
- [Forums Monitored](#forums-monitored)
- [Output Format](#output-format)
- [Success Criteria](#success-criteria)
- [Tools Used](#tools-used)
- [Examples](#examples)
- [Installation](#installation)

---

## Purpose

Monitor Reddit (primary), Chinese forums (Xiaohongshu, Zhihu, Douban), and global community platforms (Hacker News, Lobsters) for:

- Highly-upvoted posts in relevant subreddits
- Brand/product mentions across platforms
- Trending discussions by topic or industry
- Competitor mentions and community sentiment
- Emerging patterns in commerce, ecommerce, and SaaS

Part of the CHORUS brain's market intelligence discipline -- feeds into competitive intelligence, content strategy, and product direction.

---

## When to Use

Activate this skill when users say any of the following:

| User says... | Skill routes to... |
|---|---|
| "monitor subreddit r/tea" | Subreddit exploration + top posts |
| "find trending posts about Shopify" | Topic search across all platforms |
| "what's hot on Hacker News" | HN frontpage + /show /ask |
| "track mentions of Red Blossom Tea" | Brand mention scan |
| "explore r/ecommerce" | Subreddit deep dive |
| "find highly upvoted posts in r/smallbusiness" | Top/weekly/monthly scoring |
| "social listening for {brand}" | Full brand mention sweep |
| "what are people saying about {product}" | Product mention scan |
| "competitor mentions on Reddit" | Competitor brand tracking |
| "Xiaohongshu brand mentions" | Chinese platform monitoring |
| "Hacker News top posts today" | HN frontpage snapshot |
| "forum monitoring for {topic}" | All-platform sweep |

---

## Process

### Phase 1: Subreddit Exploration

Discover and prioritize relevant subreddits by topic. Use domain knowledge plus the reddit-mcp tools to find active communities.

**Default interest categories and suggested subreddits (expandable via configuration):**

| Category | Subreddits |
|----------|------------|
| Ecommerce | r/shopify, r/ecommerce, r/smallbusiness, r/dropship, r/Entrepreneur |
| Tea | r/tea, r/teasales, r/teaindustry, r/puer, r/gongfutea |
| SaaS | r/SaaS, r/startups, r/EntrepreneurRideAlong |
| Marketing | r/marketing, r/digital_marketing, r/SEO, r/content_marketing |
| Tech | r/technology, r/programming, r/webdev, r/startups |
| Fashion | r/fashion, r/streetwear, r/malefashionadvice, r/femalefashionadvice |

Process:
1. Identify relevant subreddits from user's topic/brand/industry
2. Check subreddit activity level and subscriber count
3. Prioritize high-activity communities for deeper analysis
4. **Verification:** Subreddit exists and has recent activity (posts within last 24h)

### Phase 2: Highly-Upvoted Detection

Score posts by a weighted composite of upvote ratio, comment count, and recency.

**Scoring formula:**

```
relevance_score = (
    upvote_ratio * 0.35 +
    (comment_count / max_comment_count_in_set) * 0.25 +
    (1 - hours_ago / max_hours_in_window) * 0.20 +
    (post_karma / max_karma_in_set) * 0.20
)
```

**Time ranges for top posts:**
- `top/hour` -- Breaking discussions (past 1 hour)
- `top/day` -- Daily trending (past 24 hours)
- `top/week` -- Weekly best (past 7 days) -- default
- `top/month` -- Monthly highlights (past 30 days)
- `top/year` -- All-time greats (past 365 days)
- `top/all` -- Historical best (use sparingly)

**Thresholds:**
- Minimum upvote ratio: 0.70 (filters controversial/low-quality)
- Minimum comment count: 3 (filters drive-by posts)
- Exclude: removed/deleted posts, obvious spam, self-promotion without value

### Phase 3: Brand Mention Scan

Search for specific brand names, product names, and competitor names across forums.

**Scan targets:**
- Exact brand name (case-insensitive)
- Common misspellings and variants
- Product line or SKU references
- Competitor names (specified or auto-detected from category)

**What to capture:**
1. Post title and body (excerpt with context around mention)
2. Comment-level mentions (replies that reference the brand)
3. Sentiment signal (positive/negative/neutral via keyword heuristics)
4. Engagement around the mention (upvotes, replies on the mention thread)
5. Timestamp and platform

### Phase 4: Chinese Forum Monitoring

Chinese platforms require web-based scraping (no APIs available). Use WebFetch + web_search for these.

**⚠️ Reliability caveat:** Chinese platforms have no official APIs. All results are web-scraped — expect intermittent failures, CAPTCHA blocks, and incomplete data. This is the weakest link in the monitoring chain (expected success rate: ~40-60%). If a platform blocks, note the failure — do not retry.

**Security: Sanitize search keywords.** Before constructing platform URLs, sanitize the keyword:
```python
import re, urllib.parse
keyword = urllib.parse.quote(re.sub(r'[\x00-\x1f\x7f-\x9f​-‏ - ﻿]', '', keyword))
```
This strips control characters, zero-width characters, and unicode formatting characters that could be used for injection (preventing CWE-20/CWE-116 bypass).

**Xiaohongshu / RedNote (小红书):**
- Search for brand name in Chinese and English
- Focus on: product reviews, unboxing posts, haul posts
- Note: content is image-heavy -- read surrounding text and comments
- Platform URL: `https://www.xiaohongshu.com/search_result?keyword={keyword}` (URL-encode keyword via `urllib.parse.quote`)

**Zhihu (知乎):**
- Search for brand/topic in question-answer threads
- Focus on: expert opinions, detailed product comparisons, "how-to" threads
- Platform URL: `https://www.zhihu.com/search?type=content&q={keyword}` (URL-encode keyword)

**Douban (豆瓣):**
- Search for brand/product in group discussions
- Focus on: community reviews, niche interest groups, long-form discussion threads
- Platform URL: `https://www.douban.com/search?q={keyword}` (URL-encode keyword)

**Important notes for Chinese platforms:**
- Results are web-scraped -- expect incomplete or formatted-as-HTML data  
- **Expected reliability:** Xiaohongshu ~50-60%, Zhihu ~40-50%, Douban ~20-30% (frequently blocks scrapers)
- Rate-limit to 1 request per 3 seconds to avoid blocks
- ALWAYS output the platform reliability level with each result
- Translate key findings to English with original Chinese in parentheses
- **If a platform blocks web scraping, it MUST be reported in the output** -- a blocked platform is different from "no findings" and must be surfaced as a separate status

### Phase 5: Global Platform Monitoring

**Hacker News:**
- Frontpage: `https://news.ycombinator.com/` (scrape for top 30 posts)
- Show HN: `https://news.ycombinator.com/show` (for product/service launches)
- Ask HN: `https://news.ycombinator.com/ask` (for community questions)
- Search: `https://hn.algolia.com/api/v1/search?query={keyword}&tags=story`
- Focus on: Shopify ecosystem tools, ecommerce tech, SaaS launches
- Each finding: title, points, comment count, URL, timestamp

**Lobsters:**
- Frontpage: `https://lobste.rs/` (scrape for top stories)
- Search: `https://lobste.rs/search?q={keyword}`
- Focus on: tech community discussions, developer tooling

### Phase 6: Synthesis and Reporting

Rank all findings across platforms by a combined relevance + engagement score.

**Ranking factors:**
- Engagement volume (upvotes + comments)
- Recency (fresher = higher weight)
- Relevance to user's query (title/body keyword density)
- Platform authority (Reddit + HN weighted higher than less active communities)

**Output structure:**

```json
{
  "query": {
    "topic": "shopify ecommerce",
    "brand": null,
    "platforms_scanned": ["reddit", "hackernews", "xiaohongshu"],
    "timestamp": "2026-06-30T14:30:00Z"
  },
  "summary": {
    "total_findings": 12,
    "platforms_covered": 3,
    "top_platform": "reddit (8 findings)",
    "brand_mentions": 2,
    "avg_engagement_score": 0.74
  },
  "findings": [
    {
      "rank": 1,
      "platform": "reddit",
      "community": "r/shopify",
      "title": "Best Shopify apps for small businesses in 2026?",
      "url": "https://reddit.com/r/shopify/comments/...",
      "engagement": {
        "upvotes": 342,
        "comments": 89,
        "upvote_ratio": 0.94
      },
      "timestamp": "2026-06-29T10:15:00Z",
      "relevance_score": 0.92,
      "brand_mention": false,
      "tags": ["shopify", "apps", "small-business"]
    },
    {
      "rank": 2,
      "platform": "hackernews",
      "community": "Show HN",
      "title": "Show HN: I built a Shopify analytics tool that predicts churn",
      "url": "https://news.ycombinator.com/item?id=...",
      "engagement": {
        "points": 187,
        "comments": 43
      },
      "timestamp": "2026-06-28T08:30:00Z",
      "relevance_score": 0.88,
      "brand_mention": false,
      "tags": ["shopify", "analytics", "saas", "churn"]
    },
    {
      "rank": 3,
      "platform": "reddit",
      "community": "r/tea",
      "title": "Where to buy high-quality oolong tea online? Recommendations?",
      "url": "https://reddit.com/r/tea/comments/...",
      "engagement": {
        "upvotes": 156,
        "comments": 67,
        "upvote_ratio": 0.91
      },
      "timestamp": "2026-06-27T16:45:00Z",
      "relevance_score": 0.85,
      "brand_mention": true,
      "brands_mentioned": ["Red Blossom Tea", "Yunnan Sourcing", "White2Tea"],
      "tags": ["tea", "oolong", "recommendations"]
    }
  ],
  "brand_mentions": [
    {
      "brand": "Red Blossom Tea",
      "mentions": 1,
      "platforms": ["reddit"],
      "sentiment": "positive",
      "top_post": "Where to buy high-quality oolong tea online..."
    }
  ],
  "chinese_platforms": {
    "xiaohongshu": {
      "status": "scraped",
      "findings": 3,
      "note": "Web-scraped results may be incomplete. No official API available."
    },
    "zhihu": {
      "status": "scraped",
      "findings": 1,
      "note": "Results limited by web scraping. Consider manual verification for critical mentions."
    },
    "douban": {
      "status": "blocked",
      "findings": 0,
      "note": "Douban blocked the web request. Manual check recommended."
    }
  },
  "recommendations": [
    "Monitor r/shopify daily -- 89 comments on the app recommendations thread indicates strong community interest",
    "The HN Show HN post about churn prediction is relevant -- consider reaching out to the builder",
    "r/tea has an active recommendation thread mentioning RBT -- consider engaging with brand advocates"
  ]
}
```

---

## Forums Monitored

### Configured (expandable via configuration file or inline overrides)

| Platform | Method | API Available | Reliability |
|----------|--------|---------------|-------------|
| Reddit | `reddit-mcp` tools | Yes (via MCP) | High -- official tooling |
| Hacker News | WebFetch + Algolia API | Yes (free API) | High -- Algolia API is stable |
| Lobsters | WebFetch + search | Partial (web scrape) | Medium -- HTML scraping |
| Xiaohongshu / RedNote | WebFetch + keyword search | No | Low-Medium -- web scrape only, may be blocked |
| Zhihu | WebFetch + topic search | No | Low-Medium -- web scrape only |
| Douban | WebFetch + group search | No | Low -- frequently blocks scrapers |

### Adding a new platform

1. Add platform name to the process checklist
2. Determine API status (official, reverse-engineered, or web-scrape)
3. Update the Forums Monitored table
4. Add note in the Synthesis output's platform section

---

## Output Format

### Quick Report (default, 3-5 findings)

```
## Community Monitor Report
**Topic:** shopify ecommerce | **Scanned:** 3 platforms | **Findings:** 12

### Top Findings
1. **[Reddit] r/shopify** -- "Best Shopify apps for small businesses in 2026?"
   Score: 0.92 | 342 upvotes, 89 comments | Jun 29
   → https://reddit.com/r/shopify/comments/...

2. **[HN] Show HN** -- "I built a Shopify analytics tool..."
   Score: 0.88 | 187 points, 43 comments | Jun 28
   → https://news.ycombinator.com/item?id=...

### Brand Mentions
- Red Blossom Tea: 1 mention (positive, r/tea thread)

### Chinese Platforms
- Xiaohongshu: 3 findings (scraped, may be incomplete)
- Zhihu: 1 finding
- Douban: blocked

### Recommendations
- Engage in r/shopify app recommendations thread
- Monitor HN Show HN for potential partnership
```

### Full Report (JSON, for programmatic consumption)

See JSON structure in [Process Phase 6](#phase-6-synthesis-and-reporting).

---

## Success Criteria

- [ ] **At least 4 platforms scanned** (Reddit + 3 others, or all available for the query)
- [ ] **Every finding has engagement metrics** (upvotes, comment count, or equivalent)
- [ ] **Brand mentions are clearly flagged** with brand name, platform, and sentiment signal
- [ ] **Chinese platform sources are noted** with "Web-scraped, may be incomplete" caveat
- [ ] **Output includes recommendations** -- actionable signals, not raw data
- [ ] **Platform failures are reported** -- a blocked platform is noted, not silently dropped
- [ ] **Scored and ranked** -- all findings include a relevance_score (0.0-1.0)
- [ ] **Results list is deduplicated** -- same post scraped from multiple endpoints appears once
- [ ] **Timeout handled gracefully** -- if a platform takes >10s, skip and note the timeout

---

## Tools Used

| Tool | When | What For |
|------|------|----------|
| `reddit-mcp` tools (get_subreddit_hot_posts, get_subreddit_top_posts, get_subreddit_new_posts, get_subreddit_info) | Every scan | Primary Reddit monitoring -- hot/top/new posts, subreddit metadata |
| `mcp__aeo-platform__web_search` (Tavily) | Keyword discovery, Chinese platform fallback | Topic research when subreddits aren't known; broad brand mention search |
| WebFetch | HN, Lobsters, Chinese platforms | HTML scraping of platforms without APIs |
| Python3 | Data processing | Scoring, deduplication, JSON formatting |
| Bash (curl/jq) | HN Algolia API | Fast HN search without HTML scraping |

---

## Integration Contract

**Role in CHORUS flywheel:** Stage 1 (Monitor) — social listening and brand mention discovery.

This skill's OUTPUT feeds into the brand intelligence pipeline (citation-intake-engine and brand-profile-decoder). Its findings enrich the BrandProfile schema at `src/aeo/schemas/brand_profile.py`.

**Output contract (to brand intelligence pipeline):**
```json
{
  "platform": "reddit|xiaohongshu|zhihu|douban|hn|lobsters",
  "scan_type": "subreddit_depth|keyword_discovery|brand_mention|trending",
  "query": "original search term",
  "security_checks": {"keyword_sanitized": true, "control_chars_removed": true},
  "results": [
    {
      "platform": "...",
      "title": "...",
      "url": "...",
      "score": 0,
      "relevance_to_brand": "high|medium|low",
      "key_phrase": "brand-relevant excerpt"
    }
  ],
  "platform_reliability": {
    "platform_name": "expected success rate note",
    "blocked": false
  },
  "gaps": ["platforms that returned no results"]
}
```

**Contract rules:**
- All search keywords must be sanitized (control characters stripped, URL-encoded)
- Blocked or rate-limited platforms reported explicitly — not conflated with "no findings"
- Chinese forum reliability expectations documented per-platform (Xiaohongshu ~50-60%, Zhihu ~40-50%, Douban ~20-30%)
- Results include relevance scoring for brand pipeline consumption
- Schema conforms to the shared intelligence format defined alongside BrandProfile

## Examples

### Example 1: Subreddit Deep Dive

**User:** "Explore r/tea for trending posts this week"

**Skill output (abbreviated):**

```
## r/tea -- Weekly Trending (week of Jun 24-30)

Posts scanned: 25 (top/week)
Average upvote ratio: 0.87
Top categories: brewing advice (40%), product recommendations (30%), reviews (20%), industry (10%)

### Top 5 Posts
1. "Where to buy high-quality oolong tea online?" -- 156 upvotes, 67 comments
   → Brand mentions: Red Blossom Tea, Yunnan Sourcing, White2Tea
   → Sentiment: positive recommendations, multiple commenters agreeing

2. "Beginner gongfu setup under $100" -- 134 upvotes, 45 comments
   → Equipment recommendations from community

3. "Is pu'erh worth the hype?" -- 98 upvotes, 72 comments
   → Heated debate, strong opinions on both sides

4. "Review: Spring 2026 green teas comparison" -- 87 upvotes, 23 comments
   → Detailed tasting notes, seasonal interest

5. "Best tea subscriptions 2026" -- 76 upvotes, 51 comments
   → Mei Leaf, White2Tea, Yunnan Sourcing mentioned repeatedly

### Key Signals for RBT
- Positive recommendation in post #1 (oolong thread)
- No negative mentions detected
- Competitor mentions: Yunnan Sourcing (7), White2Tea (5), Mei Leaf (3)
- Opportunity: Post #5 (subscriptions) -- RBT has no subscription offering
```

### Example 2: Brand Mention Scan

**User:** "Track mentions of Red Blossom Tea Company across all platforms"

**Skill output (abbreviated):**

```
## Brand Mention Scan: Red Blossom Tea Company

Scanning 6 platforms... Done.

### Reddit -- 2 mentions
1. r/tea -- "Where to buy..." post (recommended by /u/tealover42)
   → "Red Blossom Tea has the best Tieguanyin I've ever had"
   → 12 upvotes on the comment
2. r/teasales -- "July 4th sale at Red Blossom Tea" (crosspost)
   → 23 upvotes, 5 comments

### Hacker News -- 0 mentions
### Lobsters -- 0 mentions

### Xiaohongshu -- 1 mention
→ User post: "美国买茶推荐" (Tea recommendations in the US)
→ Mentions RBT alongside other vendors
→ Note: Web-scraped, may be incomplete

### Zhihu -- 0 mentions
### Douban -- blocked

### Summary
| Metric | Value |
|--------|-------|
| Total mentions | 3 |
| Positive | 3 |
| Neutral | 0 |
| Negative | 0 |
| Platforms with activity | 2 of 6 |
| Competitor comparison | Yunnan Sourcing: 7 mentions across 3 platforms |
```

### Example 3: Cross-Platform Topic Monitor

**User:** "Find trending posts about Shopify ecommerce"

**Skill output (abbreviated):**

```
## Topic Monitor: Shopify Ecommerce
**Scanned:** Reddit, HN, Lobsters, Xiaohongshu | **Time window:** Past 7 days

### Reddit (8 findings)
1. r/shopify "Best apps 2026" -- 342▲ 89💬 R:0.92
2. r/ecommerce "Shopify vs WooCommerce 2026" -- 234▲ 156💬 R:0.91
3. r/smallbusiness "Started on Shopify, here's what I learned" -- 198▲ 45💬 R:0.87
4. r/dropship "Shopify dropshipping margins 2026" -- 167▲ 34💬 R:0.83
5. r/Entrepreneur "Quit my job to build a Shopify store" -- 145▲ 78💬 R:0.81
6. r/shopify "Shopify SEO tips that actually work" -- 123▲ 28💬 R:0.79
7. r/shopify "Shopify B2B feature review" -- 89▲ 41💬 R:0.76
8. r/webdev "Building Shopify themes with Hydrogen" -- 67▲ 33💬 R:0.72

### Hacker News (3 findings)
1. Show HN "Churn prediction for Shopify" -- 187● 43💬 R:0.88
2. Ask HN "What Shopify stack do you use?" -- 92● 67💬 R:0.78
3. "Shopify's Q2 earnings preview" -- 78● 23💬 R:0.65

### Lobsters (1 finding)
1. "Shopify's approach to edge computing" -- 34▲ 12💬 R:0.58

### Xiaohongshu (0 Shopify-specific findings)

### Top Signals
- Strong community interest in app recommendations (89 comments)
- Platform comparison (Shopify vs WooCommerce) is the most discussed thread (156 comments)
- HN interest in Shopify-adjacent tooling (churn prediction, Hydrogen)
```

---

## Installation

```bash
bash claude-skills-marketplace/.agents/skills-god.sh ensure reddit-community-monitor
```

Or if using the marketplace installer:

```bash
bash claude-skills-marketplace/.agents/install.sh reddit-community-monitor
```

### Prerequisites

- `reddit-mcp` MCP server must be registered in `~/.claude.json` (provides `get_subreddit_hot_posts`, `get_subreddit_top_posts`, etc.)
- `mcp__aeo-platform__web_search` (Tavily) or equivalent web search tool
- WebFetch tool must be available for HN/Lobsters/Chinese platform scraping
- Python3 with `json` module (stdlib) for data processing

### Configuration

Platform list is hardcoded in this skill as a sensible default. To customize:

1. Add filtered platform list to your query (e.g., "Reddit + HN only")
2. Or extend the skill with a `platforms.yaml` config file in the skill directory
