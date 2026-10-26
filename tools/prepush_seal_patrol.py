#!/usr/bin/env python3
"""prepush_seal_patrol.py - last-seal-vs-bytes patrol over the inbox seal ledger.

Lane row (cause + evidence): memory/runs/mickey17_v2/runs/run-0/lanes/
a12-ractor-legs.json row index 3, idem
watch/inbox/index_events.jsonl#62f7d596a113. That lane ran CHECK3 (preserved
in memory/runs/mickey17_v2/runs/run-0/lanes/tmp_a12_verify.py): take each
file's LATEST sha256-bearing row and compare it to the file's actual bytes;
it measured 21/21 matches and named this standing pre-push check.

R3 TRUST UPGRADE (2026-10-05, fold row 3,
watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md): the
old organ certified representations, not things. (a) Last-row-wins let a
forged appended row erase drift (lens probe: 12 drifted files to 0) and a
backdated row mask the true latest seal (probe returned CLEAN on a violated
newest seal). (b) Whole-bytes compare could not split a living append board
(permanently red) from a true rewrite of sealed content. (c) Nothing chained
ledger rows, so a hand-typed row was indistinguishable from a writer's.
The four fixes:

1. MAX-TS SELECTION: the operative seal per file is the row with the newest
   parseable ts (ties: later ledger line). A backdated row appended after
   the true seal cannot mask it.
2. APPEND/REWRITE TAXONOMY: seal rows carry a stamped byte length (the
   autoseal "bytes" field; register rows inherit it from their same-file
   same-sha autoseal pair). One pass hashes the file and snapshots the
   digest at every sealed length (incremental prefix hash): latest seal
   prefix-intact but the file longer = a prefix-pure APPEND (quiet, the
   living-board class); any seal prefix-broken = a REWRITE of sealed
   content (alarm). Seals with no length stamp anywhere stay visible as
   unknown-class drift (the old behavior).
3. WITNESS RULE: an exact-match row with NO writer identity and NO
   same-file same-sha register partner (a hand-typed row) cannot clear a
   file whose witnessed seals are prefix-broken; that alarms as
   unwitnessed.
4. CHAIN VERIFY (exit 2): per writer, nonce/seq must never step backward
   in the window (batch seals share a value legitimately; forward gaps are
   multi-surface writer history, never fatal); rows carrying "prev" must
   digest-chain to the immediately preceding sha-bearing row. A break
   means the ledger cannot be trusted: cannot-verify exit 2, rows named.

Inherited lane laws: sealed-but-deleted files are NOT a defect (the lane
measured 42 sealed paths vs 21 on disk and ruled the deletes expected;
malformed rows are counted, never fatal - exactly 3 template rows lived in
a 10,004-line ledger).

Cost law (measured at landing): the full ledger names 5,404 distinct sha
files, 1.81 GB to hash (receipt watch/inbox/go_wave_20261004/
prepush_instruments.md), so the default window is the last 150 sha-bearing
rows; --rows widens it. Prefix snapshots add no second pass: one read,
digest copies at each checkpoint.

Ledger paths arrive as bare-relative ("board/FILE.md"), absolute inside
the estate ("C:/.../watch/inbox/..."), and the Docker surface
("/board/inbox/...", absent on the Windows host; outside-root absolutes
are skipped as other-surface, counted, never findings).

WARN-ONLY per the t40/B2-215 house pattern: the hook prints findings and
never blocks; flip to enforce is an operator call.

Exit codes: 0 = every windowed on-disk file matches its latest seal (pure
appends count as quiet, not drift); 1 = post-seal drift (rewrite of sealed
content, an unwitnessed row clearing drifted bytes, or unknown-class
drift); 2 = cannot verify (ledger missing, or the seal chain is broken).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
# Anchored to ESTATE_ROOT (violation_ratchet cwd-relative-path class, first
# landing: the bare Path("watch/inbox/...") literal sat at module scope and
# the ratchet named it). main() still re-resolves a RELATIVE --ledger against
# --root so tmp-root tests keep working.
DEFAULT_LEDGER = ESTATE_ROOT / "watch/inbox/index_events.jsonl"
DEFAULT_WINDOW = 150
HASH_CHUNK = 1 << 20

# A seal sha the patrol can actually compare (writer's full-file digest).
# Non-hex values ("size-only(>256KB)", living-style prefix seals) cannot
# prefix-classify and fall back to whole-file compare only.
HEX64 = re.compile(r"^[0-9a-f]{64}$")

# Drift classes (the R3 taxonomy).
CLS_REWRITE = "rewrite"            # sealed content itself was overwritten
CLS_UNWITNESSED = "unwitnessed"    # a hand-typed row clears drifted bytes
CLS_UNKNOWN = "unknown"            # no length stamp anywhere: cannot classify


def resolve_sealed_path(root: Path, file_field: str) -> Path | None:
    """Map a ledger 'file' value to a disk path under this estate, or None
    when the row names another surface (the Docker /board/inbox mount)."""
    p = file_field.replace("\\", "/")
    if p[1:2] == ":" or p.startswith("/"):
        try:
            resolved = Path(p).resolve()
        except (OSError, ValueError):
            return None
        try:
            resolved.relative_to(root)
        except ValueError:
            return None
        return resolved
    if p.startswith("watch/inbox/"):
        return root / p
    return root / "watch/inbox" / p


def parse_ledger(ledger: Path) -> tuple[list[dict], int]:
    """Return (sha-bearing rows in ledger order, malformed row count)."""
    rows: list[dict] = []
    malformed = 0
    with ledger.open("r", encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except Exception:
                malformed += 1
                continue
            if isinstance(row, dict) and row.get("file") and row.get("sha256"):
                row["_lineno"] = lineno
                rows.append(row)
    return rows, malformed


def _parse_ts(value) -> float | None:
    """Epoch seconds for an ISO-8601 ts (Z or offset), else None. Max-TS
    feed: a ts-less row cannot prove it is the newest seal."""
    s = str(value or "").strip()
    if not s:
        return None
    if s.endswith(("Z", "z")):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def _int_or_none(value) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _row_digest(row: dict) -> str:
    """Canonical digest of a ledger row for prev-digest chaining: the row's
    JSON minus private keys (leading _) and the chain's own 'prev' field."""
    payload = {k: v for k, v in row.items()
               if k != "prev" and not str(k).startswith("_")}
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def chain_verify(window_rows: list[dict]) -> list[str]:
    """Seal-chain verify over the window's sha-bearing rows (R3 fix 4).

    Two break classes, both exit 2 at run(): a writer's nonce or seq going
    backward in ledger order (forged or reordered row; batch seals share a
    value legitimately, forward gaps are multi-surface writer history,
    never fatal), and a "prev" field that does not equal the canonical
    digest of the immediately preceding sha-bearing row.
    """
    breaks: list[str] = []
    last_by_writer: dict[str, dict] = {}
    prev_row: dict | None = None
    for row in window_rows:
        if prev_row is not None and row.get("prev"):
            expected = _row_digest(prev_row)
            claimed = str(row["prev"]).strip().lower()
            if claimed != expected:
                breaks.append(
                    f"prev-digest break at ledger line {row.get('_lineno', '?')}: "
                    f"claims prev {claimed[:12]} but the previous sha row "
                    f"digests {expected[:12]}")
        writer = row.get("writer")
        if writer:
            state = last_by_writer.setdefault(str(writer), {})
            ln = row.get("_lineno", 0)
            nonce = _int_or_none(row.get("nonce")) if row.get("nonce") is not None else None
            seq = _int_or_none(row.get("seq")) if row.get("seq") is not None else None
            if nonce is not None:
                if state.get("nonce") is not None and nonce < state["nonce"]:
                    breaks.append(
                        f"writer {writer}: nonce {nonce} at ledger line {ln} goes "
                        f"backward after nonce {state['nonce']} at line {state.get('ln', '?')}")
                state["nonce"] = nonce
                state["ln"] = ln
            if seq is not None:
                if state.get("seq") is not None and seq < state["seq"]:
                    breaks.append(
                        f"writer {writer}: seq {seq} at ledger line {ln} goes "
                        f"backward after seq {state['seq']} at line {state.get('seq_ln', '?')}")
                state["seq"] = seq
                state["seq_ln"] = ln
        prev_row = row
    return breaks


