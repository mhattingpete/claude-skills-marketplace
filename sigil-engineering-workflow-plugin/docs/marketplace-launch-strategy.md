# Sigil Marketplace Launch Strategy

**Synthesized from 5-lens 360 review of all distribution channels.**
Sigil Project · 2026-06-30

---

## Summary

Five independent expert lenses (Engineering, Security, UX, CEO/Strategy, QA) reviewed every viable distribution channel for Sigil-certified skills. The unanimous finding: **Anthropic's official marketplace is the only distribution channel with structural ROI worth investing in at launch.** Everything else is secondary — listed as necessary for completeness, but not worth custom engineering effort.

---

## Channel Rankings

| Priority | Channel | ROI | Effort | Dependency | Launch Phase |
|----------|---------|-----|--------|------------|-------------|
| **1** | Anthropic official marketplace (`claude-plugins-official`) | HIGH | Submit plugin per guidelines | Need Anthropic to accept submissions | Phase 1 |
| **2** | GitHub README + star growth | HIGH | Polish demo GIF, share socially | Content creation only | Phase 1 |
| **3** | Product Hunt | MEDIUM | Upcoming page 4wk early, hunter, email list | Need stars + installs first | Phase 3 |
| **4** | Hacker News (Show HN) | MEDIUM | Technical write-up | Need PH success first | Phase 4 |
| **5** | Reddit (r/SideProject, r/SaaS) | MEDIUM | Build karma 2-4wk, cross-post on schedule | Need karma pre-build | Phase 2 |
| **6** | Smithery | LOW | Auto-listed from GitHub (zero effort) | GitHub stars = ranking | Ongoing |

---

## Key Findings by Lens

### Engineering
- Smithery's power-law distribution (0.3% of servers get 50k+ installs; median = ~3,100) makes organic discovery impossible without star history. Not worth active investment.
- Anthropic marketplace is already live (`claude-plugins-official`). Being first certification authority on the platform is category-defining.
- GitHub star counts directly influence both Smithery and Anthropic marketplace ranking.

### Security
- Smithery has a confirmed path traversal vulnerability history (GitGuardian, Jun 2025, 3,000+ servers exposed API keys). Never host Sigil's certification infrastructure on Smithery's runtime — directory listing only.
- Anthropic's marketplace has **zero** malware scanning, signature verification, or sandboxing for plugins. This is both a risk (impersonation attacks) and an opportunity (Sigil's certification is the missing trust layer).
- Multi-platform impersonation ("sigil-pro" lookalikes) is the highest-probability attack once Sigil gains traction. Register `sigil` namespace on ALL plugin hubs preemptively.

### UX
- Sigil's core challenge: it's a tool that *judges* code, not a tool that *builds* code. "Judgment" tools have higher onboarding friction — users must have something worth judging first.
- **Critical decision**: Animate the demo GIF showing agents disagreeing on a finding. A unanimous verdict looks staged. Showing one agent flagging a security issue while another praises the design proves the multi-perspective claim is real.
- GIF spec: 15 seconds max, 80x24 terminal, <2MB, four scenes: install → run on `auth.py` → show a disagreement → reveal certificate.

### CEO/Strategy
- **Open-core risk**: If the paid tier doesn't exist on day 1 of public launch, the community self-hosts and has no reason to upgrade. Build Pro tier (Stripe + license key validation) before any public launch.
- Market is wide open — no certification authority exists for Claude Code skills. Time-to-competition is measured in weeks, not months.
- Bundling strategy: Sigil Core (free, 5-panelist review) → Sigil Pro ($19/mo, team queues, CI integration) → Sigil Enterprise ($99/mo+, on-premise runtime, SLA)

### QA
- LLM-as-judge stochasticity is the fundamental reliability threat. Same code, different scores on consecutive runs = worthless certificate. Mitigation: run each lens 2x and average, flag runs with >15% variance.
- Data sovereignty: **every listing must explicitly say "LOCAL ONLY — code never leaves your machine."** This alone removes the biggest adoption blocker.

---

## Action Items

