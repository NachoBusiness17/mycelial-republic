# R6 - ARTIFACT IDENTITY: the build gets an ID, the pck gets a guard (2026-09-30)

Lane: R6 (Q09 / V2ASK2). Ownership: scripts/build_game.ps1 + roblox_to_godot
boot code + tests. Em-dash count: 0.

## Mission and the verdict it rode on

Q09 (V2ASK2.md): the artifact was unverifiable - built from the estate twin
(not the public tree), no sha at boot, swappable pck. The paid verdict
(results/V2ASK2.md, finish=content_filter) was CUT before its Q09 section
rendered; its reasoning tail names the design it was converging on: a
`verify.sh <tag>` that clones the public repo, rebuilds, hashes, compares
against a manifest, with pck-unpack diffing as the byte-reproducibility
fallback. This lane lands the manifest+stamp core of that (the identity and
the detection); the byte-reproducible rebuild + butler/wharf channel remain
the next lane's falsifier. Nothing here claims byte-reproducibility.

## What landed (all files byte-run, no hand-waved numbers)

1. `roblox_to_godot/core/boot_integrity.gd` - BootIntegrity autoload
   (registered in project.godot). Reads the exe's stamp trailer, hashes the
   pck beside it, prints `ARTIFACT_ID git=<sha> pck=ok|FAIL` to stderr;
   FAIL quits exit 1. Editor/source runs print `ARTIFACT_ID editor` and
   continue. Unstamped exports print `ARTIFACT_ID UNSTAMPED` and continue
   (fail-open by design: a stranger rebuilding via the editor still runs).
   Stamp lives in the EXE because any check inside the pck swaps with it -
   the exe is the half a pck-swap leaves behind.
2. Trailer format (PE overlay, loader-ignored, GDPC-safe): exe bytes +
   JSON payload + ASCII `MAGSTMP1` + u32 LE payload length as the FINAL
   4 bytes. Payload: v, git (source repo HEAD), pck_sha256, built, source
   (estate-twin|the-mountain), dirty_files when nonzero.
3. `scripts/build_game.ps1` v1: `-FromTheMountain` builds the-mountain/game/
   (default `<repo>\..\the-mountain`, `-MountainRepo` overrides) and stamps
   THAT repo's HEAD; default still builds the estate twin. Post-export:
   stamps exe (double-stamp canary), writes `mountain-manifest.json`
   (exe sha AFTER stamping, pck sha, git, boot_check) into the zip, runs a
   boot smoke of the stamped exe (`--headless --quit-after 2`, asserts
   exit 0 and pck=ok), zips, fresh-unzip gate now requires the manifest.
   PASS block prints the stranger's command.
4. the-mountain mirror (local commits `56be431` + `fa8b763`, NEVER pushed,
   per that repo's law): game/core/boot_integrity.gd byte-identical,
   [autoload] line added to game/project.godot (main_scene intentionally
   left at main.tscn - B14 title is the sync lane's set), export_presets.cfg
   copied so the public tree exports headless. Its tree was clean, so
   -FromTheMountain stamps dirty=0: the reproducible shape.
5. `roblox_to_godot/README.md`: "Verify the build artifact" section with
   the stranger's commands; core/ placeholder line corrected.

## Byte-run proofs (2026-09-30, this session)

- Estate build: `[5b] stamped exe: git=9791c757c ... source=estate-twin,
  dirty=12` (dirty = this lane's uncommitted files, honestly stamped);
  `[5d] ARTIFACT_ID git=9791c757ca0f... pck=ok`; PASS exit 0.
- -FromTheMountain build: `git=56be4311f ... source=the-mountain, dirty=0`;
  boot smoke pck=ok; zip mountain-56be4311f-mt.zip.
- Swap test (the Q09 threat): append 1 byte to the pck -> exe prints
  `pck=FAIL pck sha256 8ddf9f0a... != stamped ff72cfee... (SWAPPED PCK)`
  and exits 1; restored -> `pck=ok`, exit 0.
- Stranger's command, verbatim from the build output, run twice from the
  unzipped folder: intact -> `MOUNTAIN OK estate-twin <sha>`; pck byte
  appended -> `MOUNTAIN FAIL estate-twin <sha>`. Restored pck re-matches
  mountain-manifest.json (crosscheck True).
- The stamp tracks a moving HEAD: pytest's rebuild stamped `600b09c4b`
  after a sibling lane committed between builds, and the test asserted
  stamp.git == rev-parse HEAD at run time. Zips: mountain-600b09c4b.zip,
  mountain-9791c757c.zip, mountain-56be4311f-mt.zip (build/ is gitignored).

## The stranger's verification command

From the unzipped mountain zip folder (no Godot, stdlib only):

    python -c "import json,hashlib;f=open('TheMountain.exe','rb');f.seek(-4,2);L=int.from_bytes(f.read(4),'little');f.seek(-12,2);m=f.read(8);f.seek(-12-L,2);s=json.loads(f.read(L));p=hashlib.sha256(open('TheMountain.pck','rb').read()).hexdigest();print('MOUNTAIN',('OK' if m==b'MAGSTMP1' and p==s['pck_sha256'] else 'FAIL'),s['source'],s['git'])"

or run it: `TheMountain.exe --headless --quit-after 2` (expect
`ARTIFACT_ID ... pck=ok`, exit 0; swapped pck = FAIL line + exit 1).
The printed git sha + source says which tree built it; check that sha out
of the public repo to rebuild the same source.

## Tests (instrument, moment, delta named - census law)

`tests/test_build_artifact_id.py`, 5 tests, real pipeline run per session:
stamp pins HEAD + pck sha; manifest agrees with bytes; boot prints identity
exit 0; swapped pck -> exit 1 + SWAPPED PCK + restore -> exit 0
(specificity); missing pck -> engine-level detection (named boundary:
Godot 4.3 prints "Is the .pck file missing?" then hangs instead of exiting;
the autoload cannot fire because it lives inside the pck - the test asserts
no silent run + the engine error, and kills the hang). First run: 4 passed,
1 failed on the missing-pck timeout (the boundary above, found by running
it); after the fix: 5 passed in 46.27s (pytest -q, estate venv, 23:2x EDT).
Collect-only: 5 in this file (0.62s). Full-suite collect at the same
evening read 3,835 collected in 14.16s clean; an earlier read minutes
before showed 3,750 + 3 transient collection errors (sibling lanes
mid-write; not this file - mine collected clean in both). The AGENTS.md
census bullet was NOT touched: its refresh is the drift patrol's
instrument, and 2,303/352 (2026-09-27) staleness is pre-existing estate
drift, named here rather than papered over.

## Named boundaries and next lanes

- Missing pck: engine hangs without exit code (4.3 defect); detection is
  the error line, not a code. An exe-side guard would need a wrapper.
- Unstamped exe runs (loud). Fail-closed would break editor-exported
  rebuilds, the stranger's own path; revisit only if the release process
  mandates pipeline-only artifacts.
- `--main-pack other.pck` substitution: caught by the pck-missing branch
  (the substituted pack's autoload finds no exe-beside pck) - noted in
  the autoload comments, not separately tested.
- Byte-reproducible rebuild + butler/wharf channel + release-page manifest
  publication: the V2ASK2 falsifier, still open (next lane).
- The estate twin stays uncommitted per lane law; the-mountain has the two
  local commits above for the operator to push.

## Status

ARTIFACT NOW CARRIES ITS ID. Source sha + pck sha pinned in the exe at
build time, printed at boot, guarded at run, checked offline by one
stdlib command, buildable from the public tree with -FromTheMountain.
