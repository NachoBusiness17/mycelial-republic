# sess-05: the driving-ladder corrections mined from the record

**Item:** sess-05, source `memory/rib/RIB_DRIVING_LADDER_20260928.md`. Ask: read the rib, find
every correction in the record (grep 'stop running', 'remember', 'only hermes', 'you keep');
for each: what was the correction, what law would have prevented it, is that law now in code.
**Session:** mirror gopher, 2026-09-28. All commands in this receipt were run this session
with `.venv/Scripts/python.exe`, `git`, `grep`, `ls` (exact commands in the Method section).

## Source rib (read in full)

`memory/rib/RIB_DRIVING_LADDER_20260928.md` (37 lines): :3-5 quotes the three corrections
verbatim ("those aren't funded only hermes" / "stop running shit and start remembering" /
"what are warmed ribs for if you won't use them"); invariant 1 ONLY HERMES IS FUNDED :7-13;
invariant 2 the ladder climbs (sensing never substitutes judgment) :15-23; invariant 3
REMEMBER BEFORE RUNNING :25-31; lineage RIB_FREE_USAGE_POLICY_20260823 :33-37.

## The three named corrections

### 1. "those aren't funded only hermes" (09-27/28 night, rib :3-4)

- **What was the correction:** the seat ran workhorse/judgment work on unfunded tiers
  (Anthropic keys in .env treated as a rung, DeepSeek-era assumptions, free lanes as work).
