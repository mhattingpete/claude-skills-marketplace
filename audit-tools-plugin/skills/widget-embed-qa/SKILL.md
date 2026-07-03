---
name: widget-embed-qa
description: "Use when an embedded widget (Shopify script_tag, chat bubble, banner, any third-party JS embed) shows duplicate buttons or UI, ghost elements from an old version, elements that reappear after cleanup removes them, cleanup that only removes one of several duplicates, or a deployed fix that doesn't show on the live page. Covers duplicate IDs, getElementById vs querySelectorAll, script execution order races, MutationObserver timing windows, and stale CDN/browser cache."
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Widget Embed QA

> **Skill Type:** QA/DEBUGGING · **Category:** Embedded Widgets & Third-Party JS · **Cost:** Free

Diagnoses and fixes the "two chat buttons" class of bug: an old widget implementation (inline theme script, legacy script_tag) coexists with a new one on the same page, and every naive cleanup attempt loses a race. The skill replaces guess-and-redeploy loops with a fixed 6-layer diagnostic ladder, then applies the one fix pattern that has no timing window: **dedupe by identity, not by ID.**

**Key differentiator:** timing-window cleanups (run early, run on load, observe-then-disconnect) all race the parser and the cache. This skill's fix pattern is idempotent and time-independent, so it cannot lose the race.

## When to Use

**Activation phrases:**
- "there are two widget buttons"
- "duplicate widget elements on the page"
- "the cleanup only removed the first duplicate"
- "old widget still shows after deploy"
- "element comes back after I remove it"
- "the fix is deployed but the page didn't change"
- "getElementById only returns one of them"
- "the MutationObserver didn't catch it"
- "qa the widget embed"

**Skip if:** the widget renders wrong but only once (styling/logic bug — not a duplication/race problem); or the duplicate is inside YOUR framework tree (React/Lit double-mount — check your own mount guard first).

## The Iron Rules

1. **Never use `getElementById` to find duplicates.** It returns only the FIRST match by definition. Census duplicates with `document.querySelectorAll('[id^="prefix"]')` and remove in a loop.
2. **Never trust a cleanup that runs once.** Any single-shot cleanup races the script that creates the elements. Prove execution order before assuming it.
3. **Never dedupe by ID when old and new implementations share IDs.** Removal-by-ID is undecidable — you either miss the legacy element or delete your own widget. Mark the new elements (`data-<widget>-v2` attribute) and remove only unmarked matches.
4. **Never disconnect a cleanup observer on bundle `onload`.** A cached bundle fires `onload` before the parser reaches a late inline script — the observer dies before the enemy arrives. Disconnect only after `window.load` plus a grace period.
5. **Never debug DOM behavior until you've proven the deployed file is the file being served.** Stale CDN/browser cache makes every other observation a lie.

## The 6-Layer Diagnostic Ladder

Run the layers in order. Each layer has a verdict that either terminates or routes downward. Use `scripts/diagnose-widget-dom.js` (paste into console, or run via Playwright/preview `evaluate`) — it executes layers 0–2 and 4 in one shot and returns a JSON report.

| Layer | Question | How | Verdict routes |
|-------|----------|-----|----------------|
| 0. Census | How many instances of each ID/selector exist? | `querySelectorAll('[id^="prefix"]')`, count per id | 0 dupes → done. ≥2 → L1 |
| 1. Provenance | Which script created which element? | Enumerate `document.scripts` (index, src, inline keyword match); check markers on elements | Both from one script → your own double-mount, not this skill. Old+new sources → L2 |
| 2. Timing | When does each script execute relative to cleanup? | Script index order; async/defer flags; when observers connect/disconnect; readyState | Cleanup window closes before creator runs → L3 |
| 3. Identity | Can cleanup even distinguish old from new? | Do old and new elements share IDs? Is there a marker attribute? | Shared IDs, no marker → apply Fix Pattern below |
| 4. Delivery | Is the deployed file actually served? | `fetch(url, {cache:'reload'})`, diff a version string/byte length against the file you deployed | Stale → purge/cache-bust (`?v=`), THEN re-run L0 |
| 5. Root source | Why does the legacy script still exist at all? | Find the inline script in the theme / old script_tag in the platform admin | Client-side cleanup is a bridge. File the task to delete the legacy source. |

