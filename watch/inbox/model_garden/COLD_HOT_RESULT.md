# COLD_HOT_RESULT - the Heart of Gold trial, COLD-1 (2026-10-01)

**Schema:** coldhot.trial.v1 · **lane:** COLD-1 · **spec owner:**
`watch/inbox/model_garden/COLD_VERTEX_LAYER.md` "THE POLICY" section (falsifiable
claim: improbability-sampled steering vs GPS-gradient-only over the same budget,
judged by novelty yield per dollar; if cold never beats hot across a fair trial,
the Heart of Gold is dead as policy).

**Instrument:** `tools/code_swarm.py` (the standing swarm-review organ, unchanged;
contract byte-identity across arms verified at staging: identical 1153-char
review contract, only the SOURCE block differs per file). Families: the tool's
own cheapest config (kimi on Nous credits, glm-flash on z.ai coding endpoint,
deepseek-chat thinking-off). Budget: $0.50 cap per arm, $1.00 trial cap.

## 1. The arms (disjoint target sets, same contract, same families, 3 reviews per file)

**Visitation census first.** Reviewed-file bank built from every code-review
program's manifest: swarm1 (53 files), garden-v1 B1-B5 (5 files), riblive1 +
genlive1 (3 files) = 61 reviewed files. Cold pool: 1,446 never-reviewed .py files
in mag/tools/scripts. Cold candidates ranked by SHAREDNESS (import connectivity):
the top of that ranking is the estate's spine, never reviewed by any swarm:
orchestrator (62 importers), training_events (52), verkle_knot (50),
operator_inbox (35), skill_ledger (32), preferences (22), chain_query (20),
registry (18). Census artifact: `coldhot_visit_census.json`; helper
`coldhot_select.py` (both in this directory).

**HOT arm (GPS-gradient-only): the 10 highest verified-signal surfaces.**
scripts/descent_driver.sh (8-family converged, the grid's loudest signal) ·
watch/inbox/SHARED_SURFACE_CONTRACT.json (8-family) · mag/switchboard_v2.py
(5-family + matrix X03-X06) · tools/hermes_burn.py (matrix X01-X02) ·
mag/steer_seal.py (matrix X12-X14) · the five strongest seat-verified swarm1
REAL-cluster files: tools/ocean_v2_pilot.py, tools/roblox_npc_gateway.py,
tools/reverse_map.py, mag/preload_selector.py, mag/desk_model_probe.py.

**COLD arm (improbability-sampled): the 8 coldest shared vertices + the 2
divergence-marked regions (unsettled matrix pairs).** Cold-8 by sharedness with a
budget size cap: mag/orchestrator.py (2056 ln), mag/training_events.py,
mag/verkle_knot.py, mag/operator_inbox.py, mag/skill_ledger.py,
mag/preferences.py, mag/chain_query.py, mag/registry.py. Divergence-2 pulled
from CROSS_RACTOR_MATRIX unsettled pairs: mag/policy_engine.py (the X06
authority-model organ the matrix cites but nobody reviewed) and
mag/switchboard.py (v1 ancestor, 12 live importers, same authority/parse DNA as
X06/X14). Note: ghost.py (4242 ln) and improve.py (2786 ln) outrank some picks by
sharedness but were excluded by the budget cap; the two biggest unvisited
surfaces stay unpriced (a cold-arm handicap, named).

## 2. The burn (60 asks, 60 landed)

| arm | asks | landed | cost_usd | clusters | REAL |
|---|---|---|---|---|---|
| HOT | 30 | 30 | $0.0358 (ds 0.0267 + glm 0.0091 + kimi 0 metered) | 54 | 10 |
| COLD | 30 | 30 | $0.0471 (ds 0.0380 + glm 0.0091 + kimi 0 metered) | 69 | 6 |
| total | 60 | 60 | **$0.0829 of $1.00 cap** | 123 | 16 |

Zero kimi EMPTY_REASONING terminals, zero refusals. 2 glm 429 transport failures
on hot (steer_seal, ocean_v2_pilot) recovered by the sanctioned lower-width
catch-up (same shape as swarm1; landed outputs skip, no same-params refire).
Worst-case crosscheck with kimi priced at OpenRouter list (SWARM_1 precedent,
~$0.0068/ask): ~$0.22 total, still 22 percent of cap. Run dirs:
`watch/inbox/model_garden/coldhot-hot/`, `coldhot-cold/` (manifests sha-stamped,
raw sidecars, rollup.json).

## 3. Novelty judging (claim-level, seat byte-walked; known bank = the three
contract organ violations + swarm1's 50 REAL clusters + matrix settled rows
X01-X14 + riblive/genlive rows)

Rule: a REAL cluster counts NEW only if at least one member claim names a
mechanism not in the bank AND the seat verified it on bytes (convergence is
corroboration, not adjudication).

### HOT arm: 10 REAL -> 5 NEW (verified), 4 KNOWN re-reports, 1 dead cluster, 2 leads

NEW, byte-verified:

