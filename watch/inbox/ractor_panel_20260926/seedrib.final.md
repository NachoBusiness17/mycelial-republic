# Card seedrib, revision final (2026-09-26)

## Final

The surviving candidate seedrib-two's SEED-RIB merge design is now LANDED,
not a deleted proof tree. Durable home: watch/inbox/seed_rib_20260926/ (the
shared inbox, the estate's durable write root; judge's option list, no git
branch created, committing stays the operator's call). The deliverable:

- watch/inbox/seed_rib_20260926/seed-rib/ : the tree. 43 files, 96,507
  bytes on disk (cap 100,000; margin 3,493). Verified this revision by
  `.venv/Scripts/python.exe watch/inbox/seed_rib_20260926/check_seed_rib.py`
  : 14/14 PASS, exit 0, raw output watch/inbox/seed_rib_20260926/check.out
  (run three times on the final tree generation, 14/14 each time).
- Build: `.venv/Scripts/python.exe watch/inbox/seed_rib_20260926/build_seed_rib.py`
  rebuilds the tree from the frozen seed-3.2.0.zip + live estate and prints
  the measured reduction report (raw: build.out). derivation.json carries
  43 rows, source + method per file.
- Battery extensions beyond the candidate's 9 checks: C4b verifies the
  three named-value pointer rows against their live sources; C9 reruns the
  exact compat invocation recorded in SEED_RIB.md and fails on drift; C10
  re-derives the reduction report from the tree and fails on drift vs
  build.out.
- Canonical docs amended in the same change:
  watch/inbox/SEED_RIB_FORMAT_v0_20260926.md (v0.1 directory-carrier
  amendment) and watch/inbox/SEED_RIB_HANDOFF_KERNEL_20260926.md (TOC
  amendment log: load.order cap 600 -> 1,100, dated and reasoned; kernel
  total ceiling stays <= 9,700 binding; section-7 pointers ride as
  POINTERS.sha256).
- INDEX registration in the same change: 18 register rows appended through
  `node scripts/index_fold_host.mjs add` (receipt, three scripts,
  derivation, raw outputs, tree MANIFEST.sha256 + SEED_RIB.md + SEED_VERSION,
  both amended docs re-sealed after edit; the three scripts were
  auto-registered by the md_record_seal hook on Write). INDEX re-folded,
  1,242 active items. `python -m mag.shared_surface validate`: exit 1, ok
  false, 48 errors, ZERO touching this landing (raw: validate.out); the 48
  are pre-existing board drift in other lanes' files (cathedral_v1.html,
  other candidates' stale seals), annotated here, not fixed by this card.
- Cold-seat falsifier ADMINISTERED (details under critique bullet 1).

Honest negative results and caveats, first-class:

1. The candidate's compat claim "9 entries, 23,595 B, law_refs 11" is NOT
   reproducible. Its selection was never recorded (the judge's default-flag
   rerun produced 0 entries / 162 B). The recorded selection
   (`--glob "memory/law/*.md"` against the fleet repo, run from the tree's
   own rib/seed_rib.py) yields 9 entries / 21,473 B / law_refs 12 today;
   the registry gained its 12th law id in the working tree between the
   candidate's run and this revision. The exact command and numbers now
   live in SEED_RIB.md and C9 enforces them; they will fail loudly when the
   law corpus grows, by design.
2. memory/warm_state.json stores chain.verkle_root truncated by its writer
   (19 chars + "..."). The pointer row faithfully carries what the source
   holds; C4b compares row to source byte-exact, so the check is live.
3. Cold-seat run 1's raw output files were overwritten by run 2 before
   per-run stamps existed (harness wart, since fixed with stamped
   filenames); run 1's graded verdict lines survive in this record, runs 2
   and 3 have full raw on file.
4. Still owed (carried, not silently closed): the universe rehydration
   drill on a second machine (Owed 2: no second machine in this lane; the
   essentials row is now hash-verified against the on-disk pack, but a
   fetch-from-mirror drill has not been run), and the 3.3.0 re-merge when
   the mid-cook repack ships (Owed 4; the landed tree builds from frozen
   3.2.0 bytes, sha256 e9f4603a... verified by the judge and sealed in
   derivation rows).

## Critique addressed

Bullet 1 (administer the cold-seat falsifier). ADMINISTERED. Harness:
watch/inbox/seed_rib_20260926/coldseat_seed_rib.py. The prompt is assembled
mechanically from ONLY the 7 tree files the SEED_RIB.md cold join
prescribes (SEED_RIB.md + six kernel prose sections in join order; 9,815
prompt bytes, verbatim in coldseat_prompt.txt), and is fed to genuinely
cold local Ollama models with zero context outside it. Three
administrations, two models: gemma:2b (the fleet's own janitor scut tier)
and qwen2.5:3b-instruct. Graded transcripts coldseat_run2.out /
coldseat_run3.out; raw answers in coldseat_*_run2.out and the
stamp-suffixed run-3 files. Distribution, stated without smoothing:
qwen2.5:3b answered all four kernel questions correctly in substance on
every run (one sample named the law but omitted the concrete interpreter
string: "this repo's interpreter, never bare python on PATH"); gemma:2b
answered all four correctly in 2 of 3 samples, and in its third kept the
thesis, the never-bare-python half and the filing location but pointed at
load.order.md without naming the first files and garbled the
accompaniment. Run 1 was graded under the initial key set whose two FAILs
were key artifacts (a backtick splitting "bare `python`"; a correct
kernel-order answer to Q2 that the key did not accept); the key sets now
name both documented correct forms (load.order row 1 FRAMEWORK_LOAD, and
the SEED_RIB.md step-1 kernel order), and that first-administration
grading is disclosed rather than buried. Verdict: the join transmits the
kernel to kilobyte-class cold agents; the gate is met at the 3b tier
(4/4, raw on file), and the 2b tier is recorded as flaky on specifics.

Bullet 2 (land the tree durably + INDEX row in the same change). DONE.
Home picked: watch/inbox (alongside SEED_RIB_CURRENT_20260926.json), per
the judge's own option list; the receipt
watch/inbox/seed_rib_20260926/SEED_RIB_LANDED_RECEIPT.md lands before
promotion per the shared-surface contract, and 18 register rows are in
index_events.jsonl with INDEX re-folded (1,242 active items). The
candidate's own no-pseudo-state law is honored in spirit: what landed is
not an unverified proof tree but the battery-verified deliverable, seals
intact, rebuildable from the co-landed build script.

Bullet 3 (record the exact compat invocation). DONE, with an honest
correction. The invocation (build + verify, from the tree's own
rib/seed_rib.py, --glob "memory/law/*.md") is now IN SEED_RIB.md inside
the tree with its measured expectation (9 entries, 9 inline, 21,473 B,
law_refs 12, verify 9/9 hash-matched), and battery check C9 reruns exactly
those lines and compares against the recorded numbers, so they can never
silently rot. The candidate's 23,595 B figure stands unverified and
unreproducible (disclosed in Final point 1); the critique's own rerun
finding (default flags select nothing, 0 entries / 162 B) is encoded in
SEED_RIB.md as a warning line.

Bullet 4 (close the self-amendment loop). DONE. The load.order cap move
600 -> 1,100 is folded into the canonical B2-300 TOC
(watch/inbox/SEED_RIB_HANDOFF_KERNEL_20260926.md) as a dated, reasoned
amendment-log entry (full 64-hex sha256 seals for 7 rows cost ~450 B;
measured landed content 832 B), with the kernel-total ceiling 9,700 kept
as the binding cap and the caps-sum-vs-total semantics stated. The
directory-carrier semantics are folded into
watch/inbox/SEED_RIB_FORMAT_v0_20260926.md as the v0.1 amendment note
(file present + MANIFEST.sha256 = inline; POINTERS row = pointer;
kernel/law.heads.json = law_refs; JSON stays a build product). The battery
and the docs no longer disagree: C6 cites the amended caps, and the
amended docs are POINTERS-sealed rows in the tree (the tree was rebuilt
AFTER the doc edits so the seals cover the amended bytes; one figure in
the amendment log was corrected from 873 to the measured 832 B and the
tree rebuilt again for that, battery 14/14 after each).

Bullet 5 (make the three named-value rows checkable). DONE. C4b verifies
each against its live named source: git row vs `git rev-parse HEAD` +
`git branch --show-current` (byte-equal, PASS); verkle row vs
memory/warm_state.json chain.verkle_root + chain.index (PASS; the source
root is stored truncated by its writer, 19 chars, and the check prints
that fact); essentials row vs the dated non-VAULT pack file
watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc (1,706,469,664 B, sha256
82a4efed7745..., re-hashed in full by build and battery, PASS). The row
was also made concrete: it now carries the pack's real path, bytes and
sha256 instead of a prose pointer (first build accidentally sealed the
VAULT variant via sort order; caught by reading the battery detail line
and fixed before final landing).

Bullet 6 (wire L1-L5 into the build as a printed reduction report). DONE.
build_seed_rib.py measures every lever from the build's own bytes and
prints a REDUCTION REPORT: this build L1 VSCODE 1,340 B, L2 TOUR+SALON
3,108 B, L3 MORNING_LOOP 1,203 B, L4 ACCOUNTS 1,609 B, L5 kernel-cap
floor 232 B; L1-L4 cumulative 7,260 B; full path 7,492 B; over-budget
recovery names the lever set when a build exceeds the cap (0 B over this
build). The arithmetic is mechanical (freed = file bytes + its MANIFEST
row cost minus the added POINTERS row cost), and C10 independently
re-derives it from the tree on disk and fails on any drift vs the printed
report, so the path cannot rot into prose.

## Decision for the estate

The estate's seed carrier form is DECIDED and closed by this card: the
SEED-RIB carrier is a sealed DIRECTORY (seed_rib.v0.1 semantics re-homed:
file present + MANIFEST.sha256 = inline, POINTERS.sha256 row = pointer,
kernel/law.heads.json = law_refs), landed at
watch/inbox/seed_rib_20260926/seed-rib/ as the living seed; the
seed_rib.v0 JSON is a build product, not the carrier
(SEED_RIB_FORMAT_v0_20260926.md v0.1 note). The kernel cap law is
amended: load.order 1,100 B, kernel total ceiling 9,700 B binding
(SEED_RIB_HANDOFF_KERNEL_20260926.md amendment log). Rebuilds regenerate
stamps and state slices from live surfaces; when the law corpus or
load-order files grow, the battery fails loudly and the seed is rebuilt
by the co-landed script, never hand-edited. Open items this decision
leaves with named owners: universe rehydration drill on a second machine,
and the 3.3.0 re-merge when that pack ships; both recorded in the landed
receipt.