def _digest_checkpoints(path: Path, lengths: set[int]) -> dict[int, str]:
    """sha256 of the first L bytes for every L in lengths, one pass.

    The incremental prefix hash (R3 fix 2): the file is read once and the
    running digest is snapshotted at each sealed length (hashlib copies are
    cheap). Callers include the full file size in lengths to get the
    whole-file digest in the same pass; a length past EOF never checkpoints
    (the caller treats that seal as broken: the file shrank)."""
    digest = hashlib.sha256()
    marks: dict[int, str] = {}
    targets = sorted(lengths)
    with path.open("rb") as fh:
        pos = 0
        ti = 0
        while ti < len(targets) and targets[ti] <= pos:
            if targets[ti] == pos:
                marks[pos] = digest.copy().hexdigest()
            ti += 1
        while ti < len(targets):
            want = max(min(targets[ti] - pos, HASH_CHUNK), 1)
            chunk = fh.read(want)
            if not chunk:
                break
            digest.update(chunk)
            pos += len(chunk)
            while ti < len(targets) and targets[ti] <= pos:
                if targets[ti] == pos:
                    marks[pos] = digest.copy().hexdigest()
                ti += 1
    return marks


def patrol(root: Path, rows: list[dict], window: int) -> dict:
    """Verdict core over parsed rows (R3: max-TS selection + append/rewrite
    taxonomy + witness rule). Present-and-violated is classified, missing
    on disk is not a defect (the a12 law)."""
    seals: dict[Path, list[dict]] = {}
    for row in rows[-window:]:
        resolved = resolve_sealed_path(root, str(row["file"]))
        if resolved is None:
            continue
        raw_bytes = row.get("bytes")
        seals.setdefault(resolved, []).append({
            "sha": str(row["sha256"]).strip().lower(),
            "op": str(row.get("op", "?")),
            "ts": _parse_ts(row.get("ts")),
            "bytes": raw_bytes if isinstance(raw_bytes, int) and raw_bytes >= 0 else None,
            "lineno": row.get("_lineno", 0),
            "writer": row.get("writer"),
        })
    matched: list[Path] = []
    appended: list[tuple[Path, int, int]] = []
    drifted: list[dict] = []
    missing = 0
    for path, hist in seals.items():
        # max-TS selection order: ts-carrying above ts-less, newest ts, then
        # ledger line (ties: a register then its later autoseal pair)
        hist.sort(key=lambda s: (s["ts"] is not None,
                                 s["ts"] if s["ts"] is not None else 0.0,
                                 s["lineno"]))
        # witness feed: a register row (writer present) witnesses its
        # same-file same-sha autoseal pair
        register_shas = {s["sha"] for s in hist if s["writer"]}
        for s in hist:
            s["witnessed"] = bool(s["writer"]) or s["sha"] in register_shas
        # length-stamp inheritance: register rows inherit the stamped byte
        # length of any same-file same-sha row (their autoseal pair)
        stamped: dict[str, int] = {}
        for s in hist:
            if s["bytes"] is not None and HEX64.match(s["sha"]):
                stamped.setdefault(s["sha"], s["bytes"])
        for s in hist:
            if s["bytes"] is None and s["sha"] in stamped:
                s["bytes"] = stamped[s["sha"]]
        if not path.is_file():
            missing += 1  # sealed temp deleted after the fact: a12 law, not a defect
            continue
        size = path.stat().st_size
        lengths = {size} | {s["bytes"] for s in hist
                            if s["bytes"] is not None and HEX64.match(s["sha"])
                            and 0 <= s["bytes"] <= size}
        marks = _digest_checkpoints(path, lengths)
        full = marks.get(size, "")
        selected = hist[-1]
        # prefix-broken seals: hex sha + known length whose first-L digest no
        # longer matches (or whose length now exceeds the shrunken file)
        broken = [s for s in hist
                  if HEX64.match(s["sha"]) and s["bytes"] is not None
                  and marks.get(s["bytes"]) != s["sha"]]
        if selected["sha"] == full:
            if (broken and any(s["witnessed"] for s in broken)
                    and not selected["witnessed"]):
                # a hand-typed row is the only thing clearing drifted bytes
                drifted.append({"path": path, "sealed": selected["sha"][:12],
                                "actual": full[:12], "cls": CLS_UNWITNESSED,
                                "evidence": None})
            else:
                matched.append(path)
            continue
        if broken:
            worst = broken[0]
            drifted.append({"path": path, "sealed": selected["sha"][:12],
                            "actual": full[:12], "cls": CLS_REWRITE,
                            "evidence": (f"seal at ledger line {worst['lineno']} "
                                         f"({worst['bytes']} sealed bytes) is no "
                                         f"longer a prefix of the file "
                                         f"({size} bytes)")})
        elif (selected["bytes"] is not None and HEX64.match(selected["sha"])
              and marks.get(selected["bytes"]) == selected["sha"]):
            # latest seal prefix-intact, file longer: a living append board
            appended.append((path, selected["bytes"], size))
        else:
            # no length stamp to split append from rewrite: stays visible
            drifted.append({"path": path, "sealed": selected["sha"][:12],
                            "actual": full[:12], "cls": CLS_UNKNOWN,
                            "evidence": None})
    return {"matched": matched, "drifted": drifted, "appended": appended,
            "missing": missing, "distinct": len(seals)}


