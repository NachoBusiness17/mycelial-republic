// MAG section views — one self-contained webview per left-activity-bar button.
//
// Replaces the monolithic Control Room (which crashed when any single section
// errored) with small, isolated views. Each view polls only its own REST
// endpoints and renders only its own section, so one breaking section can't
// take down the others. Framework Map proved this pattern works.
//
// Sections:
//   Thought Surface  -> live overseer/ghost/drainer streams (the "thought surface")
//   Ops Graph        -> categorized knowledge graph (SVG radial)
//   Drainer          -> drainer status + queue
//   Ghost            -> ghost trail + sense/catalog buttons
//
// NOTE: webview HTML is an outer template literal, so the embedded script must
// use ONLY string concatenation (no `${}` / no backticks) to avoid the
// extension-host interpolation crash that broke the old Control Room.
"use strict";

const vscode = require("vscode");
const http = require("http");

const DASH_HOST = "127.0.0.1";
const DASH_PORT = 8765;

function fetchJson(path) {
  return new Promise((resolve) => {
    const req = http.get(
      { host: DASH_HOST, port: DASH_PORT, path, timeout: 4000 },
      (res) => {
        let body = "";
        res.on("data", (c) => (body += c));
        res.on("end", () => {
          try { resolve(JSON.parse(body)); } catch { resolve(null); }
        });
      }
    );
    req.on("timeout", () => req.destroy());
    req.on("error", () => resolve(null));
  });
}

function fetchPost(path, body) {
  return new Promise((resolve) => {
    const payload = JSON.stringify(body || {});
    const req = http.request(
      { host: DASH_HOST, port: DASH_PORT, path, method: "POST",
        headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(payload) },
        timeout: 20000 },
      (res) => {
        let out = "";
        res.on("data", (c) => (out += c));
        res.on("end", () => { try { resolve(JSON.parse(out)); } catch { resolve({ ok: false }); } });
      }
    );
    req.on("timeout", () => req.destroy());
    req.on("error", () => resolve({ ok: false }));
    req.write(payload);
    req.end();
  });
}

class SectionView {
  constructor(def) {
    this._def = def;
    this._view = null;
    this._timer = null;
  }

  dispose() {
    if (this._timer) {
      clearInterval(this._timer);
      this._timer = null;
    }
  }

  async _snapshot() {
    const out = {};
    const paths = this._def.paths || {};
    for (const key of Object.keys(paths)) {
      out[key] = await fetchJson(paths[key]);
    }
    return out;
  }

  async _tick() {
    if (!this._view) return;
    const snap = await this._snapshot();
    if (this._view) this._view.webview.postMessage({ type: "snapshot", data: snap });
  }

  start() {
    if (this._timer) clearInterval(this._timer);
    this._timer = setInterval(() => this._tick(), 3000);
    this._tick();
  }

  resolveWebviewView(webviewView) {
    this._view = webviewView;
    webviewView.webview.options = { enableScripts: true };
    webviewView.webview.html = this._def.html();

    webviewView.webview.onDidReceiveMessage((msg) => {
      if (msg.type === "ready") {
        this._tick();
        this.start();
      } else if (msg.type === "run") {
        const term = vscode.window.createTerminal({ name: msg.name || "MAG", cwd: undefined });
        term.show();
        term.sendText(msg.cmd);
      } else if (msg.type === "handoff") {
        fetchPost("/api/v1/handoff/deep", { goal: msg.goal }).then((data) => {
          if (this._view) this._view.webview.postMessage({ type: "handoffResult", data });
        });
      }
    });

    webviewView.onDidDispose(() => {
      this._view = null;
      this.dispose();
    });
  }
}

