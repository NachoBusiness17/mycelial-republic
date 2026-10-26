# RECEIPT: DeepSeek off-peak scheduling + 120x-to-30x cache-ratio correction (2026-09-25)

Task: MICKEY-17 v2 GO row 9 / fold row 13 of `corpus/steal/MASTER_MICKEY17_V2_20260924.md`
(`[lane: deepseek-agents, confirms-ours]`, line 90-93; GO summary line 170), named in
`watch/inbox/GO_LIST_EXECUTION_20260925.md:33` as not-done. Fold evidence base:
`memory/runs/mickey17_v2/lanes/deepseek-agents.json` rows 0-1 (pro hit/miss now 30x, was
recorded 120x; peak = 01:00-04:00 and 06:00-10:00 UTC Mon-Fri, everything else off-peak,
all token prices halve; source https://api-docs.deepseek.com/quick_start/pricing as quoted
in the lane row). No API calls were made; $0 spent.

## 1. Lane scheduler notes PATCHED

`memory/burns/MANIFEST.json` protocol (the burn program's scheduling notes, read at every
fire per `lean_fire`): added key `deepseek_windows`:
"Any paid DeepSeek call (burns, fan-outs, dig runs) fires OUTSIDE peak: peak = 01:00-04:00
and 06:00-10:00 UTC Mon-Fri (excl. Chinese public holidays); off-peak = all weekend +
04:00-06:00 + 10:00-01:00 UTC, where all token prices halve. Prefer deepseek-v4-flash over
pro (off-peak cache-hit $0.003/1M; pro cache advantage is 30x, not the stale 120x). Source:
https://api-docs.deepseek.com/quick_start/pricing via MICKEY-17 v2 fold lane deepseek-agents
rows 0-1 (GO row 9 ...); patched 2026-09-25."
Also appended to `protocol.cadence`: "; paid DeepSeek work obeys protocol.deepseek_windows".
Verified: MANIFEST re-parses, key present.

Not touched on purpose: `mag/lane_runner.py` (the in-cage lane scheduler, live per
`logs/lane_scheduler.log`) is free-lanes-only by LAW-058 (docstring line 11: refuses any
paid-lane call), so no DeepSeek window belongs in its SCHEDULE dict. `watch/LANE_SLOT_MAP_20260901.md:21`
already carries the same UTC windows but is operator-verbatim doctrine ("Do not paraphrase");
left byte-intact. `corpus/steal/ZCODE_REPO_STEAL_MAP_20260924.md:128` is the fold's prior-art
pointer (record of the zcode repo's offPeakTaskService), an archive; not modified.

## 2. 120x -> 30x corrections (living surfaces, in-place stamps per house convention)

Corrections follow the file's own convention (see kv_cache_compaction.md finding 7, corrected
the same way earlier today by another seat). Every remaining "120x" string below a stamp is
the corrected-FROM value, named as superseded.

1. `memory/research_polished/kv_cache_compaction.md` (the living doctrine file the fold names):
   line 6 essence ("30x on pro; pro figure corrected 2026-09-25 from the stale 120x, see
   finding 1 stamp"), line 9 finding 1 (pro hit/miss = 30x, corrected 2026-09-25, pre-Sept-10
   table and its pro absolutes declared stale), line 17 finding 9 (ratio resolution rewritten:
   flash 50x / pro 30x as of the 2026-09-10 table).
2. `memory/improve/deepseek_api/repack_vs_cache_analysis.md`: CORRECTION 2026-09-25 block
   inserted directly under the title; the 2026-08-02 body (lines 17/24/43/52 still carry the
   old table) kept byte-intact as a dated record, covered by the stamp.
