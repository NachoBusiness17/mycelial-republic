// flock.js — ShaderToy-style flock path preview, rendered live in the webview canvas.
// Inherent GPU-awareness: if the swarm's gpu_lifecycle says the GPU is free, we render with WebGL
// (GPU); otherwise we fall back to the 2D canvas (CPU). State is emitted ONCE from Python on a
// slow cadence; this script animates client-side via requestAnimationFrame — no per-frame Python,
// no spawns, no window storm.
(function () {
  const vscode = acquireVsCodeApi && acquireVsCodeApi();
  const canvas = document.getElementById('c');
  const sub = document.getElementById('sub');
  const ctx2d = canvas.getContext('2d');
  let gl = null;
  try {
    gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
  } catch (e) { gl = null; }  let glArr = null; // reused vertex buffer (webview heap stays flat)
  // --- deterministic local flock state (so it animates even before Python state arrives) ---
  function mulberry32(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  const N = 28, GOALS = 2, FRAMES = 48, SIZE = 512;
  let state = null;
  function defaultGoals() {
    return [{ x: 0.25, y: 0.25, r: 0.06, c: '#4ec9b0' }, { x: 0.75, y: 0.75, r: 0.06, c: '#569cd6' }];
  }
  function makeFlock(seed) {
    const rnd = mulberry32(seed || 2086788729331433854);
    const goals = defaultGoals();
    const agents = [];
    for (let i = 0; i < N; i++) {
      agents.push({ x: rnd(), y: rnd(), trail: [] });
    }
    // pre-compute the deterministic path (mirrors mag.flock_anim.evolve): simple attraction
    const frames = [];
    let cur = agents.map(a => ({ x: a.x, y: a.y }));
    for (let f = 0; f < FRAMES; f++) {
      const next = cur.map((a, i) => {
        const g = goals[i % goals.length];
        const gx = g.x * (0.5 + 0.4 * Math.sin(f * 0.1 + i));
        const gy = g.y * (0.5 + 0.4 * Math.cos(f * 0.09 + i * 0.7));
        return {
          x: a.x + (gx - a.x) * 0.04 + (rnd() - 0.5) * 0.02,
          y: a.y + (gy - a.y) * 0.04 + (rnd() - 0.5) * 0.02
        };
      });
      frames.push(next);
      cur = next;
    }
    return { goals, agents, frames, seed };
  }
  let flock = makeFlock();

  // --- WebGL (GPU) path: draw agent trail splats via textured points with additive bloom ---
  function setupGL() {
    const vs = `attribute vec2 aPos;attribute vec3 aColor;varying vec3 vC;
      uniform vec2 uScale;void main(){gl_Position=vec4(aPos*uScale,0.0,1.0);gl_PointSize=4.0;vC=aColor;}`;
    const fs = `precision mediump float;varying vec3 vC;void main(){
      float d=length(gl_PointCoord-0.5);if(d>0.5)discard;
      float a=1.0-smoothstep(0.0,0.5,d);gl_FragColor=vec4(vC,a*0.85);}`;
    function comp(t, s) {
      const sh = gl.createShader(gl[t]); gl.shaderSource(sh, s); gl.compileShader(sh);
      return sh;
    }
    const prog = gl.createProgram();
    gl.attachShader(prog, comp('VERTEX_SHADER', vs));
    gl.attachShader(prog, comp('FRAGMENT_SHADER', fs));
    gl.linkProgram(prog); gl.useProgram(prog);
    gl.uScale = gl.getUniformLocation(prog, 'uScale');
    gl.aPos = gl.getAttribLocation(prog, 'aPos');
    gl.aColor = gl.getAttribLocation(prog, 'aColor');
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.enableVertexAttribArray(gl.aPos); gl.vertexAttribPointer(gl.aPos, 2, gl.FLOAT, false, 20, 0);
    gl.enableVertexAttribArray(gl.aColor); gl.vertexAttribPointer(gl.aColor, 3, gl.FLOAT, false, 20, 8);
    gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
    gl.viewport(0, 0, canvas.width, canvas.height);
    return { prog, buf };
  }

  function toRGB(hex) {
    const h = hex.replace('#', '');
    return [parseInt(h.substr(0, 2), 16) / 255, parseInt(h.substr(2, 2), 16) / 255, parseInt(h.substr(4, 2), 16) / 255];
  }

  // GPU rendering: points per agent per visible frame of its trail
  function renderGL(frame) {
    const pts = [];
    const goals = flock.goals;
    for (let g = 0; g < goals.length; g++) pts.push([goals[g].x * 2 - 1, 1 - goals[g].y * 2, ...toRGB(goals[g].c)]);
    const seen = Math.min(frame + 1, FRAMES);
    for (let a = 0; a < flock.agents.length; a++) {
      const c = toRGB(flock.agents[a].i % 2 ? '#e6edf3' : '#8b949e');
      for (let f = Math.max(0, frame - 12); f < seen; f++) {
        const p = flock.frames[f][a];
        pts.push([p.x * 2 - 1, 1 - p.y * 2, ...c]);
      }
    }
    gl.clearColor(0.05, 0.07, 0.09, 1); gl.clear(gl.COLOR_BUFFER_BIT);
    const flat = pts.flat();
    if (!glArr || glArr.length !== flat.length) glArr = new Float32Array(flat); else glArr.set(flat);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.buf);
    gl.bufferData(gl.ARRAY_BUFFER, glArr, gl.DYNAMIC_DRAW);
    gl.uniform2f(gl.uScale, 1, 1);
    gl.drawArrays(gl.POINTS, 0, pts.length / 5);
  }

  // CPU path (2D canvas): same trail + bloom feel, cheap
  function render2D(frame) {
    ctx2d.fillStyle = '#0d1117'; ctx2d.fillRect(0, 0, SIZE, SIZE);
    const seen = Math.min(frame + 1, FRAMES);
    for (const g of flock.goals) {
      ctx2d.beginPath(); ctx2d.arc(g.x * SIZE, g.y * SIZE, g.r * SIZE, 0, 7); ctx2d.fillStyle = g.c; ctx2d.fill();
    }
    for (let a = 0; a < flock.agents.length; a++) {
      const c = flock.agents[a].i % 2 ? '#e6edf3' : '#8b949e';
      for (let f = Math.max(0, frame - 12); f < seen; f++) {
        const p = flock.frames[f][a];
        ctx2d.fillStyle = c; ctx2d.globalAlpha = 0.5;
        ctx2d.fillRect(p.x * SIZE, p.y * SIZE, 2, 2);
      }
      ctx2d.globalAlpha = 1;
    }
  }

  // --- animate client-side (no per-frame Python) — throttled, so the webview heap stays flat ---
  let frame = 0, mode = gl ? 'GPU' : 'CPU';
  let raf = null, last = 0;
  const FPS = 24, INTERVAL = 1000 / FPS;
  function tick(ts) {
    if (ts - last >= INTERVAL) { last = ts; if (gl) renderGL(frame); else render2D(frame); frame = (frame + 1) % FRAMES; }
    raf = requestAnimationFrame(tick);
  }
  raf = requestAnimationFrame(tick);

  // --- consume slow-cadence state from Python (cast REST), prefer GPU when free ---
  if (vscode) {
    window.addEventListener('message', (e) => {
      const m = e.data;
      if (m && m.type === 'state') {
        const s = m.state || {};
        const fs = s.flock;
        if (fs && fs.goals && fs.agents) {
          const rnd = mulberry32(Number(fs.seed) || 1);
          flock = { goals: fs.goals.map(g => ({ x: g.x, y: g.y, r: g.r, c: g.c })),
                    agents: fs.agents.map(a => ({ x: a.x, y: a.y, i: a.i || 0 })), frames: [], seed: fs.seed };
          for (let f = 0; f < FRAMES; f++) {
            flock.frames.push(fs.agents.map((a, i) => {
              const g = flock.goals[i % flock.goals.length];
              return { x: a.x + (g.x - a.x) * 0.04, y: a.y + (g.y - a.y) * 0.04 };
            }));
          }
        }
        // GPU lifecycle: if the swarm says GPU is free, prefer WebGL; else CPU
        const gl2 = s.gpu && s.gpu.free_for_render;
        if (gl2 && !gl) { try { gl = canvas.getContext('webgl2') || canvas.getContext('webgl'); if (gl) setupGL(); } catch (e) {} }
        mode = gl ? 'GPU' : 'CPU';
        const trig = s.trigger && s.trigger.active && s.trigger.active[0];
        sub.textContent = `flock · ${flock.agents.length} agents · ${FRAMES} frames · render=${mode} · gpu_free=${!!(s.gpu && s.gpu.free_for_render)}` +
          (trig ? ` · active_lens=${trig.lens}(${trig.top_signal})` : '');
      }
    });
  }
  if (gl) setupGL();
  sub.textContent = `flock · ${N} agents · ${FRAMES} frames · render=${mode}`;
})();
