---
name: before-you-build
description: Review product and feature risk before implementation planning starts. Use when the user wants to build a new product, add a feature, change scope, or pivot direction before asking Claude to implement it.
---

# Before You Build

Review whether a product idea or feature request should move into implementation planning.

Use this before `feature-planning` when the user is asking to build something but the product risk is still unclear.

## When to Use

- User asks to build a new product, SaaS, AI app, side project, or startup idea.
- User asks whether a feature request should be built.
- User wants to change requirements, expand scope, or pivot direction.
- User says things like "sanity-check this", "is this worth building", "will users want this", or "pour cold water on this".

## Hard Gate

Do not write code.

Do not scaffold a project.

Do not recommend a tech stack.

Do not create an implementation plan yet.

First check demand, distribution, pricing, positioning, retention, trust, and likely failure modes.

If the idea is clearly for learning, portfolio, fun, or internal practice, do not judge it by startup standards. Focus on keeping scope small.

## Interaction

If the idea is too broad, ask only this clarification first:

```text
This idea is too broad for a responsible review.

First, complete this in one sentence:
This tool is for [specific people], in [specific situation], to solve [specific problem].
```

If the current alternative is missing and the review would be too speculative, ask one more question:

```text
How do they solve this today, and why is that not good enough?
```

Ask at most two questions before giving a constrained review.

## Quick Reality Check

Default to this short structure:

```markdown
## Quick Reality Check

Assumption:
- [State the assumption if any.]

Verdict:
- Don't build yet / Build smaller / Build only if / Build small

Biggest risk:
- [The single biggest likely failure mode.]

Most likely problem:
- [Demand / distribution / pricing / positioning / retention / trust.]

What to validate first:
- [One concrete test before implementation.]

Smallest useful version:
- [The narrowest version worth testing.]
```

## Evidence Rules

Treat weak signals as weak:

- friends saying it sounds useful;
- social media likes;
- generic survey interest;
- a competitor existing;
- the user personally wanting it.

Prefer stronger evidence:

- users already paying for a workaround;
- repeated complaints in specific communities;
- manual workflows that waste real money or time;
- signed pilots, preorders, or repeated usage;
- users migrating from an existing tool.

## Handoff

Only after the idea has a narrow target user, a concrete situation, a real problem, and a first validation step should you suggest moving to implementation planning.
