# PA-S8stealth-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## 1. What Rots

**Age/overwrite.** Answer files are overwritten in place each cycle; the JSONL register is the only history.
- Source: `01__STEALTH_TRIAGE_20260930.md` section 1: "overwritten per cycle - the JSONL is the only history."
- Byte proof: `00__STEALTH_MINED_FINDINGS.jsonl` rows at `2026-10-02T01:57:18` and `2026-10-02T02:33:44` both point to the same `answer_file` path (`w-belt-cube-mechanism_openrouter1.md`). The second overwrites the first.

**Dedup.** N rows re-derive one answer; the bank grows without information growing.
- Source: `01__STEALTH_TRIAGE_20260930.md` section 1: "122 rows collapse to 3 topics x 4 lanes."
- Source: same file, F4: "44 rows today re-derived one answer (rib law: N copies collapse to one opinion)."
- The 10-02 tail shows the same pattern repeating with `w-belt-cube-mechanism` across 4 lanes.

**Contradiction.** Findings contradict standing ribs but no process resolves the conflict.
- C1: 92 free-lane rows at 100% `finish=stop` contradicts `RIB_FREE_USAGE_POLICY_20260823` claim of 429/empty. (Triage doc section 3.)
- C2: `cached_tokens=0` on all 62 ling:free rows contradicts the ~98% cache-hit claim. (Same section.)
- These contradictions are flagged but have no owner. They sit.

## 2. Triage Rule: Climb or Die

**Climb triggers** (a finding earns funded-tier verification when):
- It maps to a live repo path with a concrete patch. (F3: "dHead rung is implementable now" targeting `mag/water_graph.py`.)
- Two independent lanes converge on the same negative result. (F4: hermes + space-bunny both concluded no Kabbalah framing exists in mech-interp.)
- It contradicts a standing rib with byte evidence. (C1, C2 above.)

**Die triggers** (a finding is dropped when):
- Ponytail audit returns `false`. (F5: `{"//transformer-circuits.pub/2021/framework.html": false}` - "that citation must not propagate.")
- It is a re-derivation of an already-banked finding. (Dedup collapse rule.)
- No funded-tier seat picks it up within one triage cycle. (Implicit: the triage doc assigns actions but no deadline or assignment mechanism exists.)

## 3. Failure Mode: Triage Becomes the Second Unread Pile

The triage doc names its own death condition.
- `01__STEALTH_TRIAGE_20260930.md` section 4: "promote to `memory/` once an ingester exists."
- The JSONL note field (arch-03 D6 fix, visible in 10-02 tail rows): "no percolator/quantizer ingester exists, so the old note named modules that never read this file."

The triage is a document, not a process. It has no automated consumer, no deadline, no assignment. It will rot identically to the findings it triages: overwritten, deduplicated into silence, contradicting nothing because nothing reads it.

**Falsifier:** If a funded-tier seat implements F1 (compression-progress reward) or F3 (dHead rung) before the next triage cycle, the triage is not a second pile. If neither lands, the rule is confirmed.
