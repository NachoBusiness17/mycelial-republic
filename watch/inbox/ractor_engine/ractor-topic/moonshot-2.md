# MOONSHOT-2 (wild-eye lens) on topic=undefined, 2026-10-02

Schema: ractor.lens.v1 · lane: moonshot-2 of ractor-engine fire (bank ractor-topic) ·
all evidence personally read or run this sitting; nothing hand-copied.

## The founding irony, byte-proven

The run that minted me fired its lenses on the literal string "undefined".
The engine declares `topic: required: true` in its metadata
(.zcode/workflows/ractor-engine.dwf.ts:38-43) but nothing at runtime enforces
it: the only `throw` in the file is line 202 (error handling), and the ask
interpolation is `"The topic under raction: " + String(args.topic)`
(ractor-engine.dwf.ts:147), which stringifies a missing arg to "undefined".
The slug fallback fired too: `args.slug || "ractor-" + (args.topic || "topic")`
(line 90) is why this bank folder is `ractor-topic`. The engine whose law is
"the hostile pass is the immune system" (RACTORSWARM_MAP_20261001.md:76-78)
let a null topic through its own front door: its arg contract is prose, not
code. This is the security lens's named jacket ("gates that test only
themselves", map line 30) worn by the engine itself. N lenses plus moonshots
are burning reads to ride a null right now.

## Findings (full versions submitted through the result shape)

1. FAIL-CLOSED FRONT DOOR (15 min): add a runtime topic/slug guard at the top
   of ractor-engine.dwf.ts (non-empty, not "undefined"/"null", min length),
   amend the saved workflow per the amend-not-rewrite law. Falsifier: if the
   harness facade strips args before the script sees them, validation is
   dead code; prove by logging args at line 1 on the next fire.
2. WIRING RATCHET (45 min): the self-protection organ mag/inference_budget.py
   is imported by a rounding error of its risk class. I ran the census myself:
   grep -rlE "chat/completions|/v1/|api.openai|api.deepseek|api.anthropic|openrouter"
   over mag/ tools/ *.py gives 187 files; grep -rl "inference_budget" gives 6
   (the organ, its carriers, its test). The census's own move is "wire ~10
   standing carriers by hand" (WIRING_DEBT_CENSUS_20261001.md:166-167); the
   10x is to make breadth a ratchet: a pre-push check that fails any NEW
   endpoint-touching file lacking the import, existing 181 admitted by name
   in a baseline (tools/violation_ratchet.py plumbing already wired into
   githooks/pre-push). Counts can then only fall.
3. CLAIMS AS BYTES, PROSE AS RENDER (60 min): the estate stores its load-
   bearing numbers in English prose and then builds regex gates to defend the
   grammar: census_drift_patrol's CARRIER_LINE_RE pins the AGENTS.md bullet
   shape (tools/census_drift_patrol.py:82-83), the file itself admits the
   claim "live[s] in three hand-copied places" (line 98), and the B2-249
   carrier shape law makes rewording break the gate. The fold pattern that
   already killed a race (index_events.jsonl -> INDEX.json,
   scripts/index_fold_host.mjs:6-8, "KILLS the lost-update race structurally"
   per WIRING_DEBT_CENSUS row 3 refutation) is the moonshot shape: a
   claims.jsonl ledger where each row carries value, instrument, moment,
   re-derivation command, and the AGENTS.md bullets render FROM it. Patrol
   becomes "re-derive the row", not "parse the grammar".
4. JUNK-PATH LINT (30 min): HEAD tracks a 46,808-byte Windows temp artifact
   at repo root under a private-use-colon mangled name. Personally ran:
   git ls-tree -r HEAD --name-only | grep lane_a12 ->
   "C\357\200\272UsersfosteAppDataLocalTemplane_a12_commits.txt"; the file
   sits on disk (Oct 1 18:33). The night close documents it deliberately
   stayed staged "as the coordinator left it" (NIGHT_CLOSE_20261002.md:17-19).
   No gate in the estate checks filename provenance; secrets, citations, and
   violations are content-only. Move: relocate the bytes to watch/inbox as
   evidence with a receipt, git rm --cached, add a pre-push junk-path lint
   (Temp, ~$, nul, Thumbs.db, *.tmp, U+F000xx mangles).
