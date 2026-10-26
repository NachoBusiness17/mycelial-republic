# FIX EVERYTHING (operator order, 2026-10-01, coordinator window)

Order: "fix everything" + mid-run "quota is reset". Target set = the boot owed
list + the Q-table FAIL column (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md,
22 FAILs, S1-ranked). Shape: coordinator inline on S1 + Task-agent lanes with
disjoint file ownership, two waves. This receipt folds both waves; every number
below is from the lane reports and the coordinator's own runs, exit codes named.

## Wave 1 + inline (all landed green at filing)

1. **Q21 users.json concurrent write loses 7/8 (the S1 head) - FIXED.**
   New server/store_io.py: `exclusive(path)` (per-path RLock + cross-process
   byte lock on `<name>.lock`, msvcrt/fcntl) + `atomic_write_text`
   (mkstemp + os.replace, PermissionError-retry for lockless readers on
   Windows). AuthStore.ensure_user (server/auth.py) and SrpStore.register
   (server/auth_srp6.py) now read-modify-write under the lock.
   Reproduced first: 3/4 tests red on unfixed stores (registrations lost,
   readers saw torn files). After: tests/test_users_store_concurrency.py 4
   passed (8/8 registrations persist in both stores; no torn JSON; parent-step
   paths refused). Mimosa gate story: two blocked drafts (path-traversal class
   on derived temp paths) until the estate mkstemp idiom + resolved-allowlist
   validation - the gate enforced, the shape changed, nothing was loosened.
   Windows conditions named: os.replace vs open reader handles = retryable
   PermissionError (5s cap); reader-side sharing violations during replace are
   contention, not torn bytes - the test contract distinguishes them.
2. **Same-class jacket, mag/game_world.py - FIXED.** The world store had it
   worse: bare except on corrupt JSON -> silent empty world -> next set_state
   WIPES the store; plus unlocked non-atomic write. Now: loud ValueError on
   corrupt (bytes preserved, nothing overwritten), locked atomic save via
   store_io. tests/test_game_world_store.py 3 passed; render neighborhood 11
   passed (one iteration: first cut called _save() without its argument - the
   failing run is this sentence).
3. **Q05 identity binding unwired - FIXED** (lane). identity_challenge /
   identity_proof wired through the op ladder (IDENTITY_AUTH_DISPATCH), session
   rows record key-bound identity (session_identities), allow_unbound_hello
   policy flag (False = identity mandatory on hello), protocol table promoted
   (IDENTITY_AUTH_DIGEST 9de8ad04e75e matches the V7 pin; sibling digests
   unmoved). tests/test_identity_wiring.py 7 passed; combined 92 passed exit 0.
4. **Q23 tape rows carry no actor class - FIXED** (lane). actor_class on action
   rows: bot rows stamped INSIDE the sha (world.py:388-394), player rows
   byte-identical (absent field IS the default), grandfathered pre-Q23 rows
   verify; verdict_feed.feed_tick(exclude_bots=True) consumer wired with
   bots_excluded reporting. 6 Q23 tests green; 86 passed in the server
   neighborhood (5 failures there were the persistence defect, next row).
5. **Persistence stress restore defect (root-caused by the Q23 lane) - FIXED**
   (lane). _apply_graph_spec restored open/primed but dropped stress AND
   fractured (server/persistence.py:88-90); replay diverged on any second
   snapshot ("want stress=0 vs logged stress=2"). Both restored with
   engine-default grandfathering; honest residue: pre-stress docs whose anchor
   is not the last snapshot still refuse (replay-as-verification, inherent).
   test_server_persist 5 failed -> 11 passed exit 0; neighborhood 82 passed;
   mountain_reveal 17 passed.
6. **Q28 GPS evidence_hash self-attestation - FIXED** (lane). Citation-resolution
   gate at append in tools/gps_mcp/ledger.py: evidence bytes recomputed at
   record (resolved=1) or the row lands UNVERIFIED-class (resolved=0, named
   citation); disagreement keeps the claim, flags EVIDENCE_MISMATCH; audit mode
   (`python -m tools.gps_mcp.ledger audit <db>`) re-walks and reports
   agreed/mismatch/unresolved. First caller wired (import_duel_bank).
   tests/test_gps_evidence_resolution.py 14 passed; combined 132 passed exit 0.
   Production ledger audit (byte-copy): 242 rows, 0 agreed, 242 unresolved -
   the finding stands, now visible; duel hashes still re-provable from
   logs/duel/duels.jsonl (63/63) but the ledger could not prove them until now.
