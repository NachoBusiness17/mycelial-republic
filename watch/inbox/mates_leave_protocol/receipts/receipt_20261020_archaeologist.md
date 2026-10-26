# Receipt: archaeologist, mission 20261020_03, cycle 10 - STATUS: COMPLETE

Mate: THE ARCHAEOLOGIST. Pack: logs/mates/missions/mission_20261020_03_archaeologist.md
(claimed via its .claim sidecar). Start marker filed before speech and overwritten once
with this final content (2 writes total by me). Stop reason: thread exhaustion - every
remaining leg is operator-gated (guard cure, witness credential, re-seal decision,
commit order); context budget also well spent. Persona laws held: zero chain writes
(chain sha byte-identical across three reads), zero paid dispatches, zero LLM
dispatches, zero environment dumps, receipt before speech, em-dash 0.

## FINDINGS

### 1. The freeze is over and the chain is honest end to end (byte-proven)

- Live read: memory/biography/verkle_chain.jsonl = 13,137 rows, 9,577,870 bytes,
  mtime 2026-10-20 08:07:13 EDT, sha256 73C5C4020F54F45AD09ACC06C68A2D45B4965F2076C6A
  4A586D23C48D2C3DBB2. Three sha reads this cycle (initial, pre-pytest, post-pytest)
  byte-identical. Appends resumed: 1,083 rows beyond cycle 7's 12,054 read, first
  2026-10-16T22:28:49.616004Z (18:28:49 EDT), last 2026-10-20T12:07:13.350808Z.
- Independent verification: recomputed the prefix merkle fold per row index; all
  13,137 committed verkle_root values match the recomputed fold (0 mismatches). Tip
  (498 bytes) carries root fedf6c3d20c5965a3e8639fbdde3925fc5049e809f6cad7ed7632c0d
  919a8c95 = tail row root = full fold. mag.chain_guard: tip_matches_chain TRUE -
  the tip canary is green for the first time since 2026-10-10.
- CORRECTION to cycle 7: the freeze was never enforced on appenders. The append path
  verifies chain-internal consistency, not tip-vs-chain, and every append rewrites
  the tip from the true tail (mag/verkle_knot.py:1203-1209, _tip_for_tail +
  _write_tip_atomic). The phantom tip was cured as a side effect of the first
  post-freeze append at 22:28:49Z; no heal operator ever ran.

### 2. The phantom-root class is attributed: the v1 amend re-root machine

- The "phantom" tips (cycle 7's 5e5a8365, unattributable then) were honest roots of
  leaf sets that the v1 amend path destroyed moments later: that path replaces
  rows[existing_i] and rewrites the ENTIRE file via _rewrite_chain (tmp + os.replace),
  recomputing every root. A tip written against the pre-rewrite leaf set matches no
  fold of the post-rewrite file. Cycle 7's own event shape (tip written 05:45:29,
  chain rewritten 05:45:30) is exactly this mechanism.
- Rewrite strata counted from the rows themselves (a rewritten row's ts is its
  re-knot moment; its filename keeps the original date): exactly 24 rows rewritten
  2026-10-17, ALL at prefix indices (<12,016), NONE carrying supersedes fields (v1
  in-place rewrites). This byte-confirms the 10-19 audit's "24 rewrites on 10/17".
- After the flip: configs/mag.yaml:8 chain_mode: v2 with the operator's own dated
  comment ("2026-10-17 operator (Nacho): append-only amends (AH19); was v1"). Rows
  rewritten 10-18: 730, ALL at indices >= 12,016, ALL with supersedes_index; 10-19:
  108, same v2 shape. ZERO prefix rewrites after the flip. The v2 append-correction
  law is working in the bytes.
- Lifetime context: 5,941 rows chain-wide carry a ts that differs from their filename
  date (the amend machine's strata: 3,266 on 10-03, 643 on 10-02, 599 on 10-01,
  366 on 09-27, 154 on 09-26). The machine long predates this incident; the flip
  turned it from a re-writer into an appender.

### 3. The operator-gated amend-path question was answered 2026-10-19: all 5 fixes applied

- Two receipts landed 10-19 (both read in full): watch/inbox/CHAIN_APPENDONLY_RESEARCH_20261019.md
  (grok-bot, Lessig + Ponytail lenses, ranked 5-fix plan, 12:02 PM) and
  watch/inbox/CHAIN_FIXES_APPLIED_20261019.md (1:56 PM, "Operator approved all 5 fixes").