// Shared CSS for the small views.
const STYLE = `<style>
  :root { color-scheme: dark; }
  body { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: #0d1117; color: #c9d1d9; margin: 0; padding: 12px; }
  h1 { font-size: 13px; margin: 0 0 8px; color: #58a6ff; letter-spacing: 0.5px; }
  h2 { font-size: 11px; margin: 12px 0 6px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; }
  .row { display: flex; flex-wrap: wrap; gap: 8px; }
  .card { border: 1px solid #30363d; border-radius: 6px; padding: 6px 9px; min-width: 110px; }
  .card .k { font-size: 10px; color: #8b949e; }
  .card .v { font-size: 15px; font-weight: 600; }
  .on { color: #3fb950; } .off { color: #f85149; } .warn { color: #d29922; }
  table { width: 100%; border-collapse: collapse; font-size: 11px; }
  td, th { text-align: left; padding: 3px 6px; border-bottom: 1px solid #21262d; white-space: nowrap; }
  th { color: #8b949e; }
  .goal { max-width: 360px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .btn { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 4px; padding: 4px 9px; font-size: 11px; cursor: pointer; margin: 0 6px 6px 0; }
  .btn:hover { background: #30363d; }
  .btn.ts { border-color: #388bfd55; color: #58a6ff; }
  .muted { color: #8b949e; font-size: 10px; }
  #bar { margin: 8px 0; display: flex; flex-wrap: wrap; }
  .err { color: #f85149; font-size: 11px; padding: 8px; border: 1px solid #f85149; border-radius: 6px; background: #3d1f1f; }
</style>`;

// ── Shared webview footer (run buttons + ready signal) ──
const FOOT = `
  <script>
    const vscode = acquireVsCodeApi();
    const $ = (id) => document.getElementById(id);
    const el = (tag, text, cls) => { const e = document.createElement(tag); e.textContent = text || ''; if (cls) e.className = cls; return e; };
    function rowFor(r, kind) {
      const tr = document.createElement('tr');
      tr.appendChild(el('td', (r.ts || r.timestamp || '').slice(11, 19), 'muted'));
      tr.appendChild(el('td', (r.event || r.type || r.kind || kind || '') ));
      tr.appendChild(el('td', (r.goal || r.message || r.detail || '').slice(0, 120), 'goal'));
      return tr;
    }
    function fillTrail(rows, table, kind) {
      const tb = table.querySelector('tbody') || table.createTBody();
      tb.innerHTML = '';
      (rows || []).slice(-10).reverse().forEach(r => tb.appendChild(rowFor(r, kind)));
    }
    document.addEventListener('click', (ev) => {
      const btn = ev.target.closest('[data-cmd]');
      if (!btn) return;
      vscode.postMessage({ type: 'run', cmd: btn.getAttribute('data-cmd'), name: btn.getAttribute('data-name') || 'MAG' });
    });
    vscode.postMessage({ type: 'ready' });
  </script>
</body>
</html>`;

