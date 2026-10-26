# MOONSHOT-1: the fleet ractors itself (ouroboros R1, 2026-10-05)

<!-- no em/en dashes; plain hyphens only, per the seat law. -->

Lens seat: moonshot-1, round 1 of 5 (the fleet). Evidence base read this sitting:
state/CURRENT.md, both run spec addenda (watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md,
watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md), tools/mickey17_v2_fold.py (all 235 lines),
.zcode/workflows/mickey17-v2.dwf.ts (all 381 lines), the three mega-burn drafts in
.zcode/workflow-drafts/, memory/workflows/REGISTRY.jsonl (88 rows, full census), all 6 run
dirs under memory/runs/mickey17_v2/runs/ (including the in-flight 2026-10-05-exec), the
2026-10-02 fleet dogfood SYNTHESIS, and targeted greps over the 19 saved fleet bodies.
Every instrument I ran is named inline; everything I could not verify is marked OWED.

## F1 (CONVERGENT, rank 1): the verdict wiring is structurally blind; every unconfirmed tier-2 row rides "included"

The fold's PRISMA exclusion reads a key the runner never writes. Chain, personally verified:

- tools/mickey17_v2_fold.py:181 reads `c.get("unconfirmed")` (a top-level list per checks
  file), and :183/:190 match on `norm(x.get("claim",""))[:80]`.
- The runner persists tier-2 under the key "deep_tier2" (.zcode/workflows/mickey17-v2.dwf.ts:278-282,
  the persist phase), and the persisted entries carry exactly {evidence, row_key, verdict}:
  I walked every deep_tier2 entry in runs/2026-10-04-0/lanes and runs/run-0/lanes this
  sitting; the field set is evidence/row_key/verdict, no claim field, 0 of 12 (+ 0 of 7
  checks-written so far in-flight) files carry a top-level "unconfirmed" key.
- Live measurement (my heredoc over both completed archives): 2026-10-04-0 holds 12
  deep_tier2 verdicts = 7 verified / 5 unconfirmed; the fold's own wiring would exclude 0
  rows; the 5 unconfirmed rows (the ones carrying this week's measured corrections: 910 not
  917, 28 not 30, 250 not 160, 86.0 not 89.4) rode `included` while the fold printed
  `excluded: 0`. run-0: 15 verified / 1 unconfirmed, same blindness, same 0 exclusions.

