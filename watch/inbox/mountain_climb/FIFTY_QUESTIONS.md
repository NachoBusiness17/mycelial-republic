# FIFTY_QUESTIONS — the systematic parity-class blind-spot inventory

Owner seat: ZCode (operator order "dig first", 2026-09-29). File ownership: this file only. No commit.
Method: THE_LENSING.md finding patterns, each enumerated against estate surfaces byte-read this session (`tools/rule_parity.py`, `roblox_to_godot/tests/rule_parity_runner.gd`, `server/auth_srp6.py`, `server/ws_door.py`, `server/rooms.py`, `server/identity_binding.py`, `server/protocol.py`, `mag/water_graph.py`, `mag/hydrology.py`, `mag/flock_grid.py`, `mag/effect_broker.py`, `mag/percolator.py`, `tools/gps_mcp/ledger.py`, `tools/anomaly_flagger.py`, `tools/census_drift_patrol.py`, receipts `V5_PARITY`, `B3_NETCODE`, `B5_BUILD`, `V7_IDENTITY_BIND`, `AG5_TIP_VERIFY`, `AC12_ORAL_LAW_2`, `GAP_ANALYSIS`, `BIBLIOGRAPHY`). Nothing below is invented: every check names a runnable falsifier or names NONE (frontier).

## The nine patterns (from THE_LENSING)

- **P1 twin-implementation divergence** — two implementations of one rule set drift silently (V5 PROVED it: 29/100 sequences diverge, GDScript double-spends spring volume on the shipping board).
- **P2 identity-as-label** — "who/what" recorded as a string, not as bytes a counterfeiter cannot forge.
- **P3 wrong-region sampling** — the instrument samples the estate's region (own bytes, own machine, own author) and certifies the region that matters (strangers, other hardware, WAN, adversaries) at n=0.
- **P4 liveness-vs-success** — "the organ fired" reported as "the organ worked".
- **P5 unauthenticated-surface** — a control path whose writers are unauthenticated (LATEST-WINS, plaintext channels).
- **P6 single-family-judging** — one judge (or judge kin to contestant) certifies the field.
- **P7 writer-only-tamper-evidence** — hash chain consistent to whoever holds the disk, truth to no one else.
- **P8 tool-scope-says-zero** — the librarian: a tool reports zero because its scope excludes the thing, and zero reads as clean.
- **P9 quota-unmetered** — the binding currency (window quota, attention, operator gates) has no meter; the metered currency (dollars) isn't binding.

Format per question: **id · pattern · surface** — THE CHECK (falsifiable test) · instrument (or NONE = frontier) · governing standard (from BIBLIOGRAPHY / THE_LENSING §6).

---

## TIER 1 — the ten whose bad answer breaks a core promise (verifiable play / sovereignty / continuity)

**Q01 · P1 · water engine twins (mag/water_graph.py vs systems/water_graph.gd).** V5 measured PARITY BROKEN (29/100, shipping-board family diverges at tick 5, GDScript manufactures water). CHECK: after the fix lands, `tools/rule_parity.py all --n 1000 --seed <new>` exits 0 with zero divergent sequences across all five families, AND a CI/pre-push row re-runs it (today it is a one-off untracked artifact). Bad answer = the differentiator ("same laws both sides of the wire") is marketing. Instrument: `tools/rule_parity.py` + `tests/test_rule_parity.py`. Standard: Bettner/Terrano "1500 Archers" — the determinism contract in production.

**Q02 · P1 · hydrology rung-1 twins.** `water_graph.gd` carries HydroNode (HEAD_SCALE 256, cross_section, line 49-99) and `mag/hydrology.py` is the Python rung — but the V5 generator families (mountain/gated_siblings/economy/fracture_loop/random) were authored before hydrology graded-head; none is named for it. CHECK: inspect `_seq`/gen code for whether boards vary `cross_section` and grade-sensitive volumes; if not, gradient-head divergence is untested in both directions. Falsifier: gen family with mixed cross-sections (1, 7, 1000, milli-depth edges), run `all`, count divergences. Instrument: `tools/rule_parity.py gen` (needs a new family = small edit). Standard: Dawson "Floating-Point Determinism" (here fixed-point, but the discipline is his: name the operation classes).

