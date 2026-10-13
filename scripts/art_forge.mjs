#!/usr/bin/env node
// ART FORGE — dual-lane poster generation: Grok (x.ai) primary, CogView (z.ai) fallback.
// SSRF boundary: two literal https URLs only (api.x.ai, api.z.ai). Keys from .env, never echoed.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
let XAI = null, ZAI = null;
for (const line of readFileSync(join(ROOT, '.env'), 'utf8').split('\n')) {
  const s = line.trim();
  if (s.startsWith('XAI_API_KEY=')) XAI = s.split('=').slice(1).join('=').trim();
  if (s.startsWith('ZAI_API_KEY=') && !ZAI) ZAI = s.split('=').slice(1).join('=').trim();
}
const ARTDIR = join(ROOT, 'dashboard', 'static', 'art');
mkdirSync(ARTDIR, { recursive: true });

const POSTERS = {
  astra_dragon: 'Dark fantasy WPA federal-art-project propaganda poster, bold flat shapes, heroic low-angle composition: an enormous sleeping dragon coiled atop a hoard of unopened sealed scrolls and thick bound ledgers. Before it, a small empty wooden signing desk with a single quill planted upright like a sword. Limited palette: ember orange, antique gold, deep teal-black. Art deco border frame. Mood: the treasure already belongs to the viewer. No text, no letters, no watermark.',
  blind_gate: 'Dark fantasy art-deco propaganda poster: a colossal circular vault door at the end of a long dark corridor, its center a single glowing eye-shaped keyhole radiating soft gold light. A tiny lone figure holding a small lantern walks toward it, dwarfed by scale. A carved stopwatch above the door with hands at nearly midnight. Limited palette: deep teal-black, gold, single warm accent. Bold flat shapes, dramatic one-point perspective. Mood: you are already late. No text, no letters, no watermark.',
  cold_forge: 'Dark fantasy WPA propaganda poster: a cold dead blacksmith forge, frost-blue and dark, with exactly one living orange ember glowing in the ash. A heavy hammer rests on the anvil. Above hangs a small brass bell with a frayed rope cord, waiting. Limited palette: frost blue-black dominating, single ember orange glow. Mood: one word would relight everything. Bold flat poster shapes, deco border. No text, no letters, no watermark.',
};

async function grok(prompt) {
  const r = await fetch('https://api.x.ai/v1/images/generations', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${XAI}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'grok-2-image-1212', prompt, n: 1 }),
    signal: AbortSignal.timeout(180000),
  });
  if (!r.ok) throw new Error(`grok ${r.status}: ${(await r.text()).slice(0, 120)}`);
  const d = await r.json();
  const item = d.data?.[0] ?? {};
  if (item.b64_json) return Buffer.from(item.b64_json, 'base64');
  if (item.url) {
    const ir = await fetch(item.url, { signal: AbortSignal.timeout(120000) });
    if (!ir.ok) throw new Error(`grok dl ${ir.status}`);
    return Buffer.from(await ir.arrayBuffer());
  }
  throw new Error('grok: no image in response');
}

async function cogview(prompt) {
  const r = await fetch('https://api.z.ai/api/paas/v4/images/generations', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${ZAI}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'cogview-4-250304', prompt }),
    signal: AbortSignal.timeout(180000),
  });
  if (!r.ok) throw new Error(`cogview ${r.status}: ${(await r.text()).slice(0, 120)}`);
  const d = await r.json();
  const url = d.data?.[0]?.url;
  if (!url) throw new Error('cogview: no url');
  // download with vendor auth attached, retry once on expiry
  for (let attempt = 0; attempt < 2; attempt++) {
    const headers = { };
    if (attempt > 0) headers['Authorization'] = `Bearer ${ZAI}`;
    const ir = await fetch(url, { headers, signal: AbortSignal.timeout(120000) });
    if (ir.ok) return Buffer.from(await ir.arrayBuffer());
    if (attempt === 0 && (ir.status === 404 || ir.status === 403)) continue;
    throw new Error(`cogview dl ${ir.status}`);
  }
}

const results = {};
// custom commission mode: node art_forge.mjs <name> <prompt>
if (process.argv[2] && process.argv[3]) {
  const name = process.argv[2];
  let bytes = null, lane = 'none', errs = [];
  try { bytes = await grok(process.argv[3]); lane = 'grok'; }
  catch (e) { errs.push('grok: ' + String(e).slice(0, 90)); }
  if (!bytes) {
    try { bytes = await cogview(process.argv[3]); lane = 'cogview'; }
    catch (e) { errs.push('cogview: ' + String(e).slice(0, 90)); }
  }
  if (bytes) {
    writeFileSync(join(ARTDIR, name + '.png'), bytes);
    results[name] = `OK via ${lane}, ${bytes.length} bytes`;
    console.log(`${name}: OK via ${lane} (${bytes.length} bytes)`);
    writeFileSync(join(ARTDIR, 'forge_log.json'), JSON.stringify(results, null, 1));
    process.exit(0);
  }
  console.log(`${name}: FAILED | ${errs.join(' | ')}`);
  writeFileSync(join(ARTDIR, 'forge_log.json'), JSON.stringify(results, null, 1));
  process.exit(1);
}
for (const [name, prompt] of Object.entries(POSTERS)) {
  let lane = 'grok', bytes = null, err1 = null, err2 = null;
  try { bytes = await grok(prompt); }
  catch (e) { err1 = String(e).slice(0, 100); }
  if (!bytes) {
    lane = 'cogview';
    try { bytes = await cogview(prompt); }
    catch (e) { err2 = String(e).slice(0, 100); }
  }
  if (bytes) {
    writeFileSync(join(ARTDIR, name + '.png'), bytes);
    results[name] = `OK via ${lane}, ${bytes.length} bytes`;
    console.log(`${name}: OK via ${lane} (${bytes.length} bytes)`);
  } else {
    results[name] = `FAILED both lanes | grok: ${err1} | cogview: ${err2}`;
    console.log(`${name}: FAILED | grok: ${err1} | cogview: ${err2}`);
  }
}
writeFileSync(join(ARTDIR, 'forge_log.json'), JSON.stringify(results, null, 1));
console.log('forge complete');