CONVERGENT: both spec addenda carry this as E20 ("upgraded from defect to proof: the two
shapes can never meet"), and the in-flight execute-register lane e12 independently asks for
a fold-script hardening (draft line 102: "add the unbound-aggregate check to
tools/mickey17_v2_fold.py"). Three independent derivations, one sitting window.

The fix is ~10 lines in ONE file with FIVE consumers (saved mickey17-v2.dwf.ts:295, saved
gap-analysis.dwf.ts:312, and the three mega-burn drafts all invoke the same fold through
the same wrapper): read `deep_tier2[].verdict`, treat "unconfirmed"/"crashed" as excluded
under code 9, and match `row_key` to rows by stripping the "laneid: " prefix (built at
mickey17-v2.dwf.ts:156) and comparing norm(claim)[:60].

Falsifier: a checks file carrying a top-level "unconfirmed" list of claim-bearing entries
would make the current wiring work; measured 0 of 19 checks files across both completed
runs (instrument: my field-walk heredoc, this sitting).

## F2 (rank 2): the thrice-reused skeleton must become ONE saved parameterized engine; the copies diverge in exactly the load-bearing spots

Measured this sitting: Gap-analysis-evening.dwf.ts 397 lines (draft, Oct 3 22:21),
read-the-estate.dwf.ts 387 lines (Oct 4 17:15), execute-register.dwf.ts 359 lines
(Oct 5 00:38). Pairwise line-diffs: 179 changed (gap-evening vs read-estate), 220
(read-estate vs execute-register). Beyond the lane tables, the divergences are engine
constants:

- Slug formula: execute-register.dwf.ts:77 = topic-slug + "-exec"; read-the-estate.dwf.ts:87
  keeps the saved topic + "-" + targets-length formula (saved mickey17-v2.dwf.ts:88). The
  read-the-estate run dir "2026-10-04-0" decodes targets-length 0, which per the addendum's
  section 1.2 made its casualty `fired: 12` self-referential (--fired 0 fell back to
  n_files at tools/mickey17_v2_fold.py:120).
- Master fold name: saved runner hardcodes MASTER_MICKEY17_V2.md (8 sites,
  mickey17-v2.dwf.ts:321-355); drafts renamed to MASTER_READ_ESTATE.md / 
  MASTER_EXECUTE_REGISTER.md (read-the-estate:327, execute-register:304) = E33.
- Workspace collision: ALL FIVE copies hardcode the same WSOUT
  "C:/Users/foste/.zcode/workspace/default/mickey17_v2" and the same fold_run.sh
  (read-the-estate:81-82, execute-register:74-75, Gap-analysis-evening:82-83, saved
  mickey17-v2:80-81). Two burns 12h apart shared one wrapper script and one workspace;
  only the master-file rename (luck, not design) prevented byte collision.
- The E26 cure (tier-2 persist merges instead of overwriting, observed working in
  read-the-estate per the addendum Law 6) lives only in draft-plus-prompt bytes; the saved
  engine's spec file was never updated to bless it (addendum E26: "promote what the runner
  already does into the spec's A3+A4 wording").

The steals die in drafts because drafts are one-fire bodies: nothing reads them back.
Move: amend mickey17-v2.dwf.ts into the parameterized engine (args: genre, master_name,
bank_root; slug = topic-slug + "-" + UTC moment stamp, never targets-length; WSOUT per
run slug), then the three drafts retire at next fire. The gate already blesses amendments
over rewrites (REGISTRY ledger law; amend-not-rewrite).

Falsifier: if the drafts' engine sections were byte-identical (only lane tables differ),
parameterization buys nothing; the measured 179/220 changed lines and the three engine
constants above say otherwise.

## F3 (CONVERGENT, rank 3): the counting gate misleads at this shape; tier-1 is an entropy sink the fold dresses as signal

Personally verified in tools/mickey17_v2_fold.py: the verifier table counts list LENGTHS
(:157-160 `vc[k] += len(v)`), so the fold line "verdicts: checks 10, deep_tier2 12,
entries 5, supports 45" carries zero verdict values; the real splits (tier-1 48 no / 12
yes = 80% no; tier-2 7 verified / 5 unconfirmed) I decoded only by hand-walking the checks
files, and they are computed nowhere in script. The Law-7 gate line prints unconditionally
(:177) with zero discriminating power at the uniform 5-row floor (top-10 share 83.3% is
arithmetic at 12 lanes, median=max=min=5), and TOP-K ranks (leverage, lane-id, row-index)
(:204) = alphabetical, cutting r05#3 while 21 later-alphabet high rows rank below. The tier
system misled: tier-1's 80% no-rate is the demotion-rule-instead-of-demotion pattern (E6),
substance lives at tier-2, yet the fold gives tier-1 four key-name buckets and tier-2 zero
decoded values. CONVERGENT with E5/E6/E23/E24 as re-derived by my own census, third
independent derivation across the two addenda and this sitting.

Move: verifier table prints value splits beside length sums; the gate line prints
rows/lane variance and stays silent when variance = 0; TOP-K tiebreaks by tier-2 verdict
presence and classified-quote novelty, not lane-id.

Falsifier: any archived fold where the current verifier-table numbers alone let a reader
detect an unconfirmed row; none exists in the folds I read (both addenda hand-decoded every
one; my census concurs).

## F4 (rank 4): three laws earned promotion from receipt-prose into script bytes and never got it

- (a) Minimum-viable-fleet retirement (2026-10-02 SYNTHESIS fleet card: RETIRE the-50,
  tree-doctrine-dig, music-cut, the 5 game-dig veins; MERGE wide-dig into drop-dig; STAMP
  the gala variants). Verified this sitting: 19 name-plates still in .zcode/workflows/,
  zero RETIRED stamps, zero amended descriptions; music-cut re-gated PASS
  2026-10-03T21:56:30Z and the-50/tree-doctrine re-gated in the 2026-10-04T02:34 sweep
  (my registry census). The retirement exists only as commit a53b101d4 prose.
- (b) The struck 191.8M phantom still rides three saved descriptions (fill-ball.dwf.ts:7,
  gap-analysis.dwf.ts:8, olm-mine.dwf.ts:8; my grep this sitting) because .zcode/ is
  gitignored and the citation lint never scans fleet bytes (SYNTHESIS:23).
- (c) GALA_ROOT hardcode: six bodies bank every fire into watch/inbox/gala_20260925
  against their own arg docs (drop-dig:94, fill-ball:88, wide-dig:91, salon-mine:94,
  librarian-expedition:89, the-gala:91; my grep this sitting, 4 literal hits each in
  drop-dig and fill-ball).

The promotion path is proven live: G8-width-shape was minted into tools/workflow_gate.py
(header :37, check :94+) from a run finding THIS WEEK (curiosity-register row 3), with its
fail_g8 fixture rows landing in the registry at 2026-10-05T05:19:34Z and 05:20:28Z (my
census). Gates can eat laws; these three were never fed. Move: mint G9-static-bank-root
(reject a hardcoded watch/inbox/<literal> bank constant not derived from an arg) and
G10-metadata-phantom (lint description strings), plus the one-sitting file edits
themselves (stamp RETIRED, parameterize GALA_ROOT, strike 191.8M).

Falsifier: an operator order reversing the retirement; none found in the receipts I read
this sitting (CURRENT.md, SYNTHESIS, registry). Scoped: my "still present" claims are
greps+ls of this sitting's tree, not fire-journal claims (those are the SYNTHESIS's,
scoped to its 101 dwfrun records).

