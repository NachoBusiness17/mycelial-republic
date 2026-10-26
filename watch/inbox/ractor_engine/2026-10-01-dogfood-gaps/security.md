# SECURITY LENS - the GAP_REGISTER under the lethal-trifecta frame

Ractor: ractor_engine, lens: security (threat-model auditor). Topic:
`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`. Frame: private data +
untrusted content + communication. Every check below was executed this
sitting, 2026-10-01 ~22:50-23:20 EDT. Laws held: no fabrication (unverified
items marked OWED), no em-dashes, path:line citations, win32 subprocesses
run through the Bash tool only.

## Verdict in one line

The register's security rows are mostly STILL REAL and byte-confirmed, but
the register itself is the sharpest unmodeled attack surface in the estate:
an unverified-adoption, directive-bearing, already-decayed instruction bus
with no liveness contract, while the scheduled tasks it fixes remain an
unpinned persistence primitive it never models.

## F1. The steer_seal gate's DEFAULT state and the hermes steering surface
are unarmed - the drill suite already exists; only the flip is missing
(CORRECTED after hostile second pass; scope narrowed, move replaced)

- `mag/steer_seal.py:84-102`: mode resolution is "explicit arg > env
  MAG_STEER_SEAL_MODE > sentinel > warn", and line 102 is a bare
  `return "warn"` - warn is the default state.
- `ls -la ~/.mag/` this sitting: the directory contains ONLY
  `steer_seal_seen/`. No keyfile, no `steer_seal_mode` sentinel.
- `MAG_STEER_SEAL_MODE` is referenced only inside `mag/steer_seal.py`
  (:15, :84, :90) and its test (`tests/test_steer_seal.py:46,233`): no
  script, task, or launcher sets it. The warn default is the deployed
  state.