// ====================================================================
// THOUGHT SURFACE — live overseer / ghost / drainer streams (REDESIGNED)
// ====================================================================
function thoughtSurfaceHtml() {
  return '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8">\n<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; script-src \'unsafe-inline\';">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>MAG Thought Surface</title>' + STYLE + '\n<style>\n  .tab-bar { display: flex; border-bottom: 1px solid #30363d; margin-bottom: 8px; }\n  .tab { padding: 4px 10px; cursor: pointer; font-size: 11px; color: #8b949e; border-bottom: 2px solid transparent; }\n  .tab.active { color: #58a6ff; border-bottom-color: #58a6ff; }\n  .tab-panel { display: none; }\n  .tab-panel.active { display: block; }\n  .status-card { border: 1px solid #30363d; border-radius: 6px; padding: 8px 10px; margin-bottom: 6px; }\n  .status-card .hd { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }\n  .status-card .nm { font-size: 12px; font-weight: 600; }\n  .status-card .st { font-size: 10px; padding: 1px 6px; border-radius: 8px; }\n  .st-live { background: #1a3a1a; color: #3fb950; }\n  .st-stale { background: #3a2a0a; color: #d29922; }\n  .st-down { background: #3a1a1a; color: #f85149; }\n  .status-card .snippet { font-size: 10px; color: #8b949e; line-height: 1.4; }\n  .status-card .snippet b { color: #c9d1d9; }\n  .tooltip { display: none; position: absolute; background: #161b22; border: 1px solid #30363d; border-radius: 4px; padding: 6px 8px; font-size: 10px; max-width: 280px; z-index: 10; word-break: break-all; }\n</style>\n</head><body>\n  <h1 style="display:flex;align-items:center;gap:6px;"><span style="font-size:16px">⚡</span> Thought Surface <span class="muted" id="ts"></span></h1>\n  <div class="tab-bar">\n    <div class="tab active" data-tab="overseer">◉ Overseer</div>\n    <div class="tab" data-tab="drainer">⚙️ Drainer</div>\n    <div class="tab" data-tab="ghost">👻 Ghost</div>\n  </div>\n  <div class="tab-panel active" id="panel-overseer"><div id="overseer-cards"></div></div>\n  <div class="tab-panel" id="panel-drainer"><div id="drainer-cards"></div></div>\n  <div class="tab-panel" id="panel-ghost"><div id="ghost-cards"></div></div>\n  <div class="tooltip" id="tooltip"></div>\n  <script>\n    var lastSnap = {};\n    function ago(ts) {\n      if (!ts) return "";\n      try {\n        var d = new Date(ts.replace("Z","") + "Z");\n        var s = Math.floor((new Date() - d) / 1000);\n        if (s < 60) return s + "s ago";\n        if (s < 3600) return Math.floor(s/60) + "m ago";\n        return Math.floor(s/3600) + "h ago";\n      } catch(e) { return ""; }\n    }\n    function statusDot(lines, maxAge) {\n      if (!lines || !lines.length) return "st-down";\n      var last = lines[lines.length-1];\n      try {\n        var d = new Date((last.ts||last.timestamp||"").replace("Z","") + "Z");\n        var age = (new Date() - d) / 1000;\n        if (age < maxAge) return "st-live";\n        if (age < maxAge*3) return "st-stale";\n      } catch(e) {}\n      return "st-down";\n    }\n    function renderCards(panelId, lines, label, maxAge, desc) {\n      var panel = document.getElementById(panelId);\n      if (!panel) return;\n      var cls = statusDot(lines, maxAge);\n      var last = (lines && lines.length) ? lines[lines.length-1] : null;\n      var snippet = "";\n      if (last) {\n        var ev = last.event || last.type || last.kind || "";\n        var detail = (last.goal || last.message || last.detail || "").slice(0, 140);\n        if (ev && detail) snippet = "<b>" + ev + "</b>: " + detail;\n        else if (detail) snippet = detail;\n        else snippet = "(waiting for data)";\n      } else {\n        snippet = "(no data — " + label + " may be down)";\n      }\n      var full = last ? JSON.stringify(last, null, 2).slice(0, 500) : "";\n      panel.innerHTML = \'<div class="status-card" data-tip="\' + full.replace(/"/g, "&quot;") + \'">\' +\n        \'<div class="hd"><span class="nm">\' + label + \'</span><span class="st \' + cls + \'">\' + ago(last&&last.ts||last&&last.timestamp) + \'</span></div>\' +\n        \'<div class="snippet">\' + snippet + \'</div>\' +\n        \'<div style="font-size:9px;color:#484f58;margin-top:3px;">\' + desc + \'</div>\' +\n        \'</div>\';\n    }\n    document.querySelectorAll(".tab").forEach(function(t) {\n      t.addEventListener("click", function() {\n        document.querySelectorAll(".tab").forEach(function(x) { x.classList.remove("active"); });\n        document.querySelectorAll(".tab-panel").forEach(function(x) { x.classList.remove("active"); });\n        t.classList.add("active");\n        var p = document.getElementById("panel-" + t.getAttribute("data-tab"));\n        if (p) p.classList.add("active");\n      });\n    });\n    document.addEventListener("mouseover", function(ev) {\n      var card = ev.target.closest("[data-tip]");\n      var tip = document.getElementById("tooltip");\n      if (card) {\n        tip.textContent = card.getAttribute("data-tip");\n        tip.style.display = "block";\n        tip.style.left = Math.min(ev.pageX + 8, window.innerWidth - 290) + "px";\n        tip.style.top = (ev.pageY - 10) + "px";\n      } else {\n        tip.style.display = "none";\n      }\n    });\n    window.addEventListener("message", function(ev) {\n      var d = (ev.data || {}).data || {};\n      if (ev.data.type !== "snapshot") return;\n      lastSnap = d;\n      var any = d.overseer || d.drainer || d.ghost;\n      var tsEl = document.getElementById("ts");\n      if (tsEl) tsEl.textContent = any && any.ts ? " · " + ago(any.ts) : "";\n      var ovLines = (d.overseer && d.overseer.lines) || [];\n      var drLines = (d.drainer && d.drainer.lines) || [];\n      var ghLines = (d.ghost && d.ghost.lines) || [];\n      renderCards("overseer-cards", ovLines, "Overseer", 30, "Routes questions to the right model. Ask \u2192 decide \u2192 dispatch.");\n      renderCards("drainer-cards", drLines, "Drainer", 20, "Pulls from the queue and spawns agent tasks. The workhorse.");\n      renderCards("ghost-cards", ghLines, "Ghost", 45, "Silent steer. Senses system health and deploys test vectors.");\n    });\n  </script>' + FOOT;
}

