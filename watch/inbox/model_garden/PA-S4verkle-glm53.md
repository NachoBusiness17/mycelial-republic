# PA-S4verkle-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# STRANGER AUDIT, SURFACE 4: THE VERKLE CHAIN

**Citation convention:** the evidence bundle was replayed with head/tail truncation and carries no line numbers, so every citation below is `file :: quoted bytes (line UNVERIFIED)`. Bytes quoted are verbatim from the bundle; anything I could not quote is marked UNVERIFIED outright.

**Instrument/moment assumptions for every verdict below:** SHA-256 Merkle list per `00__verkle_knot.py :: "_merkle_root"`; chain state = live bytes on disk at audit moment 2026-10-01; witness = the single gist per `02__tip_witness.py :: "Gist law: ONE gist"`; adversary = write-capable insider ( filesystem write access, holds whatever keys the estate holds) or a tool bug with the same write power. I do NOT assume the adversary controls GitHub or the operator's PAT.

---

## (1) ATTACK SURFACE MAP

### 1a. The tip witness is a tip hash only. Interior rewrites with a recomputed tip: is that true here?

**Yes for count-preserving rewrites, NO for count-growing rewrites. Proof from the code:**

The witness compares exactly two fields, `02__tip_witness.py :: compare()`:

```
if witnessed["root"] == live["root"] and witnessed["n_leaves"] == live["n_leaves"]:
    return ("WITNESS-MATCH", ...
if live["n_leaves"] > witnessed["n_leaves"]:
    return ("WITNESS-LAG", ... "(normal growth; publish due)")
if live["n_leaves"] < witnessed["n_leaves"]:
    return ("WITNESS-DIVERGENT", ... "chain SHRANK")
return ("WITNESS-DIVERGENT", ... "same count ... but root differs")
```

`live` is read from `verkle_tip.json` (`load_tip()`), which the adversary also rewrites. The design's own docstring states the ratchet: `02__tip_witness.py :: "the witness only ADVANCES on leaf-count growth, never backward (shrunk chain) and never sideways (same-count root change)"`.

Attack T1 (count-preserving interior rewrite): amend 33% of rows per the chain's own admission `00__verkle_knot.py :: chain_mode() :: "v1 (default): amend-in-place - a re-save of an existing session replaces its row and rewrites the WHOLE chain file ... 2,821/8,626 rows were amend rewrites"`, recompute all `verkle_root` fields, rewrite `verkle_tip.json` via the same `_write_tip_atomic` the repair tool uses (`01__chain_repair.py :: "_write_tip_atomic(tip)"`). Result: `n_leaves` unchanged, root in tip matches rewritten chain. Witness verdict: same-count root differ = DIVERGENT - **the witness fires, but it fires on EVERY legitimate amend too**. This is the fatal ambiguity: the design has 2,821 amend rewrites in the live chain, and every one of them (before any publish) produces the same signal as laundering. Detection collapses into noise. (Publish pending the PAT scope denial: `02__tip_witness.py :: "the current fine-grained PAT has gist READ but gist WRITE denied"`.)

Attack T2 (the real hole): interior rewrite **plus one appended leaf**. `live["n_leaves"] > witnessed["n_leaves"]` = WITNESS-LAG = "normal growth; publish due". The operator's own next action - `--publish --go` - advances the gist onto the forged root. **The witness is not merely blind to T2; the adversary launders THROUGH the publish path.** Proven from the quoted `compare()` bytes above; no other check exists between chain and gist (the docstring disclaims it: `02__tip_witness.py :: "tip-vs-chain consistency is AG5's job, not recomputed here"`).

Attack T3 (tool-bug class, already happened twice): `01__chain_repair.py :: "concurrent append from a long-lived process running OLDER verkle_knot code ... computes its committed root from a pre-race leaf set"`. The repair tool's own cure **rewrites historical rows in place**: `bad["verkle_root"] = true_root; bad["parent_verkle_root"] = true_parent` then `tmp.replace(CHAIN)`. `true_root` is computed from the row bytes as found: `hashes = [str(r["leaf_hash"]) for r in rows if r.get("leaf_hash")]` - **the repair tool trusts `leaf_hash` bytes unconditionally**. A buggy or malicious writer that corrupts a leaf's `leaf_hash` (not its `verkle_root`) makes `_verify_chain_consistent` fail, and repair then launders the corrupted hashes into the committed roots and stamps `chain_race_repaired` as cover.

