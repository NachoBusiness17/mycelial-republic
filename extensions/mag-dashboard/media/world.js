// world.js — world_rib mesh viewer: renders the compiled 2D scalar field + 3D .obj terrain live.
// State (the field + mesh) is emitted ONCE from Python (world_rib.world_from_rib); this script
// draws it client-side. GPU-free path = 2D canvas heightmap; GPU path = WebGL wireframe/points.
(function () {
  const vscode = acquireVsCodeApi && acquireVsCodeApi();
  const canvas = document.getElementById('c');
  const sub = document.getElementById('sub');
  const ctx = canvas.getContext('2d');
  let gl = null;
  try { gl = canvas.getContext('webgl2') || canvas.getContext('webgl'); } catch (e) { gl = null; }
  const SIZE = 512;

  // default deterministic world (mirrors mag.world_rib.compile relief) so it shows before state
  function defaultWorld() {
    const w = 64, h = 64; const field = [];
    let seed = 1337;
    const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
    for (let y = 0; y < h; y++) { const row = [];
      for (let x = 0; x < w; x++) {
        let v = 0.5 + 0.5 * Math.sin(x * 0.18 + rnd() * 0.2) * Math.cos(y * 0.18);
        row.push(Math.max(0, Math.min(1, v)));
      } field.push(row);
    }
    return { field, w, h, peaks: [{ x: 0.3, y: 0.3, r: 0.08 }, { x: 0.7, y: 0.7, r: 0.08 }] };
  }
  let world = defaultWorld();
  let renderMode = gl ? 'GPU' : 'CPU';

  function toRGB(hex) {
    const h = hex.replace('#', '');
    return [parseInt(h.substr(0, 2), 16) / 255, parseInt(h.substr(2, 2), 16) / 255, parseInt(h.substr(4, 2), 16) / 255];
  }

  function setupGL() {
    const vs = `attribute vec2 aPos;attribute vec3 aColor;varying vec3 vC;void main(){
      gl_Position=vec4(aPos,0.0,1.0);gl_PointSize=2.0;vC=aColor;}`;
    const fs = `precision mediump float;varying vec3 vC;void main(){gl_FragColor=vec4(vC,1.0);}`;
    function comp(t, s) { const sh = gl.createShader(gl[t]); gl.shaderSource(sh, s); gl.compileShader(sh); return sh; }
    const prog = gl.createProgram();
    gl.attachShader(prog, comp('VERTEX_SHADER', vs));
    gl.attachShader(prog, comp('FRAGMENT_SHADER', fs));
    gl.linkProgram(prog); gl.useProgram(prog);
    gl.aPos = gl.getAttribLocation(prog, 'aPos');
    gl.aColor = gl.getAttribLocation(prog, 'aColor');
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.enableVertexAttribArray(gl.aPos); gl.vertexAttribPointer(gl.aPos, 2, gl.FLOAT, false, 20, 0);
    gl.enableVertexAttribArray(gl.aColor); gl.vertexAttribPointer(gl.aColor, 3, gl.FLOAT, false, 20, 8);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.prog = prog; gl.buf = buf;
  }

  function renderWorldGL() {
    // Cap the sample grid (webview heap stays small even if Python sends a huge field).
    const { field, w, h } = world;
    const fw = Math.max(1, Math.min(w, 256)), fh = Math.max(1, Math.min(h, 256));
    const sx = w / fw, sy = h / fh;
    const pts = [];
    for (let y = 0; y < fh; y++) for (let x = 0; x < fw; x++) {
      const v = field[Math.floor(y * sy)][Math.floor(x * sx)];
      pts.push(x / fw * 2 - 1, 1 - y / fh * 2, 0.2 + v * 0.5, 0.4 + (1 - v) * 0.3, 0.5 + v * 0.4);
    }
    gl.clearColor(0.05, 0.07, 0.09, 1); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(pts), gl.DYNAMIC_DRAW);
    gl.drawArrays(gl.POINTS, 0, pts.length / 5);
  }

  // Reuse ONE ImageData buffer — never allocate per frame (keeps the webview heap flat).
  let imgBuf = null;
  function renderWorld2D() {
    const { field, w, h } = world;
    const fw = Math.max(1, Math.min(w, 256)), fh = Math.max(1, Math.min(h, 256));
    const sx = w / fw, sy = h / fh;
    if (!imgBuf || imgBuf.width !== fw || imgBuf.height !== fh) imgBuf = ctx.createImageData(fw, fh);
    const data = imgBuf.data;
    for (let y = 0; y < fh; y++) for (let x = 0; x < fw; x++) {
      const v = field[Math.floor(y * sy)][Math.floor(x * sx)];
      const i = (y * fw + x) * 4;
      data[i] = 40 + v * 160; data[i + 1] = 90 + (1 - v) * 90; data[i + 2] = 120 + v * 120; data[i + 3] = 255;
    }
    ctx.putImageData(imgBuf, 0, 0);
  }

  // Static renderer: draw on demand (state change / resize), never a 60fps idle loop.
  function render() { if (gl) renderWorldGL(); else renderWorld2D(); }
  let resizeRaf = null;
  window.addEventListener('resize', () => { if (resizeRaf) return; resizeRaf = requestAnimationFrame(() => { resizeRaf = null; render(); }); });

  if (vscode) {
    window.addEventListener('message', (e) => {
      const m = e.data;
      if (m && m.type === 'state') {
        const s = m.state || {};
        if (s.world && s.world.field && s.world.w && s.world.h) {
          world = { field: s.world.field, w: s.world.w, h: s.world.h,
                    peaks: s.world.peaks || world.peaks };
          render();
          sub.textContent = `world · ${world.w}×${world.h} field · render=${renderMode} · gpu_free=${!!(s.gpu && s.gpu.free_for_render)}`;
        } else {
          sub.textContent = `world · awaiting swarm state (field) · render=${renderMode}`;
        }
      }
    });
  }
  if (gl) setupGL();
  render(); // first paint (after GL setup so the GL path has its buffer)
  sub.textContent = `world · ${world.w}×${world.h} field · render=${renderMode}`;
})();
