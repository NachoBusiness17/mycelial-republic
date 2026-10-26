# SYNTHESIS - OUROBOROS ROUND 1: THE FLEET (2026-10-05)

Filed by the synthesis seat. Seventeen artifacts rode this round (accuracy,
communication, dogfood, economics, logic, moonshot-1/2, operations, plus seven
hostile passes); everything below was either re-verified by my own reads and
censuses this sitting (instruments named inline) or is marked as carried from a
named lens. The fold script was NOT executed: it rewrites FOLD_SECTIONS.md in
place (tools/mickey17_v2_fold.py:227-228) and would mutate the archives this
chapter measures.

## The thesis no single lens could see

The snake ate, and the eating worked. This round alone the content loop closed
twice under hostile fire: the 35-vs-40 row dispute reconciled to 40 by naming
instruments (the bare JSON array in e07-receipt-bindings.json eats rows-key-only
readers; ERRATUM at operations.md:191-198), and the "6 fires, 3rd most-fired"
claim was withdrawn to "8 gate certificates, zero launches of current bytes"
(operations.md:200-206). Corrections land, fabrications die, instruments get
named. That is the estate working.

But the engine that does all this counting cannot count itself, and the reason
is one disease wearing four coats: every instrument reads a surface nobody
writes. The fold script reads a top-level `unconfirmed` list
(tools/mickey17_v2_fold.py:181) while every runner persists tier-2 verdicts as
`deep_tier2` arrays (mickey17-v2.dwf.ts:278-284; my full read of the fold file
finds zero `deep_tier2` tokens in 235 lines). The brand-new G8 width gate
matches literal `max_concurrency` declarations (per the accuracy lens's read of
tools/workflow_gate.py:147) while my grep over all 19 saved workflows finds
zero literals, only the-gala prose at :11 and :24. The fire journal's payload
carries {lowered, args} with no width (carried from the lens's extraction of
dwfrun-e9656e14; I did not re-extract: OWED). And the laws that name all of
this live in receipts and addenda that no script bytes ever read.

The design knows. The folder agent is explicitly instructed to include every
tier-2 unconfirmed row in DISPUTED or negatives (mickey17-v2.dwf.ts:323)
because the counting script cannot see them. The engine pays a prose layer to
compensate for its blind instrument, every run, forever. That is not a bug
report; that is the architecture confessing.

The archive holds the proof in one file. run-0's own FOLD_SECTIONS.md prints
"verdicts: checks 15, deep_tier2 16, rows 10, supports 50" at line 27 and
"excluded: 0" at line 40 (my read this sitting). The same file counted the
deep_tier2 list in its verifier table and could not exclude a single one of
them in its PRISMA flow. Six substantive corrections (910 not 917, 28 not 30,
250 not 160, 86.01 not 89.4, plus two) rode as included across the last two
mega-burn folds, surviving only because seat layers hand-decoded what the
script cannot see. Both spec addenda independently byte-confirmed this
(MICKEY17_V2_RUN_SPEC_ADDENDUM.md and READ_ESTATE_RUN_SPEC_ADDENDUM.md sec
1.1-1.2): CONVERGENT, three runs, one defect.

## The fork disease beneath it

The thrice-reused skeleton is the carrier. The "evening burn" was an md5-
identical file-copy refire (a02467a715532191a7e8db94ee7270a6 across
gap-analysis.dwf.ts, Gap-analysis-amend, Gap-analysis-evening; my md5sum),
pure friction a saved re-fire would have avoided. The next two derivations
drifted 174 and 244 changed lines (my diffs: mickey17-v2 vs read-the-estate
174, vs execute-register 244, rte vs exec 220), and each fixed organs locally:
three slug formulas (mickey17-v2:88 appends targets length, rte:87 keeps the
vestige whose schema defines no targets, exec:77 hardcodes "-exec"), per-copy
master-name hardcodes (MASTER_MICKEY17_V2 at mickey17-v2:321 ff,
MASTER_READ_ESTATE at rte:327 ff, MASTER_EXECUTE_REGISTER at exec:304 ff), and
none inherited the tier-1 merge fix. The vestigial suffix even resolves a
lineage puzzle: the evening draft's args are exactly {period, slug} (lines
15-26, my read) while :90 appends args.targets.length, so every fire of it
mints "-0"; run-0's slug needed no override theory.