## The Fix Pattern (identity-based cleanup)

Three parts, all required:

```js
// 1. NEW widget marks its elements at creation (in the widget source):
el.setAttribute('data-mywidget-v2', '');

// 2. Loader: idempotent sweep — removes ONLY unmarked matches, safe to run
//    any time, any number of times:
function removeLegacy() {
  var legacy = document.querySelectorAll('[id^="mywidget"]:not([data-mywidget-v2])');
  for (var i = legacy.length - 1; i >= 0; i--) legacy[i].remove();
}

// 3. Run the sweep at EVERY lifecycle edge + a persistent observer:
removeLegacy();                                            // now
new MutationObserver(removeLegacy)                         // whenever DOM changes
  .observe(document.documentElement, { childList: true, subtree: true });
document.addEventListener('DOMContentLoaded', removeLegacy);
window.addEventListener('load', function () {
  removeLegacy();
  setTimeout(removeLegacy, 3000);                          // post-load grace, then optionally disconnect
});
bundleScript.onload = function () { removeLegacy(); api.init(); };
```

Delivery hardening: pin the bundle URL with a per-deploy version param (`?v=20260702a`), never `Date.now()` (kills caching entirely).

## Verification Gate (definition of done)

Not done until, on the LIVE page (not localhost):
1. The diagnostic script reports **zero duplicate IDs** and **new-widget marker present**.
2. Served loader bytes contain the new version string (`fetch` with `cache:'reload'`).
3. The widget still works (button opens panel) — cleanup didn't eat the new widget.

## Rationalization Table

| Excuse mid-debug | Reality |
|------------------|---------|
| "getElementById + remove() cleaned it up" | It removed ONE. Census with querySelectorAll before claiming done. |
| "My cleanup runs first, so it wins" | Running first is the problem — the creator runs after you. Order ≠ victory. |
| "The MutationObserver will catch it" | Only while connected. Prove the disconnect happens after the legacy script runs. |
| "I deployed it, the page must have it" | Caches lie. Verify served bytes before interpreting any DOM behavior. |
| "One more redeploy and re-check" | Three failed variants at the same layer = wrong layer. Move down the ladder. |
| "The client-side cleanup works, ship it" | It's a bridge. The legacy source is still injected on every page load. File its deletion. |

## Example Interaction

```
User: "Two chat buttons on the storefront again, cleanup didn't work"

Skill:
1. Runs diagnose-widget-dom.js on the live page → census: #widget-btn ×2,
   scripts: loader at index 0 (src), legacy inline at index 54
2. L2 verdict: observer disconnects on bundle onload (cached → fires before index 54)
3. L3 verdict: old and new share #widget-btn — ID-based removal undecidable
4. Applies fix pattern: marker attr in widget source + identity sweep in loader
5. Rebuilds, deploys with ?v= bump, re-runs diagnostic → 1 button, marked, panel opens
6. Files task: remove legacy inline script from theme (root source)
```

## Tools Used

- **Bash**: rebuild bundles, deploy, `curl`/`fetch` served-bytes checks
- **Read/Grep**: locate the legacy script source, loader, widget mount code
- **Edit/Write**: apply marker + identity-sweep pattern
- **Browser eval** (Playwright MCP, preview_eval, or DevTools paste): run `scripts/diagnose-widget-dom.js`

## Integration

- After fixing, run **lit-auto-fix** if the widget is Lit-based (this plugin).
- Escalate to **system-qa** for full runtime QA of the widget's backend.
- The root-source deletion (Layer 5) is a platform change — theme edit or script_tag API call — treat with that platform's deploy gates.
