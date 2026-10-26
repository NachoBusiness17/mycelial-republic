# T1W1_RACTOR: ractor distillation of the four stranger audits

Sources (premium verdicts, reasoning-channel traces, anthrop/claude-opus-5.5, landed 2026-10-01):

- watch/inbox/hermes_burn/T1W1_stranger_boot_path.md
- watch/inbox/hermes_burn/T1W1_stranger_shared_surface.md
- watch/inbox/hermes_burn/T1W1_stranger_auth_stack.md
- watch/inbox/hermes_burn/T1W1_stranger_verkle.md

Method: every quote below was byte-verified with a fixed-string sweep against the four source files (57 candidates, 5 misses dropped or re-cut to hitting substrings; no quote contains an em-dash). Every ticket names the estate bytes this distillation itself re-read (file:line pins from grep/sed on 2026-10-01). Live chain truth at distillation moment: 8777 rows in memory/biography/verkle_chain.jsonl, all hashed, last row n_leaves 8777, chain_mode absent (v1) in the tail rows.

---

## LAWS

### L1. witness prefix-consistency (LAG launders rewrites)
- law: witness prefix-consistency
- claim: An external witness that compares only (root, n_leaves) at the tip cannot tell growth from rewrite-then-grow: any interior rewrite paired with one append reads as normal LAG and publish advances the ratchet onto the tampered root. The only external defense is a prefix check: recompute the commitment at the witnessed length over the live data and refuse on mismatch. Verified in bytes: tools/tip_witness.py:112-119 returns WITNESS-LAG for any live n greater than witnessed n with no prefix verification, and the module docstring (lines 10-11) claims a rewritten chain cannot drag the witness with it, which the LAG branch disproves for rewrite-plus-append.
- quote: "an attacker could rewrite an interior entry, append a single new leaf, and the comparison would just report LAG rather than detecting the tampering"
- source: watch/inbox/hermes_burn/T1W1_stranger_verkle.md
- steal (one sitting): extend tools/tip_witness.py compare() to recompute the prefix root at witnessed n_leaves from the chain file (reuse the prefix-root helper in mag/verkle_knot.py) and return WITNESS-REWRITTEN on mismatch; pure appends must still return LAG.
- falsifier: a ten-leaf chain, witnessed, with one interior leaf mutated plus one append, where compare() still says WITNESS-LAG and publish advances. The current bytes falsify the docstring today; the patched compare must flip that case to WITNESS-REWRITTEN while keeping honest appends at LAG.
- leverage: high

### L2. writer-only gates prove consistency, never provenance
- law: self-referential gate limit
- claim: A hash gate the writer itself recomputes proves internal consistency only; against anyone with write access, tamper-evidence is zero, so every in-repo integrity gate must either name its external anchor or admit it has none. Verified in bytes: mag/verkle_knot.py:614-632 (_verify_chain_consistent) rebuilds the merkle tree over the leaf_hash column the writer itself stores and checks only the last row root plus the tip.
- quote: "Every writer recomputes its own commitments, so tamper-evidence means nothing against a malicious writer"
- source: watch/inbox/hermes_burn/T1W1_stranger_verkle.md
- steal (one sitting): add one docstring line to mag/verkle_knot.py::_verify_chain_consistent naming it a consistency-only gate and pointing at tools/tip_witness.py as the only provenance anchor.
- falsifier: an in-repo gate catching a full consistent recompute by the legitimate writer. Impossible by construction; that impossibility is the law.
- leverage: high

### L3. a merkle root under duplicate-last padding does not bind leaf count
- law: root-count binding (CVE-2012-2459 class)
- claim: With duplicate-last padding, one root covers at least two leaf counts ([a,b,c] and [a,b,c,c] share a root), so a root check alone never binds chain length; root and count must be checked as a pair, and membership proofs must bind index and count. Verified in bytes: mag/verkle_knot.py:223-226 documents the "legacy duplicate-last Merkle root" construction; the witness binds n (tip_witness compare line 112), the chain gate does not (mag/verkle_knot.py:614-632 checks roots only).
- quote: "the duplicate-last-leaf Merkle construction echoes the classic CVE-2012-2459 vulnerability"
- source: watch/inbox/hermes_burn/T1W1_stranger_verkle.md
- steal (one sitting): grep every consumer of _merkle_root (mag/verkle_knot.py, tools/chain_repair.py) and confirm each pairs the root with a leaf count before trusting it; file the pairing table as a receipt row.
- falsifier: two different-count leaf sets producing different roots at every prefix under the estate's construction. If that holds the law dies; the construction guarantees it will not.
- leverage: medium

### L4. a reader stamping its own clock launders freshness
- law: freshness-field provenance
- claim: A reader that reports its own clock as the freshness of a frozen artifact makes stale bytes look live; freshness fields must carry the artifact's own mtime (or the source's timestamp), never read time. Verified in bytes: mag/hermes_warm_boot.py:184 returns "updated": _now() for memory/briefs/latest.md, which AGENTS.md declares FROZEN 2026-09-26; every warm boot reports the frozen brief as updated-now.
- quote: "effectively lying about freshness"
- source: watch/inbox/hermes_burn/T1W1_stranger_boot_path.md
- steal (one sitting): change mag/hermes_warm_boot.py:184 to report BRIEF.stat().st_mtime (ISO) instead of _now(), or drop the field.
- falsifier: a warm_state.json whose session_brief.updated equals the brief file's mtime after the fix. Today it always equals read time, so the falsifier cannot fire pre-fix.
- leverage: medium

