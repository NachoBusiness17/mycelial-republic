# MASTER FOLD - MICKEY-17 v2.1 - run port-debt-20261011

- folded_at: 2026-10-12T11:17:18Z (fold script sha256 58bd72c79c6d). Every number in the verbatim sections below was computed by that script from the lane archive at `memory/runs/mickey17_v2/runs/port-debt-20261011/lanes`. The fold seat wrote the prose around them; quotes are copied from the lane rows; every steal sentence carries its lane id and row index.
- Sources read this fold: `FOLD_SECTIONS.md` plus all six lane files (`single-judge-gate-invariant.json`, `cloud-suffix-refuse.json`, `schema-placement-law.json`, `cap-draw-range-invariant.json`, `heal-log-drain.json`, `kv-env-contract.json`) and their six persisted checks files in the same directory (twelve deep_tier2 checks across them).
- Fold-seat checks run this ask (script `fold_join_check_20261012.py` on the repo venv, temp copy): scoreboard recount from lane bytes matches the script exactly (28 rows; executed 24 / executed-with-deviation 3 / blocked 1; leverage high 14 / medium 12 / low 2); the deep_tier2 row_key join replicates at 11/12 with the miss identified (see EXECUTIONS preamble); the script's one normalized cross-lane duplicate quote reproduces as the pair `cap-draw-range-invariant#3` / `heal-log-drain#4` (the same ratchet summary line, filed by both lanes as shared sibling-debt evidence).
- Revision 2026-10-12, post-critique (fold-seat edits, no script-computed number changed): the sources-read line's checks-file count corrected - byte recount reads six `.checks.json` files in the lanes directory carrying exactly twelve `"verdict"` entries, all verified, so the old "twelve persisted checks files" was a file/verdict conflation; negative reason 7 now records the 4-vs-5 GROWTH-claim disagreement between its two sources (cap-draw-range-invariant#3 vs heal-log-drain#4) instead of silently printing cap's 4; register row 6 re-marked as an operator one-command `baseline-update` accept because three findings across three files cannot fit one seat one sitting.
- Copies: estate `corpus/steal/MASTER_PORT_DEBT_20261011.md`; workspace `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_PORT_DEBT_20261011.md`.

The run in one paragraph: six lanes fired at the port debt named by the 2026-10-11/12 frontier steal cards (kv-cache context engineering, open-local language models, inference efficiency). All six landed parseable archives. Two laws were minted into the percolator register (no single judge gates waste; caps sit above the family draw range). One refusal law landed in verify_pins with its two tests. One schema-placement law landed in the context freeze. One heal-log drain landed in the knowledge-graph build and cured the live estate graph. One fleet env contract was set on the janitor Ollama service and verified trust-bytes. Twenty-seven of 28 rows executed (three with filed deviations); one row blocked.

## CASUALTY HEADER (script, verbatim)

- fired: 6
- landed (parseable files): 6
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## SCOREBOARD (script, verbatim)

- rows: 28
- estate_status: executed 24, executed-with-deviation 3, blocked 1
- leverage: high 14, medium 12, low 2

## PRISMA FLOW (script, verbatim)

- identified: 28
- screened: 28 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 28
- invariant: identified == included + excluded **HOLDS** (28 = 28 + 0)

## EXECUTIONS (script TOP-K, proof quotes attached)

Preamble, verification ledger. The script computed twelve top steals, all leverage high. Behind them sit the persisted verdicts: fidelity 28/28 rows with quote, source, steal and estate_status non-empty (100.0%); 28 supports votes splitting 23 yes / 5 no (every no names quote insufficiency - `single-judge-gate-invariant#0`, `#1`, `#3`, `heal-log-drain#4`, `kv-env-contract#3` - and none names a false execution); 12 deep_tier2 byte-checks, all 12 verdict verified, joining to lane rows at 11/12. My prefix-join replication this fold identifies the single join-miss as `cloud-suffix-refuse#1`: the deep check's row_key reads "Two tests added (lines 182-219)" while the lane claim reads "Two tests added in the digest-pins section (lines 182-219)", so the key does not prefix-match; the row itself is deep-verified (its assert byte-found at `tests/test_pin_digest_thinking.py:199-201`), which is why the script labels the miss verified, no exclusion weight, not fatal. Two further lane-claimed high rows sit outside this list; they file DISPUTED at the end of this section.

### The twelve

