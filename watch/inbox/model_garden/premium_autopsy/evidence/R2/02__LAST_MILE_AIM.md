# LAST_MILE_AIM - what the remaining credits are FOR (2026-10-01, operator ask)

Operator: "I think we need to understand what the last mile looks like and use the money
towards that goal using all we are DOING."

## THE RECAP (day 1 of the burn, in numbers)

Spent $31.34 of $145. What it bought:
- 9 laws + 14 tickets + 16 to-verify from 4 stranger audits (T1W1, $2.74 - best value on the board)
- 8 EASY tickets LANDED as code (verkle integrity fail-closed, atomic tip writes, chain repair,
  grounding sha256 bindings, leaf-count proof binding, warm-boot truth) + 11 new tests
- 3 carrier patches LANDED (landed-beats-force, REFUSED terminal, evidence preflight) - 21 tests
- The WAVE24 loop PROVEN end-to-end once: sherpa -> premium -> ractor -> build/verify -> send-back
- 3 ribs minted (GPU ladder, DeepSeek shoulders, + the descent protocol rib from before)
- The bleed found and gated: $18.89 (63%) of day spend was theater (A1 x45 re-burn, 82 refusal
  retries, 14 duels fired blind); all three root causes named in bytes and patched
- DG1 landed: mating->MoE naive form DEAD, but a live narrower door (see below), sherpa
  corrected (mergekit-moe exists)

## WHAT THE LAST MILE IS (plain words)

The last mile is NOT more receipts. It is the estate reaching the state where all of this
survives without us: (1) THE LOOP RUNS ALONE - asks fire themselves, tickets redeem themselves,
laws feed the next wave, and the redemption denominator (issued vs run vs dropped) is counted
and above zero; (2) THE STRANGER PASSES - a fresh seat boots on ribs + state alone and lands a
workday without re-deriving anything (the lensing verdict's stranger-first reorder; T1 is
literally the test); (3) THE CREDITS BECOME LAW - every dollar leaves a rib, a test, a skill,
or a spec that a future window consumes (the descent falsifier). When those three hold, the
estate is sovereign: cheap daily driver free, frontier bought only as propagating judgment.

The DG1 door is the last mile's build proof: if MATE_MOE_v0 feeds, the estate's original
contribution (population fusion) gains its runtime shape on hardware we own.

## THE MONEY ($113.66 remaining, aimed at the last mile)

1. FINISH T1 (stranger audits, ~$10-15): T1W2 evidence-attached refire (docker/mates/stealth)
   + T1W3 (net_client, effect broker, flock netcode). This IS last-mile test (2).