### L5. in a seq-ordered append-only log, the biggest writer-chosen seq wins
- law: seq oligarchy (shared surface ordering)
- claim: Where events are ordered by writer-chosen seq and the fold is last-register-wins, the writer that mints the largest seq owns the final state; without writer authentication, any seat can forge any event under any writer string, and a bytes-versus-recorded-sha validate cannot see who wrote or whether history was replayed. Verified in bytes: scripts/index_fold_host.mjs:42-56 (exact seqs compare via BigInt, last-register-wins named at line 47), and no prev_hash anywhere in the fold.
- quote: "an attacker could pick an absurdly large seq value to force their write to win every ordering comparison"
- source: watch/inbox/hermes_burn/T1W1_stranger_shared_surface.md
- steal (one sitting): add a fold warning in scripts/index_fold_host.mjs when an event's seq exceeds that writer's prior max by more than one step; lands as noise-naming, not a redesign.
- falsifier: a fold that flags or rejects a forged writer string or a seq jump while accepting honest same-writer events. Nothing in the current fold reads writer identity, so the falsifier cannot fire today.
- leverage: high

### L6. authenticating the transport does not authorize the identity in the payload
- law: connection-versus-identity (sid as bearer token)
- claim: If an op handler takes the session id from the message body while the frame-MAC gate arms only for sessions that opted in, the sid is a bearer token replayable from any fresh unauthenticated connection; identity must be bound to the connection at hello. Verified in bytes: server/server.py:313-317 applies the MAC gate only when peer["mac_state"] is not None, line 350-351 dispatches op "action" straight to _admit_action(msg), and _admit_action (line 655) receives no peer at all.
- quote: "frame MACs protect the connection but sids authorize the action"
- source: watch/inbox/hermes_burn/T1W1_stranger_auth_stack.md
- steal (one sitting): bind sid to peer id at hello (self._peers already keys by connection) and reject op "action" when the connection never hello'd that sid; structural check, no crypto needed.
- falsifier: a bare op "action" with a foreign sid rejected by a default-flags server (allow_plaintext_hello=True, require_frame_mac=False today, so the falsifier cannot fire pre-fix).
- leverage: high

### L7. a repair tool that recomputes commitments is a laundering primitive
- law: repair must not launder
- claim: Any tool that rewrites commitments over whatever data it finds converts repair into laundering; repair must be restricted to the last committed row, must refuse to shrink the tip below the chain's leaf count, and must match a recognized race signature before overwriting anything. Verified in bytes: tools/chain_repair.py:39-46 (find_bad_tail_index walks rows from index 0, head-first, despite the name) and :63 plus :70 (repair writes the FULL-chain root into rows[bad_i], corrupting an interior row when the first mismatch is not the last).
- quote: "chain_repair fixes only the first bad row without re-verifying the rest"
- source: watch/inbox/hermes_burn/T1W1_stranger_verkle.md
- steal (one sitting): make find_bad_tail_index scan from the tail and exit 2 (refuse) when the first mismatch is not the final hashed row.
- falsifier: a repair run that heals an interior mismatch with post-verify passing. Today the full-root overwrite leaves the tail stale and post-verify returns 1, but the corrupted write already happened; the patched tool must refuse before writing.
- leverage: high

### L8. an unread external checkpoint witnesses only its own writer
- law: external anchor is the revision history
- claim: A published checkpoint nobody else consumes is a witness only to its writer; the actual trust anchor is the host's append-only revision history, so verification must walk revisions and enforce monotonic leaf counts rather than trusting the current line.
- quote: "a witness nobody else reads isn't really independent verification"
- source: watch/inbox/hermes_burn/T1W1_stranger_verkle.md
- steal (one sitting): extend tools/tip_witness.py --verify to fetch the gist history array and assert n_leaves never decreases across revisions.
- falsifier: a gist revision whose n_leaves decreases yet verify passes.
- leverage: medium

### L9. unrotated compromised credentials outrank every cryptographic defense
- law: rotation debt is standing attack surface
- claim: Credentials recorded as compromised but not rotated remain the cheapest attack surface in the estate regardless of any hash gate above them; rotation receipts, not admission notes, close this class.
- quote: "haven't actually been rotated despite rotation being"
- source: watch/inbox/hermes_burn/T1W1_stranger_boot_path.md
- steal (one sitting): grep configs/keys.json and .env for the two named keys (Discord token, xAI key), rotate both, file the rotation receipts in watch/inbox.
- falsifier: a rotation receipt dated after the compromise admission. Absent that receipt the law stands.
- leverage: high

---

## TICKETS

EASY means one sitting; CLIMB means design work first.