**1. [high] cap-draw-range-invariant#0 - the cap law minted.** The cap-above-draw-range law is minted into the percolator register through its own sanctioned writer (atomic replace, LAW-065 receipt; rows 674 -> 675 on disk): caps must sit above the model family's measured reasoning draw range, family-conditional, glm-5.3-flash excepted at any cap; source key `steal-inference-efficiency-cap-draw-range` matches the sibling steal-mint precedent [cap-draw-range-invariant#0]. Proof quote:

```
"a10175ab487448b4": { "text": "caps must sit above the model family's measured reasoning draw range, family-conditional: glm-5.3-flash emptied at ANY max_tokens cap (2600/4200/9000/16000, rib census 2026-10-01)
```

Verification: supports yes; deep_tier2 verified (register entry byte-found in `memory/percolator/invariants.json`; 675 rows counted; the LAW-065 receipt timestamp equals the minted record's first_seen to the second).

**2. [high] cap-draw-range-invariant#1 - the same law filed beside the terminal check.** A 14-line law comment landed at `mag/inference_budget.py:309-322`, immediately upstream of the EMPTY_REASONING terminal return, naming the invariant key, the outside cap-2000-vs-8000 measurement, and the glm-5.3-flash any-cap census exception; comment-only, no behavior bytes changed, module imports clean [cap-draw-range-invariant#1]. Proof quote:

```
# CAP-ABOVE-DRAW-RANGE law (percolator invariant a10175ab487448b4, minted
    # 2026-10-12): the preventive half upstream of this terminal check.
```

Verification: supports yes; deep_tier2 verified (comment spans exactly :309-322; git diff shows a comment-only +14 hunk; venv import check printed IMPORT_OK with unchanged terminal classification).

**3. [high] cloud-suffix-refuse#0 - the refusal law landed.** Cloud-suffix REFUSE landed in verify_pins: a `CLOUD_SUFFIX` constant plus `_is_cloud_tag` helper (lines 85-90) and a refusal scan (lines 186-191) that refuses any tag carrying `-cloud` found in either the pin config or the daemon's installed inventory, with reason `cloud_suffix`; refusal rows carry expected/actual as None so the CLI refusal printer cannot KeyError [cloud-suffix-refuse#0]. Proof quote:

```
for tag in sorted({*pins, *installed}):
        if _is_cloud_tag(tag):
            refused.append({"tag": tag, "expected": None, "actual": None,
                            "reason": "cloud_suffix"})
```

Verification: supports yes; deep_tier2 verified (quote byte-identical at `mag/ollama_policy.py:188-191` by sed+diff; the printer's direct indexing of both keys read in bytes).

**4. [high] cloud-suffix-refuse#1 - the two asked tests.** `test_verify_pins_cloud_suffix_refuses` pins DESK_DEFAULT to `gpt-oss:120b-cloud` with the daemon listing it and asserts ok False with exactly one `cloud_suffix` row naming the tag; `test_verify_pins_clean_tags_pass` keeps the gate open on all-clean pins and inventory; daemon HTTP mocked per the file's house pattern [cloud-suffix-refuse#1]. Proof quote:

```
cloud = [r for r in out["refused"] if r["reason"] == "cloud_suffix"]
    assert len(cloud) == 1
    assert cloud[0]["tag"] == "gpt-oss:120b-cloud"
```

Verification: supports yes; deep_tier2 verified (asserts byte-found at `tests/test_pin_digest_thinking.py:199-201`; git diff shows both tests as additions; the deep row_key prefix-join miss on this row is wording drift only, per the preamble).

**5. [high] heal-log-drain#0 - the drain is the last step before the write.** build() gains the heal-log drain: it re-applies authored why_context edges from the newest graph_heal heal log, idempotent by sha256 edge id over from/to/text, dangling endpoints dead-lettered to `heal_drain_dead_letters.jsonl` (append-only merged by edge id) instead of vanishing. Filed deviation: the Mimosa security hook blocked the first candidate (sha1 weak-crypto, open-with-variable-path traversal); the landed code carries sha256, a `_contained()` ROOT-escape guard, and the module's tmp-twin + os.replace pattern [heal-log-drain#0]. Proof quote:

```
    # m7-heal-log-drain (2026-10-12, port-debt-20261011): the LAST step before
    # the write. Re-apply the authored why_context edges the newest heal log
    # mirrors, so a rebuild restores manual weaving instead of wiping it (the
    # 117 -> 0 wipe documented at the drain section above); dangling endpoints
    # dead-letter instead of vanishing. Idempotent by edge id: the second
    # build replays the same log rows onto a freshly regenerated edge set and
    # lands the same edges again, never duplicates.
```

Verification: supports yes; deep_tier2 verified (quote byte-match at `mag/knowledge_graph.py:770-776`; only graph-dict assembly sits between drain and write; no sha1 anywhere in the file).

**6. [high] heal-log-drain#2 - the live cure proof.** kg.build() run twice on the real estate graph: before, zero why_context edges in `memory/knowledge_graph.json` with all 117 only in the heal log; after, 96 restored and 21 dangling log rows (knot ids no longer in the rebuilt node set) dead-lettered; the second build byte-identical in edge-id set with total edges stable at 1237 [heal-log-drain#2]. Proof quote:

```
BUILD1: edges=1237 why_context=96 log_rows=117 restored=96 dup_skipped=0 dead=21 malformed=0
BUILD2: edges=1237 why_context=96 log_rows=117 restored=96 dup_skipped=0 dead=21 malformed=0
```

Verification: supports yes; deep_tier2 verified (persisted file holds exactly 96 why_context occurrences across 96 unique ids; heal log 117 rows; dead-letter file 21 rows whose id set equals an independent re-simulation of the drain's classification logic).

**7. [high] kv-env-contract#0 - the env contract persisted.** `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_DEBUG=1` persisted REG_SZ in HKCU\Environment, joining the five prior OLLAMA_* keys; new shells and relaunches inherit it [kv-env-contract#0]. Proof quote:

```
OLLAMA_FLASH_ATTENTION    REG_SZ    1
    OLLAMA_KV_CACHE_TYPE    REG_SZ    q8_0
    OLLAMA_DEBUG    REG_SZ    1
```

Verification: supports yes; deep_tier2 verified (reg query byte-match; PowerShell property listing cross-checks exactly eight OLLAMA_* names).

**8. [high] kv-env-contract#1 - the restart carried it.** The janitor Ollama service restarted under the full eight-var contract (old PID 27208 killed 2026-10-12T10:17:48Z, new PID 29280); the new instance's own startup dump names the flipped values against the old instance's `false`/empty [kv-env-contract#1]. Proof quote:

```
OLLAMA_FLASH_ATTENTION:true OLLAMA_GO_TEMPLATE:true OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://0.0.0.0:11434 OLLAMA_IGPU_ENABLE: OLLAMA_KEEP_ALIVE:10m0s OLLAMA_KV_CACHE_TYPE:q8_0
```

Verification: supports yes; deep_tier2 not persisted for this row (persisted checks cover kv row 0 only).

**9. [high] kv-env-contract#2 - the trust-bytes accept gate passed.** With OLLAMA_DEBUG=1, llama-server launched with `--cache-type-k q8_0 --cache-type-v q8_0` and the engine log names the loaded cache type per side plus flash_attn enabled; 76.50 MiB total at 8192 ctx matches the q8_0 halving arithmetic derived from the named per-side bytes [kv-env-contract#2]. Proof quote:

```
llama_kv_cache: size =   76.50 MiB (  8192 cells,  18 layers,  1/1 seqs), K (q8_0):   38.25 MiB, V (q8_0):   38.25 MiB
```

Verification: supports yes; deep_tier2 not persisted for this row.

**10. [high] schema-placement-law#0 - only stable schemas enter the freeze hash.** The schema-placement law landed in the A2 freeze: a DYNAMIC_TOOL_SCHEMA_NAMES registry, `register_dynamic_tool_schemas`, and `split_tool_schemas`; freeze_system_prompt now hashes only the session-stable half and records kept-out dynamic names in `dynamic_schema_names`, so dynamic schema bytes can never flip the prefix hash or refreeze a session [schema-placement-law#0]. Proof quote:

```
Schema-placement law: the hash covers only SESSION-STABLE schemas. Schemas registered dynamic (register_dynamic_tool_schemas) are dropped from the frozen block and the hash entirely
```

Verification: supports yes; deep_tier2 verified (quote contiguous at `mag/context_pack.py:1057-1059` under whitespace normalization; split at :1070, stable-only hash input :1071-1077, dynamic_schema_names :1081 all read in bytes).

**11. [high] schema-placement-law#1 - dynamic schemas render in the tail.** A new `dynamic_tool_contracts` renderer (name + description + canonical parameter JSON, deterministic, 2400-char cap) is wired into `evolving_tail(dynamic_tool_schemas=...)` behind a "## Dynamic tool contracts" section, so mid-session churn renders as plain-text contracts and never touches the frozen prefix [schema-placement-law#1]. Proof quote:

```
dynamic_tool_schemas: dynamic (mid-session-churning) tool schemas render here as plain-text contracts (dynamic_tool_contracts), never inside the frozen prefix (schema-placement law).
```

Verification: supports yes; deep_tier2 verified (quote byte-match at `mag/context_pack.py:1104-1106`; renderer and wiring runtime-checked in-process, deterministic render and freeze-drops-dynamic both true).

**12. [high] schema-placement-law#3 - the churn test.** The new test `test_mid_session_dynamic_schema_change_lands_in_tail_without_refreeze` registers `mcp_live_probe`, proves dynamic bytes excluded from `tool_schemas_text`, proves hash-independence (stable half + dyn_v1 vs dyn_v2 give the same prefix_hash), proves the mid-session flip returns the cached frozen object (f3 is f1, no refreeze) and lands the v2 contract in the tail [schema-placement-law#3]. Proof quote:

```
assert '"version": 1' in tail_v1 and '"version": 2' in tail_v2
```

Verification: supports yes; deep_tier2 verified (test def at `tests/test_context_freeze.py:185`, quote at :259; the verifier re-ran the single test: 1 passed in 4.68s).

### DISPUTED (2)

The script's rule: a lane-claimed top steal outside the TOP-K list files as DISPUTED. Two rows carry lane-claimed high leverage outside the list - `single-judge-gate-invariant#0` and `single-judge-gate-invariant#1`. In both cases the dispute is quote sufficiency, not execution truth: the supports verifier voted the row 0 quote "proves the law text was composed, not that the percolate() compile path was executed with those metadata" and the row 1 quote "a bare off-by-default assertion fragment" showing none of the claimed specifics. deep_tier2 independently verified both rows against estate bytes (registry entry and metadata at `memory/percolator/invariants.json:6229-6239` with the sanctioned-path hash recomputation returning canonical 106c128a06aae07c; the v2 profile's fields, raw-capture prevalence counts, and an in-process loader smoke run returning the all -4.0 bias map). Filed as DISPUTED per the rule: outside TOP-K, no exclusion weight, executed status unchanged in the scoreboard [single-judge-gate-invariant#0, single-judge-gate-invariant#1].

## BLOCKED (1 row)

**single-judge-gate-invariant#3** (estate_status: blocked, leverage: medium). What is owed: the steal card's secondary probe - re-score an existing banked waste/verdict surface with a second judge arm and report raw agreement. Reason it is blocked: outside this lane's finish line (mint + cut) and it needs a second-judge dispatch the lane did not have armed. Consequence stated in the row: the minted invariant 106c128a06aae07c is currently a law record, not a firing gate, and no estate surface yet carries a measured agreement score. The same row inherits two unmeasured quantities: string-token logit_bias wire shape on llama-cpp-python 0.3.36, and penalty magnitudes (uniform -4.0, prevalence-validated only) [single-judge-gate-invariant#3].

Next-sitting unblock, in the row's own words: "Re-score ~100 rows of an existing banked waste/verdict surface with a second judge arm and report raw agreement; near the 61% precedent the invariant is mandatory before any waste gate fires, at >=90% it scopes as overkill there (steal card falsifier)." One seat, one sitting: arm the second-judge dispatch on a funded lane, run it against roughly 100 banked rows, file the raw agreement beside the invariant.

## NEGATIVE RESULTS (counted reasons)

No row executed false. The negative material is non-execution and residual debt, counted by reason:

| # | Reason | Count | Where (lane#row / lane record) |
|---|--------|-------|--------------------------------|
| 1 | Full 4,358-test census suite not run; verification scoped to touched files and suites | 5 | single-judge-gate-invariant#2 (checks: 46 passed on 4 files), cloud-suffix-refuse#2 (19 + 44 passed), cap-draw-range-invariant notes (55 passed on 4 files), heal-log-drain not_run (27 passed on 4 suites), kv-env-contract adjacent_surfaces (47 passed on 4 files, 18:51) |
| 2 | Second-judge dispatch not armed; probe blocked; invariant stays a law record, not a firing gate | 1 | single-judge-gate-invariant#3 |
| 3 | Inherited-unmeasured: string-token logit_bias wire shape on llama-cpp-python 0.3.36; penalty magnitudes | 1 | single-judge-gate-invariant#3 |
| 4 | Scoped-out residual: OLLAMA_NO_CLOUD env pin not landed (steal card port half 2) | 1 | cloud-suffix-refuse#0 |
| 5 | No live tool registered dynamic today; live-path schema split is a no-op by construction | 1 | schema-placement-law#4 |
| 6 | File-too-long debt accepted: mag/inference_budget.py at 414 of the 400-line cap; prune owed on next edit | 1 | cap-draw-range-invariant#2 |
| 7 | Sibling pre-push debt, unowned: 3 NEW ratchet findings (gstd_accounts.py:63, prepush_verkle_hermeticity.py:415, suno_lane.py:171) + GROWTH claims - the two sources disagree (cap-draw-range-invariant#3: 4 pre-existing; heal-log-drain#4: 5; conflict recorded, not resolved by the fold, which holds no recount of a moved tree) - + 3 zknot PHANTOM-NUMBER records | 2 | cap-draw-range-invariant#3, heal-log-drain#4 (shared evidence; the script's one cross-lane duplicate quote) |
| 8 | f16-vs-q8_0 A/B KV delta never measured (baseline /api/ps empty pre-restart) | 1 | kv-env-contract#2 |
| 9 | Contingent: a second tailnet Ollama host would need its own env contract; none reachable, nothing skipped | 1 | kv-env-contract#4 |
| 10 | graph_heal end-to-end heal pass after the drain not run (117-row log consumed as-is) | 1 | heal-log-drain not_run |

Tombstones: [] (zero; casualty header reads missing 0 and parse errors 0, and the run metadata carries an empty tombstoned list, so nothing is subtracted from owed).

## NEXT REGISTER (top 10 residuals, one seat one sitting)

1. **Unblock the second-judge re-score** (single-judge-gate-invariant#3, the run's only blocked row): arm a second-judge dispatch on a funded lane, re-score ~100 rows of an existing banked waste/verdict surface, report raw agreement beside invariant 106c128a06aae07c. Falsifier rides on the row: near the 61% precedent the gate is mandatory, at >=90% it scopes as overkill.
2. **Full-suite census on the folded tree** (reason 1 above, five lanes scoped their runs): run the census instrument, file instrument, moment, and real numbers per the census denominator law; never difference counts taken at different moments.
3. **Prune mag/inference_budget.py under the 400-line cap** (cap-draw-range-invariant#2): the file sits at 414 with accepted_lines frozen at 414 (baseline entry 26adccc77fbb17ba); the next edit to that file trims or splits the module before anything else is added.
4. **Pin OLLAMA_NO_CLOUD on the janitor host env** (cloud-suffix-refuse#0 residual): persist, restart, re-run the live gate; closes the steal card's second port half behind the already-landed suffix refusal.
5. **Wire the first dynamic tool registration** (schema-placement-law#4 residual): an MCP-style grant registered through `register_dynamic_tool_schemas` so the live-path split stops being a no-op by construction, and audit which future grants should register dynamic.
6. **Dispose the three sibling NEW ratchet findings** (cap-draw-range-invariant#3 + heal-log-drain#4): tools/gstd_accounts.py:63 except-pass, tools/prepush_verkle_hermeticity.py:415 file-too-long, tools/suno_lane.py:171 env-key-read. Three files, three owners - not a one-seat sitting - so the marked disposition is the operator's one command: `python tools/violation_ratchet.py baseline-update --by <operator> --note "port-debt-20261011 register row 6"` accepts all three by name; per-owning-seat fixes remain the alternative that recovers the debt instead of registering it. The tree ratchet exits 1 until one of the two happens.
7. **Fix the three zknot PHANTOM-NUMBER records** (heal-log-drain#4): memory/zknot/*.md blocks citation lint at pre-push; downgrade the claims or cite the named sources.
8. **Run the f16-vs-q8_0 A/B probe** (kv-env-contract#2 residual): fixed num_ctx size delta via ollama ps plus a 10-prompt scut quality spot check; no f16 baseline size was ever recorded.
9. **Dispose the 21 dead-lettered heal edges** (heal-log-drain#3): every dangling edge points at a verkle knot id no longer in the rebuilt node set; restore the knots or retire the log rows so the dead-letter file stops being the resting place.
10. **Measure the string-token wire shape and penalty magnitudes** (single-judge-gate-invariant#3 inherited-unmeasured): logit_bias string-token behavior on llama-cpp-python 0.3.36 and the uniform -4.0 magnitudes must exist in evidence before any v2 profile default flip.

Fold close: both copies of this document are written byte-identically (estate and workspace). The script owns the numbers; the lanes own the quotes; the fold owns the prose.