Because .zcode/ is ignored wholesale (.gitignore:198; git ls-files .zcode/
returns only the-gala.dwf.ts, my run), the runs ride untracked drafts and the
auditors read the wrong bytes. The read-the-estate SPEC seat audited the SAVED
runner and concluded 12 lanes ran targetless (E22); the DRAFT that actually ran
defines all 12 lanes inline at rte:103-117 with TARGETS = ALL.slice(0, WIDTH).
The inference is falsified by the draft's own bytes. The audit of the audit
failed for want of a manifest, and the missing manifest bites downstream right
now: exec lane e01's start field points at watch/inbox/read_estate_2026-10-04/
(my grep of exec:92) while my ls proves that folder does not exist. Dead
pointer, live run.

And the dead do not stay dead. tree-doctrine-dig was retired by the 10-02
fleet verdict (a53b101d4), yet its latest gate certificate was minted
2026-10-04T02:34:06Z inside the 12-row zero-launch PASS sweep (registry row 75,
my grep; launch signature TREE_DOCTRINE_V rides exactly 1 of 110 journal
records, the pre-save dwfrun-15738edf). Nothing connects a death verdict to
the certifier, so zombies collect notarizations.

One timing fact decides the ranking: memory/runs/mickey17_v2/runs/
2026-10-05-exec/ contains ONLY lanes/ at my read moment (my ls; mtimes
01:19-02:38, zero deep_tier2 keys yet, four tier-1 key names live: supports 38,
rows 16, checks 2, entries 1 across the lane and checks files). The third
blind fold has not fired. The window to fix the instrument before it lies
again is open, and it closes when run 3 folds.

## THE RANKED AMENDMENT TABLE