Attack T4 (lock surface): `verkle_lock` breaks locks held by dead PIDs, including on ambiguous Windows errors: `00__verkle_knot.py :: "except OSError: # Windows may report a generic missing-process error. stale = True"`. An insider who can signal-kill the legitimate holder (or any process on a Windows build surfacing SystemError) breaks the lock mid-rewrite and re-enters. Also `LOCK.unlink()` on the stale path is itself a write an insider can force by touching the lock file's mtime backward.

Attack T5 (grounding wave, the anchored rows): the wave is a self-referential jsonl with genesis `"0" * 64` (`03__grounding_wave.py :: GENESIS`). Every G1-G3 gate runs at WRITE time against the same tape the adversary can rewrite: full-tape rehash + tip-free = undetectable in-repo. `_HEX64`, `_KIND_KEYS`, the admission ladder - all verified by code reading the same mutable file. No external checkpoint exists for `GROUNDING_WAVE.jsonl` at all (nothing in the bundle references one).

### What the witness WOULD catch vs miss

| Rewrite | Witness verdict | Caught? |
|---|---|---|
| Shrink chain (delete rows), no tip forge | DIVERGENT (shrunk) | YES |
| Same-count interior rewrite, tip NOT forged | DIVERGENT (sideways) | YES (but indistinguishable from any unpublish amend - noise) |
| Same-count interior rewrite, tip forged | MATCH | **NO** |
| Interior rewrite + 1 appended leaf | LAG, then ADVANCED on publish | **NO - laundered through the ratchet** |

---

## (2) THE 3 WEAKEST JOINTS (ranked)

**J1 - Witness count-ratchet laundering (T2).** `02__tip_witness.py :: compare() :: "if live['n_leaves'] > witnessed['n_leaves']: return ('WITNESS-LAG'...)"`. The single external checkpoint the design offers is bypassed by any rewrite that also appends one row, and the operator is prompted to sign the result.

**J2 - Repair tool trusts leaf hashes and rewrites history in place (T3).** `01__chain_repair.py :: "hashes = [str(r['leaf_hash']) for r in rows if r.get('leaf_hash')]"` feeding `bad["verkle_root"] = true_root`. The incident-response path is itself an undetectable history-mutation channel.

**J3 - Grounding wave has no external witness at all (T5).** `03__grounding_wave.py :: GENESIS = "0" * 64` with verify() reading `LEDGER = ROOT / "watch" / "GROUNDING_WAVE.jsonl"` - full-tape rewrite recomputes every `prev`/`hash` and passes G1-G3 because the gates check the tape against itself.

---

## (3) PATCH SPEC (the landable deliverable)

### PATCH-J1: per-era witness lattice (fixes count-ratchet laundering)

In `tip_witness.py`, stop witnessing one tip; witness era checkpoints.

Spec:
1. Every time `live.n_leaves` crosses a multiple of `ERA=256`, the publish path writes an ADDITIONAL immutable gist line: `MAG-TIP-ERA.v1 era_start=<n0> root=<root-at-era> n_leaves=<n0+256> ts=<ISO>` to a SECOND, create-only gist (PATCH once, never patched afterward; era k+1 goes to a new gist). Creation-only gists are append-only in the witness layer, defeating the "append one forged leaf and publish" move: the forged tip cannot reproduce the era roots that sit in earlier create-only gists, because those roots are over the ORIGINAL leaf set at counts the adversary's forged chain cannot match without shrinking (which trips DIVERGENT).
2. `verify` gains era checks: for each published era gist, recompute `_merkle_root(leaf_hashes[:n0+256])` from the live chain and compare. Any era mismatch = DIVERGENT regardless of tip.
3. Falsifier: forge a chain that is one leaf longer than the last witnessed count, with 300 rewritten interior rows, publish, run `--verify`. Current code: WITNESS-ADVANCED, exit 0. Patched code: era-0 mismatch, DIVERGENT, exit 1. The test is a 10-line pytest with the existing injectable `Transport` (`02__tip_witness.py :: "Transport = Callable[[urllib.request.Request, int], tuple]"`).

### PATCH-J2: repair tool must not launder leaf hashes

In `chain_repair.py`, before any rewrite:
1. Re-derive each leaf hash from its knot source of truth: `recomputed = _leaf_hash(json.loads((KNOTS / r["filename"]).read_text()))` and require `recomputed == r["leaf_hash"]`; any mismatch = refuse with a new exit code 3 listing filenames (`_leaf_hash` exists at `00__verkle_knot.py :: "def _leaf_hash(obj)" :: "return _h(b'leaf:' + raw)"`).
2. Write a pre-repair frozen copy: `CHAIN.with_suffix(".jsonl.prerepair.<ts>")` before `tmp.replace(CHAIN)`; never GC these. Today a repair destroys the only pre-repair bytes (`01__chain_repair.py :: "tmp.replace(CHAIN)"` is the sole write; no backup exists in the quoted code).
3. Post-repair, require the operator to run `tip_witness --publish --go` in the same incident runbook so the repair era is externally checkpointed (ties into PATCH-J1).
4. Falsifier: corrupt one row's `leaf_hash` in a test fixture, run `chain_repair`. Current code: exit 0, corrupted hash committed into `true_root` with a `chain_race_repaired` stamp. Patched code: exit 3, no write.

