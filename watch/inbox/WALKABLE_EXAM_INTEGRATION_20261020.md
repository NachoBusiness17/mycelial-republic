# WALKABLE EXAM INTEGRATION: FABLE ROOM & SAME BOOK (2026-10-20)

**Operator directive:** "all three in order: 1. Recur Compile, 2. Grade Round 2 Matrix, 3. The Walkable Exam"  
**Classification:** PEDAGOGY & GWAP EVALUATION PIPELINE  
**House Law Compliance:** Strictly zero unicode em-dashes (-- and - only); strictly zero git commits.

---

## 1. Executive Summary

Direction 5 from `OUROBOROS_SYNTHESIS_20261020.md` is now built, integrated, and verified:
- **Core Module:** `tools/walkable_exam.py` wraps `mag/fable_room.py` (LAW-061 engine) into an interactive socratic exam puzzle.
- **The Mechanic:** The agent is placed at entrance chamber (0,0) facing a choice:
    - *Option A (The Map Shortcut):* Blindly trusts the linen map promising an unverified opening -> Trapped by solid stone (`MAP_LIE` at `chamber_2_2`, score 0).
    - *Option B (Floor Hash Verification):* Puts the map in its pocket, checks floor hashes, follows hollow boards -> Resolves the map lie via `fix_map_from_floor`, unlocking the verified 5-chamber exit path (score 100).
- **Automated Verification:** 4/4 unit tests passing in `tests/test_walkable_exam.py`.

---

## 2. Fleet Evaluation Results

Fleet decisions recorded in `canon/same_book/walkable_exam_results.json`:

| Model / Policy | Decision | Verdict | Score | Path Generated |
|---|---|---|---|---|
| **Nous Beam 501B** | Option B (Floor trust) | PASS_FLOOR_VERIFIED | 100/100 | `[0,0 -> 1,0 -> 2,0 -> 2,1 -> 2,2]` |
| **Laguna-S 2.1** | Option B (Floor trust) | PASS_FLOOR_VERIFIED | 100/100 | `[0,0 -> 1,0 -> 2,0 -> 2,1 -> 2,2]` |
| **Naive Agent Control** | Option A (Map shortcut) | FAIL_MAP_TRAP | 0/100 | Trapped at `chamber_2_2` (`MAP_LIE`) |

---

## 3. Architectural Significance

1. **GWAP Exact:** The exam is no longer a passive multiple-choice questionnaire; it is a walkable grid game. Playing is testing.
2. **Floor Hash as Ground:** Directly dogfoods LAW-061: the map can lie, the floor cannot. An agent only passes if it actively verifies reality over representation.
3. **Zero Commit Overhead:** All tools, tests, and json evaluation outputs land on disk cleanly, ready for the background sweeper.