// ====================================================================
// DRAINER — status + queue
// ====================================================================
function drainerViewHtml() {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Drainer</title>${STYLE}
</head><body>
  <h1>⚙️ Drainer <span class="muted" id="ts"></span></h1>
  <div id="bar">
    <button class="btn" data-cmd="python -m mag.drainer_stats" data-name="Drainer Stats">Stats</button>
    <button class="btn" data-cmd="python -m mag.session_state_brief" data-name="Brief">Refresh Brief</button>
  </div>
  <div class="row" id="pipeline"></div>
  <h2>Queue <span class="muted" id="queueCount"></span></h2>
  <table id="queue"><tr><th>status</th><th class="goal">goal</th><th>provider</th></tr></table>
  <div class="err" id="err" style="display:none;">Dashboard not reachable (:8765)</div>
  <script>
    window.addEventListener('message', (ev) => {
      const msg = ev.data;
      if (msg.type !== 'snapshot') return;
      const d = msg.data || {};
      const s = d.stats || {};
      if (!s.schema) { $('err').style.display = 'block'; return; }
      $('err').style.display = 'none';
      $('ts').textContent = (s.ts || '').slice(11, 19);
      const pl = $('pipeline'); pl.innerHTML = '';
      const dr = s.drainer || {}, q = s.queue || {};
      const card = (k, v, cls) => { const c = document.createElement('div'); c.className = 'card'; c.appendChild(el('div', k, 'k')); c.appendChild(el('div', v, cls || '')); pl.appendChild(c); };
      card('drainer', dr.enabled ? 'ON' : 'OFF', dr.enabled ? 'on' : 'off');
      card('autorun', dr.autorun_allowed ? 'allowed' : 'paused', dr.autorun_allowed ? 'on' : 'warn');
      card('operator', s.operator && s.operator.operator_active ? 'active' : 'away', (s.operator && s.operator.operator_active) ? 'on' : 'muted');
      card('fleet live', s.fleet ? s.fleet.live_n : '-', '');
      card('handoffs', s.pending_handoffs_n || 0, '');
      card('queue running', (q.counts && q.counts.running) || 0, '');
      const qb = $('queue').createTBody(); qb.innerHTML = '';
      $('queueCount').textContent = (s.queue_items || []).length;
      (s.queue_items || []).slice(0, 12).forEach(i => {
        const tr = document.createElement('tr');
        tr.appendChild(el('td', i.status));
        tr.appendChild(el('td', i.goal, 'goal'));
        tr.appendChild(el('td', i.provider));
        qb.appendChild(tr);
      });
    });
  </script>${FOOT}`;
}

// ====================================================================
// GHOST — trail + sense/catalog buttons
// ====================================================================
function ghostViewHtml() {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Ghost</title>${STYLE}
</head><body>
  <h1>👻 Ghost <span class="muted" id="ts"></span></h1>
  <div id="bar">
    <button class="btn" data-cmd="python -m mag.ghost --sense" data-name="Ghost Sense">Sense</button>
    <button class="btn" data-cmd="python -m mag.ghost --catalog" data-name="Ghost Catalog">Catalog</button>
  </div>
  <div class="row" id="aware"></div>
  <h2>Live Trail</h2>
  <table id="trail"><tr><th>ts</th><th>event</th><th class="goal">detail</th></tr></table>
  <div class="err" id="err" style="display:none;">Dashboard not reachable (:8765)</div>
  <script>
    window.addEventListener('message', (ev) => {
      const msg = ev.data;
      if (msg.type !== 'snapshot') return;
      const d = msg.data || {};
      const lines = (d.ghost && d.ghost.lines) || [];
      if (!lines.length) { $('err').style.display = 'block'; return; }
      $('err').style.display = 'none';
      $('ts').textContent = lines.length ? (lines[lines.length-1].ts || '').slice(11, 19) : '';
      fillTrail(lines, $('trail'), 'ghost');
      // awareness card (from context on ghost trail rows, best-effort)
      const last = lines[lines.length-1] || {};
      const aw = $('aware'); aw.innerHTML = '';
      const card = (k, v, cls) => { const c = document.createElement('div'); c.className = 'card'; c.appendChild(el('div', k, 'k')); c.appendChild(el('div', v, cls || '')); aw.appendChild(c); };
      card('outcome', last.outcome || '?', last.outcome === 'deployed' ? 'on' : 'muted');
      card('auto_deploy', last.auto_deploy || '?', (last.auto_deploy || '').indexOf('suppressed') === 0 ? 'warn' : '');
    });
  </script>${FOOT}`;
}