**Q03 · P5 · post-auth frame integrity (server/protocol.py).** Grep proves hmac exists only inside `auth_srp6.py` M1 compare; line-JSON frames after the SRP6 handshake carry no MAC and no TLS. CHECK: complete one srp6 login over the TCP door, then flip one byte of a subsequent move frame on-path; does the server reject? If not, every anti-cheat receipt and hash-chain row attributes forged moves to the authenticated identity. Instrument: a socket test in `tests/` (NONE exists — frontier-grade but cheap). Standard: RFC 5054 (K must key the record layer) / THE_LENSING §1 P2; pinned-cert `StreamPeerTLS` as the Godot-side fix.

**Q04 · P2 · SRP6 group + hash below standard (server/auth_srp6.py).** Header confirms N_HEX is the fixed 256-bit group, k=3, SHA1 throughout, imported verbatim from mangos realmd. CHECK: `len(N)*4 >= 2048` fails today; falsifier = an RFC 5054 2048-bit-group + SHA-256 port whose test vectors pass, or a documented retirement of SRP6 from this path in favor of TLS+pinned-cert+memory-hard hash. Bad answer = "auth never sees the password" is a 2^~70-offline-guess away from meaningless on a stolen users.json. Instrument: `tests/test_realmd_client.py` (vectors exist; group swap is the edit). Standard: RFC 5054 minimum group; OPAQUE (RFC 9807) at federation width.

**Q05 · P2 · identity binding not on the hello path (server/server.py).** `server/identity_binding.py` (V7) mints challenges and verifies sshsig, but grep shows no identity wiring in server.py — only srp6 and roster code. CHECK: connect, complete srp6, receive sid — was any key-bound identity required or recorded? If any connection can hold a sid, "external bytes the estate did not author" (P6-first-contact falsifier) is undecidable from the tape. Falsifier: a tape row whose actor field carries a verified key fingerprint. Instrument: `server/identity_binding.py` exists; wiring + tape row = frontier. Standard: THE_LENSING §2 SSH-key challenge; GitHub `.keys` as the publication anchor.

**Q06 · P3 · replay determinism never left one machine.** 202/202 frozen-tape replays are same-machine, same-arch (x86 Windows), and the gd runner binary is `tools/godot/Godot_v4.3-stable_win64.exe`. CHECK: run the frozen-tape suites on the M4 (ARM macOS) from offsite bytes only; 202/202 there, or name the first divergent tick. Bad answer = "every session is a receipt" is a single-libm-dependent claim. Instrument: NONE (the M4 itself). Standard: Dawson (libm/SIMD/summation-order classes); Gaffer's determinism-vs-authority tree.

**Q07 · P7 · the verkle chain is writer-only tamper-evident (mag/verkle_knot.py).** AG5 made tip writes atomic and boot verifies consistency — but `_verify_chain_consistent()` still proves only that leaves hash together; whoever holds the disk (operator, captured agent) can regenerate a consistent chain, and 618 evidence_lost / 2,821 amended rows are an unaudited amendment channel. CHECK: is any tip root published to a location the estate does not control (public commit, gist, transparency log), and does any amendment require a second key? If both are no, forge-test: rewrite one old leaf, recompute chain, ask verify — it passes. Instrument: `mag/verkle_knot._verify_chain_consistent` (demonstrates the pass = the failure); witness = NONE/frontier. Standard: Crosby-Wallach tamper-evident logging; RFC 6962 consistency proofs + gossip.

**Q08 · P9+P4 · continuity is one disk deep.** Backup is same-disk (audit row); the C2 restore drill (offsite encrypted copy → M4 → chain verify at published tip) has no receipt. CHECK: restore on a machine with no repos, run `_verify_chain_consistent()` at tip and `pytest -q`; any FAIL row = continuity promise broken by one disk failure. Instrument: NONE (drill is physical). Standard: in-toto/SLSA (provenance survives the rebuild); THE_LENSING C2.

