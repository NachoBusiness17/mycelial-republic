# B2-264 LINKS.jsonl seal-byte recovery, 2026-09-26

## Verdict

OWED-PARTIAL with NEW live evidence. The two admin-gated sources the brief names are confirmed blocked from this seat: NTFS USN journal (fsutil usn readjournal C: -> "Error: Access is denied") and volume shadow copies (vssadmin list shadows -> "You don't have the correct permissions...elevated administrator privileges"); this box is NOT admin (net session fails). The transcript arm was swept exhaustively instead and comes up empty for the seal window: every trajectory step from 13:05:45Z to 13:22Z across ALL sessions (12 steps enumerated) touched QUEUE.md, the forge daemon, or handoff boards, none wrote LINKS.jsonl; the one LINKS-writing step (scout step 22211 at 13:05:47Z, sess_c424b80a) appended exactly the two scout rows ALERT-ORACLE-CUT and SCOUT-QUIET-LANES, and both are byte-identical INSIDE git blob 116fa75a1 (rows 333-334), so they are not the tail. Reconstruction attempts this lane: blob + each post-blob row of the current file (rows 335-339) with LF/CRLF/no-terminator all fail against 9DC30BDD. THE NEW FINDING: the same mystery-writer class is LIVE and byte-proven right now. LINKS.jsonl grew from B2-221's census 335 rows to 339 this lane; rows 337-339 (20:00:19Z, 20:03:54Z, 20:06:47Z) carry the off-schema hand-append shape ("op":"register", seq, canonical/url, no canonical_sha256 per mag/link_library.py:16) and have ZERO trajectory steps, so an unlogged background process appends LINKS rows on this host, outside the B2-27 add gate and outside the seat trajectory. This is the first live-observed instance of the exact mechanism class that plausibly produced the 193-byte sealed tail, and it makes B2-237's mechanism question answerable by surveillance instead of recovery.

## Evidence file:line quotes

- Admin block: "Error: You don't have the correct permissions to run this command. Please run this utility from a command window that has elevated administrator privileges." (vssadmin list shadows); "Error: Access is denied." (fsutil usn readjournal C:); "NOT-ADMIN" (net session probe).
- Trajectory sweep (steps.jsonl, all sessions, 13:05:45-13:22Z, 12 steps): 22211 scout append (LINKS + endpoint_news + commit), 22212-22219 QUEUE.md appends/queries (sess_fd5ec147), 22214 docker forge daemon (no LINKS in command or output), 22221 handoff board append. No LINKS writer in-window.
- Scout step 22211 (13:05:47.030Z): command appends exactly two rows via json.dumps(ensure_ascii=False) + "\n" then commits; verified "blob[-2] is r1: True", "blob[-1] is r2: True" (r1 ALERT-ORACLE-CUT 649 chars, r2 SCOUT-QUIET-LANES 425 chars, byte-equal inside blob 116fa75a1).
- Seal records (index_events.jsonl): :3088 13:21:20.489Z whole-file sha256 9DC30BDD313CD17A57071253E3C597F1658F458885EE8E9F89CA9067C7949C45; :3091 13:30:57.884Z living size 219904, same sha. Blob 116fa75a1 = 219,711 bytes / 334 rows. Delta = 193, matching B2-221's "219711 + 193" layout arithmetic.
- Live writer evidence (this lane): current LINKS.jsonl 339 rows (B2-221 census: 335). Row 337 ts 20:00:19Z (686 chars), row 338 ts 20:03:54Z (735), row 339 ts 20:06:47Z (5,361, "canonical": "https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching"). Grep: seq fragments "1790452819074584", "1790453034386849", "1790453207582906" in steps.jsonl = False, False, False. Row shape: "{"seq": ..., "ts": ..., "op": "register", "canonical": ...}" (off-schema "op" field, the B2-221-flagged bypass shape).
- Reconstruction failures (this lane): sha256(blob + row N + terminator) for N in 335..339 x {LF, CRLF, none} = 15 candidates, none equal 9DC30BDD (B2-221's ~55k-candidate brute force remains the ceiling).

## Work done

- Ran the admin-gated pulls; recorded the exact denial errors; probed admin status.
- Enumerated the complete trajectory window (all sessions, not just the logged driver); read the scout step's full command; proved its rows are in the blob; read the docker step's command and output; found no LINKS writer in-window.
- Extracted the current file's post-blob rows, tested 15 reconstructions, all fail; consistent with B2-221.
- Discovered and byte-proved the live unlogged-writer class (rows 337-339, no trajectory steps, off-schema shape); named the surveillance follow-up that can capture the writer's row bytes in the act and answer B2-237's mechanism question without admin recovery.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer; recovery stays OWED (admin USN/VSS pull by the operator, or live capture).

## Falsifier

- The brief's original falsifier stands armed: any recovered 219,904-byte state (admin USN/VSS, or a surfaced copy) whose bytes differ from "all-LF rows 1-334 + 193-byte tail" inside rows 1-333, or whose tail is far from 193 bytes, kills the B2-221 reconstruction.
- The live-writer claim dies if rows 337-339 turn up in a trajectory source this lane did not sweep (e.g. a second steps.jsonl for another harness install, or docker-side logs); the sweep named its scope.
- If LINKS.jsonl does NOT grow again without a trajectory step within its normal cadence, the "live unlogged writer" inference weakens to "three unlogged rows once"; the surveillance follow-up is the discriminator.
- Recovery becoming possible (admin shell) retro-activates this brief: the diff command is sha256 over the recovered 219,904 bytes vs 9DC30BDD, then row-level diff vs blob 116fa75a1.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_221_prefix_editor_20260926.md (Evidence + Work done, the reconstruction ceiling); watch/inbox/burn_wave_20260926/B2_222_hot_living_20260926.md line 28 (sibling touches); watch/inbox/index_events.jsonl :3088, :3091, :3076, :3100; git show 116fa75a1:watch/inbox/LINKS.jsonl (219,711 bytes, 334 rows, scout rows verified inside); memory/trajectory/steps.jsonl (full window sweep, step 22211, step 22214); watch/inbox/LINKS.jsonl current bytes (339 rows, rows 335-339 quoted); vssadmin/fsutil/net session denial transcripts. No web sources. Em-dash count 0.
