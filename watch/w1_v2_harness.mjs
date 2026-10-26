// W1 V2 — DRAFT-L0 + self-built L2 (MIXED-CORPUS) vs naive A0, DeepSeek, waves of 5, 30/arm
import https from 'https';
import fs from 'fs';

const KEY = process.env.DEEPSEEK_API_KEY;
const API = 'api.deepseek.com';
const MODEL = 'deepseek-chat';
const MAX_TOKENS = 300;
const WAVE = 5;
const N = 30;
const RUN = new Date().toISOString();

// ---- static prefix assets ----
function fileBody(p) {
  return fs.readFileSync(p, 'utf8');
}
const L0 = fileBody('/board/corpus/L0_universal_contract.DRAFT.md');
const L2 = fileBody('/board/corpus/L2_riichi.md');
const PREFIX = `${L0}\n\n${L2}\n\n`; // byte-stable static prefix (A2 arm)

// ---- task suffix set (riichi tutor questions, deterministic) ----
const QS = [
  "If I hold 5m 6m 7m plus a pung of East, what is my minimum hand?",  
  "Explain riichi declaration rules and the ippatsu condition.",
  "What is the yaku minimum required to win a standard hand?",
  "How many tiles are in the wall and how is the initial deal structured?",
  "Describe kan: open kan, closed kan, added kan, and the rinshan draw.",
  "What happens on an exhaustive draw (sanma) with noten penalties?",
  "List the abotive-draw conditions that restart a round.",
  "Explain chombo and its consequence.",
  "How does the point ladder scale beyond mangan?",
  "What is furiten and when does riichi become void?",
  "Show the scoring base: fu and han to base points.",
  "A player wins by self-draw: how much is paid and by whom?",
  "Describe the riichi declared-score sacrifice of 1000 points.",
  "What is tanyao and which terminals are excluded?",
  "Explain pon vs chi priority and the strict single-chance rule.",
  "How many distinct tile types exist and how many copies of each?",
  "What is the canonical state encoding field order from the contract?",
  "Explain the seeded-external RNG and how a dice roll resolves.",
  "Describe yakuhai: which triplets score and at what han?",
  "What is the thirteen-orphans special hand and its score?",
  "Explain the 7-pairs special hand validity.",
  "How does dealer status and renchan work after a win or draw?",
  "Describe the six-function game contract in one paragraph.",
  "What is UNKNOWN-RULE and when must I emit it?",
  "How is the state-hash computed and when is it recomputed?",
  "Explain the terminal-detection loop rule with state-hash.",
  "What does the verifier check on a legal transition?",
  "When is a move marked legal versus hard false?",
  "Describe the canonical restatement that must lead every answer.",
  "How do scoring ties and ranking order get resolved per pack?",
];

