const fs = require('fs');
const html = fs.readFileSync('dashboard/static/games/mud.html', 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/);
const src = m[1];
const lines = src.split('\n');
let depth = 0, inStr = null;
const zeroHits = [];
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  for (let j = 0; j < line.length; j++) {
    const ch = line[j];
    if (inStr) { if (ch === inStr) inStr = null; continue; }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = ch; continue; }
    if (ch === '/' && line[j + 1] === '/') break;
    if (ch === '{') depth++;
    if (ch === '}') depth--;
  }
  if (depth === 0 && i > 1) zeroHits.push(i + 1);
  if (depth < 0) { console.log('NEGATIVE at line', i + 1, ':', line.slice(0, 70)); break; }
}
if (zeroHits.length) console.log('IIFE closed early at lines:', zeroHits.join(', '));
else console.log('depth never returned to 0 — final:', depth);
if (zeroHits.length === 0) {
  // report depth at every function declaration to find the orphan
  let d2 = 0;
  const decls = [];
  let s = null;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (let j = 0; j < line.length; j++) {
      const ch = line[j];
      if (inStr) { if (ch === inStr) inStr = null; continue; }
      if (ch === '"' || ch === "'" || ch === '`') { inStr = ch; continue; }
      if (ch === '/' && line[j + 1] === '/') break;
      if (ch === '{') d2++;
      if (ch === '}') d2--;
    }
    if (/^function |^const |^let |^window\.MUD/.test(line)) decls.push({ n: i + 1, d: d2, t: line.slice(0, 60) });
  }
  console.log('declarations with depth !== 1:');
  for (const dcl of decls) if (dcl.d !== 1) console.log('  d' + dcl.d, 'line', dcl.n, dcl.t.slice(0, 60));
}
