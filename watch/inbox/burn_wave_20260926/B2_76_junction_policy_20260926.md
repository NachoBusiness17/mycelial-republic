# B2-76 Catalog v3 junction policy · 2026-09-26

## Verdict

LANDED. The junction handling that the 2026-09-18 inline v3 walk did as a
one-off (catalog 946,773 to 757,667 rows, delta -189,106, "v3 walk:
junction-pruned") is now codified policy in the catalog scanner itself:
mag/catalog_scan.py carries the XIDIG-WIN law as its module spec (P1-P5),
prunes reparse-point directories at walk time, emits every reparse point to
a new ledger catalog/junctions.jsonl with target classification, and the
seam where the -189,106 story was Unproven (duplicate vs intentional mount)
is now instrumented instead of folklore. The gap row's Windows/storage law
(watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md:23) moves from "reparse-point
handling owed" to "policy landed, junction diff runnable". The MFT
fast-refresh half of that row is spec-cited, not coded; it is self-fed as
B2-331. 9/9 junction-policy tests pass, violation ratchet PASS with NEW=0.

## Evidence

- Law bytes, verified-live LINKS rows (watch/inbox/LINKS.jsonl lines 327-331,
  ts 2026-09-26T11:53:49Z, writer x-intel-dig):
  XIDIG-WIN-REPARSE-LAW (reparse data incl. tag and GUID <= 16 KB; 63 reparse
  points per path, 31 when the target is fully qualified; a directory must be
  empty to take a reparse point), XIDIG-WIN-JUNCTION-RULES (junctions link
  directories only, may cross local volumes, may NOT reference mapped network
  volumes or files, implemented through reparse points), XIDIG-WIN-SYMLINK-RULES
  (a symlink MAY target a remote UNC path directly; relative symlinks are
  restricted to a single volume), XIDIG-WIN-MFT-ENUM + XIDIG-WIN-USN-REFRESH
  (the fast-refresh path, spec-cited only in this lane).
- The 189K story, from filed bytes: catalog/TAG_REPORT.md:3 "757,667 rows,
  v3 walk: junction-pruned, deduped, fresh";
  watch/inbox/CORPUS_MAP_SALON_20260918.md:400-405 "one reparse point found
  at local_sovereign_agent/training - v2 walked junctions and counted
  duplicate trees, v3's confinement prunes them. Full attribution of the
  delta to junctions = Unproven"; SOCRATIC_GAPS_20260918.md:40 "You pruned
  189K rows through a junction and called them duplicates" and :102 the
  falsifier "A junction diff showing only byte-duplicate trees would
  falsify the intentional mirror worry".
- Live probe (B2_76_junction_probe.py -> B2_76_junction_probe_results.json,
  2026-09-26T15:57:37Z): exactly one pre-existing reparse point in the whole
  estate root: local_sovereign_agent/training, tag 0xA0000003
  (IO_REPARSE_TAG_MOUNT_POINT), dir, target
  \\?\C:\Users\foste\Documents\projects\local_sovereign_agent\memory\training.
  The probe's own naive UNC check (startswith backslash-backslash) misread
  that device path as network; the shipped classifier encodes the correct
  split (device_local = win32 device namespace, local volume, NOT network),
  which is exactly the trap a junction policy has to get right.
- Codified-policy verify on live bytes (B2_76_scan_verify.py ->
  B2_76_scan_verify.json, 2026-09-26T16:15Z, full scan_tree walk of the
  catalog root, read-only): 485,998 rows, 0 in-walk dups, 5 reparse points,
  all pruned, 0 rows emitted under the local_sovereign_agent/training/
  prefix, the real junction recorded target_class device_local,
  violation false, action pruned. The other 4 records are junctions this
  lane's own pytest runs created moments earlier inside agents/pytest-tmp-*
  trees; the policy sees and records its own test residue, which is the
  ledger doing its job.
- Row-count drift attributed with bytes, not vibes. Live walk 485,998 vs
  filed 757,667 is -271,669, and junction pruning accounts for at most 28
  rows of it (24 files under memory/training today, plus the 4 tmp
  junctions). The mass holders shrank on disk between Sep-18 and today:
  memory/biography_backup 212,530 -> 68,202 files, memory/ghost
  142,269 -> 16,407, memory/biography_backup_20260825 42,249 -> 0,
  memory/runs 42,626 -> 47,281, memory/biography 39,189 -> 44,365; the five
  deltas sum to -302,608, more than the whole gap. The Sep-18 catalog is
  estate truth, not walker truth; self-fed B2-332 owns the refresh.
- Tests: tests/test_catalog_scan_junctions.py, 9 passed (.venv python
  3.11.15): six classifier laws including device-local-is-not-network and
  the over_cap 16 KB check; a real-junction walk test via
  _winapi.CreateJunction proving the mirrored tree counts exactly once at
  its real path with the junction recorded (the v2 disease, dead); the
  junction-to-file rule firing as violation; the symlink/junction UNC split
  (same target class: contrast note for a symlink, violation for a
  junction). Ratchet: python tools/violation_ratchet.py check --changed ->
  scope=16, hits=14, registered=14, NEW=0, PASS.

## Work done

Spec first: mag/catalog_scan.py's module docstring is now the owning spec
(history, the three law families with their LINKS ids, and consequences
P1-P5), written into the module in the same edit as the code so no orphan
behavior. Code: v2 -> v3. P1 every kept directory entry is lstat-checked;
a reparse point is recorded to catalog/junctions.jsonl and pruned from
os.walk traversal (Python 3.11 walk does not treat junctions as links; that
gap is how v2 double-counted). P2 a reparse-point FILE is recorded and
emitted from lstat bytes, never followed, never opened for a title (UNC
hang risk; the reparse payload is not content). P3 targets are classified
device_local / local_volume / unc_remote / relative / over_cap; unc_remote
or over_cap on a junction flags violation, the same class on a symlink
carries the contrast note. P4 the 63/31 limits are documented bounds, not
dead branches: pruning means a walked path holds at most one reparse
component. P5 rows dedupe by relpath per walk with the count reported.
Also fixed against its own docstring: v2 claimed machinery dirs were
"COUNTED in the summary" and never counted them; v3 counts them (1,010 in
the verify walk). Row schema of catalog.jsonl is unchanged and write mode
stays append; the atomic-replace rebuild stays an operator-invoked flow
per the salon receipt. Not done, on purpose: MFT/USN enumeration is not
implemented (the scanner still os.walks); that is B2-331. Landed artifacts:
mag/catalog_scan.py (v3), tests/test_catalog_scan_junctions.py,
catalog/junctions.jsonl (created on first scan run; empty until then),
B2_76_junction_probe.py + results, B2_76_scan_verify.py + results, this
receipt, LEDGER row, QUEUE self-feeds B2-330/331/332, INDEX registration.

## Falsifier

Fired and survived: the live-junction walk test reproduces on every run
(each pytest run mints fresh junctions in its own tmp tree; the walker
pruned every one); the estate verify walk found the real junction and
emitted zero rows under its prefix. The verdict dies if: (a) os.walk
semantics change so that pruning names from dns stops preventing descent
(the prune is re-verified per Python version; it is attribute-based, not
islink-based, so 3.12+ isjunction additions do not touch it); (b) a
junction with a UNC or over-cap target ever folds into junctions.jsonl
without violation=true (test pins the junction/symlink split); (c) the
B2-330 diff, once run, shows the training target tree is not a
byte-duplicate of what the walk counted, which would reopen
duplicate-vs-intentional-mount as a live mirror and demand a catalog
decision, not a prune preference. Disclosed: full attribution of the
2026-09-18 -189,106 delta remains Unproven by design (the old catalog was
replaced before a diff could run); this lane makes the diff runnable and
attributes today's live-vs-filed drift to measured estate churn, not to
the junction.

## Bibliography closed

watch/inbox/LINKS.jsonl:327-331 (XIDIG-WIN-*, verified-live);
watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md:23; catalog/TAG_REPORT.md:3;
watch/inbox/CORPUS_MAP_SALON_20260918.md:397-405;
watch/inbox/SOCRATIC_GAPS_20260918.md:38-42,95-104;
mag/catalog_scan.py (v2 bytes pre-edit, v3 landed);
mag/catalog.py (read, unchanged, separate surface);
scripts/index_fold_host.mjs (registration law, read);
mag/shared_surface.py (living-file law, read);
memory/burns/LEDGER.jsonl (append target); QUEUE.md law block (claim law
checked: mag/catalog_scan.py was committed-clean, no CLAIM needed). This
lane: B2_76_junction_probe.py, B2_76_junction_probe_results.json,
B2_76_scan_verify.py, B2_76_scan_verify.json,
tests/test_catalog_scan_junctions.py, catalog/junctions.jsonl, this
receipt. Closed 2026-09-26.
