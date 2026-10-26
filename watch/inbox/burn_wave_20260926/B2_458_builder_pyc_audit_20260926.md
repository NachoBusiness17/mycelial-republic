# B2-458 Builder pyc-exclusion audit (SW-07, 2026-09-26)

## Verdict

CONFIRMED WIRED (audit brief; the author-path exclusion and the gate ordering both live in the builder code, verified on bytes plus a measured probe). tools/seed_v2.py: (a) purges `seed/**/__pycache__/` directories and excludes `*.pyc`/`*.pyo` and any `__pycache__` path from the seal walk, so zero .pyc rows can enter MANIFEST.sha256; (b) the zip is emitted from the `sealed` row list plus the manifest itself, so zip contents equal seal contents by construction and a stray loose .pyc can never ship either; (c) `cold_boot_test.gate()` runs after the MANIFEST write and before the first zip byte, and a blocked gate raises SystemExit (nonzero) before any zipfile is opened, emitting no zip.

## Evidence file:line quotes

- Build book spec, watch/inbox/SEED_V2_BUILD_BOOK_20260925.md:175 "SPEC: PYC EXCLUSION AT SEAL ... Excluded from collection: any path under `__pycache__/`, plus `*.pyc` / `*.pyo` anywhere in the seed tree. Purge before seal ... Purge-only is not enough ... and exclude-only is not enough" and :203 "SPEC: PRE-ZIP COLD-BOOT GATE ... run `tools/cold_boot_test.py::gate()` between the seal and zip emission ... On block, the builder exits nonzero naming the blockers and emits no zip".
- tools/seed_v2.py:908-910 purge arm: `for cache in sorted(SEED.rglob("__pycache__")): if cache.is_dir(): shutil.rmtree(cache)`; :911-916 walk arm: `if not f.is_file() or f.name == "MANIFEST.sha256": continue` / `if f.suffix in (".pyc", ".pyo") or "__pycache__" in f.parts: continue`; :920 MANIFEST written; :931-934 `gate_ok, gate_line = cold_boot_test.gate()` / `if not gate_ok: raise SystemExit(f"seed_v2: pre-zip gate BLOCKED zip emission - {gate_line}")`; the zipfile block (:936+) sits strictly after that guard and writes members `sorted(sealed + [SEED / "MANIFEST.sha256"], ...)`.
- tools/cold_boot_test.py:69-76 `def gate() -> tuple[bool, str]` docstring: "ok is False when any check ends CRASH, ERROR, or TIMEOUT" with the t28 cause comment; the suite runs in a temp copy so nothing executes inside seed/.
- Measured probe (spec-correct synthetic tree with engines/cooker.py, engines/__pycache__/cooker.cpython-311.pyc, stray.pyc, ok.md): sealed rows == ["engines/cooker.py", "ok.md"], zero pyc/pyo/__pycache__ entries in manifest lines, and the zip membership list (sealed + MANIFEST) contains no pyc -- "probe v2 PASS". A first probe run mis-asserted that loose stray.pyc is deleted from disk; the spec only purges __pycache__ dirs and relies on the walk exclusion for strays -- the builder matches the spec, the probe assertion was wrong and is corrected here.

## Work done

- Read the two SPEC sections whole and the corresponding builder bytes; ordered the seal -> gate -> zip flow from source.
- Ran the synthetic-tree probe proving both exclusion arms and the zip-membership derivation; no production build was fired (the audit is code-order + probe, per the brief's "confirm both are wired in code").
- Named the one nuance for the next auditor: loose *.pyc strays are excluded from seal and zip but not deleted from the author tree; that is the spec's own design (exclude-only for strays, purge for pycache dirs), not a gap.

## Falsifier

The brief's falsifiers: "a rebuild whose manifest contains any .pyc row, or a code path that emits the zip when gate() returns False". Both are falsified by the quoted code order (SystemExit precedes the zip block; the walk filter precedes the manifest write) and the probe. Reopen if: seed_v2.py gains a zip/members path that bypasses `sealed`, or the gate call moves after the zipfile open, or the walk filter loses an arm.

## Bibliography closed

Read: watch/inbox/SEED_V2_BUILD_BOOK_20260925.md (both SPEC sections whole), tools/seed_v2.py (seal/gate/zip region), tools/cold_boot_test.py (gate() contract), probe transcripts (both runs, including the corrected mis-assertion). No external sources.
