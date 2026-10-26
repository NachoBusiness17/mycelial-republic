# Steal card: open-local-language-models (frontier fold 2026-10-07, round 1)

Three confirmed finds, all three primaries re-verified by this seat this round, not carried on the finder's word: the nimble benchmarks page fetched raw (HTTP 200, 38,286 bytes), the Ollama v0.34.3 release metadata via the GitHub API (200, 36,539 bytes), the X post resolved through the fxtwitter JSON door (200, 2,767 bytes), and the estate's own daemon probed live (version read, three POST /api/show calls). One arithmetic correction to find 1 is banked below: the table says 9 of 13, not 8.

## Steal 1 (primary-verified, closes a standing OWED): the Jev public-suite figures live on the vendor's own page

- Bytes on disk: `sweep/nimble_public_benchmarks.md`, sha256 360ddfccd33cc646731fc8a9eea5fafbae94d796122a3b41b9943f4de3b8c4f0. The find's quote verifies byte-true at `:48` ("No vendor-published public-dataset result for Jev exists."). `:12-13`: Bespoke-Nimble-9B and Jev 1.13.0 run on every subset, 3,880 records total, with a results section.
- The OWED this closes: `frontier_olm_2026-10-02/register.jsonl:22` banked the Ollama blog row with "13 datasets, 3,880 decisions, no figures published", and the 10-02 steal card restated it (`watch/inbox/frontier_olm_2026-10-02/steal/open-and-local-language-models.md:45-46`). The figures now exist estate-side.
- Results table `:380-394` (13 subsets, accuracy with 95% CI, agreement, exact McNemar p). Verified headline rows: nimble-9b's best subset is massive-en-US at 86.9% (82.9 to 90.0), `:387`, which straddles the estate's 0.880 sovereignty trigger (`mag/verb.py:490`, `:505`); nimble collapses to 39.0% (33.1 to 45.1) on rubric scoring, helpsteer2, `:385`; the overall row `:418`: nimble macro 74.8 / micro 75.9 vs jev 76.0 / 77.3.
- CORRECTION to the find: jev beats nimble on 9 of 13 subsets, not 8. The nine (jev accuracy above nimble accuracy): boolq `:383`, civil_comments `:384`, massive-de-DE `:386`, massive-en-US `:387`, paws `:389`, pubmedqa `:390`, squad2 `:391`, summeval-consistency `:392`, vitaminc-dev `:394`. The four losses: aegis2 `:382`, helpsteer2 `:385`, multinli `:388`, summeval-relevance `:393`.
- Mechanism for the estate: the 0.880 gate is not soft. The vendor flagship's single best subset sits at a point estimate under the gate with a CI that straddles it, and the vendor's own macro is 74.8. Any estate replica that clears 0.880 on its own labeled distribution is doing something the vendor's public suite does not show. Score-shaped cells are the weak class on both engines (helpsteer2 39.0 vs 34.1, agreement only 26.1%), so Fleet-Bench score rows carry the least signal per row.
- Estate organ: sovereign mirror. The trigger meter at `mag/verb.py:487-505` (drop hosted S1 API only at n>=40 AND accuracy>=0.880 over 7 days of Fleet-Bench rows) gains a calibration row from this table, plus the suite's grader discipline: Wilson intervals, exact McNemar on discordant records, family-complete accuracy, ECE and Brier (`:364-365`, `:416-418`) are the same vocabulary the estate's own weekly trigger wants.

## Steal 2 (executed on the estate daemon this round): per-model thinking controls are queryable, so the one-bug assumption becomes a fact

