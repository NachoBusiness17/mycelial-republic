"""grounding_wave — the GROUND circuit's ledger (operator algebra: GROUND primitive).

A wave post = ONE ground-truth claim with a tri-state verdict + an evidence
pointer, hash-chained to the previous post. Append-only: corrections are new
posts that cite the old hash (delete-as-append). Doctrine rides the standing
wave; the grounding wave carries only what we can point at.

LAW CITATION: files not processes; chain-side append, nothing scheduled.

CLI:
  python -m mag.grounding_wave post --claim "..." --verdict SUPPORTED \
      --evidence path-or-pointer [--note "..."]
  python -m mag.grounding_wave verify
  python -m mag.grounding_wave render
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "watch" / "GROUNDING_WAVE.jsonl"
VIEW_MD = ROOT / "watch" / "GROUNDING_WAVE.md"
VIEW_STATIC = ROOT / "dashboard" / "static" / "grounding_wave.md"
GENESIS = "0" * 64
VERDICTS = ("SUPPORTED", "DISPUTED", "UNPROVEN")

# wave v2 (salon 20260906, astra catch): rows carry a `seat` (poster identity,
# hashed — attribution is provable, forks are attributable) and verify() audits
# EVIDENCE, not just linkage — a hash-valid post whose evidence path is dead
# FAILS the chain check. Hashing uses .get defaults so v1 rows stay valid.
#
# wave v3 (20260908, astra witness #5 + salon-audit catch): the FALSE-RECEIPT
# attack passed verify() with a fabricated SUPPORTED row (0/1 rejected) —
# linkage-PASS was being read as truth-PASS. Three teeth, forward-applied:
#   1. SUPPORTED requires a second witness (v3 rows); unwitnessed SUPPORTED is
#      auto-demoted to UNPROVEN with a demotion note (delete-as-append: a later
#      witnessed post upgrades it).
#   2. post() holds an append lock (concurrent writers were a named liability).
#   3. verify() reports LINKAGE-PASS (hashes+evidence) separately from the
#      admission audit (witnessed vs legacy-unwitnessed SUPPORTED rows) — no
#      reader may quote bare "PASS" again.
_PATH_RE = re.compile(r"(?:[\w.-]+/)+[\w.-]+\.[\w]+")  # file-like paths only (ext required)
LOCK = LEDGER.parent / "GROUNDING_WAVE.lock"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _rows() -> list[dict[str, Any]]:
    if not LEDGER.is_file():
        return []
    out = []
    for ln in LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if ln:
            out.append(json.loads(ln))
    return out


_V1_KEYS = ("prev", "ts", "claim", "verdict", "evidence", "note")
_V2_KEYS = ("prev", "ts", "claim", "verdict", "evidence", "note", "seat")
_V3_KEYS = ("prev", "ts", "claim", "verdict", "evidence", "note", "seat", "witness")


def _row_hash(row: dict[str, Any]) -> str:
    # Schema-versioned: v1 rows (no seat) hash under the v1 key set so the
    # founding posts stay valid; v2 rows hash with seat; v3 rows add witness.
    if "witness" in row:
        keys = _V3_KEYS
    elif "seat" in row:
        keys = _V2_KEYS
    else:
        keys = _V1_KEYS
    core = json.dumps({k: row.get(k, "") for k in keys},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(core.encode("utf-8")).hexdigest()


class _AppendLock:
    """O_EXCL lockfile with stale-break (Windows-safe, no fcntl)."""

    def __init__(self, path: Path, timeout_s: float = 15.0, stale_s: float = 60.0):
        self.path, self.timeout_s, self.stale_s = path, timeout_s, stale_s
        self._fd: int | None = None

    def __enter__(self) -> "_AppendLock":
        import os as _os, time as _time
        deadline = _time.time() + self.timeout_s
        while True:
            try:
                self._fd = _os.open(self.path, _os.O_CREAT | _os.O_EXCL | _os.O_WRONLY)
                return self
            except FileExistsError:
                try:
                    if _time.time() - self.path.stat().st_mtime > self.stale_s:
                        self.path.unlink(missing_ok=True)  # stale lock from a dead writer
                        continue
                except FileNotFoundError:
                    continue
                if _time.time() > deadline:
                    self._fd = None
                    return self  # degrade to lockless append rather than lose the post
                _time.sleep(0.25)

    def __exit__(self, *exc: Any) -> None:
        import os as _os
        if self._fd is not None:
            _os.close(self._fd)
            self.path.unlink(missing_ok=True)


def post(claim: str, verdict: str, evidence: str, note: str = "",
         seat: str = "zcode", witness: str = "") -> dict[str, Any]:
    verdict = verdict.upper()
    if verdict not in VERDICTS:
        raise SystemExit(f"verdict must be one of {VERDICTS}")
    demoted = False
    if verdict == "SUPPORTED" and not witness.strip():
        # v3 truth-gate: SUPPORTED is a TWO-SEAT verdict. An unwitnessed post
        # still lands (the record keeps moving) but lands as UNPROVEN.
        verdict = "UNPROVEN"
        demoted = True
        note = (note.strip() + (" | " if note.strip() else "") +
                "auto-demoted from SUPPORTED: no second witness (v3 truth-gate)")
    with _AppendLock(LOCK):
        rows = _rows()
        prev = rows[-1]["hash"] if rows else GENESIS
        row = {"prev": prev, "ts": _now(), "claim": claim.strip(),
               "verdict": verdict, "evidence": evidence.strip(), "note": note.strip(),
               "seat": seat.strip(), "witness": witness.strip()}
        row["hash"] = _row_hash(row)
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    if demoted:
        print("TRUTH-GATE: SUPPORTED without second witness -> landed as UNPROVEN "
              "(re-post with --witness to upgrade)")
    if "_latest" in evidence:
        print("WARN: evidence cites a *_latest file (mutable) — prefer an "
              "immutable snapshot under state/wave_evidence/")
    render()
    return row


def _evidence_missing(rows: list[dict[str, Any]]) -> list[tuple[int, str]]:
    """Repo-relative slash-paths in evidence that do not resolve (v2 audit).

    A token also counts as resolved if it is a PREFIX of an existing path
    (timestamped/suffixed backups like .bak-row27-20260906 are one family)."""
    missing: list[tuple[int, str]] = []
    for i, row in enumerate(rows, 1):
        for tok in sorted(set(_PATH_RE.findall(row.get("evidence", "")))):
            p = ROOT / tok
            if p.exists():
                continue
            try:
                if any(ROOT.glob(tok + "*")):
                    continue  # prefix of a real sibling (e.g. .bak-suffixed snapshots)
            except Exception:  # noqa: BLE001 — malformed glob chars fall through to missing
                pass
            missing.append((i, tok))
    return missing


def verify() -> tuple[bool, str]:
    rows = _rows()
    prev = GENESIS
    for i, row in enumerate(rows, 1):
        if row.get("prev") != prev:
            return False, f"row {i}: prev-hash mismatch (chain broken)"
        if _row_hash(row) != row.get("hash"):
            return False, f"row {i}: hash mismatch (row edited in place)"
        prev = row["hash"]
    dead = _evidence_missing(rows)
    witnessed = sum(1 for r in rows
                    if r.get("verdict") == "SUPPORTED" and r.get("witness"))
    legacy_unwitnessed = sum(1 for r in rows
                             if r.get("verdict") == "SUPPORTED" and not r.get("witness"))
    msg = (f"LINKAGE-PASS: {len(rows)} posts intact, tip={prev[:12]} | "
           f"truth-gate: {witnessed} witnessed SUPPORTED, "
           f"{legacy_unwitnessed} legacy-unwitnessed")
    if dead:
        msg += (" | EVIDENCE-MISSING " +
                ", ".join(f"row {i}:{tok}" for i, tok in dead[:6]))
        return False, msg
    return True, msg


def render() -> str:
    rows = _rows()
    lines = ["# GROUNDING WAVE", "",
             "GROUND circuit ledger — one verified claim per post, hash-chained,",
             "tri-state only. Newer posts below. Ledger: `watch/GROUNDING_WAVE.jsonl`.", ""]
    for row in reversed(rows):
        lines.append(f"## {row['ts']} — {row['verdict']} — {row.get('seat', 'v1-era')}")
        lines.append(f"- **claim:** {row['claim']}")
        lines.append(f"- **evidence:** {row['evidence']}")
        if row.get("note"):
            lines.append(f"- **note:** {row['note']}")
        lines.append(f"- hash `{row['hash'][:12]}` ← prev `{row['prev'][:12]}`")
        lines.append("")
    md = "\n".join(lines)
    VIEW_MD.write_text(md, encoding="utf-8")
    VIEW_STATIC.parent.mkdir(parents=True, exist_ok=True)
    VIEW_STATIC.write_text(md, encoding="utf-8")
    return md


def resolve_ground_state(state_a: dict[str, Any], state_b: dict[str, Any], timestamp: str) -> dict[str, Any]:
    """Resolves conflicting ground states based on a deterministic strategy.
    
    For now, this is a placeholder. A robust strategy would involve:
    1. Prioritizing states with a second witness for 'SUPPORTED' verdicts.
    2. Considering the timestamp for recency in cases of 'UNPROVEN' or 'DISPUTED' states.
    3. A pre-defined hierarchy of 'seat' identities if necessary.
    """
    # Simple placeholder: if one is witnessed SUPPORTED, it wins. Otherwise, the newer one wins.
    if state_a.get("verdict") == "SUPPORTED" and state_a.get("witness"):
        return state_a
    if state_b.get("verdict") == "SUPPORTED" and state_b.get("witness"):
        return state_b
    
    # If neither is witnessed SUPPORTED, take the newer one
    if state_a.get("ts", "") > state_b.get("ts", ""):
        return state_a
    return state_b


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["post", "verify", "render"])
    ap.add_argument("--claim", default="")
    ap.add_argument("--verdict", default="SUPPORTED")
    ap.add_argument("--evidence", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--seat", default="zcode")
    ap.add_argument("--witness", default="",
                    help="second witness identity+pointer (required for SUPPORTED)")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    if args.cmd == "post":
        row = post(args.claim, args.verdict, args.evidence, args.note, args.seat,
                   args.witness)
        ok, msg = verify()
        print(f"POSTED #{row['hash'][:12]} ({row['verdict']}) — {msg}")
    elif args.cmd == "verify":
        ok, msg = verify()
        print(("PASS " if ok else "FAIL ") + msg)
        sys.exit(0 if ok else 1)
    elif args.cmd == "render":
        render()
        print(f"rendered {VIEW_MD.name} + {VIEW_STATIC.name}")


if __name__ == "__main__":
    main()
