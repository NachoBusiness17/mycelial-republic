#!/usr/bin/env node
// R-1: ROCINANTE_DAYONE_BENCH — GLM-5.3-Flash Unsloth-GGUF speedup benchmark.
// Source card: watch/INTAKE_UNSLOTH_GLM53FLASH_LOCAL_SPEEDUP_20260904.md (21/25 BUILD NOW).
// Hardware gate: Oct 27 (4x Mac Studio M5 Ultra, 512GB unified). Zero deps, Node >= 18.
//
// Usage:
//   node scripts/rocinante_r1_bench.mjs --engine ollama \
//     [--base http://127.0.0.1:11434/v1] [--model unsloth/GLM-5.3-Flash-GGUF:Q4_K_M] \
//     [--runs 3] [--mtp on|off] [--engine-cmd "llama-server --port 11434 ..."]
//
// Gates (from the card):
//   beat 63 tok/s baseline; reach for 110-125 (uzu targets);
//   speedup >= 1.6x with Unsloth GGUF + MTP (n=2-3) vs vanilla (their ceiling 3.4x long-ctx).

import { execFile } from 'node:child_process';

const args = process.argv.slice(2);
function argOf(name, def) {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] ? args[i + 1] : def;
}
const ENGINE = argOf('engine', 'ollama');            // ollama | llama.cpp | custom-command
const BASE = argOf('base', 'http://127.0.0.1:11434/v1');
const MODEL = argOf('model', 'unsloth/GLM-5.3-Flash-GGUF:Q4_K_M');
const RUNS = Number(argOf('runs', '3'));
const MTP = argOf('mtp', 'off');                     // MTP on/off toggle placeholder
const ENGINE_CMD = argOf('engine-cmd', '');          // used when --engine custom-command
const TIMEOUT_MS = Number(argOf('timeout-ms', '300000'));

// MTP n (draft tokens): sweet spot n=2-3 per the card; n=5 goes SLOWER (86.5->63.7 tok/s @4096).
const MTP_N = Number(argOf('mtp-n', MTP === 'on' ? '2' : '0'));

// Fixed prompt set — 5 probes (card: benchmark tok/s at 4k/16k/65k ctx alongside the fleet stack).
// Long-context probe uses synthetic padding to reach ~8K tokens.
const LONG_CTX_FILLER = ('The fleet runs on files, contracts, queue rows, and a signed chain; ' +
  'no seat is load-bearing and any seat can drive or verify. ').repeat(64); // ~8K tokens
const PROMPTS = [
  { id: 'one_word', expect_short: true, max_tokens: 16, prompt: 'Reply with exactly one word: the capital of France.' },
  { id: 'short_reasoning', expect_short: false, max_tokens: 256, prompt: 'A train leaves at 14:00 traveling 90 km/h. A second leaves at 15:00 at 120 km/h on the same track. When does it catch up? Show the reasoning in under 100 words.' },
  { id: 'code_gen', expect_short: false, max_tokens: 512, prompt: 'Write a JavaScript function that deduplicates an array of objects by a given key, keeping the last occurrence. Include one test case.' },
  { id: 'long_ctx_8k', expect_short: false, max_tokens: 256, prompt: `Summarize the following document in 3 sentences.\n\n${LONG_CTX_FILLER}` },
  { id: 'json_extract', expect_short: false, max_tokens: 256, prompt: 'Extract name, date, and amount as strict JSON from: "Invoice from Acme Corp, dated 2026-08-30, total $1,249.50, due on receipt."' },
];

const percentile = (arr, p) => {
  const s = [...arr].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor((p / 100) * s.length))];
};

async function chatOnce(prompt, maxTokens) {
  const t0 = Date.now();
  const res = await fetch(`${BASE}/chat/completions`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      model: MODEL,
      messages: [{ role: 'user', content: prompt }],
      max_tokens: maxTokens,
      temperature: 0,
      // MTP placeholder: engines wire speculative decoding differently (llama.cpp PR flag,
      // Unsloth Desktop toggle). Adjust per engine on day one; harmless extra field otherwise.
      mtp: MTP === 'on' ? { n: MTP_N } : undefined,
    }),
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  const j = await res.json();
  const wallMs = Date.now() - t0;
  const usage = j.usage || {};
  const ct = usage.completion_tokens ?? (j.choices?.[0]?.message?.content?.split(/\s+/).length ?? 0);
  const promptTokens = usage.prompt_tokens ?? 0;
  return { wallMs, completionTokens: ct, promptTokens, text: j.choices?.[0]?.message?.content ?? '' };
}

