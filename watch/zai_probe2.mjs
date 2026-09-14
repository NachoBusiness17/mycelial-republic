// z.ai swarm-concurrency + cache probe v2 — fault tolerant per-call.
// Usage: node zai_probe2.mjs <KEY_ENV_NAME> <model> [parallel] [label]
import { performance } from 'node:perf_hooks';

const keyName = process.argv[2];
const model = process.argv[3] || 'glm-5.3-flash';
const PAR = parseInt(process.argv[4] || '10', 10);
const label = process.argv[5] || 'batch';
const key = process.env[keyName];
if (!key) { console.error('NO_KEY', keyName); process.exit(1); }

const BASE = 'https://api.z.ai/api/paas/v4/chat/completions';

function FROZEN_PREFIX() {
  return 'SWARM_DOCTRINE_FROZEN_PREFIX_20260901_V2. ' +
    ('cache-me-now-2026 repetition builds the context cache. '.repeat(380)) +
    'END_OF_FROZEN_PREFIX.';
}

async function one(i) {
  const body = {
    model,
    messages: [
      { role: 'system', content: 'You are a terse swarm probe. One short sentence.' },
      { role: 'user', content: FROZEN_PREFIX() + ' Reply with exactly the word READY.' }
    ],
    max_tokens: 32,
    temperature: 0
  };
  const t0 = performance.now();
  try {
    const res = await fetch(BASE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept-Language': 'en-US,en',
        'Authorization': 'Bearer ' + key
      },
      body: JSON.stringify(body)
    });
    const ms = Math.round(performance.now() - t0);
    let j = null, raw = '';
    try { j = await res.json(); } catch { raw = '(non-json)'; }
    let cached = null, pTok = null, oTok = null;
    const u = j && j.usage;
    if (u) {
      pTok = u.prompt_tokens; oTok = u.completion_tokens;
      if (u.prompt_tokens_details && u.prompt_tokens_details.cached_tokens != null) cached = u.prompt_tokens_details.cached_tokens;
    }
    // Only emit safely-named error, never body content.
    const errCode = (j && j.error && j.error.code) ? j.error.code : null;
    const errType = (j && j.error && j.error.type) ? j.error.type : null;
    return { i, ok: true, http: res.status, ms, cacheTok: cached, promptTok: pTok, outTok: oTok, errCode, errType };
  } catch (e) {
    return { i, ok: false, err: String(e && e.message || e).slice(0, 120), ms: Math.round(performance.now() - t0) };
  }
}

const results = await Promise.all(Array.from({ length: PAR }, (_, i) => one(i)));
const ok = results.filter(r => r.ok);
const ms = ok.map(r => r.ms);
const lat = ms.length ? { min: Math.min(...ms), max: Math.max(...ms), med: ms.sort((a, b) => a - b)[Math.floor(ms.length / 2)] } : null;
let cacheStats = null;
const withCache = ok.filter(r => r.cacheTok != null);
if (withCache.length) {
  const hits = withCache.map(r => r.cacheTok);
  const tots = withCache.map(r => r.promptTok);
  cacheStats = { hitsMin: Math.min(...hits), hitsMax: Math.max(...hits), totalMin: Math.min(...tots), totalMax: Math.max(...tots) };
}
const errors = results.filter(r => !r.ok).map(r => ({ i: r.i, err: r.err }));
console.log(JSON.stringify({ keyName, model, label, n: PAR, okCount: ok.length, failCount: results.length - ok.length, latency: lat, cacheStats, errors: errors.slice(0, 5) }, null, 1));
