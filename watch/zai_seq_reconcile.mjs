// Billed-lane sequential cache re-hit reconcile. 2 sequential identical calls.
const key = process.env.ZAI_API_KEY;
const BASE = 'https://api.z.ai/api/paas/v4/chat/completions';
const F = 'BILLED_SEQ_CACHE_TEST_20260901. ' + ('seq-cache-check repeat prefix. '.repeat(400));
const body = { model: 'glm-5.3-flash', messages: [{ role: 'system', content: 'terse swarm probe' }, { role: 'user', content: F + ' reply READY' }], max_tokens: 16, temperature: 0 };
(async () => {
  for (let i = 1; i <= 2; i++) {
    const t = Date.now();
    const r = await fetch(BASE, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key }, body: JSON.stringify(body) });
    const j = await r.json();
    let cached = null, pTok = null;
    const u = j.usage;
    if (u) { pTok = u.prompt_tokens; if (u.prompt_tokens_details) cached = u.prompt_tokens_details.cached_tokens; }
    const errCode = j.error ? j.error.code : null;
    console.log(JSON.stringify({ call: i, http: r.status, ms: Date.now() - t, cached, promptTok: pTok, errCode }));
  }
})();