1. tools/reverse_map.py:334-340 (3-family) - probe_model returns None on ANY
   exception ("inconclusive" transient network hiccup) and the caller swaps the
   healthy PAID model to FLASH: silent judgment-tier demotion. NOT in swarm1's
   bank for this file (hash-seed rotation, worst_case_cost).
2. tools/reverse_map.py:243 (2-family) - the analyzer judge lambda hardcodes
   shape "reasoning", ignoring the probe's shape verdict, so a demoted fleet is
   analyzed with the wrong rail.
3. mag/steer_seal.py:381-387 (2-family) - on a broken-seal PERMIT word in warn
   mode, _gate returns the RAW envelope JSON (mac included) as Admitted.text:
   downstream consumers receive envelope bytes instead of the payload. Distinct
   from the banked X13 mode-sentinel fail-open.
4. watch/inbox/SHARED_SURFACE_CONTRACT.json:5-10 (2-family) - canonical.read_first
   hardcodes the container route "/board/inbox/INDEX.json" and the wsl alias
   resolves a /mnt/c host path while container resolves /board: three client
   classes following the contract literally read different (or nonexistent)
   roots. Not banked (X09 settled validator absence, not path divergence).
5. mag/preload_selector.py:336-338 (2-family, LOW materiality) - no guard that
   the conditioned and shuffled probe arms differ in order before scoring.

