#!/usr/bin/env node
// LITE LANE SUSTAINED-FLIGHT PROBE — hold N workers in continuous flight for T
// seconds; measure throughput (req/s), error rate, token burn per minute.
// This is the legions duty-cycle test. Guards: hard cap on completions, wall
// clock limit, key never echoed. SSRF: single literal https URL to api.z.ai.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
let KEY = null;
for (const line of readFileSync(join(ROOT, '.env'), 'utf8').split('\n')) {
  const s = line.trim();
  if (s.startsWith('ZAI_API_KEY_Lite=')) KEY = s.split('=').slice(1).join('=').trim();
}
if (!KEY) { console.log('RESULT: no ZAI_API_KEY_Lite in .env'); process.exit(1); }

const MODEL = 'glm-5.3-flash';
const CONCURRENCY = parseInt(process.env.PROBE_N || '50', 10);
const SECONDS = parseInt(process.env.PROBE_T || '45', 10);
const MAX_COMPLETIONS = 6000; // hard token-burn guard: ~6000 * ~30 tok = ~180K tokens max

let done = 0, failed = 0, tokens = 0, launched = 0;
const lat = [];
const codes = {};
const t0 = Date.now();
const deadline = t0 + SECONDS * 1000;
let stop = false;

async function call(i) {
  const s = Date.now();
  try {
    const r = await fetch('https://api.z.ai/api/paas/v4/chat/completions', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: 'user', content: `Reply with exactly: FLIGHT-${i}` }],
        thinking: { type: 'enabled' },
        reasoning_effort: 'low',
        max_tokens: 24,
        temperature: 0.0,
      }),
      signal: AbortSignal.timeout(60000),
    });
    const dt = (Date.now() - s) / 1000;
    if (!r.ok) {
      const d = await r.json().catch(() => ({}));
      const c = r.status;
      codes[c] = (codes[c] || 0) + 1;
      return false;
    }
    const d = await r.json();
    done++; tokens += d.usage?.total_tokens ?? 0; lat.push((Date.now() - s) / 1000);
    return true;
  } catch (e) {
    failed++; codes[0] = (codes[0] || 0) + 1;
    return false;
  }
}

async function worker(wid) {
  let i = wid;
  while (!stop && done < MAX_COMPLETIONS && Date.now() < deadline) {
    launched++;
    await call(i);
    i += CONCURRENCY;
  }
}

await Promise.all(Array.from({ length: CONCURRENCY }, (_, w) => worker(w)));
const elapsed = (Date.now() - t0) / 1000;
lat.sort((a, b) => a - b);
const med = lat[Math.floor(lat.length / 2)] ?? null;
console.log(JSON.stringify({
  test: 'sustained-flight', concurrency: CONCURRENCY, wall_seconds: +(elapsed).toFixed(1),
  completed: done, failed, launched,
  throughput_rps: +(done / elapsed).toFixed(2),
  tokens: tokens, tokens_per_minute: Math.round(tokens / (elapsed / 60)),
  lat_med_s: med, lat_max_s: lat[lat.length - 1] ?? null,
  p90_s: lat[Math.floor(lat.length * 0.9)] ?? null,
  fail_codes: codes,
}, null, 1));