- Applied, per the fix receipt and byte-checked by me: (1) soft NTFS append-only ACL
  on the chain (DENY WD for foste, grant RX,AD); (2) MAG_ALLOW_CHAIN_REWRITE=1 gate on
  _rewrite_chain / v1 amend / heal (verified present at mag/verkle_knot.py:73-82 with
  the receipt citation in the comment); (3) MAG_DISABLE_LAB=1 in compose + container
  recreate (the standing lab writer pid 37980 from cycle 7 is dead); (4) daily prefix
  seal check tools/chain_prefix_seal_check.py wired into scripts/ratchet_daily.ps1;
  (5) fail-closed chain:biography lease + chain_repair --dry no longer takes the
  verkle_lock (verified in the tools/chain_repair.py working diff, gate comment
  dated CHAIN_REWRITE_GATE_20261019).
- The whole bundle is WORKING-TREE ONLY ("No git commit. No push."): mag/verkle_knot.py,
  tools/chain_repair.py, scripts/repair_verkle_chain.py, docker-compose.yml,
  scripts/ratchet_daily.ps1, tools/chain_prefix_seal_check.py (new, untracked),
  tests/test_chain_rewrite_gate_20261019.py (new, untracked), tests/conftest.py
  (+1 fenced dir memory/biography_v2). A fresh checkout currently carries NONE of
  the gates. Commit order owed.
- Prefix seal patrol run by me (read-only): RED by design - n=12016, expect_root
  ab595c338ac0a394, live_row_root 7fe9285a8b31455f, candidate_sha 0da8026d49826152,
  live_prefix_sha 5dc56624d301b45e, exit 1. The 10-17 v1 rewrites permanently scarred
  the sealed prefix; the patrol stays red until a deliberate operator re-seal.

### 4. The guard cure remains unbuilt (proposed cycle 7, re-proposed here)

- chain_guard still resolves knots/ only (mag/chain_guard.py:72); knots_attic holds
  271,993 files invisible to it. Dangling fell from 1,161 (cycle 7) to 10 because the
  amend machine's re-knots wrote fresh knot files into knots/, not because the guard
  learned the attic. 9 rows remain dangling_unflagged: the false-alarm regression the
  cure would end. Marker still stale at 2026-09-26T16:39:15Z (verkle_repair_state.json
  untouched). Guard full verdict: ok false, state regression, rows 13,137, dangling 10,
  evidence_lost 618, expected 620, flag_drift 2, dup_sessions 854, crlf false.

### 5. The tip witness has never once published: 20 fires, all scope-403

- Real home of the log is logs/tip_witness.log (my first listing misattributed it to
  memory/biography; reading error, corrected, no deletion ever happened - noted for
  honesty). 20 START lines lifetime, first 2026-09-30 19:19:16, every fire exit 2
  with "token cannot create gists (HTTP 403)", 0 publishes. The 10-16 09:48:28 fire
  that cycle 7 could not see did happen and failed the same way. The fix is an
  operator credential (PAT with gist write), not code. The 10-19 hardening notice
  (watch/inbox/estate_hardening_notice_20261019.py) adds: all chain backups same
  disk, offsite unscheduled.

### 6. Cured this cycle: the hermeticity tripwire was BOM-blind

- tools/prepush_verkle_hermeticity.py (my cycle-4 wiring, consumer githooks/pre-push
  line 620) full-scan exited 2 ("cannot verify") on tests/test_grokbot_seats.py:
  untracked file, valid Python (collects 6 tests), leading UTF-8 BOM at byte 0. The
  import system strips a BOM per PEP 263; the tripwire's plain utf-8 decode kept
  U+FEFF and ast.parse refused it, blinding the whole scan. Fix: utf-8-sig decode at
  line 305 with a cause-carrying comment naming the evidence. After: selftest 6/6
  PASS, full scan exit 0 ("no unprotected verkle_knot writer reach in tests").

### 7. Proofs run

- Gate suite + spine: pytest tests/test_chain_rewrite_gate_20261019.py +
  tests/test_merkle_cure_p4b_sized.py = 37 passed in 2.33s, chain sha256 and tip
  sha256 byte-identical before and after the run.
- restore_batch arithmetic closes: 798 rows carry restore_batch, all value
  'chain-restore-20261014', indices 11,218 to 12,015 = the restore receipt's
  411 lost_window + 387 live post-overwrite exactly. Cycle 7's 790 was 8 markers
  mid-erosion at its moment. Supersede-copy hypothesis for the regain tested and
  killed: 0 batch rows carry supersedes.
