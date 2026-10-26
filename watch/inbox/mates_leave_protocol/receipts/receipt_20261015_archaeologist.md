# Receipt: archaeologist, mission 20261015_03, cycle 6 - STATUS: COMPLETE

Mate: THE ARCHAEOLOGIST. Pack: logs/mates/missions/mission_20261015_03_archaeologist.md
(claimed via .claim sidecar 08:12:02). Start marker filed before speech, overwritten at
close per the pack contract (2 writes total by me). Stop reason: rideable surface
exhausted (restore GO-gated; the hybrid-tip writer hunt ended in artifact absence, the
honest limit; the class cure is drafted and filed) with context budget also well spent.
Persona laws held: zero chain writes (sha identical at boot and close), zero paid
dispatches, zero LLM dispatches, zero env dumps, receipt before speech, em-dash 0.

## FINDINGS

### 1. The headline is now the WRITE-FREEZE, and the locksmith filed the same page independently

- The estate's chain has refused every append since 2026-10-10T03:52:31Z. I verified the
  mechanism in code this cycle: mag/verkle_knot.py's INTEGRITY GATE (its own comment:
  "2026-08-16, party_subchain pattern: refuse to extend an unverified chain") sits at the
  top of _append_verkle_knot_unlocked and returns "refusing to extend an unverified
  verkle chain" while the tip root mismatches the recomputed root. The gate is an August
  founding decision still load-bearing: git log -S dates its first commit to 799ddb6fe
  ("wip 20260819", LOCAL ONLY, not pushed).
- The locksmith's [priority][decision] row (memory/attention.md:1223) asks the operator
  to BLESS THE CHAIN HEAL; I verified both of its citations byte-present:
  watch/inbox/PROMISE_PILE_LEDGER_20261013_locksmith.md row 1 (owner O, "RE-ASK,
  SHARPEST"; notes the VERKLE_V2 flip queues behind the heal) and
  watch/inbox/BASECAMP_20261011.md Amendment 1 (the L112-area analysis: n_leaves and
  last-leaf hash agree between tip anchor and chain tail, only the root differs; the
  chain side is content-consistent; the anchor root matches nothing recomputable).
- Two boots anchor two different roots, byte-witnessed this cycle: memory/rib_boot.json
  stamps the TIP FILE's root 2b1da0ea... as ok:true (its chain block copies the tip's
  fields verbatim), while memory/warm_state.json carries the honest tail root
  ae71aee2558f1419... This is the BASECAMP's "default boot path ... invisible mismatch"
  class, now on the record from two independent boot artifacts.

### 2. New forensics: the last row ts corrected, and a post-walk uninstrumented write pair proven

- The last chain row's ts is 2026-10-10T03:52:31.494745Z EXACTLY (byte-read this cycle).
  Cycles 2 and 5 recorded ":35" as the row time; that was the chain FILE mtime
  (23:52:35 EDT = 03:52:35Z), not the row ts. The locksmith's 03:52:31Z was exact.
- Write-order forensics: last row appended 03:52:31.49Z; the TIP file's mtime is
  23:52:34 EDT (03:52:34Z); the CHAIN file's mtime is 23:52:35 EDT (03:52:35Z). So the
  tip was rewritten ~3 seconds AFTER the last append, and the chain file was rewritten
  ~1 second after that, with NO new row (no row carries a ts after :31.49). The append
  path writes chain-then-tip under the lock in one call; no current writer produces a
  tip-then-chain pair. This is a third uninstrumented write event, after the 10-07/08
  clobber and the 10-10 walk itself.
- The tip on disk is a hybrid: root 2b1da0ea599a0755... (stale, unattributable) over
  n_leaves 3,415, last_leaf_hash cc6ea448..., last_filename
  2026-10-10_0351_mirror_01a123f0_2362d100.knot.json, updated_minute 2026-10-10T03:52:00Z
  (all real tail fields, minute-truncated). Its note string is _tip_for_tail's.

### 3. The tip root 2b1da0ea equals NO recompute of any natural hash set (11 folds computed, 0 matched)

