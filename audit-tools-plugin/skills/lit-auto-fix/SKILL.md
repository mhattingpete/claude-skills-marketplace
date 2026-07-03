---
name: lit-auto-fix
description: Use when auditing Lit/TypeScript components for framework anti-patterns off-the-shelf linters miss
---

# Lit Auto-Fix

## Overview

8 Lit anti-patterns that `eslint-plugin-lit`, `lit-analyzer`, and other standard tools miss. Covers serialization, lifecycle, security, a11y, and performance patterns specific to Lit's Shadow DOM and reactive system.

**Iron law:** Never declare a Lit component clean without running the full pattern suite. A component that compiles and renders can still leak listeners, serialize `[object Object]` to attributes, or break under Shadow DOM optimizations.

**REQUIRED BACKGROUND:** The patterns below assume familiarity with LitElement lifecycle, `@property`/`@state` reactivity, and `lit/directives/`. Run detection first, understand each finding, then fix.

## When to Use

**Always:**
- New or modified Lit component files
- After `tsc --noEmit` passes but before merge
- Before declaring a widget/bundle "ready for preview"

**Activation phrases:**
- "audit the Lit components"
- "check for Lit anti-patterns"
- "fix the widget Lit issues"
- "run lit-detect"
- "check Shadow DOM for listener leaks"
- "audit the Lit widget before merge"
- "scan Lit components for serialization bugs"
- "is this Lit component clean?"

**Skip if:**
- Non-Lit code (use standard lint/typecheck)
- Third-party Lit components you don't own
- Generated code (but verify the generator emits correct patterns)

When NOT to use: don't run against node_modules, dist/, or generated files.

## Quick Reference

| # | Anti-pattern | Risk | Fix |
|---|-------------|------|-----|
| 1 | `<button>` without `type="button"` | Form submission in any `<form>` context | Add `type="button"` |
| 2 | `renderRoot.querySelector()` | Wrong lifecycle point; breaks Shadow DOM optimizations | Replace with `@query`/`@queryAll` |
| 3 | HTML strings rendered without `unsafeHTML` | Escaped as text content, not DOM | Import + wrap `unsafeHTML(contentHtml)` |
| 4 | `@property({type: Object/Array})` without `attribute: false` | Serializes to `[object Object]` attribute | Add `attribute: false` |
| 5 | `connectedCallback`/`disconnectedCallback` missing `super.()` | Breaks LitElement lifecycle side-effects | Add as first line in body |
| 6 | `addEventListener` without `removeEventListener` | Memory leak — component + closures retained | Track refs, teardown on disconnect |
| 7 | `this.requestUpdate()` after reactive property assignment | Wasted render cycle | Remove — `@property` setter auto-queues updates |
| 8 | Interactive element (`@click` + `tabindex>=0`) missing role/aria/keyboard | Keyboard users can't activate; a11y violation | Add role, aria-label, keyboard listener |

## Detection

```bash
# Full suite
bash scripts/lit-detect.sh src/

# Single pattern (e.g. P4)
bash scripts/lit-detect.sh src/ 4
```

## Fix Actions

### P1: `type="button"`
```ts
// <button @click=${fn}> → <button type="button" @click=${fn}>
```

### P2: `@query` / `@queryAll`
```ts
// Before: this.renderRoot.querySelector(".sel")
// After:
//   @query(".sel")
//   private _myEl!: HTMLElement | null;
```
Add `query` to Lit decorator import, replace field + call. Move any `querySelector` in `updated()` / `firstUpdated()` to a `@query` field.

### P3: `unsafeHTML`
```ts
import { unsafeHTML } from "lit/directives/unsafe-html.js";
// Before: html`<span>${contentHtml}</span>`
// After:  html`<span>${unsafeHTML(contentHtml)}</span>`
```
Only use when the string is pre-escaped (e.g., markdown output). Never use on raw user input without sanitization.

### P4: `attribute: false`
```ts
// Before: @property({ type: Object })
// After:  @property({ type: Object, attribute: false })
```
Applies to ALL `@property({ type: Object })` and `@property({ type: Array })`. `@state` does not serialize to attributes so it doesn't need this.

### P5: `super.connectedCallback()` / `super.disconnectedCallback()`
Insert as the first line of each override. If you use `addEventListener` in `connectedCallback`, you must also add `disconnectedCallback` with the matching `removeEventListener` (see P6).

### P6: Listener leak
```ts
connectedCallback() {
  super.connectedCallback();
  this._boundResize = () => this._onResize();
  window.addEventListener("resize", this._boundResize);
}
disconnectedCallback() {
  super.disconnectedCallback();
  window.removeEventListener("resize", this._boundResize);
}
```
Use bound method references (not inline closures) so the remove call matches the add. If the component is always destroyed with `el.remove()`, listeners on the element itself are GC'd — the risk is listeners on long-lived targets (window, document, shared EventTarget).

### P7: Redundant `requestUpdate()`
Remove any `this.requestUpdate()` immediately after a `@property` or `@state` field assignment — Lit already queues an update. **Keep if:** inside a `setTimeout`/`setInterval` callback, or a nanostore/RxJS subscriber that doesn't mutate a reactive field. These are outside Lit's normal reactivity cycle.

### P8: Interactive element a11y
```ts
// Before: <div @click=${fn} tabindex="0">
// After:
//   <div role="button" tabindex="0" aria-label="Activate"
//        @click=${fn}
//        @keydown=${(e) => { if (e.key==="Enter"||e.key===" ") { e.preventDefault(); fn(); } }} >
```
Native `<button>` elements don't need this — the browser provides implicit role, keyboard activation, and focus management. This pattern targets `<div>`, `<span>`, and custom elements used as interactive controls.

## Verification

- [ ] `tsc --noEmit` exits 0
- [ ] `bash scripts/lit-detect.sh src/` reports "NONE" for all 8 patterns (or false positives documented)
- [ ] Vite/build produces expected bundle size
- [ ] For P3: the unsafeHTML call has the correct import path (`lit/directives/unsafe-html.js`)
- [ ] For P6: every new `addEventListener` on window/document has a paired `removeEventListener`
- [ ] False positives noted with explanation (e.g., "P6 in index.ts: cleanup removes DOM element, GC collects listeners")

## Cross-References

- **REQUIRED SUB-SKILL:** 360-deep-audit Layer 4 (Custom Gates) — this skill is the auto-fix layer for Layer 4's Lit detection findings
- `eslint-plugin-lit` — covers template syntax (missing `{{ }}`, invalid directives), does NOT cover these 8 patterns
- `lit-analyzer` — covers type incompatibilities in templates, does NOT cover lifecycle leaks or serialization