// ====================================================================
// OPS GRAPH — categorized knowledge graph (SVG radial)
// ====================================================================
function opsGraphHtml() {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:;">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Ops Graph</title>${STYLE}
<style>
  #wrap { width: 100%; height: 62vh; border: 1px solid #21262d; border-radius: 6px; overflow: hidden; }
  svg { width: 100%; height: 100%; display: block; }
  .node circle { stroke: #0d1117; stroke-width: 1.5; }
  .node text { fill: #c9d1d9; font-size: 9px; text-anchor: middle; pointer-events: none; }
  .edge { stroke-opacity: 0.55; fill: none; }
  #legend { display: flex; gap: 12px; flex-wrap: wrap; font-size: 10px; color: #8b949e; margin: 6px 0; }
  .lg { display: inline-flex; align-items: center; gap: 4px; }
  .sw { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
</style>
</head><body>
  <h1>🕸️ Ops Graph <span class="muted" id="ts"></span></h1>
  <div id="bar">
    <button class="btn" data-cmd="python -m mag.ops_graph --ingest" data-name="Ops Graph">persist</button>
  </div>
  <div id="legend"></div>
  <div id="wrap"><svg id="svg"></svg></div>
  <div class="muted" id="status"></div>
  <script>
    const COLORS = {};
    const NODE_FEED = { 'sub:ghost': 'ghost', 'sub:drainer': 'drainer', 'sub:autorun': 'drainer', 'sub:orchestrator': 'drainer' };
    function openFeed(n) {
      const kind = NODE_FEED[n.id];
      if (!kind) return;
      vscode.postMessage({ type: 'run', cmd: 'python -m mag.live_feed ' + kind, name: 'MAG Thought · ' + kind });
    }
    function legend(cats) {
      const elm = $('legend'); elm.innerHTML = '';
      Object.keys(cats || {}).forEach(k => {
        const c = cats[k]; COLORS[k] = c.color;
        const span = document.createElement('span'); span.className = 'lg';
        span.innerHTML = '<span class="sw" style="background:' + c.color + '"></span> ' + c.label;
        elm.appendChild(span);
      });
    }
    function layout(g) {
      const nodes = g.nodes || [];
      const center = nodes.find(n => n.id === 'run:current');
      const mid = nodes.filter(n => n.category === 'subsystem' || n.category === 'operator');
      const outer = nodes.filter(n => ['provider','signal','metric'].indexOf(n.category) >= 0);
      const pos = {}, W = 900, H = 600, CX = W/2, CY = H/2, R1 = 150, R2 = 270;
      function ring(list, r) {
        const n = list.length;
        list.forEach((node, i) => {
          const a = (i / Math.max(n,1)) * 2 * Math.PI - Math.PI/2;
          pos[node.id] = { x: CX + r*Math.cos(a), y: CY + r*Math.sin(a) };
        });
      }
      if (center) pos[center.id] = { x: CX, y: CY };
      ring(mid, R1); ring(outer, R2);
      return pos;
    }
    function render(g) {
      legend(g.categories);
      const pos = layout(g);
      const svg = $('svg'), NS = 'http://www.w3.org/2000/svg';
      svg.innerHTML = '';
      svg.setAttribute('viewBox', '0 0 900 600');
      (g.edges || []).forEach(e => {
        const s = pos[e.src], d = pos[e.dst];
        if (!s || !d) return;
        const line = document.createElementNS(NS, 'line');
        line.setAttribute('class', 'edge');
        line.setAttribute('x1', s.x); line.setAttribute('y1', s.y);
        line.setAttribute('x2', d.x); line.setAttribute('y2', d.y);
        line.setAttribute('stroke', (g.edge_types && g.edge_types[e.type]) || '#8b949e');
        line.setAttribute('stroke-width', '1.2');
        svg.appendChild(line);
      });
      (g.nodes || []).forEach(n => {
        const p = pos[n.id]; if (!p) return;
        const gEl = document.createElementNS(NS, 'g');
        gEl.setAttribute('class', 'node');
        gEl.setAttribute('transform', 'translate(' + p.x + ',' + p.y + ')');
        const r = n.id === 'run:current' ? 26 : (n.category === 'subsystem' ? 20 : 14);
        const circ = document.createElementNS(NS, 'circle');
        circ.setAttribute('r', r);
        circ.setAttribute('fill', (COLORS[n.category] || '#8b949e'));
        circ.setAttribute('fill-opacity', n.status === 'warn' ? '0.55' : '0.85');
        circ.setAttribute('data-tip', n.id + ' [' + n.status + ']');
        if (NODE_FEED[n.id]) { circ.style.cursor = 'pointer'; circ.addEventListener('click', () => openFeed(n)); }
        gEl.appendChild(circ);
        const t = document.createElementNS(NS, 'text');
        t.setAttribute('y', r + 12);
        t.textContent = n.label.length > 22 ? n.label.slice(0, 22) + '\u2026' : n.label;
        gEl.appendChild(t);
        svg.appendChild(gEl);
      });
    }
    window.addEventListener('message', (ev) => {
      const msg = ev.data;
      if (msg.type !== 'snapshot') return;
      const g = msg.data.graph || {};
      $('ts').textContent = (g.ts || '').slice(11, 19);
      $('status').textContent = (g.nodes ? g.nodes.length : 0) + ' nodes · ' + (g.edges ? g.edges.length : 0) + ' edges · click a node to open its feed';
      if (g.nodes) render(g);
    });
  </script>${FOOT}`;
}

// ====================================================================
// HANDOFF — deep-model drop-in via the session maze (memory-framework test)
// ====================================================================
function handoffViewHtml() {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Handoff</title>${STYLE}
</head><body>
  <h1>🔀 Handoff to Deep</h1>
  <div class="muted">Drop this run onto a deeper model (deepseek-v4-pro) via the session maze. It reads <code>state/HANDOFF.md</code> — no re-pasted chat, no re-paid context tax.</div>
  <h2>Goal to continue</h2>
  <textarea id="goal" rows="4" style="width:100%;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:4px;font-family:ui-monospace,monospace;font-size:11px;"></textarea>
  <div id="bar">
    <button class="btn ts" id="deepBtn">⇩ Handoff to DeepSeek V4 Pro Max</button>
    <button class="btn" id="mazeBtn">◉ Preview Maze</button>
  </div>
  <pre id="result" style="white-space:pre-wrap;background:#161b22;border:1px solid #21262d;border-radius:6px;padding:8px;font-size:10px;color:#8b949e;"></pre>
  <script>
    function show(d) {
      var pre = document.getElementById('result');
      try { pre.textContent = JSON.stringify(d, null, 2); } catch (e) { pre.textContent = String(d); }
    }
    document.getElementById('deepBtn').addEventListener('click', function () {
      var goal = document.getElementById('goal').value.trim();
      if (!goal) { show({ error: 'enter a goal to continue' }); return; }
      show({ status: 'assembling maze + spawning deepseek-v4-pro...' });
      vscode.postMessage({ type: 'handoff', goal: goal });
    });
    document.getElementById('mazeBtn').addEventListener('click', function () {
      show({ status: 'assembling maze...' });
      vscode.postMessage({ type: 'handoff', goal: '' });
    });
    window.addEventListener('message', function (ev) {
      var m = ev.data || {};
      if (m.type === 'handoffResult') { show(m.data); }
    });
  </script>${FOOT}`;
}

// ====================================================================
// SURFACE AUDIT — surfaces + groups + seam verdict (Surface Hub)
// ====================================================================
function surfaceHubHtml() {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Surface Audit</title>${STYLE}
<style>
  .verdict { display:inline-block; font-size:10px; padding:2px 8px; border-radius:8px; margin-left:6px; }
  .verdict.ready { background:#1a3a1a; color:#3fb950; }
  .verdict.attention { background:#3a2a0a; color:#d29922; }
  .bar-row { display:flex; align-items:center; gap:8px; margin:3px 0; font-size:11px; }
  .bar-row .lab { width:86px; color:#8b949e; text-align:right; }
  .bar-row .track { flex:1; background:#161b22; border:1px solid #21262d; border-radius:4px; height:12px; overflow:hidden; }
  .bar-row .fill { height:100%; background:#58a6ff; }
  .bar-row .num { width:34px; color:#c9d1d9; }
  .check { font-size:11px; padding:2px 0; }
  .check.ok { color:#3fb950; }
  .check.fail { color:#f85149; }
</style>
</head><body>
  <h1>🔎 Surface Audit <span class="muted" id="ts"></span><span class="verdict" id="verdict">—</span></h1>
  <div class="muted" id="meta"></div>
  <h2>Surfaces</h2>
  <div class="row" id="surfaces"></div>
  <h2>Functional groups <span class="muted">(by function)</span></h2>
  <div id="groups"></div>
  <h2>Seam checks</h2>
  <div id="checks"></div>
  <div class="err" id="err" style="display:none;">Dashboard not reachable (:8765)</div>
  <script>
    window.addEventListener('message', (ev) => {
      const msg = ev.data;
      if (msg.type !== 'snapshot') return;
      const a = msg.data.audit || {};
      if (!a.schema) { $('err').style.display = 'block'; return; }
      $('err').style.display = 'none';
      $('ts').textContent = (a.ts || '').slice(11, 19);
      $('meta').textContent = 'v' + (a.version || '?') + ' · ' + (a.entries || 0) + ' entries · ' + (a.checks || []).length + ' seam checks';
      const v = $('verdict');
      v.textContent = (a.verdict || 'n/a').toUpperCase();
      v.className = 'verdict ' + (a.verdict === 'ready' ? 'ready' : 'attention');
      const s = $('surfaces'); s.innerHTML = '';
      (a.surfaces || []).forEach(function (surf) {
        const c = document.createElement('div'); c.className = 'card';
        c.appendChild(el('div', surf.label, 'k'));
        c.appendChild(el('div', surf.count, 'v'));
        s.appendChild(c);
      });
      const g = $('groups'); g.innerHTML = '';
      const counts = (a.groups || []).map(function (x) { return x.count || 0; });
      const max = Math.max.apply(null, counts.concat([1]));
      (a.groups || []).forEach(function (grp) {
        const row = document.createElement('div'); row.className = 'bar-row';
        row.appendChild(el('div', (grp.icon || '') + ' ' + grp.label, 'lab'));
        const track = document.createElement('div'); track.className = 'track';
        const fill = document.createElement('div'); fill.className = 'fill';
        fill.style.width = Math.round(100 * (grp.count || 0) / max) + '%';
        track.appendChild(fill);
        row.appendChild(track);
        row.appendChild(el('div', grp.count, 'num'));
        g.appendChild(row);
      });
      const ch = $('checks'); ch.innerHTML = '';
      (a.checks || []).forEach(function (c) {
        const d = document.createElement('div'); d.className = 'check ' + (c.ok ? 'ok' : 'fail');
        d.textContent = (c.ok ? '✓ ' : '✗ ') + c.name + ' — ' + (c.detail || '');
        ch.appendChild(d);
      });
    });
  </script>${FOOT}`;
}

// ====================================================================
// Factory — build all section views
// ====================================================================
function buildViews() {
  const views = {
    thoughtSurface: new SectionView({
      paths: {
        overseer: "/api/v1/live-feed?kind=overseer&limit=10",
        drainer: "/api/v1/live-feed?kind=drainer&limit=10",
        ghost: "/api/v1/live-feed?kind=ghost&limit=10",
      },
      html: thoughtSurfaceHtml,
    }),
    drainerView: new SectionView({
      paths: { stats: "/api/v1/drainer/stats" },
      html: drainerViewHtml,
    }),
    ghostView: new SectionView({
      paths: { ghost: "/api/v1/live-feed?kind=ghost&limit=20" },
      html: ghostViewHtml,
    }),
    opsGraph: new SectionView({
      paths: { graph: "/api/v1/graph/ops" },
      html: opsGraphHtml,
    }),
    handoffView: new SectionView({
      paths: {},
      html: handoffViewHtml,
    }),
    surfaceHub: new SectionView({
      paths: { audit: "/api/v1/surface-audit" },
      html: surfaceHubHtml,
    }),
  };
  return views;
}

module.exports = { buildViews };