- Over the current 3,415 stored leaf hashes: legacy full fold = ae71aee2558f1419 (equals
  the tail row's committed root, confirming the chain side), sized fold = bb3d2abd,
  drop-first-3 = 3c211769, reversed = 699c0e8d, deduped (no dups exist) = ae71aee2,
  prefix-3414 = 7ad1d94b, first-3 = 365c8734.
- Over the 10-03 backup's 11,201 hashes: full = fb517e63, prefix-8839 = 5e7dbc53,
  prefix-8212 = ff87d695, prefix-7757 = 51205ca4.
- Six tip backups on disk carry six other roots (133bca5f/n2, 7c459c00/n7757,
  392349eb/n7369, ddb671bc/n7369, 3db7799f/n7924, a57b50f3/n7377): none is 2b1da0ea.
- CORRECTION to cycle 2's record: row 2's committed root is 365c87341475cbfb, and my own
  recompute confirms 365c8734 IS the legacy fold over the three fixture leaves. Therefore
  the fixture tip _hand_chain would write would carry root 365c8734 with n_leaves 3, and
  the surviving tip (2b1da0ea, n 3,415) is NOT the fixture tip: it is a third artifact.
  Cycle 2's "the live tip was overwritten with the fixture tip" described the test's
  action correctly but the surviving bytes are a later hybrid, not fixture bytes.
- 2b1da0ea appears in exactly one other file I could find (git grep + targeted sweeps):
  memory/rib_boot.json, which merely witnesses the tip (its stamp is generated fresh;
  today's regeneration ~07:26 EDT shows age_min 7643.2 from the tip's generated ts).

### 4. The hybrid tip's writer is UNATTRIBUTABLE from every artifact tried; walk-time code is byte-exonerated

- The walk ran on commit 6685db6bc's mag/verkle_knot.py: 1,173 lines, byte-identical to
  the working tree (diff shows only em-dash mojibake artifacts from my own extraction).
  The walk therefore used today's append path, whose every successful append writes a
  full-recompute tip (root = fold over all hashes so far, via _tip_for_tail +
  _write_tip_atomic). The final append would have left root ae71aee2. It did not.
- All production _tip_for_tail/_write_tip_atomic call sites enumerated: vk repair
  (recomputes), vk append (recomputes), vk self-heal (recomputes true root),
  mag/merkle_sized.py migration (would stamp merkle_binding into the tip; absent),
  mag/usage_digest.py (manual tip dict, different note and updated_minute=None shape),
  tools/chain_repair.py (recomputes true root), tests/test_merkle_cure_p4b_sized.py
  _hand_chain (would write n=3 fixture fields). None can produce the hybrid. The
  dashboard/rest.py, dashboard/server.py and the mag/* files matching "verkle_tip" are
  readers.
- Named honestly: the writer's identity is beyond the surviving artifacts. Its
  SIGNATURE is now on record (writes a _tip_for_tail-shaped tip whose root matches no
  current-code fold, then touches the chain without appending a row). This is the same
  class as the 10-02 incident (attention.md:280: tip aba227fd matched NO chain prefix
  while all 8,839 rows stayed consistent, "mixed-version writer race suspected", healed
  same day by repair_tip_if_consistent): the SECOND unattributable-root incident, and
  the overall THIRD uninstrumented write to the substrate after B2-388 (09-26) and the
  walk (10-10).

### 5. Class cure drafted this cycle (cycle-5 next-cycle item 4, spec before behavior)

- watch/inbox/DROP_CHAIN_WRITE_RECEIPT_LAW_20261015_archaeologist.md: any writer of
  verkle_chain.jsonl or verkle_tip.json must (a) hold the verkle lock, (b) write a
  pre-write .bak, (c) append a receipt row to watch/inbox/CHAIN_WRITE_LOG.jsonl
  (ts, writer id, rows/bytes/sha before and after), (d) fail closed. Enforcement v1 is
  a daily mtime/sha patrol vs the write log (WARN-ONLY first landing, t40/B2-215
  precedent); v2 routes stamping into the vk helpers. Falsifier named. The proposal
  does NOT unblock the restore; it governs the next write, whatever its author.

### 6. Standing state re-verified by bytes (boot and close reads identical)

- Chain: 3,415 rows, 2,506,261 bytes, mtime 2026-10-09 23:52:35 EDT, sha256
  EB07097CBE05B348DEE736451F32D2F4488F6773E5F453D46758453CFD6D91FA. Static 6 days over
  the clobbered state; the walk has NOT resumed.
- chain_guard check (read-only): ok false, regression, rows 3,415, dangling 9,
  evidence_lost 0, expected_evidence_lost 620, flag_drift 620, tip_root 2b1da0ea599a0755
  vs chain_root ae71aee2558f1419, tip_matches_chain false, marker stale
  2026-09-26T16:39:15Z. Unchanged across cycles 3-6.
- No operator GO anywhere: zknot LATEST (operator window is gstd/v8/spore work), 
  state/CURRENT.md chain hits are unrelated on-chain crypto work, attention.md carries
  no chain order, 28 commits since 2026-10-13 00:00 with zero chain/verkle/merkle
  subjects. The three evidentiary files remain uncommitted (tests/test_merkle_cure_
  p4b_sized.py M, githooks/pre-push M, tools/queue_close.py M;
  tools/prepush_verkle_hermeticity.py untracked).
- Tip witness: 15 runs total (2026-09-30 19:19:16 first, 2026-10-14 09:30:02 last),
  zero PUBLISHED ever, every run HTTP 403 (gist scope). The 10-15 09:30 fire had not
  run at ride close (08:22 EDT). Fix named in the witness's own output: fine-grained
  PAT with Account permissions Gists read/write, or a classic PAT with gist scope.

## JOURNEY

Threads followed, in order, with the why of each turn:

1. Read the pack; its seed row points at the live successor thread. Filed the start
   marker. Turn: contract first.
2. Read all five prior archaeologist receipts in full (10-06 c1, 10-10 c2, 10-12 c3,
   10-13 c4, 10-14 c5) plus zknot LATEST. Turn: resume-not-respawn; dig only the
   undated and the changed.
3. Standing duties in order: chain bytes (boot read identical to cycle 5's close),
   git status (evidentiary files still uncommitted), commit sweep since 10-13 (28
   commits, 0 chain-subject), chain_guard check (unchanged regression), tip_witness
   count (15/0). Dead end in the literal sense: no GO anywhere; restore stays gated.
4. NEW STRATUM: attention.md:1223 locksmith BLESS-THE-CHAIN-HEAL row. Turn: a
   [priority][decision] ask citing two files is exactly my hunting ground; verified
   both citations byte-present (PROMISE_PILE row 1, BASECAMP Amendment 1). The freeze
   (appends refuse since 03:52:31Z) became the ride's headline.
5. Mechanism dig: read the gate, append path, tip writer, repair path in
   mag/verkle_knot.py. Found the INTEGRITY GATE, comment-dated 2026-08-16; git log -S
   pinned its birth commit 799ddb6fe (wip 20260819, LOCAL ONLY). Turn: the pack's
   hunting ground names August strata still load-bearing; this one freezes the estate's
   spine.
6. Tip forensics: read the tip file (hybrid), stat'ed tip and chain mtimes, byte-read
   the last row ts (03:52:31.494745Z; corrects cycles 2/5's ":35" which was the file
   mtime; cycle 5's "if the chain moves, date it from row ts" instruction followed).
7. Root hunt: computed 11 candidate folds over current and backup hash sets (legacy
   full/prefix/drop-head/reversed/dedup/first-3; sized; backup full/8839/8212/7757).
   Zero matched 2b1da0ea. Turn: extend the BASECAMP's negative finding with
   independent variants before claiming unattributable.
8. Fixture identity check: read chain rows 0-2 (roots 0cf389f5/51baf40a/365c8734),
   recomputed the fixture folds, proved the surviving tip is NOT the fixture tip.
   Filed the cycle-2 correction in FINDINGS 3 (the archaeologist does not bury
   errata).
9. Walk-time code reconstruction: extracted mag/verkle_knot.py at 6685db6bc, diffed
   against the working tree (byte-identical, 1,173 lines). Turn: if the walk wrote
   full-recompute tips, the hybrid tip is a post-walk write; that re-dates the
   incident surface.
10. Writer enumeration: every _tip_for_tail/_write_tip_atomic call site read and
    eliminated on shape (binding stamp absent, note string wrong, n=3 wrong, true-root
    wrong). Dead end named: unattributable from surviving artifacts; signature filed
    instead.
11. rib_boot.json found as the only other 2b1da0ea carrier (witness, not origin);
    warm_state.json found anchoring the honest root ae71aee2 (two boots, two roots).
12. Third-instance pattern closed: read attention.md's 10-02 incident line (aba227fd,
    same class, healed by repair_tip_if_consistent). Turn: the class already has a
    sanctioned healer; what it lacks is a write law. That became the product.
13. Product: drafted the chain-write receipt law spec (4 legs, 2 enforcement tiers,
    falsifier) and appended the cycle-6 UPDATE line to the attention.md alert block.
14. Close duties: final chain sha read (identical), receipt-dir census (63), pack
    claim check (.claim sidecar present, 0 bytes, 08:12:02), em-dash check on my two
    written files (0 hits). Wrote this receipt, then spoke.
15. Dead ends named for honesty: (a) no GO, restore untouched; (b) the hybrid-tip
    writer unattributable (11 recomputes, 6 backups, 7 call sites, walk-time code
    diff, rib_boot witness all exhausted); (c) whole-estate recursive sweep timed out
    at 120s (cycle 2's lesson re-learned: never walk the 68GB tree; replaced with
    targeted reads); (d) mesh index snapshots hold file shas, not tip roots: no dating
    value; (e) PowerShell one-liner JSON parsing failed on multi-line tip backups
    (replaced with a python read); (f) the Grep tool searched the whole mag/ tree when
    I pointed it at one file (switched to Select-String with an explicit path).

## COUNTS

- Receipt files (receipt_*.md) in watch/inbox/mates_leave_protocol/receipts/ at close:
  63 (cycle 5 closed at 55). My writes: 2 (start marker overwritten once).
- Chain reads this cycle: 2 sha reads (boot 08:22:47, close), byte-identical: 3,415
  rows, 2,506,261 bytes, mtime 2026-10-09 23:52:35 EDT, sha256
  EB07097CBE05B348DEE736451F32D2F4488F6773E5F453D46758453CFD6D91FA. Days static: 6.
  Chain writes by this seat: 0.
- chain_guard today: ok false; regression; dangling 9; dangling_unflagged 9;
  evidence_lost 0; expected_evidence_lost 620; flag_drift 620; tip 2b1da0ea599a0755 vs
  chain ae71aee2558f1419 (mismatch); dup_sessions 0; marker e26157d613efd104 at
  2026-09-26T16:39:15Z.
- Freeze accounting: appends refused since 2026-10-10T03:52:31.494745Z; at ride close
  (2026-10-15 08:22 EDT = 12:22Z) that is 5 days 8 hours 30 minutes of write-freeze.
- Root recomputes this cycle: 11 (7 over the current hash set, 4 over the 10-03
  backup), matches for 2b1da0ea: 0. Tip backups read: 6, matches: 0.
- Tip-writer call sites enumerated and eliminated: 7 production + 1 test.
- Commits dated as evidence: 2 primary (799ddb6fe gate birth, wip 20260819 LOCAL ONLY;
  6685db6bc walk-time code, byte-compared). Commit sweep since 2026-10-13 00:00: 28
  commits, 0 chain/verkle/merkle-subject.
- Locksmith citations verified: 2 of 2 byte-present.
- Tip witness: 15 runs lifetime, 0 published, last run 2026-10-14 09:30:02.
- Files written by me this cycle: 3 (memory/attention.md UPDATE line,
  watch/inbox/DROP_CHAIN_WRITE_RECEIPT_LAW_20261015_archaeologist.md, this receipt as
  2 writes). Files edited: 1 (attention.md). Commits: 0 (no commit order received).
  Uncommitted evidentiary files riding the tree: 3 M + 1 untracked (unchanged).
- Paid API calls this mission: 0. LLM dispatches: 0. Task agents: 0 (solo seat,
  concurrency peak 1, law cap 16). Environment dumps: 0. RAM-gate deferrals: 0 (all
  commands light; heaviest was a sha256 over 2.5MB and python imports).
  Em-dash bytes in this receipt: 0.
- Incident age accounting: clobber 2026-10-07/08; first record 10-10 (cycle 2); first
  operator page 10-12 (cycle 3); class gate standing 10-13 (cycle 4); walk classified
  10-14 (cycle 5); write-freeze named and third instance proven 10-15 (this cycle);
  restore: still blocked on operator GO at close.

## Resume-not-respawn

Successor thread state for the next cycle: receipt_20261010 finding 5 steps 1-3
(restore from the 10-03 backup under the verkle lock, tip heal via the
mag.verkle_audit module verb, guard re-mark) remain blocked on operator GO; start
there the moment GO exists and re-read the backup head before anything else (trust
bytes). New this cycle: the hybrid-tip writer hunt is at its artifact floor; if
resumed, re-run the 11 recomputes against any NEW tip root that appears and check
CHAIN_WRITE_LOG.jsonl (proposed in the DROP) for a first row. The class cure spec
waits an operator decision; enforcement v1 is patrol-class and cheap. Standing duties
unchanged: re-verify chain static, re-sweep for GO, confirm the wired gate still scans
green, and date any new stratum that appears.

## CLOSING ADDENDUM (same cycle, post-receipt deep close, 2026-10-15 ~09:55 EDT)

Filed after the receipt was first written: the mixed-version hypothesis from the
10-02 precedent had not actually been tested, and it was the strongest one. Tested
now. Receipt contract honored with an amendment, not a rewrite.

1. Mixed-version fold hypothesis ELIMINATED. The fold algorithm (H(b"node:" +
   left + b":" + right), duplicate-last padding, leaf:/empty domains) is identical
   across every reachable vk version: the gate-birth commit 799ddb6fe (wip 20260819,
   extracted via git show), the 09-12 snapshot
   (dist_audit/nacho_business_audit_20260912T214050Z/mag/verkle_knot.py:147), and the
   current tree (mag/verkle_knot.py:245). No version difference can produce 2b1da0ea.
   The S4verkle evidence copy
   (watch/inbox/model_garden/premium_autopsy/evidence/S4verkle/00__verkle_knot.py) is
   a truncated autopsy replay (head 7,875 + tail 2,625 of 47,886 chars, moment
   2026-10-01), not runnable; its visible head carries the same algorithm.
2. Domain-variant sweep: 11 fold variants over the current 3,415 stored hashes
   (node: no-sep, no-domain colon, no-domain no-sep, N:, merkle:, raw-bytes operands,
   reversed operands, single concatenation, running hash, last-leaf passthrough):
   zero match.
3. Truncated-view sweep: all 3,415 suffix folds rows[k:3415] (the artifact a
   head-truncated mid-walk reader would produce; the hybrid tip's last_leaf_hash
   matches the true tail, so the writer's set ended at cc6ea448): zero match.
   Double-loaded set (6,830 leaves), drop-1-head, drop-1-tail: zero match. drop-1-tail
   reproduces the receipt's prefix-3414 value 7ad1d94b, confirming instrument
   consistency.
4. Knot re-derivation attempt INCONCLUSIVE (named, not buried): naive leaf_hash
   recompute from the knot files mismatches stored hashes on 3,406 of 3,415 rows,
   which proves knot file bytes are NOT byte-identical to the append-time leaf dict
   (extra or missing keys beyond leaf_hash). A faithful re-derivation requires
   porting the exact dossier-to-leaf construction (mag/verkle_knot.py:379-412) over
   all dossiers: beyond this cycle's time-box. This also sharpens BASECAMP's
   "197/197 knot stems reproduce row hashes": stems reproduce, whole-dict rehashes do
   not. The surviving untested family is exactly this: a writer folding a hash set
   not derivable from live-chain or backup bytes.
5. Tip witness correction: 16 runs, not 15. The task fired today (Last Run
   10/15 09:30:01, Result 2; alert section landed at memory/attention.md:1381 with
   the usual exit-2 scope verdict) but wrote NO lines to logs/tip_witness.log (the
   log still ends at 10-14 09:30:02): a log-append anomaly, alert channel healthy.
   Zero published lifetime, unchanged.
6. Verdict unchanged and now floor-tested: the 2b1da0ea writer remains
   unattributable. Elimination attempts this cycle total: 11 natural-set recomputes +
   11 domain variants + 3,415 suffix folds + double-load + drop-1-head + drop-1-tail
   + 3-version algorithm identity check + 1 inconclusive knot re-derivation + 6
   backup tips + all tip-writer call sites. Every candidate set derivable from live
   or backup bytes is now excluded.
7. Chain re-verified static after all sweeps (3rd read this cycle): 3,415 rows,
   2,506,261 bytes, mtime 2026-10-09 23:52:35 EDT, sha256
   EB07097CBE05B348DEE736451F32D2F4488F6773E5F453D46758453CFD6D91FA. Zero chain
   writes by this seat, full stop. Em-dashes in this addendum: 0.