- The unarmed SURFACE is the hermes steering path:
  `mag/hermes_steering.py:270` calls `steer_seal.admit_text(args.nudge)`
  with no mode arg - an unsealed permit word (including a fullwidth
  "\uff27\uff2f" GO, which `classify` leaves a permit: see the NFKC
  decision at `tests/test_steer_seal.py:172-186`, "deliberately not
  applied anywhere") passes with a logged warning on the live channel.
- CORRECTION (second pass accepted): "every steer permit on this host" was
  overbroad. `tools/field_experiment.py:515-524` mints its own keyfile
  (`ss.write_keyfile(keyfile, key, force=True)`) and admits with
  `mode="enforce"`, returning None fail-closed on any non-operator-seal
  authority. That lane is ARMED and excluded from this finding.
- CORRECTION: the forge-drill move is withdrawn as redundant.
  `tests/test_steer_seal.py` (10,990 bytes, mtime Oct 1 14:33) already
  drills forged MAC (:66), replayed nonce (:85), missing-keyfile fails
  closed in enforce (:146-148), restrictive-words-pass/keyfile-absent
  (:160-168), the Cyrillic-lookalike NFC edge (:172-186), and the enforce
  flip via env (:233). The gate's logic is tested; the DEPLOYMENT is not.
- Register cross-ref: GAP_REGISTER.md:78 (rank 5) - confirmed accurate.
- Falsifier (tightened): `~/.mag` gains a keyfile + `steer_seal_mode`
  sentinel (or the steering launcher exports MAG_STEER_SEAL_MODE=enforce)
  AND a live receipt shows `permit_refused_enforce` on the hermes path
  (the log event `tests/test_steer_seal.py` already asserts). Absent both,
  the finding stands.
- One-sitting move: the OPERATOR flip is the whole remaining gap -
  `.venv\Scripts\python.exe -m mag.steer_seal write-keyfile` (per
  `mag/steer_seal.py:125` write_keyfile) plus one sentinel/env line in
  whatever launches cmd_steer, then one forged-word probe on the live
  channel to bank the refusal receipt. ~10 minutes, operator-gated because
  it changes refusal behavior of the live steering channel.

## F2. verify_seal is PAM-forgable by construction; the Ed25519 port is
still unlanded; the SS-1 ticket was still never minted (STILL REAL)

- `tools/seed_v2.py:776-792`: the generated `verify_seal.py` resolves
  `root = Path(__file__).resolve().parent` (line 780) and checks sha256 of
  each file against `MANIFEST.sha256` read from that same directory (line
  782). Verifier, manifest, and payload share one writable trust domain:
  rewrite the file and its manifest row and verification passes. This is
  the PAM forgery class, confirmed by my own read of the generator source,
  not inherited from the lane's claim.
- `find . -name "*.seal" -not -path "./.git/*"` over the repo this sitting:
  zero hits. No .seal sidecars exist anywhere.
- `mag/seed_seal.py` is ABSENT (checked by ls). The port spec exists:
  `watch/inbox/localfirst/pam.md:65` ("The estate port: Ed25519-signed
  arc-seed export (the seed-seal slot)") and `:89` ("fail closed to
  UNVERIFIED"); `pam.check.txt` is on disk at
  `watch/inbox/gala_20260925/localfirst-steal/lanes/pam.check.txt` (3,226
  bytes). Note: my first three path guesses for pam.md were wrong; the
  register's anchor is real, it resolves at watch/inbox/localfirst/pam.md.
- `grep -cE "SS-1|CP-1|R2-1" watch/inbox/hermes_burn/TICKET_LEDGER.md` = 0.
  The file exists; the three named tickets do not. Rank 11 confirmed live.
- Falsifier: .seal sidecars plus a verify-at-consume path that fails closed
  on a missing/invalid signature, and a TICKET_LEDGER row for SS-1.
- One-sitting move: the red demonstration first - a test that writes a
  package file, rewrites its MANIFEST.sha256 row, asserts verify_seal exits
  0, and fails the suite with "forgery accepted". Proving the hole is the
  prerequisite the port spec assumes; 15 minutes.

## F3. The register itself is the injection surface, and it already decayed
within 15 minutes of landing (REGISTER MISSED THIS ABOUT ITSELF)

- The trifecta is assembled in one artifact. Private data: the register
  carries estate state, paths, costs, owners. Untrusted content:
  GAP_REGISTER.md:20-22 admits only 5 load-bearing quotes were
  byte-checked and "everything else in the table is adopted as
  lane-reported". Communication: GAP_REGISTER.md:5-6 makes it the lane
  table that "tells that job what to fire, in what order, at what cost, and
  who owns it" - directive reach into future autonomous seats, including
  external fetch instructions (fill 10: pullpush/arctic-shift; fill 9:
  fxtwitter). A fabricated or poisoned row in any lane file is promoted,
  with no byte check, into standing orders for the next burn.
- The decay is not hypothetical. File mtimes this sitting (stat, EDT):
  GAP_REGISTER.md written 18:41:58; lanes
  `memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/`:
  a14-coverage.json 18:48:13, a09-balls.json 18:49:19, a10-drops.json
  18:53:47, a12-commits.json 18:54:58. The register's poll claim
  (GAP_REGISTER.md:13-15, "Lanes a09-a14 produced NO files") was true at
  its moment and false seven minutes later. All of a09-a14 now exist on
  disk (ls of the lanes dir: a09-balls, a10-drops, a11-build-queue,
  a12-commits, a13-cadence, a14-coverage, plus a15-rollup). The register's
  own amendment law (GAP_REGISTER.md:15-16, "if a09-a14 land later, they
  amend this register, they do not rewrite it") has no enforcer: no tool
  watches the lanes dir, and the amendment has not happened. The register
  presents as the complete lane table at 8/15 coverage.
- The unmerged lanes carry security-relevant loads: a09-balls.json's first
  row refutes the 10-01 OLM commit headline (2093ca518) as an OVERCLAIM
  against `tools/abliterate_p1_probe.py` - a phantom-citation class instance
  riding a commit message, the estate's most-consumed record genre.
  a12-commits.json audited object retention (3 seeded hashes resolvable
  only in Mag-backup.git; 21,136 unreachable objects). OWED: I read only
  ~700 bytes of each; the full a09-a14 gap sets are not merged or verified
  by me.
- Falsifier: an amended register carrying a09-a14 rows, or a lanes-dir
  watcher that files the amendment receipt on landing.
- One-sitting move: execute the register's own amendment law (merge
  a09-a14 rows, mark the rank-1-style stale rows), and - the structural
  fix - give the future `tools/citation_lint.py` (rank 3) a second mode
  that validates every GAP row's anchor before the next job fires on it.

## F4. The scheduler is an unpinned persistence primitive, and no register
row models it (THE CLASS THE REGISTER MISSED)

- `schtasks /Query /TN EstateWalkDaily /V`: Task To Run is
  `powershell -NoProfile -ExecutionPolicy Bypass -File
  C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\estate_walk_daily.ps1`.
  `Estate Ratchet` runs the same shape on `scripts\ratchet_daily.ps1`;
  `Estate KeyAudit` runs the repo venv python on `mag.key_law`. The repo
  working tree is writable by every seat and lane (git status at session
  start shows ~60 modified files across organs). ExecutionPolicy Bypass
  defeats script policy; cadence is daily under the operator's context;
  no hash pin, seal, or self-check stands between the scheduler and the
  payload file. Any lane content that can write a repo file can
  alter-or-acquire operator-context scheduled execution. The 10-01
  EstateWalkDaily incident proves the class is live in practice: the
  scheduler executed a repo file whose contents had a fatal defect, and
  only luck (a build script, not a payload) decided the blast radius.
- OWED: I verified 3 of the ~10 Estate* task command lines, not the full
  inventory; the finding is proven for the shape, the census is not done.
- Falsifier: task actions pointing at integrity-checked copies outside the
  writable tree, or scripts that self-verify against hashes stored
  out-of-band (this is exactly the seed_seal slot of F2 - one port closes
  both).
- One-sitting move: pin the highest-value task (Estate Ratchet: it gates
  pushes) to a sealed copy, or add a self-hash assert to ratchet_daily.ps1
  against a digest stored outside the repo. ~30 minutes.

## F5. Dogfood: register rank 1 is fixed in bytes, but its alarm channel
still cannot see its own non-start (MISRANKED AS OPEN, PARTIALLY CLOSED)

- Fixed: `scripts/estate_walk_daily.ps1:11` is an absolute
  `$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"`,
  PATH LAW comment at lines 5-10 naming the System32-CWD cause; commit
  5d2263f10 carries the receipt; the smoke proof ran
  (`logs/estate_walk_daily.log` ends with
  "END 2026-10-02T00:37:54Z exit=0"). The register's rank-1 line "repeats
  10-02 09:15 with the same relative-path defect" is STALE.
- schtasks this sitting: Last Result still 1 (the pre-fix 10-01 fire),
  Status Ready, Next Run 10/2/2026 9:15 - the fix is pending its live
  proof fire. Correct state, but the register should say so.
- The residual wound: the alarm channel lives INSIDE the script
  (`estate_walk_daily.ps1:19-21` writes memory/attention.md only if
  powershell started the script). Any failure before script parse - repo
  moved, drive letter changed, script deleted, venv python missing -
  reproduces red-AND-silent exactly: LastTaskResult=1 with both channels
  dark, the third failure shape a08 named (GAP_REGISTER.md:223-224), which
  is a property of the SCHEDULER, unfixable by any in-script path law.
  Nothing watches LastTaskResult. And the fill-1 requirement "prove BOTH
  channels fire on an injected failure" was NOT executed: full-tree grep
  this sitting finds `ESTATE-WALK-BAKE-FAILED` only in the a08 lane files
  (a08-48h-synth.json:27 and its checks.json) and the original
  script-writing trajectory step (memory/trajectory/steps.jsonl:36579,
  which shows the OLD relative-path `$log = "logs/estate_walk_daily.log"`);
  memory/attention.md has zero hits, and the smoke run was success-path
  only (END exit=0 in logs/estate_walk_daily.log). The alarm branch of the
  repaired script has never fired, in a drill or in anger.
- Falsifier: a scheduler-level watcher that reads EstateWalkDaily's
  LastTaskResult after 09:15 and alarms on non-zero, or an
  injected-failure drill receipt showing both channels firing.
- One-sitting move: a 10-line watcher (second scheduled task or a block in
  an existing daily) comparing LastTaskResult to a receipt stamp at
  ~09:20. Closes the self-test bootstrap hole the register itself suffers
  from in F3.

## Meta-gap verdict under the lens

The register ranks MINED-NEVER-SCHEDULED as the dominant class
(GAP_REGISTER.md:44-49); my bytes agree it is the widest (TICKET_LEDGER 0
SS-1/CP-1/R2-1 rows, percolator.py 0 "candidates" occurrences, seed_seal
and citation_lint absent, and rank 4's ERRATA fill not started:
`watch/inbox/48h_synth/ERRATA.md` does not exist and STORY.md:240 still
carries the 191.8M phantom whose named source has zero "191" hits, my
grep this sitting; the a08 checks.json deep pass independently confirmed
the same zero-hit result at 2026-10-01T23:09Z). But the class that
dominates SECURITY-wise is its own meta-gap 4, GATES LIVE BUT UNARMED
(GAP_REGISTER.md:63-68): confirmed still open 3-of-4 (steer_seal warn,
verify_seal hash-only, no seed_seal; EstateWalkDaily fixed). What the
register missed entirely: (1) register-decay-unwatched - consumed
directive records with no liveness contract (F3); (2) scheduler-integrity
- unpinned persistence primitives (F4). Both are the same disease the
estate names elsewhere: an enforcement surface that trusts its own
writable domain.

## Blind spots (honest)

- I read ~700 bytes of each of 3 of the 6 unmerged lanes; their full gap
  sets are unmerged and unverified by me.
- I audited the PAM forgery by reading the generator source; I did not
  execute a forgery. The hole is proven by construction, not by exploit.
- I verified 3 of ~10 Estate* task command lines; the persistence
  inventory is not enumerated.
- The fill-1 injected-failure drill: grep-closed this sitting - the alarm
  branch of the repaired script has never fired anywhere (only the a08
  lanes and the old trajectory step carry the ESTATE-WALK-BAKE-FAILED
  string); what I cannot see is whether any drill receipt landed outside
  the paths I grepped (memory/, watch/, logs/).
- I did not verify the register's rank 2 (elder lens), rank 7/8 (index
  state), rank 9/10 (KVarN, trio), rank 12 (Move 1) - out of lens scope,
  left to the accuracy and operations lenses.