1. EASY - mag/hermes_warm_boot.py:41 - hardcoded Vercel deployment URL ("https://vercel-deploy-7jx41m3r3-mag-d961.vercel.app/public/soul_frontier.html", team slug mag-d961 baked into source). Move it into the vercel-deploy registry or an env override; keep slugs out of tracked source.
2. EASY - mag/hermes_warm_boot.py:184 - _session_brief reports "updated": _now() for the FROZEN brief. Report BRIEF.stat().st_mtime instead (see law L4).
3. EASY - memories/session/next-window-handoff.md:22 and :433 - two identically titled "## STATE (update this section only)" headers (verified: grep -c "update this section only" returns 2). Rename the archived lower one (e.g. STATE (ARCHIVED)) so the single authoritative edit target is unambiguous.
4. EASY - tools/chain_repair.py:87 - TIP.write_text writes the tip non-atomically while the chain three lines above gets tmp+replace (:84-85). Give the tip the same tmp.replace pattern.
5. CLIMB - tools/chain_repair.py:39-46 and :63,:70 - find_bad_tail_index returns the first mismatch walking from the head; repair then writes the full-chain root into that row. Restrict repair to the last hashed row, write the prefix root at that index, and refuse (exit 2) on interior mismatches. Needs a decision on what interior mismatches mean (tamper alarm, not repair).
6. CLIMB - tools/tip_witness.py:109-119 - compare() has no prefix check (law L1). Add the prefix-root recompute and WITNESS-REWRITTEN verdict plus the gist-revision monotonicity walk (law L8). CLIMB not EASY because v1 amends legitimately rewrite interior rows: without the v2 chain mode (live chain is v1 today: tail rows carry chain_mode None) or an append-only amend log, the honest signal fires on every amend older than the last witness. Land with the amend-era plan.
7. EASY - mag/verkle_knot.py:614-632 - _verify_chain_consistent: a missing or JSON-corrupt tip passes (the except at :630-631 swallows OSError and JSONDecodeError and passes). Make a corrupt or missing tip on a non-empty chain fail the gate: recompute the expected tip from the tail and compare.
8. EASY - mag/verkle_knot.py:423 and :790 - two unlink sites: consolidate unlinks old knot files inside the loop before the conflicts refusal at :427-434 (a refusing repair may already have deleted files), and the v1 amend path unlinks the old knot before the chain rewrite (crash between leaves the chain pointing at a deleted file and destroys the pre-amend leaf). Move to an attic directory instead of unlink, and in consolidate defer unlinks until after the conflicts check passes.
9. EASY - mag/verkle_knot.py:485 (_rewrite_chain) - chain rewrite is a direct write; switch to temp file plus os.replace so a crash mid-amend cannot truncate history. The audit's fuller ask (pre-rewrite snapshots per era, append-only amend log) is the CLIMB part and rides with ticket 6.
10. CLIMB - mag/verkle_knot.py:171 - os.kill(owner, 0) stale-lock probe. On Windows 0 is CTRL_C_EVENT (verified on this host: signal.CTRL_C_EVENT prints 0), so the probe either sends a real Ctrl+C to a same-console holder or fails WinError 87, which the SystemError branch (:174-177) treats as stale and unlinks a possibly live holder's lock. Replace with psutil.pid_exists or a ctypes OpenProcess probe and fail closed on probe error. CLIMB because the current WinError-87-as-stale behavior is documented as deliberate in the comment; changing it needs a policy decision plus a real crash-case test (see TO-VERIFY V1: the audit's TerminateProcess mechanism for signal 0 is contradicted; the false-stale unlink risk is real).
11. EASY - mag/grounding_wave.py:233 and :244 - G2 binding uses sha256 hexdigest()[:12], a 48-bit truncation. Widen new bindings to the full digest; keep [:12] on the read side for legacy rows.
12. EASY - mag/verkle_knot.py:534 (VerkleProof.verify) - the audit says the proof does not bind n or an index range, so a proof against a duplicated position can pass unnoticed. Pass expected n (leaf count) into verify and check it.
13. CLIMB - server/server.py:350-351 and :655 - op "action" dispatches to _admit_action(msg) with no peer binding (law L6). Bind sid to connection at hello and reject actions whose sid the connection does not own. CLIMB because realmd/mobile clients may rely on bearer sids; coordinate the migration and consider defaulting require_frame_mac=True once SRP6 is the standing door.
14. CLIMB - scripts/index_fold_host.mjs plus writer plumbing - session-scope writer ids (the audit cites the estate's own seq 42 note: two concurrent sessions share one writer id) and add per-event tamper evidence (prev_hash) so reorder, edit and replay become detectable. Schema change: coordinate configs/events_key_schema.json and the B2-40 seq scheme.

---

## TO-VERIFY

Each row: the audit claim, why it smells, the exact command that checks it against bytes, and status where this distillation already ran it.

- V1. CONTRADICTED - "on Windows, os.kill with signal 0 actually calls TerminateProcess rather than just checking liveness". CPython routes os.kill(pid, 0) on Windows through GenerateConsoleCtrlEvent (CTRL_C_EVENT is 0), not TerminateProcess; TerminateProcess is the fallback for other signal values. The estate's own comment at mag/verkle_knot.py:174-177 documents the observed WinError 87 behavior, which is the GenerateConsoleCtrlEvent failure path. The audit's conclusion (a false-stale unlink is possible on Windows) survives via that path, but the named mechanism is wrong. Commands: `./.venv/Scripts/python.exe -c "import signal; print(signal.CTRL_C_EVENT)"` (ran: prints 0) and `grep -n "SystemError" -B 4 mag/verkle_knot.py` (ran: shows the deliberate WinError 87 branch).
- V2. RESOLVED TRUE - the audit self-flagged "checking grounding_wave.py shows it has no reference to verkle at all" as UNVERIFIED. Command: `grep -ci verkle mag/grounding_wave.py` (ran: 0 hits; grounding wave runs its own ledger, watch/GROUNDING_WAVE.jsonl at mag/grounding_wave.py:89).
- V3. RESOLVED TRUE - "The log also isn't tamper-evident since there's no prev_hash chain". Command: `grep -c prev_hash scripts/index_fold_host.mjs` (ran: 0 hits).
- V4. RESOLVED TRUE - the leaf counts the audit wavered on (2,821 of 8,626 / 9,873 lines / 5,874 leaves) are indeed unreliable: none matches the live tree. Command: `./.venv/Scripts/python.exe -c "import json; rows=[json.loads(l) for l in open('memory/biography/verkle_chain.jsonl',encoding='utf-8') if l.strip()]; print(len(rows), rows[-1].get('n_leaves'))"` (ran at distillation: 8777 rows, last row n_leaves 8777).
- V5. RESOLVED TRUE - "v2 chain mode isn't actually live yet". Command: `./.venv/Scripts/python.exe -c "import json; rows=[json.loads(l) for l in open('memory/biography/verkle_chain.jsonl',encoding='utf-8')]; print({r.get('chain_mode') for r in rows[-5:]})"` (ran: {None}, v1 default).
- V6. OPEN - "The compiled laws file only checks staleness against its own compile_report timestamp" (an attacker just sets it to now). Command: `grep -n "compile_report" mag/context_pack.py`.
- V7. OPEN - "CURRENT_OBJECTIVE.md gets carried into every reply across every mode with no integrity check". Consumer found at mag/context_pack.py:1157 (memory/boot/CURRENT_OBJECTIVE.md). Command: `grep -n "CURRENT_OBJECTIVE" mag/context_pack.py` then check which pack modes include the block.
- V8. OPEN - rib doctrine files "included by filename sort order", so "anything named to sort first, like" a 000_ prefix slips in automatically. Command: `grep -n "rib" mag/context_pack.py | head -20` (find the include loop and check for sorted() over memory/rib).
- V9. OPEN - "there's no actual drill receipt in the evidence" (the verkle restore drill). Command: `grep -rli "restore" watch/inbox --include="*.md" | head` plus `ls tools/verkle_restore_prep.py`.
- V10. OPEN - "nonce gaps already flood fold_warnings with noise". Command: `./.venv/Scripts/python.exe -m mag.shared_surface validate` and count fold warnings.
- V11. OPEN - "classification is just free text chosen by the writer" with inconsistent casing (RECEIPT / FACT / LAW / DOCTRINE). Command: `./.venv/Scripts/python.exe -c "import json,collections; idx=json.load(open('watch/inbox/INDEX.json',encoding='utf-8')); print(collections.Counter(str(i.get('classification','')).strip() for i in idx['items']))"`.
- V12. OPEN - "a backup copy of an API key file that still exists" and token storage in %LOCALAPPDATA% and %TEMP%. Command: `ls -la .env* 2>/dev/null` plus `git status --porcelain --ignored | grep -iE "env|key|bak" | head`.
- V13. OPEN - "an unexplained outside actor killing stealth driver processes roughly every ten minutes and deleting a fuel state log, with no tamper alarm covering that state". Command: `grep -rn "fuel" --include="*.py" mag/ tools/ | head` to locate the fuel log path, then inspect its recent lines and any watcher.
- V14. OPEN - 'That's indistinguishable from the drift-patrol-cron's routine "hash refresh" behavior' (a re-register launders an overwrite). Smells conflated: census drift patrol may never write index events at all. Command: `grep -n "register\|sha" tools/census_drift_patrol.py | head`.
- V15. OPEN - "sids aren't bound to connections": how sids are minted or leaked was declared not in evidence by the audit itself. Command: `grep -n "def _on_hello\|new_session_id\|sid" server/server.py | head -20`, then read _on_hello to see whether hello mints or accepts caller-chosen sids.
- V16. OPEN - the docstring-contract question the shared-surface audit raised but never closed: whether the contract read_first path matches the real file. Resolved here as NO discrepancy: watch/inbox/SHARED_SURFACE_CONTRACT.json:9 reads "read_first": "/board/inbox/INDEX.json" and watch/inbox/INDEX.json exists byte-real (an INDEX.md also exists; its role is unexplained). Command: `grep -n "read_first" watch/inbox/SHARED_SURFACE_CONTRACT.json && ls watch/inbox/ | grep -i "^INDEX"`.

Footer: quotes carried byte-verification receipts in-session (fixed-string sweep, 2026-10-01); misses were dropped, never reworded. No em-dashes in this file.

---

## BUILD REPORT (2026-10-01, build lane, ~20:35Z)

EASY tickets executed one at a time, highest leverage first. Every fix was
probed with a direct run before being claimed; pinned suites follow. No git
commits (coordinator commits). No em-dashes added to any touched file.

### EASY rows

1. PROMOTED-TO-CLIMB - mag/hermes_warm_boot.py:41 hardcoded Vercel URL.
   Reason: the slug now lives in tracked configs/deployments.json AND in four
   AH5 tests landed 2026-09-30 that pin it as the required default fallback
   (tests/test_ah5_warmboot.py:27,60-66,101-106,111-115,118-124, with the
   AH5 comment at mag/hermes_warm_boot.py:37-39 naming the "break nothing"
   default as deliberate). Removing it reverses a one-day-old, receipted,
   test-pinned decision and "slugs out of tracked source" additionally
   requires gutting the tracked config the ticket did not name. Needs a
   policy call: empty default vs untracked local registry, plus AH5 test and
   spec rewrites.
2. LANDED - mag/hermes_warm_boot.py:190 session_brief.updated now reports
   BRIEF.stat().st_mtime in UTC ISO (law L4). Evidence: the frozen repo brief
   (FROZEN 2026-09-26) now reports updated=2026-09-26T18:01:29Z instead of
   read time; tests/test_t1w1_ractor_fixes.py::test_session_brief_reports_mtime_not_read_time
   pins it deterministically via os.utime. AH5 suite 16/16 green.
3. LANDED - memories/session/next-window-handoff.md:433 lower duplicate
   header renamed to "## STATE (ARCHIVED)" with a receipt comment; marker
   grep count went 2 -> 1 (verified). No python tooling parses the marker
   string (checked: only the file path is referenced, mag/clippy.py:53,83).
4. LANDED - tools/chain_repair.py:92 tip write rides _write_tip_atomic (same
   tmp+os.replace contract the chain gets three lines up). Evidence: probe on
   a synthetic poisoned-tail chain: repair rc=0, exactly 1 atomic tip write
   (spy), post-verify green, no tmp residue; tests/test_t1w1_ractor_fixes.py::
   test_chain_repair_tip_rides_atomic_writer; the dry-return contract test
   tests/test_mcp_bridge_r1.py 2/2 green.
7. LANDED - mag/verkle_knot.py:684 _verify_chain_consistent now recomputes
   the expected tip from the tail and compares: root and n_leaves must match
   exactly, last_leaf_hash checked when present; corrupt, absent and
   empty-JSON tips over a non-empty chain fail closed (the old except passed
   them all). Fail-closed is safe: repair_tip_if_consistent (verkle_audit
   --auto-heal) heals, and the probe shows append-refusal then heal then
   append-success. Live estate stayed green before and after (verified at
   8778 and 8790 leaves). Pinned: tests/test_t1w1_ractor_fixes.py (4 gate
   tests). AG5+AH19+compaction+audit suites 42/42 green; compaction fixture
   writes root+n_leaves only, last_leaf_hash stays check-when-present by
   design for legacy tips.
8. LANDED - mag/verkle_knot.py:389-421 _attic_dir/_retire_knot (attic is a
   KNOTS sibling, never inside: every scanner globs KNOTS directly);
   consolidate collects to_retire and executes only after the conflicts
   refusal (:443,:468); v1 amend retires instead of unlinking (:883). The
   pre-amend leaf now survives a mid-amend crash. Pinned:
   tests/test_t1w1_ractor_fixes.py (3 attic tests: amend-retire, refusal-
   retires-nothing, success-retires-superseded).
9. LANDED - mag/verkle_knot.py:555-559 _rewrite_chain writes tmp + os.replace
   (bytes, LF-only law preserved). A crash mid-amend can no longer truncate
   history. Pinned: tests/test_t1w1_ractor_fixes.py::
   test_rewrite_chain_atomic_no_residue_lf_only.
11. LANDED - mag/grounding_wave.py:225,250,762 G2 bindings widen to the full
    sha256 (field name src_sha256_12 unchanged: the row schema pins the
    key); read sides (_src_ok, _evidence_mutated) accept legacy 12 and full
    64. Pinned: tests/test_t1w1_ractor_fixes.py (binding width + legacy
    acceptance + mutation flag) and the updated
    tests/test_grounding_wave_v4.py::test_evidence_mutation_detected_identity_not_existence.
12. LANDED - mag/verkle_knot.py:584,670 VerkleProof.verify takes n_leaves and
    refuses index >= n and cross-band path depth; prove() passes it. Honest
    limit named in the test: a same-band count with the same root cannot be
    distinguished inside the proof (duplicate-last padding, CVE-2012-2459
    class); that residual is closed by the tip binding root AND count as a
    pair, which ticket 7's gate now enforces. Pinned:
    tests/test_t1w1_ractor_fixes.py::test_proof_verify_binds_leaf_count.

CLIMB tickets 5, 6, 10, 13, 14 untouched, as ordered.

### CARRIER-PATCH rows (priority insert, same day ~20:25Z)

Driver is STOPPED throughout; memory/runs/hermes_burn/DRIVER_STOP left in
place. Byte root causes found before writing any fix:

- The A1 bleed mechanism is a stale force flag:
  memory/plans/hermes_burn_batch1/A1_steer_antiforgery/ask.json carries
  force=true (mtime 09:18, never cleaned), which bypassed the old
  exists-skip at every 45s cycle of scripts/descent_driver.sh. The
  "flag hygiene" fix only cured NEW staging (refire dirs 14:14 carry
  force=false), never the standing flag.
- The duel/T1W2 evidence disease is a staging shape: the DUEL ask contracts
  carry ask_bank's NON-reveal draw metadata JSON (bank/draw_id/material_path/
  first_line, exactly tools/ask_bank.py cmd_draw without --reveal) with
  evidence: [], so the material was never attached anywhere.

