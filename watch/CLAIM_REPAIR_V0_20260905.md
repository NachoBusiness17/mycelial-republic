# CLAIM_REPAIR_V0 — FINDING 2 closed: corrupt claims are sweepable (2026-09-05)

**Build seat:** zcode weekend pool, A3 (RAMP 2, per CONVO 09-05 ~04:2xZ).
**Closes:** FINDING 2 in `watch/CLAIM_ORGAN_RACE_TEST_20260904.md` — "corrupt
claim files are unsweepable permanent locks"; left OPEN by
`watch/CAS_FIX_RECEIPT_20260904.md` (that surgery was scoped to FINDING 1).
**Verdict: SHIPPED — 46/46 harness checks PASS, existing split-brain harness
still 4/4 (CLAIM-RACE PASS), organ file byte-untouched.**

## What was built

- `mag/claim_repair.py` — the repair organ. Reuses `mag/bay_organs.py`
  primitives (`_read_claim`, `pid_alive`, `try_claim`, `release_claim`,
  `claim_is_active`); the organ itself is UNMODIFIED (sha 7d286e3cd08bd192
  matches pre-build state; repair is additive).
- `watch/test_claim_repair_20260905.py` — corruption harness mirroring the
  4/4 split-brain harness (temp dirs only, stdlib, $0).

## Corruption classes (mission name -> implemented class)

| Mission class | Implemented as | Organ failure pre-repair (proven) |
|---|---|---|
| unparseable | `unparseable` (bad JSON **or** valid-JSON-non-object) | sweep skips it AND `try_claim` loses forever (stranded); non-object makes the sweeper/claimant CRASH (`AttributeError` on `.get`) |
| missing-token | `missing-fields` (missing any of pid/ts/token, detail lists keys) | missing ts -> `claim_is_active` False -> a LIVE holder's item gets STOLEN by a rival `try_claim` (double-execution hazard); dead-pid variants blind-deleted by sweep |
| expired-lease | `expired-lease` (pid dead, or lease past its window) | sweep blind-DELETES — evidence destroyed, no receipt, no re-issue accounting |
| tomb-mismatch | `tomb-mismatch` (aged `.expired-*` residue, corrupt or well-formed; token recorded) | sweep blind-deletes after grace; corrupt tombs leave zero evidence |

Repair behavior per class: classify -> **quarantine** (move-aside with
timestamped name under `watch/bay/repair/quarantine/`, sha256 recorded,
NEVER deleted) -> typed append-only receipt row (jsonl) -> re-issue ONLY the
tranche whose work is verifiably not done (re-issue = `try_claim` win +
immediate `release_claim` — proves the item is claimable again and leaves it
free for the fleet). Re-issue is refused when the work's own markers say
done/parked: churn state `parked` map, THIN output head, substantive output
file, or no verifiable queue row (unverifiable -> refuse, safe default).
Live holders (pid alive, lease unjudgeable) are LEFT IN PLACE, never yanked.
Fresh tombstones are never touched — the FINDING 1 CAS fix relies on them
transiently. Active claims never touched.

## Laws compliance

- **Dry-run default:** plain run reports + writes `would-*` receipt rows,
  moves nothing. `--apply` mutates.
- **Backup-first:** on `--apply`, before any move, the whole claims store is
  copied to `watch/bay/repair/backup-<UTCts>/claims/` (sha-verified in harness).
- **Quarantine-don't-delete:** every repairable file is moved aside with
  evidence preserved; nothing is ever removed by this tool.
- **Idempotent:** quarantine moves the file out of scan scope; second apply
  run = 0 repairs, store byte-identical (proven).
- **No organ surgery:** `mag/bay_organs.py` and
  `watch/test_claim_race_20260904.py` untouched (hashes above vs pre-build).
- **No new daemons/scheduled tasks** — CLI + importable module only.
- Live bay touched only by a dry-run scan (march228: scanned=0, to_repair=0).

## Harness results (watch/test_claim_repair_20260905.py — 46/46 PASS)

- **BEFORE repair (TEST P, against the unmodified organ):** P1 unparseable
  claim — sweep removes 0, two independent claimants both strand (lose
  forever). P2 valid-JSON-non-object — `sweep_expired` raises AttributeError
  (sweeper chokes) and a claimant crashes. P3 claim missing ts with a LIVE
  holder — rival `try_claim` STEALS the live worker's item. P4 stale
  parseable claim — sweep blind-deletes, evidence unrecoverable.
