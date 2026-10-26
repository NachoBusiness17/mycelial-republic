const fs = require('fs');
const path = '/board/probes/boundary/';

const FILLER = [
  "The coastal survey of the Meridian estuary documented tidal gradients,",
  "sediment transport rates, and the seasonal migration of benthic fauna.",
  "From April to September, samples were taken at fortnightly intervals along",
  "a forty-kilometer transect, and each station was logged with its depth,",
  "temperature, salinity, and substrate composition. The data were normalized",
  "against a reference baseline and then smoothed using a moving average that",
  "suppressed short-period noise while preserving the underlying seasonal",
  "signal. Notable anomalies, such as the unusually high turbidity readings",
  "in late June, were flagged for follow-up and cross-referenced against",
  "upstream discharge records before any interpretation was accepted.",
  "The final report recommended a reduced sampling cadence for the following",
  "season, given the stability of the observed regime."
].join(' ');
const TOKENS_PER_FILLER = 110;

// FIXED context ~32K tokens for ALL docs (identical, cacheable).
const TARGET_CTX = 32000;

// Realizable needle->query distances within a 32K ctx (query at end-of-context).
// 64k/128k cannot fit on the 32K rung; they belong to the longer-context ladder probe.
const DISTANCES = [512, 4096, 16384, 32768];

const sentinel = "SENTINEL-OCTAGON: the violet cargo manifest was sealed under brass in dock eleven.";

function repeatToTokens(target) {
  const parts = [];
  let acc = 0;
  while (acc < target) {
    parts.push(FILLER);
    acc += TOKENS_PER_FILLER;
  }
  return parts.join('\n\n');
}

function build(tokensAfterNeedle) {
  // Structure: [before][needle][after=tokensAfterNeedle][QUESTION]
  // Total = TARGET_CTX (+ small fixed question overhead ~20 tokens).
  const beforeToks = Math.max(2, TARGET_CTX - tokensAfterNeedle - 30);
  const before = repeatToTokens(beforeToks);
  const after = repeatToTokens(tokensAfterNeedle);
  const q = "QUERY-MARKER: quote verbatim the single sentence in this document that begins with the token SENTINEL-OCTAGON.";
  return [before, sentinel, after, q].join('\n\n');
}

for (const d of DISTANCES) {
  const doc = build(d);
  const fname = `needle_${d}.md`;
  fs.writeFileSync(path + fname, doc + '\n');
  const tokEst = Math.round(doc.split(/\s+/).length);
  console.log(`${fname}: ~${tokEst} tokens (~32K ctx), needle ${d} tokens before query`);
}
console.log('DONE');