C1. LANDED - LANDED BEATS FORCE: tools/hermes_burn.py:196-219 _landed_skip
    (+ entry call at :278). A fire is refused when the output file exists
    unless a revision rides turn2_only (the standing revision shape; a
    revision flag without turn2_only skipped at entry under the old gate
    too). force can no longer re-burn a landed deliverable. Every (re)fire
    enters through run_ask, so the entry check is the single choke point for
    both cycle-boundary retry triggers (empty content channel, provider
    refusal). Evidence: tests/test_carrier_patch_t1w1.py::
    test_landed_output_skips_even_with_force (force=true + landed out ->
    skip, zero _call) and the two revision-shape parity tests; live dry-run
    over memory/plans/hermes_burn_batch1 prints "A1_steer_antiforgery
    (skipped)" where the bleed used to fire.
C2. LANDED - REFUSED IS TERMINAL: tools/hermes_burn.py:166-193 _refusal_state/
    _mint_refused_marker, entry skip-on-sight with ledger backfill (:266-275),
    mint at the second banked refusal (:331). Evidence:
    tests/test_carrier_patch_t1w1.py::test_second_refusal_mints_marker_then_skip_on_sight
    (1st refusal banked no marker, 2nd banks and mints, 3rd run skips, _call
    count stays 2) and ::test_ledger_backfill_mints_marker_without_another_fire
    (42 pre-seeded refusal rows -> skip + marker, zero fires). Live heal:
    dry-runs minted REFUSED markers for DUEL1_hidden_5 (46 ledger refusals)
    and N1_parables_songmap (42), both carrying the real refusal snippet;
    both queues now print skipped.
