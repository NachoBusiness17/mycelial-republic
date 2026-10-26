# PARABLE-AS-SIGNPOST - smallest build + dogfood (2026-10-23, times EDT)

## Paths found (read-only)
PC repo C:\Users\foste\Documents\projects\local_sovereign_agent (branch mag/run-beta1-factory-build-audi-20260806T231709Z):
- MCP server: mag/mcp_server.py (SERVER_INFO name "mag-tool-map" - a TOOL map, not a parable map), mag/mcp_http.py, mag/mesh/door.py (MCP door: search/get_by_hash/propose_write/verify_chain).
- MCP registry drafts: watch/inbox/burn_reset_20260927/flash50/{mcp-registry-design.md, mcp_registry.sample.yaml, mcp_registry_check.py, mcp-mapbox.md}; watch/inbox/fifty_wide_20260917/FW07_mcp_index.md; configs/tools/mcp_pin.json (GitHub).
- Keys: canon/same_book/KEY_V1.md, canon/same_book/KEY_V3.json, canon/same_book/KEY_MASTER_ORCHESTRA.json, canon/same_book/THE_ORCHESTRA_OF_THE_HOUSE.md (all marked WITHHELD FROM PLAYERS).
- PUBLIC DOOR: canon/same_book/door/PUBLIC_DOOR.md (sha256 c1b3876c..., byte-identical to GitHub mag-public).
- Parable ledger: campaigns/parable_ledger_capture/module.json; watch/inbox/PARABLE_LEDGER_ERRATUM_R5_20261010.md.
- Parables: corpus/canon/THE_PARABLE_OF_THE_FIELD_AND_THE_STONES.md, docs/ref/THE_PARABLE_OF_THE_MOVING_WALL.md, docs/templates/FRONT_DOOR_TEMPLATE.md, canon/same_book/door/{THE_WELL_AND_THE_JARS,THE_HOUSE_THAT_RAN_ITSELF,THE_SPORE,ELI5,LEVEL12,GROW_YOUR_OWN}.md, watch/inbox/parables/scarecrow_20261012/, watch/inbox/hermes_burn/N1R_parables_songmap.md.
- GitHub standing-wave head 8cf2520eafeb0154d524b20bfae09a822f19e97e; README line 3: "Compiled 2026-10-16 from 60 rib files, 675 invariants, twelve cards" - CONFIRMED 675. (Branch tree has only README.md.)
NOT FOUND: (a) any "quanta-sized parables already mapped" store; (b) any parable->MCP wiring; (c) any file identifiable as "door gate v1 model" (searched names + git grep for door_gate/gate_v1; nearest: tools/door_reply_grader.py, mag/mesh/door.py, mag/canon_gate.py - none emits pass/block/hold for the door).

## Format spec (parable_signpost.v0)
1. BEACON <=~200 B, one line, pipe-separated: ID | title | rule digest | `HOLD->lookup <ns>:Lxx` | `ask:<who>`. (BEACON.txt = 190 B.)
2. RULE CARD <600 tokens (here ~257 words): `ID | rule | what to DO | lookup ID`, one per rule, plus an FP (false-premise) line.
3. FETCH RULE: PASS/BLOCK -> no fetch; HOLD -> resolve the gate's listed IDs; still unsure -> ask the operator.
4. WHERE/WHO: canonical URL, quanta store, operator.
5. DEPTH section for frontier models (mechanisms, drifts, cross-links). Small models may stop before it.
Quanta (quanta.json, parable_quanta.v0): {id, law, scene (VERBATIM sentences), sentences[a,b], drift, source URL, source_sha256}. Pointer IDs `pd1:L01..L10`, `pd1:FP`.

## Files built (new only)
PUBLIC_DOOR_SIGNPOST.md, BEACON.txt, build_quanta.py, quanta.json (11), signpost_lookup.py (CLI + stdio MCP stub, tool parable.resolve; scenes load only on HOLD), door_gate_v1_signpost.py (NEW reference stub - no original found to copy), gate_demo_answers.json, PROMPT_3B.txt, run_3b.py, DEEPSEEK_PROMPT.txt, ds_call.py, src_PUBLIC_DOOR.md/src_story.txt (copies), raw/.

## 3B (qwen2.5:3b-instruct, Ollama, temp 0, ~3 min)
Listed all 11 rule IDs correctly; PASS -> no fetch (correct); still unsure -> ask Nacho (correct). On HOLD for "rewrite the torn page" it named pd1:L03 + the command - correct primary pointer but missed pd1:L08 (the gate emits both). Basics: yes. Pointer: partial. Raw: raw/qwen3b_output.md.

## DeepSeek (ONE call, direct key via tools.ds_workhorse.load_key, not Hermes)
Requested deepseek-reasoner, max_tokens 65536; API reported model "deepseek-flash"; 1746 in / 6772 out (5965 reasoning); 11:58:39-11:59:21 EDT.
Judged all three gate verdicts correct; followed Q4 pointers and answered from quanta only, citing pd1:L03 s30-31 + pd1:L08 s39; said the L03->L08 drift/cross-link note is accurate. Critique: the beacon is not enough alone because `Lxx` is a placeholder and it doesn't say PASS/BLOCK = no fetch. Suggested: `gate=HOLD? resolve exactly its listed pd1:* pointers; PASS/BLOCK? no fetch; unresolved? ask Nacho`. Raw: raw/ds_content.md, ds_reasoning.md, ds_meta.json.
Build note: the first gate run gave Q4 a false PASS (keyword "rewrit" was on the hit list); fixed before any model call.

## Open decisions for Nacho
1. Which file is "door gate v1 model"? None found; built a new stub instead of copying.
2. The signpost edition reveals rules that KEY_V1 marks as withheld. It is kept separate and labeled not-the-exam. Should it be published at all?
3. KEY_V1 vs public story drift: L06 (count vs declare ignorance) and L07 (warm board vs ash/wet pen). Which wins?
4. Adopt DeepSeek's beacon fix? It costs about 40 B more.
5. Where should quanta live as an MCP server: in mag/mesh/door.py (get_by_hash) or as a standalone parable-signpost server?
6. The API served deepseek-flash for deepseek-reasoner. Is that acceptable as "max reasoning"?
