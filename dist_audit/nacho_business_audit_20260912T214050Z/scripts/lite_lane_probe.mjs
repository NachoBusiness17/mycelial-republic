#!/usr/bin/env node
// LITE LANE PROBE — aliveness + concurrency ramp on glm-5.3-flash.
// Operator order: use the lite key for dumb-model concurrent calls, fun + data,
// without burning through. Total burn < ~5K tokens. Key never echoed.
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

const URL_ = 'https://api.z.ai/api/paas/v4/chat/completions';
const MODEL = 'glm-5.3-flash';

async function call(i) {
  const t0 = Date.now();
  try {
    const r = await fetch('https://api.z.ai/api/paas/v4/chat/completions', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: 'user', content: `Reply with exactly: LITE-${i}` }],
        thinking: { type: 'enabled' },
        reasoning_effort: 'low',
        max_tokens: 32,
        temperature: 0.0,
      }),
      signal: AbortSignal.timeout(60000),
    });
    const dt = (Date.now() - t0) / 1000;
    if (!r.ok) {
      const d = await r.json().catch(() => ({}));
      return { ok: false, dt, code: r.status, err: `${d?.error?.code ?? ''} ${String(d?.error?.message ?? '').slice(0, 90)}` };
    }
    const d = await r.json();
    return { ok: true, dt, model: d.model, content: (d.choices?.[0]?.message?.content || '').slice(0, 24), tok: d.usage?.total_tokens ?? 0 };
  } catch (e) {
    return { ok: false, dt: (Date.now() - t0) / 1000, code: 0, err: String(e).slice(0, 90) };
  }
}

async function ramp(n) {
  const results = await Promise.all(Array.from({ length: n }, (_, i) => call(i)));
  const oks = results.filter(r => r.ok);
  const fails = results.filter(r => !r.ok);
  const dts = oks.map(r => r.dt).sort((a, b) => a - b);
  const codes = {};
  for (const f of fails) codes[f.code] = (codes[f.code] || 0) + 1;
  return {
    sent: n, ok: oks.length,
    lat_min: dts[0] ?? null, lat_med: dts[Math.floor(dts.length / 2)] ?? null, lat_max: dts[dts.length - 1] ?? null,
    fail_codes: codes,
    tok: oks.reduce((s, r) => s + (r.tok || 0), 0),
    sample: oks[0]?.content ?? (fails[0]?.err ?? ''),
    model: oks[0]?.model ?? '',
  };
}

console.log('=== ALIVENESS (1 call) ===');
const a = await ramp(1);
console.log(JSON.stringify(a));
if (a.ok === 0) { console.log('RESULT: LANE DEAD —', a.sample); process.exit(0); }

let total = a.tok;
for (const n of [5, 10, 20, 50]) {
  console.log(`=== RAMP n=${n} ===`);
  const r = await ramp(n);
  total += r.tok;
  console.log(JSON.stringify(r));
  await new Promise(res => setTimeout(res, 1000));
}
console.log(`=== TOTAL BURN: ${total} tokens ===`);
