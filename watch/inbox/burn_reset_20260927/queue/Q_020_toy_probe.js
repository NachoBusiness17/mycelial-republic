// Q-020 / FW-01 toy re-land probe: run candidate tapes against the HEAD toy.html walker
// physics (speed 95, 1.35 chase, 45% lunge, reach 38) and print the verb events.
'use strict';
const fs = require('fs');
const path = require('path');
const GAME = path.join(__dirname, '..', '..', '..', '..', 'dashboard', 'static', 'games', 'toy.html');
const html = fs.readFileSync(GAME, 'utf8');
const code = html.match(/<script>([\s\S]*)<\/script>/)[1];
const fakeCanvas = { width: 0, height: 0, style: {}, getContext: () => new Proxy({}, { get: (t, k) => k === 'canvas' ? fakeCanvas : (...a) => ({}), set: () => true }), addEventListener: () => {}, getBoundingClientRect: () => ({ left: 0, top: 0, width: 960, height: 600 }) };
const shimDocument = { getElementById: () => fakeCanvas, createElement: () => ({ width: 0, height: 0, getContext: () => ({}) }) };
function loadToy() {
  const w = { innerWidth: 960, innerHeight: 600, addEventListener: () => {} };
  new Function('window', 'document', 'requestAnimationFrame', code)(w, shimDocument, () => 0);
  return w.TOY;
}
function run(tape, label) {
  const T = loadToy();
  T.start(20260916);
  for (const row of tape) T.tape.push(row);
  T.pump(3600);
  const r = T.receipt();
  const ev = r.events.filter(e => ['telegraph', 'hit', 'hit_dodged', 'kill', 'end', 'swing'].includes(e.e));
  console.log(label, 'verdict=' + r.verdict, 'hits=' + r.hits_taken, 'illegal=' + r.hits_no_telegraph, 'dur=' + r.duration_s);
  console.log('  ', JSON.stringify(ev));
  return r;
}
const A = JSON.parse(process.argv[2]);
run(A, 'CANDIDATE_A');