### Pre-Launch (this week)
- [ ] Register `sigil` namespace on all discoverable plugin hubs (Smithery, Anthropic, community manifests)
- [ ] Build demo GIF: asciinema + agg, 15s, showing 5-agent review with visible disagreement
- [ ] Add "LOCAL ONLY — code never leaves your machine" to every listing description
- [ ] Create Stripe + license validation for Sigil Pro tier (even if $0/draft — the plumbing must exist)

### Phase 1 (week 1-2): Anthropic Marketplace + GitHub
- [ ] Submit sigil plugin to `claude-plugins-official` per Anthropic's developer guidelines
- [ ] Optimize GitHub README for Smithery auto-indexing (keywords: code-review, code-quality, certification)
- [ ] Push repo stars via tweet by Alice/Charles + technical sharing on social

### Phase 2 (week 2-4): Reddit + Community
- [ ] Build 2-4 weeks of genuine Reddit karma (r/MachineLearning, r/programming, r/devops)
- [ ] Post technical write-up to r/SideProject: "We audited the most popular Claude Code skill. Here's what we found wrong."
- [ ] Cross-post to r/alphaandbetausers (most permissive self-promo sub)

### Phase 3 (week 4-5): Product Hunt
- [ ] Create "Upcoming" page 3-4 weeks in advance
- [ ] Onboard an established hunter from the AI/devtools space
- [ ] Seed email list from GitHub stars + Reddit interest

### Phase 4 (week 5-6): Hacker News
- [ ] Show HN post: "Sigil — Multi-Perspective Code Certification with Adversarial Agent Review"
- [ ] **Do NOT use "AI" in the HN title** (triggers spam filter)
- [ ] Post Tuesday 8am PT for best front-page timing

---

## Launch Checklist (per-channel)

### All Channels
- [ ] Architecture label: "LOCAL ONLY — code never leaves your machine"
- [ ] Link to GitHub repo with demo GIF
- [ ] Link to Sigil certificate verification docs
- [ ] Support contact (GitHub Issues or Discord)

### Anthropic Marketplace
- [ ] Determine submission process (gated application or open?)
- [ ] Optimize 3-line truncated description to include "certification authority"
- [ ] Tagline: "5 AI experts certify your code before you ship it"

### Smithery
- [ ] GitHub repo must have README with `code-review` and `code-quality` in first paragraph
- [ ] smithery.yaml pointing to a specific commit SHA (not branch — supply chain safety)
- [ ] Pin to tag, not branch

### Product Hunt
- [ ] 10+ real certificate outputs to show
- [ ] 5 beta users willing to comment on launch day
- [ ] Do NOT launch until existing install base exists (PH amplifies existing interest, doesn't create it)

### Hacker News
- [ ] Pre-write response to "why not just use ruff + code review" — this WILL be the top comment
- [ ] Technical methodology post, not a product launch
- [ ] Show adversarial architecture (5 agents must disagree to be trustworthy)

### Reddit
- [ ] Title: problem-framed, not feature-framed: "I built 5 AI agents that have to DISAGREE before certifying code"
- [ ] Post in self-promo thread (r/SideProject), not standalone link post
- [ ] Account must have 500+ karma before posting
- [ ] Wait 60 days between posts on same subreddit

---

## Metrics to Track

| Metric | Target | Channel |
|--------|--------|---------|
| GitHub stars | 50-100 pre-launch → 300+ post-PH | All |
| PH upvotes | 200+ (realistic first launch) | Product Hunt |
| HN front page | 50-100 upvotes in first 2 hours | Hacker News |
| Reddit upvotes | 50-100 per post | Reddit |
| Plugin installs | 100+ in first month | Anthropic marketplace |
| Smithery installs | Any (auto-listed, passive) | Smithery |

---

## Appendix: What a "Done" Launch Looks Like

1. Sigil plugin is searchable and installable from Anthropic's official marketplace
2. GitHub README has a compelling 15-second demo GIF showing multi-agent review with visible agent disagreement
3. Product Hunt page has 200+ upvotes with 5+ real user comments
4. HN Show HN post has 50+ points and a productive discussion thread
5. Reddit r/SideProject post has 100+ upvotes driving GitHub traffic
6. Smithery auto-listings show 20+ installs (passive)

Anything less than this means the channel isn't working yet — not that the channel is broken.
