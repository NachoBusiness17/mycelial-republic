# R11 RESTORE DRILL - C2 continuity, LOCAL half - 2026-09-30

**Verdict: RESTORE-VERIFIED** (run 3, 20:03-20:31 EDT, log tail reproduced in section 4;
independently re-proven green by run 4 at the fixed script's commit, section 4a).
The mechanism is proven on one machine: restic snapshot of the four backup sets -> restore
into a TEMP twin tree -> `_verify_chain_consistent` PASS on the RESTORED copy (restored
module + restored data) -> pytest smoke (parity + water families) outcome IDENTICAL to the
baseline twin -> `RESTORE-VERIFIED`. The full C2 drill (offsite medium + second machine) is
the **M4 OPERATOR GATE** (section 5). Script: `scripts/restore_drill.ps1 -Local`.

## 1. Inputs read before building

- `watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md` - the four-set table (biography / seals /
  state / .env, ~679 MB), the restic choice, the `-Verify` restore-test law, the passphrase
  law, the never-inside-the-git-tree repo boundary. The drill's script reuses the same set
  table as `scripts/backup_offsite.ps1`.
- **V2ASK2's verdict on the runbook: IT NEVER LANDED.** The volley-2 fire
  (`watch/inbox/frontier_asks/volley2/results/V2ASK2_raw.json`) finished with
  `finish_reason=content_filter` at **2,053 content chars of a 64,000 max** (3,403
  completion tokens, $0.0705, 46.2 s) - the answer dies mid-Q07 ("Spec W1"), before Q08.
  The only Q08 text that exists is the ASK itself (`volley2/V2ASK2.md`): the drill must
  carry restic restore commands, the verify call, the pytest gate, expected timing on a
  679 MB set, and the second machine's prerequisites. This receipt supplies all five from
  byte-backed local execution instead; nothing below is attributed to V2ASK2.

## 2. What the drill does (scripts/restore_drill.ps1 -Local)

Twin-tree design (the two honest failures that forced it are in section 6):

- **Baseline twin**: `git archive HEAD` code layer (smoke scope ~430 MB: mag tools tests
  configs config.py server scripts githooks watch/cage_bin conftest.py pytest.ini) +
  **plain file copy** of the four live sets.
- **Restored twin**: the IDENTICAL `git archive HEAD` layer + the four sets arriving via
  **restic snapshot -> restore** (temp repo under `%TEMP%`, throwaway per-run passphrase,
  never inside the estate git tree).
- Equal pytest outcomes on identical code isolate EXACTLY the restic roundtrip; the dirty
  live working tree cannot leak flakiness in. No live-vs-restored sha256 diff: the chain
  grew 8691 -> 8693 leaves across the drill window (concurrent seats), and mid-drill
  appends would fake a mismatch that is not a restore defect. The restored-copy gate
  self-verifies internal consistency instead.

## 3. The live run (run 3 facts, bytes from the drill output)

Environment: restic 0.19.1 windows/amd64 (binary fetched from the official GitHub release,
zip sha256 `da948ad707ed690426473aaba2046cd61f8f90f6f0e7dab6be0d5796531de67d` verified
against the release `SHA256SUMS`; winget install not required for the drill), git HEAD
`0b846c01fc0c45e87a62595bd19bae8fe55fb8bc`, Python 3.11.15, PS 5.1. Machine was under the
full-burn wave (30+ concurrent python processes): timings below are a CEILING, not a floor.

Snapshots (tag -> id): biography `05866c74`, seals `8f15992f`, state `198d9e74`, env `7dc0e427`.

Sizes (live bytes in; matches plan section 3 within drift):

| Set | Files | Bytes |
|---|---|---|
| biography | 47,452 | 363,701,574 |
| seals | 403 | 216,654,445 |
| state | 4,230 | 98,539,515 |
| env | 1 | 5,868 |
| total | 52,086 | 678,901,402 |

Drill restic repo on disk after zstd+dedup: **169,739,278 B** (679 MB -> 170 MB). Restored
twin on disk (git layer + 4 sets): 1,108,030,951 B / 54,485 files.

Timing (phase / seconds): restic-init 2.2; backup biography 112.2, seals 4.1, state 11.9,
env 1.2 (sum 129.4); restic check 5.3 (PASS); restore biography 183.4, seals 14.5, state
25.1, env 0.7 (sum 223.7); chain gate 0.8; baseline-twin pytest 21.2; restored-twin pytest
16.0; code-layer archive into both twins 1,262.2 (Expand-Archive PS slowness under load,
the drill's known fat; the RESTORE path itself is ~4 minutes). Sum 1,660.8 s.

## 4. The verification result (the proof lines)

Phase E (the audit fix #4 law, run against the RESTORED copy, on the restored tree's own
module):

```
[phase E] [chain-gate module] ...\mag-restore-drill-20260930-200334\tree\mag\verkle_knot.py | [chain-gate PASS] chain consistent (8693 leaves)
```

Phase B/F (smoke families: test_hunger_ledger_parity, test_parity_gate_hook_pin,
test_rule_parity, test_k8s_water, test_water_computer, test_water_graph,
test_water_graph_campaign, test_water_graph_starvation, test_water_swarm):

```
baseline twin  : 18 failed, 63 passed in 17.31s
restored twin  : 18 failed, 63 passed in 11.53s  (identical outcome = smoke PARITY)
```

The comparison law requires the SAME failed ids and the SAME pass count; the script
enforces set equality and names any divergent id. The 18 failures are HEAD-code failures
present IDENTICALLY in both twins (the live working tree carries uncommitted water-module
edits the twins deliberately do not have; `test_k8s_water.py::test_ledger_workload_feeds_simulator`
also fails on the live tree itself). They are properties of commit `0b846c01`, not of the
restore; the drill verifies the roundtrip, not HEAD's greenness.

Final line: `RESTORE-VERIFIED`, exit 0, workspace then cleaned.

### 4a. Run 4 — independent refire at the FIXED script's commit (this seat)

Run 3's script fix was committed (`785b1b13934b499c74f394578fc5a6c39e8d0181`); a second
live run against that HEAD (workspace `mag-restore-drill-20260930-203841`, 20:38-20:49
EDT, lighter machine load) went green again — the mechanism is REPRODUCIBLE, not a
one-off. Bytes from its output (`%TEMP%\r11_drill_run4.log`, workspace cleaned):

- Snapshots: biography `c4e06ff2`, seals `859fefdc`, state `dfb42c77`, env `0396ae3c`;
  `restic check` PASS; sets in 678,920,928 B / 52,086 files (biography 363,701,547).
- `[chain-gate PASS] chain consistent (8693 leaves)` — restored module, restored data.
- `baseline twin : 18 failed, 63 passed in 10.49s` / `restored twin : 18 failed, 63
  passed in 13.50s (identical outcome = smoke PARITY)` — same 18 HEAD-code failure ids
  in both twins as run 3.
- Drill repo on disk 167,176,259 B; restored twin 1,106,653,148 B / 54,487 files.
- Phase seconds: code-layer 220.1; init 2.3; backup bio 149.4 / seals 4.0 / state 7.8 /
  env 3.2; check 3.6; restore bio 196.2 / seals 21.3 / state 21.5 / env 0.9; chain gate
  0.6; baseline pytest 13.9; restored pytest 17.2. **Sum 662.0 s** (~11 min end-to-end;
  restic backup+check+restore alone ~4.4 min). Two greens, two HEADs, 45 min apart:
  expected timing band for a 679 MB set on this box = **~11-28 min wall clock**,
  restic-path ~4-6 min regardless of load.


## 5. M4 OPERATOR GATE - the second-machine half (not automatable from this seat)

`scripts/restore_drill.ps1` without `-Local` prints this gate card and exits 3:

1. Pick + live a real offsite medium (plan section 4: USB SSD / laptop-over-Tailscale-sftp /
   B2). Not scheduled, not chosen - operator's door.
2. Second machine (the disk-loss survivor) needs: python 3.11+, the repo venv deps
   (`scripts/ensure_venv.ps1`), restic (`winget install --id restic.restic`), git.
3. The offsite passphrase stored off-machine BEFORE trusting a green run (passphrase law).
4. On the second machine: `scripts\backup_offsite.ps1 -Repository <offsite-url> -Verify`
   (restore + sha256 diff + chain gate), then this drill's phases against that restore,
   and verify the tip against the PUBLISHED witness tip once Q07's witness fires.
Expected second-machine cost from section 3: <6 min of restic work for the 679 MB set on
uncontended hardware (backup ~2 min + restore ~4 min here UNDER full-burn load).

## 6. The two honest failures before the green (lessons now baked into the script)

- **Run 1 (19:13, FAIL)**: the frozen smoke family included
  `tests/test_parity_gate_hook_pin.py`, which was **staged but not committed** at drill
  time (`git ls-files` reads the index; `git archive HEAD` reads the commit). A restore
  can only return committed code - the drill caught the estate's dirty-tree exposure
  mid-flight (the file landed in commit `0b846c01` while the drill ran). Fix: the family
  list is intersected with HEAD via `git cat-file -e` and every exclusion prints loudly.
- **Run 2 (19:35, FAIL)**: twin collection errored - `tools/__init__.py` imports root
  `config` and `test_rule_parity.py` imports `server.world`; both tracked, both outside
  the original grep-derived scope. Fix: `config.py` + `server` added to the scope list.

## 7. Boundaries honored

- Live tree never touched by restore (both twins under `%TEMP%`), drill repo outside the
  git tree, throwaway per-run drill passphrase (never the offsite passphrase; scrubbed in
  `finally`), workspaces deleted on success / kept on failure, no scheduling, no effects
  beyond `%TEMP%`. The failed run-1 and run-2 workspaces were inspected for diagnosis and
  removed after the lessons were captured.