## F5 (rank 5): no manifest, no landing journal: "fired" and "width N held" are permanently unearnable, and the in-flight run proves it live

Verified this sitting: runs/2026-10-05-exec/ contains only lanes/ (my ls); 8 lane files
banked 5 rows each (40 rows, my walk) with zero concurrency record, zero input record; no
manifest exists in any of the 6 run dirs (my ls; addenda E22/E32 concur from their own
searches). The casualty header's `fired` came from --fired TARGETS.length
(mickey17-v2.dwf.ts:295), which for read-the-estate decodes as 0 (the "-0" slug), so the
fold's `fired: 12` measured the file count (fold :120 fallback). bankLane()
(mickey17-v2.dwf.ts:168-172) reports but never journals; A6 rewrites destroy mtime
ordering, so even post-hoc reconstruction is dead. Move: phase-0 manifest write
(runs/<slug>/manifest.json {topic, target ids, width, moment, runner digest}) + one
journal.jsonl append per bankLane/refire/tombstone; the fold then prints manifest-vs-files
as the honest casualty line and the OPERATING ENVELOPE section (E3: my grep reads 0 hits
in both newest folds; E7: no timestamp line, my grep 0 hits) from journal data.

Falsifier: an estate-side journal/manifest instrument I missed; my instruments were ls of
all 6 run dirs, the fold source, and the runner source; the two addenda independently
searched and found none either (E22, E32).

## THE RANKED AMENDMENT TABLE (executable)

