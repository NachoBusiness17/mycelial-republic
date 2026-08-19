// mag-dashboard — Sovereign activity-bar views. Live in-canvas rendering, fed CHEAPLY by our swarm.
// Design: Python emits the deterministic state ONCE (tiny); the webview canvas animates it client-
// side via requestAnimationFrame — no per-frame Python, no spawns, no window storm.
const vscode = require('vscode');
const STATE_URL = 'http://127.0.0.1:8766/api/v1/swarm/state'; // our cast REST surface

async function fetchJson(url) {
  try {
    const r = await fetch(url);
    return await r.json();
  } catch (e) {
    return { ok: false, error: String(e) };
  }
}

function makeView(scriptFile, getState) {
  class View {
    resolveWebviewView(webviewView) {
      const wv = webviewView.webview;
      wv.options = { enableScripts: true };
      const script = require('fs').readFileSync(
        require('path').join(__dirname, 'media', scriptFile), 'utf8');
      wv.html = `<!DOCTYPE html><html><head><style>
        body{background:#0a0e14;color:#e6edf3;font-family:system-ui;margin:0;padding:8px}
        canvas{width:100%;height:auto;background:#0d1117;border-radius:8px;border:1px solid #21262d}
        .sub{color:#8b949e;font-size:11px;margin:6px 0}
        </style></head><body><canvas id="c" width="512" height="512"></canvas>
        <div class="sub" id="sub">loading…</div>
        <script>${script}</script>
        </body></html>`;
      // refresh state on a cadence (cheap: once per few seconds, not per frame)
      const refresh = async () => {
        const st = await getState();
        wv.postMessage({ type: 'state', state: st });
      };
      refresh();
      setInterval(refresh, 4000);
      webviewView.onDidDispose(() => clearInterval(refresh));
    }
  }
  return View;
}

function activate(context) {
  const flockView = makeView('flock.js', () => fetchJson(STATE_URL));
  const worldView = makeView('world.js', () => fetchJson(STATE_URL));
  const emergeView = makeView('emerge.js', () => fetchJson(STATE_URL));
  // verkle-knot standing-wave view — reuses the game graph (mag/verkle_render + /api/verkle).
  const verkleView = makeView('verkle.js', () => fetchJson('http://127.0.0.1:8766/api/verkle'));
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider('magFlock', new flockView()),
    vscode.window.registerWebviewViewProvider('magWorld', new worldView()),
    vscode.window.registerWebviewViewProvider('magEmerge', new emergeView()),
    vscode.window.registerWebviewViewProvider('magVerkle', new verkleView())
  );

  // ── LEARNED TRIGGER → auto-focus the active lens's view (2026-08-11) ──
  // The trigger_learn decision (state.trigger.active) says which lens is hot based on learned
  // user signals. We reveal the matching view ONLY on change, so it never thrashes the UI.
  const lensToView = { flock: 'magFlock', world: 'magWorld', emerge: 'magEmerge', verkle: 'magVerkle', 'steal-lens': 'magEmerge' };
  let lastFocused = null;
  const autoFocus = async () => {
    const st = await fetchJson(STATE_URL);
    const trig = st && st.trigger;
    if (!trig || !trig.ok) return;
    const top = (trig.active && trig.active[0]) || (trig.triggers && trig.triggers[0]);
    if (!top) return;
    const viewId = lensToView[top.lens] || 'magWorld';
    if (viewId === lastFocused) return;
    lastFocused = viewId;
    try {
      await vscode.commands.executeCommand(viewId + '.focus');
    } catch (e) { /* view may not be open; ignore */ }
  };
  setInterval(autoFocus, 8000);
}

function deactivate() {}

module.exports = { activate, deactivate };
