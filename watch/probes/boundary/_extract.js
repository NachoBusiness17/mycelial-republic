const fs = require('fs');
const files = [
  '/root/.openclaw/agents/worker/sessions/0d37679f-a697-4d07-b28c-21363a82b414.jsonl',
  '/root/.openclaw/agents/worker/sessions/61861a2d-eb69-4fd5-9689-e02712c09e69.jsonl',
  '/root/.openclaw/agents/worker/sessions/94f1efd5-c43d-4f00-bc2e-5252266bce30.jsonl',
  '/root/.openclaw/agents/worker/sessions/a226f760-f0ea-4e4d-9300-1726643ccd3c.jsonl'
];
for (const f of files) {
  console.log('========== ' + f.split('/').pop() + ' ==========');
  const lines = fs.readFileSync(f, 'utf8').trim().split('\n');
  const out = [];
  for (const l of lines) {
    try {
      const o = JSON.parse(l);
      if (o && o.type === 'message' && o.message && o.message.role === 'assistant') {
        out.push(o.message.content);
      }
    } catch (e) {}
  }
  const last = out[out.length - 1];
  console.log(typeof last === 'string' ? last : JSON.stringify(last));
}
