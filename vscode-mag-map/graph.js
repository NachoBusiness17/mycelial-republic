// MAG Ops Knowledge Graph — categorized live telemetry as an SVG graph.
// Fetches /api/v1/graph/ops from the dashboard and renders nodes (colored by
// category) + edges in a radial layout. Refreshable, no external deps.
"use strict";

const vscode = require("vscode");
const http = require("http");

const DASH_HOST = "127.0.0.1";
const DASH_PORT = 8765;

class OpsGraphPanel {
  constructor(extensionUri, panel) {
    this._extensionUri = extensionUri;
    this._panel = panel;
    this._timer = null;
    this._poll = true;
  }

  static create(extensionUri, column) {
    const panel = vscode.window.createWebviewPanel(
      "magMap.opsGraph",
      "MAG Ops Graph",
      column || vscode.ViewColumn.Active,
      { enableScripts: true, retainContextWhenHidden: true }
    );
    const inst = new OpsGraphPanel(extensionUri, panel);
    panel.webview.html = inst._html();
    panel.webview.onDidReceiveMessage((msg) => {
      if (msg.type === "ready") inst._tick();
      else if (msg.type === "poll") {
        inst._poll = msg.value;
        if (inst._poll) inst._tick();
      } else if (msg.type === "run") {
        const term = vscode.window.createTerminal({ name: msg.name || "MAG Graph", cwd: undefined });
        term.show();
        term.sendText(msg.cmd);
      }
    });
    panel.onDidDispose(() => inst.dispose());
    return inst;
  }

  dispose() {
    if (this._timer) {
      clearTimeout(this._timer);
      this._timer = null;
    }
  }

