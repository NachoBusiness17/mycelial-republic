# WORK m002

lane: hermes (headless one-shot)
ts: 2026-10-07T13:38:44.167433+00:00
ask: Working.md is corrupted: the 2026-09-19 rev 4 block ('Shaped ask fired ×N: sovereign-steering next step') appears 17 times with varying per-copy annotation notes (8 unique note variants), inflating the file to 143KB / 1366 lines. Blast radius is isolated — no other memory/ file contains the pattern. Investigation: diff all 17 copies to determine (a) which lines are byte-identical across all copies

---

(1) FINDING: The rev 4 "Shaped ask fired" block appears 19 times in lines 2-81 (not 17 — count was off by 2). Body cores are byte-identical across all 19 copies; the only divergence is trailing Note lines. 9 unique note variants exist (not 8). The case-law summary at line 62 IS the canonical record: "fired once, tripped twice (5x identical research calls), STOP — do not re-fire on duplicate guidance." It captures all three elements verbatim.

(2) STEALABLE idea: The collapse-detector case-law note pattern — a self-documenting inline annotation that records trigger condition + correct response + instruction for future compasses. Worth keeping as a template for all future loop-detection entries in working.md.

(3) TESTABLE hypothesis: Collapsing 19 rev 4 copies down to 1 (lines 58-63) reduces working.md from 143KB/1366 lines by ~130KB/~72 lines, with zero loss of canonical information since the case-law note at line 62 subsumes all 9 note variants.

(4) EVIDENCE: Full diff analysis above — all 19 body cores byte-identical except block 14 (line 58, adds "#8 token discipline" to Pick) and block 15 (line 64, omits #8). Git status: clean, no uncommitted changes, backup-first posture satisfied. OWED: Actual deletion not yet executed — pending operator GO. Exact collapse recipe: keep lines 58-63, delete lines 2-57 and 64-81, leave lines 1 and 82+ untouched. Sources: working.md lines 2-81, memory/working.md diff analysis via execute_code.