- **AFTER repair (TEST D/A/I):** dry-run classifies 6 fixtures (unparseable 2,
  missing-fields 1, expired-lease 1, tomb-mismatch 2), moves nothing, store
  byte-identical. Apply: backup taken first (sha matches), all 6 quarantined
  exactly once with sha-preserved evidence, exactly ONE re-issue (the
  verifiably-not-done tranche, via try_claim win + release proof); done /
  parked-thin / unverifiable refused; fresh tombstone KEPT; live claim
  untouched, token unchanged; second apply run = 0 repairs, store
  byte-identical, no second backup.
- **REGRESSION (TEST R):** existing `test_claim_race_20260904.py` run
  unmodified as subprocess — exit 0, "CLAIM-RACE PASS (tests A=ok B=ok C=ok
  D=ok E=ok, 14 race rounds x 6 racers)". 4/4 split-brain verification holds.

## Exact re-run commands

```
# SUPERSEDED (FW-11 2026-09-28): v0 proof commands, executed 2026-09-05 (FINDING 2 closed at v0). Do not re-run from prose. Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
# the proof (exit 0 = FINDING 2 closed at v0):
python watch/test_claim_repair_20260905.py

# no-regression proof:
python watch/test_claim_race_20260904.py

# operate on the live bay (dry-run first, ALWAYS):
python -m mag.claim_repair                    # report only
python -m mag.claim_repair --apply            # quarantine + re-issue (backs up first)
python -m mag.claim_repair --queue march228 --apply   # one queue only
```

## TRI-STATE

| Claim | State | Evidence |
|---|---|---|
| "Corrupt claim files strand/choke/steal the organ pre-repair" | **Supported** | TEST P 6/6: strand x2, sweep AttributeError + claimant crash, live-holder steal, blind-delete |
| "Repair quarantines every corrupt claim exactly once, preserving evidence" | **Supported** | 6/6 quarantined, sha-preserved, backup-first verified, idempotency: second run 0 repairs + byte-identical store |
| "Repair re-issues ONLY verifiably-not-done tranches (never double-executes)" | **Supported** | exactly 1 re-issue (not-done), refused for done / parked-thin / unverifiable; re-issue = claim+release proof, item left free; no work executor invoked |
| "Repair never disturbs healthy organ state" | **Supported** | fresh tombstone kept, live claim token unchanged, active-claim skip path, 4/4 race harness regression PASS |
| "The live bay currently contains zero corrupt claims" | **Unproven** (point-in-time) | live dry-run 09-05: march228 scanned=0 to_repair=0 — empty store proves nothing about future corruption; schedule re-scans |
| "Repair covers every corruption shape that can occur" | **Unproven** | classes derived from the organ's read paths (`_read_claim`, `claim_is_active`, sweep); exotic shapes (binary garbage, oversized files, permission-locked files) untested at v0 |

## Falsifier (how someone proves this repair WRONG)

1. **Double-execution:** produce a store where a task's work markers say
   not-done, run `--apply` twice, and show the tranche's work executed twice
   — or simpler: show `watch/bay/repair/claim_repair_receipts.jsonl` holding
   TWO `reissued: true` rows for the same `task` across runs (the harness's
   TEST I asserts exactly-once; a counterexample store breaks it).
2. **Eats a live claim:** hold a fresh claim from any live process, run
   `--apply`, and show the claim file gone/quarantined or its token changed
   (harness TEST A `live-claim-untouched` asserts the opposite; a stolen
   live claim falsifies the live-holder guard — the missing-ts case is the
   sharpest attack: half-write a claim with a live pid and no ts).
3. **Stranding survives:** craft any corrupt file the sweeper still skips
   after `--apply` (e.g. a file `classify_file` mislabels `skip-foreign`) and
   show `try_claim` still loses forever.
4. **Regression:** run `test_claim_race_20260904.py` after any future organ
   change and catch a non-4/4 result that the repair tool masked.

## Open for v1

- Auto-scan hook: an organ-side call site (churn pick loop) invoking
  `claim_repair.repair(apply=True)` on a cadence is NOT wired (deliberately —
  no new daemons law; needs the operator's word on where it lives).
- `work_state` knows the churn queue manifest shape (`<queue>.jsonl` with
  `id`/`output`) — other queue formats need adapters.
- Exotic corruption shapes (binary garbage, permission-locked) untested.
- Chain knot for this receipt not minted (v1, same as arena-bench).
