# WORK m1

lane: hermes (headless one-shot)
ts: 2026-10-07T13:02:07.053682+00:00
ask: Investigate the Belady-anomaly finding's downstream chain-integrity bug: grep mag/.mimosa/hook-state/ for session autonomous-auto-fkb-183618 and read its baseline to test the hypothesis that the Hermes autosave compactor truncates commit SHAs and stringifies tension_index when the session exceeds its scratch buffer. Then check verkle_chain.jsonl for how many of the 677 fkb: rows have non-float ten

---

---

(1) FINDING

The Belady-anomaly chain-integrity bug is confirmed, but the mechanism is not a buffer-overflow truncation — it is a systematic schema encoding that stores 8-char commit prefixes instead of full 40-char SHAs, and category strings instead of float tension indices. All 1033 `fkb:` rows in verkle_chain.jsonl carry both anomalies simultaneously.

Exact malformed values:
- dossier_commit: 8-char prefix (e.g. "t30fbf98") — 1033/1033 rows, zero 40-char full SHAs
- tension_index: string category tag (e.g. "fkb:amd_", "fkb:run_") — 1033/1033 rows, zero float values

tension_index distribution across fkb rows: fkb:run_ 400, fkb:amd_ 220, fkb:_:d2 119, fkb:sour 101, fkb:guar 87, fkb:grep 53, fkb:writ 26, fkb:read 12, fkb:sear 7, fkb:loop 7, fkb:list 1, fkb:lane 1

Session autonomous-auto-fkb-183618: exists in verkle_chain.jsonl at index 8211 (ts 2026-09-28T16:11:09Z, tension_index "fkb:amd_", dossier_commit "t30fbf98"). NOT present in hook-state/ — no baseline directory for this session ID exists there. The baseline directory that DOES exist (sess_10fe54a8... .mtcau02s-17096-542c5d8381.baseline) contains .source files named with full 40-char SHAs, confirming the short-prefix encoding happens at chain-write time, not at baseline-creation time.

(2) STEALABLE idea worth keeping

The baseline .source files use full 40-char commit SHAs as filenames — that is the correct reference format. The verkle chain should store full SHAs (or at minimum a collision-resistant prefix >= 12 chars). The 8-char prefix is a Belady-anomaly trigger: shrinking the reference width increases collision risk. The dashboard's witness_snapshot.json already expects full 40-char dossier_commit (e.g. "e700f9b85ab4dfcfa671b40aa32e87e3b001a6116a051aac1fb858e2547285") — the chain and the dashboard are speaking different SHAs.

(3) TESTABLE hypothesis

The 8-char dossier_commit prefix collisions will cause leaf-hash mismatches when the verkle chain is traversed forward from a short-prefix anchor. Test: pick any 3 fkb rows with identical 8-char dossier_commit prefix, resolve their full SHAs from the baseline .source files, and verify the leaf_hash chain reconciles. If two different full SHAs share the same 8-char prefix, the chain has an unresolvable ambiguity — that is the Belady anomaly in kernel form (smaller buffer = more collisions = more misses).

(4) EVIDENCE or OWED

EVIDENCE:
- verkle_chain.jsonl: 1033 fkb rows, all 8-char dossier_commit, all string tension_index — grep output cited above
- hook-state baseline: full 40-char SHA filenames in .source files — directory listing cited above
- verkle_audit --dry: flags only "chain rows (11618) != knot files (28957)" backfill gap — zero flags for tension_index or dossier_commit malformation
- dashboard/chain_witness.html: reads dossier_commit and tension_index from chain rows but performs no type validation — server.py passes through reg.get("tension_index") and sk.get("tension_index") unchanged
- witness_snapshot.json: stores full 40-char dossier_commit — format mismatch with chain

OWED:
- topic_evolution.json: found only in pytest tmp dirs (agents/pytest-tmp-12580/), not in production — could not verify if any production consumer exists
- Whether the dashboard has already failed or silently skipped malformed rows: no error logs found, but no validation path exists either — silent skip is the likely behavior, unproven
- The hypothesis that "Hermes autosave compactor truncates SHAs when session exceeds scratch buffer": NOT supported by evidence. The truncation is systematic (all 1033 rows, not just large sessions) and looks like a schema choice, not a buffer overflow. The 183618 session has no baseline in hook-state to compare against.

Sources: mag/.mimosa/hook-state/, memory/biography/verkle_chain.jsonl, dashboard/static/chain_witness.html, dashboard/server.py, dashboard/static/witness_snapshot.json, mag/verkle_audit module