7. **Q11 legality mirror covers only water verbs - FIXED** (lane). GDScript
   mirror (rule_parity_runner.gd) extended to all six verbs + RATE_CAP /
   STALE_NONCE / BAD_MAC keyless arms (tag arm needs session K = named v1
   debt); python twin extended in lockstep; receipt corpus family added (0.08
   share). Parity FULL 14,040 rows 0 diverged exit 0; 186 passed across the
   legality suites; godot parse checks exit 0 in both repos. Residue closed by
   coordinator: tools/legality_dataset.py was pinned to the 4-verb DEFAULT
   table (mislabeled say/whisper UNKNOWN_VERB in training data) - now sources
   CHAT_TABLE.verbs; 5 passed.
8. **Q15 - PREMISE STALE, row flipped.** The 3 red tests were closed by the R4
   refire window 2026-09-30 20:10 (receipt R4_FLOCK_PARITY.md); re-run 23
   passed / 46 passed / 22 passed, exit 0 each. Dated addendum appended to
   FIFTY_QUESTIONS_ANSWERED.md (rows never rewritten). Law re-learned: re-run
   the instrument before fixing any owed row.
9. **Optics standing-red test - FIXED** (lane). Not a standing red: a 5.36%
   flake, two collision modes in the grove's content-addressing (4.30% leaf
   cell collisions starve GROK_THRESHOLD; 1.06% knot-key/leaf namespace
   collision swallowed growth forever). Root fix: knot keyed in its own
   namespace (game.grok.<region>), test steers to threshold not steer-count.
   200/200 stress runs green; -k game 83 passed.
10. **Q48 effect broker production metering - FIRST REAL ROUTE LANDED** (lane).
    mag/state_snapshot.py capture_summary now files brokered board_write
    evidence with corr_id join (mint per AH14); broker banks meter rows on
    memory/runs/effect_broker/effects.jsonl (fail-visible: unbankable meter =
    FAILED receipt + exit 1). Production ledger EXISTS and grew on 3 real $0
    runs (row sample corr_id 5a480001 joins the pile row). Coverage honest:
    3 of 25,427 calls (0.012%) - the completeness problem is NOT solved; the
    25,427 writers still bypass the broker. Next organs named: duel_harness,
    improve candidate append. 8 new tests; 41 neighborhood passed.
11. **R2.5 estate_receipt_append - BUILT TO SPEC** (lane). Bridge tool per the
    mcp.md section-9 spec: wave/name regex + .. refusal, 65536-byte cap,
    resolve+prefix inside watch/inbox only, overwrite rotates to .bak_<ts>,
    INDEX.json never touched, {ok, path, sha256, bytes} return (sha256 =
    disk-byte truth, the falsifier arm). 8 tests (7 named + INDEX guard),
    50 passed across MCP suites exit 0. New tool pinned at first connect, no
    drift alarm; bridge profile declares 7.
12. **MCP-1 repin - DONE by coordinator under the fix-everything order.**
    Review: the estate_thought_compile drift IS the landed f7768cd10 design
    (COMPILE_SIZE_CAP bounds + local property; description hash unchanged;
    OUT_DIR pin intact); the 09-29 pin simply predates the landing by 53
    minutes. Repinned with reason naming the commit; pin --check on a fresh
    bridge manifest: rc 0, invalid 0. Bridge now serves 7/7.
13. **Fold debts:** logic.md written (coordinator fold from lanes/logic.json +
    logic.check.txt, provenance labeled, the 2 lane quote-misses stay misses);
    selfsteal section-6 addendum: all 7 finish-line receipts re-probed PROVEN
    (bytes named in the addendum).
14. **Re-seal by name:** live drift was keys.json + violation_baseline.json
    (0b846c01f D-wave landed unsealed) + mirrors.json (standing stealth-driver
    refresh, organ alive) + unsealed reverse_map_questions.json; all sealed
    with causes; 61/61 PASS. Warts named: tools/violation_ratchet.py
    baseline-update IGNORES unknown flags - "--help" EXECUTED a bulk register
    (14 rows); register is content-hash keyed so rows re-flag while lanes move
    files - final register happens at this window's commit.