2. THE DUEL REDEMPTION (~$5): refire the 6 empty-evidence duels with rendered payloads; the
   judge pass (DeepSeek judge #2 per the shoulders rib) follows. This tests the carrier fix
   with real money - the redemption arc.
3. MATE_MOE_v0 falsifier (~$0 premium, CPU + local): the DG1 one-sitting experiment; premium
   only adjudicates the result if ambiguous (~$0.5 held).
4. T2 SPECS (~$15-20): the maps a stranger needs (top 3 from the roast), each riding the
   DeepSeek forge+adversary shoulders per the rib.
5. T3 ROASTS (~$10): including the roast of the descent protocol itself (no sacred cows).
6. T6 TRIAGE + the denominator (~$5): the ticket ledger instrument (elder-lens's question) so
   last-mile test (1) is measurable.
7. RESERVE (~$50): unallocated on purpose; the next window aims it with better information
   (DG door result, T1W2 results, judge family verdicts).

CUT ORDER if money runs tight: T5 narrative first (lowest findings-per-dollar per the
cross-ractor), then T3 second roast, then T2 third spec. Never cut: T1, the duel redemption,
the denominator.

## WHAT REMAINS BEFORE NEXT WINDOW (the honest list)

- DG1 ractor turn (the door verdict becomes law rows + the falsifier becomes a staged local run)
- T1W2 evidence attach + refire (one sitting: add evidence paths to the 3 ask.jsons)
- 6 empty-evidence duel refires with rendered payloads (one sitting)
- Coordinator commit (many untracked landings: ribs, patches, receipts, tests)
- Driver heartbeat (W2-L5) so the loop survives window close - one sitting
- One-sitting owed: bibliography row, skill ledger amendment, board runway math, denominator probe
- Standing owed: 4 v4 fixtures, memlance witness at next boot, quant tag research,
  V12 credential .bak cleanup (operator), V15 sid-binding design, Godot precompile cache (CLIMB)

## REDEMPTION-STAGING (2026-10-01 ~21:40Z, the repair lane; retires the two lines above)

T1W2 evidence attach - all 4 asks in the queue, not 3 (S5_stores had the same
disease: evidence:[] and a landed output opening with "The EVIDENCE block is empty"):

- T1W2_S5_stores -> ["server/store_io.py"]
- T1W2_S6_docker -> ["docker-compose.yml", "Dockerfile", "docker/autoclaw/docker-compose.yml"]
  (the mag service + 0.0.0.0 bind + env_file are in the root compose; the /board/inbox
  bridge is the autoclaw compose's ./board:/board mount)
- T1W2_S7_mates -> ["scripts/run_mate.ps1", "configs/mates.yaml"]
- T1W2_S8_stealth -> ["watch/inbox/STEALTH_MINED_FINDINGS.jsonl" (the findings bank,
  239748 bytes), "watch/inbox/STEALTH_TRIAGE_20260930.md" (the banked-09-30 triage
  receipt), "watch/inbox/STEALTH_SWEEP_LATEST.md"]
- Slot release: the 4 pre-patch outputs (fired evidence-less 15:17-15:18Z) were renamed
  *.md.poisoned-evidenceless (bytes preserved) because the landed-skip gate, not the
  preflight, was holding the ids; a landed poison file blocks refire even with evidence.
- First refire landed clean: T1W2_S5_stores.md at 21:28:40Z, 2997 prompt tokens
  (the code bytes rode), evidence-cited, $0.1152.

Duel refires staged: 20, not 6. The "6" counted only hermes_burn_duel1; the 14
hermes_burn_duel2 asks carry the identical poison (every landed output opens with
"the EVIDENCE block is empty" or "the material is absent"; every ask.json has
evidence:[] with the non-reveal draw-metadata JSON pasted into the contract,
root cause per DAY1_CROSS_RACTOR E3/N3 and DAY1_RIB_WARMTH X5).

- Pre-check: ask_bank verify PASS (bank v1, 6 hidden + 14 train, no material sha drift).
- Repair per ask: ask_bank draw --id <ask_id> --{hidden,train} --reveal re-rendered the
  material (new draw ids v1h-0015..v1h-0020 and v1t-0016..v1t-0029; each draws.jsonl row
  carries the note "refire-stage <old> -> <old>_r2 (C3 evidence repair)"). New dir beside
  the old one: id *_r2, contract = the reveal render's ask body + a material-binding line
  (path + sha256), evidence = [material_path] so the bytes ride via the carrier EVIDENCE
  render; model/max_tokens unchanged (claude-sonnet-5.5, 8000) for blind-judging parity.
  Old dirs, old REFUSED marker, and old outputs untouched.
- DUEL1_hidden_5 (the 46x refusal loop) restarts clean under DUEL1_hidden_5_r2: a new id
  has zero refusal-ledger rows; its exploit shape may refuse again, the carrier banks it.
- Offline preflight sweep through the carrier's own _assert_evidence_in_body:
  24/24 PASS (4 T1W2 + 20 _r2), prompt sizes 4.8k to 247.6k chars.

Blockers: none. ask_bank's reveal needs no key and no interactive step (--id + --reveal
is deterministic; the only write is the sanctioned draws.jsonl ledger row).

Remaining for other lanes: the live driver fires the _r2 asks on its 45s cycles; the
judge-family blind pass consumes the new contender outputs.