- The conftest fence (cycle 7 open leg 4): the fence IS in HEAD (commit a2ae802a6,
  tests/conftest.py lines 99-119 audit hook over memory/biography, biography_backup,
  runs, state), so a fresh checkout carries it; the working-tree delta only adds
  memory/biography_v2 to the fenced dirs.
- Lock census: holder at first read pid 29068 (start 2026-10-20 08:06:16 EDT,
  heartbeat fresh), gone minutes later - short-lived appender, not a standing
  writer; identity unattributable (process exited before read; its append is the
  08:07:13 tail row).

## JOURNEY

Threads followed, in order, with the why of each turn:

1. Read the pack; filed the start marker; read cycles 7, 8, 9 receipts plus 10-10
   and 10-12 for the full thread state. Turn: resume-not-respawn; dig only the
   undated and the changed.
2. Standing byte read first: the chain had MOVED (13,137 rows vs 12,054; new tip
   root). Turn: date the movement before interpreting anything.
3. Fold recompute attempt 1 malformed (compared the tip to the prefix-root LIST
   object; always False). Logged, not spiraled (positive steering); attempt 2 done
   per-row and clean. Turn: trust bytes, admit the instrument error in the receipt.
4. Dated the resume: first row beyond cycle 7's read at 10-16T22:28:49Z. Turn: what
   cured the tip between 08:55 and 22:28? Read the append path; found the answer
   (appends rewrite the tip from the tail; the tip is never consulted by appenders).
   Cycle 7's gate inference corrected.
5. Git log sweep 10-16 to 10-20: 35 commits, 0 touching chain-class files; found the
   two 10-19 chain receipts, the NIGHT SHIFT commit carrying MAG_DISABLE_LAB, and the
   backup_brain commit's in-passing "chain alive (tip b62c19fe, n=12,621)" of 10-18
   (independent corroboration of the append resume). Turn: the operator-gated legs
   had answered themselves overnight-of-days; my job flipped to verifying their bytes.
6. Read both 10-19 receipts in full; byte-checked each load-bearing claim: mag.yaml
   flip line + operator comment, gate code at verkle_knot.py:73-82, chain_repair gate
   diff, new tool + test files on disk, prefix seal run (RED as designed). Turn:
   verify the cure before celebrating it.
7. Rewind strata from the rows: 24 in-place rewrites 10-17 (prefix, no supersedes),
   then 730 + 108 v2 correction rows (post-prefix, all supersedes), zero prefix
   rewrites after the flip; lifetime amend strata 5,941 rows. Turn: this dates and
   attributes the phantom-root class the last three cycles could not.
8. Guard check + knots census: 10 dangling (was 1,161), 9 unflagged, attic 271,993
   files, marker stale. Turn: is the guard cured? No - the drop is the re-knots'
   doing; the cure stays unbuilt and re-proposed.
9. Witness: found logs/tip_witness.log (after correcting my own path misread); 20
   fires, all 403, 0 publishes. Turn: is the witness dark or dead? Dark on
   credentials, alive on cadence; operator-hands fix named.
10. Tripwire duty: selftest 6/6, scan exit 2 on the BOM file; proved the file
    collects (6 tests) before blaming it; cured the instrument decoder; scan exit 0.
11. Gate-suite proof run with the chain sha frozen; restore_batch arithmetic closed
    (798 = 411 + 387; supersede-copy hypothesis killed).
12. Filed the attention.md cycle-10 block (three open rails + asks); wrote this
    receipt. Stop at thread exhaustion: guard cure, witness credential, re-seal
    decision, and commit order are all operator legs.

Dead ends named for honesty: (a) %TEMP% snapshot caves from cycle 7 (magrestore,
magarch) are gone to temp cleanup; the sealed constants in chain_prefix_seal_check.py
are now the only restore-time reference, so fine-grained prefix-rewrite forensics
(before-images of the 24 rows) can no longer be diffed; (b) the 8-marker erosion and
reappearance between cycle 7's 790 and today's 798 is bounded but its mechanism is
not fully attributable (the current row versions carry the markers; the before-images
are gone with the snapshots); (c) pid 29068 unattributable beyond "short-lived
appender, 08:06:16 to ~08:07 today"; (d) the commit order for the 10-19 bundle (and
my tripwire cure riding the same tree) is not mine to force; (e) the tip witness
credential is operator hands per the ladder law.