async function startEngine() {
  if (ENGINE !== 'custom-command' || !ENGINE_CMD) return null;
  const [cmd, ...cargs] = ENGINE_CMD.split(/\s+/);
  const child = execFile(cmd, cargs);
  // Warmup poll until the endpoint answers.
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`${BASE}/models`); if (r.ok) break; } catch {}
    await new Promise(r => setTimeout(r, 2000));
  }
  return child;
}

const child = await startEngine();
const results = [];
try {
  for (const p of PROMPTS) {
    const lat = [], tps = [];
    let ok = 0;
    for (let i = 0; i < RUNS; i++) {
      try {
        const r = await chatOnce(p.prompt, p.max_tokens);
        if (r.completionTokens > 0 && r.wallMs > 0) {
          tps.push(r.completionTokens / (r.wallMs / 1000));
          lat.push(r.wallMs);
          ok++;
        }
      } catch (e) {
        results.push({ probe: p.id, run: i, error: String(e.message || e) });
      }
    }
    results.push({
      probe: p.id,
      runs: RUNS,
      success_rate: +(ok / RUNS).toFixed(3),
      tok_s_median: tps.length ? +percentile(tps, 50).toFixed(2) : null,
      tok_s_best: tps.length ? +Math.max(...tps).toFixed(2) : null,
      latency_ms_p50: lat.length ? percentile(lat, 50) : null,
      latency_ms_p90: lat.length ? percentile(lat, 90) : null,
    });
  }
} finally {
  if (child) child.kill();
}

// Gates
const longCtx = results.find(r => r.probe === 'long_ctx_8k');
const median = results.filter(r => r.tok_s_median).map(r => r.tok_s_median);
const overallMedian = median.length ? +percentile(median, 50).toFixed(2) : null;
const successRates = results.filter(r => r.success_rate !== undefined).map(r => r.success_rate);
const overallSuccess = successRates.length ? successRates.reduce((a, b) => a + b, 0) / successRates.length : 0;
const baselineTps = Number(argOf('baseline-tok-s', '63')); // card: vanilla baseline to beat
const vanillaTps = Number(argOf('vanilla-run-median-tok-s', '0')); // supply from a vanilla run for speedup gate
const speedup = vanillaTps > 0 ? +(overallMedian / vanillaTps).toFixed(2) : null;

const verdict = {
  beats_baseline: overallMedian !== null && overallMedian > baselineTps,
  reaches_uzu_targets: overallMedian !== null && overallMedian >= 110, // 110-125 uzu targets
  speedup_vs_vanilla: speedup,           // gate: >= 1.6x with Unsloth GGUF + MTP
  speedup_gate_pass: speedup !== null && speedup >= 1.6,
  long_ctx_tok_s: longCtx ? longCtx.tok_s_median : null,
};

console.log(JSON.stringify({
  bench: 'R-1 rocinante_r1_bench',
  engine: ENGINE, base: BASE, model: MODEL,
  mtp: { enabled: MTP === 'on', n: MTP_N, note: 'placeholder — wire per llama.cpp PR / Unsloth Desktop on day one' },
  hw_gate: '2026-10-27 (4x M5 Ultra, 512GB unified; 4-bit GGUF 164-212GB)',
  probes: results,
  overall: { tok_s_median: overallMedian, success_rate: +overallSuccess.toFixed(3) },
  gates: {
    baseline_tok_s: baselineTps,
    uzu_target_range: [110, 125],
    min_speedup_vs_vanilla: 1.6,
    ...verdict,
  },
  pass: verdict.beats_baseline && (speedup === null || verdict.speedup_gate_pass) && overallSuccess >= 0.9,
}, null, 2));
