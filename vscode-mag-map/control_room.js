// MAG Control Room — live view of drainer / orchestrator / ghost.
// Polls the framework REST endpoints and renders live status.
"use strict";

const vscode = require("vscode");
const http = require("http");

const DASH_HOST = "127.0.0.1";
const DASH_PORT = 8765;

class MagControlRoomProvider {
  constructor(extensionUri) {
    this._extensionUri = extensionUri;
    this._view = null;
    this._timer = null;
  }

  dispose() {
    if (this._timer) {
      clearInterval(this._timer);
      this._timer = null;
    }
  }

  _fetch(url) {
    // Node http GET (guaranteed in extension host; fetch/timeout is unreliable there).
    return new Promise((resolve) => {
      const req = http.get(
        { host: DASH_HOST, port: DASH_PORT, path: url, timeout: 4000 },
        (res) => {
          let body = "";
          res.on("data", (c) => (body += c));
          res.on("end", () => {
            try {
              resolve(JSON.parse(body));
            } catch {
              resolve(null);
            }
          });
        }
      );
      req.on("timeout", () => req.destroy());
      req.on("error", () => resolve(null));
    });
  }

  async _snapshot() {
    const stats = await this._fetch("/api/v1/drainer/stats");
    const drainerLive = await this._fetch("/api/v1/live-feed?kind=drainer&limit=6");
    const ghostLive = await this._fetch("/api/v1/live-feed?kind=ghost&limit=6");
    const overseerLive = await this._fetch("/api/v1/live-feed?kind=overseer&limit=6");
    const sessionFreeze = await this._fetch("/api/v1/session/freeze");
    return { stats, drainerLive, ghostLive, overseerLive, sessionFreeze };
  }

  start() {
    if (this._timer) clearInterval(this._timer);
    this._timer = setInterval(() => this._tick(), 3000);
    this._tick();
  }

  async _tick() {
    if (!this._view) return;
    const snap = await this._snapshot();
    if (this._view) {
      this._view.webview.postMessage({ type: "snapshot", data: snap });
    }
  }

  resolveWebviewView(webviewView) {
    this._view = webviewView;
    webviewView.webview.options = { enableScripts: true };
    webviewView.webview.html = this._html();

    webviewView.webview.onDidReceiveMessage(async (msg) => {
      if (msg.type === "ready") {
        this._tick();
        this.start();
      } else if (msg.type === "run") {
        const term = vscode.window.createTerminal({ name: msg.name || "MAG", cwd: undefined });
        term.show();
        term.sendText(msg.cmd);
      }
    });

    webviewView.onDidDispose(() => {
      this._view = null;
      this.dispose();
    });
  }