def run(root: Path, ledger: Path, window: int) -> int:
    if not ledger.is_file():
        print(f"SEAL-PATROL: cannot verify, seal ledger missing: {ledger}")
        return 2
    rows, malformed = parse_ledger(ledger)
    breaks = chain_verify(rows[-window:])
    if breaks:
        print(f"SEAL-PATROL: cannot verify - seal chain broken "
              f"({len(breaks)} break(s)), ledger {ledger.as_posix()} "
              f"({len(rows)} sha rows), window last {window}")
        for b in breaks:
            print(f"  {b}")
        print("  fix: never hand-edit the ledger; re-seal through the owning "
              "writer and investigate the named rows (a broken chain means "
              "every seal in the window is untrustworthy)")
        return 2
    result = patrol(root, rows, window)
    head = (f"ledger {ledger.as_posix()} ({len(rows)} sha rows, {malformed} malformed), "
            f"window last {window}: {result['distinct']} distinct file(s), "
            f"{len(result['matched'])} match, {len(result['appended'])} append-quiet, "
            f"{result['missing']} missing-on-disk "
            f"(skipped: expected seal-chain deletes per a12-ractor-legs row 3)")
    if not result["drifted"]:
        print(f"SEAL-PATROL: ok - {head}")
        return 0
    print(f"SEAL-PATROL: DRIFT - {head}")
    for d in result["drifted"]:
        path = d["path"]
        rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
        if d["cls"] == CLS_REWRITE:
            print(f"  rewrote sealed content: {rel}")
            print(f"    seal sha {d['sealed']} vs actual bytes {d['actual']}; {d['evidence']}")
        elif d["cls"] == CLS_UNWITNESSED:
            print(f"  seal row without writer identity clears drifted bytes: {rel}")
            print(f"    claimed seal sha {d['sealed']} vs actual bytes {d['actual']} "
                  f"matches, but a witnessed seal's content was rewritten")
        else:
            print(f"  moved after its last seal: {rel}")
            print(f"    sealed sha {d['sealed']} vs actual bytes {d['actual']}")
    print("  fix: re-seal through the owning writer (register/autoseal append to "
          "watch/inbox/index_events.jsonl) or restore the sealed bytes; never "
          "hand-edit the ledger")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="last-seal-vs-bytes patrol over the inbox seal ledger (a12 row 3)")
    ap.add_argument("--root", type=Path, default=ESTATE_ROOT,
                    help="estate root (default: this repo)")
    ap.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER,
                    help="seal ledger (default: watch/inbox/index_events.jsonl)")
    ap.add_argument("--rows", type=int, default=DEFAULT_WINDOW,
                    help=f"window of trailing sha-bearing rows to check "
                         f"(default {DEFAULT_WINDOW}; full ledger is 1.81 GB of hashing)")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    ledger = args.ledger
    if not ledger.is_absolute():
        ledger = root / ledger
    return run(root, ledger, args.rows)


if __name__ == "__main__":
    sys.exit(main())