- **Law that would have prevented it:** invariant 1 (rib :7-13) and the FUNDING-STATEMENT
  card (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:50-55`: "update the tier ladder in
  AGENTS.md + ribs the same hour; the ladder drives all dispatch. (Current: ONLY
  Hermes/Nous $180 funded.)").
- **Attested root cause still live in the record:** the predecessor rib
  `memory/rib/RIB_FREE_USAGE_POLICY_20260823.md:25` still teaches "DeepSeek (funded) - the
  reliable workhorse" (:24-28 the old routing ladder). Full 46-line read this session: the
  file has NO superseded banner and no pointer to the driving ladder rib, while
  `mag/context_pack.py:312-315` loads ALL of `memory/rib/*.md` (sorted glob) into agent
  context. A fresh seat can still read the stale funded rung today.
- **Is that law now in code: YES, partially.** Commit `709e2928a` (verified via
  `git show --stat`: 2026-09-27 21:09:08 -0400, AGENTS.md +1, tools/stealth_driver.py +11
  -3) landed: AGENTS.md:32 carries the driving ladder as standing law, and
  `tools/stealth_driver.py:483-492` marks every free-lane dispatch row `status: "sensed"`
  with the CODE-AS-LAW comment citing the rib (:486-489: "a free-lane dispatch is SENSED,
  never DONE"); `tools/stealth_driver.py:495-503` `_llama_guard` POST-allowlists only
  openrouter / nous-inference / llm7.
- **Gaps found this session:** (a) no "done" status exists anywhere in stealth_driver.py
  (`grep -n '"done"' tools/stealth_driver.py` -> zero hits); both dispatch paths mark
  sensed, including the hermes lane (:386-388), so the promised funded-tier verify flip to
  done is not implemented - enforcement is one-sided (free lanes structurally cannot
  produce done rows). (b) `grep -rln stealth_work_state mag tools scripts` -> only
  `tools/stealth_driver.py` (plus pycache): no other module reads
  `state/fuel/stealth_work_state.json`, so nothing downstream consumes the sensed gate
  yet. (c) the stale DeepSeek rung (RIB_FREE_USAGE_POLICY:25) is uncorrected in the rib
  library the context pack loads.

### 2. "stop running shit and start remembering" (09-27/28 night, rib :4-5)

- **What was the correction:** the seat kept re-running and re-deriving instead of
  consuming compiled memory; the rib says it outright (:27-28 "A fresh seat re-derived
  what this rib held, and had to be corrected three times").
- **Law that would have prevented it:** invariant 3 REMEMBER BEFORE RUNNING (rib :25-31)
  plus the CORRECTION card protocol (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:27-31`:
  operator correction -> STOP running -> root-cause -> mint LAW (rib + AGENTS.md if
  load-bearing + enforcement in code) -> commit; the card names the driving ladder as one
  of its three evidences).
- **Is that law now in code: NO gate; read-path only.** Infrastructure exists:
  `mag/context_pack.py:305-315` `_rib_doctrine()` reads `memory/rib/*.md` into stateless
  agent context; `mag/rib_bus.py` is the rib distribution surface. But nothing forces the
  consumption: `grep -in "rib|warm" githooks/pre-push` -> zero hits (the hook runs
  violation_ratchet, config_seal, description_pin, freshness; head of file read this
  session); `grep -n warm tools/workflow_gate.py` -> zero hits; and the session-start warm
  path `mag/hermes_warm_boot.py:84-93` builds a payload of schema/generated/chain/
  deployments/session_brief/verify only - it loads chain state but NOT ribs.

### 3. "what are warmed ribs for if you won't use them" (09-27/28 night, rib :5)

- **What was the correction:** same class as 2 - ribs existed and were warmed, the seat
  did not use them. The invariant was named verbatim from his words
  (`watch/inbox/burn_reset_20260927/flash50/mirror-decision-tree.md:309`).
- **Law that would have prevented it:** same invariant 3; the rib itself (:31) says "Warm
  them, then act."
- **Is that law now in code: NO** (same status as 2). An independent sibling audit agrees:
  `watch/inbox/burn_reset_20260927/flash50/deep-linguistic-dna.md:95` classes "warm the
  ribs / warmed ribs" as "boot-order prose only ... YOUNG: load-bearing intent, decorative
  instrumentation so far" - my greps (no gate in pre-push, no ribs in warm_boot payload)
  independently confirm that verdict.

## Lineage corrections on the same topic (earlier instances the greps surfaced)

The operator has corrected on the warmed-ribs topic at least 6 times from 09-19 to 09-28;
the rib's "three in a row" is the 09-27/28 night batch alone.

4. 09-19 "warmed RIBs should negate all this extra shit" and 5. "you have no idea how to
   access them" - `memory/continuity/seat_memory_20260927/two-machine-drive-bridge-20260919.md:15`
   ("pushed back twice ... He was right on both counts"). Response: the travel-kit carve
   (same file :19, `scripts/build_travel_kit.py`). Law lineage: ribs are the portable unit.
6. 09-20 "you're being obtuse load your pre warmed knowledge" -
   `watch/inbox/burn_wave_20260926/B2_130_session_inputs_raw.txt:343` (primary raw operator
   turn, session sess_dd9ad303).
7. 09-22 "load the prewarmed ribs and summon the elder" -
   `watch/inbox/burn_wave_20260926/B2_130_session_inputs_raw.txt:708`;
   `memory/runs/elder_asks/ASK_FLEET_BROKEN_AUDIT_20260922.md:3`; executed as event
   `watch/inbox/index_events.jsonl:1431` (RIB library loaded, 43 doctrine files).

## Fourth grep pattern, different topic ('you keep')

8. "you keep forgetting what tools you have for console display. fix it please all of it"
   - primary `memory/living_map.json:19051`; receipt
   `watch/inbox/FLEET_IMPRINT_20260917.md:167`. Landed in code as the consolidated organ
   `mag/console_render.py` ("the ONE console-display surface"). Same correction grammar as
   the CORRECTION card shape ("you keep X-ing", RIB_BEHAVIOR_CARDS_20260928.md:28-29):
   organ in code, no gate.

## Coverage statement (what the record does and does not hold)

- The 09-27/28 primary session tapes are NOT in the record: `ls
  corpus/oral_history/seat_pools/codex_sessions/2026/09/` -> 01 02 04 05 06 07 08 09 (no
  27, no 28), and the byte-level exact-phrase scan over the whole tree (all file sizes)
  found zero correction-phrase hits in any session tape or grok prompt history. The exact
  correction WORDS are attested only through the rib (:3-5), the 709e2928a commit message,
  and receipts quoting the rib (mirror-decision-tree.md:51-59 and :307-309;
  deep-operator-model.md:1-16). The 09-19/20/22 lineage corrections DO have primary text
  (B2_130 raw turns, two-machine-drive-bridge).
- Noise scale, honestly: 'stop running' 28 hits (18 are third-party corpus/mine noise);
  'you keep' 3,953 hits (dominated by canon/library prose); bare 'remember' census by root
  (files < 5MB, archive roots counted not scanned): memory 9,651, root 1,225, watch 873 -
  correction-shaped filter ('remember' + stop/you keep/load the/warm the rib/before
  running/never repeats) -> 373 hits, all accounted for by the law texts above plus this
  session's own scan scratch. No additional operator correction with 'remember' exists in
  the live tree.

## Verdict table

| Correction | Law | In code? |
|---|---|---|
| those aren't funded only hermes | ONLY HERMES IS FUNDED (rib :7-13) | YES partial: stealth_driver.py:483-503 sensed-never-done + allowlist; AGENTS.md:32. Gaps: no done-flip verifier, no downstream reader of work state, stale DeepSeek rung still live at RIB_FREE_USAGE_POLICY_20260823.md:25 |
| stop running shit and start remembering | REMEMBER BEFORE RUNNING (rib :25-31) | NO gate: read-path only (context_pack.py:305-315, rib_bus.py); pre-push hook 0 rib refs, workflow_gate 0 warm refs, warm_boot payload has no ribs |
| what are warmed ribs for if you won't use them | same invariant 3 | NO (same); sibling audit deep-linguistic-dna.md:95 independently says "boot-order prose only" |

## Method (exact commands run this session)

1. `.venv/Scripts/python.exe` os.walk scan, terms ['stop running','only hermes','you
   keep','start remembering','warmed ribs'], text files < 5MB -> 28 / 18 / 3,953 / 6 / 10
   hits, listed per file:line.
2. `.venv/Scripts/python.exe` byte-level scan, ALL file sizes, terms ["aren't funded",
   'not funded only', 'stop running shit', 'what are warmed ribs', "won't use them",
   'only hermes'] -> 44 hits (raw output banked as `_sess05_scan2.txt` alongside this
   receipt).
3. `.venv/Scripts/python.exe` bare-'remember' census by root + correction-shaped filter ->
   counts above, 373 shaped hits reviewed.
4. `.venv/Scripts/python.exe` greps of B2_130_session_inputs_raw.txt and
   _oral01_raw_user_turns.txt for funded/remembering/warmed/pre warmed/only hermes/you
   keep -> lineage turns at B2_130 lines 124, 343, 443, 708.
5. `git show --stat --date=iso 709e2928a` + `git log --oneline --all --grep="driving
   ladder" -i`.
6. Reads: rib + lineage ribs in full; tools/stealth_driver.py:455-530 + targeted greps;
   mag/context_pack.py rib greps; mag/hermes_warm_boot.py:84-98; githooks/pre-push head;
   RIB_BEHAVIOR_CARDS_20260928.md card sections; two-machine-drive-bridge-20260919.md in
   full; memory/trajectory/steps.jsonl keyword rows; ls of codex_sessions/2026/09/.

Em/en dash scan of this file: run at bank time (venv python, chr(8212)/chr(8211)), result
recorded in the commit message.
