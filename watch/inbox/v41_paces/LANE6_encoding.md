# LANE 6 — the encoding/ folder dig (DeepSeek-V4.1-Flash)

Date: 2026-09-11 (operator clock). Lane 6/8, triparty wave.
Sources: fetched raw from
https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/raw/main/encoding/
— README.md (12 KB), encoding.py (37 KB, ~950 lines), test_encoding.py,
tests/test_input_1.json, tests/test_input_2.json. All five read or skimmed.

## THE POINT

The mystery resolves boring, and boring is the answer: `encoding/` is the
**chat template, shipped as source code**. Not a KV-serialization format, not
a novel context encoding, not a page store. It is the standalone reference
implementation of the V4.1 prompt wire format: OpenAI-style messages in, exact
prompt string out (`encode_messages`), and completion text back into a
structured message (`parse_message_from_completion_text`). DeepSeek ships it
so anyone self-hosting can reproduce the exact tokens the model was trained
on, without importing their inference stack. The tests are paired
JSON-input / TXT-expected-output fixtures proving the format.

## What encoding/ actually contains

- `encoding.py` — pure serializer + parser. Special tokens
  (`<｜User｜>`, `<｜Assistant｜>`, `<｜System｜>`, `<think>`, `<｜DSML｜ …>`,
  `<｜deepseek_image｜>`), tool-call DSML markup, image placeholders with an
  ordered media dict. Zero hashing, zero content addressing, zero cache or
  block machinery (grep for hash/cache/page/kv: only false positives).
- `README.md` — format spec. Documents three V4.1-vs-V4 changes:
  1. DSML tool tags now use a leading space (`<｜DSML｜ calls>` vs
     `<｜DSML｜tool_calls>`).
  2. Reasoning effort is a NUMERIC budget 1–100 (`low`=50, `high`=75,
     `max`=100), rendered once at conversation index 0, thinking mode only.
  3. Mid-conversation system messages via `<｜System｜>` (count as user turns
     for generation-header purposes).
- `test_encoding.py` + `tests/*.json` — pytest fixtures for the above.

## Findings worth keeping (tri-state)

1. SUPPORTED (code, encoding.py:452-470): the numeric effort budget is real
   and the README claims intermediate values "elicit interpolated reasoning
   behavior". That interpolation claim is UNPROVEN — vendor assertion, never
   benchmarked publicly. Cheap tesuji probe if we ever touch a V4.1 endpoint.
2. SUPPORTED (code, encoding.py:738-756): `drop_thinking` strips
   `reasoning_content` from every assistant turn BEFORE the last user message,
   auto-disabled when tools are present. This is the vendor trimming re-fed
   stale reasoning at the prompt-assembly layer.
3. SUPPORTED (code, encoding.py:745): hidden roles `latest_reminder` and
   `direct_search_results` exist in the keep-set. Mutable volatile data
   (date/locale reminders, injected search results) rides in dedicated slots,
   not salted through history.
4. SUPPORTED (README): "quick instruction" single-token task probes ship in
   the format itself: `<｜action｜>` (search-or-answer router),
   `<｜title｜>`, `<｜query｜>`, `<｜authority｜>` (source-authoritativeness
   classifier!), `<｜domain｜>`, `<｜read_url｜>`. These are DeepSeek's own
   internal classification probes, exposed as tokens.
5. UNPROVEN: whether HF serving stacks run this exact file as their template.
   It is labeled "reference"; the deployed template could drift.

## KV-OS relevance verdict: SKIP as a page format — wrong layer

`encoding/` is a deterministic wire serializer. `mag/kvos_block.py` is a
content-addressed block store (sha256-chained 400-word blocks over the
corpus). They do not compete and one cannot be adopted as the other. There is
no page format here to adopt — no addresses, no dedup, no store.

But the file is the best **vendor-side evidence for the KV-OS premise** we
have found: DeepSeek's own template carries drop_thinking (delete stale
reasoning before re-feeding), a dedicated reminder slot (keep volatile bytes
out of the stable prefix), and tool-result merging into user messages (one
canonical placement). They fight the same re-fed-prefix bloat refeed_guard B1
measured (94% of input re-fed reads) — at the assembly layer, with heuristics.
KV-OS attacks it at the storage layer, with addresses. Same disease, our
answer is upstream of theirs.

## Steal list (small, concrete)

- STEAL the convention: numeric reasoning-effort prefix (1–100, aliases
  low/high/max) — finer-grained than our lane-level low/high mapping; test
  on deepseek lanes before trusting.
- STEAL the pattern: mutable data in a dedicated early slot
  (`latest_reminder` style), never interleaved into stable prefix — direct
  design rule for any KV-OS page layout that carries timestamps/reminders.
- STEAL the evidence: drop_thinking = the vendor confirming stale reasoning
  is bloat. Cite this card in the KV-OS P1 fold as independent confirmation.
- REFERENCE ONLY: DSML tool-call format (namespaced tools `search::lookup`,
  `string="true|false"` param typing) — the spec to copy if we ever
  hand-craft V4.1 prompts or build deepseek tool-calling lanes.
- TESUJI SEED: the six quick-instruction tokens are ready-made single-token
  field probes against any V4.1 surface (`<｜authority｜>` alone is their
  moderation-adjacent classifier — wrongthink-map adjacent).

Verdict one line: SKIP adoption, file as reference — steal three conventions,
keep the card as vendor confirmation that the KV-OS problem is real.
