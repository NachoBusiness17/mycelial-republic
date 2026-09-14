#!/usr/bin/env node
// CONC PROBE PAST50 — falsify whether the vendor-documented 50-in-flight row is
// key-side policy or provider capacity. Third party claims c=512 serving.
// Waves: 50 -> 60 -> 70 -> 80 concurrent, max_tokens 8, 10s pause between waves.
// Total requests = 260 (cap). Single run, no loops. Key never echoed.
// SSRF boundary: single literal https URL to api.z.ai — no dynamic hosts.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
let KEY = null;
for (const line of readFileSync(join(ROOT, '.env'), 'utf8').split('\n')) {
  const s = line.trim();
  if (s.startsWith('ZAI_API_KEY_Lite=')) KEY = s.split('=').slice(1).join('=').trim();
}
if (!KEY) { console.log('RESULT: no ZAI_API_KEY_Lite in .env — dead end'); process.exit(1); }

const MODEL = 'glm-5.3-flash';

async function call(i) {
  const t0 = Date.now();
  try {
    const r = await fetch('https://api.z.ai/api/paas/v4/chat/completions', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: 'user', content: 'say ok' }],
        thinking: { type: 'enabled' },
        reasoning_effort: 'low',
        max_tokens: 8,
        temperature: 0.0,
      }),
      signal: AbortSignal.timeout(60000),
    });
    const dt = (Date.now() - t0) / 1000;
    if (!r.ok) {
      const d = await r.json().catch(() => ({}));
      const biz = String(d?.error?.code ?? '');
      return { ok: false, dt, status: r.status, biz };
    }
    return { ok: true, dt };
  } catch (e) {
    return { ok: false, dt: (Date.now() - t0) / 1000, status: 0, biz: String(e?.cause?.code ?? e?.name ?? 'net-err') };
  }
}

function p50(arr) {
  if (!arr.length) return null;
  const s = [...arr].sort((a, b) => a - b);
  return s[Math.floor((s.length - 1) / 2)];
}

async function wave(n) {
  const t0 = Date.now();
  const results = await Promise.all(Array.from({ length: n }, (_, i) => call(i)));
  const oks = results.filter(r => r.ok);
  const fails = results.filter(r => !r.ok);
  const tally = { c1302: 0, c429: 0, other: {} };
  for (const f of fails) {
    if (String(f.biz).includes('1302')) tally.c1302++;
    else if (f.status === 429 || String(f.biz).includes('429')) tally.c429++;
    else {
      const k = `${f.status}/${f.biz || 'net'}`;
      tally.other[k] = (tally.other[k] || 0) + 1;
    }
  }
  return {
    launched: n,
    http200: oks.length,
    err1302: tally.c1302,
    err429: tally.c429,
    other: tally.other,
    p50_latency_s: p50(oks.map(r => r.dt)),
    wall_s: (Date.now() - t0) / 1000,
  };
}

const WAVES = [50, 60, 70, 80];
const rows = [];
let aborted = false;
for (const n of WAVES) {
  console.log(`=== WAVE c=${n} ===`);
  const r = await wave(n);
  rows.push({ c: n, ...r });
  console.log(JSON.stringify(r));
  // Two-strike / dead-lane bail: first wave total failure, or auth rejection, stops the run.
  const authDead = Object.keys(r.other).some(k => k.startsWith('401/') || k.startsWith('403/'));
  if ((n === WAVES[0] && r.http200 === 0) || authDead) {
    console.log('STOP: lane dead or auth rejected — not burning the remaining waves.');
    aborted = true;
    break;
  }
  if (n !== WAVES[WAVES.length - 1]) await new Promise(res => setTimeout(res, 10000));
}

// Interpretation
const past = rows.filter(r => r.c > 50);
const base = rows.find(r => r.c === 50);
let verdict;
if (!base || base.http200 === 0) {
  verdict = 'INCONCLUSIVE — baseline wave c=50 failed entirely; lane/auth problem, no signal.';
} else {
  const baseRate = base.http200 / base.launched;
  const pastOk = past.filter(r => r.http200 / r.launched >= baseRate * 0.8);
  const dominated1302 = past.length > 0 && past.every(r => r.err1302 / r.launched > 0.5);
  const dominated429 = past.length > 0 && past.every(r => r.err429 / r.launched > 0.5);
  if (pastOk.length === past.length && past.length > 0) {
    verdict = 'PAST-50 SUCCEEDS at near-baseline rates — the 50-row is KEY-SIDE POLICY (per-key concurrency cap), provider capacity is higher. Third-party c=512 claim is PLAUSIBLE; our burst ceiling is self-imposed by key row.';
  } else if (dominated1302) {
    verdict = 'PAST-50 FAILS dominated by error 1302 — concurrency row ENFORCED PER KEY. 50 is a hard per-key limit; provider capacity claim neither confirmed nor denied from this key.';
  } else if (dominated429) {
    verdict = 'PAST-50 FAILS dominated by HTTP 429 — QUOTA-SIDE rate limit, not a concurrency-row wall.';
  } else {
    verdict = 'MIXED degradation past 50 — partial failures (see per-wave tallies); ceiling sits near but above 50, likely key-row-adjacent throttle with queuing.';
  }
}
console.log('=== VERDICT ===');
console.log(verdict);
console.log('=== ROWS_JSON ===');
console.log(JSON.stringify(rows.map(r => ({ c: r.c, launched: r.launched, http200: r.http200, err1302: r.err1302, err429: r.err429, other: r.other, p50_latency_s: r.p50_latency_s }))));
