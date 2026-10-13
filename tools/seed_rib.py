#!/usr/bin/env python3
"""seed_rib.py - SEED-RIB v0 generator + rebuild verifier (B2-180, 2026-09-26).

Spec: watch/inbox/SEED_RIB_FORMAT_v0_20260926.md (schema seed_rib.v0).
The seed merges the seed concept with the warmed RIB: a kilobyte JSON that
carries the boot kernel inline (sha256-sealed) and seals everything heavy as
hash pointers, so an agent can recreate the structure from kilobytes.

  build  estate subtree/file-list -> seed JSON (inline small, seal large)
  verify seed -> rebuilt tree -> hash-compare (inline exact, pointers named)

Fail-closed laws: a listed file that vanishes before sealing is a hard error;
an absolute or escaping path is void; the verifier never invents pointer bytes
(it writes <path>.SEED_POINTER stubs carrying the seal) and only passes when
every inline entry hash-matches its seal and every pointer is either
--source-checked or reported UNRESOLVED by name.
Budget law (w4-08 correction 3, 2026-09-28): the 100KB budget binds the
DECODED inline payload, not the report - build refuses and verify fails when
sum(inline entry bytes) exceeds BUDGET_BYTES. Quine law (w4-08 correction 1):
the generator must ride inline in its own seed; build refuses otherwise.
Freshness SLO (w4-08 correction 2): a seed older than FRESHNESS_DAYS is past
its measured pointer half-life and should be re-rendered (reported, not
enforced in exit code); any verify exit 1 voids watch/inbox/SEED_RIB_CURRENT.

Usage:
  .venv/Scripts/python.exe tools/seed_rib.py build --root . --out seed.json \
      --file docs/DNA.md --glob "memory/law/*.md" [--pointer-list paths.txt]
  .venv/Scripts/python.exe tools/seed_rib.py verify --source .
      # default seed = watch/inbox/SEED_RIB_CURRENT resolved; --into optional
Exit 0 on success, 1 on any seal/structure mismatch, 2 on cannot-verify.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "seed_rib.v0"
DEFAULT_INLINE_MAX = 8192
BUDGET_BYTES = 100000
FRESHNESS_DAYS = 3
CURRENT_PTR = "watch/inbox/SEED_RIB_CURRENT"
LEVERS = ("L1 pointer-ize VSCODE.md; L2 TOUR.md+SALON.md; L3 MORNING_LOOP.md; "
          "L4 ACCOUNTS.md; L5 tighten kernel caps to B2-300 minimums")
ROLES = ("law", "doctrine", "boot", "receipt", "ledger", "pointer")


def classify_role(rel: str) -> str:
    if rel.startswith("memory/law/"):
        return "law"
    if rel.startswith("docs/") or rel in ("CONSTITUTION.md",):
        return "doctrine"
    if rel == "AGENTS.md" or rel.startswith("state/") or "handoff" in rel.lower():
        return "boot"
    if rel.startswith("watch/inbox/"):
        return "receipt"
    if rel.endswith(".jsonl"):
        return "ledger"
    return "pointer"


def expand_inputs(root: Path, files: list[str], globs: list[str]) -> list[Path]:
    out: list[Path] = []
    for f in files:
        p = (root / f)
        if not p.is_file():
            raise SystemExit(f"2 cannot verify, listed file missing: {f}")
        out.append(p)
    for g in globs:
        out.extend(p for p in sorted(root.glob(g)) if p.is_file())
    # dedupe, preserve order
    seen: set[Path] = set()
    uniq = []
    for p in out:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            uniq.append(p)
    return uniq


def rel_of(root: Path, p: Path) -> str:
    return p.resolve().relative_to(root.resolve()).as_posix()


def resolve_current(root: Path) -> Path:
    """Resolve the SEED_RIB_CURRENT pointer doc (JSON) to the live seed path."""
    doc = json.loads((root / CURRENT_PTR).read_text(encoding="utf-8"))
    return root / doc["pointer"]["path"]


def expand_pointer_list(root: Path, listfile: str) -> list[Path]:
    """Paths (one per line, # comments) force-carried as pointer entries."""
    out: list[Path] = []
    for line in (root / listfile).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = root / line
        if not p.is_file():
            raise SystemExit(f"2 cannot verify, pointer-listed file missing: {line}")
        out.append(p)
    return out


def build(root: Path, files: list[str], globs: list[str], pointer_list: str | None,
          inline_max: int, out_path: Path) -> dict:
    inputs = expand_inputs(root, files, globs)
    forced = expand_pointer_list(root, pointer_list) if pointer_list else []
    force = {p.resolve() for p in forced}
    # dedupe across kernel inputs and the pointer list (force wins the carrier)
    seen: set[Path] = set()
    ordered: list[Path] = []
    for p in inputs + forced:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            ordered.append(p)
    entries = []
    law_refs: list[str] = []
    for p in ordered:
        rel = rel_of(root, p)
        if rel.startswith("/") or ".." in rel.split("/"):
            print(f"void path refused: {rel}")
            return {}
        raw = p.read_bytes()
        seal = hashlib.sha256(raw).hexdigest()
        carrier = ("pointer" if p.resolve() in force
                   else "inline" if len(raw) <= inline_max else "pointer")
        entry = {"path": rel, "role": classify_role(rel), "bytes": len(raw),
                 "sha256": seal, "carrier": carrier}
        if carrier == "inline":
            entry["content_b64"] = base64.b64encode(raw).decode("ascii")
        entries.append(entry)
    gen = Path(__file__).resolve()
    try:
        grel = gen.relative_to(root).as_posix()
    except ValueError:
        grel = None
    if grel is not None:
        ge = next((e for e in entries if e["path"] == grel), None)
        if ge is None or ge.get("carrier") != "inline":
            print(f"cannot verify, quine law: generator {grel} must ride inline "
                  f"in its own seed (shrink it or raise --inline-max)")
            return {}
    decoded = sum(e["bytes"] for e in entries if e["carrier"] == "inline")
    if decoded > BUDGET_BYTES:
        print(f"cannot verify, decoded inline payload {decoded} > budget "
              f"{BUDGET_BYTES} B; levers: {LEVERS}")
        return {}
    reg = root / "memory" / "law" / "registry.json"
    if reg.is_file():
        try:
            law_refs = sorted(json.loads(reg.read_text(encoding="utf-8")).keys())
        except Exception as exc:  # noqa: BLE001
            print(f"cannot verify, registry unparseable: {exc}")
            return {}
    seed = {"schema": SCHEMA,
            "created_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_root": root.resolve().name,
            "inline_max_bytes": inline_max,
            "entries": entries,
            "law_refs": law_refs}
    out_path.write_text(json.dumps(seed, indent=1), encoding="utf-8")
    inl = [e for e in entries if e["carrier"] == "inline"]
    print(f"SEED-RIB build: {len(entries)} entries ({len(inl)} inline, "
          f"{len(entries) - len(inl)} pointer), seed {out_path.stat().st_size} bytes, "
          f"decoded payload {decoded}/{BUDGET_BYTES} B, law_refs {len(law_refs)}")
    return seed


def verify(seed_path: Path, into: Path, source: Path | None) -> int:
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    if seed.get("schema") != SCHEMA:
        print(f"cannot verify, schema {seed.get('schema')!r} != {SCHEMA!r}")
        return 2
    into.mkdir(parents=True, exist_ok=True)
    ok = True
    inl_ok = ptr_res = ptr_unres = 0
    for e in seed.get("entries", []):
        rel = e["path"]
        if rel.startswith("/") or ".." in rel.split("/"):
            print(f"VOID path in seed: {rel}")
            ok = False
            continue
        target = into / rel
        if e.get("carrier") == "inline":
            raw = base64.b64decode(e.get("content_b64", ""))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            if hashlib.sha256(raw).hexdigest() == e["sha256"] and len(raw) == e["bytes"]:
                inl_ok += 1
            else:
                print(f"SEAL MISMATCH (inline): {rel}")
                ok = False
        else:
            resolved = False
            if source is not None:
                sp = source / rel
                if sp.is_file():
                    live = hashlib.sha256(sp.read_bytes()).hexdigest()
                    if live == e["sha256"]:
                        ptr_res += 1
                        resolved = True
                    else:
                        print(f"SEAL MISMATCH (pointer vs source): {rel}")
                        ok = False
                        resolved = True
            if not resolved:
                stub = into / (rel + ".SEED_POINTER")
                stub.parent.mkdir(parents=True, exist_ok=True)
                stub.write_text(f"seed_rib.v0 pointer sha256={e['sha256']} bytes={e['bytes']}\n",
                                encoding="utf-8")
                ptr_unres += 1
    decoded = sum(e["bytes"] for e in seed.get("entries", [])
                  if e.get("carrier") == "inline")
    if decoded > BUDGET_BYTES:
        print(f"SEAL MISMATCH (budget): decoded inline payload {decoded} > "
              f"{BUDGET_BYTES} B; levers: {LEVERS}")
        ok = False
    reg = next((e for e in seed.get("entries", [])
                if e.get("path") == "memory/law/registry.json"
                and e.get("carrier") == "inline"), None)
    if reg is not None:
        try:
            ids = set(json.loads(base64.b64decode(reg.get("content_b64", ""))).keys())
        except Exception:  # noqa: BLE001 - unreadable carried registry fails below
            ids = set()
        phantom = [r for r in seed.get("law_refs", []) if r not in ids]
        if phantom:
            print(f"SEAL MISMATCH (law_refs not in carried registry): {phantom}")
            ok = False
    try:
        built = datetime.strptime(seed.get("created_ts", ""),
                                  "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        age = (datetime.now(timezone.utc) - built).days
    except ValueError:
        age = -1
    if age > FRESHNESS_DAYS:
        print(f"WARNING (freshness SLO): seed age {age}d > {FRESHNESS_DAYS}d "
              f"measured pointer half-life; re-render and refresh {CURRENT_PTR}")
    print(f"SEED-RIB verify: inline {inl_ok} hash-matched, pointers "
          f"{ptr_res} source-checked / {ptr_unres} UNRESOLVED (stubbed, named), "
          f"law_refs {len(seed.get('law_refs', []))}, "
          f"decoded payload {decoded}/{BUDGET_BYTES} B, seed age {age}d "
          f"(rebuild SLO {FRESHNESS_DAYS}d)")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="SEED-RIB v0 build/verify")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--root", default=".")
    b.add_argument("--out", required=True)
    b.add_argument("--file", action="append", default=[])
    b.add_argument("--glob", action="append", default=[])
    b.add_argument("--pointer-list", default=None,
                   help="file of paths (one per line, # comments) carried as pointers")
    b.add_argument("--inline-max", type=int, default=DEFAULT_INLINE_MAX)
    v = sub.add_parser("verify")
    v.add_argument("--seed", default=None,
                   help="seed JSON (default: resolve watch/inbox/SEED_RIB_CURRENT)")
    v.add_argument("--into", default=None,
                   help="rebuild target dir (default: a fresh temp dir)")
    v.add_argument("--source", default=None)
    a = ap.parse_args()
    if a.cmd == "build":
        seed = build(Path(a.root).resolve(), a.file, a.glob, a.pointer_list,
                     a.inline_max, Path(a.out))
        return 0 if seed else 2
    src = Path(a.source).resolve() if a.source else None
    base = src if src is not None else Path.cwd()
    seed_p = Path(a.seed) if a.seed else resolve_current(base)
    into = Path(a.into) if a.into else Path(tempfile.mkdtemp(prefix="seed_rib_verify_"))
    return verify(seed_p, into, src)


if __name__ == "__main__":
    sys.exit(main())