**Q09 · P2 · artifact identity (B5 build).** B5 built `TheMountain.exe` from the estate twin `roblox_to_godot/`, not the public the-mountain tree at HEAD 7d5dbe2; receipt carries sha256s but no evidence the sha is printed at boot or embedded in the pck; exe+pck are separate files (a stranger can swap the pck). CHECK: swap the .pck with a modified one and run the exe — does anything detect it? And: does boot print the source commit? Both no = the thing a stranger runs is unverifiable against the public repo. Instrument: NONE (clean machine). Standard: Reproducible Builds / SLSA provenance levels; itch butler + Wharf as the courier alternative.

**Q10 · P5 · secrets are a pipeline, not an incident.** Seven live secrets sat in `memory/trajectory/steps.jsonl` because the trajectory logger records agent steps and agent steps contain secrets. CHECK: does a pre-commit/append-time scanner gate `steps.jsonl` and every new append path (grep for secret_gate wiring on trajectory_step), and has rotation landed? Plant a fake key in a step row, run the gate. Instrument: `tools/secret_gate*.py` exists; wiring-to-writer = the check. Standard: git-secrets/trufflehog class scanners; THE_LENSING §3 "rotate, purge, gate" order.

---

## TIER 2 — verifiable play surfaces (twin engines, game systems)

**Q11 · P1 · legality mirror completeness.** `rule_parity_runner.gd` _validate covers UNKNOWN_SID/UNKNOWN_VERB/UNKNOWN_TARGET/DRY_POOL for verbs boil/valve/tag. CHECK: diff `server/protocol_table.py` verb rows (and server/world.py validate branches) against the gd _validate switch — every server reject code must have a gd twin or offline mode accepts/labels what the server rejects. Instrument: `tools/rule_parity.py compare` verdict fields + a static diff script. Standard: Yan/Randell cheat taxonomy (logic-modification class).

**Q12 · P1 · protocol table vs dispatch parity.** Frozen table rows compile to handlers (B4/LW6 law); CHECK: a test asserting every table row maps to a handler and every dispatched op maps to a row (no shadow verbs). Falsifier: one op reachable with no row, or one row with no handler. Instrument: `server/protocol_table.py` + `tests/`. Standard: protocol conformance (RFC-style registry discipline).

**Q13 · P1 · net_client.gd repo twins.** B3 diffed estate `roblox_to_godot/scripts/net_client.gd` vs the-mountain's byte-identical AT THAT MOMENT. CHECK: re-run the diff today and gate it (any hook/CI row?). Drift = the public repo ships client bytes the estate never tested against its server. Instrument: `git diff --no-index` (exists, ungated). Standard: single-source-of-truth; Reproducible Builds.

**Q14 · P1 · flock triple-source port.** `flock.gd` header says ported from `dashboard/static/games/swarm.html` + `roblox/src/shared/Flock.luau`; `mag/flock_grid.py` is a fourth (numpy). CHECK: feed one seeded frame to Luau and GD ports (or JS), compare positions after N ticks. No harness exists. Instrument: NONE. Standard: Dawson-class determinism; the 1500-Archers contract generalized.

**Q15 · P1 · live constant drift inside the client tree (flock.gd vs fish_brain.gd).** Bytes prove it: flock.gd FLEE_RADIUS=20.0 (Z14 push) while fish_brain.gd:30 still reads `const FLEE_RADIUS := 14.0`, excused as "its lane's call". CHECK: grep every shared constant (CATCH/SCHOOL/TRAIL/TIRED/POOL_PREF) across both files, diff, and pin with a test. This is V5's disease inside ONE language. Instrument: grep + a constants test (NONE). Standard: single-source-of-truth law (estate's own).

**Q16 · P1 · integer-domain parity (64-bit caps).** Python ints unbounded, GDScript 64-bit; `depth = volume * DEPTH_SCALE / cross_section` (volume*1000) can cross 2^63 on stress boards. CHECK: gen family with volumes ~1e15-1e17, run both engines, compare hashes + overflow behavior. Instrument: `tools/rule_parity.py gen` custom family. Standard: Dawson (representation classes).