C3. LANDED - EVIDENCE PREFLIGHT: tools/hermes_burn.py:220-259
    _assert_evidence_in_body, called before every _call (:308). Per the
    coordinator spec: every evidence[] path must exist on disk and its
    rendered head (first 400 chars, always inside the 400k render cap) must
    appear in the message body being sent; failure names the path and fires
    closed BEFORE any API call. Plus the E3 steal clause (DAY1_CROSS_RACTOR
    E3: "exit 2 on an evidence-less fire"): an empty evidence list fails
    closed with the remedy named, because the two named diseases (DUEL2 x14,
    T1W2 x4) both carried evidence: [] and a per-path check alone cannot
    catch them. Evidence: tests/test_carrier_patch_t1w1.py (missing path,
    unrendered material via render-loss stub, empty list, empty file, and
    the healthy-fire control with material bytes asserted inside the fired
    body).

Relaunch posture: RELAUNCH-SAFE with the standing tree (every existing ask
now skips, terminal-refuses, or would fail closed before any paid call), but
the driver stays stopped per order; DRIVER_STOP untouched. Known open items
outside this patch: the DG1 ask.json sits at the plan root so the driver
reports USAGE-ERROR (RIB_WARMTH footnote), and the ledger-total $0.53 delta
(X7) remains unnamed.

