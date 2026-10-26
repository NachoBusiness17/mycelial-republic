# MASTER FOLD: GSTD x MYCELIAL KICKOFF (run gstd-mycelial-kickoff-20261007, MICKEY-17 v2.1)

- folded_at: 2026-10-07T13:53:09Z (script sha256 58bd72c79c6d); prose folded the same day by the folder seat.
- Lane archive read in full this fold: `memory/runs/mickey17_v2/runs/gstd-mycelial-kickoff-20261007/lanes` (5 lane files, 23 rows). Quotes below are the lane rows' own `quote` fields. Verifier facts are the run's persisted `laneChecks`/`deepChecks` metadata.
- Number law: the script's sections are verbatim and authoritative. The only numbers not from the script are tallies marked `carried` (counted by hand from the same archive this fold).
- Row indices are 0-based within each lane file, matching the script's TOP-K keys.
- DISPUTED: 0. The script files a lane-claimed top steal outside its TOP-K as DISPUTED; a grep of the lane archive for "top steal" claims returned zero hits (grep exit 1, run this fold). Nothing disputes the list.
- Fold observation (`carried`): the scoreboard counts 13 high-leverage rows but the script's TOP-K lists 12. The 13th, g5-wallet-door#3, is the Ollama-bind negative finding; it is folded under NEGATIVE RESULTS below, where it belongs, and is not claimed as an execution.

## CASUALTY HEADER (verbatim from the script)

- fired: 5
- landed (parseable files): 5
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

Tombstones: [] (run metadata). Nothing was subtracted from owed.

## PRISMA FLOW (verbatim from the script)

- identified: 23
- screened: 23 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 23
- invariant: identified == included + excluded **HOLDS** (23 = 23 + 0)

## SCOREBOARD (verbatim from the script)

- rows: 23
- estate_status: executed 21, executed-with-deviation 2
- leverage: high 13, medium 9, low 1

## EXECUTIONS (the script's TOP-K, with proof quotes)

Script fidelity and verifier lines, verbatim:

- rows with all of quote/source/steal/estate_status non-empty: 23/23 (100.0%)
- verdicts: deep_tier2 12 (verdict split: verified 12), supports 23 (supports split: no 6, yes 17)
- deep_tier2 join: 10/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 2

All 12 TOP-K rows carry a persisted deep_tier2 verdict of verified (run metadata deepChecks). The 6 supports=no rows were quote-sufficiency findings by the support checker; where a deep_tier2 byte-check exists for the same row it cured them: g3-fleet-lane-spec#0 and g5-wallet-door#0 show the cure in their EXECUTIONS entries, and g3-fleet-lane-spec#1 and g5-wallet-door#1 carry the same cure inside their verified verdicts.

FLAGGED IN PLACE, supports=no with NO persisted deep check, exactly 2 rows (neither is a TOP-K row, so neither has an EXECUTIONS entry; each quote-sufficiency finding stands as filed, not byte-cured):

- g1-clone-compose#3 (live node census via the one permitted GET /api/v1/nodes curl): substance carried at NEXT REGISTER item 4.
- g3-fleet-lane-spec#4 (deviation row, first pytest 1 failed / 12 passed): substance carried in NEGATIVE RESULTS, gate/test first-run failure row.

