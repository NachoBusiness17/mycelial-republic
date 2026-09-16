'use strict';
const fs = require('fs');
const html = fs.readFileSync('C:/Users/foste/Documents/projects/local_sovereign_agent/dashboard/static/games/frontier_souls.html', 'utf8');
const code = html.match(/<script>([\s\S]*)<\/script>/)[1];
function makeCtx(){ return new Proxy({},{get:(t,k)=> k==='canvas'?fakeCanvas:(...a)=>makeCtx(),set:()=>true}); }
const fakeCanvas = {width:0,height:0,style:{},getContext:()=>makeCtx(),addEventListener:()=>{},getBoundingClientRect:()=>({left:0,top:0,width:960,height:600})};
const w = {innerWidth:960,innerHeight:600,addEventListener:()=>{}};
const d = {getElementById:()=>fakeCanvas, createElement:()=>({width:0,height:0,getContext:()=>makeCtx()})};
const fn = new Function('window','document','localStorage','location','fetch','setInterval','requestAnimationFrame','performance','URLSearchParams', code);
fn(w,d,{getItem:()=>null,setItem:()=>{}},{search:''},()=>Promise.resolve({json:()=>Promise.resolve({ok:true})}),()=>0,()=>0,performance,URLSearchParams);
const M = w.FS;
const P = () => M.player;
M.startRun(0);
P().hp = 100; P().iframes = 2; P().maxHp = 100;
const sc = M.foes.find(f => f.type === 'scorpion');
if (sc) sc.hp = 0;
M.ambient.length = 0;
M.forceRattleKill = true;
const sn = M.spawnFoe('snake', P().x + 30, P().y);
for (let i = 0; i < 480; i++) {
  M.pump(1);
  if (i % 40 === 0) console.log('f' + i, 'state', sn.state, 'd', Math.round(Math.hypot(sn.x - P().x, sn.y - P().y)), 'cd', sn.cd && sn.cd.toFixed(2), 'st', sn.st !== undefined ? sn.st.toFixed(2) : '-', 'flee', sn.flee !== undefined ? sn.flee.toFixed(2) : '-', 'iframes', P().iframes.toFixed(2), 'hp', Math.round(P().hp), 'G', M.G.state);
  if (M.G.state === 'dead') { console.log('DEAD at frame', i); break; }
}