KNOWN re-reports (excluded per the mission): descent_driver cluster (mv-loss,
%H%M collision, unbounded log: all X07/X08 bank; glm's "header promises skip but
loop never checks" REFUTED on bytes: the skip lives in the child
tools/hermes_burn.py, proven by this trial's own rerun behavior) · ocean_v2_pilot
cluster (cost-cap + Gate-B-justify: both swarm1-banked) · switchboard_v2 replay-set
cluster (in-memory restart wipe: X03 bank corollary) · switchboard_v2 confirm()
cluster (kimi TTL claim = the X05-refuted haiku claim; glm "check_budget never
rerun" refuted by policy_engine's own validate_authority docstring step 4).
Leads, unsettled, not counted: ds's confirm()-budget-frozen-snapshot claim
(switchboard_v2:452), ds's /api/ps eviction-timing claim (desk_model_probe:107;
its convergent partner kimi zero-division was REFUTED: the `if size and vram`
guard exists).

### COLD arm: 6 REAL -> 6 NEW (all verified; nothing banked on never-reviewed files)

1. mag/chain_query.py:142-165 (3-family) - since() compares ISO timestamps as raw
   strings (format divergence and missing ts misorder, "" sorts earliest);
   exists()/breadcrumb() substring+regex over the FULL json.dumps of each knot,
   so any value matches, not just ids.
2. mag/preferences.py:17-24 (3-family) - load_prefs returns {} on corrupt file,
   and every set_* is an unlocked read-modify-write over it: the next write after
   a corrupt load WIPES all other keys; concurrent set_* calls lose updates
   (whole-file replace, no lock). One member (kimi) re-reports organ-c
   atomicity; the wipe and lost-update mechanisms are new.
3. mag/preferences.py:48-53 + set_drainer (2-family) - API asymmetry:
   set_drainer honors the MAG_DRAINER env lock and refuses shadowed writes;
   set_operator_active has no such check, so writes under a set
   MAG_OPERATOR_ACTIVE are silently ineffective (env shadows at read).
4. mag/preferences.py:46-54 (2-family) - the env-vs-pref contradiction surface:
   status reports env_locked but the setter ignores it (same organ as 3, merged
   for law purposes).
5. mag/skill_ledger.py:213-238 (2-family) - seed_from_bench has NO dedupe
   (seed_from_training dedupes by content_hash; bench passes content_hash="")
   so every re-run re-appends all bench rows and inflates the ok_rate buckets
   proven_moves trusts.
6. mag/switchboard.py:527-595 (2-family) - unresolved steer targets silently
   fall back to holder tier "T2" and still post to a raw task_id string
   (typo'd or dead targets write anyway); the drop record reports
   context_len = len(context) but persists only context[:2000], corrupting
   consumers that trust the length.

Divergence-marked pick postscript: policy_engine produced 0 REAL clusters. The
X06/X14 unsettled questions are intent questions; the matrix already ruled them
premium-tier judgment, and the defect contract could not advance them. The
unsettled pairs REMAIN unsettled; this trial does not resolve them.

## 4. Yields per dollar (the three pre-registered novelty axes)

| axis (per dollar) | HOT ($0.0358) | COLD ($0.0471) | winner |
|---|---|---|---|
| NEW REAL clusters | 5 -> 139.7 | 6 -> 127.4 | HOT +9.7 pct |
| new law candidates | 3 (+1 weak) -> 83.8 | 5 -> 106.2 | COLD +26.7 pct |
| indirect connections | 2 -> 55.9 | 3 -> 63.7 | COLD +14.0 pct |
| composite (sum) | 279.4 | 297.3 | COLD +6.4 pct |

**New law candidates minted by the trial.** HOT: L-H1 FAIL-OPEN-PAYLOAD-LEAK (a
warn-mode admit must never hand downstream the raw envelope bytes; unwrap or
refuse) · L-H2 NO-SILENT-TIER-DEMOTION (a transport error must not swap the
judgment tier to flash; demotion is a routed verdict, ties directly to
RIB_DRIVING_LADDER) · L-H3 CONTRACT-PATH-RECONCILIATION (read_first must be
alias-resolved per client class) · weak L-H4 PROBE-ARMS-MUST-DIFFER. COLD: L-C1
TIME-NORMALIZATION-BEFORE-COMPARE · L-C2 LOAD-FAILURE-MUST-NOT-WIPE (a
load-or-default joined with RMW silently wipes the store on next save) · L-C3
IDEMPOTENT-SEEDERS (re-runs must not inflate counters that trust feeds) · L-C4
NO-SILENT-TIER-FALLBACK (unresolved steer targets fail loud, never default tier
and post) · L-C5 UNLOCKED-RMW-ON-SHARED-PREFS.

**Indirect connections (the 13,444-indirect-pairs thesis, in findings form).**
HOT: reverse_map demotion <-> the driving-ladder rib (judgment never silently
rides flash) · contract path divergence <-> the AGENTS.md WSL/Docker client rows
(read_first contradicts the WSL row). COLD: chain_query ts-compare <-> riblive1
U3 L3 (preload_selector missing-ts recency collapse: same disease family,
independently discovered on two surfaces; the LAW is the connection) ·
preferences wipe <-> matrix X04 (switchboard_v2 corrupt-line silent drop: the
silent-state-loss family spans hot and cold terrain) · switchboard v1
_resolve_peer -> _live_peers -> orchestrator/router/seat_registry (the finding
names the live coupling between the dormant v1 and the spine).

## 5. VERDICT: COLD-PAYS (narrowly, composite 297 vs 279; the raw-cluster axis
is a statistical tie inside the confounds)

The Heart of Gold LIVES AS POLICY, in exactly the two-regime form the spec
wrote: route by heat, sample by cold. It does NOT live as a replacement for the
GPS gradient: the hot arm kept paying on fifth-review files (5 new verified
clusters, including the steer_seal payload leak and the tier-demotion hole).
What cold bought that hot could not: law-class yield (5 vs 3) and cross-surface
connections (3 vs 2), at 6 new clusters on the estate's unreviewed SPINE for
four and three-quarters cents. The operator's "not falsifiable" objection is
answered by this run: the policy printed a number, the number cleared the
composite bar, and the falsifier is now cheap and repeatable.

## 6. Honest confounds (read before quoting the verdict)

1. **Selection bias, named: cold files may be cold because boring.** Partial
   control applied: cold picks are 12-to-62-importer load-bearing organs, not
   demo orphans (visitation measured REVIEW visits, not importance). A fairer
   trial: size- and churn-matched hot/cold pairs, several independent 10-file
   draws per arm, and blind grading by a seat that does not know which arm a
   cluster came from.
2. **Empty-bank asymmetry.** Cold files had nothing to exclude; hot had 4
   clusters excluded as known. If either unsettled hot lead (confirm-budget
   snapshot, /api/ps timing) settles as novel, hot's count rises to 6 and the
   raw axis widens; the composite stays inside noise.
3. **Cost/size asymmetry.** Cold carried 1.6x the chars (orchestrator 80K);
   per-dollar normalization is the mission's metric, but bigger inputs change
   finding odds per ask in both directions (more surface, more diluted cites:
   the 2056-line orchestrator itself produced 0 REAL clusters, single-family
   UNIQUE claims only).
4. **Hot pre-selection for defect density** (triple violators + matrix
   surfaces) inflates hot's re-report burden (excluded) yet hot still won the
   raw cluster axis: hot veins persist under re-mining.
5. **Contract boilerplate lie.** "This file already carries three KNOWN wiring
   violations" is false for the clean cold files; identical across arms so the
   A/B stands, but absolute cold yields are mildly deflated (families spent
   defect slots on the named organs).
6. **Two of ten cold slots were divergence-marked, not coldest.** policy_engine
   paid 3 asks for 0 REAL (the unsettled pairs are intent questions, as the
   matrix ruled); switchboard v1 paid the trial's richest cluster. The mission
   mandated the mix; the confound cuts both ways and is priced in.
7. **Single trial, single grading seat, N=10 per arm.** A one-cluster swing
   flips the raw axis; the verdict rests on the composite and the law/connection
   axes, which both point cold.
8. **Kimi rides prepaid Nous credits** ($0 metered); worst-case list pricing
   puts the trial at ~$0.22, still under cap.

## 7. Artifacts

- This receipt: watch/inbox/model_garden/COLD_HOT_RESULT.md
- Runs: watch/inbox/model_garden/coldhot-hot/, coldhot-cold/ (manifest.jsonl
  sha-stamped, asks/, raw/<family>/, rollup.json)
- Census + helper: coldhot_visit_census.json, coldhot_select.py (this directory)
- Usage: memory/runs/model_garden/usage.jsonl rows coldhot-hot-*/coldhot-cold-*
- No commits. $0.0829 metered. No em-dashes.

Lane COLD-1 seat, 2026-10-01.