- Release body verified at `sweep/ollama_v0343_release.json:654`: "GET /api/show now advertises each model's thinking controls and default", with the gemma4 CLI example (levels false, true; default true) and the glm-5.3-flash:cloud API example (values low/high/max, default max). Scope note the find blurred: the glm-5.3-flash example is a cloud model ("Also available on ollama.com directly for cloud models", same body). No glm model is installed on this box (`sweep/local_api_tags.json`; the flash-family local name is frob/ling-3.0-flash:latest), so the glm figures stay release-example carried, never estate-measured.
- Local instrument re-read this round: GET /api/version returned {"version":"0.34.3"}, matching the 10-01 bank. Anchor correction: the find cited "steal line 31"; the byte-true lines are `frontier_olm_2026-10-01/steal/open-local-language-models.md:79` and `frontier_olm_2026-10-01/DIGEST.md:48`.
- Probe EXECUTED this round (bodies and responses in sweep/, hashes below): three POST /api/show calls.
  - gemma4: capabilities [completion, vision, audio, tools, thinking], and a structured block "thinking":{"values":[false,true],"default":true} (`show_resp_gemma4.json`), matching the release example.
  - qwen2.5:7b: capabilities [completion, tools]; no thinking key anywhere in the response (rg count 0, `show_resp_qwen25_7b.json`).
  - deepseek-r1:1.5b: capabilities [tools, thinking, completion]; capability advertised but no structured values/default block (`show_resp_dsr1_15b.json`).
- Mechanism: the one-bug law says omission of the thinking key is a MEASURED ON state (`memory/rib/RIB_MODEL_GATES_20261001.md:120`, `memory/rib/RIB_DEEPSEEK_ELDER_SEAT.md:189`). Until now that law ran on hand-curated knowledge; on daemon 0.34.3 the default is one localhost call away per model. `mag/agent_state_router.py:5` auto-selects model and thinking level, with hand-set entries at `:33` ("high") and `:45` ("none"). Port move: warm boot and seat boot call /api/show for each pinned model, bank the advertised values/default into the condition ledger, and every verdict row records the thinking condition read from the daemon rather than assumed.
- Estate organ: gopher fleet (seat config and the one-bug condition ledger). Three response shapes measured: structured default (gemma4), absent key (qwen2.5:7b), capability without defaults (deepseek-r1:1.5b); the port must handle all three, defaulting to "unknown, assume ON" on the absent-key shape, never to OFF.

## Steal 3 (vendor-claimed, cells UNMEASURED): qwen3.5 small rungs with native tool calling, one pull away

- Post verified verbatim through the fxtwitter door (`sweep/fx_ollama_2028514180936908842.json`): "The Qwen 3.5 small models are available on Ollama. All models support native tool calling, thinking, and multimodal capabilities in Ollama." with run commands for 9b, 4b, 2b, 0.8b and the library link. created_at "Mon Mar 02 16:54:03 +0000 2026" matches the find's 2026-03-02; the date is outside the 30-day candidate window and is named as such, exactly like the find did.
- Estate anchors, verified this round: tool and classify work routes through qwen2.5:7b and gemma:2b today (`mag/task_router.py:11,13`; `mag/lanes.py:45,48` clerk and router both gemma:2b); the one-hot VRAM law on the 6GB AMD host governs any new rung (`mag/ollama_policy.py:1-3`, `:56-87`, janitor pin at `:16`, qwen-desk in KEEP_ALIVE at `:18`). Qwen3.5-4B Q4_K_M 2.74 GB Apache-2.0 was verified live on 10-01 (`frontier_olm_2026-10-01/DIGEST.md:41`, abliterate lane) and the April quants comparison rode pre-window (`DIGEST.md:70`).
- Measured contrast this round: qwen2.5:7b advertises [completion, tools] and no thinking (`show_resp_qwen25_7b.json`). The qwen3.5 claim of native tools + thinking + multimodal in the 0.8b to 9b band is vendor text until an estate instrument fires; the cells stay UNMEASURED per the find's own framing and the instruments-only law.
- Estate organ: gopher fleet (the tool-calling rung) with a percolator candidate row; the A/B instrument is ToolCall-15, banked in the fold at `frontier_olm_2026-10-02/sweep/quantization-compression-x.md:125` (AlphaSignalAI, Apr).

## Estate map (organ per steal)

1. Sovereign mirror: calibration row + grader discipline for the 0.880 trigger (`mag/verb.py:487-505`).
2. Gopher fleet: daemon-read thinking conditions at seat boot (one-bug law, `mag/agent_state_router.py:5,33,45`).
3. Gopher fleet (tool rung) + percolator (candidate row): qwen3.5:4b arm vs qwen2.5:7b under the one-hot law.
Quantizer, context pack, and water graph are not fed by these finds (no quant recipe, no pack content, no cost or provenance-graph row); stated so no organ is padded.

