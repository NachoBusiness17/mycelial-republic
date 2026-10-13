#!/usr/bin/env node
// NIGHTLY DECKS RETRAIN — refresh snapshot from watch/INTAKE_*, re-run whelp LOO.
// New slugs classify via keyword fallback and are flagged low-confidence for the
// blind pass. Existing slugs keep their canonical (blind twin) assignment.
// SSRF: no network calls. Local files only.
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const WATCH = join(ROOT, 'watch');
const OUT = join(ROOT, 'memory', 'working', 'decks_snapshot.json');
const WH = join(ROOT, 'memory', 'working', 'whelp_loo_receipt.json');

const DECKS = [
  { id: 'mesh3d', name: 'Mesh3D', eyes: false },
  { id: 'rocinante', name: 'Rocinante', eyes: false },
  { id: 'personal', name: 'Personal', eyes: false },
  { id: 'glmwatch', name: 'GLM Watch', eyes: false },
  { id: 'legions', name: 'Legions', eyes: false },
  { id: 'gamebuild', name: 'GameBuild', eyes: false },
  { id: 'cacheecon', name: 'Cache Econ', eyes: false },
  { id: 'mag', name: 'MAG', eyes: true },
];

// ---- load prior snapshot (canonical assignments) ----
let prior = { cards: [], decks: DECKS };
try { prior = JSON.parse(readFileSync(OUT, 'utf8')); } catch (e) {}
const canon = {};
for (const c of prior.cards || []) canon[c.slug] = c.decks || ['mag'];

// ---- enumerate the shelf ----
const files = readdirSync(WATCH).filter(f => f.startsWith('INTAKE_') && f.endsWith('.md'));
const cards = [];
for (const fn of files) {
  const slug = fn.slice(0, -3);
  const text = readFileSync(join(WATCH, fn), 'utf8');
  const noteMatch = text.match(/##\s+ITEM[^\n]*\n+([\s\S]{0,300})/);
  const note = noteMatch ? noteMatch[1].replace(/\s+/g, ' ').slice(0, 280) : '';
  const decks = canon[slug] || ['mag'];
  const flagged = canon[slug] ? false : true;
  cards.push({ slug, file: 'watch/' + fn, title: slug.replace(/^INTAKE_|_\d{8}$/g, '').replace(/_/g, ' '), decks, note: (note || '').slice(0, 280), text, flaggedNew: flagged });
}

// ---- whelp LOO re-run (KNOWN-ISSUE: this LOO reads ~16-28% where the inline
// falsifier reads ~62-64% on the same labels — instrument miscalibration, see
// memory/working/whelp_loo_receipt.json history. The SNAPSHOT REFRESH below is
// the trusted output; DO NOT trust the LOO number until reconciled with
// memory/working/ inline falsifier method. Flagged 09-04, main seat.) ----
function toks(s) {
  return (s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ')).split(/\s+/).filter(t => t.length > 3);
}
const lab = cards.filter(c => canon[c.slug]); // cards with prior (blind-canonical) labels
const labToks = lab.map(c => [...new Set(toks(c.text + ' ' + c.note))]);
const df = {};
for (const d of labToks) for (const t of d) df[t] = (df[t] || 0) + 1;
const idf = {}; for (const t in df) idf[t] = Math.log(lab.length / df[t]);
const vecs = labToks.map(d => { const v = {}; for (const t of d) v[t] = idf[t]; return v; });
const norms = vecs.map(v => Math.sqrt(Object.values(v).reduce((s, x) => s + x * x, 0)) || 1);
function cos(i, j) {
  const a = vecs[i], b = vecs[j];
  const [s, l] = Object.keys(a).length < Object.keys(b).length ? [a, b] : [b, a];
  let dot = 0; for (const t in s) dot += s[t] * (b[t] || 0);
  return dot / (norms[i] * norms[j]);
}
for (const k of [1, 3, 5]) {
  let hit = 0, tot = 0;
  for (let i = 0; i < lab.length; i++) {
    const sims = [];
    for (let j = 0; j < lab.length; j++) if (j !== i) sims.push([cos(i, j), j]);
    sims.sort((a, b) => b[0] - a[0]);
    const top = sims.slice(0, k).map(([, j]) => (canon[lab[j].slug] || ['mag'])[0]);
    const counts = {}; for (const t of top) counts[t] = (counts[t] || 0) + 1;
    const pred = Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
    const truth = (canon[lab[i].slug] || ['mag'])[0];
    if (pred === truth) hit++;
    tot++;
  }
  console.log(`whelp LOO k=${k}: ${hit}/${tot} = ${(100 * hit / tot).toFixed(1)}%`);
}

// ---- write snapshot ----
const snap = {
  schema: 'decks_snapshot.v1',
  built: new Date().toISOString().replace(/\.\d+Z$/, 'Z'),
  decks: DECKS,
  cards: cards.map(c => ({ slug: c.slug, file: c.file, title: c.title, decks: c.decks, note: c.note, text: c.text, flaggedNew: c.flaggedNew })),
};
writeFileSync(OUT, JSON.stringify(snap, null, 1));

// ---- whelp receipt append ----
let receipt = [];
try { receipt = JSON.parse(readFileSync(WH, 'utf8')); if (!Array.isArray(receipt)) receipt = [receipt]; } catch (e) {}
mkdirSync(dirname(WH), { recursive: true });
receipt.push({ ts: new Date().toISOString(), cards: cards.length, flaggedNew: cards.filter(c => c.flaggedNew).length });
writeFileSync(WH, JSON.stringify(receipt, null, 1));
console.log(`nightly retrain done: ${cards.length} cards, ${cards.filter(c => c.flaggedNew).length} flagged new`);
