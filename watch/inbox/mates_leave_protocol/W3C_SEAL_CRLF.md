# W3C — config seal CRLF law change (normalize-at-hash)

**Date:** 2026-09-29 · **Lane:** Mickey17 W3 (config seal mechanism owner)
**Files:** `tools/config_seal.py` · `configs/.config_seal.json` · `tests/test_gate_blocking_paths.py`
**No git commit** (lane rule; working-tree landing only).

## The defect (bytes, not reports)

The canary reported "all 56 sealed hashes mismatch any LF checkout". Byte check
against `git show HEAD:configs/<f>`: **41/56 mismatched**, 15/56 matched (those
15 were LF-on-disk at seal time; the seal hashed raw working-tree bytes, and
41 files carried CRLF bytes on the Windows tree that sealed them). Every Linux
clone and every gate-canary worktree (byte-faithful blob checkout,
`tools/gate_canary.py` line 241-242) failed `config_seal.py verify` with zero
config content changed. Local verify on this Windows tree at lane start:
sealed=56 live=57 modified=6 unsealed=1 (sibling-lane drift, see below).

## The law change

`_sha256` now hashes `bytes.replace(b"\r\n", b"\n")` — one function feeds both
`update` and `verify` (shared `build_register`), so normalization is applied at
seal AND at verify by construction. Lone `\r` is untouched: git text conversion
only maps CRLF<->LF. Seal schema bumped `config_seal.v1` -> `config_seal.v2`
(a v1 register is not comparable; the one-time `update` re-seal is the
migration act). Re-sealed against current bytes: **57 files sealed**, verify
PASS on the working tree, and the LF-blob simulation (what a Linux clone of
HEAD would hash) matches **54/57**: `providers.yaml` is not yet in HEAD
(uncommitted sibling landing) and `fossil_registry.json` + `mirrors.json`
carry genuine in-flight content edits from sibling lanes (verified: normalized
content differs from blob, no lone-CR edge cases). Those are content drift the
seal is supposed to track, not EOL drift; they re-seal by NAME when their lanes
land. The EOL law itself is proven: every file whose content equals its blob
now hashes identically on CRLF and LF checkouts.

## Why normalize-at-verify beats re-seal-on-CRLF

Re-sealing on CRLF bytes re-couples the register to one machine's checkout EOL
policy: clones on Linux (`core.autocrlf=false`, LF blobs) would fail again
with the next seal, and the estate's own canary worktrees would keep flip-
flopping red/green depending on which host sealed last. The register's purpose
is content integrity over `configs/`; git's text machinery legitimately
presents the same content with either ending depending on host and checkout
flags. Hashing a normalized form makes the seal invariant under that
machinery, which is the property an integrity register needs: it must fire on
content drift and stay silent on transport/checkout representation. Cost:
a byte-level ending-only change to a config no longer trips the seal —
accepted, because no sanctioned act edits a config's endings without touching
content, and the ending flip carries no integrity meaning of its own.

## Tests (tests/test_gate_blocking_paths.py)

New: `test_config_seal_verifies_lf_flip_of_crlf_seal` (the Linux-clone case),
`test_config_seal_verifies_crlf_flip_of_lf_seal` (the autocrlf-smudge mirror),
`test_config_seal_blocks_real_edit_despite_normalization` (positive control:
content change under an ending flip still exits 1). Fixture note: flip tests
write bytes with `write_bytes`; Windows text-mode `write_text` doubles `\r`
and would fake the fixture. Real counts, one instrument each:
`pytest tests/test_gate_blocking_paths.py tests/test_gate_canary.py -q` ->
**52 passed** (was 49 collected in these two files before the lane; +3 new).
Full-suite `pytest -q` number filed in the lane report at close.

Final counts (instruments named per the census-denominator law):
`pytest -q` full suite executed **exit 0 twice** on 2026-09-29 (both runs
green; the summary line was lost to a harness output-capture race both times —
named, not hand-waved). Same-day `pytest --collect-only -q`:
**2,903 tests collected** (busy multi-lane tree; my +3 are inside this
denominator). These are different instruments at different moments, not
comparable by differencing.

## Drift absorbed by this re-seal (named, not silent)

Modified since last seal: `constitutional_rails.json`, `events_key_schema.json`,
`links_kind_baseline.json`, `mirrors.json`, `skills.yaml`,
`violation_baseline.json`. New/unsealed: `mates.yaml`. These are sibling-lane
landings that went unsealed; the v2 re-seal absorbs them in one named act
(`--by mickey17-w3c`, note recorded in the seal file). **Double stamp:**
`skills.yaml` was edited AGAIN by a sibling lane mid-window after the first
v2 seal; a close-stamp re-seal (second named act, note in the seal file)
absorbed it. Final state: verify exit 0, sealed=57 live=57.