function post(prompt) {
  return new Promise((res, rej) => {
    const body = JSON.stringify({
      model: MODEL,
      max_tokens: MAX_TOKENS,
      messages: [{ role: 'user', content: prompt }],
      stream: false,
    });
    const req = https.request({
      host: API, path: '/chat/completions', method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${KEY}`,
        'Content-Length': Buffer.byteLength(body),
      },
    }, (r) => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => {
        try {
          const j = JSON.parse(d);
          if (j.error) return rej(new Error('API error: ' + JSON.stringify(j.error)));
          const u = j.usage || {};
          const hit = u.prompt_cache_hit_tokens || 0;
          const miss = u.prompt_cache_miss_tokens || 0;
          res({ hit, miss, in: u.prompt_tokens || 0, out: u.completion_tokens || 0, t: u.total_tokens || 0 });
        } catch (e) { rej(new Error('parse fail: ' + d.slice(0,200))); }
      });
    });
    req.on('error', rej);
    req.end(body);
  });
}

const RATE = { in: 0.14, out: 0.28, cache: 0.03 }; // $/1M
async function run(arm, promptFor) {
  const out = [];
  const t0 = Date.now();
  for (let wave = 0; wave < N / WAVE; wave++) {
    const batch = [];
    for (let i = 0; i < WAVE; i++) {
      const idx = wave * WAVE + i;
      batch.push((async () => {
        const ts = Date.now();
        const u = await post(promptFor(idx));
        const H = u.in ? u.hit / u.in : 0;
        const cost = (u.in * RATE.in + u.out * RATE.out + u.hit * RATE.cache) / 1e6;
        out.push({ arm, idx, ts: new Date().toISOString(), http: 200, hit: u.hit, miss: u.miss, in: u.in, out: u.out, H: +H.toFixed(4), cost: +cost.toFixed(6), ms: Date.now() - ts });
      })());
    }
    await Promise.all(batch);
    if ((wave + 1) * WAVE < N) await new Promise(r => setTimeout(r, 300));
  }
  return { out, wall: Date.now() - t0 };
}

// A0 naive: short single-prompt per request (no shared prefix)
const a0 = await run('A0', (i) => `You are a riichi mahjong tutor. ${QS[i]}`);
// A2: static corpus prefix + variable question
const a2 = await run('A2', (i) => `${PREFIX}\n\nYou are a riichi mahjong tutor. ${QS[i]}`);

const ledger = `{"run":"w1_gauntlet_v2","ts":"${RUN}","note":"MIXED-CORPUS draft-L0+self-built-L2"}`
  + '\n' + [...a0.out, ...a2.out].map(r => JSON.stringify(r)).join('\n') + '\n';
fs.writeFileSync('/board/w1_gauntlet_v2_ledger.jsonl', ledger);

// ---- summarize ----
function sum(rs) {
  const tot = rs.reduce((a, r) => a + r.in, 0);
  const cache = rs.reduce((a, r) => a + r.hit, 0);
  const cost = rs.reduce((a, r) => a + r.cost, 0);
  const ms = rs.map(r => r.ms).sort((a, b) => a - b);
  const p50 = ms[Math.floor(ms.length / 2)];
  const p95 = ms[Math.min(ms.length - 1, Math.ceil(ms.length * 0.95) - 1)];
  return { tot, cache, cost, p50, p95, Hw: tot ? cache / tot : 0 };
}
const s0 = sum(a0.out), s2 = sum(a2.out);
const outTok0 = a0.out.reduce((a, r) => a + r.out, 0);
const outTok2 = a2.out.reduce((a, r) => a + r.out, 0);
// uncached-equiv input cost for savings: in*priced as all miss + out + zero cache-credit
const equiv2 = (s2.tot * RATE.in + outTok2 * RATE.out) / 1e6;
const actual2 = (s2.tot * RATE.in + outTok2 * RATE.out - s2.cache * (RATE.in - RATE.cache)) / 1e6;
const savings = equiv2 ? (1 - actual2 / equiv2) : 0;
const mean2 = a2.out.reduce((a, r) => a + r.H, 0) / a2.out.length;
const mean0 = a0.out.reduce((a, r) => a + r.H, 0) / a0.out.length;

console.log(JSON.stringify({
  run: 'w1_gauntlet_v2', ts: RUN, corpus: 'MIXED-CORPUS (DRAFT-L0 + self-built-L2)',
  arms: {
    A0: { n: a0.out.length, Hwtd: +s0.Hw.toFixed(4), Hmean: +mean0.toFixed(4), in: s0.tot, cached: s0.cache, cost: +s0.cost.toFixed(6), p50: s0.p50, p95: s0.p95, wall: a0.wall },
    A2: { n: a2.out.length, Hwtd: +s2.Hw.toFixed(4), Hmean: +mean2.toFixed(4), in: s2.tot, cached: s2.cache, cost: +s2.cost.toFixed(6), p50: s2.p50, p95: s2.p95, wall: a2.wall },
  },
  total_cost: +(s0.cost + s2.cost).toFixed(6),
  spend_cap: 0.05,
  savings_vs_uncached: +savings.toFixed(4),
}, null, 2));
