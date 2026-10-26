# MASTER FOLD - OVERNIGHT MESH 2026-10-07 (MICKEY-17 v2.1, genre: execute)

- folded_at: 2026-10-07T03:41:14Z (counting script sha256 76bb8ea7620d). Prose folded by the folder seat from `memory/runs/mickey17_v2/runs/overnight-mesh-20261007/`: FOLD_SECTIONS.md plus all 6 lane `.json` files and all 6 persisted `.checks.json` verifier files, read in full this fold.
- Law of the fold: every number is the counting script's; quotes are verbatim lane-row bytes; anything the folder composed or generalized is tagged `carried`. Row indices are 0-based within each lane, matching the script's TOP-K. Every steal sentence carries lane id + row index.
- Copies: estate `corpus/steal/MASTER_OVERNIGHT_MESH_20261007.md` and workspace `~/.zcode/workspace/default/mickey17_v2/MASTER_OVERNIGHT_MESH_20261007.md`.
- FoldInfo: top_steal_count=12 (the script TOP-K), disputed_count=0 (grep over the lane files found no lane-claimed top steal outside the TOP-K list).

## CASUALTY HEADER (script, verbatim)

- fired: 6
- landed (parseable files): 6
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## SCOREBOARD (script recount, verbatim)

- rows: 28
- estate_status: executed 23, executed-with-deviation 3, blocked 2
- leverage: high 19, medium 9

## PRISMA FLOW (script, verbatim)

- identified: 28
- screened: 28 (all rows carry the six rubric fields or their gap notes)
- excluded: 9 verifier-unconfirmed (deep_tier2): 1
- included: 27
- invariant: identified == included + excluded **HOLDS** (28 = 27 + 1)

Folder note (`carried` reading, no number changed): the included+excluded invariant binds excluded to 1, and the verifier table names the one exclusion - the single deep_tier2-unconfirmed row, o5-gpu-ladder#0. Its lane estate_status stays "executed"; the exclusion is the fold's verdict weight, not the lane's status.

## VERIFIER TABLE / FIDELITY / WIDTH / URL LIVENESS (script, verbatim)

- rows with all of quote/source/steal/estate_status non-empty: 28/28 (100.0%)
- lanes with persisted checks: 6
- verdicts: deep_tier2 12 (verdict split: unconfirmed 1, verified 11), supports 28 (supports split: no 7, yes 21)
- deep_tier2 join: 11/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 1
- rows/lane: median 5, max 5, min 3; top-10 lanes share: 100.0%; exact cross-lane duplicate quotes (normalized): 0
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)
- URL LIVENESS: unique URLs: 0; fetched: 0; skipped non-public: 0; live: 0; dead/blocked-status: 0

## EXECUTIONS - SCRIPT TOP-K, 12 STEALS WITH PROOF QUOTES

(The script's TOP-K is authoritative; its printed lines are truncated, so the full steal text below is the lane row's own. Verdicts are the persisted `.checks.json` bytes. "not deep-checked" = no deep_tier2 entry exists for that row.)

### 1. o1-wowhead-mesh#1 [high] - the clone is a mesh surface the seed can serve
- Steal: ran `.venv/Scripts/python.exe -m tools.mesh_delta scan` after producing: 562,232 files / 7,280 MB scanned at 2026-10-07T02:16:53Z, and all 6 wow_manifest knot leaves are in delta_index.json with size 1148 and their sha256 entries.
- Proof quote (row source: memory/mesh/delta_index.json): `{"scanned": 562232, "total_mb": 7280, "ts": "2026-10-07T02:16:53.150270Z", "chain_tip_index": null}`
- Verdict: supports=no at tier 1 (the knot-leaf conjunct is not in the quote), deep_tier2=verified - the quote is scan()'s stdout return (tools/mesh_delta.py:126-127, printed at :595), not byte-in the index, but the 114,211,901-byte index carries the exact ts, len(files)=562232, total_bytes=7,634,499,095 (= 7280 MiB), and 7/7 wow-manifest knot sha256 entries match fresh disk hashes.
- estate_status: executed.