### PATCH-J3: anchor the grounding wave into the verkle tip witness

1. Extend `_KIND_KEYS["checkpoint"] = ("prev", "ts", "kind", "wave_root", "wave_n_rows", "seat")`; a cron-less standing verb (per `03__grounding_wave.py :: "files not processes; chain-side append, nothing scheduled"`, compute it inside `verify()`) appends a checkpoint row carrying `_merkle_root` over `GROUNDING_WAVE.jsonl` row hashes.
2. Publish the wave root alongside the verkle root in the era gist (PATCH-J1): `MAG-TIP-ERA.v1 ... wave_root=<hex> wave_rows=<int>`. The wave acquires the same external ratchet the chain has, and the two ledgers cross-check: forging either tape now also requires forging the other's era checkpoints.
3. Falsifier: rewrite `GROUNDING_WAVE.jsonl` in full, rehash all rows, run the estate's own verify. Current code: PASS (self-referential). Patched code: the last published era's `wave_root` mismatches, DIVERGENT, exit 1.

---

## (4) WHAT THE RESTORE DRILL PROVED AND DID NOT PROVE

PROVED (from bytes):
- The lock serializes read-modify-write across processes for chain, knots, pointers on CURRENT code: `00__verkle_knot.py :: "Every mutator below now holds this lock, so chain read-modify-write, knot unlink and pointer write are atomic with respect to each other"`.
- The mixed-version race class is real, was proven twice on bytes, and the repair verb restores consistency: `01__chain_repair.py :: "Cause class (proven twice on bytes, 2026-09-27, receipts CHAIN_RACE_REPAIR_20260927.md ...)"` and its post-verify gate `ok2, why2 = _verify_chain_consistent()`.
- The tip write path was hardened after a torn write froze appends: `01__chain_repair.py :: "the chain got tmp+replace three lines up but the tip rode a bare TIP.write_text"` -> `_write_tip_atomic`.
- The witness refuses to move backward/sideways and refuses publish on divergence: the quoted publish-refusal block `02__tip_witness.py :: "PUBLISH REFUSED: the witness never moves backward or sideways."`.

NOT PROVED:
1. **No restore-from-tamper drill exists in evidence.** Every proven scenario is a RACE or torn-write class (accident). Nothing shows detection of, or recovery from, a deliberate history rewrite. The witness has never published at all (PAT scope denial, `02__tip_witness.py :: "First real publish fails exit 2 with the SCOPE note"`), so DIVERGENT has never fired against a real external checkpoint in a drill.
2. **Interior-rewrite detection is untested and, per the compare() bytes, cannot distinguish laundering from amend noise** (see map, T1/T2).
3. **Knot-file coverage is broken as an integrity check:** the lock's own forensics concede `00__verkle_knot.py :: "Forensics: 1,044 chain rows referenced knot files that no longer existed."` A chain whose leaves can be missing cannot be fully re-derived, so full-chain re-verification post-restore is not possible for those 1,044 rows; their leaf hashes are unverifiable claims.
4. **The grounding wave restore path is a blank:** no drill, no external checkpoint, and repair of the wave is not in evidence (UNVERIFIED: any claim that `grounding_wave verify` survives a mid-tape truncation; nothing in the bundle tests it).
5. **The chain_repair tool's own tamper-safety is unproven and, per J2, false:** the tool re-roots over attacker-controlled `leaf_hash` bytes.

**Net verdict:** against the hostile-outsider surface, the chain plus a PUBLISHED witness is sound in the shrink and sideways cases and unsound in the grow case (J1). Against the write-capable insider, the only external check is bypassable, the incident-response tool is a mutation channel (J2), and the second ledger has no external check at all (J3). The witness publish flag being pending means, at audit moment, the estate has ZERO external tamper evidence in force.

**Deliverable falsifier (whole spec):** apply PATCH-J1/J2/J3; then execute the T2 forgery (interior rewrite + one appended leaf + publish). If the era-gist verify returns exit 0 on the forged chain, the spec is wrong and the witness-lattice design fails.
