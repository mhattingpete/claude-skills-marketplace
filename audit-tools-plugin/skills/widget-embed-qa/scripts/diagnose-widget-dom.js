/**
 * diagnose-widget-dom.js — Widget Embed QA diagnostic (Layers 0-2 + 4)
 *
 * Run in the LIVE page context: paste into DevTools console, or via
 * Playwright `page.evaluate`, or Claude Preview `preview_eval`.
 *
 * Usage:
 *   diagnoseWidgetDom({ prefix: 'rbt-concierge', marker: 'data-rbt-widget-v2',
 *                       loaderUrl: 'https://.../widget-embed.js',
 *                       versionString: '20260702a' })
 *
 * Returns a JSON report:
 *   census      — Layer 0: per-id instance counts (duplicates = count > 1)
 *   provenance  — Layer 1: marked vs unmarked split per element
 *   scripts     — Layer 2: script inventory (index, src|inline, keyword hit)
 *   delivery    — Layer 4: served loader bytes vs expected version string
 *   verdict     — first failing layer, or 'CLEAN'
 */
async function diagnoseWidgetDom(opts) {
  var prefix = opts.prefix;
  var marker = opts.marker || null;

  // Layer 0 — census. NEVER getElementById here: it returns only the FIRST
  // element for a duplicated id.
  var all = Array.prototype.slice.call(
    document.querySelectorAll('[id^="' + prefix + '"]')
  );
  var census = {};
  all.forEach(function (el) {
    census[el.id] = (census[el.id] || 0) + 1;
  });
  var duplicatedIds = Object.keys(census).filter(function (id) { return census[id] > 1; });

  // Layer 1 — provenance: marked (new widget) vs unmarked (legacy)
  var provenance = all.map(function (el) {
    return {
      id: el.id,
      tag: el.tagName,
      marked: marker ? el.hasAttribute(marker) : null,
      display: el.style.display || getComputedStyle(el).display
    };
  });
  var unmarkedCount = marker
    ? provenance.filter(function (p) { return !p.marked; }).length
    : null;

  // Layer 2 — script inventory: execution order is document order for
  // parser-inserted scripts; async scripts run on arrival
  var scripts = Array.prototype.map.call(document.scripts, function (s, i) {
    return {
      index: i,
      src: s.src || '(inline ' + (s.textContent || '').length + ' chars)',
      async: s.async,
      defer: s.defer,
      mentionsWidget: ((s.src || '') + (s.textContent || '')).indexOf(prefix) !== -1
    };
  }).filter(function (s) { return s.mentionsWidget; });

  // Layer 4 — delivery: bypass HTTP cache, check served loader bytes
  var delivery = null;
  if (opts.loaderUrl) {
    try {
      var res = await fetch(opts.loaderUrl, { cache: 'reload' });
      var body = await res.text();
      delivery = {
        status: res.status,
        bytes: body.length,
        hasVersionString: opts.versionString ? body.indexOf(opts.versionString) !== -1 : null
      };
    } catch (e) {
      delivery = { error: String(e) };
    }
  }

  var verdict = 'CLEAN';
  if (delivery && delivery.hasVersionString === false) verdict = 'L4-STALE-DELIVERY';
  else if (duplicatedIds.length) verdict = 'L0-DUPLICATES: ' + duplicatedIds.join(',');
  else if (unmarkedCount) verdict = 'L1-LEGACY-PRESENT: ' + unmarkedCount + ' unmarked';

  return {
    verdict: verdict,
    readyState: document.readyState,
    census: census,
    provenance: provenance,
    scripts: scripts,
    delivery: delivery
  };
}

// Console convenience: prints the report when pasted directly
if (typeof module === 'undefined' && typeof window !== 'undefined' && window.__WIDGET_QA_AUTORUN__) {
  diagnoseWidgetDom(window.__WIDGET_QA_AUTORUN__).then(function (r) {
    console.log(JSON.stringify(r, null, 2));
  });
}