  _html() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy"
  content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Control Room</title>
<style>
  :root { color-scheme: dark; }
  body { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: #0d1117; color: #c9d1d9; margin: 0; padding: 12px; }
  h1 { font-size: 14px; margin: 0 0 10px; color: #58a6ff; letter-spacing: 0.5px; }
  h2 { font-size: 12px; margin: 14px 0 6px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; }
  .row { display: flex; flex-wrap: wrap; gap: 8px; }
  .card { border: 1px solid #30363d; border-radius: 6px; padding: 8px 10px; min-width: 120px; }
  .card .k { font-size: 10px; color: #8b949e; }
  .card .v { font-size: 16px; font-weight: 600; }
  .on { color: #3fb950; } .off { color: #f85149; } .warn { color: #d29922; }
  table { width: 100%; border-collapse: collapse; font-size: 11px; }
  td, th { text-align: left; padding: 3px 6px; border-bottom: 1px solid #21262d; white-space: nowrap; }
  th { color: #8b949e; }
  .goal { max-width: 380px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .btn { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 4px; padding: 3px 8px; font-size: 11px; cursor: pointer; margin-right: 6px; }
  .btn:hover { background: #30363d; }
  .btn.ts { padding: 6px 12px; font-size: 12px; border-color: #388bfd55; color: #58a6ff; }
  .btn.ts:hover { background: #1f3a5f; border-color: #58a6ff; }
  .muted { color: #8b949e; font-size: 10px; }
  #bar { margin: 10px 0; display: flex; gap: 6px; flex-wrap: wrap; }
  .live { color: #3fb950; animation: pulse 1.6s infinite; }
  @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
</style>
</head>
<body>
  <h1>⚙️ MAG Control Room <span class="muted" id="ts"></span>
    <span class="live" id="liveDot" style="display:none;">●</span>
    <span class="off" id="errorDot" style="display:none;">●</span>
  </h1>
  <div id="errorBanner" style="display:none; background:#3d1f1f; border:1px solid #f85149; border-radius:6px; padding:8px; margin-bottom:10px; font-size:11px;">
    <span class="off">⚠ Dashboard not reachable (port 8765)</span>
    <button class="btn" data-cmd="python main.py lab">Start Dashboard</button>
    <button class="btn" id="retryBtn">Retry</button>
  </div>
    <button class="btn" data-cmd="python -m mag.drainer_stats">Drainer Stats</button>
    <button class="btn" data-cmd="python -m mag.live_feed drainer">Drainer Feed</button>
    <button class="btn" data-cmd="python -m mag.live_feed ghost">Ghost Feed</button>
    <button class="btn" data-cmd="python -m mag.live_feed overseer">Overseer Feed</button>
    <button class="btn" data-cmd="python -m mag.session_state_brief">Refresh Brief</button>
  </div>

  <h2>Drainer / Pipeline</h2>
  <div class="row" id="pipeline"></div>

  <h2>Session State <span class="muted" id="sessionTs"></span></h2>
  <div class="row" id="sessionCards"></div>
  <div class="muted" id="sessionGoal" style="margin:4px 0 10px;"></div>
  <div style="margin:4px 0 8px;">
    <button class="btn" data-cmd="python -m mag.session_freeze --compact">Freeze Snapshot</button>
    <button class="btn" data-cmd="python -m mag.session_freeze --file memory/freeze/manual.json">Freeze to File</button>
  </div>

  <h2>Queue <span class="muted" id="queueCount"></span></h2>
  <table id="queue"><tr><th>status</th><th class="goal">goal</th><th>provider</th></tr></table>

  <h2>Pending Handoffs <span class="muted" id="handoffCount"></span></h2>
  <table id="handoffs"><tr><th>from → to</th><th class="goal">goal</th></tr></table>

  <h2>Live Trail — Drainer</h2>
  <table id="drainerTrail"><tr><th>ts</th><th>event</th><th class="goal">detail</th></tr></table>

  <h2>Live Trail — Ghost</h2>
  <table id="ghostTrail"><tr><th>ts</th><th>event</th><th class="goal">detail</th></tr></table>

  <h2>Live Trail — Overseer</h2>
  <table id="overseerTrail"><tr><th>ts</th><th>event</th><th class="goal">detail</th></tr></table>

  <script>
    const $ = (id) => document.getElementById(id);
    const el = (tag, text, cls) => { const e = document.createElement(tag); e.textContent = text || ''; if (cls) e.className = cls; return e; };

    function trailRows(rows, table, kind) {
      const tb = table.querySelector('tbody') || table.createTBody();
      tb.innerHTML = '';
      (rows || []).slice(-8).reverse().forEach(r => {
        const tr = document.createElement('tr');
        tr.appendChild(el('td', (r.ts || r.timestamp || '').slice(11, 19), 'muted'));
        tr.appendChild(el('td', (r.event || r.type || r.kind || kind || '')));
        tr.appendChild(el('td', (r.goal || r.message || r.detail || '').slice(0, 120), 'goal'));
        tb.appendChild(tr);
      });
    }

    window.addEventListener('message', (ev) => {
      const msg = ev.data;
      if (msg.type !== 'snapshot') return;
      const d = msg.data || {};
      const s = d.stats || {};
      $('ts').textContent = (s.ts || '').slice(11, 19);

      // Show live dot, hide error
      $('liveDot').style.display = 'inline';
      $('errorDot').style.display = 'none';
      $('errorBanner').style.display = 'none';

      // pipeline
      const pl = $('pipeline');
      pl.innerHTML = '';
      const dr = s.drainer || {};
      const q = s.queue || {};
      const card = (k, v, cls) => { const c = document.createElement('div'); c.className = 'card'; c.appendChild(el('div', k, 'k')); c.appendChild(el('div', v, cls || '')); pl.appendChild(c); };
      card('drainer', dr.enabled ? 'ON' : 'OFF', dr.enabled ? 'on' : 'off');
      card('autorun', dr.autorun_allowed ? 'allowed' : 'paused', dr.autorun_allowed ? 'on' : 'warn');
      card('fleet live', s.fleet ? s.fleet.live_n : '-', '');
      card('handoffs', s.pending_handoffs_n || 0, '');
      card('queue running', (q.counts && q.counts.running) || 0, '');

      // queue
      const qb = $('queue').createTBody();
      qb.innerHTML = '';
      $('queueCount').textContent = (s.queue_items || []).length;
      (s.queue_items || []).slice(0, 12).forEach(i => {
        const tr = document.createElement('tr');
        tr.appendChild(el('td', i.status));
        tr.appendChild(el('td', i.goal, 'goal'));
        tr.appendChild(el('td', i.provider));
        qb.appendChild(tr);
      });

      // handoffs
      const hb = $('handoffs').createTBody();
      hb.innerHTML = '';
      $('handoffCount').textContent = (s.pending_handoffs || []).length;
      (s.pending_handoffs || []).slice(0, 10).forEach(h => {
        const tr = document.createElement('tr');
        tr.appendChild(el('td', (h.from || '') + ' \u2192 ' + (h.to || '')));
        tr.appendChild(el('td', h.goal, 'goal'));
        hb.appendChild(tr);
      });

      trailRows(d.drainerLive && d.drainerLive.lines, $('drainerTrail'), 'drainer');
      trailRows(d.ghostLive && d.ghostLive.lines, $('ghostTrail'), 'ghost');
      trailRows(d.overseerLive && d.overseerLive.lines, $('overseerTrail'), 'overseer');

      // session state (from session/freeze endpoint)
      const sf = d.sessionFreeze || {};
      const ses = (sf.layers && sf.layers.session_context) || sf.summary || {};
      $('sessionTs').textContent = (sf.ts || '').slice(11, 19);
      const sc = $('sessionCards');
      sc.innerHTML = '';
      const scard = (k, v, cls) => { const c = document.createElement('div'); c.className = 'card'; c.appendChild(el('div', k, 'k')); c.appendChild(el('div', v || '?', cls || '')); sc.appendChild(c); };
      scard('goal', (ses.current_goal || sf.summary?.goal || '?').slice(0, 60) + (((ses.current_goal || sf.summary?.goal || '')?.length || 0) > 60 ? '…' : ''), 'goal');
      scard('status', ses.current_status || sf.summary?.status || '?', (ses.current_status || '') === 'running' ? 'on' : ((ses.current_status || '') === 'blocked' ? 'off' : 'warn'));
      scard('tier', ses.current_tier || '?', '');
      scard('step', ses.current_step || '?', '');
      scard('plan steps', ses.current_plan_steps != null ? ses.current_plan_steps : '?', '');
      scard('brief verkle', ses.brief_verkle_root || '?', '');
      scard('coding session', ses.coding_session_status || '?', (ses.coding_session_status || '') === 'ready' ? 'on' : '');
      const kw = ses._keywords || sf.summary?.keywords || [];
      if (kw && kw.length) {
        const kwDiv = document.createElement('div');
        kwDiv.style.cssText = 'font-size:10px;color:#8b949e;margin-top:4px;';
        kwDiv.textContent = 'keywords: ' + kw.slice(0, 8).join(', ');
        sc.appendChild(kwDiv);
      }
      const goalText = ses.current_goal || sf.summary?.goal || '';
      if (goalText) {
        $('sessionGoal').textContent = '▸ ' + goalText;
      }
    });

    document.addEventListener('click', (ev) => {
      const btn = ev.target.closest('.btn');
      if (!btn) return;
      if (btn.id === 'retryBtn') {
        acquireVsCodeApi().postMessage({ type: 'ready' });
        return;
      }
      const cmd = btn.getAttribute('data-cmd');
      acquireVsCodeApi().postMessage({ type: 'run', cmd, name: 'MAG Control' });
    });

    // Show error state after 10s if no snapshot received
    setTimeout(() => {
      if ($('liveDot').style.display === 'none' || !$('liveDot').style.display) {
        $('errorDot').style.display = 'inline';
        $('errorBanner').style.display = 'block';
      }
    }, 10000);

    // Signal ready to start polling
    acquireVsCodeApi().postMessage({ type: 'ready' });
  </script>
</body>
</html>`;
  }
}

module.exports = { MagControlRoomProvider };