15. **queue_closes_sweep latent NameError** (undefined ROOT; flagged by the
    R2.5 lane) - fixed with the module's own pin idiom; 4 passed.
16. **X intel drop filed** (watch/inbox/x_intel_drop_20261001.md): the
    NachoQuixotic rap is this estate's doctrine in verse by a stranger
    (bead/chain/residual/stateless seat/tesuji); thesupermannx =
    weight-crossover model mating (the mates-program mechanism, paper dig
    owed); ishaan_jaff = LiteLLM Lens (gateway-telemetry convergence with our
    broker doctrine + a name collision with THE LENSING); ollama log diagnosis
    (PTQ1_0 quant unreadable by 0.34.3 = /api/tags noise, blob likely intact,
    operator call; Vulkan GPU path healthy at 84-89 tok/s; "driver too old" is
    the ROCm probe only).

## Coordinator verification passes

- Combined server-side suite (server_v0 + persist + identity_wiring + chat +
  rooms + verdict_feed + frame_mac + auth_srp6 + realmd + protocol_table):
  151 passed, 2 skipped (live-realmd skips), exit 0, 10.44s.
- Sanity sweep -k "auth or store or game_world or srp": 76 passed.
- Config seal: 61/61 PASS. Pin check: rc 0.

## Wave 2 (all landed)- **Q22 ws mask enforcement - LANDED.** RFC 6455 5.1 strict-by-default:
  unmasked client frame -> close 1002 + drop, check at header parse;
  allow_unmasked_client=True opt-in restores the v0 leniency (the
  allow_plaintext_hello flag shape, inverted default). Caller census proved
  strict-default safe: WsDoor has ZERO production callers yet, browser
  WebSockets always mask, in-repo raw clients mask. tests/test_room.py 9
  passed (3 new); family 20 passed exit 0. Residue: fragmentation stays
  minimal-scope (named); mud_relay keeps its own leniency (separate owner).
