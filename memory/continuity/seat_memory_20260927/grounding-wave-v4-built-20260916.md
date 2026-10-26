---
name: grounding-wave-v4-built-20260916
description: V4 admission boundary BUILT — write-time gates make row-122 bypass
  physically impossible; void/contest/witness/view verbs live; staged VOID
  awaits operator signature and second seat
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

grounding_wave.py v3 → v4 BUILT per A2 epistemology engine design (Codex packet's "most useful next synthesis"). Three gates run at write time inside the append lock: G1 structural (canonical hash + chain), G2 source binding (src_sha256_12 at post, re-hashed at verify → EVIDENCE-MUTATED), G3 warrant (command hashed into row, witnesses record g3_exit). Row 122's bypass path is physically impossible — a row missing hash/prev is refused at the door, not discovered later.

New verbs: `void` (reason_code enum MALFORMED|FORGED|EVIDENCE_DEAD|CONTEST_SUSTAINED, named second seat required, void-of-void reversal works), `contest`, `witness` (SELF_SIGNED refusal), `view` (effective ledger with admission ladder RECORDED → CORROBORATED → CONTESTED → VOID). No migration — v1/v2/v3 key sets hash byte-identically (test-pinned).

26 new tests in tests/test_grounding_wave_v4.py covering all five A2 scenarios including planted-failure propagation. v3's render crash on live tape (KeyError from row 122's missing keys) incidentally fixed by v4's defensive view.

Two pre-existing test failures remain: test_falsifier_ledger (row 122's missing evidence key) and test_wave_driver (banner contract) — unrelated to v4.

**Operator's remaining hand-action:** the row-122 VOID is staged as a dry-run PROPOSAL only. Operator names his second seat, executes `void --row "#122" --reason-code MALFORMED` + the matching void for row 123 (hash `d2c81c2dc98a…`, empty-prev unseeded SUPPORTED), has the second seat append witness rows — then verify returns LINKAGE-PASS with `ADMISSION: 2 voided`. The "author is inside the machine too" caveat (A2) means this decision is his, not the fleet's.

LANDED in checkpoint commit `118333dd1` (checkpoint #5 of the night; chain 5305a99b1 → 0f34a8f3e → 75c030d29 → 9546bb7f8 → 118333dd1). Two build bugs caught by v4's own tests and pinned: Windows `shlex` posix=False kept quote chars in warrants (warrants never spawned) and admission-tip collapse to GENESIS mid-tape (broke void-of-void reversal). v3's `render()` had been crashing on the live tape since row 122 landed (KeyError on missing keys) — v4's defensive view fixed that incidentally. Grounding selector run after v4: `2 failed, 65 passed` — both failures pre-existing (test_falsifier_ledger trips on live row 122's missing evidence key; test_wave_driver wants a "v0 TICK" banner the untouched driver no longer prints).
