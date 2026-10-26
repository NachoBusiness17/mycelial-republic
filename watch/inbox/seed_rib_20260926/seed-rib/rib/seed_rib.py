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

Usage:
  .venv/Scripts/python.exe tools/seed_rib.py build --root . --out seed.json \
      --file docs/DNA.md --glob "memory/law/*.md"
  .venv/Scripts/python.exe tools/seed_rib.py verify --seed seed.json \
      --into /tmp/rebuilt [--source .]
Exit 0 on success, 1 on any seal/structure mismatch, 2 on cannot-verify.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "seed_rib.v0"
DEFAULT_INLINE_MAX = 8192
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


def build(root: Path, files: list[str], globs: list[str],
          inline_max: int, out_path: Path) -> dict:
    entries = []
    law_refs: list[str] = []
    for p in expand_inputs(root, files, globs):
        rel = rel_of(root, p)
        if rel.startswith("/") or ".." in rel.split("/"):
            print(f"void path refused: {rel}")
            return {}
        raw = p.read_bytes()
        seal = hashlib.sha256(raw).hexdigest()
        entry = {"path": rel, "role": classify_role(rel), "bytes": len(raw),
                 "sha256": seal,
                 "carrier": "inline" if len(raw) <= inline_max else "pointer"}
        if entry["carrier"] == "inline":
            entry["content_b64"] = base64.b64encode(raw).decode("ascii")
        entries.append(entry)
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
          f"law_refs {len(law_refs)}")
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
    print(f"SEED-RIB verify: inline {inl_ok} hash-matched, pointers "
          f"{ptr_res} source-checked / {ptr_unres} UNRESOLVED (stubbed, named), "
          f"law_refs {len(seed.get('law_refs', []))}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="SEED-RIB v0 build/verify")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--root", default=".")
    b.add_argument("--out", required=True)
    b.add_argument("--file", action="append", default=[])
    b.add_argument("--glob", action="append", default=[])
    b.add_argument("--inline-max", type=int, default=DEFAULT_INLINE_MAX)
    v = sub.add_parser("verify")
    v.add_argument("--seed", required=True)
    v.add_argument("--into", required=True)
    v.add_argument("--source", default=None)
    a = ap.parse_args()
    if a.cmd == "build":
        seed = build(Path(a.root).resolve(), a.file, a.glob, a.inline_max, Path(a.out))
        return 0 if seed else 2
    src = Path(a.source).resolve() if a.source else None
    return verify(Path(a.seed), Path(a.into), src)


if __name__ == "__main__":
    sys.exit(main())
