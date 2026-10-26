# Receipt: cartographer cycle 10, corpus/apk fold, resumed (OPEN, stub)

Mate: THE CARTOGRAPHER. Mission pack: logs/mates/missions/mission_20261019_01_cartographer.md
(launched by tools/leave_dispatcher.py, X12 static-runner unblock). Claimed via its .claim
sidecar (was 0 bytes; now carries mate=cartographer cycle=10 thread=corpus-apk
resumed_from=receipt_20261018_cartographer.md status=opening).

Resume-not-respawn: cycle 10 of the cartographer ride. The pack's generic start point
(corpus/oral_history/seat_pools, seed thread session_index.jsonl) was folded at cycle 5
(oral_law_map.jsonl, 63 rows); cycles 6 through 9 rode the receipt chain instead of the generic
start. Cycle 9 (2026-10-18) opened the corpus/apk thread, filed its stub, and died mid-road:
its claim close reads pid=19628 exit=1, no cartographer_20261018_data dir exists, and its
receipt was never amended with FINDINGS, JOURNEY, or COUNTS. The thread is open and unmapped.
Turn taken: resume cycle 9's thread, not the pack's generic start; re-walking mapped ground
spends a cycle on nothing.

First-look truth from disk, measured now (trust bytes, not reports): corpus/apk holds 2 files,
9,360,306 bytes total. aurora_store_76.apk is 9,360,088 bytes (mtime 2026-09-05 14:35:33 local,
sha256 FD9C75D90D0F4A7C132B9B4A5A2CF1992A45E03B8D8FF988B7DCFBC0DB2C4D11);
.mimosa/hook-state/sess_297f5a13-4e0a-4ce3-827a-dff7a3e98386.json is 218 bytes (mtime
2026-09-05 14:35:55 local, sha256 0DD4A1BEFF865C03673E5AEEF304C2E678B5B41C320323C72B7808EE87E76A3A).
Parts sum exactly to the shelf total. This matches cycle 9's stub numbers exactly.

Plan this cycle: identify the apk from bytes (zip central directory, entry census, manifest
data); read the 218-byte hook-state file and name what wrote it; trace the shelf's origin thread
in the receipts (who asked for Aurora Store, when, why); wire tools/ghidra_audit.py in the R2.0
image-digest pattern (cycle 8's debt row 5: the deep rung is vendored-but-unwired, zero .py
consumers); point the wired tool at the shelf one rung in (unzip the apk, census contents,
identify native libraries, analyze one if present); fold thread -> decision -> filed-law-or-debt
rows anchored to verbatim lines; spot-verify a sample of anchors; bank artifacts into
cartographer_20261019_data/ beside this receipt with primaries in logs/mates/cartographer/;
amend this receipt with FINDINGS, JOURNEY, COUNTS; close the claim; name cycle 11's thread.

STEER honored: all reading, extraction, and judgment work is local-seat work on this account;
no Nous/Hermes API, no paid lanes. Rolling concurrency: fan-out sized under 16 simultaneous.
RAM gate: read before any analyzeHeadless launch (27.5 GB free at claim time; gate is free minus
2 GB), recorded in COUNTS. Env vars: never dumped. Positive steering: cycle 9's exit=1 is
logged as weather, its road is picked up here; errors this cycle get logged with cause and fix,
the ride continues.

This stub is filed before any other speech, per the receipt-before-speech law and the operator's
before-and-after instruction. FINDINGS, JOURNEY, and COUNTS will be amended onto this same file
when the fold lands or when the context budget stops the ride (resume-not-respawn applies; the
next cycle resumes by id). No em-dash, real counts only, no fabricated anything.
