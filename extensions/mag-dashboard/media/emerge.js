// emerge.js — emergence grid: live analytics from the emergence module (memory/emergence/grid.jsonl),
// rendered as a scrolling grid + trend in-canvas. Cheap: state once per cadence, animate client-side.
(function () {
  const vscode = acquireVsCodeApi && acquireVsCodeApi();
  const canvas = document.getElementById('c');
  const sub = document.getElementById('sub');
  const ctx = canvas.getContext('2d');
  const SIZE = 512;
  let rows = []; // [{label, value, delta, lens}]
  let grid = null;

  function draw() {
    ctx.fillStyle = '#0d1117'; ctx.fillRect(0, 0, SIZE, SIZE);
    // header bar
    ctx.fillStyle = '#161b22'; ctx.fillRect(0, 0, SIZE, 28);
    ctx.fillStyle = '#8b949e'; ctx.font = '11px system-ui'; ctx.fillText('EMERGENCE GRID · self-improve loop', 8, 18);
    let y = 36;
    const shown = rows.length ? rows : defaultRows();
    const h = Math.floor((SIZE - 36) / Math.max(shown.length, 1));
    for (const r of shown.slice(0, 16)) {
      const x = 8;
      ctx.fillStyle = '#c9d1d9'; ctx.fillText(r.label, x, y + 12);
      ctx.fillStyle = r.delta > 0 ? '#3fb950' : r.delta < 0 ? '#f85149' : '#8b949e';
      ctx.fillText(String(r.value), SIZE - 90, y + 12);
      const up = r.delta > 0;
      ctx.fillStyle = up ? '#3fb950' : r.delta < 0 ? '#f85149' : '#6e7681';
      ctx.fillText((up ? '▲' : r.delta < 0 ? '▼' : '·') + (r.delta !== 0 ? Math.abs(r.delta) : ''), SIZE - 44, y + 12);
      // sparkline bar
      ctx.fillStyle = '#21262d'; ctx.fillRect(90, y, SIZE - 190, 2);
      ctx.fillStyle = up ? '#3fb950' : '#8b949e';
      ctx.fillRect(90, y, Math.min((SIZE - 190) * Math.min(Math.abs(r.delta) / 100, 1), SIZE - 190), 2);
      y += h;
    }
  }

  function defaultRows() {
    return [
      { label: 'flock paths rendered', value: 48, delta: 12, lens: 'compiler/world' },
      { label: 'invariants sharded', value: 15, delta: 3, lens: 'memory/invariant' },
      { label: 'steals lensed', value: 7, delta: 2, lens: 'memory/invariant' },
      { label: 'novelty score (avg)', value: 0.62, delta: 0.05, lens: 'memory/invariant' },
      { label: 'cache hit %', value: 99.2, delta: 0.4, lens: 'economics/cost' },
      { label: 'spikes predicted', value: 2, delta: 1, lens: 'economics/cost' },
    ];
  }

  function drawLoop(loop) {
    // republic_loop output: per-step ok/error + the loop's measured feedback. The heartbeat visible.
    ctx.fillStyle = '#0d1117'; ctx.fillRect(0, 0, SIZE, SIZE);
    ctx.fillStyle = '#161b22'; ctx.fillRect(0, 0, SIZE, 28);
    ctx.fillStyle = '#8b949e'; ctx.font = '11px system-ui';
    ctx.fillText('REPUBLIC LOOP · ' + (loop.n_ok || 0) + '/' + (loop.n_steps || 0) + ' steps ok', 8, 18);
    const steps = loop.steps || [];
    const h = Math.floor((SIZE - 34) / Math.max(steps.length, 1));
    steps.forEach((s, i) => {
      const y = 34 + i * h;
      const ok = s.ok;
      ctx.fillStyle = ok ? '#3fb950' : '#f85149';
      ctx.fillRect(6, y + 2, 4, h - 6);
      ctx.fillStyle = '#c9d1d9'; ctx.font = '10px system-ui';
      ctx.fillText((s.step || '') + (ok ? '' : ' · ' + ((s.error || '').slice(0, 40))), 16, y + h - 4);
    });
    // footer: measured loop output
    const lo = loop.loop_output || {};
    ctx.fillStyle = '#8b949e'; ctx.font = '10px system-ui';
    ctx.fillText('output: ' + JSON.stringify(lo), 6, SIZE - 6);
  }

  // Static renderer: draw on demand (state change), not a continuous 60fps idle loop.
  draw();

  function drawShader(frame) {
    // lens_shader frame: render each lens as a colored weight bar (the lensing map as a texture)
    ctx.fillStyle = '#0d1117'; ctx.fillRect(0, 0, SIZE, SIZE);
    ctx.fillStyle = '#161b22'; ctx.fillRect(0, 0, SIZE, 28);
    ctx.fillStyle = '#8b949e'; ctx.font = '11px system-ui';
    const active = frame.active_lens || '';
    ctx.fillText('LENS SHADER · ' + (frame.render_target || 'cpu').toUpperCase() + ' · active=' + active, 8, 18);
    const cols = frame.frame || [];
    const h = Math.floor((SIZE - 36) / Math.max(cols.length, 1));
    cols.forEach((l, i) => {
      const y = 40 + i * h;
      const c = l.color || [0.5, 0.5, 0.5];
      const rgb = 'rgb(' + Math.round(c[0] * 255) + ',' + Math.round(c[1] * 255) + ',' + Math.round(c[2] * 255) + ')';
      ctx.fillStyle = '#21262d'; ctx.fillRect(90, y, SIZE - 180, h - 6);
      ctx.fillStyle = rgb; ctx.fillRect(90, y, (SIZE - 180) * (l.weight || 0), h - 6);
      ctx.fillStyle = l.active ? '#e6edf3' : '#8b949e';
      ctx.font = '11px system-ui';
      ctx.fillText((l.active ? '▶ ' : '') + l.lens, 8, y + 14);
      ctx.fillText(String(l.weight), SIZE - 84, y + 14);
    });
  }

  if (vscode) {
    window.addEventListener('message', (e) => {
      const m = e.data;
      if (m && m.type === 'state') {
        const s = m.state || {};
        // republic_loop output takes priority (the whole heartbeat at a glance)
        if (s.republic_loop && s.republic_loop.steps) {
          drawLoop(s.republic_loop);
          sub.textContent = `loop · ${s.republic_loop.n_ok}/${s.republic_loop.n_steps} steps · ` +
            JSON.stringify(s.republic_loop.loop_output || {});
          return;
        }
        const em = s.emergence;
        if (em && em.metrics) {
          rows = Object.entries(em.metrics).map(([label, v]) => ({
            label, value: typeof v === 'number' ? (Math.round(v * 100) / 100) : String(v), delta: 0, lens: 'metrics'
          }));
          draw();
        }
        if (s.lens_shader && s.lens_shader.frame) {
          drawShader(s.lens_shader);
          const gpu = (s.gpu && s.gpu.free_for_render) ? 'gpu_free' : 'gpu_busy';
          sub.textContent = `lens-shader · ${s.lens_shader.frame.length} lenses · active=${s.lens_shader.active_lens} · target=${s.lens_shader.render_target} · ${gpu}`;
          return;
        }
        sub.textContent = `emerge · ${rows.length} metrics · gpu_free=${!!(s.gpu && s.gpu.free_for_render)}`;
      }
    });
  }
  sub.textContent = `emerge · live lens-shader + emergence grid`;
})();
