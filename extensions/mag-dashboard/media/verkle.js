// verkle.js — mag-dashboard verkle-knot standing-wave view (reuse of the game graph, 2026-08-15).
// Reuses the SAME renderer as game.html / verkle_knot_wave.html. State comes from /api/verkle
// (h_chain: {tip, evolution, ...}) — we extract the real knots from evolution.series.
// The shape is never stored — only the chain. Deterministic client-side animation, no per-frame Python.
(function () {
  const vscode = acquireVsCodeApi && acquireVsCodeApi();
  const canvas = document.getElementById('c');
  const sub = document.getElementById('sub');
  const ctx = canvas.getContext('2d');

  const THEME_COLORS = { mirror_meta:'#e6c07a', mag_hands:'#7fb2ff', scrum_plan:'#ff7b3d',
    constitution:'#7dffb0', dashboard:'#ffb057', harness:'#a07dff', biography:'#d8cfc0',
    data_r0:'#5fd4ff', autonomous_janitor:'#ff9db0', standing_wave:'#7dffb0', ghost:'#8fd8a8' };
  const DEF = '#9c8570';

  let KNOTS = [];
  let TIP = { root:'', n_leaves:0 };

  function buildKnots(evolution){
    const series = (evolution && evolution.series) || [];
    const list = series.filter(k=>k && k.dominant_theme).slice(-260);
    return list.map((k,i)=>{
      const th = String(k.dominant_theme||'untagged');
      return { i, theme:th, color:THEME_COLORS[th]||DEF,
        tension: parseFloat(k.tension_index)||0, hash:String(k.leaf_hash||'').slice(0,8) };
    });
  }

  function layout(W,H){
    const cx=W*0.44, cy=H*0.5, N=KNOTS.length, step=Math.min(W,H)*0.5/Math.max(1,N)*0.9;
    const pts=[];
    for(let i=0;i<N;i++){ const a=i*2.39996323; const r=16+i*step; pts.push({x:cx+Math.cos(a)*r,y:cy+Math.sin(a)*r}); }
    return pts;
  }

  function draw(t){
    const W=canvas.width, H=canvas.height;
    ctx.clearRect(0,0,W,H);
    if(!KNOTS.length){ sub.textContent='no knots yet — waiting for /api/verkle…'; return; }
    const pts=layout(W,H), N=KNOTS.length;
    ctx.strokeStyle='rgba(127,178,255,.16)'; ctx.lineWidth=1; ctx.beginPath();
    for(let i=0;i<N-1;i++){ ctx.moveTo(pts[i].x,pts[i].y); ctx.lineTo(pts[i+1].x,pts[i+1].y); } ctx.stroke();
    const wf=(t/4)%1, wi=wf*(N-1), wp=pts[Math.floor(wi)]||pts[0];
    const g=ctx.createRadialGradient(wp.x,wp.y,0,wp.x,wp.y,30);
    g.addColorStop(0,'rgba(127,255,176,.95)'); g.addColorStop(1,'rgba(127,255,176,0)');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(wp.x,wp.y,30,0,Math.PI*2); ctx.fill();
    for(let i=0;i<N;i++){ const k=KNOTS[i], osc=Math.sin(t*0.05+i*0.35);
      const r=1.6+(k.tension*3)+Math.max(0,osc)*1.6;
      ctx.globalAlpha=0.45+0.55*Math.abs(osc); ctx.fillStyle=k.color;
      ctx.beginPath(); ctx.arc(pts[i].x+osc*1.2,pts[i].y,r,0,Math.PI*2); ctx.fill(); ctx.globalAlpha=1; }
    const tip=pts[N-1]||pts[0]; ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(tip.x,tip.y,4,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,.5)'; ctx.beginPath(); ctx.arc(tip.x,tip.y,8,0,Math.PI*2); ctx.stroke();
    sub.textContent = KNOTS.length+' real knots · '+TIP.n_leaves+' leaves · root '+(TIP.root||'').slice(0,10)+'…';
  }

  window.addEventListener('message', e=>{
    const st = (e.data && e.data.state) || {};
    KNOTS = buildKnots(st.evolution || st);
    TIP = st.tip || TIP;
  });

  function loop(t){ draw(t/60); requestAnimationFrame(loop); }
  requestAnimationFrame(loop);
})();
