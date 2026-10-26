# w4-10: A temporal type system for artifact freshness, built from freshness_check.py + census_drift_patrol.py

2026-09-28, flash50 deep item w4-10. Read in full this session: `tools/freshness_check.py` (309 lines) and `tools/census_drift_patrol.py` (404 lines). The AGENTS.md Clippy bullets (B2-215, B2-216, B2-244, B2-245, B2-249, B2-274, B2-338) are ask-provided workspace material. A sibling artifact in this directory, `deep-temporal-types.md` (17,203 chars), already inventories the estate's four age ladders, four time bases, and three grandfather mechanisms. This item does not repeat that census. It develops the theory the two named gates embody: what a freshness type IS, when demotion may fire, when promotion is sound, and what a consumption-time checker must re-derive at every read. The design contribution is that the five requested states are not a chain but a partial order indexed by consumption position, and that demotion is a motion-relative conjunction rather than a TTL.

## 0. Receipts (commands run this session, read-only)

```
$ ./.venv/Scripts/python.exe tools/freshness_check.py
FRESHNESS: repo heartbeat 0.0d since last commit (alive=yes; bar: stale=7d, heartbeat=2d)
  BOOT_4_7.md: 2.9d old  [frozen-ok]
  state/CURRENT.md: 1.5d old [untracked-mtime]  ok
  state/START_BRIEF.md: 0.1d old [untracked-mtime]  ok
  state/HANDOFF.md: 2.4d old [untracked-mtime]  [frozen-ok]
(exit 0)

$ ./.venv/Scripts/python.exe tools/census_drift_patrol.py
CENSUS-PATROL: ok - census 2026-09-27 (2303 collected / 352 files)
  grew: 2026-09-28 tests/test_silentpass_batch2.py   (5 files listed, all dated 2026-09-28)
  disk candidate files: 369
CENSUS-PATROL: ok - census 1d old of 7d bar, growth noted but inside the window
  (5 file(s) since census), disk 369 vs carrier 352 (instrument lag ...)
(exit 0)

$ ./.venv/Scripts/python.exe tools/freshness_check.py --self-test
RECEIPT SELF-TEST: PASS   (18 ok checks: fresh/re-hash/drifted/None/non-dict/
missing-hash/unparseable/future-dated/naive-UTC/json round trip/...)

$ ./.venv/Scripts/python.exe tools/census_drift_patrol.py --self-test
CENSUS-PATROL SELF-TEST: PASS   (30 ok checks, including: "the real 12-day
fossil is STALE"; "age exactly at bar passes with growth"; "age bar+1 without
any growth is OK"; "over-direction is instrument lag, not stale"; "future
census is UNVERIFIABLE exit 2"; four hook-pairing checks)
```

