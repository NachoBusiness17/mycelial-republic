# SPORE SHARING - SECURITY LENS (2026-10-05, lens-security)

Frame: the lethal trifecta (private data + untrusted content + communication) over the
spore question (push the estate to github.com/NachoBusiness17/mycelial-republic so a
second operator can regrow it with dormant subsystems). Jacket: the gate that tests
itself and nothing else. Every check below was run in this sitting unless marked OWED.

## TL;DR

The spore cannot ship as a git push of this clone. HEAD's own tree carries seven tracked
biography tars (one holds a live-shaped xai- credential per the estate's own history
audit), the lan.key private-key blob is reachable from HEAD's history, 20 zknot session
files carrying the operator's prompts are tracked, and the public remote is already wired
to this repo. The estate's secret defenses are three permissive layers: the daily gate
scanned 13 changed files at a 10MB cap today, a history mode exists but is unwired, and
the push-time credential gate printed six unaccepted fingerprints at the exact public
push and stood down WARN-ONLY. Meanwhile the .env model everyone fears is the one clean
surface. The regrow side re-arms persistence and spend as a documented boot step
("fire the crons", state/GENOME.md:74) and loads PR-writable law files at boot with no
integrity check found.

## F1 (CRITICAL, CONVERGENT with LANE4C): a git push of this clone publishes the estate's private layer

EVIDENCE (all run this sitting):
- `git remote -v` → `github https://github.com/NachoBusiness17/mycelial-republic.git`
  (fetch+push) is wired on this clone, plus sibling `local .../Mag-backup.git`.
- `git ls-tree HEAD attic/20260923_biography_rotation/biography_backup_20260825.tar`
  → blob 6fb541750f9fa9f476a2e95d31c0987a31504c52, committed in HEAD's tree; the seven
  tracked tars total ~562MB on disk (`ls -la attic/20260923_biography_rotation/`).
- LANE4C receipt `watch/inbox/audit_20260926/LANE4C_HISTORY_SECRETS.md`: line 5 (two
  history-only XAI-KEY HIGH findings, same credential, reachable from 19 commits,
  2026-08-01..2026-09-14), line 42 ("the same live-shaped key is still inside a tracked
  tar in the current tree", fingerprint fp_2fc97957ab09), line 49 (memory/tls/lan.key,
  PRIVATE-KEY-BLOCK critical, present in 318 commit trees, HEAD included at audit time),
  line 6 ("Nothing was fixed, rotated, purged, or rewritten").
- `git merge-base --is-ancestor 799ddb6feaad HEAD` → rc=0: the lan.key introduction
  commit rides any push of HEAD. (`git cat-file -e cd2f8e6a520d` rc=0: the history-only
  secret root commit exists locally on other refs, e.g. refs/remotes/local/.)
- `git ls-files memory/zknot` → 19 dated session knots + LATEST.md tracked; AGENTS.md:5
  says LATEST.md carries "his prompts". The operator's prompt history is in the pack.
- `git push --dry-run github HEAD:master` → local gates ran, then
  `! [rejected] HEAD -> master (non-fast-forward)`; the unrelated 13-commit scaffold on
  the public side (merge-base rc=1, `git log --oneline github/master` tip dc6649943) is
  currently the only thing that makes the naive push fail. `--force` or a re-clone push
  removes even that.
- Blast radius check on the public side today: `git ls-tree -r --name-only github/master
  | grep -icE "\.env$|\.key$|xai-|credential|secret"` → 0. Nothing has leaked YET.

FALSIFIER: a full-blob history re-scan (gate history mode or gitleaks over
`rev-list --objects --all`) that returns zero reachable credential blobs from any ref
would kill this; so would proof that attic/, memory/zknot, and the lan.key blob are
purged from history before any push. LANE4C itself is refutable by re-extraction of the
tar (deliberately not repeated here: no secret bodies printed, per LANE4C:108).

MOVE (one sitting, ~60 min): first command today, `git remote remove github` on this
clone (1 min, closes the footgun while the recipe is designed); then define the spore as
a fresh-root export (`git archive` of a prune list, or a new init + tracked-copy) with a
DIRECTORY-CLASS denylist: attic/, memory/ (except the whitelisted seed set),
memory/zknot/, watch/inbox raw scrapes, any tar/zip/archive blob (55 min).

## F2 (the jacket): the secret gate is three permissive layers, each blind in a documented way

EVIDENCE:
- Daily layer: `watch/inbox/secret_gate_results/changed_20261005T075617Z.json` →
  `"mode": "changed"`, `"scope_basis": "worktree+untracked"`, census 18 files seen /
  13 scanned / 5 large_skipped, `"max_file_bytes": 10485760`, rule_counts {} ,
  blocking_count 0. The known dirty artifacts are structurally invisible to it: the tar
  is 189,808,640 bytes (19x over the cap) and binary; history blobs are not in the
  changed window.
