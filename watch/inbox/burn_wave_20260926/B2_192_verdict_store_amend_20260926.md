# B2-192 Verdict-store spec gap, 2026-09-26

## Verdict

DECIDED: amend the owning doc (the brief's option b) — queue/lanes/<lane>/trail.jsonl is named the canonical verdict store in watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md section 2, via a dated in-place amendment directly under the stale sentence. No verdict-row appender to memory/law/enforcement_trail.jsonl was built, deliberately: the bytes show verdict rows already flow to the lane trails (mag/lane_runner.py _trail and the GATE_VERDICT_V2 writer both append to lane_dir/trail.jsonl) and the B2-34 cluster organ reads exactly that store (_trail_verdicts, "the file gate_drop actually writes"), so the doc sentence was the only stale byte in the loop. memory/law/enforcement_trail.jsonl re-verified this lane: 935 rows, zero containing "verdict" — it is the LAW-enforcement trail (mag/law.py TRAIL constant), a different schema, and pointing verdict rows at it would co-mix two ledgers for zero readers.

## Evidence file:line quotes

- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md:33 (pre-edit): "The muratcan fold: cluster before propose, not once by hand. Append every verdict row to `memory/law/enforcement_trail.jsonl` as today, plus a rolling cluster step in the lane runner:".
- Same file (post-edit), lines 35-40: "> **Canonical verdict store (amendment 2026-09-26, burn lane B2-192):** verdict rows live in > `queue/lanes/<lane>/trail.jsonl` (the file the lane runner's `_trail`/GATE_VERDICT and > GATE_VERDICT_V2 writers actually append to, and the only store the B2-34 cluster organ > reads). The original sentence naming `memory/law/enforcement_trail.jsonl` was stale spec: ... No verdict-row appender is to be pointed at it; the lane trail is canonical for verdicts."
- mag/law.py:47: TRAIL = LAW_DIR / "enforcement_trail.jsonl"; live count this lane: 935 rows in memory/law/enforcement_trail.jsonl, grep -c 'verdict' = 0.
- mag/lane_runner.py:89 `with (lane_dir / "trail.jsonl").open("a", encoding="utf-8") as f:` (the _trail writer); :321-324 the GATE_VERDICT_V2 row build and append to the same file; :384 _trail_verdicts reads GATE_VERDICT_V2 from queue/lanes/<lane>/trail.jsonl (per the B2-34 receipt: "the file gate_drop actually writes").
- Live trail census this lane: queue/lanes/builder/trail.jsonl 1,015 rows; day_work 1,475; economist 36; elder 29; bard_ledger 34; android_surface 12; forge 24; harvest 24 — the verdict rows live there, not in the law trail.
- watch/inbox/burn_wave_20260926/B2_34_cluster_detectors_20260926.md: "reads GATE_VERDICT_V2 nested verdict objects from queue/lanes/<lane>/trail.jsonl, the file gate_drop actually writes".

## Work done

- Claim law: CLAIM SW-00 filed for the working-tree-modified owning doc before reading-for-edit; retired at landing.
- Verified the gap in bytes: 935 law rows / zero verdict rows in enforcement_trail.jsonl; located the doc file (watch/inbox/, the repo-root path does not exist); located the real writers and the real reader.
- Weighed the arms: an appender to the law trail would create a second verdict store nobody reads and co-mix schemas; amending names the existing, read, written store canonical. Amend chosen.
- Edited the doc: the stale sentence now reads "Append every verdict row to the lane's own trail" with the dated amendment block directly beneath it (no-erase preserved: original wording quoted inside the amendment), naming writers, reader, and the reason.
- Em-dash check: 0 in added bytes. Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Any module that starts appending verdict rows to memory/law/enforcement_trail.jsonl after this amendment contradicts the spec and must be reverted or re-amended with a new dated block.
- If the lane trails are ever renamed/moved (queue/lanes/<lane>/trail.jsonl path change), this amendment and the B2-34 organ break together; the amendment names the path, so the break will be loud.
- A reader citing BURN doc line 33 verbatim from a pre-amendment copy (git history keeps it) must find the amendment immediately beneath; if the amendment block is deleted without a successor block, the stale spec is back.
- The zero-verdict count in the law trail is a snapshot; the law stands regardless, but a sudden non-zero count with no module change is the falsifier firing.

## Bibliography closed

watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md (section 2 pre/post-edit); mag/law.py (TRAIL constant); memory/law/enforcement_trail.jsonl (935-row census); mag/lane_runner.py (_trail :89, GATE_VERDICT :192, GATE_VERDICT_V2 :306-324, _trail_verdicts :384); queue/lanes/*/trail.jsonl row counts; watch/inbox/burn_wave_20260926/B2_34_cluster_detectors_20260926.md. No web sources. Em-dash count 0.