  _fetch() {
    return new Promise((resolve) => {
      const req = http.get(
        { host: DASH_HOST, port: DASH_PORT, path: "/api/v1/graph/ops", timeout: 4000 },
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

  async _tick() {
    if (!this._panel) return;
    const g = await this._fetch();
    if (!g || !this._panel) return;
    this._panel.webview.postMessage({ type: "graph", data: g });
    if (this._poll) {
      this._timer = setTimeout(() => this._tick(), 5000);
    }
  }

  _html() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy"
  content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:;">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Ops Graph</title>
<style>
  :root { color-scheme: dark; }
  body { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: #0d1117; color: #c9d1d9; margin: 0; padding: 12px; }
  h1 { font-size: 14px; margin: 0 0 8px; color: #58a6ff; letter-spacing: 0.5px; }
  .muted { color: #8b949e; font-size: 10px; }
  #bar { display: flex; gap: 6px; align-items: center; margin-bottom: 8px; flex-wrap: wrap; }
  .btn { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 4px; padding: 3px 8px; font-size: 11px; cursor: pointer; }
  .btn:hover { background: #30363d; }
  #legend { display: flex; gap: 12px; flex-wrap: wrap; font-size: 10px; color: #8b949e; margin-bottom: 6px; }
  .lg { display: inline-flex; align-items: center; gap: 4px; }
  .sw { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
  #wrap { width: 100%; height: 66vh; border: 1px solid #21262d; border-radius: 6px; overflow: hidden; }
  svg { width: 100%; height: 100%; display: block; background: #0d1117; }
  .node circle { stroke: #0d1117; stroke-width: 1.5; }
  .node text { fill: #c9d1d9; font-size: 9px; text-anchor: middle; pointer-events: none; }
  .node:hover circle { stroke: #fff; }
  .edge { stroke-opacity: 0.55; fill: none; }
  #status { margin-top: 6px; font-size: 10px; color: #8b949e; }
</style>
</head>
<body>
  <h1>🕸️ MAG Ops Knowledge Graph <span class="muted" id="ts"></span></h1>
  <div id="bar">
    <button class="btn" id="refresh">⟳ refresh</button>
    <button class="btn" id="toggle">⏸ pause</button>
    <button class="btn" data-cmd="python -m mag.ops_graph --ingest">persist snapshot</button>
    <button class="btn" data-cmd="python -m mag.ops_graph">CLI table</button>
  </div>
  <div id="legend"></div>
  <div id="wrap"><svg id="svg"></svg></div>
  <div id="status">connecting…</div>
  <script>
    const vscode = acquireVsCodeApi();
    const $ = (id) => document.getElementById(id);
    let poll = true;
    const COLORS = {};
    // subsystem node -> live-feed kind (click a node to open its thought surface)
    const NODE_FEED = { 'sub:ghost': 'ghost', 'sub:drainer': 'drainer', 'sub:autorun': 'drainer', 'sub:orchestrator': 'drainer' };

    function openFeed(n) {
      const kind = NODE_FEED[n.id];
      if (!kind) return;
      vscode.postMessage({ type: 'run', cmd: 'python -m mag.live_feed ' + kind, name: 'MAG Thought · ' + kind });
    }

    function buildLegend(cats) {
      const el = $('legend');
      el.innerHTML = '';
      Object.keys(cats || {}).forEach(k => {
        const c = cats[k];
        COLORS[k] = c.color;
        const span = document.createElement('span');
        span.className = 'lg';
        span.innerHTML = '<span class="sw" style="background:' + c.color + '"></span> ' + c.label;
        el.appendChild(span);
      });
    }

    function layout(g) {
      // layered radial layout by category
      const cat = (n) => n.category;
      const nodes = g.nodes || [];
      const center = nodes.find(n => n.id === 'run:current');
      const mid = nodes.filter(n => n.category === 'subsystem' || n.category === 'operator');
      const outer = nodes.filter(n => ['provider','signal','metric'].includes(n.category));
      const pos = {};
      const W = 900, H = 620, CX = W/2, CY = H/2;
      const R1 = 150, R2 = 270;

      const ring = (list, r) => {
        const n = list.length;
        list.forEach((node, i) => {
          const a = (i / Math.max(n,1)) * 2 * Math.PI - Math.PI/2;
          pos[node.id] = { x: CX + r*Math.cos(a), y: CY + r*Math.sin(a) };
        });
      };
      if (center) pos[center.id] = { x: CX, y: CY };
      ring(mid, R1);
      ring(outer, R2);
      return pos;
    }

    function render(g) {
      buildLegend(g.categories);
      const pos = layout(g);
      const svg = $('svg');
      const NS = 'http://www.w3.org/2000/svg';
      svg.innerHTML = '';
      const W = 900, H = 620;
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

      // edges
      (g.edges || []).forEach(e => {
        const s = pos[e.src], d = pos[e.dst];
        if (!s || !d) return;
        const line = document.createElementNS(NS, 'line');
        line.setAttribute('class', 'edge');
        line.setAttribute('x1', s.x); line.setAttribute('y1', s.y);
        line.setAttribute('x2', d.x); line.setAttribute('y2', d.y);
        line.setAttribute('stroke', (g.edge_types && g.edge_types[e.type]) || '#8b949e');
        line.setAttribute('stroke-width', '1.2');
        if (e.label) line.setAttribute('data-tip', e.label);
        svg.appendChild(line);
      });

      // nodes
      (g.nodes || []).forEach(n => {
        const p = pos[n.id];
        if (!p) return;
        const gEl = document.createElementNS(NS, 'g');
        gEl.setAttribute('class', 'node');
        gEl.setAttribute('transform', 'translate(' + p.x + ',' + p.y + ')');
        const r = n.id === 'run:current' ? 26 : (n.category === 'subsystem' ? 20 : 14);
        const circ = document.createElementNS(NS, 'circle');
        circ.setAttribute('r', r);
        circ.setAttribute('fill', (COLORS[n.category] || '#8b949e'));
        circ.setAttribute('fill-opacity', n.status === 'warn' ? '0.55' : '0.85');
        const tip = n.id + ' [' + n.status + ']' + (n.meta ? ' ' + JSON.stringify(n.meta) : '');
        circ.setAttribute('data-tip', tip);
        if (NODE_FEED[n.id]) {
          circ.style.cursor = 'pointer';
          circ.setAttribute('data-feed', NODE_FEED[n.id]);
          circ.addEventListener('click', () => openFeed(n));
        }
        gEl.appendChild(circ);
        const t = document.createElementNS(NS, 'text');
        t.setAttribute('y', r + 12);
        t.textContent = n.label.length > 22 ? n.label.slice(0, 22) + '…' : n.label;
        gEl.appendChild(t);
        svg.appendChild(gEl);
      });
    }

    window.addEventListener('message', (ev) => {
      const msg = ev.data;
      if (msg.type !== 'graph') return;
      const g = msg.data;
      $('ts').textContent = (g.ts || '').slice(11, 19);
      $('status').textContent = (g.nodes ? g.nodes.length : 0) + ' nodes · ' + (g.edges ? g.edges.length : 0) + ' edges · ' + g.schema;
      render(g);
    });

    $('refresh').addEventListener('click', () => vscode.postMessage({ type: 'poll', value: true }));
    $('toggle').addEventListener('click', () => {
      poll = !poll;
      $('toggle').textContent = poll ? '⏸ pause' : '▶ resume';
      vscode.postMessage({ type: 'poll', value: poll });
    });
    document.addEventListener('click', (ev) => {
      const btn = ev.target.closest('[data-cmd]');
      if (!btn) return;
      vscode.postMessage({ type: 'run', cmd: btn.getAttribute('data-cmd') });
    });
    vscode.postMessage({ type: 'ready' });
  </script>
</body>
</html>`;
  }
}

module.exports = { OpsGraphPanel };
