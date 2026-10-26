# STEERING v2 — design (paper only)
2026-10-23, written about 11:55 AM EDT. DESIGN ONLY: nothing built, no configs changed, no git writes, no model or API calls.
Tags: **[F]** = seen on disk this session (path checked, or a line quoted). **[B]** = from box research notes (`/workspace/salon_research_20261023.md`, `/workspace/standing_wave_gate_research_20261023.md`, `/workspace/door_invariant_20261023/`). **[P]** = paper claim / proposal, with no evidence yet.
Repo root = `C:\Users\foste\Documents\projects\local_sovereign_agent` (LSA).

## 0. Steel inventory (reuse, don't rebuild)
| organ | path | status |
|---|---|---|
| salon runner v4 | `LSA\watch\salon_runner.py` | [F] exists; v4 docstring per [B] |
| local playbook | `LSA\mag\local_playbook.py` + `LSA\configs\local_playbooks.yaml` | [F] |
| DeepSeek workhorse | `LSA\tools\ds_workhorse.py` | [F] |
| cheap swarm dispatch cap | `LSA\mag\cheap_swarm.py`: `DEFAULT_MAX_PER_DAY = 6`, `dispatch(pkg, max_per_day=...)` returns `"daily_cap"` | [F] |
| renderman.py | `LSA\mag\renderman.py` (+ `mag\renderman_ask.py`, `memory\runs\renderman_specs\`) | [F] docstring: "Lazy evaluation → lazy model routing" |
| rib bus | `LSA\mag\rib_bus.py` (siblings rib_cache/rib_store/rib_renderer per [B]) | [F] |
| dirac_loop.py | `LSA\mag\dirac_loop.py` (+ `tools\dirac_loop_shim.py`) | [F] |
| the 100 Ractor act | `LSA\watch\inbox\foreign_seats\CONGRESS_ACT_100_RACTOR_ORGAN_20261022_17d5cc59.md` (companion: `THE_100_RACTOR_TESUJI_MOONSHOT_RESEARCH_DIRECTIONS_20261022.md`) | [F] filename only; body not read |
| congress charter | `LSA\canon\congress\CHARTER.md` | [F] |
| phone_door.py | `LSA\mag\phone_door.py` | [F] |
| cache_identity.py | `LSA\mag\cache_identity.py` | [F] |
| behavior cards | `LSA\tools\behavior_cards_x.py` (rib translation: `watch\inbox\babelfish_selfmine_20261010\RIB_TRANSLATED_rib_behavior_cards_20260928.md`) | [F]. No standalone card *store* dir found |
| Water Governor | `LSA\tools\water_governor.py`, ledger `LSA\memory\runs\water_governor\usage.jsonl` | [F] |
| parable-signpost (parallel job) | `LSA\watch\inbox\parable_signpost_20261023\` | **NOT FOUND** as of 11:50 AM EDT. This design only references it and does not define its contents |
| quanta parables / MCP map | — | **NOT FOUND** in this pass (location is an open decision) |
| Racter feed | `LSA\watch\inbox\ractor_parables_20261023\` (build.py, run_lane.py, door_story.md, SUBJECT_BRIEFS.md); `mag\ractor_selfsteal_seeds.py`, `mag\ractor_corpus.py`; box `/workspace/door_invariant_20261023/racter.py, RACTERED.md` | [F] |

## 1. Beacon format
The parallel job owns the beacon spec. v2 consumes only this envelope [P]:
`{"b":<beacon_id>,"card":<rule_card_id>,"q":[<quanta pointer ids>],"sha":<sha256 of card bytes, 12 hex>,"tip":<corpus_tip_hash>}`. The envelope is ~200 bytes, deterministic, and has no wall clock (this follows the `tools/regen_front_door.py` determinism law [B]).
- The beacon parable is the hook, carried in a `note`. The rule card (<600 tokens) is the spec. Quanta parables are expanded **only on a hold** (delayed read).
- If the signpost files land with different field names, v2 adapts to them. It does not fork a second format.

## 2. Routing ladder (LOD: compact at the frontier, expand at the cheap end)
Every item enters at R0 and climbs only on a trigger, so each rung is lazy (renderman "only compute visible").
| rung | engine (reused) | does | escalate when |
|---|---|---|---|
| R0 regex | `scripts/inbox_librarian.py`-style shelf + beacon sha check [B] | parse the envelope, verify the card sha, match a deterministic rule | no rule matched, sha mismatch→**block**, or the match is ambiguous (more than one shelf) |
| R1 3B | `qwen2.5:3b-instruct` via the local_playbook shape, temp 0, num_predict ≤120, cached prefix (cache_identity) | classify against the rule card into an output shape `{id,verdict,rule,conf}` | an output without its id is void (ds_workhorse law), conf < threshold, verdict=hold, or the card says "needs quanta" |
| R2 7B on hold | `qwen2.5:7b-instruct-q8_0` + delayed-read of the quanta parables (RIB DelayedReadArchive pattern, rib_bus/rib_cache) | re-judge with the expanded quanta | R1 and R2 disagree, the item touches estate laws/canon, or conf is still low |
| R3 frontier | salon_runner v4 blind lanes plus a verifier seat (DeepSeek via ds_workhorse / salon_openclaw), capped by cheap_swarm `max_per_day` | attack, don't validate: probe → Socratic return → fold → verifier grades tri-state gradable claims | verifier disagrees or the cap is hit → **escalated** to Nacho / Congress committee queue |
The frontier gets only the compact card plus the claim (compact at the frontier). The cheap rungs get the full quanta (expand at the cheap end).

## 3. Governor banking
Every hop writes one row through the existing `_bank(beat, tank, model, ok_api, ok_material, latency_ms, note)` [F]. v2 adds fields carried **inside** `note` or as a proposed additive extension (open decision D2):
`{"beat":"steer_v2","tank":"regex|ollama|deepseek|openrouter_free|...","model":..., "item":<id>,"rung":"R0..R3","outcome":"passed|block|hold|escalated","beacon":<b>,"card_sha":..,"parent_row":..}`
**Conservation check** (per beat, plus over the ledger in `report`): for each rung, `items_in(r) = passed(r)+block(r)+hold(r)+escalated(r)`. Also `escalated(r) = items_in(r+1)`, and holds resolve into a later row, or the item stays open and is listed. Any open item without a row means the beat fails. This generalizes today's `conservation_ok = dispatched == banked` [F].

## 4. Racter parable feed-in
The Racter lanes (`ractor_parables_20261023\run_lane.py`, box `door_invariant_20261023/racter.py`) produce parable candidates [F]. v2 treats them as **untrusted input at R0**. Each candidate gets a provisional beacon, is graded blind by R1/R2 against the rule card it claims to teach (the PUBLIC_DOOR "teach without stating, we hold the answer key" pattern [B]), and is promoted to the quanta pool only on pass. The 100 Ractor act (Congress) is the authority that admits it (body unread; open D5).

## 5. Self-steal fold-back loop
Mouthpieces: DeepSeek, Argon/Gemini, Claude, ZAI Fostertron Max, Nacho Business Corp Lite, Ollama.
1. **Steal**: each mouthpiece's R3 replies plus its own past outputs (`mag/ractor_selfsteal_seeds.py` pattern; box `selfsteal/`) are harvested as claims.
2. **Strip**: keep only tri-state gradable claims carrying an item id.
3. **Cross-grade**: every claim is graded by a *different* mouthpiece seat (the verifier never grades its own lane).
4. **Fold**: survivors become rule-card diffs or new quanta. A card diff changes the card sha, so beacons re-issue.
5. **Bank**: one row per steal/grade/fold, with `beat:"steer_v2_fold"`, conserved the same way.
Browser-only mouthpieces (Gemini/Claude UI) enter by paste-back into `watch/salon_inbox/` (salon_runner door B) [B]. Otherwise they stay off-ledger.

## 6. Phases (smallest first, paper effort)
| # | deliverable | files to touch (new unless noted) | reused organs | hrs | done-test |
|---|---|---|---|---|---|
| P0 | Governor dry ledger: outcome-enum rows + 4-way conservation in report | `tools/water_governor.py` (additive `report` check) or new `mag/steer_bank.py` | water_governor `_bank` | 2 | replaying a 20-item fixture banks 20 in, and the sum of outcomes equals 20 per rung; one dropped row makes report fail |
| P1 | R0 regex rung + beacon envelope reader | `mag/steer_v2.py`, `configs/steer_v2_rules.yaml` | inbox_librarian, regen_front_door determinism | 3 | fixture: a sha mismatch→block, a known pattern→pass, an unknown→escalated; byte-identical output across 2 runs |
| P2 | R1 3B playbook against one rule card | `configs/local_playbooks.yaml` (+1 playbook), steer_v2.py | local_playbook, cache_identity, ds_workhorse laws | 4 | 50 labelled items: id-less outputs = void and counted; 2nd-run prefill shows cache re-light; agreement with labels is reported (no threshold claimed yet) |
| P3 | R2 7B hold with delayed-read quanta | steer_v2.py, adapter to rib_cache/rib_bus | rib_bus, renderman lazy routing | 4 | holds resolve to a later row; quanta bytes are read only for held items (counted) |
| P4 | R3 frontier salon + verifier, capped | small adapter calling salon_runner v4 | salon_runner, cheap_swarm cap, ds_workhorse | 5 | an over-cap item lands as `escalated`, not dropped; verifier rows are banked; tri-state matrix produced |
| P5 | Racter feed-in | adapter to ractor_parables run_lane output | racter.py, ractor_selfsteal_seeds | 3 | 10 Racter candidates all banked; only passed ones reach the quanta pool |
| P6 | Self-steal fold-back across mouthpieces | `mag/steer_fold.py` | salon_inbox door B, selfsteal seeds, dirac_loop (optional cycle check on the claim graph) | 6 | one card diff from cross-graded claims → new sha → beacons re-issue; fold conservation holds |
| | **total** | | | **~27 h** | |

## 7. Risks
- The signpost format isn't on disk yet, so the beacon fields could drift between the two jobs.
- 3B false-pass would leak past R1. Mitigation (paper): sample passes upward to R2.
- Changes to the conservation schema could break existing `report` consumers of usage.jsonl.
- The cheap_swarm cap of 6/day may make R3 the queue bottleneck.
- Mouthpiece self-grading collusion. Browser seats are off-ledger.
- The quanta/MCP map location is unknown. The 100 Ractor act body hasn't been read, so its rules may conflict with this design.

## 8. Open decisions for Nacho (not decided here)
- D1 Where do the quanta parables and the MCP map live, and who owns their IDs?
- D2 Extend the `_bank` signature (additive fields) vs. pack the v2 fields into `note`?
- D3 R1 confidence threshold, and the sample rate of passes audited at R2.
- D4 R3 daily cap: keep 6, or give steer_v2 its own cap?
- D5 Does the 100 Ractor act / a Congress committee (Beacon? Experiment?) own Racter admission and card diffs?
- D6 Which mouthpieces count as verifier seats, and is Ollama allowed to verify frontier output?
- D7 Do card diffs from fold-back auto-apply or need operator sign-off?
- D8 Do holds expire (and to what outcome), or stay open indefinitely?