### 2. o1-wowhead-mesh#2 [high] - guarded fetch round trip through the serve door
- Steal: fetched the wow_manifest_5 knot chunk through the mesh_delta serve door 127.0.0.1:8767 /chunk via the client's own _guarded_fetch: 1148 bytes arrived with sha256 equal to both the index sha and a fresh disk read, and a tampered request (all-zero sha) was refused HTTP 403 - round trip verified, law held.
- Proof quote (watch/inbox/WOWHEAD_MESH_P1_20261007.md:75-76 per the deep check): `ROUND TRIP MATCH: True` / `TAMPER REFUSED: HTTP 403 {"error": "refused: outside memory root, over cap, or sha mismatch"}`
- Verdict: supports=yes; deep_tier2=verified - disk knot sha256 7a35c3a1f7855a44...78d5ff1 (1148 B) matches index and receipt; the 403 law byte-verified at tools/mesh_delta.py:206-212 with read_chunk :168-175; _guarded_fetch loopback allowlist at :249-282.
- estate_status: executed.

### 3. o2-crsqlite-spike#0 [high] - multi-master local-SQL merge proven on the gps ledger shape
- Steal: cr-sqlite v0.16.3 Windows x86_64 extension driven end to end on two staged copies of gps_ledger.db3 (782336 bytes each): independent write per replica, merged both directions through crsql_changes, both replicas converged to 32 identical capability rows; same-pk conflict write (0.10 on a, 0.90 on b) converged to 0.9 on both; live db3 sha256 unchanged, no wal/shm/journal sidecars.
- Proof quote (spike_crsqlite_p2/MERGE_RECEIPT_P2.md:43 per the deep check): `PASS capability rows identical across replicas post-merge :: 32 rows a vs 32 rows b`
- Verdict: supports=yes; deep_tier2=verified - the two row counts are two named scripts at two moments, not a contradiction: the quote's "32 rows a vs 32 rows b" is the counting script's own number (spike.py:175-176 emits it at the phase-4 post-merge convergence check, taken before the phase-5 conflict row existed, spike.py:195), while the deep check's read-only read-back of the landed replicas read 33 capability rows each, identical, conflict pass_rate 0.9 on both, distinct crsql site ids - 33 = 30 kept + 2 spike rows + 1 conflict row (deep check: `capability count a=33 b=33; rows identical a vs b: True ... 33 = 30 + 2 spike + 1 conflict, reconstructing the 32-row checked moment`); live ledger sha256 63f2069ca52c3c...d7c7949 byte-unchanged with mtime predating the spike; crsqlite.dll sha256 030c10703e2cda85...15079d, 1,443,655 B.
- estate_status: executed. Row residual: schema-versioned migration before adoption + carry merge batches over the chunk door or MCP dialect (register items 4 and 5).