- **Q27 verdict sid -> key binding - LANDED.** VerdictFeed identities param
  (the server's session_identities by reference); bound sid stamps
  identity_fingerprint INSIDE the gwap payload before row_sha256 (the
  actor_class precedent), receipt_sha256 recomputed over the extended body;
  unbound sids omit the field (grandfather law) with identity_fingerprint:
  None in reports; malformed binding refuses typed BAD_IDENTITY_BINDING.
  26 passed (4 new); neighborhood 216 passed exit 0. Residue: gwap scene-id
  regex caps 64 chars (granted sids must alias); attribution is
  per-feed-session not per-claim.
- **R2.0 docker surface parity - LANDED.** mag-mcp recreated from the
  2026-09-30 image (was running a dangling 09-26 build; no rebuild needed -
  the image postdates the last committed mcp touch and the uncommitted R2.5
  bytes must not bake half-landed). Standing tool tools/mcp_parity.py:
  per-transport manifest compare (stdio/http/docker) + image-digest stanza
  (the actual defect class), pin-withholds verdict-neutral + named,
  down-transport = named SKIP, exit 0/1/2 contract. Docker now fully green
  (served=17/17, image match); tests 16 passed exit 0. Residue: http gateway
  diverges on estate_receipt_append until the next sanctioned image rebuild
  (post-commit step, named below); mag-worker runs a dangling 09-23 image
  (operator call). Receipt: watch/inbox/ractor50/MCP_PARITY_R20_20261001.md.
- **Q02 hydrology/graded-head parity family - LANDED.** Four engineered
  shapes (cascade with guaranteed tick-1 boolean-vs-graded divergence,
  equalize, backwater/drowned-inlet, head_hill) + conductance/cross-section
  sweeps, 0.06 mix share; rung-1 fixed-point law as the oracle
  (mag.hydrology.HydrologyGraph). TWIN STATUS HONEST: the gd ENGINE twin
  exists (water_graph.gd Z10) but the parity RUNNER is boolean-only - the
  family is Python-oracle-FROZEN today (per-tick hashes banked,
  byte-reproducibility self-check, engine digest in latest.json so a dirty
  oracle cannot hide); the future runner extension diffs against the frozen
  corpus. PARITY ok exit 0 (hydrology 1 seq 0 diverged quick; all 8 families
  0 diverged); 92 passed across the water suites (6 new Q02 tests incl the
  both-directions divergence pin: cross-section flux 11/8/0 vs boolean
  100/100/100).
- **Q18 GDScript near-miss twin - LANDED.** The scalar verdict kernel
  (raw/strict/renorm margin rules) ported line-for-line to
  roblox_to_godot/tests/ldt_nearmiss_runner.gd; floats travel as IEEE-754
  double bits (Q14 law at 64 bits). Frozen corpus 92 rows (sha256-pinned):
  0 divergences across 1,104 compared values through real headless Godot
  4.3. Faithfulness chained (scalar == engine numpy == real evaluate_lattice
  aggregates); one bring-up instrument bug (hex codec) caught by the
  tau-echo guard and fixed, preserved in the report. 15 passed (7+8). Q18
  verdict: the FAIL closes; deeper port layers (MLP forward, propagator)
  named as the narrowing.

## Wave 3 (all landed)

- **Q40 gate-age patrol + gate register - LANDED.** configs/gate_register.json
  (7 rows, each receipt-cited; 5 open: adam-invite, nous-portal-topup,
  key-rotation, verkle-v2-flip, offsite-medium; 2 decided) +
  tools/gate_age_patrol.py (WARN-only, 14d bar, attention.md alert with
  same-day dedup, no-fabrication teeth: a register row without its receipt =
  exit 2). Live run exit 0 (oldest open: verkle-v2-flip 2d); WARN path proven
  via --days 1 --dry-run (exit 1, named gate, no pollution). 8 tests passed.
  No scheduling created (no-crons law; the operator recipe is named in the
  docstring). Sister-tool convergence named: gate_digest.py renders the same
  gates without alerting - the register seed_note orders one-edit updates.
- **Q36 flagger integrity arm - LANDED.** integrity_of() beside the shape arm
  (basis read from mag/trajectory_step, loud-fail if the owner's basis
  changes); TAMPERED only on comparable hash + mismatch; missing basis =
  hash_unverifiable (named); census line always prints the denominator.
  16 passed (5 new; a trajectory_minimizer fixture with a fake hash was
  aligned to an honest recompute, 15 passed). REAL FINDING on the live
  stream (copy-read, moment 2026-10-01T10:08Z, 39,344 rows): tampered 874,
  unverifiable 22, verified 38,412; cross-check reconciles exactly against
  the owner verify (39,336 - 38,404 = 932 = 874+22+36). The 874 span every
  stream day 09-05..09-30 and already fail the owner's own verify -
  tampering-or-schema-drift attribution stays with the operator. Residue:
  the 6165/36 baseline does not reproduce today (live stream, census law);
  anomaly_flagger 433 lines = registered debt.
- **Q33 dispatch-vs-landing join - LANDED.** tools/dispatch_landing_join.py
  over the real ledger (memory/runs/orchestrator/tasks/, 6,267 files, 317
  seat-dispatch rows). Match rule: tier-1 exact id in inbox evidence with a
  bulk-dump guard (>=8 ids = enumeration, not provenance); tier-2
  corpus-rare name tokens (>=3 shared, >=60% contained; the boilerplate
  clause killed 12 false PROVENs found on first live run). OUTBOX is
  deliberately not evidence (the dispatcher writes it itself).
  LIVE FINDING (read-only): PROVEN-LANDED 4 / CLAIMED-DONE-NO-RECEIPT 238 /
  FAILED 73 / OPEN 2, exit 1 - the fleet's dispatches land in OUTBOX, not
  the shared inbox; the fabrication-smell class is the norm and now
  visible. 12 tests passed.
- **Q51 estate CI workflow - LANDED.** .github/workflows/ci.yml: gates job
  (ubuntu, py 3.11 = venv match, fetch-depth 0): named-core pytest trio
  (59 passed at HEAD probe, exclusions ledger in the yml: live ports,
  ollama, godot win32 PE, the end_to_end skipif trap), ratchet FULL-tree
  mode (the --changed mode is vacuous on CI - empty scope), workflow-gate
  scenario suite. Honest: ratchet was RED at HEAD with 13 unregistered
  claims - all registered this fold, so CI lands green after this commit.
- **Q49 env/lockfile reconciliation - LANDED.** The conflict was tabfm's
  typeguard<3 hard pin vs evennia's inflect >=4; tabfm is an off-lock leaf
  whose AH9 trial is COMPLETE (receipt: overkill for clean tables) ->
  uninstalled with its verified orphan chain (jaxtyping, wadler-lindig,
  absl-py), typeguard restored to the lock's 4.6.0. pip check exit 0;
  canaries 61 passed twice (one unreproduced transient first run, named);
  requirements.txt +3 honest rows (pandas/sklearn/scipy - the
  pain_replication stack was declared nowhere). Residue: 5 lock extras
  remain (declared, unlocked; lock refresh is an operator call); tabfm
  refire re-breaks pip check (documented in its receipt).

## Fold gates + census (instrument + moment + delta, B2-216)

- RATCHET DEFECT FIXED AT ROOT: iter_py_files used glob (top-level only), so
  subdir debt (tools/gps_mcp/*, tools/pain_replication/*, mag/tests/*) was
  INVISIBLE to baseline-update while check --changed saw it - the two scopes
  could never agree (full-tree PASS + --changed FAIL on the same bytes).
  Now rglob; both scopes PASS; 15 hidden pre-existing rows surfaced and
  registered by name (gps_mcp ledger/router/test too-long, pain_replication
  HF_TOKEN env reads + except-pass + cwd-relative + too-long, mag/tests
  except-pass). Second wart twice-confirmed and filed: baseline-update
  ignores unknown flags (--help EXECUTES); Q02's lane hit it too and
  honestly reverted its claim.
- Register: 992 claims after the fold (919 + 15 hidden + the window's
  accepted growth rows). Config seal: 61/61 PASS.
- CENSUS: pytest --collect-only -q at 2026-10-01T10:2xZ: 3,953 tests
  collected / 484 files. Delta vs the AGENTS.md carrier (3,550/455,
  2026-09-30 census): +403 collected / +29 files. Attribution: this
  window's landings - new files test_users_store_concurrency(4),
  test_game_world_store(3), test_identity_wiring(7),
  test_gps_evidence_resolution(14), test_effect_broker_production(8),
  test_mcp_parity(16), test_gate_age_patrol(8), test_dispatch_landing_join(12),
  test_ldt_nearmiss_gd(8), plus the R4-window untracked test_game_constants
  and test_flock_parity files now committed, plus items inside existing
  files (rule_parity +6, server_v0 +4, verdict_feed +4, room +3,
  server_persist +2, anomaly_flagger +5, minimizer fixture alignment).
  Denominator law applies: collected != executed; no same-moment executed
  sum exists for this window (scoped runs only, each named in its row).
- LINKS: memory/corpus/LINKS.jsonl row fix-everything-20261001 (ledger
  224 -> 225).

## Final tally against the Q-table (22 FAIL verdicts)

FIXED this window: Q02, Q05, Q11, Q15(stale-flipped), Q18, Q21, Q22, Q23,
Q27, Q28, Q36(integrity arm; live rows reported not repaired), Q49, Q51 +
Q48 (first route landed, coverage honest) + optics-red + persistence-stress
(both root-caused inside other lanes' work). STALE-FLIPPED: Q15.
OPERATOR-GATED: Q10 (key rotation), Q07 (PAT scope). STAGED with reasons
(see Staged section): Q30/Q32, Q41, Q42, Q34, Q45, Q47.
UNKNOWN-frontier items were never in scope (no instrument exists: Q06, Q08,
Q14, Q19, Q24, Q26, Q50, Q52).

## Staged, not dispatched (named follow-ons with reasons)

- Q30/Q32 duel identity (weights hash, response-id, contender provenance):
  touches the ask-bank/duel-bank lineage mid-flight (D6 contamination work);
  needs its own spec sitting, not a rushed lane.
- Q41 steer anti-forgery verifier + Q42 steering-channel spoof rejection:
  security-design sensitive (secret mechanism + replay harness owed); design
  first per build discipline.
- Q34 attention metering (consumed/read_at on stealth findings): organ design
  choice (schema + who writes consumed_at), one-sitting spec owed.
- Q45 hand calibration audit (20-row), Q47 rib re-derivation patrol: audit
  instruments, next window's hygiene floor.

## Still operator-gated (unchanged)

- Q10 key rotation (the 7 live keys; exploit window open until rotated).
- Q07 verkle tip external publish (GitHub PAT scope; tip_witness exits 2 daily).
- Ollama PTQ1_0 model: remove/re-pull/run-via-llama-server = operator call.

(moved to the Fold gates section above - census 3,953 collected / 484 files, 2026-10-01T10:2xZ)