Three live facts to keep. First, the census carrier is AGING right now, not Fresh: 1 day old, 5 test files committed since the snapshot, disk candidates 369 against the claimed 352, verdict ok with growth named. Second, two boot docs are Fossil live (`BOOT_4_7.md`, `state/HANDOFF.md`, both `[frozen-ok]` via the register at `tools/freshness_check.py:44-51`). Third, the patrol self-test vectors are already the typing judgments of the system below, pinned as executable tests. NOT run: the `--collect` deep check (needs a full pytest collection pass through the venv; the ask's named work was reading and design, and I report it as not run rather than approximating it with the default gate).

## 1. Staleness is relative motion, not absolute age

Both gates refuse to demote on age alone, and this is the load-bearing discovery of the dig.

- Boot docs: `is_stale = heartbeat and age > STALE_DAYS and not frozen` (`tools/freshness_check.py:292`, with `STALE_DAYS = 7`, `HEARTBEAT_DAYS = 2` at lines 53-54). Old doc plus a heartbeat is the disease (the doc is being left behind by a moving repo). Old doc in a silent repo is not flagged at all.
- Census claims: `stale = age_days > max_age_days and grew` (`tools/census_drift_patrol.py:265`), where `grew` is committed test-file additions after the census day or a disk count that shrank below the claim (lines 261-264). The patrol's own docstring states the doctrine: "The tripwire fires only when the snapshot is old AND the world moved under it" (line 21-22), and the self-test pins the boundary: bar+1 without growth passes.

So demotion is a two-place predicate over (artifact age, world motion), not a one-place TTL. Formally: `stale(c) = age(c) > B  AND  exists a provable witness w with W(now) != W(t_c) on c's scope`. Compare HTTP caching (RFC 7234 section 4.2), where a response goes stale on age alone and every stale reuse owes a revalidation. The estate's conjunction moves that cost: the demotion signal itself (a git log scan, a directory glob) is the cheap proof that a re-read would find something different. A TTL system sometimes demotes and finds nothing; this system demotes only when motion is already witnessed, which is why the patrol can afford to run on every pre-push.

Two refinements make the motion witness a typed value rather than a boolean:

1. Direction typing. On the disk-count arm, only shrink is a provable drift witness; the over-direction is the constant zero-collect instrument gap and is evidence only, never a demotion trigger (B2-247 rationale in the docstring at `census_drift_patrol.py:15-17` and the pure core at lines 250-258; the self-test names it: "over-direction is instrument lag, not stale"). The witness therefore carries a direction and only the provable direction fires demotion.
2. Provenance typing. On the growth arm, only git-committed additions count (`test_files_added_since`, lines 219-247); a fresh untracked test file on disk never demotes the carrier. Both arms of `grew` require provenance: a commit record, or a subset relation violated (`disk_files < carrier_files`, possible only if files were deleted or the claim invented).
3. Scope typing. The two gates witness motion at different granularities: the freshness gate uses repo-global heartbeat (any lane's commit keeps every boot doc un-demoted, `freshness_check.py:272`), while the patrol witnesses `tests/`-scoped growth. Scope is a parameter of the type: coarser scope means more tolerated drift before demotion.

A corollary the estate already lives with: in a fully silent repo, freshness goes vacuous. Everything passes as ok because nothing is being left behind. The patrol self-test pins the same vacuity in directory scope ("age bar+1 without any growth is OK"). Read as a bug this looks like flattery; read as theory it is correct: a snapshot frozen in a world that stopped moving is not stale, it is a historical record.

## 2. The state space: five names, a partial order, and three kinds of death

The five requested states, with their exact instantiations in the two gates:

- **Fresh**: age inside the bar, witness verified. The receipt layer's strongest form requires both arms: `fresh: age Xs of Ys bar, source hash verified` (`freshness_check.py:192-193`).
- **Aging**: inside the stale bar but with named drift signals. The patrol prints exactly this state live today: "growth noted but inside the window (5 file(s) since census)" plus the instrument-gap detail (lines 280-287). The deep check adds a numeric tolerance band, `COLLECT_DRIFT_TOLERANCE = 20`, symmetric in both directions (lines 122-125, 197-216): Fresh/Aging is a quantitative boundary on measured delta, not only on time.
- **Stale**: age beyond the bar AND witnessed motion (both gates' conjunction, section 1).
- **Fossil**: old by registration, never by aging. Entry requires a registration act carrying reason plus date (`FROZEN_OK`, `freshness_check.py:44-51`, header self-declaration required by the module docstring lines 12-14), or the frozen-vector law B2-274 for the patrol's regression fixtures (`census_drift_patrol.py:96-116`).
- **Dead**: absent, unverifiable, or corrupt. This is not one state but three, with different exit semantics: verified absence (a missing boot doc sets `is_stale = True` and exits 1, `freshness_check.py:289-290`: absence is itself a verified finding); meter failure (git failure refuses to guess and exits 2, `freshness_check.py:57-62`, `PatrolError` at `census_drift_patrol.py:231-232`); corrupt witness (future-dated beyond tolerance, `census_drift_patrol.py:310-312` with `FUTURE_TOLERANCE_DAYS = 1` at line 80, or the receipt layer's clock-skew guard `CLOCK_SKEW_SECONDS = 300` at `freshness_check.py:86` and the future arm at lines 179-180).

The ordering that matters is NOT the naive chain Fresh > Aging > Stale > Fossil > Dead. For consumption positions that want live truth, that chain holds with Fossil aside. But the B2-274 ownership law shows Fossil is orthogonal, not below Stale: the frozen regression vectors exist precisely because they must NOT track the live count ("the live count moving (1,837 -> 1,879 -> 1,910 in one day) must not move the fixtures, because a frozen vector is the only witness that can catch a grammar break", `census_drift_patrol.py:104-110`). A fossil that silently refreshed would be a BROKEN fossil. So in WITNESS position, becoming Fresh is the violation. The type judgment is position-indexed: State(position, artifact), not State(artifact). The same physical bytes are authoritative in LINEAGE position exactly because they are disqualifying in LIVE_TRUTH position.

The patrol's measured failure mode proves the custody separation is necessary, not decorative (B2-274 experiment, lines 111-116): reword the live AGENTS.md bullet and, with the parser unchanged, the self-test and pytest stay GREEN while the live patrol fail-closes exit 2. Grammar (the regex plus comment, lines 96-116), live data (the AGENTS.md bullet), and regression vectors (self-test and tests) form a three-body custody separation, the same parser/spec/fixture split language engineers use, and the failure is only visible from the third body.

## 3. Witnesses and clocks: a claim is well-typed only at a pinned grammar

`parse_carrier` (`census_drift_patrol.py:148-170`) returns None unless the claim sits in the canonical clause shape `N tests [collected] / M files (YYYY-MM-DD census` (regex at lines 117-119). The B2-245 history explains why the grammar is anchored on the parenthesized clause: the retired regexes took the FIRST date and the FIRST counts anywhere on the bullet, so tripwire prose ("31 files grown") silently became the parse (lines 85-95). This is the "make illegal states unrepresentable" move applied to prose: a claim that cannot be typed is Dead (exit 2), never loosely interpreted. The B2-249 carrier shape law in AGENTS.md is the same discipline enforced on the writers' side: editing the bullet into any other grammar breaks the gate loudly instead of quietly re-typing the claim.

Three clocks are in production across these two files, each with a matching corruption check, forming a trust gradient:

| clock | where | corruption check |
|---|---|---|
| mint time (embedded receipt `observed_at`) | `freshness_check.py:111-133` | future beyond `CLOCK_SKEW_SECONDS = 300` rejected (lines 179-180); unparseable rejected (174-176) |
| commit time (git `%cI`) | `freshness_check.py:65-73` | git failure exits 2, never guesses (57-62) |
| self-declared valid time (census date inside prose) | `census_drift_patrol.py:310-312` | future beyond 1 day = "fabrication smell", exit 2 |
| mtime fallback (untracked docs) | `freshness_check.py:282-287` | none: a later touch refreshes it without content change; weakest |

In bitemporal terms (Snodgrass's temporal databases; SQL:2011 system-versioned tables), the hand-copied census disease is exactly a claim whose valid time froze while transaction time ran on: the "1,341 tests / 264 files" headline was typed by no instrument after 2026-09-14 and rode 12 days (patrol docstring lines 4-7). The receipt layer is the estate's bitemporal correction: a claim may only be consumed through a witness that names its transaction time and re-verifies content identity.

## 4. Demotion rules (automatic)

As a transition system over the five states, with the observation event as the unit of change:

- T1 Fresh -> Aging: age exceeds the young bar (900 s default for tool results, `freshness_check.py:85`), or a drift signal is named while inside the stale bar (the patrol's "growth noted" arm, lines 280-287).
- T2 Aging -> Stale: age beyond the stale bar AND a provenance- and direction-typed motion witness (line 265; line 292). Strict inequality: the self-test pins "age exactly at bar passes with growth".
- T3 any -> Dead(corrupt): witness future-dated beyond tolerance, unparseable, or missing its hash (lines 174-176, 179-180; patrol 305-312).
- T4 any -> Dead(absent): artifact missing at a position that requires it (289-290).
- T5 verdict -> UNVERIFIABLE: the meter itself failed (git exit 2, collection failure, timeout, `census_drift_patrol.py:344-352`). State unknown; consumption blocked anyway, but the operator response is fix-the-meter, not fix-the-artifact.

The exit triad encodes the distinction: 0 ok, 1 verified violation, 2 cannot verify. Conflating 1 and 2 is the channel-failure mode B2-338 already caught in the opposite direction: the hook case-matched the lowercase prefix "CENSUS-PATROL: ok" because the old uppercase OK head fell into the WARN arm on every green push, "training operators to dismiss the channel" (lines 321-325). A checker's own health is part of the judgment: a verdict is well-typed only when emitted by a meter that was itself verified.

## 5. Promotion rules: re-observation only

Age is monotone; the only sanctioned state improvement is a new observation event. Time heals nothing. Both gates print the same promotion rule as their fix text: rerun the instrument, then refresh the carrier with the new counts and today's date (`freshness_check.py:299`; `census_drift_patrol.py:336-337, 368-369`). The receipt layer makes promotion sound by construction: `receipt()` mints `{observed_at, source_hash, max_age_seconds}` (lines 111-133) and the bar rides inside the receipt so a JSON round trip cannot launder it (self-test: "json round trip preserves hash and verdict"). The retired hand-copied headline was an unsound promotion: a claim re-typed Fresh by fiat twelve days after its last observation, with no mint event.

Promotion has a cost type. The default patrol never runs pytest, "which keeps pre-push fast and dependency-free" (docstring lines 34-38); the `--collect` deep check is opt-in because it needs the venv and a full collection pass (lines 53-61). So instruments split into cheap mints (re-hash a file, glob candidates, scan git log; safe to run at every consumption) and expensive mints (full collection; gated behind an explicit act or a scheduled task, per the MagCensusPatrolDaily registration in AGENTS.md). This is RFC 5861's stale-while-revalidate split, stated as economics: cheap revalidation may happen automatically on a stale read; expensive revalidation is a decision. A concrete follow-up would be an `--autorefresh` flag that executes only the cheap mint set on read and prints the expensive one.

## 6. The consumption-time checker

The embryonic form already exists: `ClaimVerdict` with `__bool__` so a consumption site writes `if stale_claim(rec): block` (`freshness_check.py:89-94`), and `stale_claim` re-derives everything at the moment of consumption, including re-hashing the source to catch the world moving after observation (lines 185-191; self-test: "drifted source fails gate"). The docstring's law generalizes: "a timed-out tool call mints no receipt at all, and stale_claim(None) is stale for exactly that reason" (lines 18-23). Absence of witness is death, not innocence: fail-closed by construction.

The design generalizes this into a position table. A `Position` declares: requirement, accepted states, clock, bar, motion-scope, and the instrument that may mint promotions. A single `judge(position, path, now)` re-derives the state at every consumption and returns `{state, reason, exit}` with blame strings in the `ClaimVerdict` style:

| position | requirement | accepted | clock | motion witness |
|---|---|---|---|---|
| BOOT_DOC (state/CURRENT.md, state/START_BRIEF.md) | LIVE_TRUTH | Fresh, Aging | commit; mtime fallback (282-287) | repo heartbeat |
| CENSUS_CLAIM (the AGENTS.md **Tests:** bullet) | STATISTIC | Fresh, Aging (delta within 20 at deep check) | self-declared + future guard | tests/ committed adds; disk shrink |
| TOOL_RESULT (receipt layer) | REVALIDATED | Fresh only, 900 s default | mint | source re-hash |
| LINEAGE (FROZEN_OK entries) | LINEAGE_OK | Fossil | registration date | none, exempt |
| REGRESSION_VECTOR (B2-274 fixtures) | WITNESS | Fossil only; Fresh here is the violation | pinned day | must not track |

Two rows are the punchline of the partial order: in LINEAGE position only a Fossil is acceptable, and in WITNESS position freshness is the defect. The checker maps verdicts to the exit triad of section 4, and an unknown position fails closed as UNVERIFIABLE (exit 2), never as ANY.

Mechanically: one new module (say `tools/temporal_types.py`) owning `State`, `Witness(direction, provenance, scope)`, `Position`, and `judge()`; the two existing gates become thin adapters that keep their own constants (`STALE_DAYS`, `HEARTBEAT_DAYS`, `CENSUS_STALE_DAYS`, `COLLECT_DRIFT_TOLERANCE`) as position parameters, so no behavior changes on landing; a registry maps paths to positions and fails closed when missing. The 30 patrol self-test vectors port directly as typing judgments of `judge`, which matters because the ratchet and scenario-suite gates (`githooks/pre-push`, per AGENTS.md) already require gate changes to carry re-provable cards.

## 7. Literature anchors

The design is an application of named prior art, with the estate's twist marked: region-based memory management and its lifetime types (Tofte and Talpin 1997; Rust's borrow checker): a receipt is a region token and consuming a stale claim is the temporal analogue of use-after-free, defined as unsound rather than merely crash-prone. Higher-order contracts (Findler and Felleisen 2002): `ClaimVerdict.reason` is blame assignment, and the gate-friendly `__bool__` puts the contract check at the boundary. Gradual typing (Siek and Taha 2006): AGENTS.md prose is the untyped substrate and the carrier regex is the typed boundary where blame lands (B2-249 is the boundary law). Liquid types (Rondon, Kawaguchi, Jhala 2008): the refinements are exactly `{r: Receipt | age(r) <= bar(r)}` with the bar carried in the value. Pluggable type systems (Bracha 2004): the checker is optional over prose and adds authority only where the position demands it. Bitemporal databases (Snodgrass; SQL:2011): mint time is transaction time, the census date is valid time, and the 12-day fossil is a valid-time-frozen claim. HTTP caching (RFC 7234; RFC 5861): freshness evaluated at request time, heuristic freshness, stale-while-revalidate as the promotion-on-read pattern. The estate's twist on all of these is the motion conjunction of section 1: none of the cited systems demote on relative motion, and the B2-216 census denominator law in AGENTS.md ("name instrument, moment, and delta before comparing counts; never difference two counts taken at different moments") is the matching typing rule for numbers themselves: a count without an instrument annotation is ill-typed for cross-moment comparison.

## 8. Limits and what was not done

The `--collect` deep check was not run this session (needs a full pytest collection; reported as not run). `mag/boot_check.py`, `tools/fossil_check.py`, `tools/thought_quantizer.py`, and `mag/catalog_tags.py` are cited by the sibling artifact and were NOT independently re-read here; anything taken from them is marked as sibling-cited, not re-verified, and the live fossil_check output quoted in that sibling is its receipt, not mine. No code was changed; this item is analysis and design only. The judge design is unimplemented; its test vectors are identified (the 30 patrol checks plus the 18 receipt checks) but not yet ported.
