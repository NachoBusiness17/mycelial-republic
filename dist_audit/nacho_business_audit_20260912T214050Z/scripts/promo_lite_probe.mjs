import fs from 'fs';

let KEY = '';
for (const line of fs.readFileSync('.env', 'utf8').split('\n')) {
  const s = line.trim();
  if (s.startsWith('ZAI_API_KEY_Lite=')) KEY = s.split('=').slice(1).join('=').trim();
}
if (!KEY) { console.log('RESULT: no ZAI_API_KEY_Lite in .env — dead end'); process.exit(1); }

const t0 = Date.now();
const res = await fetch('https://api.z.ai/api/coding/paas/v4/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY },
  body: JSON.stringify({
    model: 'glm-5.3-flash',
    messages: [{ role: 'user', content: 'reply with the single word: alive' }],
    max_tokens: 1536,
    thinking: { type: 'low' }
  })
});
const ms = Date.now() - t0;
console.log('HTTP', res.status, '| ms:', ms);
const j = await res.json().catch(() => null);
if (j && j.choices && j.choices[0]) {
  const c = j.choices[0].message;
  console.log('alive:', JSON.stringify((c.content || '').trim().slice(0, 40)));
  console.log('usage:', JSON.stringify(j.usage || {}));
  console.log('model:', j.model || 'unreported');
} else {
  console.log('body-class:', JSON.stringify(j).slice(0, 200));
}
