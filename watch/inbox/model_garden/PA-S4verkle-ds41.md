# PA-S4verkle-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# STRANGER AUDIT — SURFACE 4: THE VERKLE CHAIN

Writer-capable adversary. Full deliverable below.

---

## PROVENANCE NOTE

Evidence arrived as three head+tail slices of four files. The middle of `00__verkle_knot.py` (between `_merkle_root` and the tail's `_series_point` region), the middle of `02__tip_witness.py` (the GistAPI body, `fetch_witness_line`, `run_verify`, `run_publish` head), and the middle of `03__grounding_wave.py` (the `_admit` gate, `post`, `void`, `witness`, `verify`) are NOT in the visible bytes. Any claim about those regions is marked UNVERIFIED and I do not lean on it. Every line I cite is quoted from bytes I can see.

---

## (1) ATTACK SURFACE MAP

### 1a. The witness is a tip hash. Interior rewrites with a recomputed tip are invisible to it. TRUE. Proof from the code.

`02__tip_witness.py` `compare()`:

```
if witnessed["root"] == live["root"] and witnessed["n_leaves"] == live["n_leaves"]:
    return ("WITNESS-MATCH", ...)
...
return ("WITNESS-DIVERGENT",
        f"same count ({live['n_leaves']} leaves) but root differs - "
        f"same-length rewrite, laundering alarm")
```

The witness stores exactly two facts: `root=<64-hex>` and `n_leaves=<int>`. Root is the Merkle root over the leaf-hash list (`_merkle_root(leaf_hashes)` in `00__verkle_knot.py`). Leaf hash is `sha256(b"leaf:" + canonical_json(obj))` (`_leaf_hash`). The chain row stores `leaf_hash` per row (used by `find_bad_tail_index` in `01__chain_repair.py`: `hashes.append(str(r["leaf_hash"]))`, then `_merkle_root(hashes)`).

So the witness's guarantee is exactly: *the tuple (root, n_leaves) at publish time equals the tuple (root, n_leaves) at verify time*. It says nothing about the interior.

**Attack A-1 (interior rewrite, same tip):** an insider rewrites an interior row's payload — say the `claim` field of a v4 grounding row, or the `dominant_theme` on a knot leaf — and does NOT change `leaf_hash`. The row's own `leaf_hash` is now inconsistent with its content. But `_verify_chain_consistent` (invoked by `01__chain_repair.py` `repair()`) compares `r["verkle_root"]` against `_merkle_root(hashes)` where `hashes` is drawn from `r["leaf_hash"]`. If the attacker leaves `leaf_hash` untouched, the Merkle root is unchanged, `_verify_chain_consistent` is unchanged, and `compare()` returns `WITNESS-MATCH`. **The witness is blind.**

**Attack A-2 (recompute both leaf and every ancestor, same count):** if the attacker recomputes `leaf_hash` for the changed row and recomputes `verkle_root` on every row from the changed index to the tail, then also rewrites `verkle_tip.json`, the tuple (root, n_leaves) changes — but the count is unchanged. `compare()` falls through to the last line: `"same count ... but root differs - same-length rewrite, laundering alarm"`. **Caught, but only because the tip file was also rewritten.** If the attacker rewrites the chain and leaves `verkle_tip.json` stale, `verify` sees LAG or MATCH against the stale root — and `01__chain_repair.py` will cheerfully rewrite the offending row's `verkle_root` back to `_merkle_root(hashes)` of the *already-tampered* leaf hashes, printing `CHAIN-REPAIR: row N ... <old_root> -> <true_root>` and returning 0. **The repair tool launders the tamper.** This is the sharpest joint in the whole surface: `repair()` treats "committed root disagrees with recomputed root over surviving leaf hashes" as a race, and unconditionally prefers the recomputed side. There is no cross-check against the witness inside `repair()`.

**Attack A-3 (amend-in-place, the design's own edge):** `chain_mode()` defaults fail-closed to `v1`, which the docstring states is "amend-in-place — a re-save of an existing session replaces its row and rewrites the WHOLE chain file (O(n) bytes per save; live forensics: 2,821/8,626 rows were amend rewrites)." v1 amend gives the attacker a *built-in reason* to rewrite the whole chain file. A rewrite that produces a legal-looking v1 chain (every row's `verkle_root` = `_merkle_root` of the leaf hashes through that row) is indistinguishable from a legitimate amend by any verifier that only calls `_verify_chain_consistent`. The witness catches it only if `n_leaves` shrinks or the final root diverges — and the attacker controls both, because they control the tip file too (`_write_tip_atomic` writes it; the witness `load_tip` reads it, per `02__tip_witness.py` `load_tip` docstring: "*reads memory/biography/verkle_tip.json as the live tip; tip-vs-chain consistency is AG5's job, not recomputed here*"). **That sentence is an explicit admission that the witness's trust boundary is the tip file, which the writer owns.**

**Summary of what the witness WOULD catch:** (i) tip file rewritten to a shorter chain while leaves remain (LAG, reported as normal growth — not even an alarm); (ii) tip file rewritten to a same-count-different-root while gist is current (DIVERGENT, because the gist holds the old root and the live root differs); (iii) tip file left behind while the chain grows (LAG, normal). **What it would MISS:** any interior rewrite that does not change the (root, n_leaves) tuple at the tip; any interior rewrite followed by a matching tip rewrite and a matching `--publish` (the ratchet advances on count growth, so if the attacker also appends one junk leaf to bump `n_leaves`, `run_publish` will see `WITNESS-LAG` and *advance the witness to the attacker's new tip* — the ratchet launders one extra hop); and any tamper inside `find_bad_tail_index`'s window that `repair` then "fixes."

### 1b. Attack surface of the repair tool as a laundromat

`repair()` in `01__chain_repair.py`:

1. `find_bad_tail_index(rows)` returns the first i where `r["verkle_root"] != _merkle_root(hashes_through_i)`.
2. It then overwrites that row's `verkle_root`, `parent_verkle_root`, `n_leaves` with recomputed truth, and stamps `chain_race_repaired`.
3. It rewrites the whole file (`tmp.replace(CHAIN)`) and refreshes the tip.

Every one of these bullets is an attacker-controlled primitive if the attacker can produce any pair of (chain bytes, tip bytes) where a row disagrees. The tool does not consult the witness, does not require an out-of-band signature, and does not refuse when more than one row is inconsistent (it stops at the FIRST bad row, so a multi-row tamper gets partially repaired and the tail stays broken — see `repair()` exit 1 when `ok2` fails, but the file has already been rotated to tmp+replace with the row mutating operator-supplied bytes).

### 1c. Corollary: the lock does not protect against a writer, only against colliding writers

`verkle_lock` serializes concurrent mutators process-wide and seat-wide. It does nothing against a single insider who legitimately holds the lock and writes tampered bytes. This is fine as designed (it is a race fix, not a trust fix: "the lost-update fix" is the docstring's own word) but the surface must name it so no reader mistakes "single-writer" for "trusted writer."

---

## (2) THE 3 WEAKEST JOINTS, RANKED

### JOINT 1 — `_merkle_root` is not exposed to any reader that could pin it against a witness; repair() recomputes it from surviving leaf hashes and unconditionally trusts the recompute.

`01__chain_repair.py`, `find_bad_tail_index` + `repair`:

```
def find_bad_tail_index(rows): ...
    if r.get("verkle_root") and r["verkle_root"] != _merkle_root(hashes):
        return i
...
true_root = _merkle_root(hashes)
...
bad["verkle_root"] = true_root
bad["parent_verkle_root"] = true_parent
```

The recompute uses `hashes` derived from `r["leaf_hash"]` fields, which are attacker-writable. The tool has no independent copy of a previously-agreed root. Witness (`tip_witness.py`) has such a copy but is a separate tool (W3, published 2026-09-30) and `01__chain_repair.py` does not import or call it — verified by reading the import block: `from mag.verkle_knot import (_load_chain_rows, _merkle_root, _verify_chain_consistent, verkle_lock, _tip_for_tail, _write_tip_atomic, TIP, CHAIN)`. No witness import.

**Falsifier for this claim:** a `find_bad_tail_index`/`repair` code path in the unread middle of `01__chain_repair.py` (file is 105 lines here; the visible slice contains both functions entire) that consults the witness. The file is short enough that both functions are in the visible bytes, so I am confident the falsifier does not exist in this file.

### JOINT 2 — the witness's trust input is the tip file, and the tip file is writer-owned.

`02__tip_witness.py` module docstring:

> `Trust boundary: reads memory/biography/verkle_tip.json as the live tip; tip-vs-chain consistency is AG5's job, not recomputed here.`

`load_tip` reads `TIP_FILE = ROOT / "memory" / "biography" / "verkle_tip.json"`. The witness's external guarantee reduces to: *the (root, n_leaves) tuple in the tip file now equals the tuple that a gist row recorded at last publish*. The chain's actual root is compared to the witnessed tuple only via the tip file. If AG5 (whatever recomputes tip-vs-chain — UNVERIFIED, not in evidence) is itself part of the same writer-accessible tool path, the entire external witness chain is one attacker-controlled write away from being superseded.

### JOINT 3 — the v1 amend path rewrites the whole chain file (O(n) bytes) as an ordinary operation, so no byte-level invariant suffices.

`00__verkle_knot.py` `chain_mode` docstring:

> `v1 (default): amend-in-place — a re-save of an existing session replaces its row and rewrites the WHOLE chain file (O(n) bytes per save; live forensics: 2,821/8,626 rows were amend rewrites).`

The whole-file rewrite is the design's house-style ordinary write. That means every detection scheme must survive an attacker whose legitimate write pattern already touches every byte. External checkpoints and per-row signatures are the only remaining walls.

---

## (3) PATCH SPEC PER JOINT

All three patches are landable as-is. Line numbers reference what is visible; a seat with the full file should re-anchor.

### PATCH 1 — Repair tool must consult the witness before overwriting any row's root.

File: `watch/inbox/model_garden/premium_autopsy/evidence/S4verkle/01__chain_repair.py` (canonical path: `tools/chain_repair.py`).

Add to the import block:

```python
from tools.tip_witness import (
    load_tip as _wit_load_tip,
    parse_line as _wit_parse_line,
    WitnessError as _WitError,
)
```

Insert immediately after the `if ok: ... return 0` early-return in `repair()`, before `with verkle_lock(...)`:

```python
    # W4 (2026-10-01, stranger audit surface 4): refuse to repair silently when
    # the pre-repair tip disagrees with what the external witness already
    # published. Discriminates the mixed-version race class (repairable) from
    # a rewrite that also touched the tip (NOT repairable here - file incident).
    try:
        live_tip = _wit_load_tip()
    except _WitError as e:
        print(f"CHAIN-REPAIR: cannot read tip for witness cross-check: {e}",
              file=sys.stderr)
        return 2
    state_path = ROOT / "memory" / "biography" / "tip_witness_state.json"
    witnessed = None
    if state_path.is_file():
        try:
            st = json.loads(state_path.read_text(encoding="utf-8"))
            witnessed = _wit_parse_line(str(st.get("last_line") or ""))
        except (OSError, ValueError):
            witnessed = None
    if witnessed is not None:
        if witnessed["n_leaves"] > live_tip["n_leaves"]:
            print(f"CHAIN-REPAIR: REFUSED - witness holds more leaves "
                  f"({witnessed['n_leaves']}) than live tip "
                  f"({live_tip['n_leaves']}); shrunk chain is not a race. "
                  f"File the incident.", file=sys.stderr)
            return 2
        if (witnessed["n_leaves"] == live_tip["n_leaves"]
                and witnessed["root"] != live_tip["root"]):
            print(f"CHAIN-REPAIR: REFUSED - same leaf count, different root "
                  f"vs last published witness; laundering signature. "
                  f"File the incident.", file=sys.stderr)
            return 2
```

Effect: the mixed-version race is still repaired (that path leaves the tip ahead of the witness, or equal-and-same-root), but a same-count root change against the last published witness is now an exit-2 refusal, not a silent "true_root" overwrite. This is the smallest possible wall in front of **JOINT 1**.

**Falsifier for this patch:** a mixed-version race that also advances the live tip to a same-count-different-root state. If such a race is possible (I do not see one in the visible `_rewrite_chain`/`append` code, but the middle is truncated), the guard would false-positive and turn a repairable incident into an exit-2. Mitigation: the `chain_race_repaired` note path in `01__chain_repair.py` already proves the race class produces a *stale* tip (the race is "old module computes from a pre-race leaf set"), so tip root under-count is the expected signature, not same-count-different-root. I accept the risk.

### PATCH 2 — Interior-tree witness: two extra fields in the published witness line, verified on read.

File: `watch/inbox/model_garden/premium_autopsy/evidence/S4verkle/02__tip_witness.py`.

Change `LINE_RE` to accept an optional interior anchor:

```python
LINE_RE = re.compile(
    r"^MAG-TIP-WITNESS\.v1 root=([0-9a-f]{64}) n_leaves=(\d+)"
    r"(?: head=([0-9a-f]{64}) stride=(\d+))? ts=(\S+)$"
)
```

Update `build_line`:

```python
def build_line(root, n_leaves, ts, head=None, stride=None):
    if head is not None and stride:
        return (f"MAG-TIP-WITNESS.v1 root={root} n_leaves={n_leaves} "
                f"head={head} stride={stride} ts={ts}")
    return f"MAG-TIP-WITNESS.v1 root={root} n_leaves={n_leaves} ts={ts}"
```

Where `head = sha256(b"head:" + b"".join(bytes.fromhex(h) for h in leaf_hashes[:stride]))` — a rolling prefix-hash of the first `stride` leaf hashes, published alongside the tip.

On every `--publish`, `stride = n_leaves // 2` (or a fixed cap such as 512, whichever is smaller). `head` is recomputed from the chain being published.

Change `compare()` to require a head match when the witnessed line carried one:

```python
def compare(witnessed, live, live_head=None):
    if witnessed.get("head") is not None and live_head is not None:
        if witnessed["head"] != live_head:
            return ("WITNESS-DIVERGENT",
                    f"interior head mismatch: witnessed {witnessed['head'][:12]} "
                    f"vs live {live_head[:12]} - interior rewrite")
    # ... existing count/root logic unchanged ...
```

Effect: a **rewrite of any of the first `n_leaves//2` leaf hashes that leaves the tip tuple unchanged is now caught**, because the interior head no longer matches. Cost: 64 bytes in the gist line, one sha256 over 32·(n/2) bytes at publish. That closes the specific hole named in the contract.

**Falsifier for this patch:** an attacker who rewrites only the *second half* of the interior. They stay invisible until `n_leaves` grows enough that the old second half becomes the new head's first half, at which point the head check fires. Not a proof, a ratchet. If you want full coverage, publish `head` for both halves (`head_lo` over `[:n//2]`, `head_hi` over `[n//2:]`) — same cost, one line, no blind spot.

### PATCH 3 — Freeze an era snapshot independent of the rewrite path.

File: new, `tools/verkle_snapshot.py` (landable as-is).

```python
#!/usr/bin/env python3
"""verkle_snapshot - per-era frozen copy of the leaf-hash list.

W4 (2026-10-01, stranger audit surface 4): the chain's own v1 amend rewrites
the whole file, so no in-file invariant survives a writer with the lock. An
era snapshot is a read-only copy of (n_leaves, list_of_leaf_hashes, root) at
a moment the operator chose, written under a name that no chain mutator
touches. Tool inputs are the chain bytes; tool output is one file per era.

  python tools/verkle_snapshot.py              # write snapshots/era-<n>.json
  python tools/verkle_snapshot.py --verify-all # every snapshot vs current chain

Exit 0 ok; 2 = a snapshot's prefix disagrees with the current chain (that
prefix was rewritten).
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mag.verkle_knot import CHAIN, _merkle_root, verkle_lock  # noqa: E402

SNAPS = ROOT / "memory" / "biography" / "snapshots"


def _hashes() -> list[str]:
    out = []
    for line in CHAIN.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("leaf_hash"):
            out.append(str(row["leaf_hash"]))
    return out


def write_snapshot() -> int:
    with verkle_lock(timeout=120.0):
        hs = _hashes()
        n = len(hs)
        root = _merkle_root(hs)
    SNAPS.mkdir(parents=True, exist_ok=True)
    dest = SNAPS / f"era-{n}.json"
    if dest.exists():
        print(f"verkle_snapshot: era-{n} already frozen, no-op")
        return 0
    dest.write_text(json.dumps({
        "schema": "verkle_snapshot.v1",
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_leaves": n,
        "root": root,
        "leaf_hashes": hs,
    }, indent=2), encoding="utf-8")
    print(f"verkle_snapshot: era-{n} frozen ({n} leaves, root {root[:12]})")
    return 0


def verify_all() -> int:
    if not SNAPS.is_dir():
        print("verkle_snapshot: no snapshots to verify")
        return 0
    live = _hashes()
    bad = 0
    for p in sorted(SNAPS.glob("era-*.json")):
        try:
            s = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            print(f"verkle_snapshot: {p.name} UNREADABLE")
            bad += 1
            continue
        n = int(s["n_leaves"])
        if len(live) < n:
            print(f"verkle_snapshot: {p.name} FAIL - chain shrunk below era "
                  f"({len(live)} < {n})")
            bad += 1
            continue
        if live[:n] != s["leaf_hashes"]:
            print(f"verkle_snapshot: {p.name} FAIL - first {n} leaf hashes "
                  f"differ (interior rewrite inside era)")
            bad += 1
            continue
        if _merkle_root(live[:n]) != s["root"]:
            print(f"verkle_snapshot: {p.name} FAIL - era root mismatch")
            bad += 1
    if bad:
        return 2
    print(f"verkle_snapshot: all {len(list(SNAPS.glob('era-*.json')))} eras "
          f"consistent with current chain")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-all", action="store_true")
    a = ap.parse_args()
    return verify_all() if a.verify_all else write_snapshot()


if __name__ == "__main__":
    sys.exit(main())
```

Effect: after `era-N` is frozen, any rewrite of the first N leaf hashes is caught by `--verify-all` regardless of tip file contents. This is the *only* one of the three patches that survives an attacker who controls both chain and tip. It closes **JOINT 3** by making some bytes of the chain history non-rewritable by the chain's own tooling. Run `--verify-all` on the same cadence as `tip_witness --verify`; add it to whatever scheduled verify exists (UNVERIFIED whether one does).

**Falsifier for this patch:** an attacker with write access to `memory/biography/snapshots/`. Mitigation: put the directory on a different mount, or `chattr +i` after freeze, or (best) push eras to the same gist as the witness. The patch as written does not defend against a writer with write access to the snapshots directory; it defends against a writer of the chain file only, which is the joint named by the contract.

---

## (4) WHAT THE RESTORE DRILL PROVED AND DID NOT PROVE

I have no drill receipt in evidence. I cannot cite a file for what a drill proved. Anything below is a statement of what the visible tooling can and cannot *demonstrate* about chain integrity when run; I mark it as such.

**`01__chain_repair.py --dry` proves:** that from the tail inward, there exists an index i such that rows [0..i] are self-consistent under `_merkle_root` over their own `leaf_hash` fields. `find_bad_tail_index` returns `None` when this holds for every row.

**`01__chain_repair.py --dry` does NOT prove:** that the leaf hashes correspond to the bytes the leaves originally asserted. It cannot, because it reads `r["leaf_hash"]` and compares only to the recomputed `_merkle_root`. A chain in which every `leaf_hash` was rewritten in place, followed by a recomputed `verkle_root` on every row, passes `--dry` clean.

**`01__chain_repair.py --dry` also does NOT prove:** that the tip file matches the recomputed root. That comparison is done elsewhere (`_verify_chain_consistent` presumably, UNVERIFIED — not in evidence). `repair()` calls it twice (`ok, why = _verify_chain_consistent()` at the top, `ok2, why2` at the bottom) so the function exists, but its body is not visible.

**`02__tip_witness.py --verify` proves:** that the local `memory/biography/verkle_tip.json` `(root, n_leaves)` equals the `(root, n_leaves)` last published to the single gist.

**`02__tip_witness.py --verify` does NOT prove:** any interior byte of the chain. That is the contract's own hypothesis and it is confirmed above by direct citation of `compare()`. It also does NOT prove that the gist holds the *latest* tip; `WITNESS-LAG` is reported as "normal growth; publish due" — an attacker who is also the operator can hold the witness in LAG indefinitely by never running `--publish`, and the verifier will keep returning LAG (exit 0), never DIVERGENT.

**The missing drill:** no visible tool proves that the current leaf hashes are the same bytes that were in the chain on any prior date. The only artifact in evidence capable of that is the era snapshot — which does not exist in the codebase as of the visible bytes. That is the gap patches 2 and 3 close.

**Falsifier for the "no snapshot code exists" claim:** a `tools/verkle_snapshot.py`, `mag/verkle_era.py`, or an era-block in the truncated middle of `00__verkle_knot.py`. The visible head of `00__verkle_knot.py` ends mid-`_merkle_root` and the tail jumps to `_series_point`-adjacent code, so I cannot rule out a snapshot facility in the unread 33KB. A seat with the full file should check for `snapshot`, `era`, and `frozen` before landing patch 3.
