// z.ai swarm-concurrency + cache probe. Never prints key values.
// Usage: node zai_probe.mjs <KEY_ENV_NAME> <model>
// Reads the key from process env, 10 parallel identical-prefix tiny calls.
import { performance } from 'node:perf_hooks';

const keyName = process.argv[2];
const model = process.argv[3] || 'glm-5.3-flash';
const key = process.env[keyName];
if (!key) { console.error('NO_KEY', keyName); process.exit(1); }

const BASE = 'https://api.z.ai/api/paas/v4/chat/completions';

// Frozen long prefix (~2K tokens) repeated identically across all 10 calls.
const FROZEN_PREFIX = 'SWARM_DOCTRINE_FROZEN_PREFIX_20260901. ' +
  'Repetition builds context cache. Repetition builds context cache. ' +
  ('The quick brown fox jumps over the lazy dog. cache-me-now-2026. '.repeat(400)) +
  'END_OF_FROZEN_PREFIX.';

const body = {
  model,
  messages: [
    { role: 'system', content: 'You are a terse swarm probe. Reply in one short sentence.' },
    { role: 'user', content: FROZEN_PREFIX + ' Please reply with the single word: READY.' }
  ],
  max_tokens: 64,
  temperature: 0
};

async function one(i) {
  const t0 = performance.now();
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
  let j = null;
  try { j = await res.json(); } catch { j = { raw: '(non-json)' }; }
  return { i, http: res.status, ms, j };
}

const results = await Promise.all(Array.from({ length: 10 }, (_, i) => one(i)));
// Summary only; never dump the whole body (avoid leaking key/prefix) — we know prefix, just print numbers.
const rows = results.map(r => {
  let cached = '-', promptTok = '-', out = '-';
  const u = r.j && r.j.usage;
  if (u) {
    promptTok = u.prompt_tokens;
    out = u.completion_tokens;
    if (u.prompt_tokens_details && u.prompt_tokens_details.cached_tokens != null) cached = u.prompt_tokens_details.cached_tokens;
  }
  return { i: r.i, http: r.http, ms: r.ms, cacheTok: cached, promptTok, outTok: out };
});
console.log(JSON.stringify({ keyName, model, base: BASE, n: results.length, rows }, null, 1));
