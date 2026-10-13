/* FEED STALE badge — fixed-position amber badge shown when a page's feed data
   is older than 24h or unreachable. Wire any page with one line before </body>:
     <script src="feed_badge.js" data-feeds="overseer.json,live_feed.json"></script>
   (comma-separated feed URLs, relative to the page). No badge = feed fresh. */
(function () {
  var MAX_AGE_MS = 24 * 60 * 60 * 1000;
  var script = document.currentScript;
  var raw = (script && script.getAttribute('data-feeds')) || window.FEED_URLS || '';
  var feeds = raw.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
  if (!feeds.length) return;

  var TS_KEYS = ['generated_at', 'updated_at', 'updatedAt', 'timestamp', 'ts',
                 'captured_at', 'capturedAt', 'time', 'when', 'date', 'mtime'];

  function toMs(v) {
    if (typeof v === 'number') return v > 1e12 ? v : (v > 1e9 ? v * 1000 : null); // ms or s epoch
    if (typeof v === 'string') { var t = Date.parse(v); return isNaN(t) ? null : t; }
    return null;
  }

  function findTs(x, depth) {
    if (x == null || depth > 4) return null;
    var direct = toMs(x);
    if (direct) return direct;
    if (Array.isArray(x)) {
      for (var i = x.length - 1; i >= 0; i--) {          // newest entry last (JSONL / append logs)
        var t = findTs(x[i], depth + 1);
        if (t) return t;
      }
      return null;
    }
    if (typeof x === 'object') {
      for (var k = 0; k < TS_KEYS.length; k++) {
        if (TS_KEYS[k] in x) { var v = toMs(x[TS_KEYS[k]]); if (v) return v; }
      }
      for (var key in x) { var v2 = findTs(x[key], depth + 1); if (v2) return v2; }
    }
    return null;
  }

  function parse(text) {                                // whole-file JSON, else JSONL (last line wins)
    try { return JSON.parse(text); } catch (e) {}
    var lines = text.trim().split('\n'), last = null;
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line) continue;
      try { last = JSON.parse(line); } catch (e) { return null; }
    }
    return last;
  }

  function show(dateLabel) {
    var el = document.getElementById('feed-stale-badge');
    if (!el) {
      el = document.createElement('div');
      el.id = 'feed-stale-badge';
      el.style.cssText = 'position:fixed;right:12px;bottom:12px;z-index:99999;' +
        'background:#f59e0b;color:#111;font:700 11px/1.3 ui-monospace,Consolas,monospace;' +
        'padding:6px 10px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.5);pointer-events:none';
      (document.body || document.documentElement).appendChild(el);
    }
    el.textContent = 'FEED STALE \u2014 ' + dateLabel;
  }

  function hide() {
    var el = document.getElementById('feed-stale-badge');
    if (el) el.remove();
  }

  function check() {
    var pending = feeds.length, stale = null;
    feeds.forEach(function (url) {
      fetch(url, { cache: 'no-store' })
        .then(function (res) { if (!res.ok) throw new Error(res.status); return res.text(); })
        .then(function (text) {
          var ts = findTs(parse(text), 0);
          if (!ts || Date.now() - ts > MAX_AGE_MS) {
            stale = ts ? new Date(ts).toISOString().slice(0, 10) : 'unknown date';
          }
        })
        .catch(function () { stale = 'feed unreachable'; })
        .finally(function () {
          if (--pending === 0) { if (stale) show(stale); else hide(); }
        });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', check);
  } else { check(); }
  setInterval(check, 5 * 60 * 1000);                    // re-check every 5 min
})();