### Test evidence summary (moment ~20:30-20:35Z)

- tests/test_t1w1_ractor_fixes.py: 11 passed (new).
- tests/test_carrier_patch_t1w1.py: 10 passed (new).
- Pinned existing suites: AG5+AH19+compaction+verkle_audit 42/42; AH5
  warmboot 16/16; mcp_bridge chain contract 2/2; steer_seal +
  grounding_witness_binding + both new files together 49/49.
- Broad sweep (37 files importing the touched modules): 375 passed, 5
  failed. Of the 5: the 4 test_grounding_wave_v4.py ladder/view failures
  were bisected to HEAD bytes (they fail identically with my edits reverted;
  pre-existing on the moving tree, another lane has mag/context_compression.py
  dirty), and tests/test_context_pack_delivery.py::
  test_render_fits_budget_without_hard_clip[build] passed 6/6 in isolation
  immediately after (live-tree flake: the chain grew mid-sweep, 8778 to 8790
  leaves, while packs rendered off it).

---

## T1W2_S5 STORES

Source: watch/inbox/hermes_burn/T1W2_S5_stores.md (stranger audit of server/store_io.py, anthropic/claude-opus-5.5, landed 2026-10-01). Method as the T1W1 distillation: every quote below was byte-verified with a fixed-string sweep (grep -cF) against the audit file before use (18 candidates, 2 initial misses recut to shorter hitting substrings because the source backticks `/mnt/c`, `flock` and `msvcrt.locking`, 0 dropped; the source contains no em-dash). Every file:line pin was re-checked against live bytes: the audit's hand-count warning proved conservative, worst skew 1 line (its :119-123 deadline check is :119-124 live). Pins cite server/store_io.py unless another file is named. Caller census: server/auth.py:89, server/auth_srp6.py:489 and mag/game_world.py:87 are the only exclusive() users in the estate (mag/local_scheduler.py:374 run_exclusive and mag/party_subchain.py:112 _exclusive are unrelated same-name helpers); none nests two exclusive() scopes today, so S1 is latent, not firing. The only existing test is tests/test_users_store_concurrency.py (the Q21 concurrency probe), which does not cover re-entry.

