# ACCURACY LENS - dogfood the standing workflow fleet (2026-10-03, run 2026-10-02-workflow-dogfood)

Falsifier-hunter pass. Every claim below was run or read this sitting; instruments are
named where an absence is claimed. No em-dashes. Convergence flags marked.

## Instruments I ran (so the absences have names)

1. ListSavedWorkflows (the harness census): 19 saved project workflows. The ask names 12.
   The 7 unnamed: game-dig-coop-social, game-dig-creature-farming, game-dig-horror-maze,
   game-dig-liveops-seasonal, game-dig-roguelike-runs, game-mechanics-deep-dig, music-cut.
2. Full enumeration of memory/workflows/REGISTRY.jsonl: 63 rows, 2026-09-25T18:52:02Z to
   2026-10-03T21:56:30Z (venv python json parse of every line, all rows printed).
3. tools/workflow_gate.py read: REGISTRY constant at line 42, docstring line 10 "every
   submission registers a row", the append write at line 324. Scenario mode writes no row
   (lines 268-270).
4. MD5 grouping of all 19 saved scripts (.zcode/workflows/*.dwf.ts) plus 63 drafts
   (.zcode/workflow-drafts/*.dwf.ts), with mtimes.
5. watch/inbox top-level census: 116 dirs; targeted listings of fillball (7 files),
   gala_20260925 (51 items), gap_analysis_20261001 (1 file), librarian_exp (16),
   salon_mine (26, incl. 19 m*.md lane files), localfirst (8), spiking_wide (8),
   mickey (50 items, 09-11-era names), frontier_olm_* (5 dated folders), music (13 files).
6. Walk of watch/inbox/ractor_engine/: 5 prior run folders + this one = 6.
7. Filename greps over the watch/inbox tree for THE50 / GAMEDIG / MICKEY / tree /
   doctrine / fifty (hit lists banked in the session log).
8. File stats: the-50.dwf.ts mtime 09-26 16:33; THE50_RELAUNCH_VERDICT_20260925.md mtime
   09-25 21:09; draft THE-50--reset-day-fullsend.dwf.ts mtime 09-19 14:16; music folder
   newest artifact 10-02 17:47 vs music-cut.dwf.ts saved mtime 10-03 17:55;
   TREE_DOCTRINE_V2_DIGEST_20260925.md exists, 160,327 bytes.
9. Bank-path extraction (regex over artifact.file / ROOT lines in each saved script) and
   difflib similarity for the game-dig family.
10. git check-ignore .zcode/workflows/the-gala.dwf.ts -> rc 1 (not ignored);
    git ls-files .zcode/ -> 1 tracked file in the whole tree.
11. ListWorkflowRuns: workflow_introspection_unavailable. CONVERGENT: both prior ractions
    hit the same gap (watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md:132
    "workflow_introspection_unavailable, reproduced"). This is the third reproduction.
12. Reads: state/CURRENT.md whole (60 lines), SYNTHESIS.md of 2026-10-01-dogfood-gaps and
    2026-10-02-dogfood-48h, fillball-1001_RECEIPT.md (head), MICKEY17_WAVE_LEDGER_20260929.md
    (head, 598 lines total), MICKEY17_RUN_PLAN_20260929.md (head, 50 lines).

## Finding 1: the "12 workflows" premise is wrong twice; the fleet is 19 name plates on about 5 bodies

The census reads 19 saved workflows, not 12 (instrument 1). Worse for the fleet question:
byte identity collapses the named 12 into a handful of engines. MD5 group 8bf79d38ca holds
15 byte-identical files: the saved the-gala.dwf.ts plus 14 mission-named drafts that ARE
the 10-01 wave's actual fires (Fill-ball-one-sittings, Librarian-gathering-expedition,
Localfirst-steal-wave, Salon-mine-20deep, Spiking-wide-dig, Music-ractor, Ouroboros-meta,
Build-it-all, DD-selfsteal-big-one, Hitler-dig-full-dogfood, Lyric-workover-stage1,
Vonnegut-final-cut, Salon-vault-offpeak, Salon-vault-stragglers). The saved drop-dig,
wide-dig, salon-mine, librarian-expedition and fill-ball all still carry the-gala's bank
internals verbatim (bank-path extraction: all six return watch/inbox/gala_20260925;
drop-dig.dwf.ts:94 `GALA_ROOT = ESTATE + "/watch/inbox/gala_20260925"`, receipt writes at
:345 and :360). Group 692d2b1616: saved mickey17-v2.dwf.ts is byte-identical to draft
Gap-analysis-100m.dwf.ts, so the 10-01 "gap-analysis run" rode mickey17-v2's body with
different args. Group c444aad504: saved olm-mine.dwf.ts plus 5 byte-identical daily drafts.
The fleet is not 12 tools; it is roughly one universal battery (the-gala), one daily mine
(olm-mine), one audit engine (ractor-engine, group 943723e3e1 with 4 copies), one paced
burn (mickey17-v2), and the game-dig template, wearing 19 name plates.
Falsifier: re-run the MD5 grouping; these are live working files and siblings are editing
them right now (Gap-analysis-evening draft created 22:21 during this ask).
Move (30 min): mint a repo-tracked manifest mapping each saved name to its body hash,
bank root, and last-fire evidence, so the name-plate layer can never silently diverge
from the body layer again.

## Finding 2: no single ledger counts fires; counted correctly, 4 workflows are repeat-fired, 7 fired exactly once, and at least 8 saved bodies have never fired at all

REGISTRY.jsonl is a gate-submission ledger, not a run ledger (workflow_gate.py:10, write
at :324). Same-digest triple rows prove it overcounts (tree-doctrine-dig.dwf.ts at
21:19:32, 21:19:43, 21:19:55 on 09-26, identical digest d2a6783b55be: three rows, zero
additional runs). The harness run journal is unreachable from this seat (instrument 11).
The honest instrument is bank folders plus byte-identical drafts, and it gives:
- Fired many: the-gala (20+ fires; 6 byte-identical v1 drafts in group 42d45780aa plus 14
  v2 drafts in 8bf79d38ca, banked under watch/inbox/gala_20260925/ whose 51 items carry
  the matching subfolders and receipts); olm-mine (5 dated banks: frontier_olm_20260928,
  -2026-09-30, -2026-10-01, -2026-10-02, -2026-10-03, plus 2 same-day drafts on 10-03
  incl. a retry); ractor-engine (6 bank folders incl. this run; 4 byte-identical copies of
  the saved body created on 10-03 alone); mickey17-v2 (09-25 wave receipts
  MICKEY17_WAVE2_QUALITY_20260925.md, the 09-29 24-wide MICKEY17_WAVE_LEDGER_20260929.md,
  plus the 10-01 body-borrow by gap-analysis).
- Fired once: gap-analysis (bank = gap_analysis_20261001/ holding exactly 1 file,
  GAP_REGISTER.md, mtime 2026-10-01T18:41:58 per the 10-01 synthesis line 13), fill-ball
  (fillball-1001, 7 lanes, close stamp 2026-10-02T06:37:17Z,
  gala_20260925/fillball-1001_RECEIPT.md), librarian-expedition, drop-dig (localfirst/,
  8 files), wide-dig (spiking_wide/, 8 files), tree-doctrine-dig
  (TREE_DOCTRINE_V2_DIGEST_20260925.md), salon-mine (one bank folder, 19 lane files, two
  family fires of which one rode the saved body byte-identically).
- Zero fires as saved body: the-50 (saved 09-26 16:33; every THE50 receipt predates the
  save: RELAUNCH_VERDICT 09-25 21:09, REVIEW_R9 09-19, FOLD_VERIFICATION 09-20; the
  reset-day draft is 09-19, a week before the save; no bank folder), music-cut (saved
  10-03 17:55; newest artifact in its bank is CUT_PRESS_JUNKET.md 10-02 17:47), the 5
  patched game-dig veins (GAMEDIG receipts all 09-26 plus MASTER_ATLAS 09-27, the patch
  date; zero post-patch GAMEDIG receipts; pairwise byte similarity 0.976,
  game-dig-coop-social vs game-dig-roguelike-runs), and in fact 8 of the named 12 saved
  bodies, whose "proof" runs all rode byte-different predecessors.
Falsifier: any bank folder, receipt, or INDEX.json row outside watch/inbox naming a fire
of these saved bodies; my absence claims are scoped to the 63-row registry, the 116-dir
inbox census, the filename greps, and the file stats named above.
Move (45 min): extend the gate row with run-id and fired-at, and have each workflow's
receipt land one line in a single runs.jsonl, so "fired twice" becomes a one-grep fact
instead of a three-instrument archaeology.

## Finding 3: the saved-workflow layer is outside every estate gate and still carries the struck 191.8M phantom

The estate struck the 191.8M-token headline with its own instruments: the 10-01 synthesis
records STORY.md:240 re-anchoring the clause at 00:29:21 (watch/inbox/ractor_engine/
2026-10-01-dogfood-gaps/SYNTHESIS.md:22-25), and AGENTS.md's citation-lint bullet names
"the struck 191.8M-token headline" as the lint's founding fixture. Yet my grep this
sitting finds the number still asserted as provenance in three saved descriptions:
olm-mine.dwf.ts:8 ("Provenance: 191.8M-token run 2026-09-29"), gap-analysis.dwf.ts:8,
fill-ball.dwf.ts:7. The reason it survives: .zcode/ is git-untracked (instrument 10:
1 tracked file repo-wide), so the ratchet, citation lint, and freshness checks, all of
which ride repo files at pre-push, never scan the fleet's bytes. The fleet's name plates
and descriptions are the one prose surface in the estate with no lint coverage.
Falsifier: re-grep the three files; a sibling amending gap-analysis right now could
already have fixed one.
Move (45 min): amend the three descriptions in the same sitting, then add a mirror of
.zcode/workflows/*.dwf.ts (or at least their description blocks) into a repo-tracked file
that tools/citation_lint.py --files can be pointed at.

## Finding 4: six saved workflows promise six different bank folders; all six write into one party folder from 09-25

The arg descriptions promise per-workflow banks: drop-dig "watch/inbox/localfirst_<slug>/",
fill-ball "gala_<slug>/", wide-dig "<topic>_wide_<slug>/", salon-mine "salon_mine_<slug>/",
librarian-expedition "librarian_exp_<slug>/". The bodies say otherwise: bank-path
extraction shows the-gala, drop-dig, wide-dig, salon-mine, librarian-expedition and
fill-ball all hardcode watch/inbox/gala_20260925 (drop-dig.dwf.ts:94, :345, :360), and I
found no arg-driven bank-root substitution in any of the six (grep scoped to artifact.file
and ROOT lines). The consequence is visible on disk: gala_20260925/ holds fillball-1001,
librarian-expedition, localfirst-steal, spiking-wide, salon-mine, music-ractor,
ouroboros, hitler-dig, build-it-all and receipts - the entire 10-01 "12 workflow" wave
banked as subfolders of one 09-25 gala. A consumer following any of the five documented
contracts greps the wrong tree. (The per-workflow folders DO exist with lane outputs -
salon_mine/ m01-m19 - so each run wrote to two roots, one documented, one coded; which
seat wrote which root is OWED.)
Falsifier: a script site that computes the bank root from the slug/topic args; I read
none in the six.
Move (45 min): thread a bank_root arg through the-gala's body and correct the six
descriptions to name the real root until then.

## Finding 5: minimum viable fleet is 4 engines plus 3 functional saves; the rest is profile or museum, and the audit organ out-runs the fill organ it audits

Keep, on multi-fire evidence: the-gala (the universal battery), olm-mine (the only
workflow with a real daily cadence), ractor-engine (standing audit; 4 byte-identical
fires of the saved body on 10-03 alone), mickey17-v2 (the paced wide-burn engine, fired
twice-plus with its own refire/pacing machinery). Keep as functional saves with one
proven run each: gap-analysis and fill-ball, because they are the one proven composition
chain: GAP_REGISTER.md written 2026-10-01T18:41:58 was cut into fillball-1001's 7 lanes
(same evening, close stamp 2026-10-02T06:37:17Z), and the 2026-10-01-dogfood-gaps raction
then consumed the same register as its topic - register to fill to audit inside 24h.
Keep librarian-expedition as the only holdings instrument. Everything else: the-50,
music-cut and the 5 game-dig veins are saved bytes with zero fires as saved (finding 2);
tree-doctrine-dig is mission-complete; drop-dig, wide-dig and salon-mine are the-gala
lane profiles and should be demoted to arg templates, not saved scripts. The 5 veins
collapse into game-mechanics-deep-dig plus a vein arg (0.976 pairwise identity is the
proof). Meanwhile the fleet audits itself faster than it converts: ractor-engine has 6
dogfood/meta ractions in 3 days (ractor-topic mtime 10-02 03:24; 2026-10-01-dogfood-gaps;
2026-10-02-dogfood-48h; 2026-10-03-surface-migration; 2026-10-03-grokbot-estate;
Ractor-fleet-meta draft 10-03 18:37; plus this run), while its own organ-level findings
stay unfired - the 10-02 synthesis's "BUILT, NEVER FIRED: seed_seal, percolator
--candidates" line (2026-10-02-dogfood-48h/SYNTHESIS.md:155-156) is the same disease
this lens finds one layer up. CONVERGENT: built-never-fired as a pattern (they found it
in organs, I re-derived it in workflows - independent derivation, outranks novel
single-source). COUNTERWEIGHT, honestly noted: the dogfood loop does convert sometimes;
the 10-02 synthesis's move to refresh state/CURRENT.md landed (state/CURRENT.md:8 now
reads updated 2026-10-03T23:55:00Z), and citation lint is wired at githooks/pre-push
(AGENTS.md a05-r2 bullet). The loop works when a move is small and named; it has never
once produced a second fire of the saves that need one.
Falsifier: a composition that only works through a demoted save, or a post-save receipt
for the-50 / music-cut / any vein.
Move (60 min): one sitting - amend the-50, music-cut and the 5 veins into archived
profiles, collapse the veins into game-mechanics-deep-dig + vein arg via SaveWorkflow,
then fire ONE production percolator --candidates run to convert the loop's oldest
never-fired organ while the census is fresh.

## OWED (not asserted)

- The 09-29 mickey17 24-wide wave has zero gate rows in all 63 registry rows (no mickey
  name on 09-29). Whether that is an ungated fire, a saved-rerun path that bypasses the
  gate, or a draft name I cannot map: OWED. The run's receipts are real (598-line ledger).
- The 191.8M run's own bank folder: no frontier_olm_2026-09-29 folder exists; the nearest
  name is frontier_olm_20260928 (which does hold a RECEIPT.md). Mapping OWED.
- Which seat wrote the lane outputs to the per-workflow folders vs the receipts to
  gala_20260925 (finding 4): OWED.
- Ractor-fleet-meta (10-03 18:37) and Gap-analysis-evening (10-03 22:21): sibling runs in
  flight during this ask; their banks unread.
- The true token count of the 09-29 olm run: not re-derived by me; only the persistence
  of the struck number is asserted.
- Whether the-50's reset-day draft (09-19) ever completed: its bank is unlocated; the
  FOLD_VERIFICATION_20260920.json exists but was not read for a verdict field.

## Blind spots (what this lens could not see)

- No run journal access (workflow_introspection_unavailable, third reproduction): fire
  counts rest on banks, registry, and drafts; a run that banked nowhere and left no
  receipt is invisible to every instrument I ran.
- I did not open the 51 gala_20260925 subfolders; mission-to-bank mapping rests on
  names, receipts, and byte-identical drafts, not on reading each lane file.
- Two banks per run (finding 4) means my per-folder run counts could double-count or
  under-count individual runs that wrote to both roots.
- The tree moved under me: sibling drafts were created during this ask (Fill-ball-amend
  18:38, Gap-analysis-evening 22:21); every hash and mtime here is one moment.
- This is a read-only raction: I fired no workflow, so every "never fired" claim is an
  absence across instruments, not an experiment.
- I did not read the 10-03-surface-migration, 10-03-grokbot-estate, or fleet-meta
  syntheses; if a sibling raction already landed the same findings today, mine are
  convergent duplicates counted as novel (the exact failure the duplication law names).

Verification stamp: all checks listed under Instruments run this sitting by this seat on
the repo at C:/Users/foste/Documents/projects/local_sovereign_agent; venv python used
throughout; no workflow fired; em-dash count in this file: 0.


## REVISION (hostile pass, 2026-10-04): finding 2 verdicted weakened; re-run on the journal the pass named

The hostile pass was right that I missed an instrument: .zcode/workflow-runs/ holds 101
dwfrun-*.mjs launch snapshots (plus 2 dwfeval and a 2-byte .gitignore). Each record embeds
payload.lowered, the args-free compiled code, so launches cluster by md5(payload.lowered):
43 clusters over 101 launches, run by me this sitting. My original 4/7/8 census is
withdrawn. Corrected census, code-cluster standard:

- Repeat-fired on saved code: the-gala 21 launches on cluster 8479acceeb (10-01 04:56 to
  10-03 18:38; this one cluster IS the saved code of the-gala, drop-dig, wide-dig,
  salon-mine, librarian-expedition and fill-ball at once - their saved sources differ
  only in description metadata) plus 8 on v1 cluster b6370c1a93; olm-mine 6 (cluster
  11366ac475, exactly the daily slugs); ractor-engine 4 on saved cluster cdb886fcc5
  (surface-migration, grokbot, fleet-meta, this run) plus 3 on predecessor code;
  salon-mine 5 salon-slug launches (3 post-save); gap-analysis 3 on its amended saved
  code (cluster 46fad86762 = 10-03 17:18/18:38/22:21) plus 1 borrowed fire of mickey17-v2
  saved code (10-01 18:00, cluster f0d1ef3c82 shared with arena_day_one 10-03 17:13);
  mickey17-v2 2 launches on its own saved bytes, both under other missions names;
  librarian-expedition 2 (10-01 18:54+18:57); fill-ball 2 (fillball-1001 10-01,
  fillball-amend 10-03); drop-dig 1; wide-dig 1.
- Never fired on their saved bytes (9 of 19): tree-doctrine-dig (single launch 09-25
  14:59 predates the 09-26 01:30 save; exactly one TREE_DOCTRINE literal hit in the
  journal), the-50 (one 09-19 launch, pre-save), music-cut (zero launches,
  music_cut_gate literal 0/101), game-mechanics-deep-dig (all its fires predate the
  10-02 06:43 save), and the 5 game-dig veins (15 vein launches, all 09-26 18:22-18:28,
  zero containing shrink, while the saved bodies are stamped 09-27 07:21 with the
  PATCHED note and 5 shrink sites each).

Verifications of the pass: registry 63 to 75 rows byte-true; the 12-row gate sweep at
2026-10-04T02:33:47-02:34:06Z names exactly the asks 12 workflows with zero launches in
that window; digest d2a6783b55be at lines 13,19,22-25,75; the ten vein pairwise ratios
re-measured at 0.9618-0.9869. Corrections to the pass: its cluster ids are not journal
literals (0/101 files contain them; 46fad86762bc reproduces as my md5 of payload.lowered,
first 10 hex); its patch time 07:21 is a file mtime, not a commit (git log --all --grep
shrink/GAMEDIG/vein returns zero commits; 09-27 05:00-09:00 has none); its matches-no-
surviving-draft holds only at .mjs format - at source level the 18:38 and 22:21 launch
drafts (Gap-analysis-amend, Gap-analysis-evening) are byte-identical (md5 a02467a715) to
saved gap-analysis.dwf.ts with mtimes equal to the launch minutes, so the gap trio
attributions resolve to the saved body, not OWED. Still OWED: the 09-29 mickey17 24-wide
wave has no journal launch record at all (not a dwfrun; mechanism unknown), and the
journal is garbage-collectable by its own header (line 2: safe to delete once the run has
settled) and .gitignored, so every absence above is only as strong as its retention.

Tightened falsifier: a fire whose dwfrun record was cleaned (header sanctions deletion),
or a launch surface that writes no dwfrun (the 09-29 wave is live proof such a surface
exists). Move (45 min): tools/dwfrun_census.py - cluster payload.lowered hashes, join to
saved-body hashes and REGISTRY rows, emit fires-as-saved per name plate; run it in the
daily census patrol so the fleet table is a command, not an archaeology.