| # | File | Exact edit | Defect prevented | Evidence row |
|---|------|-----------|------------------|--------------|
| 1 | tools/mickey17_v2_fold.py:179-202 | PRISMA block: collect unconfirmed from `deep_tier2[].verdict in ("unconfirmed","crashed")`, match row to row_key by stripping the "^<laneid>: " prefix (built at mickey17-v2.dwf.ts:156) and comparing norm(claim)[:60]; count under code 9 | 5 unconfirmed rows riding included (2026-10-04-0), 1 (run-0); excluded: 0 theater | my census heredoc this sitting; addendum READ_ESTATE 1.1 |
| 2 | tools/mickey17_v2_fold.py:154-166 | Verifier table: decode values, print tier-1 yes/no split and tier-2 verified/unconfirmed/crashed split beside the length sums | E5 fifth recurrence: 48/12 and 7/5 invisible to every fold reader | my checks-file walk; addendum 1.1 both files |
| 3 | tools/mickey17_v2_fold.py:127 and :227 | First line "written: <UTC ISO>"; new OPERATING ENVELOPE section sourced from manifest+journal when present, else named OWED | E3 (0 hits in 5 folds, my grep), E7 (no fold timestamp) | my grep 0 hits, both newest folds |
| 4 | .zcode/workflows/mickey17-v2.dwf.ts:80-88 + new phase-0 + bankLane :168 | slug := topic-slug + "-" + UTC-moment (never targets-length); WSOUT := workspace/mickey17_v2/<slug>; phase-0 writes runs/<slug>/manifest.json {topic, target ids, width, moment}; bankLane appends one line to runs/<slug>/journal.jsonl; add args genre + master_name, replace the 8 hardcoded MASTER_MICKEY17_V2.md sites | E22 self-referential fired; E32 no width receipt; E33 master-name divergence; WSOUT/fold_run.sh collision across 5 copies; draft divergence class itself | draft diffs 179/220 lines; my WSOUT grep (5 identical constants); addendum 1.2 |
| 5 | the-gala.dwf.ts:91, drop-dig:94, fill-ball:88, wide-dig:91, salon-mine:94, librarian-expedition:89 | `const GALA_ROOT = ESTATE + "/watch/inbox/" + String(args.bank_root || "gala_20260925");` (+ add the arg to each header block) | every fire of 5 non-gala bodies banking into the one 09-25 party folder against their arg docs | my grep this sitting, 6 sites, 4 literal hits each in drop-dig/fill-ball |
| 6 | fill-ball.dwf.ts:7, gap-analysis.dwf.ts:8, olm-mine.dwf.ts:8 | strike "the 191.8M phantom" / "191.8M-token run" from the description headers; cite the ERRATA instead | struck phantom living as provenance in saved metadata the lint cannot see | my grep this sitting, 3 hits |
| 7 | tools/workflow_gate.py (after G8, :94+) | new check G9-static-bank-root: FAIL when a `const X_ROOT = ESTATE + "/watch/inbox/<literal>"` is not derived from an args field; scenario card per the LAW-12 suite | recurrence of amendment 5's class in every future save | G8 precedent minted this week (gate header :37; fail_g8 registry rows 2026-10-05T05:19/05:20Z, my census) |
| 8 | the-50, tree-doctrine-dig, music-cut, game-dig-* (5) headers | prepend "RETIRED per the 2026-10-02 fleet card (SYNTHESIS.md); do not fire" to each description (amend-not-delete, RETIRED.md Q7 precedent) | museum plates re-gated and re-swept as if live (music-cut PASS 10-03, the-50/tree-doctrine in the 10-04T02:34 sweep) | my registry census; SYNTHESIS fleet card |

Kill verdict (no sacred cows): nothing in the saved 19 deserves deletion; 8 deserve the
RETIRED stamp and one (mickey17-v2) deserves to become the single parameterized engine so
the drafts stop being the real fleet. The true theater surface is the drafts layer: 68
draft bodies, each gated PASS once, never read back by anything.

## Blind spots (honest)

- I did NOT execute tools/mickey17_v2_fold.py (it rewrites FOLD_SECTIONS.md in place and
  would mutate the archives I audit); every fold-defect claim is grounded in the read
  source lines plus my read-only simulations over the archives. The amendment table's fold
  edits are therefore untested against a live fold run: OWED, first execute on the
  in-flight 2026-10-05-exec archive after its lanes settle.
- I did not read the three master folds in full (structure via the addenda plus targeted
  greps only); content-level findings were out of ask scope (engines, not content).
- I did not inspect .zcode/workflow-runs/ (the fire journal) this sitting; "never fired"
  claims are relayed from the 2026-10-02 SYNTHESIS and scoped to its 101 records.
- Draft-vs-saved diff counts (179/220) are raw line-diff counts; some changed lines are
  the lane tables themselves, so the "engine divergence" fraction is approximate, stated
  as such.
- The in-flight run's tier-2 state: 7 checks files existed at my read moment, 0 carried
  deep_tier2; its final verdict shape is OWED until the run settles.
- Line-diff and diff-count instruments ran under bash via the harness shell; no bare
  subprocess was spawned by me on win32 outside the sanctioned .venv python heredocs, so
  the CREATE_NO_WINDOW law saw no contact surface this sitting.
