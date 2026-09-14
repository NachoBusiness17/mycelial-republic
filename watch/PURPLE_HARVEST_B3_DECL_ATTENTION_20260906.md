# PURPLE HARVEST B3 — DECLARATIVE ATTENTION (built + falsifiers PASS, 2026-09-06)

**Card:** watch/TRIAGE_HAUL_BOT_01_20260906.md (cite-gate 5/5 PASS, ROUTE: BUILD) ·
**Paper:** arXiv:2609.02737 "Language Models Can Control Their Own Attention" (KAIST AI +
Google DeepMind), verified against arxiv.org/html/2609.02737 this turn. ·
**Built by:** zcode seat, same turn as launch (LAUNCH LAW amendment 5).

## What was built

`mag/decl_attention.py` (445 lines, stdlib only) — the DA protocol as a **byte-level
view protocol** over real fleet read loads. No GPU in this cage, so no fake kernels:
the honest proxy for the paper's attended-KV-positions metric is **attended BYTES** —
bytes actually read from disk via `seek()+read()`. Skipped blocks are never read.
That is the whole point, made literal.

- Block table (the paper's KV block table): `Block`/`Table` (decl_attention.py:63-81),
  built once per doc — `build_table` (:110). Two loaders: boundary-aware text splitter
  `_text_blocks` (:125) using the paper's coarsest-boundary cascade `_CASCADE` (:60)
  (paragraph → newline → sentence → clause → space, never inside a word; 1200B targets
  as our ~2048-token analog), and one-block-per-card depth scan `_card_blocks` (:140)
  for topic_index-shaped JSON (a card IS the retrieval split — the magic-chunk analog
  for a card catalog). Every block sha256-hashed; gaps and the file tail are folded so
  the table tiles the file exactly (that exactness is falsifier F-a).
- Declarations + state machine: `parse_declarations` (:195) — the paper's §2.3 machine
  verbatim in spirit: transitions on the `>` of an opening tag, reverts to GLOBAL on
  the closing tag, and `<global>` produces NO transition (it is the default state).
  Mode axis / selector axis / window axis stay distinct attributes (pyncd law).
- Visibility planner: `plan_visible` (:217). Selectors: `magic_chunks="0,2"` (exact
  paper attribute), `topic="mcp"` (build-time block metadata), `section="5."` (heading
  spans rounded outward to block boundaries — the paper's kept-span outward-rounding,
  headings held in `Table.headings` so naming a span never reads its content),
  `lines="a-b"`; `<local window="N">` takes the recent-N suffix.
- Serving: `read_visible` (:260) — one open, seek per visible block, bytes counted.
  `naive_read` (:273) is the vanilla baseline. Quiz reader is regex extraction only
  (`extract` :278) — zero tokens end to end.
- Surfaces: `python -m mag.decl_attention demo` (falsifier run, exit code = verdict) ·
  `view --doc X --decl '<focus topic="mcp">'` (human read of any block table).

## Falsifier numbers (real, from `demo` run 2026-09-06)

**(a) GLOBAL == naive full read, byte-identical — PASS both docs.**
- corpus/CURRICULUM.md: attended 7,913 == naive 7,913 (sha dfded2e9a77f)
- watch/topic_index.json: attended 283,221 == naive 283,221 (sha 7be832380c5d)

**(b) FOCUS cuts >= 30% with answers intact — PASS both docs.**
- CURRICULUM: `q_nc_license` → CC-BY-NC-4.0 at 79.8% cut (1/6 blocks); `q_economist_lane`
  → "ECONOMIST / COST" at 80.2%; `q_addendum_clone` → human-atlas at 78.3%.
- topic_index: `q_mcp_bucket` — "how many cards carry mcp" → 94, identical under
  GLOBAL and `<focus topic="mcp">`, at **89.3% cut** (94/1,041 blocks, 30,248B of
  283,221B). This is the "read the row, not the zone" seat law compiled into a mask.

**(c) LOCAL cuts >= 60%, recent answers intact, out-of-window REPORTED — PASS both.**
- CURRICULUM: window=2 keeps the answer (CC-BY-NC-4.0 from the Wave-1 table) at
  78.3% cut; window=3 kept in the receipt too — 59.0%, honestly UNDER the bar (the
  knob has a cost; we show it, not just the passing row). Out-of-window drop
  detected + reported: `q_nc_license_local` → None (answer lives in block 0).
- topic_index: newest-card title intact at **91.3% cut** (window=100). Out-of-window
  drop reported: `q_first_card` — LOCAL returns the first in-window card
  (watch/rows/drift_check_2.row.md), NOT silently the global answer. `q_header_total`
  under focus → None, reported (the header is out of scope for an mcp focus — that
  is the paper's accuracy-drop analog, surfaced not hidden).

**OVERALL: PASS.** Table-build honesty: build reads the whole file ONCE (7,913B /
283,221B — computing offsets, hashes, tags; the paper's analog is the pre-placed
magic-chunk transcript in the scaffold). Per-query numbers above are per-query.

## Verified vs not (tri-state)

- SUPPORTED (measured here): all three modes over two real fleet artifacts; byte
  identity, cut percentages, answer integrity, honest drop reporting. Numbers above.
- SUPPORTED (paper's, not ours): −52.0%/−31.1% attended tokens, −1.27pp/−2.75pp
  accuracy on Gemma-4-31B / Qwen-3.6-27B over 15 tasks; vLLM hooks with no kernel
  changes; FlashAttention compatibility. **We did not run any of that — no GPU in
  this cage. Our numbers are a byte proxy; theirs are kernels. The protocol SHAPE
  is what we verified.**
- UNPROVEN: transfer of these byte cuts to LLM context costs on the fleet's live
  lanes (the byte→token ratio is doc-dependent); focus success-rate analogs for a
  real model emitting declarations (the paper's 58-99% adherence is model-dependent).
- Quiz readers are deterministic regex, chosen knowing the answers' locations —
  this is a protocol-conformance test, not a benchmark.

## Lineage (steal the bones, name the reinterpretation)

- **Zero-Mem** (memory/steal/STEAL_ZERO_MEM_20260814.md): "memory ops are not
  generation" — DA-as-view is fully non-generative, deterministic routing at query
  time. Zero-Mem kept ONE reader LLM call; this goes stricter: regex readers, zero
  tokens. Their dual-view-over-raw-traces is the same move at memory scale.
- **pyncd attention** (memory/steal/STEAL_PYNCD_ATTENTION_20260814.md): "distinct
  axes stay distinct; the diagram is the check" — mode/selector/window never merge
  in the declaration grammar, and the TEST (byte-identity reconstruction + quiz
  answer identity) is the composition check that would catch a merged axis.
- **Seat law** "read the row, not the zone" (SELF-STEAL 2026-08-26) = `<focus>`
  compiled into a mask — the triage card's own tape, now running code.
- Next doors (not built, no scope creep): serve the topic-index FOCUS lane to
  real seat queries (the 89.3% cut is the organism's daily food); a declaration-
  emitting reader on a live lane to measure OUR focus success rate.

*Files: mag/decl_attention.py (new). Nothing else touched — no dashboard/static, no
chain writes, no processes. Demo is idempotent and read-only.*

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran `python -m mag.decl_attention demo` fresh: EXIT=0, every number
reproduces line-for-line — GLOBAL byte-identity shas (dfded2e9a77f / 7be832380c5d),
FOCUS cuts 80.2% / 89.3% with answers intact, LOCAL 78.3% / 91.3% with out-of-window
drops REPORTED (q_nc_license_local, q_first_card), and the under-bar window=3 59.0%
case shown not hidden. Builder's own first-run failures (byte gaps, mode-dispatch
case mismatch, heading-vs-span selector) were caught by the falsifiers before landing
— the verify half genuinely ran. VERDICT: PASS.
