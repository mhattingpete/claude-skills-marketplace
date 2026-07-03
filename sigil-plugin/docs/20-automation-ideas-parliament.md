# 20 Automation Product Ideas — Parliament of Experts

**Generated:** 2026-07-01
**Source:** Reddit Pain Researcher baseline report (`reddit-pain-report-2026-07-01.md`)
**Panel:** Engineering (systems), Product (needs), Growth (distribution), Sales (signals), Operations (viability)

---

## Top 10 (ranked by build-time-to-impact)

| Rank | Idea | Pain Point | Build Time | Distribution |
|------|------|-----------|-----------|-------------|
| 1 | Freelance Client Risk Score API | Client hell (non-payment, harassment) | 3 days | Reddit crosspost with nightmare stories |
| 2 | Lead Lag Dashboard | Execution gap (leaky bucket) | 2 days | Founder Twitter, r/Entrepreneur |
| 3 | Follow-up Coach Email Generator | Lead follow-up paralysis | 3 days | r/smallbusiness, Zapier alternatives |
| 4 | Scope Creep Radar | Client hell, pricing paralysis | 4 days | r/freelance, freelance forums |
| 5 | Trade Show ROI Forecaster | Trade show inefficiency | 3 days | Conference organizers, r/sales |
| 6 | Reddit Pain Index Dashboard | All (meta) | 1 week | Viral chart share + VC subscription |
| 7 | Commission Parser + Visualizer | Commission opaqueness | 1 week | r/sales grassroots |
| 8 | N8n Template Marketplace | All 13 pain points | 2 weeks | SEO + Reddit + Product Hunt |
| 9 | Procurement Pathfinder | Procurement surprises | 2 weeks | Direct sales outreach |
| 10 | Resignation Risk Detector | Quality-of-hire collapse | 2 weeks | r/recruiting, HR Tech |

---

## Full 20 Ideas

### Engineer (systems architect lens)

1. **Freelance Client Risk Score API** — Score prospective clients 0-100 based on contract behavior, payment speed, communication volume, and review history. Save 6 months of unpaid follow-up. n8n workflow: client email -> reverse-entity search -> public records -> review sentiment -> score.

2. **Invoice-to-Receipt Reconciliation Bot** — Match deposits to invoice line items. Flag partial vs over-payment. Auto-apply to correct invoice in QBO/Xero. Hits: "Some of the amounts flowing through Shopify are actually A/R collections."

3. **Multi-Entity Expense Router** — LLM reads memo/vendor/amount from bank feed, routes expense to correct LLC entity in QBO. Catches "whichever card was convenient" syndrome. n8n: bank webhook -> LLM classify entity -> QBO split -> alert if ambiguous.

4. **AI Procurement Pathfinder** — Scrapes prospect LinkedIn org chart + SEC filings + past RFPs + vendor lists. Spits out procurement process map before first meeting. Attach to every deal >= $50k. Hits: "Finding out far too late about new hurdles and approvals."

5. **Commission Parser + Visualizer** — Feed comp plan PDF. Output: per-deal earning calculator, quota attainment dashboard, scenario planner ("close 3 small deals vs 1 big one"). Hits the $22-on-$76K pain (213 upvotes).

### Product Manager (user needs lens)

6. **Monthly Pain Trends Report ("The Pain Index")** — Productized Reddit sweep as recurring deliverable. Trend heatmap of what's getting worse across 15 subreddits. Sell to VCs, founders, product teams for $200/mo.

7. **Trade Show ROI Forecaster** — Input: booth cost, travel, team hours, target industry. Output: expected leads, conversion, "better uses for this $50k" alternatives. Matches: "dropped 50k on a booth and got four leads."

8. **Recruiting Quality Scorecard Enforcement Tool** — Structured interview scorecard that blocks candidate advancement without completion. Tie to 90-day retention data. Hits: "they 'knew' the hire would be bad but picked the least bad" (+123).

9. **Scope Creep Radar for Freelancers** — Tracks hours per revision, change request frequency, client message sentiment drift. Alerts at "this client is entering fire territory." Hits the Nightmare Client From Hell pattern (34 upvotes, 100+ comments).

10. **Lead Lag Dashboard** — Measures: time from lead capture to first contact, quote to follow-up, demo to proposal. Green < 1hr, yellow < 24hr, red > 24hr. Hits: "fixed that before touching the ad budget and conversion went up."

### Growth (distribution lens)

11. **N8n Workflow Template Marketplace** — Curated downloadable n8n JSON templates for each of the 13 pain points. First 3 free. Deep ones at $29-$99. SEO: "n8n workflow for prospect list qualification."

12. **"Automate Your Annoying Thing" Referral Engine** — Landing page: pick your profession -> pick what's annoying you -> get a 5-minute n8n workflow. Reddit crosspost into every researched subreddit.

13. **Reddit Pain Index (public dashboard)** — Real-time heatmap. 30 subreddits. Pain scores by category. Free public version for awareness. Paid API for VCs/startups doing market research.

14. **Follow-up Coach Email Sequence Generator** — Input: prospect name, company, conversation context. Output: 5-email personalized follow-up sequence. One-click deploy. Hits: "I lose potential clients because I don't follow up."

15. **Freelance Onboarding Bot** — New client signed -> Bot sends welcome packet -> collects scope -> generates contract -> collects deposit -> sets milestones -> creates timeline. Zero effort from freelancer.

### Sales (buying signal lens)

16. **"MQL is Dead" Intent Alert System** — Crawl prospect behavior: pricing page opened 3x? Case study viewed? RFP downloaded? Alert rep: "This one is ready. Call now." Hits execution gap.

17. **Auto RFP Responder (Small Business Edition)** — Not $50k enterprise tools. Simple n8n: PDF RFP received -> LLM extracts requirements -> matches capabilities -> fills pricing template -> human reviews 3 bullet points. Hits procurement pain.

18. **Resignation Risk Detector** — Scan Glassdoor/Blind/Fishbowl for company name + "toxic"/"looking"/"exit." Cross-reference with GitHub commit velocity, Slack activity drops. Flag at-risk employees before they quit.

19. **Trade Show Lead Router** — Scan badges. Auto-scores, adds to CRM, sends personalized follow-up referencing what they asked about. Follow-up sent before you leave the convention center. Hits 161-upvote broken trade show thread.

20. **Freelance Financial Stability Analyzer** — Connects to Stripe/PayPal/invoicing. Predicts lean months, needed clients to hit target, and dangerous concentration (>30% from one client). Nudges before the lean month hits.
