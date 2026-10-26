// B2-279 attribution probe v2: replay the OLD (B2-40) comparator and the NEW
// (B2-279 total-order) fold over the SAME production event bytes, WITH the
// real fold's path normalization and outside/unresolved drops mirrored, and
// name every active item whose winning register changed. Read-only.
// Run: node B2_279_order_attribution.js 2>/dev/null > B2_279_order_attribution_results.json
import { readFileSync } from 'fs';

const INBOX_DIR = 'C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox';
const lines = readFileSync(`${INBOX_DIR}/index_events.jsonl`, 'utf8').split('\n').filter((l) => l.trim() !== '');

// ---- mirror readEvents normalization (scripts/index_fold_host.mjs) --------
const INBOX_ROOTS = [...new Set([
  INBOX_DIR,
  'C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox',
].map((r) => String(r).replace(/\\/g, '/').replace(/\/+$/, '')))];

const normInboxFile = (f) => {
  let p = String(f || '').trim().replace(/\\/g, '/').replace(/^\/+/, '');
  p = p.replace(/^(board|app)\/inbox\//, '');
  while (p.startsWith('inbox/')) p = p.slice(6);
  for (const root of INBOX_ROOTS) {
    if (p.length > root.length && p.slice(0, root.length + 1).toLowerCase() === root.toLowerCase() + '/') {
      p = p.slice(root.length + 1);
      break;
    }
  }
  while (p.startsWith('inbox/')) p = p.slice(6);
  return p;
};
const OUTSIDE_RE = /^(mag|memory|queue|scripts|dashboard|docs|site|tests|models|backend|configs?|deploy|state|watch|research|corpus|dist_audit|attic|handoff|tools|bridge|harness|router|experiments|window|agents)\//;
const isUnresolved = (p) => p === '' || /^[A-Za-z]:\//.test(p) || /(^|\/)\.\.(\/|$)/.test(p);

const events = [];
lines.forEach((line) => {
  try {
    const ev = JSON.parse(line);
    if (typeof ev.file === 'string') ev.file = normInboxFile(ev.file);
    ev._outside = typeof ev.file === 'string' && OUTSIDE_RE.test(ev.file);
    ev._unresolved = typeof ev.file === 'string' && isUnresolved(ev.file) && !ev._outside;
    if (ev._outside || ev._unresolved) return; // the fold drops both classes
    events.push(ev);
  } catch { /* tolerant reader */ }
});

const MAX_SAFE = BigInt(Number.MAX_SAFE_INTEGER);

function seqOfOld(ev) {
  const s = ev.seq;
  if (typeof s === 'number' && Number.isInteger(s)) return BigInt(s);
  if (typeof s === 'string' && /^\d+$/.test(s)) return BigInt(s);
  return null;
}
function compareOld(a, b) {
  const sa = seqOfOld(a);
  const sb = seqOfOld(b);
  if (sa !== null && sb !== null && sa !== sb) return sa < sb ? -1 : 1;
  if (a.ts < b.ts) return -1;
  if (a.ts > b.ts) return 1;
  return 0;
}
function keyNew(ev) {
  const s = ev.seq;
  if (typeof s === 'number') {
    if (Number.isSafeInteger(s)) return { tier: 2, seq: BigInt(s) };
    if (Number.isInteger(s)) return { tier: 1, seq: BigInt(s) };
    return { tier: 0, seq: null };
  }
  if (typeof s === 'string' && /^\d+$/.test(s)) return { tier: 2, seq: BigInt(s) };
  return { tier: 0, seq: null };
}
function compareNew(a, b) {
  const ka = keyNew(a);
  const kb = keyNew(b);
  if (ka.tier !== kb.tier) return ka.tier < kb.tier ? -1 : 1;
  if (ka.seq !== null && kb.seq !== null && ka.seq !== kb.seq) return ka.seq < kb.seq ? -1 : 1;
  const ta = a.ts || a.register_ts || '';
  const tb = b.ts || b.register_ts || '';
  if (ta < tb) return -1;
  if (ta > tb) return 1;
  const pa = a.path || a.file || '';
  const pb = b.path || b.file || '';
  if (pa < pb) return -1;
  if (pa > pb) return 1;
  return 0;
}

function foldWith(cmp) {
  const active = new Map();
  for (const ev of [...events].sort(cmp)) {
    if (ev.op === 'register' && ev.file) active.set(ev.file, ev);
    else if (ev.op === 'invalidate' && ev.file) active.delete(ev.file);
  }
  return active;
}

const oldFold = foldWith(compareOld);
const newFold = foldWith(compareNew);

const paths = new Set([...oldFold.keys(), ...newFold.keys()]);
const changed = [];
for (const p of [...paths].sort()) {
  const o = oldFold.get(p);
  const n = newFold.get(p);
  const sig = (e) => (e ? JSON.stringify([String(e.seq ?? null), e.ts, e.sha256 ?? null, e.living === true, e.seal ?? null]) : null);
  if (sig(o) !== sig(n)) {
    changed.push({
      path: p,
      old: o ? { seq: String(o.seq ?? null), ts: o.ts, sha256: o.sha256, living: o.living === true, seal: o.seal ?? null } : null,
      new: n ? { seq: String(n.seq ?? null), ts: n.ts, sha256: n.sha256, living: n.living === true, seal: n.seal ?? null } : null,
      old_seq_class: o ? (keyNew(o).tier === 1 ? 'inexact-band' : keyNew(o).tier === 2 ? 'exact' : 'null-seq') : null,
      new_seq_class: n ? (keyNew(n).tier === 1 ? 'inexact-band' : keyNew(n).tier === 2 ? 'exact' : 'null-seq') : null,
    });
  }
}
const out = {
  events: events.length,
  active_items: newFold.size,
  changed_active_items: changed.length,
  changed,
};
console.log(JSON.stringify(out, null, 2));
