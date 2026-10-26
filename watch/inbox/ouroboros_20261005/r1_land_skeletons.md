# R1 LAND: SKELETON AMENDMENTS (rows 2 + 4) - 2026-10-05

Filed by the R1-landing lane of the ouroboros night loop. Executes amendment
rows 2 and 4 of watch/inbox/ractor_engine/2026-10-05-ouroboros-r1-fleet/
SYNTHESIS.md against the three thrice-reused mickey17-family skeletons.
Edit tool only on the .dwf.ts files; tools/ and mag/ untouched (live
workflow owns them); no git commit. No em-dashes in anything this lane
wrote (grep-verified over every inserted line).

## Path note (read before auditing)

The task named .zcode/workflow-drafts/mickey17-v2.dwf.ts, which does not
exist. The real file is .zcode/workflows/mickey17-v2.dwf.ts (the saved
workflow), and its pre-edit line numbers match the SYNTHESIS row 2
citations exactly (tier-1 persist at :145-146, tier-2 merge at :278-284,
estate-filer at :349-353), so that file is what was edited. The other two
targets were at their named draft paths.

## ROW 2: tier-1 merge clause (E26 data-destruction vector) - LANDED x3

The tier-1 supports-check persist instruction in supportsAsk() now carries
the merge law in all three files, byte-identical wording, verified by grep
(1 hit per file, phrase contiguous on one line):

  "Read the file first if it exists; keep every existing key verbatim
  (including deep_tier2); replace only lane/supports/counts"

- .zcode/workflows/mickey17-v2.dwf.ts:152 (was :145-146)
- .zcode/workflow-drafts/read-the-estate.dwf.ts:164 (was :155-157)
- .zcode/workflow-drafts/execute-register.dwf.ts:150 (was :143-144)

Each insert names the tier-2 persist as the law it mirrors and the E26
defect it cures (a refire tier-1 rewrite destroying persisted deep_tier2
verdicts). First refire after this landing is protected in-flight.

## ROW 4: run manifests + definition tracking - LANDED x3

Every estate-filer ask now files the run interface record (the E22 cure):
(d) copy the running script bytes to runs/<slug>/RUNNER.dwf.ts
(Read whole, Write byte-identical, mkdir -p first) and (e) write
runs/<slug>/manifest.json beside the lane archive with exactly
{topic, width, lanes, fired, script_path, moment} (moment = UTC ISO 8601
at write; ALL FILED only if both landed). New consts feed it:

- mickey17-v2: RUNROOT :90, SCRIPT :95 (points at the saved workflow),
  filer extension :358-368
- read-the-estate: RUNROOT :90, SCRIPT :95 (draft path), filer extension
  :365-375; exec has no WIDTH const so width = the fired lane count
- execute-register: RUNROOT :78, SCRIPT :83 (draft path), filer extension
  :337-347

RUNROOT refactor: LANES = RUNROOT + "/lanes" in all three (grep: 1 hit
each); the fold wrapper still receives (fired-count, run-slug) unchanged.

### Slug suffix decisions (evidence, not preference)

- read-the-estate :89: targets-length suffix DROPPED. Provably vestigial:
  its schema declares only period + slug (no targets), so the formula
  minted "-0" on every fire. Comment updated to match (no orphan prose).
- mickey17-v2 :89: targets-length suffix KEPT. Not vestigial there: the
  schema declares targets (required json), the count is real, and the
  archive comment :85-88 documents runs/<topic-slug>-<laneCount>/ as the
  dwfrun-6d6dfd07 cure (the fixed global dir folded 89 lanes / 459 rows
  across two runs). Dropping it would recollide same-topic
  different-width refires, the exact disease the comment receipts.
- execute-register :77: no targets-length suffix existed; the "-exec"
  discriminator is functional (separates exec fires from read fires in
  the shared runs/ tree) and was not touched.

### The read-the-estate "no targets passed" throw: KEPT, with cause

Verification per instruction: the lane table literal ALL (12 rows) is
unconditionally non-empty, but TARGETS = ALL.slice(0, WIDTH)
(read-the-estate:124) honors an undeclared args.width
(:108: typeof args.width === "number" ? args.width : 12), so a width of
0 or less empties the slice and reaches the throw (:125-127). The throw
is therefore NOT unconditionally dead and stays. (Making it dead would
mean pinning WIDTH or guarding width < 1, which is row 3
parameterization work, not row 4.) mickey17-v2 and execute-register
throws also untouched (out of scope; mickey17-v2's is live - targets is
a declared arg that can arrive empty).

## GATES (all numbers, .venv interpreter)

prepush_workflow_metadata.py: "WORKFLOW-METADATA: ok - scanned 87
workflow file(s) (22 without a metadata block, skipped), 0 finding(s)
(0 accepted by name)" EXIT=0.

workflow_gate.py check --script (verdict / digest / exit):
- .zcode/workflows/mickey17-v2.dwf.ts: PASS 729b053f2b70 EXIT=0,
  8/8 gates ok (G6 ok via its source-fetched: 2026-09-26 stamp)
- read-the-estate.dwf.ts: PASS a441aa9d3cd9 EXIT=0, 7 ok + 1 soft WARN
  G6-receipts (no dated stamp label; pre-existing, soft rows never block)
- execute-register.dwf.ts: PASS cc27c6e1e631 EXIT=0, 7 ok + 1 soft WARN
  G6-receipts (same pre-existing class; this lane added no stamp lines)

Both WARNs predate this sitting (neither file ever carried a
source-fetched-style stamp); the 0/1/2 exit contract was untouched.
Three PASS registry rows minted at memory/workflows/REGISTRY.jsonl,
ts 2026-10-05T10:41:18Z (one per script, digests above).

## Honest residue

- git status shows .zcode/workflows/the-gala.dwf.ts modified: NOT this
  lane (zero Edit calls targeted it; pre-existing working-tree state from
  a sibling lane). This lane's three targets are gitignored wholesale
  (.gitignore:198), which is itself SYNTHESIS row 4's finding: the
  RUNNER.dwf.ts + manifest.json convention is the stopgap until the
  operator decides the git add -f exception.
- The manifests land on the NEXT fire of each script, not retroactively;
  the in-flight 2026-10-05-exec run still has no manifest.
- Not done here (owned elsewhere): row 1 fold-script fix, row 3
  parameterized burn, git tracking decision, spec port (row 10).