- Capability layer: `tools/secret_gate.py:119-120` defines `--history` ("scan every
  ADDED line across git history") and `:183` even says "rotate anything live BEFORE
  stripping history", but no scheduled path runs it; the only result receipt on disk
  from today is the changed-mode one.
- Push layer: `git push --dry-run github HEAD:master` printed six credential
  fingerprints (d2c6c6159157b588, 40e65f6f759579a0, d490fb12f0b36db9, c990171ad3a64390,
  782dd42793948b98, aaf6377cce055a1a) and then, verbatim, "the push is NOT blocked
  (WARN-ONLY)". The baseline `configs/prepush_credential_baseline.json` does not exist
  (`ls` rc=1), so all six are unaccepted findings sitting in the push channel.
- Design admission: `tools/prepush_credential_shape.py:23-26` scopes the push scan to
  "changed/staged content only ... a full-tree scan in pre-push is a gate nobody keeps";
  `:41-43` fixes WARN-ONLY as the first landing with flip-to-enforce as an operator call
  that has not been called.

FALSIFIER: if the scheduled gate task actually invokes --history/--tree mode (I verified
only the 07:56Z run's mode), or if flipping prepush to enforce still yields zero findings
on the outgoing pack, this finding dies. Note the six fingerprints are printed but not
per-path attributed in what I captured; a run of the tool with JSON output would name
them.

MOVE (~30 min): run the gate's own history mode once against the full ref set
(`.venv/Scripts/python.exe tools/secret_gate.py --history`; runtime expect minutes to
~20 min per LANE4C:102, OWED, not executed this sitting), and flip the prepush
credential gate to enforce for pushes to remotes whose URL matches a public host.

## F3: boot law is PR-writable on the shared surface (the injection channel)

EVIDENCE:
- `state/GENOME.md:10-14`: the machine-readable genes live in memory/rib_bus/
  (doctrine.json, standing-wave.json), "loaded at boot by rib_bus.mount, and carried
  onto every task by rib_bus.inject_for".
- `git ls-files memory/rib_bus` → 51 tracked files including doctrine.json and
  standing-wave.json. They ride any push, and on GitHub they become PR targets.
- `grep -n "def mount\|verify\|sha256\|signature\|hash" mag/rib_bus.py` → hashlib import
  and one dedupe hash at line 64; `mount` at line 185. No signature or manifest
  verification found on the load path by keyword scan (scope: keyword grep, not a full
  read; see blind spots).
- The boot order itself loads a watch/inbox file: `state/GENOME.md:71-73` (step 5, the
  Delta Register, "route by it until a newer register exists"), and
  `watch/inbox/frontier_delta_register_20261003.json` is tracked (`git ls-files`
  confirmed). Untrusted banked scrape content (16 tracked X_INTEL_*.md files counted via
  `git ls-files watch/inbox | grep -c X_INTEL`) sits in the same tree, same trust tier.
- Topic material (the ask): "The rib bus has no claim system." At N=2 the same
  last-writer-wins surface that loses work also accepts law.

FALSIFIER: a full read of mag/rib_bus.py mount()/inject_for that shows a hash-pin or
signature check over the gene files before injection kills this; so does a spore recipe
that hash-pins the law set outside the PR-writable tree.

MOVE (~40 min): hash-pin the law set (GENOME.md, queue/STANDING_RAILS.md,
memory/rib_bus/*.json, the delta register) in a manifest verified by rib_bus.mount()
before injection; PR edits to law files then fail closed at boot.

## F4: dormant gates are armed-by-documentation (persistence + spend ship ON)

EVIDENCE:
- `state/GENOME.md:73-75`: cold-boot order step 6 is "Then act: drop work into the
  rails, fire the crons, bank everything". The seed itself instructs arming the crons.
- `ls scripts | grep register` → 13 tracked schtasks registrars
  (census_patrol, corpus_rescan, day_end, endpoint_news, fts_index, gap_sentinel,
  gate_canary, improve, leave, ratchet, tip_witness, vision_nightly, x_radar).
- `scripts/register_x_radar_task.ps1:17-24`: deletes any existing task then
  `schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 08:00` unconditionally; paths
  are $PSScriptRoot-relative (`:8`), so the primitive is portable to any machine with one
  command and no per-machine config. No consent or funding guard in the script body.
  `scripts/x_radar_daily.ps1:20` documents it rides a "Grok Build usage balance" (402
  handled), i.e. an account-riding egress loop.
- The tutorial side of the ask (DeepSeek keys, z.ai-lite monthly, OpenRouter, free
  lanes) is a money-arming sequence with no gate between "clone" and "funded".
- AGENTS.md:34 (DRIVING LADDER) shows what the armed state means: funded keys, spend
  orders, account names, all in the tracked tree.

FALSIFIER: if every registrar fails closed without an explicit operator flag, or the
regrow guide ships crons default-off behind a funded-keys consent step, this is cured;
my read of register_x_radar_task.ps1 shows no such guard (single-file check, not all 13;
extending the read to the other 12 is 15 minutes and would strengthen or kill it).

MOVE (~25 min): add a shared guard (e.g. `if (-not $env:ESTATE_FUNDED) { exit 1 }` via a
dot-sourced common preamble) to all 13 registrars, and rewrite GENOME boot step 6 as
"fire the crons AFTER the funding gate passes".

## F5 (CONVERGENT with .gitignore's own audit comments; the counterintuitive positive): .env is the clean surface, banked content is the dirty one

EVIDENCE:
- Full-history name census (untruncated):
  `git log --all --pretty=format: --name-only | grep -i "\.env" | sort | uniq -c` → 7
  rows, all `*.env.example` variants (.env.example x4, starter-kit, OnionClaw steal,
  configs/cloud_steering.env.example). No .env path was ever committed.
- `.gitignore:19-24`: .env, .env.local, .env.*, configs/providers.yaml,
  deploy/k8s/mag-secret.yaml all walled. Working tree: `.env` present, untracked.
- HEAD content shape: `git grep -nIE "xai-[A-Za-z0-9]{30,}" HEAD` → exactly 2 hits, both
  the synthetic test payload (tests/test_gate_blocking_paths.py:219 and
  watch/inbox/audit_20260926/GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md:20), both
  accepted by name in configs/secret_gate_baseline.json:39-45.
- The class that actually bites is directory-level banked private content: the tracked
  tars (F1), tracked zknot session prompts (F1), history-only dossier blobs
  (LANE4C:13-14), and `.gitignore:30-34`'s own record that "7 live .env values were
  committed" inside memory/trajectory/steps.jsonl with "history left intact per
  operator". A filename-based strip list (.env, *.key) would have missed every one.

FALSIFIER: an .env-named path surfacing in any ref's history (my instrument: the name
census above, run untruncated this sitting) kills the claim; a live key in tracked HEAD
text beyond the two accepted fixtures extends it.

MOVE (~15 min): write the spore manifest's strip list by directory class (attic/,
memory/zknot/, memory/portable_bags/, memory/trajectory/, all archives) and add a
pre-export tripwire that fails on any blob over 10MB or any binary blob in the export.

## Checks run this sitting (inventory)

git remote -v; git count-objects -vH (14.37 GiB size-pack, 160,429 in-pack, 878 commits
on HEAD); git log --all --pretty=format: --name-only piped greps for .env / lan.key /
pem / trajectory (300s timeout each, untruncated outputs); git ls-files greps (env,
secret, token, cred, key names; memory/rib_bus; memory/zknot; watch/inbox X_INTEL count);
git ls-tree HEAD on the 20260825 tar; git ls-tree -r github/master + secret-name grep
(count 0); git merge-base HEAD github/master (rc=1); git merge-base --is-ancestor for
cd2f8e6a520d / be3ffa520a21 / 799ddb6feaad; git cat-file -e cd2f8e6a520d; git grep
-nIE xai shape over HEAD; git push --dry-run github HEAD:master (full output read);
ls -la on attic/, memory/trajectory/steps.jsonl (56,695,409 bytes, mtime 2026-10-05
07:12), .env; grep of scripts for personal paths (none found in registrars) and grok
spend lines; keyword scan of mag/rib_bus.py; WebFetch of the public repo page (exists,
public, MIT, 13 commits).

## OWED / not run

- tools/secret_gate.py --history full run (F2 move): not executed this sitting; the
  history-dirt inventory rests on LANE4C plus my tracking/reachability commands.
- The six prepush fingerprints were not attributed per-path (no JSON out captured).
- Tar members not re-extracted (would risk printing secret material; LANE4C:108 policy).
- LANE4C's "steps.jsonl in 4 commits" did NOT reproduce under my `git log --all`
  name-only census (zero memory/trajectory rows in any ref). The working-tree file is
  56.7MB, untracked and ignored, so a git push does not carry it; a directory-copy spore
  would. Discrepancy unresolved, reported rather than harmonized.
- Live schtasks state not queried; the daily gate task's invoked mode not verified
  beyond the 07:56Z receipt.

## Blind spots

Honest: I read receipts and code, I did not run the multi-operator scenarios (N=2/4/8)
or any route_chat call; I cannot see the public repo's current state beyond the local
remote-tracking ref and one WebFetch (if GitHub advanced past the last fetch, my "clean
today" is stale); the rib_bus no-verification claim is a keyword scan, not a full read;
GitHub's 100MB blob rejection is documented platform behavior I could not trigger in
dry-run (dry-run sends no pack), so I cannot prove which artifact would trip it first.