### g1-clone-compose#1 [high]
- Claim: docker compose config validated the desktop node shape with exit 0: memory limit 536870912 bytes (512M), reservation 128M, port 8080 published tcp, healthcheck curl /health, named volume gstd-data at /data/gstdbot; no container started.
- Proof quote: `limits:` / `memory: "536870912"`
- Verifier: deep_tier2 verified. Conditions carried from the check: the quote is the resolved `docker compose config` output, not file bytes (the file itself reads `memory: 512M`; values are identical); and the claim's "empty docker ps -a" should read "no gstdbot container in docker ps -a" (the host runs 6 unrelated containers, none gstd).
- Steal (g1-clone-compose#1): residual: shipped compose lacks OLLAMA_URL, NODE_NAME, GSTD_NODE_ID and any wallet mount; apply the P1 section before the first docker compose up.

### g1-clone-compose#2 [high]
- Claim: P1 FIRST-START GROUND TRUTH section appended to docs/ref/GSTD_DOGFOOD_PLAN.md: compose env gaps (OLLAMA_URL host.docker.internal, NODE_NAME+GSTD_NODE_ID, GSTD_WALLET_ADDRESS inert in the full node), TON UQ/EQ wallet format with wallet.json as the binding source, the persistence defect (wallet at $HOME/.config/gstdbot, off the volume, new address on recreation), the fully automatic registration flow, and the live census; citation lint blocking=0.
- Proof quote: "GSTD_WALLET_ADDRESS: this env is inert in the FULL node today. Its five src/ hits are a startup print"
- Verifier: deep_tier2 verified (git diff reads 82 insertions, 0 deletions; section runs line 79 to EOF; citation lint on the doc re-run this check: ok, blocking=0, warns=8 TOKEN-MISS warn-only). Condition carried: the repo-wide pre-push lint currently reads FAIL blocking=1, but the single blocker is PHANTOM-NUMBER in watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md:17, a different file outside this deliverable.
- Steal (g1-clone-compose#2): residual: at P1 fire, add the env block plus a mount at /root/.config/gstdbot, paste the owed wallet, then docker compose up.

### g2-mcp-door#0 [high]
- Claim: plan's own command run verbatim from the repo root (claude mcp add --transport http gstd https://platform.gstdtoken.com/mcp); the gstd HTTP door is now a project-scoped seat door in C:/Users/foste/.claude.json (local scope), backup taken beforehand, claude mcp get gstd reports Connected; zero repo bytes touched.
- Proof quote: `"gstd": {` / `"type": "http",` / `"url": "https://platform.gstdtoken.com/mcp"` / `}`
- Verifier: deep_tier2 verified; the checker independently re-ran `claude mcp get gstd` (Status: Connected) and diffed the pre-add backup. Conditions carried: the literal act of running the command is a historical event bytes cannot timestamp; the zero-repo-bytes negative is consistent with every observable artifact.
- Steal (g2-mcp-door#0): done. Notes field carries the scope law: a user-scope or shared .mcp.json copy is an operator call, not taken here.

### g2-mcp-door#1 [high]
- Claim: tools/list probed through the door exactly once via anonymous JSON-RPC over streamable HTTP (no keys, no tasks submitted): initialize answered gstd-network v1.0.0 protocol 2024-11-05, then 4 tools exposed (gstd_inference, gstd_list_models, gstd_network_stats, gstd_join_network). No registration required, so the plan's BLOCKED-on-registration contingency does not fire.
- Proof quote: `"serverInfo":{"name":"gstd-network","version":"1.0.0"}`
- Verifier: deep_tier2 verified (protocol 2024-11-05, 4-tool catalog, auth_required false, registration_required false all grepped in the banked lane file). Condition carried: "exactly once" is a banked single-probe record (one initialize id:1, one tools/list id:2), not an externally observable fact.
- Steal (g2-mcp-door#1): done.

### g3-fleet-lane-spec#0 [high]
- Claim: the gstd fleet lane spec landed as the lane deliverable: the submit/poll/bank pattern (fixed-literal platform URLs, regex-gated poll segment, 10s x 30 poll window), the fail-closed per-device wallet gate, the gps_mesh_row.v1 contract keyed (node_device, task_shape, evidence_hash), honest non-scope, and the wire plan that fires only on wallet paste. The wire patch into tools/free_lane_fleet.py is by design NOT landed here.
- Proof quote: `# GSTD FLEET LANE SPEC (the 8th lane, the one that PAYS)`
- Verifier: deep_tier2 verified. The support checker had filed the title-only quote as supports=no; the tier-2 byte-check cured it: every enumerated component (fixed literals, regex gate, 10s x 30 window, fail-closed gate, gps_mesh_row.v1, non-scope, section 7 wire plan) grepped byte-present, and tools/free_lane_fleet.py confirmed unmodified (grep for gstd exit 1, empty git diff).
- Steal (g3-fleet-lane-spec#0): done, with the deferral as part of the deliverable: the wire fires on wallet paste, one sitting (spec section 7).

### g3-fleet-lane-spec#1 [high]
- Claim: the skeleton provider module landed: submit_task/poll_task/cycle_gstd all gate on wallets before any network call; SSRF guard carries the free_lane_fleet law (byte-matched literals, redirect-refusing opener, task id regex ^[A-Za-z0-9_:-]{1,80}$ before URL join); retry-never; gps_mesh_row() raises on empty evidence_hash (Q28 gate) and to_verdict_log_args() is the wire adapter into GpsLedger.record_verdict with node_device mapped to model_id gstd-mesh:<device>.
- Proof quote: `return False, ("WALLET GATE BLOCKED: no per-device wallets in .env (owed: "`
- Verifier: deep_tier2 verified (file read in full, 352 lines; gates at lines 177/198/275 precede every network call; allowlist, _NoRedirect, TASK_ID_RE, retry-never, Q28 raise, and signature-compatible wire adapter all byte-checked). Condition carried: the module produces the record_verdict kwargs but never itself calls GpsLedger; the call site lives outside the skeleton.
- Steal (g3-fleet-lane-spec#1): done.

### g3-fleet-lane-spec#2 [high]
- Claim: negative first-class, live: with zero wallets in .env, --cycle printed the blocked verdict and exited 3 with zero network calls, and --status read WALLET GATE: BLOCKED (devices with wallets: none). The no-live-submits law is proven on this box, not just claimed.
- Proof quote: "WALLET GATE BLOCKED: no per-device wallets in .env (owed: GSTD_WALLET_DESKTOP, GSTD_WALLET_BOB, GSTD_WALLET_PIXEL); P0 INPUTS OWED; live cycle refused"
- Verifier: deep_tier2 verified, and the checker re-ran both commands itself this session: --status matched, --cycle printed the quote byte-identical and exited 3; control-flow analysis proves zero network reach behind the closed gate.
- Steal (g3-fleet-lane-spec#2): residual: wire into free_lane_fleet.py PROVIDERS + first live cycle, same sitting as P1 desktop node, on wallet paste.

### g4-mycelial-kickoff#0 [high]
- Claim: Republic README v2 written and committed on branch mag/kickoff-mesh-live-20261007 (commit e9c6bf2, 2 files changed 111 insertions, push withheld pending operator GO): status flipped to THE MESH IS LIVE (2026-10-07) with the five organs, GSTD named as the settlement plane when per-device wallets land, and a live-vs-staged tri-state carrying its own falsifier row; committed bytes verified dash-free.
- Proof quote: "Status: THE MESH IS LIVE (2026-10-07). Phase 0 seed mirror shipped, and the network around it stopped being a diagram."
- Verifier: deep_tier2 verified (commit shape 2 files / 111 insertions confirmed; committed bytes sha-identical to disk; 0 em, 0 en dashes; push withheld confirmed, origin/master does not contain e9c6bf2). Condition carried: the quote matches byte-for-byte except the markdown emphasis markers around the first sentence.
- Steal (g4-mycelial-kickoff#0): done (residual: operator GO flips the push; branch mag/kickoff-mesh-live-20261007 is one command from origin).

### g4-mycelial-kickoff#4 [high]
- Claim: the activation's honesty tri-state is receipt-grounded, deliberately deviating from the task's shorthand: README v2 files the desktop leg LIVE and the two remote legs STAGED (the standing-wave receipt names seed + bob's first pull as owed; round trip proven on loopback 2026-10-07T01:40Z, 561,386 files / 7.6GB, tamper refusal 403); the GSTD settlement plane is STAGED on the owed per-device wallet paste with census numbers byte-grounded in watch/inbox/GSTD_NODE_CENSUS_20261007.md.
- Proof quote: "Owed: seed on the tailnet IP + bob's first pull (ON bob)"
- Verifier: deep_tier2 verified (owed line grepped at MESH_DELTA_SEED_20261007.md:69 and :92; loopback proof and tamper 403 at :72-80; census bytes count=4, Pi 272 tasks, 47.39 GSTD, reputation 55 byte-grounded; P0 staging grounded in GSTD_DOGFOOD_PLAN.md:20-25). Condition carried: the literal artifact name "README v2" was not found at any estate path searched (it lives in the republic repo, outside that search); the tri-state substance it describes is fully receipt-grounded.
- Steal (g4-mycelial-kickoff#4): done (residual: the two remote-leg sittings and the wallet paste are the operator's remaining GO items before the STAGED rows can flip LIVE).

### g5-wallet-door#0 [high]
- Claim: the one-paste wallet-door runbook landed (322 lines): three per-device address slots (desktop/bob/pixel), the byte-traced registration field per shape, exact landing spots, the idempotent fail-closed PowerShell paste that fires P1 and prints P2, device prereqs, and five negative findings.
- Proof quote: `# GSTD WALLET DOOR: the one-paste runbook (2026-10-07, lane g5-wallet-door)`
- Verifier: deep_tier2 verified. The support checker had filed the title-only quote as supports=no; the tier-2 byte-check cured it: wc -l reads 322 and every enumerated component (three slots, per-shape byte-trace, landing-spot table, paste section 4 with two abort guards, prereqs section 5, exactly five negative findings under the section 6 header) grepped byte-present.
- Steal (g5-wallet-door#0): done. The runbook's five negative findings ride this row: Ollama 127.0.0.1-only bind; bare .env never reaches the container; platform-side wallet validation UNREAD; cloudflared/tunnel earning path unexplored; erratum to the plan's index.ts:521 citation.

### g5-wallet-door#1 [high]
- Claim: registration contract byte-traced on gstdbot tip e0bbe4851: node-lite registers body field `wallet` from --wallet/GSTD_WALLET_ADDRESS and hard-exits without it (node-lite/index.ts:20,45-60,146-150); the FULL node registers wallet.json's address, never the env, through PlatformLink (platform-link.ts:111-116) and SwarmAgent (agent.ts:1357-1361), fed from index.ts:292-294.
- Proof quote: `if (!WALLET) {` / `console.error('Usage: gstd-node --wallet EQ... [--name my-node] [--port 8765]');` / `process.exit(1);` / `}`
- Verifier: deep_tier2 verified (tip hash confirmed; both shapes traced line-level; grep proves no FULL-node registration path reads the env). Condition carried: the row's "fed from index.ts:292-294" compresses three feed legs into one citation (that exact site is the revenue-engine feed; PlatformLink and SwarmAgent are fed from the same wallet.getAddress() at server.ts:368-370 and agent.ts:108-110); the proof doc names all three, the row compressed them. Verdict stands.
- Steal (g5-wallet-door#1): done.

### g5-wallet-door#2 [high]
- Claim: landing spots proven by rendering, not assumed: a bare .env in the clone never reaches the container while docker-compose.override.yml merges GSTD_WALLET_ADDRESS, NODE_NAME, OLLAMA_URL and the /root/.config/gstdbot wallet bind mount (docker compose config exit 0); desktop tailnet IP 100.96.161.76 verified live via tailscale ip -4; throwaway proof files removed, clone clean (git status shows only pre-existing .mimosa/).
- Proof quote: "`docker compose config` rendered no trace of the variable; with the same value in docker-compose.override.yml environment it rendered as `GSTD_WALLET_ADDRESS: EQTEST_interp_check` alongside NODE_NAME, OLLAMA_URL, and `target: /root/.config/gstdbot` (exit 0). Both test files were removed"
- Verifier: deep_tier2 verified (quote byte-matched at receipt lines 107-110; clone residue, HEAD hash, and shipped-compose coherence confirmed live this session). Conditions carried: the config render and the tailscale IP check are receipt prose the verifier flagged as asserted-not-rerun (reproducing them would have required creating throwaway files); both are internally consistent with the landed bytes.
- Steal (g5-wallet-door#2): done.

## BLOCKED TIER (gated rows: reason, next-sitting unblock)

Zero rows carry estate_status=blocked (script scoreboard: executed 21, executed-with-deviation 2). The gates below are residuals that gate the next sitting. Every one is fail-closed by design and every one was proven closed live.

1. g1-clone-compose#1, g1-clone-compose#2, g3-fleet-lane-spec#2, g4-mycelial-kickoff#4, g5-wallet-door#0: BLOCKED on the P0 wallet paste. Reason: three per-device GSTD wallet addresses (GSTD_WALLET_DESKTOP, GSTD_WALLET_BOB, GSTD_WALLET_PIXEL) exist only with the operator; every live verb gate-closes without them (proven live, g3-fleet-lane-spec#2, exit 3, zero network), and the shipped compose carries no wallet mount at all (g1-clone-compose#1). Next sitting: the operator's one paste per watch/inbox/GSTD_WALLET_DOOR_20261007.md, which fires P1 (desktop node) in the same sitting.
2. g5-wallet-door#3: BLOCKED on the Ollama bind. Reason: Ollama 0.34.3 listens on 127.0.0.1 only and refuses the tailnet IP (curl exit 7 / HTTP 000), which breaks the desktop container's host.docker.internal path AND both lite nodes; the paste's Guard fail-closes on this instead of firing into a black hole. Next sitting: operator runs setx OLLAMA_HOST 0.0.0.0, restarts Ollama, and re-curls http://100.96.161.76:11434/api/version before the first paste (steal sentence, g5-wallet-door#3).
3. g5-wallet-door#4: BLOCKED on remote-leg prereqs. Reason: P2 prints the bob and pixel commands rather than auto-firing them, because the estate's own pool-setup doc marks both prereqs unmet (bob SSH key auth, Pixel Termux). Next sitting: land bob key auth + Termux setup per watch/inbox/GSTD_POOL_SETUP_20261001.md, then run the printed P2 lines (addresses already baked in) (steal sentence, g5-wallet-door#4).
4. g4-mycelial-kickoff#0: BLOCKED on operator GO. Reason: push withheld pending operator GO; origin/master does not contain e9c6bf2 (deep-check confirmed). Next sitting: operator GO; the branch is one command from origin (steal sentence, g4-mycelial-kickoff#0).
5. g3-fleet-lane-spec (lane note, rows #0-#2): BLOCKED on wire-time truth. Reason: platform response field shapes stay defensive until verified against the live platform at wire time. Next sitting: the first live cycle after wallet paste verifies the shapes and firms the module (steal sentence, g3-fleet-lane-spec#2 residual).

## NEGATIVE RESULTS (counted reasons table)

Counts are `carried` (folded by hand from the lane archive this fold); the underlying quotes and verdicts are the archive's. Tombstones: [] (none; nothing subtracted from owed).

| Reason class | Count (`carried`) | Rows (lane#row) | Disposition |
|---|---|---|---|
| Gate/test first-run failure, cured in-ask | 3 | g1-clone-compose#4 (citation lint FAIL, 21 blocking PATH-MISSING clone-relative anchors; rewritten repo-root, re-run ok blocking=0); g3-fleet-lane-spec#4 (first pytest read 1 failed / 12 passed, adapter test contradicted the spec mapping; test aligned to spec, module unchanged, green inside the 67); g5-wallet-door verification block (citation lint first run blocked on a bare-basename PATH-MISSING anchor; fixed to full paths, re-run green) | Failures filed first-class, not hidden; final states green with receipts |
| Transient environment, re-ran clean | 1 | g4-mycelial-kickoff#3 (first combined organ-test run errored 29 PermissionErrors; subsets isolated 18 + 11, all pairs pass, combined re-ran clean twice) | Diagnosed environmental file-locking, not an organ defect |
| By-design not-run (scope honestly bounded) | 5 | g2-mcp-door negative_first_class item 1 (gstd_inference never called; ask bounds probing to the sensing class, probed false); g2-mcp-door negative_first_class item 2 (pytest and workflow-gate not run; zero repo bytes, host config only); g1-clone-compose lane note over rows #0-#4 (pytest -q not run; docs + receipt only, the prose-record citation gate is the applicable check and passes); g4-mycelial-kickoff#3 claim tail (republic suite not run; docs-only change, no test reads README.md); g5-wallet-door verification.pytest (not run; prose receipt, no code touched) | Scope recorded at row level with evidence |
| Live environment defect found (negative first-class) | 1 row-level | g5-wallet-door#3 (Ollama 0.34.3 answers on 127.0.0.1 only; tailnet curl exit 7 / HTTP 000; breaks host.docker.internal AND both lite nodes; the paste's Guard fail-closes and prints the cure) | Unblock filed: OLLAMA_HOST 0.0.0.0 flip (BLOCKED tier item 2). The runbook under g5-wallet-door#0 additionally banks five negative findings (see EXECUTIONS) |
| Deviation filed (executed-with-deviation) | 2 | g4-mycelial-kickoff#2 (uncommitted 2026-08-10 scrub hunk superseded; pre-edit 4731 bytes banked in lane artifacts; commit staged ONLY the two lane files; SOURCES.md credit carried as prose); g5-wallet-door#4 (P2 prints instead of auto-firing, gated on unmet prereqs; erratum filed: index.ts:521 is the P2P identity wire, PlatformLink feed is index.ts:292-294 plus gateway/server.ts:350) | Disclosed with receipts; matches the script's executed-with-deviation 2 exactly |
| Deferred by design | 2 | g3-fleet-lane-spec#0 (wire patch into tools/free_lane_fleet.py NOT landed; spec section 7 defers it to after P0 wallets; deep check confirmed the file unmodified); g2-mcp-door notes (user-scope / shared .mcp.json copy is an operator call, not taken) | Fires on wallet paste / operator call respectively |

Total negative instances folded: 14 (`carried`).

## NEXT REGISTER (top 10 residuals, one seat one sitting)

1. Operator, one sitting: the one-paste wallet door. Paste the three per-device addresses (GSTD_WALLET_DESKTOP, GSTD_WALLET_BOB, GSTD_WALLET_PIXEL) per watch/inbox/GSTD_WALLET_DOOR_20261007.md; the paste fires P1 (unblocks g1-clone-compose#2, g3-fleet-lane-spec#2, g4-mycelial-kickoff#4, g5-wallet-door#0).
2. Desktop seat, one sitting: setx OLLAMA_HOST 0.0.0.0, restart Ollama, re-curl http://100.96.161.76:11434/api/version before the first paste (g5-wallet-door#3).
3. Desktop seat, one sitting (same sitting as 1, after it): fire P1: env block (OLLAMA_URL host.docker.internal, NODE_NAME, GSTD_NODE_ID), the /root/.config/gstdbot mount, docker compose up (g1-clone-compose#1, g1-clone-compose#2).
4. Desktop seat, one sitting: re-curl GET /api/v1/nodes after the desktop node registers to prove the new row appears; watch falsifier 5 (swarm growth beyond household) stays unfired (g1-clone-compose#3).
5. Mesh seat, one sitting (same sitting as P1, on wallet paste): wire tools/gstd_fleet_provider.py into tools/free_lane_fleet.py PROVIDERS + first live cycle, and firm the platform response field shapes at wire time (g3-fleet-lane-spec#2, g3-fleet-lane-spec#0 deferral).
6. Bob seat, one sitting: land SSH key auth per watch/inbox/GSTD_POOL_SETUP_20261001.md, then run the printed P2 line for bob (g5-wallet-door#4).
7. Pixel seat, one sitting: land Termux setup per the same pool-setup doc, then run the printed P2 line for pixel (g5-wallet-door#4).
8. Operator, one sitting: GO flips the push of branch mag/kickoff-mesh-live-20261007; the kickoff-post sender reads the Notes section before posting (receipts paths are estate-internal, the public pointer is the starter kit repo) (g4-mycelial-kickoff#0, g4-mycelial-kickoff#1).
9. Republic seat, one sitting: disposition for the August scrub family still uncommitted in the republic tree (AGENTS.md, CONTRIBUTING.md, docs/*, cli.py, SOURCES.md, spore.py) (g4-mycelial-kickoff#2).
10. Patrol seat, one sitting: if the combined organ-test PermissionError recurs, file a patrol tripwire; the 8 warn-only TOKEN-MISS in g1-clone-compose#4 stand advisory, flip nothing (g4-mycelial-kickoff#3, g1-clone-compose#4).

## FOLD CLOSE

Five lanes fired, five landed, nothing empty, nothing missing, nothing tombstoned. Twenty-three rows in, twenty-three rows included, the PRISMA invariant holds. Twelve executions, all deep-tier2 verified. Two deviations, both disclosed with receipts. Every gate that closes, closes on purpose, and the key to every gate is one paste the operator still owes. The structure held; the register above is what sits next.