### 4. o2-crsqlite-spike#1 [high] - the documented ATTACH merge is a silent no-op
- Steal: the documented ATTACH-based crsql_changes merge silently no-ops on the 0.16.3 win build (observed rowcount 160 with zero rows applied; attached site_id reads back as the querying connection's own site for every row); the docs' two-connection streaming pattern (read rows from one connection's crsql_changes, executemany into the other's) is the working sync shape and is what landed in spike.py.
- Proof quote (spike.py run output): `MERGE: rows pulled into a=0 into b=0`
- Verdict: supports=yes (execution output of the exact no-op); not deep-checked.
- estate_status: executed.

### 5. o2-crsqlite-spike#2 [high] - the CRR refusal law
- Steal: cr-sqlite 0.16.3 refuses CRR conversion of tables with NOT NULL columns lacking DEFAULT; the real-adoption migration (rebuild capability with DEFAULTs) was applied in both replicas only and kept all 30 rows; verdict_log (703 rows, no PRIMARY KEY) cannot be a CRR until it gains a pk column.
- Proof quote (MERGE_RECEIPT_P2.md): `Table capability has a NOT NULL column without a DEFAULT VALUE. This is not allowed as it prevents forwards and backwards compatibility between schema versions.`
- Verdict: supports=yes (verbatim runtime refusal only a real CRR attempt produces); not deep-checked. The "30 rows kept" is the phase-1 rebuild count (spike.py:117-118 asserts n==30 right after the DEFAULT rebuild, before any spike rows) - the original rows the migration preserved, so it predates the 32-row merge-check moment and the 33-row final read-back (see o2#0's verdict).
- estate_status: executed. Row residual: run the capability DEFAULT rebuild + verdict_log pk migration against the real ledger, schema-versioned, never in place (register item 4).

### 6. o3-llamacpp-rpc-bobprep#0 [high] - official build verified on this box
- Steal: no existing llama.cpp build, no scoop, no choco on this box; downloaded the official Windows CPU release b11457 (sha256 ED20ED40E10C04D0853D8ACF8700F0E6C1BB8212F0CC70C3A0DA13DCBBC1B802) to C:\Users\foste\llamacpp_rpc_spike and verified ggml-rpc-server.exe + llama-server.exe --rpc (env LLAMA_ARG_RPC) work.
- Proof quote: `version: 0.6.0-dev (build 11457, commit 5ad1c5da0)`
- Verdict: supports=yes; deep_tier2=verified with a quote-provenance caveat - certutil hash byte-exact (zip 19,436,652 B), 7/7 CRC zip-member match, and the rpc/llama-server logs prove execution, but the banner is composed at runtime (format string embedded in llama-common.dll) so it was never stored as bytes anywhere; its constituents are byte-present in the dlls.
- estate_status: executed. Row residual: vulkan-x64 build for the idle Radeon RX 5600 XT would move the single-host baseline (register item 7).

### 7. o3-llamacpp-rpc-bobprep#2 [high] - split measured; the exo door needs a non-fitting model or a second machine
- Steal: gemma-2b split across two local ggml-rpc-server instances (:50052, :50053): generation 6.25/5.94 tok/s (within noise of single-host 6.48/6.01), prompt eval 24.30/28.48 tok/s (25-35% slower); placement proven by live working sets 694,352 K + 1,103,512 K on the two RPC processes plus 'Accepted client connection' in rpc_50052.log. Verdict: single-box split of a fitting small model buys zero generation throughput.
- Proof quote (server_split.log:20 per the deep check): `prompt eval time =     526.62 ms /    15 tokens (   35.11 ms per token,    28.48 tokens per second)`
- Verdict: supports=yes; deep_tier2=verified - byte-exact quote; baseline-vs-split arithmetic holds (split gen -3.5%/-1.2% vs a 7.5% run spread; prompt eval 29.1%/35.2% slower); 61/65 accept/close pairs in the rpc logs; working sets banked at watch/inbox/RPC_SPLIT_SPIKE_20261007.md:57-59.
- estate_status: executed. Row residual: cross-machine desktop+bob split measurement on bob's next boot (register items 1 and 2).

### 8. o3-llamacpp-rpc-bobprep#3 [high] - receipt banked with the env-name deviation named
- Steal: receipt banked with all measured numbers, placement proof and the bob-side one-liner; deviation: the ask said 'client RPC_SERVERS env' but the verified build env is LLAMA_ARG_RPC (checked llama-server --help), so the receipt's one-liner uses LLAMA_ARG_RPC and names the correction.
- Proof quote (RPC_SPLIT_SPIKE_20261007.md:85, byte-exact per the deep check): `.\ggml-rpc-server.exe -H 0.0.0.0 -p 50052 -t 8`
- Verdict: supports=yes; deep_tier2=verified - correction named at receipt :28 and :89-90; corrected join one-liner at :93.
- estate_status: executed-with-deviation.

### 9. o3-llamacpp-rpc-bobprep#4 [high] - BLOCKED (full treatment in the BLOCKED TIER below)
- The script's TOP-K carries this row; it is one of the run's 2 blocked rows. Counted here so the TOP-K stays whole at 12.

### 10. o4-memlance-mcp#0 [high] - memlance gets a wire
- Steal: plant/witness/tally added as three mcp tools in mesh_delta's stdio gps_mcp dialect: plant stores a lance as a content-addressed chunk under memory/mesh/lances/ ({aim, seed, planted_ts}, sha256 of payload = seed_id); witness checks a repo surface for unprompted citation and banks hit_ts + latency; tally reports per-seed hit rates; tools/list over the live server process returns all six tools.
- Proof quote: `TOOLS_LIST: ["picture", "delta", "fetch", "plant", "witness", "tally"]`
- Verdict: supports=yes (the quote names exactly the three new tools plus the three pre-existing); not deep-checked.
- estate_status: executed.

### 11. o4-memlance-mcp#1 [high] - one live plant->witness round trip, miss banked honestly
- Steal: seed_id 09d7613603db19b617bfd714ec1e651cfe04f1e7e1299de309add4bc84f05a33, chunk sha re-verified on disk (SHA_OK), witness against memory/attention.md honestly banked a miss (hit=false, latency_s=0.005; no target has cited the seed yet), both rows in memory/mesh/lances/lances_ledger.jsonl, tally reads 1 lance / 1 witness / 0 hits.
- Proof quote: `"surface": "memory/attention.md", "ts": "2026-10-07T02:31:49.846815Z", "type": "witness"`
- Verdict: supports=yes (a genuine ledger-row fragment, real execution output); not deep-checked. The miss itself is a counted negative (table below).
- estate_status: executed.

### 12. o5-gpu-ladder#0 [high] - rung 1 - VERIFIER-UNCONFIRMED, the run's one PRISMA exclusion
- Steal (lane row): Bionic 1.1.6+3 by LM Studio is installed (registry uninstall key 7c1a7243), :1234 was dead at lane start, the models tree was empty, so the ollama gemma:2b gguf blob was imported, the server started, and the free door measured: gemma-2b Q4_0 warm 72.97/72.86 tok/s, TTFT 15 ms, served through the llama.cpp Vulkan runtime, no ROCm in the path.
- Proof quote (gpu_ladder_20261007_evidence.md:79, byte-exact per the deep check): `"runtime": {"name": "llama.cpp-win-x86_64-vulkan-avx2", "version": "2.53.0", "supported_formats": ["gguf"]}`
- Verdict: supports=no at tier 1; deep_tier2=unconfirmed - the quote and the measurements are byte-grounded (runs at evidence :86-87: 72.97 / 72.86 tok/s), but the install provenance (Bionic 1.1.6+3, registry key 7c1a7243) appears nowhere in the proof file, the only :1234-dead capture was taken after `lms server stop` rather than at lane start, and "empty models tree" is contradicted by evidence line 104 (6 directories). Partially proven, so the fold excludes it.
- estate_status: executed in the lane; excluded by the fold on the unconfirmed verdict. Cure: register item 8, one bounded idempotent refill per the casualty header.

## BLOCKED TIER (2 rows, script scoreboard "blocked 2")

### o1-wowhead-mesh#4 (estate_status: blocked)
- What (lane row): negative finding, not fixed (sibling organ) - scan() reads the verkle cursor as `tip.get("index")` and `tip.get("generated")` at tools/mesh_delta.py:107-108, but memory/biography/verkle_tip.json is schema verkle_tip.v1 carrying n_leaves/updated_minute/last_filename, so the mesh picture's chain_tip_index and chain_tip_ts are structurally null on every picture/delta response.
- Proof quote (tools/mesh_delta.py:107-108): `"chain_tip_index": tip.get("index"),` / `"chain_tip_ts": tip.get("generated")`
- Reason blocked: the defect lives in a sibling organ; the fixing seat is the mesh_delta organ owner, not this lane (row steal field).
- Next-sitting unblock: the organ owner re-anchors the cursor read to the real verkle_tip.v1 key names (n_leaves / updated_minute) at tools/mesh_delta.py:107-108, re-renders one picture, and shows chain_tip_index non-null. One sitting. o1#1's quoted `"chain_tip_index": null` is the before-proof.

### o3-llamacpp-rpc-bobprep#4 (estate_status: blocked)
- What (lane row): the bob half of the P3 probe was not run because the task forbids remote exec on bob; the cross-machine tokens/sec number and the one-liner's firewall/bind behavior on his box stay unmeasured until his seat executes the banked one-liner on next boot.
- Proof quote (watch/inbox/RPC_SPLIT_SPIKE_20261007.md:102-103, byte-verified per the deep check): `No bob-side execution (task forbids remote exec); the one-liner is untested cross-machine until his seat runs it.`
- Reason blocked: the no-remote-exec rule on bob - a task boundary, not a failure.
- Next-sitting unblock: bob's seat on next boot runs `.\ggml-rpc-server.exe -H 0.0.0.0 -p 50052 -t 8` (receipt :80-82: allow TCP 50052 in Windows Defender Firewall), then the desktop seat reruns the split with his tailnet/LAN address in LLAMA_ARG_RPC (receipt :93). Two seats, one sitting each (register items 1 and 2).

## NEGATIVE RESULTS (counted reasons)

| # | reason | count | rows (lane#row, 0-based) |
|---|---|---|---|
| 1 | tombstones (hard failures subtracted from owed) | 0 | [] |
| 2 | PRISMA-excluded: deep_tier2 unconfirmed | 1 | o5-gpu-ladder#0 |
| 3 | tier-1 supports=no, cured by deep_tier2 verified | 5 | o1-wowhead-mesh#1, o6-burners-relief#0, o6-burners-relief#1, o6-burners-relief#3, o6-burners-relief#4 |
| 4 | tier-1 supports=no, not deep-checked (stands tier-1-only) | 1 | o5-gpu-ladder#4 (the "NOT purchased (operator-gated)" quote proves only the no-purchase constraint, not the rungs 4-5 documentation work) |
| 5 | blocked rows | 2 | o1-wowhead-mesh#4, o3-llamacpp-rpc-bobprep#4 |
| 6 | honest-miss results banked inside yes-rows | 2 | o4-memlance-mcp#1 (witness hit=false - no target has cited the seed yet), o5-gpu-ladder#3 (Linux detection lines untested, no Linux host; WMI AdapterRAM caps at 4095 MB on the 6 GB card) |
| 7 | in-lane-cured incident, deep-verified | 1 | o6-burners-relief#3 (first live fire 02:42:43Z wedged on compose stdin; cured with -T --interactive=false on both spells; log gap 02:42:43Z to 02:57:02Z = 14m19s) |

Sum check: rows 2-7 list 12 counted instances but touch 11 distinct rows of 28 - o6-burners-relief#3 is the one row counted in two reasons, under reason 3 (its supports=no verdict, cured by the deep check) and reason 7 (the in-lane incident that caused it); set-count over the table: 12 instances - 1 overlap = 11 distinct. supports=no total = 5 + 1 + 1 = 7, matching the script's split (o5#0 counted once, under reason 2). Tombstones zero: no owed-work subtraction (`carried` from the run metadata `tombstoned: []`).

Lane-disclosed negatives (from the lane files themselves, not row verdicts):
- o5-gpu-ladder `negative_findings` (3): the LM Studio models tree was empty (2.4 GB is runtimes only; planned pulls never happened; ollama twins of the same models are already on disk, so pulling would duplicate); the ask's "RDNA1 unsupported" expectation is struck by bytes (ollama 0.34.3 ships ggml-vulkan.dll, the ROCm path has no gfx1010 kernels, Vulkan is the card's only GPU door); the LM Studio server was stopped and the imported gguf copy deleted after measurement (TS-08 anti-duplication).
- o2-crsqlite-spike lane note: rows were written once after the debug loop settled, not incrementally per row; the Mimosa hook intercepted 3 spike.py write attempts on its SQL scanner before the literal-SQL-with-bound-params version passed (run metadata laneOut).
- o3-llamacpp-rpc-bobprep checks field: pytest not run - no repo code touched; the executed checks were the bench runs, the tasklist placement probe, log byte-verification, and port-clear teardown.
- o6-burners-relief lane note: the full 4,358-test suite was not run; only tests/test_container_setup.py + tests/test_docker_ops.py adjacent (8 passed); no test covers the burners service itself.
- o1-wowhead-mesh laneOut note: the 8767 seed was already live from a sibling and was reused (same tool, bind, and port; the seed re-reads delta_index.json per request); the checks run were the two touched test files plus the doors, not a full-repo pytest sweep.

## NEXT REGISTER (top 10 residuals, 11 rows - item 1's cross-machine measurement is two seats, one row each; one seat one sitting per row)

1. bob seat, next boot (one sitting): run the banked one-liner `.\ggml-rpc-server.exe -H 0.0.0.0 -p 50052 -t 8` (firewall TCP 50052 per receipt :80-82) - opens bob's rpc door, the precondition half of o3-llamacpp-rpc-bobprep#4's unblock.
2. desktop seat, one sitting after item 1: rerun the split against bob's tailnet/LAN address in LLAMA_ARG_RPC (receipt :93) - measures the cross-machine tok/s that unblocks o3-llamacpp-rpc-bobprep#4 and closes o3#2's residual.
3. mesh_delta organ owner, one sitting: fix the chain-tip cursor read at tools/mesh_delta.py:107-108 to the real verkle_tip.v1 keys (n_leaves / updated_minute), re-render one picture, show chain_tip_index non-null (o1-wowhead-mesh#4).
4. cr-sqlite seat, one sitting: schema-versioned migration against the real ledger - capability rebuild with DEFAULTs plus a verdict_log pk column - never in place (o2-crsqlite-spike#0 and o2-crsqlite-spike#2 residuals).
5. cr-sqlite/mesh seat, one sitting: carry crsql_changes merge batches over the mesh_delta chunk door or the MCP stdio dialect so the proven sync shape crosses seats (o2-crsqlite-spike#0 residual).
6. burners seat, daytime sitting: refire R2-fleet + R3-hermes - add env_file: [.env] to the burners service, swap free_lane_fleet_cycle.ps1 lines 11/33 and hermes_burn_247.ps1 line 22 to the cage spell, schtasks /Run each once, then retire the bare-longrunner patrol exception (o6-burners-relief#4 steal; the deep check confirmed both driver files still carry the old form and the service carries no env_file).
7. llamacpp seat, one sitting: pull the vulkan-x64 llama.cpp build for the idle Radeon RX 5600 XT and re-run the single-host baseline (o3-llamacpp-rpc-bobprep#0 residual; pairs with o5-gpu-ladder#1's Vulkan finding).
8. gpu-ladder seat, one sitting (the casualty header's ONE bounded idempotent refill): bank the rung-1 provenance bytes the deep check could not find - Bionic 1.1.6+3 registry uninstall key 7c1a7243, a lane-start :1234 dead probe, and a corrected models-tree statement - into watch/inbox/gpu_ladder_20261007_evidence.md, flipping the run's only unconfirmed verdict (o5-gpu-ladder#0).
9. bench seat, one sitting: 3-run median instead of 2 runs per config for the llama.cpp benches (o3-llamacpp-rpc-bobprep#1 residual).
10. memlance seat, one sitting: plant 4 more lances so tally can judge the 2-hits-in-5 skill falsifier; the hit path waits on real target citation (o4-memlance-mcp#1 steal).
11. burners seat, one sitting: first test coverage for the burners compose service (`carried` from the o6 lane note: "no test covers the burners service itself"; only the adjacent 8 tests ran).

Operator-gated, not seats (`carried` from o5-gpu-ladder#4): the one-decision purchase menu (6700 XT keeps AMD and lights the already-staged gfx1030 ROCm kernels; 3060 buys the CUDA ecosystem; zero purchase executed), and the Bionic seat re-live is a one-line re-import if the operator wants it (o5-gpu-ladder#0 row residual).

## FOLD PROVENANCE

- Read this fold: `memory/runs/mickey17_v2/runs/overnight-mesh-20261007/FOLD_SECTIONS.md`; all 6 lane `.json` files; all 6 `.checks.json` files; directory listings of the run dir and the workspace dir (prior MASTER_* folds present).
- Ran this fold: `grep -rin "top_steal|disputed|top steal"` over the lane `.json` files (checks excluded) - zero hits (exit 1), so no lane claimed a top steal outside the script's TOP-K: disputed_count = 0. No other command was run; the folder folds the persisted verifier bytes, it does not re-run them.
- All deep-check line citations (receipt/ps1/evidence/log lines) are quoted from the `.checks.json` files read this fold and from the run metadata the ask carried; they are the verifier seats' bytes, not the folder's.
- Repair 2026-10-07 (post-fold fresh-reader critique, REVISE on three bullets): (1) o2#0's verdict now names both row counts' provenance - 32 is the counting script's phase-4 number (spike.py:175-176, before the conflict row, spike.py:195) and 33 is the deep check's post-spike read-back; o2#2's verdict now explains its "30 rows kept" as the phase-1 rebuild count (spike.py:117-118); grounding re-run this repair: read-only sqlite3 (`mode=ro&immutable=1`, repo venv python) counted 33 capability rows in each landed replica, 3 mesh-spike rows total (crsqlite-spike-replica-a 0.9, crsqlite-spike-replica-b 0.8, crsqlite-conflict 0.9 on both) = 30 kept + 2 + 1. (2) The negatives sum check corrected: reasons 2-7 touch 11 distinct rows of 28, not 12 - o6-burners-relief#3 sits under both reason 3 and reason 7; grounding re-run this repair: set-count over the table read 12 instances, 11 distinct, one row counted twice. (3) Register item 1 split into items 1-2 so every row is one seat one sitting (11 rows, 10 residuals); items renumbered and all six in-text cross-references updated. No steal text, proof quote, or verdict substance changed - provenance naming and arithmetic only.