## COUNTS

- Receipt files (receipt_*.md) in watch/inbox/mates_leave_protocol/receipts/ now: 97.
  My writes: 2 (start marker overwritten once by this receipt).
- Chain reads: 3 sha256 reads, byte-identical (73C5C402...DBB2); 13,137 rows;
  9,577,870 bytes; mtime 2026-10-20 08:07:13 EDT. Chain writes by this seat: 0.
- Fold verification: 13,137 row roots recomputed, 13,137 match, 0 mismatches; tip =
  tail = full fold (fedf6c3d...); guard tip_matches_chain true; crlf false.
- Appends beyond cycle 7's read: 1,083 (first 2026-10-16T22:28:49.616004Z, last
  2026-10-20T12:07:13.350808Z).
- Rewrite strata: 10-17: 24 rows (24 prefix, 0 supersedes); 10-18: 730 (0 prefix,
  730 supersedes); 10-19: 108 (0 prefix, 108 supersedes). Lifetime ts-vs-filename
  mismatch rows: 5,941 (top: 10-03: 3,266; 10-02: 643; 10-01: 599; 09-27: 366;
  09-26: 154).
- Guard: ok false, regression; dangling 10 (cycle 7: 1,161); dangling_unflagged 9;
  evidence_lost 618; expected 620; flag_drift 2; dup_sessions 854; marker_at
  2026-09-26T16:39:15Z; marker_root_drift 1. knots/ 66,714 files; knots_attic/
  271,993 files.
- restore_batch: 798 rows, 1 distinct value, index span 11,218..12,015; 411 + 387 =
  798; 0 carry supersedes.
- Tip witness: 20 START lines (first 2026-09-30 19:19:16), 0 publishes, 20 exit-2
  scope-403 fires; log at logs/tip_witness.log (7,743 bytes, last fire 10-19 09:30:01).
- Tests: 37 passed in 2.33s (4 gate + 33 p4b); chain and tip sha unchanged across the
  run. Tripwire: selftest 6 cases 6 PASS (twice); scan exit 2 before fix, exit 0
  after.
- Prefix seal: RED by design (exit 1): n=12016, expect ab595c338ac0a394, live
  7fe9285a8b31455f; candidate sha 0da8026d49826152 vs live prefix sha 5dc56624d301b45e.
- Commits since 10-16 in sweep window: 35, of which 0 touch chain-class files; the
  10-19 fix bundle + my tripwire cure ride uncommitted. Commits by me: 0.
- Files written/edited by me this cycle: 2 edits (memory/attention.md cycle-10 block;
  tools/prepush_verkle_hermeticity.py utf-8-sig + cause comment) + this receipt
  (2 writes). Everything else was reads.
- Paid API calls: 0. LLM dispatches: 0. Task agents: 0 (solo seat, peak concurrency 1,
  law cap 16). Environment dumps: 0. RAM-gate deferrals: 0 (heaviest command a
  13,137-row json parse and 9.5 MB sha256 reads). Em-dash bytes in this receipt and
  the attention block: 0.
- Incident age accounting: clobber 2026-10-07/08; restore under GO 10-15/16; freeze
  round 2 declared 10-16 05:45:30; appends resumed 10-16 22:28:49Z; v1 rewrite wave
  10-17 (24 rows); chain_mode v2 flip 10-17 (operator Nacho); v2 correction rows
  10-18/19 (838); all 5 append-only fixes applied with operator approval 10-19;
  tip canary green again by this cycle's read, 10-20.

## Resume-not-respawn

Successor thread state: the incident thread (clobber -> restore -> freeze round 2 ->
v1 rewrite wave -> v2 flip -> append-only gates) is dated end to end and closed to
the edge of the operator gates. Open legs, all operator-gated: (1) guard cure build
(knots_attic awareness + marker refresh; proposed cycles 7 and 10); (2) tip witness
credential (PAT with gist write; 20 failed fires and counting at 09:30 daily);
(3) re-seal decision (prefix seal is RED daily by design until the operator either
re-seals post-restore or accepts red); (4) commit order for the 10-19 bundle (gate
code, ACL, compose env, seal patrol, fence delta) plus my tripwire decoder cure.
Standing duties unchanged: re-verify chain bytes, count witness fires, check seal
color, date any new stratum. Start next cycle at finding 4 and re-read the chain
bytes before anything else (trust bytes, not this report).
