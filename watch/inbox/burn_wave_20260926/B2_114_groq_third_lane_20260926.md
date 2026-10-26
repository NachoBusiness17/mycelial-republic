# B2-114 groq third chat lane decision (2026-09-26)

## Verdict

REGISTER THE SKIP. openai/gpt-oss-20b stays out of the groq chat rotation and
remains registered in `out_of_routing_scope` (configs/providers.yaml:322-335).
Decision-grade evidence, not inheritance: the id is live and served (fresh
probe 2026-09-26T22:52:10Z: chat call HTTP 200, content "pong", 0.43s), so the
skip is not papering over a dead id; it stands on arithmetic. External groq
limits are PER MODEL (1K RPD / 200K TPD per text model), so a third lane would
add its own independent bucket rather than split the two existing ones, which
corrects the old "held back to protect the quota" register rationale. The skip
holds because the provider-level Mag soft guard (100 calls / 100K tokens daily,
configs/providers.yaml:341-343) binds first: at its ceiling the estate can pull
at most 100K tokens/day from groq total, roughly half of ONE model's external
200K TPD bucket, so a third lane adds zero usable throughput under the current
guard. Promotion path is written into the block: re-open only if the operator
raises the guard to exploit per-model external buckets AND a consumer wants
20b-class quality. models list, default_model, quota bytes, and tier_max are
byte-untouched; the landing is comment-only on the register entry.

## Evidence with file:line quotes

- Pre-edit, configs/providers.yaml:322 (B2-116 register wording):
  `# sibling of the configured 120b lane, held back to protect the quota`
  above `- openai/gpt-oss-20b`. Post-edit, configs/providers.yaml:322-334:
  `# B2-114 third-chat-lane DECISION 2026-09-26: registered skip, stays out`
  `# of models:.` with the per-model-bucket correction, the guard-bind
  arithmetic, the promotion path, and this receipt pointer; the id line
  `- openai/gpt-oss-20b` moved 323 -> 335, still inside `out_of_routing_scope:`
  (configs/providers.yaml:310), count still 9.
- Local guard, configs/providers.yaml:341-343: `quota:` / `max_calls: 100` /
  `max_tokens: 100000` (period daily), provider-level, shared by every model
  in the lane. External denominator, watch/inbox/LINKS.jsonl:312
  (EPNEWS-GROQ-RPD-CONFIRMED): "1K requests/day and 200K tokens/day per text
  model (30 RPM, 8K TPM)"; page notes "limits apply at the organization level,
  not individual users", i.e. per-model buckets shared across keys, not
  buckets shared across models. Guard ceiling 100K tokens/day is 50 percent of
  one model's external 200K TPD; the binding constraint is local.
- Live probe bytes, watch/inbox/burn_wave_20260926/B2_114_groq_20b_probe.json
  (rerunnable via B2_114_groq_20b_probe.py, key read from .env GROQ_API_KEY,
  never printed): ts 2026-09-26T22:52:10Z; GET /models status 200,
  model_count 11, gpt_oss_20b_listed true (same roster as B2_35, 10h later);
  POST chat/completions model openai/gpt-oss-20b status 200, latency 0.43s,
  finish_reason "stop", content "pong" (4 chars), usage completion_tokens 31
  with reasoning_tokens 21, model_echo "openai/gpt-oss-20b". Listed AND
  served; also shows the reasoning-token overhead class (21 of 31 completion
  tokens on a trivial prompt).
- Post-edit validation: yaml.safe_load parse green; models ==
  [openai/gpt-oss-120b, qwen/qwen3.8-27b]; default_model openai/gpt-oss-120b;
  out_of_routing_scope count 9 with gpt-oss-20b present and absent from
  models; quota 100/100000 intact; tier_max T2. Em-dash law: zero new
  em-dashes (the one hit in the groq block is the pre-existing 2026-08-26
  two-key comment).
- Docs denominator for gpt-oss-20b, LINKS.jsonl:312 verbatim: "same for
  openai/gpt-oss-20b and qwen/qwen3.8-27b" (30 / 1K / 8K / 200K), confirming
  the brief's denominator claim against same-day bytes.

## Work done

1. Read the brief, both pointer receipts (B2_35_groq_surgery_20260926.md,
   B2_116_groq_nonchat_classification_20260926.md), B2_35_groq_models.json,
   LINKS.jsonl:312-313, and the full groq block before touching bytes.
2. Found the decision already half-made: B2-116 had registered gpt-oss-20b
   out-of-scope with a quota-protection rationale; this lane's job was to
   make the call decision-grade and fix the mechanism if wrong.
3. Filed the B2-250 claim line on configs/providers.yaml in QUEUE.md Open
   (claim 2026-09-26T22:55Z), re-read the target line, no foreign claim.
4. Ran the two-call live probe (synthetic prompt only, never private
   material) to rule out the listed-but-unserved falsifier class from B2-35
   and to measure the guard relationship on fresh bytes.
5. Landed the comment-only decision edit on the register entry (rationale
   corrected to guard-bind arithmetic, promotion path named, receipt pointer
   in the block); no behavior bytes changed.
6. Validated YAML parse and block shape with .venv/Scripts/python.exe;
   verified the em-dash law on the edited block.
7. Note: providers.yaml is gitignored (.gitignore:23), machine-local; the
   landing is the live file plus this receipt. The claim line is retired
   in place in the same QUEUE.md pass that flips this row.

## Falsifier

This decision is inverted if any of the following holds: (a) the operator
raises the groq provider guard (max_calls/max_tokens) past what the two
existing lanes' external buckets absorb, at which point the guard-bind
arithmetic expires and a third lane starts adding usable throughput (the
promotion path in the block comment names this); (b) a rerun of
B2_114_groq_20b_probe.py shows gpt-oss-20b absent from /models or serving
404 model_not_found (the skip would then rest on a dead id and the register
needs re-classification per B2-116 falsifier (a)); (c) a consumer actually
needs 20b-class quality on groq (for example both chat lanes quota-sick and
qwen unavailable), in which case holding the lane back is wrong and it should
be promoted rather than skipped; (d) the probe JSON is found fabricated
(ids or usage not reproducible by rerunning the probe against the live
endpoint).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_35_groq_surgery_20260926.md (read in full);
watch/inbox/burn_wave_20260926/B2_35_groq_models.json (read in full, roster
byte source); watch/inbox/burn_wave_20260926/B2_116_groq_nonchat_classification_20260926.md
(read in full, the register this decision upgrades); watch/inbox/LINKS.jsonl:312
(EPNEWS-GROQ-RPD-CONFIRMED, per-model denominator, quoted from bytes on disk)
and :313 (ALERT-GROQ-FLEET-IDS-GONE, context); configs/providers.yaml groq
block read in full pre- and post-edit. Fresh live endpoint calls this lane:
GET api.groq.com/openai/v1/models and one chat/completions call to
openai/gpt-oss-20b, both 2026-09-26T22:52:10Z, synthetic prompt only.
console.groq.com/docs/rate-limits accepted via the same-day EPNEWS row, not
independently fetched (no browser in this lane).