### LAWS

### S1. an RLock in front of an always-taken OS lock is self-deadlock, not re-entrancy
- law: reentrancy depth gating
- claim: The RLock (factory :90-97, RLock at :95, taken at :113) admits the same thread, but every exclusive() entry opens its own handle (:114), and both fcntl.flock (per open file description) and msvcrt.locking (per handle) treat that second acquire as a foreign contender: POSIX blocks in the kernel on our own first handle (:60; grep -c LOCK_NB over the file is 0), Windows spins forever inside _lock_byte's internal retry (:45-50), and per S2 no timeout can fire. Nested `with exclusive(p): with exclusive(p):` hangs; two sequential blocks work (both confirmed live on win32, verdict P1).
- quote: "Re-entry self-deadlock (worst)."
- source: watch/inbox/hermes_burn/T1W2_S5_stores.md
- steal (one sitting): per-path reentrancy counter beside the RLock and take the OS lock only at depth 0 (the audit's own patch direction).
- falsifier: the audit's nested-exclusive test passing unmodified on both platforms (ran on win32: hangs, verdict P1; POSIX half still OPEN, W3).
- leverage: high

### S2. a deadline checked outside the loop that swallows the failure is dead code
- law: timeout must live inside the spin
- claim: The Windows _lock_byte eats OSError and loops internally (:45-50), so the except at :119-124 never runs; the POSIX twin blocks in the kernel (:60). The _LOCK_TIMEOUT_S = 30.0 (:67) TimeoutError is unreachable on both platforms, and the tlock acquire at :113 has no timeout at all, so a hung (not dead) holder stalls every waiter forever: in-process ones queued on the RLock, cross-process ones past any budget.
- quote: "The timeout is dead code on both platforms."
- source: watch/inbox/hermes_burn/T1W2_S5_stores.md
- steal (one sitting): make _lock_byte attempt-once-and-return (LK_NBLCK) and let exclusive() own the deadline loop; use LOCK_EX|LOCK_NB on POSIX; give tlock.acquire timeout=_LOCK_TIMEOUT_S.
- falsifier: a contended acquire raising TimeoutError inside the budget on either platform (probe P1 waited 35s on win32: no TimeoutError).
- leverage: high

### S3. per-path locks compose into deadlock without a canonical order
- law: lock ordering
- claim: Nothing orders distinct paths; exclusive(a) nested in exclusive(b) against a reverse-order caller deadlocks, and S2 means no timeout rescues it. Latent today: each of the three live callers holds exactly one exclusive() scope at a time (verified by reading the call sites).
- quote: "No lock ordering."
- source: watch/inbox/hermes_burn/T1W2_S5_stores.md
- steal (one sitting): one docstring line in exclusive() naming the rule: never nest two exclusive() scopes; if a future caller must, acquire in sorted resolved-path order.
- falsifier: reverse-order nested acquires from two threads both completing. Nothing guarantees that today; the impossibility is the law.
- leverage: medium

### S4. rename atomicity buys visibility, not durability
- law: visibility versus durability
- claim: mkstemp in the target directory (:141-142) plus os.replace (:151) gives all-or-nothing visibility on a local same-volume filesystem, with the retry at :148-156 absorbing Windows PermissionError from concurrently open handles (the module's own docstring at :134-137 names exactly this); with no directory fsync (documented trade, :27-28) power-loss ordering is not guaranteed, and the fsync at :147 covers only the temp file's data, not the directory entry.
- quote: "Durability after power loss, because there is no directory fsync"
- source: watch/inbox/hermes_burn/T1W2_S5_stores.md
- steal (one sitting): none needed for account files (documented, deliberate); if a store ever becomes load-bearing for crash recovery, add the dir fsync and cite this law.
- falsifier: a power-loss replay losing the old bytes after a successful replace return. Expected on some filesystems; that expectation is the law.
- leverage: low

### S5. a byte lock's scope ends at the OS boundary its API knows about
- law: cross-OS lock invisibility
- claim: The allowlist (:72-73) is repo-relative, so it inherits whatever filesystem the repo lives on; under WSL the repo is /mnt/c and flock from the Linux side cannot see msvcrt locks held from the Windows side, so cross-OS access to the same bytes is unserialized. Live exposure: AGENTS.md lists WSL /mnt/c as a first-class surface for this exact tree, and store targets include repo state/ files.
- quote: "still admits a repo that lives on NFS or on"
- source: watch/inbox/hermes_burn/T1W2_S5_stores.md
- steal (one sitting): docstring line naming the single-OS-writer rule for store files; the real fix is policy (ticket 4).
- falsifier: a flock on the WSL side blocking while a Windows holder keeps the byte lock. Expected to pass straight through (W4, OPEN).
- leverage: medium

### S6. lockless readers trade writer starvation for tear freedom
- law: reader-writer asymmetry on Windows
- claim: Readers take no lock by design ("Lockless readers never observe a half-written file", :17); any concurrently open handle can fail os.replace, the retry is bounded by _REPLACE_TIMEOUT_S = 5.0 (:68, :148-156), after which the write raises loudly: the computed mutation is lost with an exception, not silently. Live lockless reader: mag/game_world.py get_state() calls _load() outside any exclusive() while set_state() mutates under the lock.
- quote: "Readers take no lock"
- source: watch/inbox/hermes_burn/T1W2_S5_stores.md
- steal (one sitting): none; accepted design. If a 5s replace failure ever fires in production the remedy is retry-at-caller, not a reader lock.
- falsifier: a torn read observed by a lockless reader. Impossible under the replace contract; that impossibility is the law.
- leverage: low

### TICKETS

1. EASY - server/store_io.py:111-128 plus a test beside tests/test_users_store_concurrency.py - land the reentrancy fix: per-path depth counter beside _THREAD_LOCKS, OS lock only at depth 0, plus the audit's regression test (test_exclusive_reentry_does_not_hang, verbatim) which fails today (verdict P1). The POSIX twin needs a Linux seat before the ticket closes (this host is win32; W3).
2. EASY - server/store_io.py:45-50, :60, :113, :119-124 - make the deadline reachable: _lock_byte returns success instead of looping forever, exclusive() owns the retry loop (LK_NBLCK / LOCK_EX|LOCK_NB), tlock.acquire gets timeout=_LOCK_TIMEOUT_S. Probe after: a deliberately hung holder produces TimeoutError inside 30s instead of an infinite stall.
3. EASY - server/store_io.py:100-107 - exclusive() docstring: the never-nest rule plus the sorted-path escape hatch (law S3). One line; keeps the next caller from walking into S1/S3 blind.
4. CLIMB - cross-OS serialization policy for store files under WSL/NFS (law S5): single-OS-writer rule versus moving shared stores behind one owning surface. Touches the AGENTS.md WSL row contract; operator call, not a code sitting.
5. EASY - server/store_io.py:157-161 - crashed writers leave .tmp-* siblings (documented at :17-18; the cleanup at :157-161 only runs in-process): sweep stale same-prefix .tmp-* siblings (mtime older than 1h) on exclusive() entry at depth 0, riding ticket 1's counter so it runs once per critical section.

### TO-VERIFY

- P1. RAN (win32) - the audit's own falsifier: nested exclusive() self-deadlocks and the 30s timeout never fires. Command and verdict in the PROBE VERDICTS block below.
- P2. RAN (win32) - "A dead process loses its OS locks": kill a holder process, then re-acquire from the parent. Verdict below.
- W3. OPEN - POSIX half of S1/S2: the blocking LOCK_EX at :60 self-deadlocks the second acquire. Byte-verified (grep -c LOCK_NB = 0) but not runnable on this win32 host. Probe for a Linux seat: the same nested-exclusive snippet as P1 with a join guard.
- W4. OPEN - cross-OS lock invisibility (S5). Probe: hold exclusive() on a repo state file from Windows python, then from WSL run `flock -n /mnt/c/<repo>/<state>.lock -c true`; rc=0 while the Windows holder is armed proves no mutual exclusion. Needs both sides; no single seat can close it.
- W5. OPEN - "can outlast the 5 s budget": AV or indexer handles outlasting the replace retry is environment-dependent; no deterministic probe. Accepted risk while writes fail loudly (S6).
- W6. RESOLVED - the audit's hand-counted line numbers: every pin re-checked against live bytes, worst skew 1 line (:119-123 is :119-124). No claim relied on a wrong pin.
- W7. RESOLVED - the os.replace-on-NTFS verdict "visibility-atomic under conditions": both named conditions are byte-real (same-directory mkstemp :141-142; PermissionError retry :148-156 plus docstring :134-137), so the conditional verdict stands as written, with S4 carrying the durability caveat.

### T1W2_S5 PROBE VERDICTS (2026-10-01, win32 host, .venv python)

- P1. CONFIRMED - nested exclusive() self-deadlocks and the 30s timeout never fires. Probe: the audit's own falsifier run as a python -c one-liner; sequential control, then `with exclusive(p): with exclusive(p):` in a daemon thread with join(35) and a TimeoutError watcher. Output verbatim: SEQUENTIAL_OK, elapsed=35.0, REENTRY_HANGS, TIMEOUT_FIRED=False. Audit findings A and B are live-confirmed on win32 exactly as written; the falsifier did not fire. The daemon thread was still spinning inside _lock_byte's internal retry when the interpreter exited (daemon semantics, clean exit).
- P2. CONFIRMED (after discarding one bad probe) - "A dead process loses its OS locks". Probe: child python holds exclusive() and sleeps; parent kills it 1s in (TerminateProcess), then re-acquires in a daemon thread with join(8). Output: child_acquired=L, LOCK_RELEASED_AFTER_KILL. The first run of this probe printed a false LOCK_STUCK_AFTER_KILL caused by a NameError inside the probe itself (the parent had not imported exclusive, so the re-acquire thread died instead of testing); that run was discarded, never banked, and the rerun above is clean. Audit finding D part 1 stands: a dead holder releases; only a hung alive holder is forever, per S2's dead timeout.

