# FIFTY_QUESTIONS_ANSWERED — every internally-answerable question RUN

2026-10-01 (session date 2026-09-29 context; instruments ran against the tree as it stands) ·
seat: ZCode R1 refire · file ownership: this file only · no commit · em-dash count: 0.
Source inventory: `watch/inbox/mountain_climb/FIFTY_QUESTIONS.md` (52 questions, Q01-Q52).
Every question with an instrument got the instrument RUN this session (greps, live tool runs,
test suites, hash comparisons, schema reads, executed probes). Verdicts are byte-backed; each
row names the check that ran. Tally: **18 PASS / 22 FAIL / 12 UNKNOWN**.

## Already-landed marks (per mission order)

| Landing | Receipt | Question impact |
|---|---|---|
| Parity fixed + standing gate | `watch/inbox/last_mile_20260930/D2_PARITY_GATE.md` | Q01 PASS (quick run green, pre-push gate pinned by test); R8 stress family also lands Q16 PASS |
| Identity binding V7 | `watch/inbox/last_mile_20260930/V7_IDENTITY_BIND.md` | module + 41 tests landed; Q05 still FAIL on the hello-path WIRING (see table) |
| Event ring B2 | `watch/inbox/last_mile_20260930/B2_EVENT_RING.md` | game.gd 64-slot drop-oldest ring + hud "+N dropped" + 6 tests (3-runs green); no owning question among the 52 (client display feed, AJ4's blindness) |
| Frame MAC R3 | `watch/inbox/last_mile_20260930/R3_FRAME_MAC.md` | Q03 PASS (wired in server/server.py, 16 tests green inside the 115-test run) |
| Artifact identity R6 | `watch/inbox/last_mile_20260930/R6_ARTIFACT_ID.md` | Q09 PASS (boot stamp, pck guard, swap-detect exit 1, manifest) |
| Bonus landed while answering: SRP6 upgrade R5 (2048-bit/SHA-256 default) -> Q04 PASS; quota ledger v0 (`watch/inbox/QUOTA_LEDGER.md`, tools/quota_ledger.py, 10 tests) -> Q39 PASS; census deep-check daily enforcement -> Q37 PASS; tip witness tool W3 (built, publish blocked) -> Q07 partial |

## The full table

| id | check-run (instrument, executed) | VERDICT | note |
|---|---|---|---|
| Q01 | `.venv/Scripts/python.exe tools/rule_parity.py all --quick --source refire` -> `PARITY: ok`, 6 families incl. new stress_domain, 0 diverged; `tools/rule_parity_out/latest.json` full 100/100 parity true; hook pinned by `tests/test_parity_gate_hook_pin.py` (in 115-pass run) | **PASS** | gate enforcing on twin change; would-have-caught proven on `9ed2c153f^` |
| Q02 | grep `cross_section|HEAD_SCALE|grade|hydrology` in tools/rule_parity.py gens -> 0 hits; families = mountain/gated_siblings/economy/fracture_loop/stress_domain/random | **FAIL** | no hydrology/graded-head family: gradient-head divergence untested both directions (frontier: small gen edit, D2's ownership) |
| Q03 | grep server/server.py: frame_mac wired (admit gate at decode->MAC->op ladder, `require_frame_mac`, mac_tamper chain row); `pytest tests/test_frame_mac.py` 16 passed (inside 115) | **PASS** | R3 landed; GDScript client port + s2c broadcast sealing owed (named in receipt) |
| Q04 | header + bytes of server/auth_srp6.py: `RFC5054_2048_N_HEX`, DEFAULT_GROUP rfc5054-2048, SHA-256, mangos-256 compat-flagged; `pytest tests/test_auth_srp6.py tests/test_realmd_client.py` green (inside 115) | **PASS** | R5 landed; 2048-bit default >= standard; vectors pass |
| Q05 | grep `identity_challenge|identity_proof|identity_binding` across server/*.py outside the module -> 0 wiring hits; protocol_table.py has no identity rows | **FAIL** | V7 module landed but hello path still requires/records no key-bound identity: any connection can hold a sid (wiring = frontier, rides the server.py lane) |
| Q06 | instrument NONE (the M4 itself) | **UNKNOWN** | frontier: offsite-byte replay on ARM macOS |
| Q07 | `tools/tip_witness.py` built (ratchet + 27 tests, W3); live `logs/tip_witness.log` 2026-09-30 19:19: `cannot verify: SCOPE - token cannot create gists (HTTP 403)` exit 2, alert appended; amendment second-key: absent | **FAIL** | witness BUILT but the checkpoint is NOT published: chain remains writer-only tamper-evident until the PAT scope is fixed; 618 evidence_lost amendment channel still single-key |
| Q08 | `watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md` read: DESIGN-COMPLETE, "nothing has been scheduled, nothing has been run" (medium unchosen) | **UNKNOWN** | frontier: physical restore drill (plan is ready-to-run) |
| Q09 | R6 receipt byte-read: BootIntegrity prints `ARTIFACT_ID git=<sha> pck=ok|FAIL` at boot, pck swap -> exit 1 (SWAPPED PCK), manifest in zip, -FromTheMountain build stamps dirty=0 | **PASS** | byte-reproducible rebuild + butler/wharf courier remain the next lane (owed, named) |
| Q10 | AG1 receipt + bytes: `redact()` in mag/trajectory_step.py before hash basis; `tools/precommit_secret_check.py` wired in githooks/pre-commit; steps.jsonl untracked+ignored; rotation: NOT landed (AG1 "Not done" #1) | **FAIL** | containment pipeline landed, but the 7 live keys remain unrotated in git history + on-disk pre-containment rows (operator call; the exploit window is open) |
| Q11 | verb inventory diff: server rows = boil/join/say/tag/valve/whisper; gd `_validate` + doc `verbs` = water-verb legality (UNKNOWN_SID/UNKNOWN_VERB/UNKNOWN_TARGET/DRY_POOL) only | **FAIL** | mirror covers the water subset; join/say/whisper + RATE_CAP/STALE_NONCE/BAD_MAC classes have no gd twin (offline accepts what the server rejects at receipt) |
| Q12 | `pytest tests/test_protocol_table.py` -> 25 passed (test_every_verb_routes, frozen rows, digest stability, unknown-verb typed reject) | **PASS** | every row routes; no shadow verbs |
| Q13 | `git diff --no-index roblox_to_godot/scripts/net_client.gd ..\the-mountain\game\scripts\net_client.gd` -> byte-identical (exit 0); grep githooks/CI for a twin gate -> none | **PASS** | identical today; standing diff gate absent (frontier, cheap) |
| Q14 | instrument NONE (no cross-language flock harness) | **UNKNOWN** | frontier: seeded-frame Luau/JS/GD comparison |
| Q15 | grep constants in flock.gd/fish_brain.gd: both now alias `GC.*` (game_constants.gd); `pytest tests/test_game_constants.py tests/test_flock_positive.py` -> **3 FAILED** (FOOD_PREF_DIST GC alias lost in flock.gd; FLEE_PUSH alias missing; TRAIL_RADIUS missing from mag/flock_positive.py) | **FAIL** | single-source landed but incomplete: 3 red tests prove the drift class persists inside one language |
| Q16 | R8 stress_domain family in the generator (volumes ~1e15-1e17); quick parity run: stress_domain 2 seqs, 0 diverged; float64/int guard noted in rule_parity.py:388 | **PASS** | integer-domain straddle now in every mode's corpus |
| Q17 | EXECUTED cross-language probe: adversarial names (combining accent, leading space, tab, CJK, empty) sorted + hashed in Python and in throwaway GDScript under headless Godot 4.3 -> identical order AND identical sha256 `08477f6b...b65f13` both sides (probe files deleted after) | **PASS** | encoding + sort order agree |
| Q18 | imports of tests/test_ldt_nearmiss.py: numpy + tools.* python modules only; no GDScript/godot references | **FAIL** | near-miss twins exercise the python engine only; the GD twin V5 caught diverging is untouched |
| Q19 | instrument NONE (no ws fault-injection test; test_room.py covers happy-path frames) | **UNKNOWN** | frontier: kill ws task mid-broadcast |
| Q20 | grep tests/test_anticheat.py for ws path -> 0 hits (all TCP Client); ws_door scope "text frames + ping/pong + close echo" | **UNKNOWN** | no ws-path anticheat test exists; identical-verdict claim untested (cheap extension, frontier) |
| Q21 | EXECUTED probe: 8 threads, 8 SrpStore sessions on one users.json -> **1/8 persisted, 7 users LOST** (last-writer-wins); shared-single-object variant 8/8 (GIL) | **FAIL** | confirmed torn/lost-write class on the account store; no lock, no atomic temp+rename |
| Q22 | read server/ws_door.py: mask optional (`mask = ... if masked else b"\0\0\0\0"`), header admits minimal scope (text+ping/close, no fragmentation); over-size refus
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 23337 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
lag, protocol table promoted (digest
  9de8ad04e75e matches the V7 pin); 7 new tests, 92 passed combined.
- Q23 FIXED this window: actor_class on tape rows (bot rows stamped inside the
  sha, player rows byte-identical, grandfathered old rows verify; verdict_feed
  can exclude bots; 6 Q23 tests green).
- Q28 FIXED this window: evidence-resolution gate at append in
  tools/gps_mcp/ledger.py (recompute from bytes or land UNVERIFIED) + audit
  mode; 14 tests; production ledger audit honest: 242 rows, 0 agreed (all
  self-attested - the finding stands, now visible and flagging).
- Q11 FIXED this window: gd legality mirror extended to all six verbs + RATE_CAP
  / STALE_NONCE / BAD_MAC keyless arms (BAD_MAC tag arm needs session K = v1
  debt, named); parity full 14,040 rows 0 diverged; 186 passed.
- Q48 IN FLIGHT at this addendum (broker production-metering lane); Q07/Q10 stay
  operator-gated (PAT scope; key rotation).

## ADDENDUM 2, 2026-10-01 fold (final tally of the fix-everything window)

Of the 22 FAIL verdicts at filing: 16 FIXED this window (Q02, Q05, Q11, Q18,
Q21, Q22, Q23, Q27, Q28, Q36, Q49, Q51, Q48-first-route, optics-red,
persistence-stress, legality-dataset verbs), 1 STALE-FLIPPED (Q15, prior
addendum), 2 OPERATOR-GATED (Q10 key rotation, Q07 PAT scope - unchanged,
exploit/publish windows open), 5 STAGED with named reasons (Q30/Q32 duel
provenance, Q41 steer verifier, Q42 steering-channel verify, Q34 attention
metering, Q45/Q47 audit instruments - see watch/inbox/fix_everything_20261001.md
Staged section). Consolidated receipt: watch/inbox/fix_everything_20261001.md.
Census at fold: 3,953 collected / 484 files (instrument pytest --collect-only,
moment 2026-10-01T10:2xZ; +403/+29 vs this file's session, attributed in the
receipt).

## ADDENDUM 3, 2026-10-01: Q10 + Q07-blocker corrections (stale reads owned)

Q10 "key rotation outstanding" is DONE per operator word (2026-10-01, "already
done self steal") and byte corroboration: HERMES keys rotated in 2026-09-30
(AJ9 receipt, commit e0ff8cec0: "values rotated in"; .env rewritten 09-30
10:07), steps.jsonl purged from git history in BOTH repos (main +
Mag-backup.git: git log --all -- memory/trajectory/steps.jsonl = empty),
containment rows AG1 unchanged. Residue: the first tip-witness gist still
needs one --publish --go fire (PAT scope is FIXED - live probe exits 0 in
dry-run, no 403), and KEY_ROTATION_JOURNAL.jsonl was never created (a
receipt gap, not a security gap). The fix-everything window's "still
operator-gated: Q10" row was a stale read of the 09-30 audit receipt - the
Q15 disease caught in this seat's own hand.
