# BREAK-LINEAGE: hostile second pass on the lineage lens (dwfrun-3b5af1ac)

fetched: 2026-10-04. Writer: break-lineage (this run's hostile pass). Every claim below was byte-checked or re-run this session; the exact command or path:line is named inline. No em-dashes. Zero fabrication: anything not re-run is marked carried.

Instruments I ran this session (not carried):
- `.venv/Scripts/python.exe mag/arena_bench.py --selftest` -> exit 0, `split_proven: true`, 2 PASS + 2 FAIL synthetic records, seal MATCH.
- `.venv/Scripts/python.exe -m pytest tests/test_night_march_cure_20261004.py -q` -> 6 passed in 1.72s.
- Night-trail audit (the falsifier the lens admitted skipping): jsonl parse of queue/lanes/night/trail.jsonl -> 57 rows (29 CYCLE, 27 CYCLE_FAIL, 1 WATCHER_CRUMB).
- Untruncated greps: `grep -rn "valid_at\|invalid_at" --include="*.py" mag/ tools/ tests/ scripts/` -> 0 matches; full-tree `supersede(` census -> defined mag/republic.py:396, called only at :644 and :687 (its own probe block); `superseded_by` -> 16 hits, all in mag/republic.py; `decay|evaporat` over mag/river.py + mag/swarm_tools.py + tools/gps_mcp/ledger.py -> 0 matches; `lattice` in tools/__init__.py and mag/mcp_server.py -> 0 matches; `g_best|p_best|ledger` in mag/flock_field.py -> 0 matches; fsrs/free-recall in live python -> 0 matches; memory/retrieval/ -> does not exist.
- ZMEM hunt (the lens's finding-1 falsifier): `grep -rn "EG-20\|pass@K"` over C:/Users/foste/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/memory/ (694 files) -> 5 hits, read in full.
- Lane substrate shape check: key census over all 12 queue/lanes/*/trail.jsonl tails and 10 runner_state.json files.
- Gwap chain recount: memory/runs/gwap/arena-capability.jsonl -> 618 rows, verdicts DISPUTE 293 / CHALLENGE 205 / VERIFIED_AGREE 120, zero BLOCKED, zero v3 engine rows.

## Verdicts

### Finding 1 (queue two-doors stale; EG-20 dropped; clippy promoted ungated): CONFIRMED, and its falsifier is now dead by the lens's own named instrument

Byte-checks, all exact:
- watch/inbox/ESTATE_GAP_DIG_20261004.md:63 = "EG-20 No coverage (pass@K) column in arena/gwap" and :79 = enhancement-table row 9, "Coverage column (pass@K, large K) beside win rate in arena/gwap | 2h | column present; predicts the mesh vs frontier routing on one batch". The 2h and the success meter are real at spec.
- watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:237 = rank 3 "EG-20 pass@K coverage column ... 2h (measured at spec)"; :241 = clippy at rank 7 with gate "same family schema". The gate note is real.
- watch/inbox/GWAP_INDEPENDENT_COP_20261004.md:82-83 names "arena-bench CI tripwire (1-2h), clippy-as-prober (2-4h), night-cycle checkpoint legs (2-4h)" as next doors, no gate on clippy. The 11-door ask inherited this line, not the ranked table.
- Door 2 landed: commit 00cb15c77 at HEAD touches tests/test_arena_bench.py (file present, 4020 bytes, mtime Oct 4 12:35). Correction to the lens: the file is now COMMITTED, not untracked, so its "if the sibling landing is reverted" reopener is weaker than stated; the tripwire receipt watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md exists and matches.
- Selftest re-run by me this session: exit 0, split proven (see instrument list). The bench is live.

Falsifier hunt result (this is the sharpening): I searched ZMEM, the exact store the lens named as the place a kill order could hide. There is no kill order; the store holds the opposite twice:
- ZMEM primer-adjacent-24wide-20261004.md:17 carries the operator build order WITH pass@K at position 3 ("independent-cop, arena-bench tripwire, pass@K, checkpoint legs, ...").
- ZMEM doors-build-ractor-then-go-20261004.md says "Bench live again; pass@K rides it", and its "doors 3+" enumeration is the literal source of the ask's 11-door list (clippy in, pass@K out).
So the drop is a transcription loss one hop after the same store banked the correct order, not a decision. The lens's move (reinsert EG-20, restore the gate note) stands, and the fix target is now precise: the doors file's "doors 3+" list is the stale artifact.

CONVERGENT: the arena-bench landing is independently carried by the ARENA_BENCH_TRIPWIRE receipt, commit 00cb15c77, and my selftest re-run.

### Finding 2 (night-cycle ~80 percent cured; 2-4h sizing dead spend): CONFIRMED, strengthened because I ran the falsifier the lens skipped

Byte-checks, all exact: mag/lane_runner.py:911-939 cycle_night (two-leg composite, monitor + march, once per night, $0); :932-938 the trail-before-persist comment naming the 5x CYCLE_FAIL 2026-10-03 re-run harm; :124 _save_state with the Errno-22 atomic-write cure; state/CURRENT.md:92-95 the "NIGHT SHIFT 10/10 LANDED ... night march honest-skip + atomic state saves" block (the lens's :94 cite lands mid-block, accurate in substance). My pytest re-run: 6 passed in 1.72s (lens read 2.08s; same denominator).

The falsifier, run by me: queue/lanes/night/trail.jsonl holds the 2026-10-03 Errno-22 storm (CYCLE_FAIL rows at 23:01:59Z, 23:04:10Z, 23:06:09Z, 23:08:04Z, cured at 23:10:55Z) and then exactly ONE post-cure CYCLE row (2026-10-04T08:50:01Z, "monitor rc=0; march rc=2 :: MARCH SKIP rc=2: no key") with zero repeats and zero post-cure CYCLE_FAIL. The re-run class is dead across the one full night observed. Honest caveat: one clean night is a small window, but the mechanism is landed, tested (6 tests), and the residual harm a per-leg flag could still cure is one redundant 300s monitor leg inside a once-per-night $0 composite. The lens's 30-minute cap is right; the receipt's 2-4h is dead spend.

### Finding 3 (decay vocabulary half-built: republic supersession + signals rails exist; mycelium unlinked): CONFIRMED at wider census scope

Byte-checks, all exact: mag/republic.py:114 verbatim ("superseded_by: int | None = None   # set once, by supersede(); never edited"), :117 append-only trail; mag/signals.py:44 wilson_lower, :82-90 recency_decay with the self-steal docstring ("Self-stolen from mycelium's `0.7^gap`"), :102-109 combine, :112-132 proven_move; mag/model_health.py:41 "from mag.signals import wilson_lower, recency_decay" (live consumption); mag/mycelium.py:188-198 contradict() counter-bump with no evidence link, :265-277 decay() boolean stamp with no successor, :183 the violated append-only comment; tools/gps_mcp/ledger.py:433 the 1/n running mean.

Quantifier-law upgrades I ran:
- valid_at/invalid_at: the lens scoped the zero to live mag/ + tools/gps_mcp python. My untruncated census over mag/ + tools/ + tests/ + scripts/ *.py: zero matches. The absence claim now holds at full live-python scope with the instrument named.
- supersede() dormancy: full-tree census. Live callers: none. The 7 live importers of republic (mag/abundance_rogue.py, game_portal.py, ghost.py, law.py, reconstruct.py, sovereign_handshake.py, vram_hologram.py) contain zero supersede( calls; republic_os.py (the main.py:4253 republic-os dispatch target, verified at main.py ~4252) contains zero supersede references; the only calls in the tree are republic.py's own probe block (:644, :687) plus archive copies under dist_audit/ and corpus/oral_history/. The organ is dormant exactly as claimed.
- The second falsifier half (shift detectors for the pheromone reset): both keys exist. tools/census_drift_patrol.py is on disk; endpoint_news resolves in mag/verb.py. The distribution-shift reset half of pheromone decay can key to an existing detector, so that half of the lens's falsifier does not fire either.

### Finding 4 (monoculture/shim substrate; text truncated in the ask): CONFIRMED as evidence, with the monoculture door's readiness weakened by a check the lens named but did not run

Byte-checks, all exact: tools/social_rsi.py:134 load_trails, :251-261 _needles/_needle_hits (citation-overlap machinery); mag/mcp_server.py:21-23 the pin gate, :341-353 pin_gate_filter (connect-time rug-pull withholding); tools/__init__.py:36-38 the corpus family; my `lattice` grep over tools/__init__.py and mag/mcp_server.py returns zero, so the no-lattice-tool claim holds; agentmemory grammar verified byte-wise at C:/Users/foste/Documents/projects/library_parked/agentmemory/src/mcp/server.ts:84-90 (format full/compact/narrative) and src/mcp/standalone.ts:18-26 (the 7-tool IMPLEMENTED_TOOLS set).

The falsifier the lens flagged as unchecked, checked by me: lane trail rows carry NO model identity. All 12 queue/lanes/*/trail.jsonl tails hold exactly {actor, artifacts, detail, event, ts}; all 10 runner_state.json files hold seat/last_* keys only. The monoculture proxy as specced (cross-lane agreement attributed to monoculture) cannot attribute anything from this substrate; it needs a model-identity column at trail-write time or a join to a store that has one. This does not refute the lens's stated evidence (every cite is byte-true); it fires against the door's "spec handed over verbatim, 2-4h" readiness. See addition 2.

## What the lens missed (additions)

1. **oracle_calibration.py is the estate's own proper-scoring instrument.** tools/oracle_calibration.py:127-176 computes ECE/MCE/Brier over binned confidences with a self-check at :376 ("brier_perfect_calibrated"). The build-once calibrator door (Gero-4B, watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:32-46) proposes downloading a no-evals-elsewhere model to do calibration work the estate already has local math for. Self-steal first: wire oracle_calibration's Brier/ECE over MoA/panel vote streams before any download; Gero-4B's download-and-eval gate should be scored AGAINST this local baseline. Falsifier: if oracle_calibration's binning path cannot consume MoA/panel confidence rows without new math, the steal is partial and the door keeps its download gate. Move: 20-minute wire check; likely re-rank the calibrator below the decay family or mark it cargo.
2. **The monoculture proxy's data prerequisite is absent from the estate (quantified).** 12 of 12 lane trails and 10 of 10 runner states carry zero model-identity fields (key census this session). The door needs either a model column minted at _trail() write time (a one-line schema addition plus a backfill decision) or a redirect to memory/workflows/REGISTRY.jsonl-class rows where dispatch shape is recorded. Without one of those, the proxy can only run as a fixed-premise instrument (this dig is monoculture by construction), which is a weaker, cheaper door than specced. Falsifier: a per-lane model ledger somewhere else in the estate (none found in queue/ or the runner substrate this session). Move: 15 minutes to add the column or rescope the door.
3. **The weld door's gate is half-open, not closed: the cop fix is landed in code but nothing v3 is banked.** My recount of memory/runs/gwap/arena-capability.jsonl: 618 rows, verdicts DISPUTE 293 / CHALLENGE 205 / VERIFIED_AGREE 120, zero BLOCKED, zero v3 engine rows. The new instrument's shape exists only in tests and the receipt's playground rerun; the historical re-grade is still an open operator decision (GWAP receipt:75-78). A weld door built now would bank v3-shaped scores into a chain whose 618-row history is old-instrument shaped, so the "banked scores mean something" gate passes only after the re-grade decision, not before. Move: put the re-grade decision (bank fresh v3 payloads under new scene ids, or formally freeze the old chain) in front of the weld door in the build order.

## The 11 doors after hostile pass (self-steal first, per door)

Landed, strike from queue: door 1 independent-cop (bb0f34586); door 2 arena-bench tripwire (00cb15c77, selftest re-run green this session).
Restore to top: EG-20 pass@K (2h measured at spec, success meter defined at ESTATE_GAP_DIG:79, bench live, operator build order rank 3 per ZMEM).
Park as cured: night-cycle checkpoint legs (falsifier run, zero post-cure repeats; 30-minute per-leg flag cap if touched at all).
Survives, resized by self-steal: pheromone metabolism (signals.recency_decay + wilson_lower exist and are already consumed at model_health.py:41; zero decay in river/swarm_tools/ledger by my grep; both shift detectors exist; this is a ledger.py wire-up, roughly 2-4h, not 4-8h of new math); mycelium-v2 (cheap after the shared schema; contradict/decay links confirmed missing); clippy-as-prober (after the family schema; memory/retrieval/ does not exist and live code holds zero FSRS references, clean small build); monoculture proxy (after addition 2's identity wire or rescoped).
Survives as designed, gated: three-signal query broker (embedding falsifier first; lattice substrate real: mag/lattice_query.py + memory/lattice/edges.jsonl on disk); MCP-lattice shim (reconciliation pass first; pin gate and 7-tool grammar verified byte-wise); weld door (behind addition 3's re-grade decision; beat_map.py on disk, 8347 bytes; the 574 damage rows are receipt-carried at PRIMER:313, not rerun by me); consume-the-ledger (flock_field holds zero g_best/p_best/ledger terms by my grep; semantics change stays gated, late).
Cargo calls: night-cycle (cured); build-once calibrator is cargo-or-late (the calibration half is covered by addition 1's local instrument, the card publishes no evals, and the model is a download dependency class).

Honest EV-per-hour order: (1) EG-20 pass@K, 2h measured; (2) decay-family shared schema, one sitting, unlocks three doors; (3) pheromone wire-up on signals.recency_decay; (4) clippy-as-prober; (5) mycelium-v2; (6) monoculture after its identity wire; then the gated tail with the calibrator demoted or dropped and the re-grade decision in front of the weld door.

## Honesty

Not re-run by me, carried from receipts: the 574-row beat_map damage substrate (PRIMER:313); the 529-payload playground rerun in the GWAP receipt; all external star counts and model cards; the other 7 lenses and 2 moonshots of this run (not read; cross-lens convergence beyond the receipts and commits I checked is not claimed). The GPS ledger sqlite row totals were still not recounted by me (the db_path is instance-configured; I did not locate the live DB file this session; the ledger.py 1/n mechanism at :433 is what the finding needed and that I verified). The night-trail clean window is one night; a longer window could still surface a different failure class.

End of pass.