## Probes

1. (EXECUTED this round) The /api/show read: three POSTs on the 0.34.3 daemon, results above, artifacts hashed in sweep/. Standing extension for the port: diff every thinking condition in `memory/rib/RIB_MODEL_GARDEN_ROUTING.md` and the agent_state_router entries against advertised defaults. Falsifier: any assumed default that differs from the advertised one is a latent one-bug and fires.
2. (Cheap, this week) Trigger calibration port: recompute the last 7 days of Fleet-Bench rows with Wilson intervals and exact McNemar against the rule floor. Falsifier: a trigger_ge_0880 verdict whose CI lower bound sits below 0.880 while its point estimate sits above it (the nimble table's 86.9 with CI 82.9 to 90.0 is exactly this straddle, so the estate should know which shape its own trigger verdict has).
3. (Gated on one pull) qwen3.5:4b vs qwen2.5:7b on ToolCall-15 items, same items both arms, one-hot enforced. Falsifiers, any one fires: a tool-contract failure, median latency above the qwen2.5:7b arm, or janitor eviction from VRAM.

## Evidence appendix (every check this round)

- Fetches: curl -sS to raw.githubusercontent.com/bespokelabsai/nimble/main/docs/PUBLIC_BENCHMARKS.md (200, 38,286B), api.github.com/repos/ollama/ollama/releases/tags/v0.34.3 (200, 36,539B), api.fxtwitter.com/ollama/status/2028514180936908842 (200, 2,767B), localhost:11434/api/tags (200, 7,466B). All saved under `watch/inbox/frontier_olm_2026-10-07/sweep/`.
- Live probes: GET /api/version -> {"version":"0.34.3"}; POST /api/show x3 (gemma4 via body file `show_body_gemma4.json`, qwen2.5:7b and deepseek-r1:1.5b inline bodies), all 200, responses saved. Extraction greps: thinking block in gemma4 only; capabilities arrays in all three; thinking-string count 0 for qwen2.5:7b.
- Hashes (sha256): nimble_public_benchmarks.md 360ddfcc..., ollama_v0343_release.json 20378f25..., fx_ollama_2028514180936908842.json 8b77b0d2..., local_api_tags.json d3134ae5..., show_resp_gemma4.json fa2169ed..., show_resp_qwen25_7b.json 12a2d053..., show_resp_dsr1_15b.json 9d5dd355... (full digests in the sweep dir listing).
- Anchor verification: rg over `frontier_olm_2026-10-01` (0.34.3 at steal `:79`, `:197`, DIGEST `:48`; Qwen3.5-4B GGUF at DIGEST `:41`; April quants at `:70`), `frontier_olm_2026-10-02/register.jsonl:22` (the OWED-figures blog row, read whole via PowerShell index), `mag/verb.py:478-505` (Read), `mag/ollama_policy.py` (Read, whole), `mag/task_router.py:11,13` and `mag/lanes.py:45,48` (rg), one-bug texts at `memory/rib/RIB_MODEL_GATES_20261001.md:120` and `RIB_DEEPSEEK_ELDER_SEAT.md:189` (rg), `mag/agent_state_router.py:5,33,45` (rg), ToolCall-15 at `frontier_olm_2026-10-02/sweep/quantization-compression-x.md:125` (rg).
- Overlap: rg -l -i "bespokelabsai|PUBLIC_BENCHMARKS" over catalog/catalog.jsonl, both prior frontier_olm sweep dirs, and memory/percolator exited 1 (zero hits); same for "api/show" over both steal dirs and memory/percolator. The find's zero-overlap claims verify.

## OWED

- qwen3.5 cells UNMEASURED: no pull, no ToolCall-15 run this round; the vendor capability claim is untested estate-side.
- glm-5.3-flash: release-example (cloud variant) only; not installed locally, so its low/high/max default is not estate-measured.
- Fold-editor note: find 1's "8 of 13" corrected to 9 of 13 from the table bytes; find 2's "steal line 31" anchor corrected to `:79`/DIGEST `:48`.
- fxtwitter is the mirror door (house recipe); the x.com primary itself was not fetched directly.
- The nimble page is a mutable main-branch document; the sha256 above pins the version these figures were read from.