5. RETURN METER (45 min): spend is banked per turn (memory/runs/hermes_burn/
   usage.jsonl rows carry cost_usd; the night lane metered $8.9954 across two
   ledgers, NIGHT_CLOSE_20261002.md:50-56) but return is narrative. The
   descent falsifier ("ledger grew but no rib carries a frontier contribution
   = spend theater", AGENTS.md DESCENT PROTOCOL leg falsifier) was evaluated
   once, by hand, in the CROSS-RACTOR pass ("63 pct of day spend was theater",
   HEAD commit 0c9d72a06). Move: a fold over usage.jsonl joining corr_id to
   landed receipts, emitting $/landed-finding per lane at every close.

## Honest blind spots

- I cannot see the driver's intent or sibling lenses' outputs from inside a
  rider; if the operator intentionally fired a topic-less dry run, finding 1
  is a UX catch, not a failure. The bytes still stand: required is unenforced.
- I ran no pytest and no gates end-to-end this sitting; all checks are grep,
  git, and reads. Nothing was substituted for a named check because the ask
  named none.
- PACK_OFFLOAD.jsonl (5.4 MB) and STEALTH_MINED_FINDINGS.jsonl are unread;
  findings hiding in the 48h jsonl floors are invisible to me.
- The on-disk mangled filename's exact codepoint (U+F03A vs plain colon) is
  ambiguous in shell rendering; the git-tracked name is my trusted evidence.
- Finding 5 is proposed, not prototyped: corr_id-to-receipt join coverage is
  unmeasured, and if it is low the fold computes noise.

## STEERING-ROUND ERRATA (2026-10-02, hostile pass verdicted 2 weakened; both re-checked on bytes this sitting)

- Finding 2 counts corrected: real import statements are exactly 3
  (tools/code_swarm.py:44, tools/hermes_burn.py:59, tools/model_garden.py:56);
  my "6" conflated docstring mentions (code_swarm.py:8,72; overmind_brain.py:5;
  overmind_loop.py:12) with imports. The class count is sitting-relative
  (182 census :155 / 187 my grep / 188 hostile), which is now the finding's
  core: only a baseline-admitted gate makes the ratio stable. Census quote is
  at :158 (I cited :161). Cure cite :166-167 and githooks/pre-push:10,:25
  re-verified.
- Finding 5 corrected: corr_id exists in NEITHER usage ledger (grep -c: 0/236,
  0/725, key sets enumerated from head -1), so the proposed fold had no join
  key; revised to a two-legged move (add corr_id at the carriers' bank sites
  first, fold prospectively, mark the existing 961 rows unjoinable). The
  CROSS-RACTOR cite is commit 43f50ed71 (git log --grep verified), not HEAD
  0c9d72a06 as I wrote. AGENTS.md:35 falsifier line re-verified.

Filed by moonshot-2, ractor-engine fire of 2026-10-02. No em-dash bytes.

---

# MOONSHOT-2 second fire, 2026-10-06: same null topic, the estate after the ouroboros close

Fired again on the literal string "undefined", four days after the first fire
banked above. Boot reads this sitting: newest AUTHORED state doc is
state/CURRENT.md (state/LIVE_REPORT.md excluded as machinery per load row 0a,
mtime 18:59 vs CURRENT 14:31, my dir listing), then
state/NIGHT_LOOP_20261005.md (the loop canon) and
watch/inbox/DAWN_REPORT_20261006.md. Every check below was run this sitting.

## Finding 0 (CONVERGENT, the founding irony recurred): the engine still rides a null topic four days after its own lens banked the cure

The 2026-10-02 fire above (finding 1) specced the fail-closed topic guard at
15 minutes. Re-verified on bytes today: .zcode/workflows/ractor-engine.dwf.ts:31-34
still declares topic required:true with no runtime guard, and the ask
interpolation "The topic under raction: " + String(args.topic) still
stringifies the missing arg (my sed of lines 140-150 and grep -c undefined = 3).
Two fires of the same lens independently rode the same null: the fix economy
did not reach this organ. The ractor's own law is "audits become law"; this
audit became a bank file instead.

## The five findings this fire

1. SELF-PLAY EVIDENCE CHANNEL IS FALLBACK-BLIND. mag/selfplay_orchestrator.py:166-170:
   scorer fallback returns the literal "0.5" (:249-252) and the bottleneck
   ledger then stamps ok=True on the leg unconditionally; :154 drops the
   bridge's ok:False/fallback:True flags so placeholder moves ride into
   elo.update (:179). The uncommitted bridge diff (git diff HEAD --
   mag/llama_cpp_bridge.py, lane d13) confesses "the bridge silently rode its
   fallback path for three full probe runs", and watch/inbox/selfimp/imp002.md:31
   banks the 0.5 scorer as a "fix". memory/runs/selfplay/evidence_latest.json
   has no fallback field; its session reads real only by timing inference
   (avg_actor_ms 3472.6). Same class as R2's 13 dead fleet fires under
   LastTaskResult 0 (state/NIGHT_LOOP_20261005.md:142-144). CONVERGENT.
   Move (30 min): fallback counters + CONTAMINATED banner in SessionReport
   and evidence JSON. Falsifier: a dead-scorer session whose report prints
   scorer ok=False; today the identical session prints ok=True.
2. LAW-PACK INHALATION: PACK SIDE PROVEN FRESH TODAY, SEAT SIDE STILL OWED.
   My run: .venv python -c "from mag.context_pack import _quantized_laws; ..."
   returned 1583 chars, "[compile v0.4 2026-10-06]", carrying the POST-DATUM
   rows and the R4b MOUNTED-AT-BOOT amendment, via the seam at
   mag/context_pack.py:435-458. The relay's falsifier stands narrowed
   (state/NIGHT_LOOP_20261005.md:259-263: "seat inhalation ... is the
   falsifier for propagated"): no seat boot has been shown carrying the rows.
   Move (20 min): every seat boot brief prints the compile stamp it inhaled.
   Falsifier: a seat class whose context path never calls context_pack.
3. HERMES 24/7 IS LIVE BUT PINNED TO HAIKU BY A ONE-KEY PICKER. My tail -3
   memory/runs/hermes_burn/usage.jsonl: ok=true H247 rows at
   2026-10-06T23:55:08Z/23:55:27Z, haiku-4.5, $0.0337 the pair. But
   tools/hermes_burn.py:84-95 (_hermes_key) returns the first live key once
   per process; there is no per-ask 402 path, so the premium rung cannot
   fail over cross-key even when the other key holds credits (a3d9d614d F1).
   Per the DESCENT PROTOCOL leg 3, checkpoint climbs are where premium value
   lands. Move (45 min): on premium-SKU 402, flip key for that ask and
   remember. Falsifier: both keys' premium credits aged out means top-up is
   the only cure and the move becomes a double-402 alert to attention.md.
4. THE STASH CLASS IS LIVE ON THIS BRANCH RIGHT NOW. My git stash list: three
   stashes on mag/run-beta1-factory-build-audi-20260806T231709Z, stash@{0}
   carrying the operator-gated GSTD join ("ONE input owed: GSTD_WALLET_ADDRESS"),
   stash@{1} R1 landing WIP, stash@{2} e0ff8cec0-era WIP. Class found
   independently by R3 (:53) and the R5 communication lens (:280-287, "no
   sweeps while a fold is uncommitted"). CONVERGENT. Move (40 min): diff each
   stash against its base, land or label-and-drop, and write the no-sweep
   clause into watch/inbox/SHARED_SURFACE_CONTRACT.json. Falsifier: all three
   diffs empty against history reduces the move to dropping them.
5. THE P0 SECRET GATE WAS SKIPPED BY --no-verify ON A LANDED COMMIT,
   SELF-DISCLOSED, AND MY PROBE SHOWS THE GATE HEALTHY TODAY.
   watch/inbox/selfimp/imp002.md:49-52 admits the bypass ("Pre-commit hook
   broken (path resolution C:\c\... on MSYS) - bypassed with --no-verify; files
   manually verified clean"); githooks/pre-commit:1-15 is the secrets gate;
   core.hooksPath=githooks (my git config); my probe `bash githooks/pre-commit`
   exits 0 today. The named defect does not reproduce on the direct path, and
   the skip also bypassed the pre-push ratchet and citation gates for that
   commit. Move (30 min): commit-msg wrapper writes any --no-verify commit to
   memory/law/enforcement_trail.jsonl (FIRE_LEDGER pattern) so a bypass is a
   ledger fact. Falsifier: reproduce the C:\c\... failure from the harness's
   own git execution context, which I could not test from here.

## Verified cures this sitting (credit where the estate landed them)

- dashboard/data/ESTATE_INDEX.pointer.json regenerated 2026-10-06T13:09:25Z
  with sane numbers (1,218,137 rows / 363,012,458 B master, walk 140,510,023,713 B
  labeled estate-wide), reader at dashboard/server.py:189-211: the
  fiction-numbers caveat in the logic-lens amendment is cured on disk.
- The bridge diff's spawn fixes (flags renamed for llama-cpp-python 0.3.36,
  DEVNULL pipe fix, /health to /v1/models, ratchet debt assigned instead of
  passed) carry receipts in their own comments: model form, uncommitted.

## Blind spots (this fire)

- No seat boot, no pytest, no ratchet run: every check claimed is the exact
  command printed in this file; nothing substituted.
- The three stashes were listed, not diffed; their unique bytes are unverified.
- R4 S5's 1,204-orphan knowledge-graph claim is cited from receipts, not
  re-censused here.
- PACK_OFFLOAD.jsonl, the 48h jsonl floors, and the sibling r5 lens files
  (economics.md, logic.md, communication.md) are unread this sitting; the
  first fire's blind spot persists.
- I did not diff stash contents nor test the harness's git context for the
  MSYS path defect; both are named falsifiers, not discharged ones.

Filed by moonshot-2, second fire, 2026-10-06. No em-dash bytes.

---

## STEERING-ROUND ERRATA (2026-10-06, hostile pass verdicted finding 5 weakened; one clause withdrawn, core re-grounded on new bytes this sitting)

Withdrawn: "the skip also bypassed the pre-push ratchet and citation gates
for that commit." Wrong on git mechanics (commit-time --no-verify skips
pre-commit and commit-msg hooks only; pre-push is a separate event) and moot
on the event timeline: `git branch -a --contains cb5c20edf` returns only the
local branch (remotes github + local exist, neither contains the commit), so
the push gates have not yet fired for it. They are pending, not dodged.

Corrected and strengthened:
- The commit-msg leg skipped was a no-op: githooks/commit-msg:1-6 is a
  never-blocks deletion-trailer lint ("Never blocks: always exits 0") and the
  commit deleted nothing (git show cb5c20edf --stat: 1 file, 52 insertions).
- The receipt admission is imp002.md:52 exactly (my grep -n "no-verify").
- NEW BYTE: I re-scanned the dodged commit's blob with the P0 gate's own
  method (mag.trajectory_step.redactions live values, non-secret filter per
  tools/precommit_secret_check.py:31-36, substring match per :75-77), in
  memory, names-only output: pairs_checked 49, blob_chars 2407, HITS NONE.
  The receipt's "manually verified clean" is now byte-verified.
- Sharpened residual gap: the live-.env-value scan exists ONLY at pre-commit,
  the one event --no-verify kills; the push-time backstop
  (githooks/pre-push:384-407, tools/secret_gate.py gate 10, enforcing,
  fail-closed) detects provider-shaped secrets, a different shape, so a
  --no-verify commit carrying a live .env value that is not provider-shaped
  would pass every remaining gate.
- Move updated: wire the P0 value-substring scan into githooks/pre-push over
  the pushed range (feed git show <sha>:<path> blobs to the same method) so
  the gate the bypass kills gains a backstop at the event the bypass cannot
  reach: 30 min. Falsifier tightened: the finding dies when bypasses are
  ledger-visible before push; it escalates to incident if a bypassed-commit
  re-scan ever hits, or if the MSYS defect reproduces in the harness's git
  execution context (still unreproduced from this seat; untestable here).


