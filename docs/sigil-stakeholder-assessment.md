# 360 Stakeholder Assessment + Paradigm Improvement for Sigil

**Date:** 2026-06-30
**Method:** Stakeholder mapping across Sigil's 4 defensible moat items.

---

## The 4 Moat Items

| Moat | Description | Type |
|------|-------------|------|
| Sigil Certification | 5-lens review + structured certificates | Protocol/Standard |
| readme-doctor | README audit + rewrite pipeline | Tool/Skill |
| reddit-research | Reddit MCP research engine | Tool/Skill |
| 360-review | User story generator | Tool/Skill |

---

## Stakeholder Analysis

### 1. Skill Authors / Plugin Developers

**Uses:** Certification, readme-doctor, 360-review

**What they need:**
- Trust signal to stand out in a flooded marketplace (425 plugins in jeremylongshore alone)
- Feedback on their skill before publishing — what's wrong, what's overclaimed
- A way to prove quality without self-assessment
- README that converts — they're devs, not marketers

**Pain points:**
- r/claudeskills "Why are all skill files pointless" (185 upvotes) — they know their READMEs are bad
- No way to differentiate from low-effort "you are an expert" prompts
- Self-assigned quality scores are meaningless (jeremylongshore's 100-point rubric)

**Current workaround:** None. They guess. They publish. They hope.

**Sigil value:** Clear — certification is the only external trust signal in the ecosystem. readme-doctor fixes their worst blind spot (README quality).

---

### 2. Marketplace Operators (Anthropic, Vercel, jeremylongshore, Smithery)

**Uses:** Certification (as an integration), Badge API

**What they need:**
- Reduce fraud and low-quality listings — spam erodes marketplace trust for everyone
- Differentiation — "Our marketplace has Sigil-certified skills" vs "ours has everything"
- Automated quality gate — don't want to hire a human review team

**Pain points:**
- Zero infrastructure for quality control
- Making skills discoverable without ratings/reviews feel like an unsolved problem
- Liability concern: if a malicious skill exfiltrates data, the marketplace is at fault

**Current workaround:** None. Manual takedowns after incidents.

**Sigil value:** Potential — if Sigil becomes the quality gate for their marketplace, they outsource trust to us. This is a B2B play.

---

### 3. Enterprise Buyers / Compliance Officers

**Uses:** Certification (as audit trail)

**What they need:**
- "Which Claude Code skills are safe for my team to use?"
- Audit trail — evidence that a third party reviewed the skill
- Security and compliance coverage (ISO 27001 skills, SOC 2 skills, GDPR)

**Pain points:**
- Can't evaluate 425 plugins individually
- Corporate approved vendor lists have no AI skill equivalent
- No boundary: does this skill read my files? Send data externally? Modify git history?

**Current workaround:** Ban all skills. Default deny. Miss the productivity gain.

**Sigil value:** Goldmine. Enterprise will pay for certified skill registries. This is the $5k/month-per-client market.

---

### 4. Open Source Maintainers

**Uses:** Certification, readme-doctor

**What they need:**
- Trust signal for their OSS project's README/docs
- Catch overclaiming before users file issues

**Pain points:**
- READMEs grow stale, overclaim, or misrepresent what the code actually does
- Documentation is the last thing maintained

**Current workaround:** Peer review (slow, inconsistent)

**Sigil value:** Moderate — readme-doctor is the main draw. Certification for OSS libraries is a new market.

---

### 5. Beginner Claude Code Users

**Uses:** reddit-research, Certification (as discovery)

**What they need:**
- "Which skill should I install first?"
- "Is this skill safe to use?"
- "How do skills even work?"

**Pain points:**
- Overwhelmed by choice (425+ plugins, 2800+ skills)
- No way to evaluate quality
- Official docs are inadequate — Reddit is the real learning resource
- 90% of tutorials are "waste of time" per community consensus

**Current workaround:** Go to Reddit. Ask. Hope someone answers.

**Sigil value:** Huge — Sigil registry as "the list of skills worth installing." reddit-research as the beginner's guide to what people actually use.

---

### 6. Agency / Service Providers (custom skill builders)

**Uses:** Certification, readme-doctor

**What they need:**
- Certify client deliverables
- Charge premium for "Sigil-certified" skills

**Pain points:**
- Client doesn't know if they're getting quality or a prompt wrapper
- The $5k/month seller from r/claudeskills built an agency

**Current workaround:** Reputation. Word of mouth.

**Sigil value:** Certification becomes a commercial differentiator for their proposals.

---

### 7. Competitors (Superpowers, jeremylongshore)

**Uses:** None directly (competitive)

**What they do:**
- **Superpowers (242K stars):** Full SDLC workflow. No certification, no quality standard.
- **jeremylongshore (2.5K stars):** Quantity play. 425 plugins. Self-assigned 100-point scores.
- **Vercel skills.sh:** Quality-adjacent (paid tiers imply curation) but no explicit certification.

**Our gap they could exploit:**
- Superpowers could add a review step to their 7-step workflow
- Vercel could partner with Anthropic to create an official certification

**Their gap we exploit:**
- None of them have a trust standard. Superpowers is workflow, not verification.
- jeremylongshore's scores are self-assigned — we can call this out publicly.

---

## ═══ PARADIGM IMPROVEMENT ═══

### The Problem: Certification as a Static Artifact

Right now, Sigil certification is a **document**: you submit → review → certificate.json → done. This is better than nothing, but:

1. The certificate expires (90 days) but no one checks
2. A skill can change between reviews — cert says "clean" but the code now has malware
3. Cross-marketplace trust is zero — a cert from our plugin means nothing on Smithery
4. No network effects — more certs don't make the next cert more valuable

### The Paradigm Shift: **Sigil Trust Protocol**

Shift from **"Sigil the tool"** (you run it) to **"Sigil the protocol"** (marketplaces embed it).

```
Current:  Skill → submit to Sigil → certificate.json → done
Paradigm: Skill ↔ Sigil Badge API [live] ↔ 5+ marketplaces [embedded] ↔ users [continuous trust]
```

### What changes

| Dimension | Current (Tool) | Paradigm (Protocol) |
|-----------|---------------|---------------------|
| Model | You run Sigil | Sigil always monitors |
| Output | Certificate file | Live badge + trust score |
| Reach | One repo | Cross-marketplace |
| Economics | Free/OSS | Badge API free + premium registry + enterprise |
| Trust signal | Static | Dynamic (updating) |
| Entry point | User's `sigil review` | Marketplace's `Sigil Certified` badge |

### Components

**1. Sigil Badge API** — universal trust token

A lightweight, persistent trust signal that any marketplace can embed:
- `GET /.sigil/badge?skill=<name>&version=<semver>` → `{"verified": true, "score": 92, "expires": "2026-09-28"}`
- Returns an SVG badge or JSON for API consumption
- Marketplaces render it next to the skill name: `[Sigil Certified ✅ 92/100]`
- Marketplace just embeds an image/API call — no integration complexity

**2. Continuous Re-Certification Engine**

Skills aren't certified once — they're continuously monitored:
- **Dependency scan**: when a critical CVE drops, re-check all skills for exposure
- **Model update**: when Fable 5 goes GA, re-check all skills optimized for Opus 4.8
- **Content drift**: if a skill's SKILL.md changes after certification, flag for re-review
- **Version pinning**: each version is independently certified — `v1.0` cert ≠ `v1.1` cert
- **Stale alert**: auto-notify skill authors 30 days before cert expiration

This solves: the SECURITY FAIL from the assessment. Continuous monitoring catches what a static cert misses.

**3. Cross-Marketplace Revocation**

If a skill author is found to have malicious intent on ANY marketplace:
- Sigil revokes across ALL marketplaces simultaneously
- Users who installed the skill via any marketplace get a revocation alert
- This is the nuclear option — creates trust because it's a real enforcement mechanism

**4. Sigil Trust Score (0-100)**

| Weight | Factor | Source |
|--------|--------|--------|
| 60% | Review quality | 5-lens panel verdict (PASS/BLOCKER count) |
| 15% | Responsiveness | Author's time-to-fix reported issues |
| 10% | Freshness | Time since last version + cert validity |
| 10% | Community signal | GitHub stars, install count, issue resolution |
| 5% | Marketplace diversity | Available on N marketplaces |

This is the **quantifiable quality signal** that no marketplace provides. A skill with 92/100 means something concrete.

**5. Sigil Registry** — public searchable database

```
sigil.sh/search?q=code+review&min_score=80&domain=security
→ Found 12 certified skills matching "code review"
→ [Sigil Certified ✅ 92/100] code-review-mcp · smithery.com
→ [Sigil Certified ✅ 87/100] security-audit · anthropic marketplace
→ ...
```

- Community-curated directory of all certified skills
- Searchable by domain, score, marketplace, price
- "Only Sigil-certified skills" filter
- Never hosts skills — just links out to marketplaces (no hosting liability)

### Why This Is Paradigm-Level

**The incumbents can't copy this easily:**
- **Superpowers** (242K stars) is a workflow tool. Adding certification means building 5 expert agents, a badge API, a registry, and a cross-marketplace revocation system. That's not their core competency.
- **jeremylongshore** is quantity-first. 100-point scores are self-assigned — switching to verified scores means admitting their scores were meaningless.
- **Vercel/Anthropic** could build this but it's an "everyone's second priority" feature. Neither has shown any movement on it.

**Network effects kick in:**
1. More certified skills → registry is useful → more users check it → more authors want certs
2. More marketplaces embed badges → badges become expected → universal trust standard
3. Continuous monitoring makes certs MORE valuable over time (not less, like static certs)

**Revenue paths:**
- Regulated for free, Badge API free for marketplaces
- Registry premium: skill authors pay for featured placement in search results
- Enterprise: certified skill whitelist for corporate teams ($50-200/mo)
- Continuous monitoring: paid tier for authors who want auto-re-certification
- Cross-marketplace revocation: premium service for marketplace operators

### Build Order

| Phase | What | Duration |
|-------|------|----------|
| Phase 1 | Sigil Registry MVP — searchable cert database | 1 week |
| Phase 2 | Badge API — SVG + JSON endpoint, embed docs | 3 days |
| Phase 3 | Continuous monitoring — CVE scanning, drift detection | 2 weeks |
| Phase 4 | Cross-marketplace revocation — notification system | 1 week |
| Phase 5 | Enterprise certified whitelist — paid tier | 2 weeks |

### Risk

- **If Anthropic builds certification natively**: Our protocol becomes a spec, not a service. Mitigation: partner early (before they build it).
- **If Superpowers adds review step**: They'd need 5 expert agents and evidence markers. Possible but expensive. Mitigation: our certification is already deeper than a simple review step.
- **Adoption chicken-and-egg**: No certs → no badges → no registry value. Mitigation: pre-certify top 50 skills from the community, seed the registry, show value immediately.

---

## Summary Verdict

| Lens | Grade | Why |
|------|-------|-----|
| Engineering | PASS | All components are buildable, API surface is clean. |
| Security | PASS | Continuous monitoring > static cert. Cross-revocation is novel. |
| UX | PASS_W_CONCERNS | Badge API is simple to embed. Registry needs good search UX. |
| CEO/Strategy | PASS | Network effects, defensible against all 3 competitors. |
| QA | PASS | Phase 1 (registry) is low-risk. Phase 3-4 scalable. |