**Q17 · P1 · canonical hash on non-ASCII names.** State hash = sha256 over canonical text; node names sorted as strings. CHECK: gen boards with unicode/CRLF-risk names, verify python hashlib and gd `sha256_text()` hash identical bytes (encoding + sort order agree). Instrument: rule_parity with adversarial names. Standard: canonical serialization (Reproducible Builds' archive-ordering discipline).

**Q18 · P1 · near-miss twin corpus scope.** 600 near-miss twins + propagator oracle (`test_ldt_nearmiss.py`, `test_propagator`). CHECK: do any near-miss cases exercise the GDScript side, or only `mag.water_graph`? If only python, the twin that V5 caught diverging is the twin the twins never touch. Instrument: `tests/test_ldt_nearmiss.py` imports. Standard: 1500 Archers (determinism must be tested as a contract, not assumed).

**Q19 · P3 · dual doors, one liveness (server/ws_door.py vs TCP door).** ws_door is asyncio, the TCP door blocking sockets; two transports, one world. CHECK: kill/hang the ws task mid-broadcast — does the TCP door or the room pump notice, or does the room tick on half its peers forever (head-of-line inverse)? Instrument: a fault-injection test (NONE). Standard: Gaffer transport series; EVE GDC load-shedding (degrade visibly, never silently).

**Q20 · P1/P5 · three surfaces, one anticheat gate.** TCP door, ws door, rooms — LW7's anti-cheat receipt gate is wired where? CHECK: connect via ws_door, stage the same illegal verb sequence the TCP tests use; identical verdicts and receipt rows? Instrument: `tests/test_anticheat.py` (extend to ws path). Standard: Yan/Randell (protocol manipulation class).

**Q21 · P5 · users.json / SrpStore concurrent write safety.** JSON-file stores, no DB. CHECK: N concurrent registers/logins on one store file — torn write or lost user? Instrument: a threading test against `server/auth_srp6.SrpStore` + `server/persistence.py`. Standard: persistence ACID discipline (EQEmu DB-driven contrast in BIBLIOGRAPHY §2).

**Q22 · P3 · ws_door RFC 6455 conformance.** Hand-rolled frame logic ported from mud_relay. CHECK: send unmasked client frames, fragmented frames, masked payload with the 1 MiB cap boundary, close-frame mid-message — reject per RFC or misparse? Instrument: byte-level ws test (NONE). Standard: RFC 6455 itself.

**Q23 · P2 · innkeeper provenance in the tape.** Server-side tapes record moves; is the bot's actor class distinguishable from a player's? CHECK: read a tape row schema for actor type; if absent, GWAP-style agreement rounds can be satisfied by the bot. Instrument: `server/room.py` / persistence row schema. Standard: von Ahn CACM 2008 (participant independence is a design property, not an assumption).

**Q24 · P3 · snapshot interpolation clock domain.** `snapshot_buffer.gd` stamps arrivals with a LOCAL monotonic clock. CHECK: two clients, +2s clock skew, same server — do rendered worlds diverge (one living 2s in the past)? Not a rules break, but "what the player saw" stops matching "what the receipt proves". Instrument: a two-client bench (NONE). Standard: Gaffer "Snapshot Interpolation"; Source wiki (interpolation delay budget).

**Q25 · P1 · rooms cross-isolation.** rooms.py makes isolation structural (peer in exactly one room). CHECK: hello targeted at room A, then a verb aimed at room B's world node — structurally unreachable or routing-level reachable? Instrument: `tests/` rooms tests (extend with cross-room probe). Standard: EQEmu zone separation (BIBLIOGRAPHY §2).

**Q26 · P3 · load region n=0.** Server tests bind localhost with a handful of connections. CHECK: 50/500 concurrent peers × 60s on one room — tick time distribution, broadcast backlog, memory. First contact with 3 strangers on a WAN would already be new data. Instrument: a load bench (NONE). Standard: EVE single-shard GDC (measure before shedding); Gaffer tickrate-as-budget.

**Q27 · P5 · verdict feed integrity.** `server/verdict_feed.py` — are verdict rows bound to a session/connection id that is itself key-bound (see Q05)? CHECK: schema read + forge test (write a verdict row from a second connection under the first's label). Instrument: verdict_feed row schema; identity = Q05 dependency. Standard: Baughman/Levine cheat-proof playout (binding claims to unforgeable handles).

**Q28 · P8 · GPS record_verdict evidence channel.** record_verdict accepts `evidence_hash: str = ""` and never resolves it (lensing §6.1 defect 2, still visible in ledger.py:182-197). CHECK: submit a verdict whose evidence_hash is empty or fabricated — does any code path recompute it from artifacts? If no, GPS rows are self-attestation. Instrument: `tools/gps_mcp/ledger.py` + a forge test. Standard: GWAP output-agreement (verification must be a side effect of independent action, not a form field).

**Q29 · P6 · GPS positive-floor Goodhart (LM7).** The floor clamps fails during rising windows so "recording a fail is never a way to gain standing". CHECK: simulate a cheap-pass pump (passes to open a rising window) alternating with true fails — can pass_rate ratchet above true rate? Instrument: a ledger simulation test. Standard: Goodhart/reward-hacking (the estate's own AC10 law); Foldit scoring literature as the honest-scoring contrast.

**Q30 · P2 · duel family identity.** Families keyed on catalog model names; the lensing's provider-weight-swap kill applies (Nous serves both contestant and catalog label). CHECK: does any duel row bind the judge/contestant to a weights hash, response-id, or provider-attested digest? Instrument: `tools/w8_series_duel.py` row schema. Standard: single-family judging kill (THE_LENSING §2); independence requirement from von Ahn CACM 2008.

**Q31 · P6 · judge-family census today.** AJ1 landed an alt-judge harness (`aj1_alt_jrozen` files exist). CHECK: count DISTINCT judge families in the duel ledger with >=1 W-series rejudge receipt after AJ1; if <2, the p=0.0156 six-coin inference still stands alone. Instrument: `tools/aj1_alt_judge.py` + `memory/workflows` receipts. Standard: GWAP independence; basic experimental design (blocked judging).

**Q32 · P6 · glm self-contamination rerun.** W8 glm row marked session-authored. CHECK: do fresh same-ask glm API answers (not seat-authored) exist post-V8 with a receipt? If no, the 6-0 is the seat grading itself. Instrument: `w8_contenders_20260930.jsonl` provenance fields. Standard: contest/judge separation (Foldit's scoring was never player-attested).

---

## TIER 3 — estate meters, memory organs, fleet, build

**Q33 · P4 · mates dispatch liveness.** Mates can dispatch PROVEN while child execution is BROKEN (lensing §1). CHECK: join dispatch rows to landing receipts; count PROVEN rows with no completed child artifact in the last 30 days. Instrument: `mag/seat_dispatch.py` + receipt tree (cross-join script NONE). Standard: Google-SRE-style alert on outcomes (outside bib: NONE) — the estate's own "trust bytes, not reports".

**Q34 · P4 · stealth fleet consumption.** Heartbeat cycle 235 proves the loop ran, not that findings were read. CHECK: is there any consumed-at/read-at field on stealth findings; if not, the fleet's output currency is unmetered production. Instrument: `tools/stealth_*.py` outputs + `memory/attention.md`. Standard: NONE (frontier — attention metering).

**Q35 · P4 · improve loop success metric.** `improve --status` reports runs; CHECK: date of the last PROMOTED candidate vs last RUN — if promotions are weeks stale while runs are daily, the organ fires without working. Instrument: `mag/improve.py --status` + `memory/improve/`. Standard: NONE (internal law: pile habit).

**Q36 · P8 · anomaly flagger shape-only hashes.** anomaly_flagger checks step_hash SHAPE `[0-9a-f]{16}`, never recomputes (its own header says recomputation stays with trajectory_step verify). CHECK: mutate row text, keep hash shape — flagger exits 0? Then "clean" means "well-formed", not "intact". Instrument: `tools/anomaly_flagger.py` + a tamper test. Standard: Crosby-Wallach (verification = recompute, not inspect).

**Q37 · P8 · census patrol inner-file blindness (B2-244 known-open).** Default patrol sees file growth only; `--collect` deep check is opt-in. CHECK: append a parametrize inside an existing test file, run default patrol — exit 0 while the carrier count is now wrong. Known debt; the question is whether anything enforces the deep path daily (MagCensusPatrolDaily log START today). Instrument: `tools/census_drift_patrol.py`, `logs/census_patrol.log`. Standard: the estate's own census denominator law (B2-216).

**Q38 · P8 · secret scanner scope vs actual secret geography.** The leak was in `memory/trajectory/steps.jsonl` — was that path in the scanner's scope before the audit? CHECK: list scanner roots from `tools/secret_gate_rules.py`; diff against every jsonl/json the fleet writes (`memory/runs/`, trajectory, briefs). Any writer path outside scope = the librarian again. Instrument: `tools/secret_gate_scan.py`. Standard: trufflehog class coverage discipline.

**Q39 · P9 · quota ledger absence.** Dollars metered to the call; the 5h rolling window that killed a 20-wide window has no ledger. CHECK: search for any per-account rolling-window counter; if none, build the falsifier: two bursts 4h apart vs the wall — predicted hold/fail from the ledger vs observed. Instrument: NONE exists; `mag/cost_ledger.py` is the natural home. Standard: NONE (frontier); the driving-ladder ribs (RIB_DRIVING_LADDER) hold the law without the meter.

**Q40 · P9 · operator-gate clock.** Three operator-only gates (Adam invite, Nous top-up, Phase-2 GO) can stall indefinitely; no "gate open N days" row exists. CHECK: grep attention.md/queue for any gate-age row; if absent, lanes burn quota behind silent gates without an alarm. Instrument: `memory/attention.md` (row absent = answer). Standard: NONE (frontier); THE_LENSING §3 names it.

**Q41 · P5 · STEER forgery.** Anti-forgery is a field any file-writer can set (lensing §1). CHECK: write a steer row with the anti-forgery field set by a non-operator process; does any consumer verify? Instrument: `mag/steer.py` read path + forge test. Standard: signed operator intent — the V7 sshsig pattern applied to steering; RFC 6962 gossip as the witness analog.

**Q42 · P5 · phone/Discord steering channel.** Hermes phone path is Discord plaintext. CHECK: replay a steering message spoofed from the operator's handle (in a test harness) — anything reject it? Instrument: `mag/phone_door.py`/`hermes_steering.py` auth surface. Standard: THE_LENSING §3; pinned-TLS rule from C1.

**Q43 · P7 · shared-surface receipt binding.** SHARED_SURFACE_CONTRACT says preserve hashes and bounded pointers. CHECK: tamper one byte of a receipt payload but keep its recorded hash — does `mag.shared_surface validate` recompute and fail, or trust the recorded hash? Instrument: `.venv/Scripts/python.exe -m mag.shared_surface validate` on a poisoned copy. Standard: in-toto layout verification.

**Q44 · P4 · verkle compaction vs verification (AG5 adjacent).** Compaction (`mag/verkle_compaction.py`) rewrites history representation while `_verify_chain_consistent` re-derives. CHECK: run verification against a compacted chain from a RESTORED copy (not the live tree) — does the compacted form verify standalone, or only with sidecar state? Instrument: `tests/test_verkle_compaction.py` + a restore drill. Standard: Crosby-Wallach (proofs must survive representation changes).

**Q45 · P6 · percolator lexicon judging with no external calibration.** Percolator classifies SIGNAL/THEATER/NOISE by lexicon, deterministically, no LLM — a single judge family of one (the lexicon author). CHECK: hand-audit 20 NOISE rows against raw inputs; count false negatives (real signal filed as noise). Any hit rate below, say, 90% = the invariant compiler eats signal. Instrument: `mag/percolator.py` + manual audit. Standard: inter-rater reliability (outside bib: NONE; honest gap).

**Q46 · P3 · oral-law index sampling honesty.** 93 rows from 852 grok sessions, digest-recipe sampled; laws cite digest text, not full threads. CHECK: pick 5 random laws, verify each against the RAW thread bytes (not the digest); any law unverifiable at raw depth = the index carries digest artifacts upward. Instrument: `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` + `corpus/oral_history/seat_pools/`. Standard: source-traceability (the index's own falsifier law, AC12).

**Q47 · P2 · rib freshness vs rib truth.** AGENTS.md names rib warm-up as law; ribs are prose files with hand-written claims (the census bullet itself was once hand-copied). CHECK: for 3 load-bearing ribs (FREE_USAGE_POLICY, DRIVING_LADDER, LANE_WINDOW_BOOT), does any instrument re-derive the rib's numbers from bytes (the way census_drift_patrol now does for the census bullet)? Instrument: NONE generalized — the patrol pattern is the template. Standard: the estate's own "trust bytes, not reports".

**Q48 · P3 · effect broker coverage vs doctrine.** Broker docstring: "Every side effect in MAG must route through this broker"; delegates are model_call + lane_spawn only (AH18 "real-but-narrow"), denylist history includes the empty-string incident. CHECK: count metered provider calls in `memory/runs/effect_broker/effects.jsonl` vs the cost rollup's 24,939-call denominator; the gap = effects outside the broker. Instrument: `tools/cost_rollup.py` vs effects.jsonl join. Standard: reference-monitor completeness (the broker's own cited pattern).

**Q49 · P1 · requirements.txt / dependency twins.** Merge markers were found once (AG2). CHECK: `pip check` + `requirements.lock` vs a fresh-venv install from requirements.txt on the clean machine; drift = the estate's environment is a twin of its lockfile, unverified. Instrument: `scripts/ensure_venv.ps1` + lock diff. Standard: Reproducible Builds (environment reproducibility).

**Q50 · P3 · clean-machine first run (the stranger simulation we can do today).** No headless gate covers SmartScreen/AV/first-run of the B5 zip. CHECK: fresh Windows VM (never had the repos): download zip, unzip, run — record SmartScreen prompt, AV interference, boot-to-board time, crash log. Instrument: NONE (a VM). Standard: Reproducible Builds; the itch butler/GOG offline-installer distribution bar.

**Q51 · P3 · CI green vs game-executed gap.** the-mountain CI is self-declared "no-engine" (syntax/UTF-8 only; GAP_ANALYSIS row 6). CHECK: does any CI job on either repo run the server test suite or one headless godot frame? Grep `.github/workflows/` for pytest/godot invocations. If none, green CI certifies spelling, not play. Instrument: CI config read. Standard: CI red-blocks-merge discipline (the estate's own scenario-gate pattern ported to the game).

**Q52 · P3 · contact-log for first contact (contamination bound).** P6's "seat stays quiet" is discipline, not a gate; nothing records seat-to-Adam contact. CHECK: does any log/instrument exist that would show, post-contact, which friction points Adam hit unaided vs after a hint? If none, N=1 evidence is quietly co-authored and unverifiable. Instrument: NONE (build: contact log + pre-registered silence rules). Standard: pre-registration (P8 fix pattern); GWAP independence discipline.

---

## Ranking honesty

- 52 questions: 10 Tier-1 (core-promise breakers), 22 Tier-2 (verifiable play), 20 Tier-3 (estate organs).
- Instruments named NONE (frontier) on: Q03 (frame-MAC test), Q05 (wiring), Q06 (M4), Q08 (drill), Q09/Q50 (clean machine), Q14 (flock parity), Q24/Q26 (bench), Q34/Q39/Q40/Q45 (attention/quota/calibration meters), Q52 (contact log) — these are the asks the next paid pass should carry.
- Byte-verified anchors already in hand: V5 parity BROKEN 29/100 (`watch/inbox/last_mile_20260930/V5_PARITY.md`); fish_brain.gd:30 FLEE_RADIUS=14 vs flock.gd FLEE_RADIUS=20; no frame MAC in `server/protocol.py`; SRP6 256-bit N + SHA1 in `server/auth_srp6.py` header; identity module unwired in `server/server.py`; record_verdict's unverified evidence_hash (`tools/gps_mcp/ledger.py:182`); rule-parity families lack a hydrology family.
- Feeds: the ractor pass (patterns → essay) and the next deliberate ask (the NONE rows are the ask list).
