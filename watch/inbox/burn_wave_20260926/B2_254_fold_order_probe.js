// B2-254 probe: node-authoritative fold order for the three living files.
// Mirrors scripts/index_fold_host.mjs normInboxFile + seqOf + compareBySeqTs.
const fs = require('fs');
const lines = fs.readFileSync('watch/inbox/index_events.jsonl', 'utf8').split('\n').filter((l) => l.trim());
const targets = new Set(['burn_wave_20260926/QUEUE.md', 'LINKS.jsonl', 'phone_relay_log.jsonl']);
const norm = (f) => {
  let p = String(f || '').trim().replace(/\\/g, '/').replace(/^\/+/, '');
  p = p.replace(/^(board|app)\/inbox\//, '');
  while (p.startsWith('inbox/')) p = p.slice(6);
  p = p.replace(/^c:\/users\/foste\/documents\/projects\/local_sovereign_agent\/watch\/inbox\//i, '');
  while (p.startsWith('inbox/')) p = p.slice(6);
  return p;
};
function seqOf(s) {
  if (typeof s === 'number' && Number.isInteger(s)) return BigInt(s);
  if (typeof s === 'string' && /^\d+$/.test(s)) return BigInt(s);
  return null;
}
const rows = [];
lines.forEach((line, i) => {
  let ev;
  try { ev = JSON.parse(line); } catch { return; }
  const p = norm(ev.file);
  if (!targets.has(p)) return;
  rows.push({
    line: i + 1, seqRaw: String(ev.seq), seqParsed: seqOf(ev.seq), ts: ev.ts,
    op: ev.op, p, writer: ev.writer, living: !!ev.living, size: ev.size, seal: ev.seal,
  });
});
rows.sort((a, b) => {
  const sa = a.seqParsed, sb = b.seqParsed;
  if (sa !== null && sb !== null && sa !== sb) return sa < sb ? -1 : 1;
  if (a.ts < b.ts) return -1;
  if (a.ts > b.ts) return 1;
  return 0;
});
for (const r of rows) {
  console.log(
    r.line, r.seqRaw, r.seqParsed === null ? 'NULL' : String(r.seqParsed),
    r.ts, r.op, r.p, r.writer, 'living=' + r.living, 'size=' + r.size, 'seal=' + r.seal
  );
}