| # | Workflow file / organ | Exact edit | Defect prevented | Evidence row |
|---|---|---|---|---|
| 1 | tools/mickey17_v2_fold.py:179-201, :156-162, :127-129 | Walk deep_tier2, match rows by lane-id + claim-head prefix (row_key format per mickey17-v2:156), count unconfirmed/crashed into PRISMA excluded code 9; print verdict-VALUE splits for any verdict-like list; stamp folded_at UTC + sha256(script)[:12] in the header; print gate-vacuous when median==max==min | Six unconfirmations riding included as excluded:0; splits hand-decoded every run; unversioned folds (E7); vacuous Law-7 line | run-0 FOLD_SECTIONS.md:27 vs :40 (my read); fold:181 vs mickey17-v2:278-284; both addenda 1.1-1.2; CONVERGENT x3 |
| 2 | mickey17-v2.dwf.ts:146 + rte:156 + exec:144 | After "(Write tool)" insert: "Read the file first if it exists; keep every existing key verbatim (including deep_tier2); replace only lane/supports/counts." | Refire tier-1 rewrite destroying persisted tier-2 verdicts (E26 root cause); in-flight exec bites on first refire | My reads: :145-146 no merge vs :278-284 merge; rte:156 vs :286-287; exec:144 vs :269 |
| 3 | NEW saved mickey17-burn.dwf.ts (parameterized); edit gap-analysis.dwf.ts:90 + rte:87 + rte dead guard | genre: audit / estate-read / execute; lane table = args.targets OR genre-default inline lanes; master name derived from slug; findings 1-2 baked in; drop the vestigial targets-length suffix (schemas define no targets); delete the dead throw at rte after inline lanes | Fork-and-forget: 174/244-line drift, three slug formulas, "-0" slugs, per-copy master hardcodes | md5 trio a02467a7; my diffs; RUNSLUG lines :88 / rte:87 / exec:77; evening args :15-26 (my read) |
| 4 | estate-filer ask (mickey17-v2.dwf.ts:349-353) + repo root | Copy running script bytes to runs/<slug>/RUNNER.dwf.ts; write manifest.json {topic, width, lanes, fired, script_path, moment}; git add -f .zcode/workflows/*.dwf.ts with .gitignore exception; per-slug addendum paths | Auditors reading the wrong runner (E22 falsified); interface record unrecoverable; single-path addendum already ate the 10-03 SPEC pass | git ls-files .zcode/ = 1 file; .gitignore:198; rte:103-117 vs addendum 1.2; exec:92 start vs missing dir (my ls ENOENT) |
| 5 | all 19 .zcode/workflows/*.dwf.ts headers | Add "// max_concurrency: N"; when N>3 add "// envelope-receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md" (exists, 1009 B, my ls) | G8 passing the entire standing fleet vacuously (zero literals declared) | My grep: 2 hits, both the-gala prose :11/:24; scenario suite exit 0 this sitting (9 cards, my run) |
| 6 | tools/workflow_gate.py | Stop-cert clause: a retired-status script fails or skips re-certification | Zombie certificates minted after death verdicts | Registry row 75 ts 2026-10-04T02:34:06Z postdating a53b101d4; TREE_DOCTRINE_V in 1/110 records (my greps) |
| 7 | tools/workflow_gate.py (check-time append) | Append {ts, script, fired_args, max_concurrency} to memory/workflows/FIRE_LEDGER.jsonl | 110 journal records, zero readers, no artifact joining fire to width | My census: 110 dwfrun records; grep -rln workflow-runs over tools/ + mag/ = RC=1 (no readers); payload shape carried from lens (OWED my extraction) |
| 8 | olm-mine.dwf.ts:8 | Replace the struck 191.8M provenance figure with the corrected one + ERRATA cite | Struck phantom re-inherited by every seat loading the saved def (10-02 law, unexecuted 3 days) | My read :8; a53b101d4 message names this file |
| 9 | Fleet membership (operator call) | Execute the 10-02 minimum-viable-fleet verdict: retire the-50, tree-doctrine-dig, music-cut, the 5 game-dig near-twins; merge wide-dig | Amendment-surface noise; dead members still gate-PASS and collect certificates | My ls: all 19 present; 10-02 SYNTHESIS card; zero launches of current bytes |
| 10 | Spec ports block (MICKEY17_V2 engine spec) | Pin slug formula + manifest + master-name conventions; strike E31's "or the slug was overridden" branch (addendum :109) | Third slug shape in three runs; decode drift downstream | Evening :85-90 (my read); three RUNSLUG bytes |

Rows 1-2 stop this week's active bleeding (30 min + 15 min). Rows 3-4 cure the
fork disease so the next fix lands once instead of three times. Rows 5-8 make
the gate and the journal bite real surfaces. Rows 9-10 are the operator's pen.

No sacred cows: nothing on engine evidence alone earns a death sentence this
round; the retirement candidates in row 9 ride the 10-02 economics verdict and
need the operator's signature, which is the finding, not a hedge.

## Honest residue

- Not run by me: the fold script (mutates archives); the G8 single-script
  falsifier (workflow_gate.py check --script writes a registry row, and minting
  a certificate for a retirement candidate IS the zombie theater of row 6; the
  scenario suite I ran is the read-only instrument and validated both G8 cards);
  any parameterization fire (finding 5's falsifier needs a real CreateWorkflow).
- Carried, not re-verified by me: the e9656e14 payload's missing maxConcurrency
  (lens extraction); the OLM mine engine's internals (32/32, the daymora kill);
  the parked-decisions 88-finding and hostile-5-3 numbers; a07's overwrite note
  inside run-0's addendum. The exec run is in flight: my lane census is a
  moment-read (B2-216 applies).
- The 2026-10-05-exec fold, when it fires, will print excluded: 0 over whatever
  tier-2 verdicts land unless row 1 lands first. That is the round's one
  time-sensitive fact.