3. `memory/improve/deepseek_api/multi_agent_integration_plan.md:11` ("cache hits 50x flash /
   30x pro cheaper; pro corrected 2026-09-25 from the stale 120x").
4. `memory/improve/deepseek_api/seat_division_of_labor.md:13` (same correction inline).
5. `watch/inbox/kv50_findings.json` entry idx 47 (the cache-doctrine finding): evidence quote
   annotated with a [CORRECTION 2026-09-25] marker (its quote captured pre-correction bytes);
   "50-120x hit-price ratio" in finding corrected to "50x (flash) / 30x (pro)". File re-parses,
   48 findings intact.
6. Outside the named doc scope but part of "everywhere it appears", code/config comments:
   `mag/cache_router.py:9`, `configs/mag.yaml:17-19`, `configs/providers.yaml:317-318`
   (all "50x flash / 30x pro" with the correction stamp). Verified: cache_router.py parses
   (ast.parse OK), both YAML files parse (yaml.safe_load OK).

## 3. Verification (ran this session)

Command: `grep -rnE "120[- ]?x" memory/research_polished/ memory/improve/deepseek_api/
memory/burns/ watch/inbox/kv50_findings.json mag/cache_router.py configs/mag.yaml
configs/providers.yaml` (all living surfaces): every hit eyeballed; ZERO lines assert
pro = 120x as current fact. Remainders are (a) stamps naming the superseded value, (b) the
stamped 2026-08-02 body of repack_vs_cache_analysis.md. JSON/YAML/Python parse checks all ran
and passed (commands in section 2 items 5-6 and section 1).

Estate-wide census command: `grep -rlE "120[- ]?x" memory/ watch/ corpus/` = 130 files at
mid-session; re-run after fixes = 127 files. The raw-string count stays high BY DESIGN: every
correction stamp names the superseded value ("from the stale 120x"), the fold records carry the
task's own text, and the sealed/derived/archive classes below are untouched on purpose. The
claim-level check is the living-surface grep above: zero files assert pro = 120x as current fact.
Non-claim survivors left untouched, by class:
- sha256-sealed / frozen records: `memory/research_packs/20260809T*` + `steal_cache_miss_spike_detection_20260811.answer.remote.md`
  (protocol.json files carry "freeze-before-run" seals), `memory/runs/compaction_eval/steps_frozen_20260920.jsonl`,
  `memory/seals/*/configs/providers.yaml` (14 point-in-time seals). Rewriting these falsifies
  sealed history (the exact defect class MICKEY-17 A1/E1 was written to kill).
- append-only session/trajectory logs: `memory/agent_sessions/*.json` (4), `memory/trajectory/steps.jsonl`,
  `memory/training/events.jsonl`, `memory/training/refined_training_data.jsonl`,
  `memory/biography/residual/*`, `watch/session_digest.jsonl` (live stream, still being
  appended to by the session logger; its 2 hits are dated 2026-08-06 tool_result previews).
- fold/burn records that ARE the correction's provenance: `memory/runs/mickey17_v2/lanes/deepseek-agents.json`
  (the detecting lane row), `memory/runs/mickey17_v2/runs/.../deepseek-week.json`,
  `memory/runs/mickey17/digest_*.jsonl`, `memory/runs/mickey17/MASTER_INDEX_20260920.md`
  ("map off 120x" = unrelated file-count ratio), `memory/runs/session_mining/2026-08-26/MEMORY/fold_z_ai3_c272.md`
  (dated fold verdict), `memory/runs/union_audit/audit_02_summary.md` (dated audit),
  `corpus/steal/MASTER_MICKEY17_V2_20260924.md` (the GO item text itself: "was recorded 120x"),
  `watch/inbox/GO_LIST_EXECUTION_20260925.md` (the task name "120x->30x").
- derived indexes/graph state over sealed sources: `memory/lenses/corpus_index.json`,
  `memory/mycelium/graph_snapshot.json`, `memory/mycelium/nodes.jsonl`,
  `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`. Regenerate from sources; sources are sealed, so
  hand-editing the derived copies would desync them. Named as owed cleanup if the estate ever
  re-seals the packs.
- false positives / unrelated numbers: "120x120.png" filename (`memory/runs/file_dogfood/manifest.jsonl`),
  "read 120 bytes" (kv50 idx 28), "map off 120x" (2 files), "Same sentence, 120x price spread"
  (`memory/runs/jev_salon2/economist.md` = drive-vs-keystroke cadence pricing, not cache),
  vendor/course libraries and oral history under `corpus/library/`, `corpus/oral_history/`,
  `memory/corpus/`, `corpus/training_materials/` (external archives), browser-profile binaries
  in `memory/runs/host_browser/`, `watch/inbox/qdrop_export/*.png` (binary), archaeology copies
  under `corpus/oral_history/nacho_archaeology/` (frozen dig of the pre-fix tree),
  `configs/providers.yaml.bak-*` (timestamped backup).

## 4. NOT done, stated plainly

- The pro ABSOLUTE prices in code (`mag/cache_map.py:42` hit 0.003625 / miss 0.435,
  `tools/tier_probe.py:22,60,295`, same values echoed in `mag/session_maze.py:202,224` comments)
  are left at the pre-Sept-10 numbers: the fold gives the new RATIO (30x) but no verified new
  pro absolutes, and inventing prices is fabrication. Per kv_cache_compaction.md finding 9's own
  rule, re-pull the live pricing page before touching billing math. This is the one owed follow-up.
- No live re-fetch of https://api-docs.deepseek.com/quick_start/pricing was performed; the 30x
  figure is taken from the fold row (`memory/runs/mickey17_v2/lanes/deepseek-agents.json` row 0),
  which is the ask's designated evidence. The claim chain is fold -> receipt, not fold -> web.

## 5. Sibling-surface note

`watch/inbox/GO_LIST_EXECUTION_20260925.md` gets a dated addendum marking GO row 9 closed;
that file's own list is otherwise untouched (other seat's record).
