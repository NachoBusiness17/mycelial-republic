// Minimal DOM/canvas shim: does the game script boot and paint green?
const calls = [];
function makeCtx() {
  const ctx = {};
  for (const k of ['clearRect','fillRect','strokeRect','beginPath','arc','ellipse','moveTo','lineTo','stroke','fill','save','restore','translate','rotate','scale','setLineDash','closePath','quadraticCurveTo','drawImage','fillText','strokeText','measureText','createLinearGradient','createRadialGradient']) {
    ctx[k] = (...a) => { if (k==='fillRect'||k==='clearRect') calls.push([k,...a]); if(k==='fillRect') { if(!global.__lastFill) global.__lastFill = {style: ctx.__fillStyle, a}; } };
  }
  let _fs = '';
  Object.defineProperty(ctx, 'fillStyle', { set(v){ ctx.__fillStyle = v; _fs = v; }, get(){ return _fs; } });
  ctx.lineWidth = 1; ctx.strokeStyle = ''; ctx.font = ''; ctx.globalAlpha = 1;
  ctx.measureText = () => ({ width: 10 });
  ctx.createLinearGradient = () => ({ addColorStop(){} });
  ctx.createRadialGradient = () => ({ addColorStop(){} });
  return ctx;
}
const elements = {};
function makeEl(id) {
  const el = {
    id, style: {}, classList: { add(){}, remove(){}, contains(){ return false; } },
    addEventListener(){}, textContent: '', innerHTML: '',
  };
  return el;
}
const canvasEl = Object.assign(makeEl('gc'), { width: 0, height: 0, getContext: () => mainCtx });
const mainCtx = makeCtx();
global.document = {
  getElementById(id){ if(id==='gc') return canvasEl; if(!elements[id]) elements[id] = makeEl(id); return elements[id]; },
  querySelectorAll(){ return { forEach(){} }; },
  addEventListener(){},
};
global.window = {
  innerWidth: 1280, innerHeight: 720,
  addEventListener(){},
};
global.performance = { now: () => Date.now() };
let rafQueued = 0;
global.requestAnimationFrame = (fn) => { rafQueued++; if (rafQueued <= 5) setImmediate(() => fn(performance.now())); };
global.Date = Date;

try {
  const src = require('fs').readFileSync(__dirname + '/_sf_script_extracted.js', 'utf-8');
  eval(src);
  // drive loop frames
  setTimeout(() => {
    console.log('BOOT_OK');
    console.log('canvas.width set to:', canvasEl.width, 'height:', canvasEl.height);
    console.log('fillRect calls:', calls.length);
    console.log('last fill:', JSON.stringify(global.__lastFill));
    process.exit(0);
  }, 200);
} catch (e) {
  console.log('TOP_LEVEL_EXCEPTION:', e.constructor.name + ':', e.message);
  console.log(e.stack.split('\n').slice(0,5).join('\n'));
  process.exit(1);
}
