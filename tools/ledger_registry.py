#!/usr/bin/env python3
"""ledger_registry.py — one mount table for every hash-chain on the estate.

The disease this cures (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md return 19,
cross-organ lane): ONE chain law, SEVEN private implementations (wow_player,
gwap_payload, party_subchain, tesuji_map, verkle_knot, +3 more) — and only the
verkle chain is guarded (mag/chain_guard.py exists because that chain was
silently corrupted TWICE before its canary); six chains run unguarded.
mag/chain_query.py declares every-module-asks-the-chain-first but mounts only
the verkle chain, so the law covers ~10% of the append-only truth.

THE FIX IS A MOUNT TABLE, NOT ANOTHER VERIFIER. Each family registers
{name, schema, verify, tip_rows, hash_fields, globs/paths}; verify_all() runs
each chain's OWN verify function (the estate already wrote seven correct
referees — reimplementing an eighth would be copy N+1 of the disease); the
nightly canary files idempotent attention alerts when any chain fails its own
verify; query_by_hash() is the cross-ledger receipt-hash stub (the meter's
first customer and the judge queue become one line of code).

MOUNTED TODAY (2026-09-29):
  wow_player    memory/runs/wow_player/ply-*.json   mag/wow_player.verify_file
  gwap          memory/runs/gwap/*.jsonl            mag/gwap_payload.verify_chain_file
  server_world  logs/world*.jsonl, memory/runs/server_world/*.jsonl
                server/world.load_log_rows — the server writes a log only where
                --log points, and the only world chains currently on disk are
                44 throwaway agents/pytest-tmp-* fixtures, deliberately NOT
                swept: fixture churn is not estate truth; sanctioned homes only
                (production tapes belong in the two mounted globs).
  verkle        memory/biography/verkle_chain.jsonl via its OWN guard
                (mag/chain_guard.check — the ask's law, no side door).

Copy N+1 of the house chain pattern becomes a mount: append one entry dict.

Canary alerts: memory/attention.md blocks in the estate patrol shape,
idempotent by key exactly like tools/gap_sentinel.py (stolen and credited) —
jsonl record first (logs/ledger_registry/alerted.jsonl, single writer),
attention.md second (the B2-465 multi-writer law); the key carries
family+chain+detail, so the alert refires only on a NEW failure origin and a
persistent failure stays exit 1 but never re-files.

Exit codes: 0 = every mounted chain passes its own verify; 1 = chain
failures (canary filed once per key); 2 = cannot verify (a family's verify
module failed to import — the registry itself is broken, no chain verdict).

Usage:
  python tools/ledger_registry.py verify             # the chain table (read-only)
  python tools/ledger_registry.py canary            # nightly: verify + alert once per key
  python tools/ledger_registry.py query --hash abc123
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

ESTATE_ROOT = Path(__file__).resolve().parent.parent
if str(ESTATE_ROOT) not in sys.path:
    sys.path.insert(0, str(ESTATE_ROOT))

ALERTED_RELPATH = "logs/ledger_registry/alerted.jsonl"
RUNS_RELPATH = "logs/ledger_registry/runs.jsonl"
ATTENTION_RELPATH = "memory/attention.md"
QUERY_LIMIT = 50

CANARY_RESPONSE = (
    "the named chain fails its OWN verify (return 19: only verkle was guarded, "
    "six chains ran bare); treat every receipt quoting that chain's tip as "
    "unproven until the owning writer is inspected. Re-run: "
    "python tools/ledger_registry.py verify"
)


# ── family adapters: each calls the chain's own verify, never a reimpl ──


def _verify_wow_player(path: Path) -> tuple[bool, str]:
    from mag import wow_player
    ok, reason = wow_player.verify_file(json.loads(path.read_text(encoding="utf-8")))
    return bool(ok), str(reason)


def _tip_rows_wow_player(path: Path) -> tuple[int, str | None]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    ledger = doc.get("ledger") or []
    return len(ledger), (ledger[-1].get("hash") if ledger else None)


def _iter_wow_player(path: Path) -> Iterator[tuple[int, dict]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    for i, row in enumerate(doc.get("ledger") or [], 1):
        yield i, row


def _verify_gwap(path: Path) -> tuple[bool, str]:
    from mag import gwap_payload
    ok, bad = gwap_payload.verify_chain_file(path)
    return bool(ok), "OK" if ok else f"BROKEN_CHAIN first_bad_row={bad}"


def _tip_rows_gwap(path: Path) -> tuple[int, str | None]:
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return len(rows), (rows[-1].get("row_sha256") if rows else None)


def _verify_world(path: Path) -> tuple[bool, str]:
    from server.world import load_log_rows
    load_log_rows(path)  # raises ValueError on a corrupt chain — its own referee
    return True, "OK"


def _tip_rows_world(path: Path) -> tuple[int, str | None]:
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return len(rows), (rows[-1].get("sha") if rows else None)


def _verify_verkle(_path: Path) -> tuple[bool, str]:
    from mag import chain_guard
    res = chain_guard.check()
    return bool(res.get("ok")), str(res.get("state") or "check-returned-no-state")


def _tip_rows_verkle(_path: Path) -> tuple[int, str | None]:
    from mag import chain_guard
    res = chain_guard.check()
    return int(res.get("rows") or 0), (res.get("chain_root") or res.get("tip_root"))


def _iter_jsonl(path: Path) -> Iterator[tuple[int, dict]]:
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        yield i, row


FAMILY_BUILDERS: dict[str, Callable[[], dict[str, Any]]] = {
    "wow_player": lambda: {
        "name": "wow_player", "schema": "wow_player.v1",
        "verify": _verify_wow_player, "tip_rows": _tip_rows_wow_player,
        "iter_rows": _iter_wow_player, "hash_fields": ("hash",),
        "globs": ("memory/runs/wow_player/ply-*.json",),
    },
    "gwap": lambda: {
        "name": "gwap", "schema": "mag_gwap_payload.v1",
        "verify": _verify_gwap, "tip_rows": _tip_rows_gwap,
        "iter_rows": _iter_jsonl, "hash_fields": ("row_sha256",),
        "globs": ("memory/runs/gwap/*.jsonl",),
    },
    "server_world": lambda: {
        "name": "server_world", "schema": "world_log rows {seq, prev, sha}",
        "verify": _verify_world, "tip_rows": _tip_rows_world,
        "iter_rows": _iter_jsonl, "hash_fields": ("sha",),
        "globs": ("logs/world*.jsonl", "memory/runs/server_world/*.jsonl"),
    },
    "verkle": lambda: {
        "name": "verkle", "schema": "verkle_chain.jsonl via mag/chain_guard",
        "verify": _verify_verkle, "tip_rows": _tip_rows_verkle,
        "iter_rows": _iter_jsonl, "hash_fields": ("leaf_hash",),
        "globs": ("memory/biography/verkle_chain.jsonl",),
        "singleton": True,
    },
}


def default_families(root: Path = ESTATE_ROOT) -> list[dict[str, Any]]:
    """The mount table. Copy N+1 becomes one entry here."""
    entries = []
    for build in FAMILY_BUILDERS.values():
        entry = build()
        entry["root"] = root
        entries.append(entry)
    return entries


def discover(entry: dict[str, Any]) -> list[tuple[str, Path]]:
    """(chain label, path) per mounted chain. Explicit paths win over globs
    (tests mount fixture chains through the same door)."""
    if entry.get("paths"):
        return [(str(Path(p).name), Path(p)) for p in entry["paths"]]
    root = Path(entry.get("root") or ESTATE_ROOT)
    out: list[tuple[str, Path]] = []
    for g in entry.get("globs", ()):
        for p in sorted(root.glob(g)):
            out.append((p.relative_to(root).as_posix() if p.is_relative_to(root)
                        else str(p), p))
    return out


# ── verify_all: run each chain's own verify over the whole mount table ──


def _one_chain(entry: dict[str, Any], label: str, path: Path) -> dict[str, Any]:
    row: dict[str, Any] = {"family": entry["name"], "chain": label,
                           "ok": False, "detail": "", "rows": None, "tip": None}
    try:
        ok, detail = entry["verify"](path)
        row["ok"], row["detail"] = ok, detail
    except ImportError as exc:
        row["detail"], row["cannot_verify"] = f"IMPORT_ERROR {exc}", True
        return row
    except (OSError, ValueError, KeyError, TypeError) as exc:
        row["detail"] = f"{type(exc).__name__}: {exc}"[:200]
        return row
    try:
        rows, tip = entry["tip_rows"](path)
    except (OSError, ValueError, KeyError, TypeError, ImportError):
        # tip/rows is metering, never a verdict: the verify word already landed
        row["tip_unreadable"] = True
    else:
        row["rows"], row["tip"] = rows, tip
    return row


def verify_all(entries: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """The chain table: one row per mounted chain, each judged by its own verify."""
    entries = default_families() if entries is None else entries
    rows: list[dict[str, Any]] = []
    for entry in entries:
        for label, path in discover(entry):
            rows.append(_one_chain(entry, label, path))
    return {
        "rows": rows,
        "chains": len(rows),
        "failing": [r for r in rows if not r["ok"]],
        "cannot_verify": any(r.get("cannot_verify") for r in rows),
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def render_table(result: dict[str, Any]) -> str:
    lines = [f"LEDGER REGISTRY verify_all {result['ts']}"]
    fam_order: list[str] = []
    for r in result["rows"]:
        if r["family"] not in fam_order:
            fam_order.append(r["family"])
    for fam in fam_order:
        fam_rows = [r for r in result["rows"] if r["family"] == fam]
        lines.append(f"family {fam} — {len(fam_rows)} chain(s)")
        for r in fam_rows:
            tip = (r.get("tip") or "")[:16] or "-"
            mark = "OK  " if r["ok"] else "FAIL"
            lines.append(f"  {mark} {r['chain']} rows={r['rows']} tip={tip} {r['detail']}")
    lines.append(f"TOTAL chains={result['chains']} failing={len(result['failing'])}")
    return "\n".join(lines)


# ── nightly canary: idempotent attention alerts (gap_sentinel law) ──


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _alerted_keys(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    keys: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row.get("key"), str):
            keys.add(row["key"])
    return keys


def _file_alert(attention_p: Path, alerted_p: Path, key: str, block: str, now: datetime) -> bool:
    """Idempotent: jsonl record first (single writer), attention.md second.
    True only when newly filed (stolen-and-credited from tools/gap_sentinel.py)."""
    if key in _alerted_keys(alerted_p):
        return False
    text = attention_p.read_text(encoding="utf-8", errors="replace") if attention_p.is_file() else ""
    if f"- key: {key}" in text:
        _append_jsonl(alerted_p, {"ts": now.isoformat(), "key": key, "healed": True})
        return False
    _append_jsonl(alerted_p, {"ts": now.isoformat(), "key": key})
    attention_p.parent.mkdir(parents=True, exist_ok=True)
    with attention_p.open("a", encoding="utf-8") as fh:
        fh.write(block)
    return True


def _alert_block(stamp_local: str, verdict: str, key: str) -> str:
    return (
        "\n---\n\n"
        f"### Ledger registry canary fired ({stamp_local})\n\n"
        f"- verdict: {verdict} (exit 1)\n"
        "- record: `logs/ledger_registry/alerted.jsonl` (single-writer truth; this "
        "attention.md block is best-effort per the B2-465 multi-writer law)\n"
        f"- response: {CANARY_RESPONSE}\n"
        f"- key: {key}\n"
    )


def canary(root: Path = ESTATE_ROOT, entries: list[dict[str, Any]] | None = None,
           now: datetime | None = None) -> int:
    """Nightly pass: verify_all, then alert once per failure-origin key."""
    now = now or datetime.now(timezone.utc)
    result = verify_all(entries)
    if result["cannot_verify"]:
        print("LEDGER-REGISTRY: cannot verify — a family's own verify module "
              "failed to import; no chain verdict, no alerts")
        return 2
    stamp_local = now.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    filed: list[str] = []
    for r in result["failing"]:
        key = f"ledger-registry {r['family']} {r['chain']} {r['detail']}"
        verdict = (f"LEDGER-REGISTRY: CHAIN-FAIL - {r['family']} {r['chain']}: "
                   f"{r['detail']} ({len(result['failing'])}/{result['chains']} chains failing)")
        block = _alert_block(stamp_local, verdict, key)
        if _file_alert(root / ATTENTION_RELPATH, root / ALERTED_RELPATH, key, block, now):
            filed.append(key)
            print(f"  alert filed key: {key}")
        else:
            print(f"  alert already on file, not duplicated key: {key}")
    _append_jsonl(root / RUNS_RELPATH,
                  {"ts": now.isoformat(), "exit": 1 if result["failing"] else 0,
                   "chains": result["chains"], "failing": len(result["failing"]),
                   "filed": filed})
    return 1 if result["failing"] else 0


# ── query-by-hash stub (cross-ledger receipt hash; index is v1 debt 2026-09-29) ──


def query_by_hash(prefix: str, entries: list[dict[str, Any]] | None = None,
                  limit: int = QUERY_LIMIT) -> list[dict[str, Any]]:
    """Scan mounted chains for rows whose top-level hash field matches the
    prefix. Stub scope: top-level row hashes only (wow hash, gwap row_sha256,
    world sha, verkle leaf_hash); nested evidence hashes (gwap
    meter_credit.receipt_sha256) are v1 debt (2026-09-29)."""
    entries = default_families() if entries is None else entries
    if not prefix or any(c not in "0123456789abcdefABCDEF" for c in prefix):
        return []
    hits: list[dict[str, Any]] = []
    for entry in entries:
        for label, path in discover(entry):
            for no, row in entry["iter_rows"](path):
                for field in entry["hash_fields"]:
                    value = row.get(field)
                    if isinstance(value, str) and value.startswith(prefix):
                        hits.append({"family": entry["name"], "chain": label,
                                     "row": no, "field": field, "hash": value})
                        if len(hits) >= limit:
                            return hits
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ledger-registry",
                                 description="one mount table for every estate hash-chain")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verify", help="run every chain's own verify; print the table")
    sub.add_parser("canary", help="nightly: verify + idempotent attention alerts")
    q = sub.add_parser("query", help="cross-ledger receipt-hash lookup (stub)")
    q.add_argument("--hash", required=True, help="hex prefix of the row/receipt hash")
    args = ap.parse_args(argv)
    if args.cmd == "verify":
        result = verify_all()
        print(render_table(result))
        if result["cannot_verify"]:
            return 2
        return 1 if result["failing"] else 0
    if args.cmd == "canary":
        return canary()
    hits = query_by_hash(args.hash.strip())
    for h in hits:
        print(json.dumps(h))
    print(f"query: {len(hits)} hit(s) for prefix {args.hash.strip()!r} "
          f"(stub: top-level row hashes only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
