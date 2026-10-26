#!/usr/bin/env python3
"""ask_bank.py - versioned hidden ask bank for the duel series (AJ2, 2026-09-30).

W8 follow-up #3 / LW9 v3 groundwork. The disease: every duel so far fired
asks that live in plain sight (W8_MULTIFAMILY.md, lw9_duel_series.py), so
contender models may already have them cached or learned from the receipt
corpus. The cure: a versioned bank whose hidden half never sits in a
prompt-visible path, drawn one ask at a time for future duels.

Layout (bank root configs/ask_bank/<version_id>/): train.jsonl (14 seed
asks, tracked, safe to quote anywhere), manifest.json (version + counts +
sha256 of both halves, tracked), and hidden/ (GITIGNORED, the only
prompt-invisible surface): bank.jsonl (all 20 entries, source of truth,
survives clones only on this machine, detectable via manifest shas),
hidden.jsonl (the 6 hidden entries), draws.jsonl (draw ledger).

Contract (enforced here, restated in the receipt):
  - Only this module reads or writes anything under hidden/. The seed
    corpus (5 materials x 4 shapes = 20 fresh combinations, no W8/LW9 duel
    material reused) lives frozen in tools/ask_bank_seed.py.
  - split is deterministic: entries sorted by sha256(ask_id) ascending,
    first round(n*ratio) train, rest hidden; hidden_no hb-01.. in order.
  - Integrity: verify (exit 0 ok / 1 drift or tamper / 2 cannot verify)
    recomputes the manifest shas of train/hidden/bank plus every entry's
    material_sha256 and the .gitignore coverage of the hidden dir.
  - draw --hidden without --reveal prints ONLY the draw id, ask id, shape,
    material pointer and FIRST LINE of the ask body; --reveal prints the
    full rendered ask (body + material + laws) to stdout with the citation
    line on stderr, for the duel script to pipe into the contender prompt.
  - CONVENTION for future duels: cite "ask_bank v1 draw <draw_id>" in the
    receipt and quote at most the first line of a hidden ask there. Never
    print the hidden half whole anywhere prompt-visible.

The generator itself is tracked code: secrecy lives in the split artifacts
and the draw discipline, not in the generator (disclosed in AJ2 receipt).

Usage: python tools/ask_bank.py seed|split|verify|draw|status [--root PATH]
  seed [--force] · split [--ratio 0.7] [--force] · verify ·
  draw (--hidden | --train) [--id ASK_ID] [--reveal] [--note TEXT] · status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:  # package import (tests, python -m) with script-mode fallback (census
    # patrol pattern): plain `python tools/ask_bank.py` puts tools/ first
    from tools.ask_bank_seed import (BANKED_DUEL_MATERIALS, CREATED,
                                     GITIGNORE_RULE, LAWS, MATERIALS, RATIO,
                                     SCHEMA_ENTRY, SCHEMA_MANIFEST, SHAPES,
                                     VERSION, VERSION_ID)
except ImportError:  # pragma: no cover - script-mode path only
    _here = str(Path(__file__).resolve().parent)
    if _here not in sys.path:
        sys.path.insert(0, _here)
    from ask_bank_seed import (BANKED_DUEL_MATERIALS, CREATED, GITIGNORE_RULE,
                               LAWS, MATERIALS, RATIO, SCHEMA_ENTRY,
                               SCHEMA_MANIFEST, SHAPES, VERSION, VERSION_ID)

ESTATE_ROOT = Path(__file__).resolve().parents[1]


def bank_root(root: Path) -> Path:
    return root / "configs" / "ask_bank" / VERSION_ID


def hidden_dir(root: Path) -> Path:
    return bank_root(root) / "hidden"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_text(t: str) -> str:
    return sha_bytes(t.encode("utf-8"))


def read_material(root: Path, rel: str) -> tuple[str, str]:
    """Material sha hashes newline-normalized text on purpose: a git autocrlf
    checkout flip must never fake drift (test pins this semantics)."""
    p = root / rel
    text = p.read_text(encoding="utf-8", errors="replace")
    return text, sha_text(text)


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.is_file():
        return rows
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_jsonl_safe(path: Path) -> tuple[list[dict], int]:
    """Tamper-tolerant loader for verify: bad lines count, never crash
    (a hand-edited half is an integrity verdict, not a traceback)."""
    rows: list[dict] = []
    bad = 0
    if not path.is_file():
        return rows, bad
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            if not isinstance(row, dict) or "ask_id" not in row:
                bad += 1
                continue
            rows.append(row)
    return rows, bad


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="") as f:  # LF-stable, see split
        f.write(json.dumps(row, sort_keys=True) + "\n")


def first_line(body: str, limit: int = 120) -> str:
    for line in body.splitlines():
        if line.strip():
            return line[:limit]
    return ""


def render(entry: dict, material_text: str) -> str:
    return (entry["body"] + "\n\n<SOURCE path=" + entry["material_path"]
            + " sha256=" + entry["material_sha256"] + ">\n" + material_text
            + "\n</SOURCE>\n\n" + LAWS)


def build_entries(root: Path) -> list[dict]:
    entries: list[dict] = []
    for mat in MATERIALS:
        text, sha = read_material(root, mat["path"])
        for shape, template in SHAPES.items():
            body = template.format(path=mat["path"], title=mat["title"],
                                   angle=mat["angles"][shape])
            entries.append({
                "schema": SCHEMA_ENTRY, "ask_id": f"ab{VERSION}-{mat['key']}-{shape}",
                "bank_version": VERSION, "shape": shape,
                "material_path": mat["path"], "material_sha256": sha,
                "material_bytes": len(text.encode("utf-8")), "body": body,
                "split": None, "hidden_no": None, "created": CREATED})
    return entries


def cmd_seed(root: Path, force: bool) -> int:
    bank = hidden_dir(root) / "bank.jsonl"
    if bank.is_file() and not force:
        print(f"bank already exists ({bank}); pass --force to reseed")
        return 1
    entries = build_entries(root)
    bank.parent.mkdir(parents=True, exist_ok=True)
    with open(bank, "w", encoding="utf-8", newline="") as f:  # LF-stable, see split
        for e in entries:
            f.write(json.dumps(e, sort_keys=True) + "\n")
    mats = {m["path"] for m in MATERIALS}
    assert not (mats & set(BANKED_DUEL_MATERIALS)), "material overlap with duels"
    print(json.dumps({"seeded": len(entries), "bank": str(bank),
                      "materials": len(MATERIALS), "shapes": len(SHAPES),
                      "provenance": "fresh combinations; no W8/LW9 duel material"},
                     indent=2))
    return 0


def split_order(entries: list[dict]) -> list[dict]:
    return sorted(entries, key=lambda e: sha_text(e["ask_id"]))


def cmd_split(root: Path, ratio: float, force: bool) -> int:
    bank = hidden_dir(root) / "bank.jsonl"
    if not bank.is_file():
        print("no bank; run seed first")
        return 2
    entries = load_jsonl(bank)
    ordered = split_order(entries)
    n_train = round(len(ordered) * ratio)
    for i, e in enumerate(ordered):
        if i < n_train:
            e["split"], e["hidden_no"] = "train", None
        else:
            e["split"] = "hidden"
            e["hidden_no"] = f"hb-{i - n_train + 1:02d}"
    train_p = bank_root(root) / "train.jsonl"
    hidden_p = hidden_dir(root) / "hidden.jsonl"
    manifest_p = bank_root(root) / "manifest.json"

    def write_rows(path: Path, rows: list[dict]) -> bytes:
        path.parent.mkdir(parents=True, exist_ok=True)
        blob = "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows)
        # newline="" keeps LF on Windows (text-mode write would CRLF-translate
        # the disk bytes away from the hashed bytes; caught by verify on the
        # first real run 2026-09-30); sha comes from disk, never from memory.
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(blob)
        return path.read_bytes()

    train_blob = write_rows(train_p, ordered[:n_train])
    hidden_blob = write_rows(hidden_p, ordered[n_train:])
    manifest = {
        "schema": SCHEMA_MANIFEST, "bank_version": VERSION,
        "version_id": VERSION_ID, "created": CREATED,
        "counts": {"total": len(ordered), "train": n_train,
                   "hidden": len(ordered) - n_train},
        "ratio": ratio,
        "split_rule": ("entries sorted by sha256(ask_id) hex ascending; first "
                       "round(n*ratio) train, rest hidden; hidden_no assigned "
                       "hb-01.. in that order"),
        "sha256": {"bank": sha_bytes(bank.read_bytes()),
                   "train": sha_bytes(train_blob), "hidden": sha_bytes(hidden_blob)},
        "materials": [{"path": m["path"], "asks": len(SHAPES)} for m in MATERIALS],
        "provenance": ("fresh combinations (AJ2); W8/LW9 duel materials excluded: "
                       + ", ".join(BANKED_DUEL_MATERIALS)),
        "convention": ("future duels draw via `draw --hidden --reveal` and cite "
                       "'ask_bank v1 draw <draw_id>'; receipts quote at most the "
                       "drawn ask's first line; hidden half never printed whole "
                       "in any prompt-visible path"),
    }
    if manifest_p.is_file() and not force:
        old = json.loads(manifest_p.read_text(encoding="utf-8"))
        if old.get("sha256") != manifest["sha256"]:
            print("manifest exists with different shas; pass --force to overwrite")
            return 1
    manifest_p.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8", newline="")
    print(json.dumps({"split": manifest["counts"],
                      "train_sha256": manifest["sha256"]["train"],
                      "hidden_sha256": manifest["sha256"]["hidden"],
                      "manifest": str(manifest_p)}, indent=2))
    return 0


def cmd_verify(root: Path) -> int:
    br = bank_root(root)
    bank, train_p = hidden_dir(root) / "bank.jsonl", br / "train.jsonl"
    hidden_p, manifest_p = hidden_dir(root) / "hidden.jsonl", br / "manifest.json"
    problems: list[str] = []
    for p in (bank, train_p, hidden_p, manifest_p):
        if not p.is_file():
            problems.append(f"missing artifact {p.name}")
    if problems:
        for p in problems:
            print(f"CANNOT VERIFY: {p}")
        return 2
    man = json.loads(manifest_p.read_text(encoding="utf-8"))
    for name, p in (("bank", bank), ("train", train_p), ("hidden", hidden_p)):
        got = sha_bytes(p.read_bytes())
        if got != man["sha256"].get(name):
            problems.append(f"{name} sha drift: manifest {man['sha256'].get(name)}"
                            f" vs file {got}")
    entries, bad_bank = load_jsonl_safe(bank)
    train_rows, bad_train = load_jsonl_safe(train_p)
    hidden_rows, bad_hidden = load_jsonl_safe(hidden_p)
    for name, bad in (("bank", bad_bank), ("train", bad_train),
                      ("hidden", bad_hidden)):
        if bad:
            problems.append(f"{bad} malformed rows in {name}")
    train_ids = {e["ask_id"] for e in train_rows}
    hidden_ids = {e["ask_id"] for e in hidden_rows}
    all_ids = {e["ask_id"] for e in entries}
    if train_ids & hidden_ids:
        problems.append(f"overlap {sorted(train_ids & hidden_ids)}")
    if train_ids | hidden_ids != all_ids:
        problems.append("train plus hidden does not cover bank")
    counts = man.get("counts", {})
    if counts.get("train") != len(train_ids) or counts.get("hidden") != len(hidden_ids):
        problems.append(f"count drift: manifest {counts} vs files "
                        f"{len(train_ids)}/{len(hidden_ids)}")
    for e in entries:
        try:
            _, sha = read_material(root, e["material_path"])
        except OSError:
            problems.append(f"material unreadable at {e['material_path']}")
            break
        if sha != e["material_sha256"]:
            problems.append(f"material drift at {e['material_path']}")
            break
    gi = root / ".gitignore"
    gi_text = gi.read_text(encoding="utf-8", errors="replace") if gi.is_file() else ""
    if GITIGNORE_RULE not in gi_text:
        problems.append(".gitignore lacks the hidden dir rule")
    if problems:
        for p in problems:
            print(f"ASK-BANK INTEGRITY: {p}")
        return 1
    print(json.dumps({"ask_bank": man["version_id"], "ok": True,
                      "counts": counts, "draws": len(load_jsonl(hidden_dir(root)
                                                                / "draws.jsonl"))}))
    return 0


def cmd_draw(root: Path, half: str, ask_id: str | None, reveal: bool,
             note: str) -> int:
    man_p = bank_root(root) / "manifest.json"
    if not man_p.is_file():
        print("no manifest; run split first")
        return 2
    man = json.loads(man_p.read_text(encoding="utf-8"))
    src = (hidden_dir(root) / "hidden.jsonl" if half == "hidden"
           else bank_root(root) / "train.jsonl")
    rows = load_jsonl(src)
    if not rows:
        print(f"no {half} rows")
        return 2
    ledger = load_jsonl(hidden_dir(root) / "draws.jsonl")
    drawn = [r["ask_id"] for r in ledger if r.get("half") == half]
    if ask_id:
        match = [e for e in rows if e["ask_id"] == ask_id]
        if not match:
            print(f"ask_id {ask_id} not in {half} half")
            return 2
        entry = match[0]
    else:
        entry = min(rows, key=lambda e: (drawn.count(e["ask_id"]),
                                         rows.index(e)))
    seq = len(drawn) + 1
    draw_id = f"v{VERSION}{'h' if half == 'hidden' else 't'}-{seq:04d}"
    append_jsonl(hidden_dir(root) / "draws.jsonl", {
        "draw_id": draw_id, "ask_id": entry["ask_id"], "half": half,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": note or ""})
    if reveal:
        text, _ = read_material(root, entry["material_path"])
        print(f"[ask_bank {man['version_id']} draw {draw_id} "
              f"{entry['ask_id']}]", file=sys.stderr)
        print(render(entry, text))
    else:
        print(json.dumps({
            "bank": man["version_id"], "draw_id": draw_id,
            "ask_id": entry["ask_id"], "half": half, "shape": entry["shape"],
            "material_path": entry["material_path"],
            "material_sha256": entry["material_sha256"],
            "first_line": first_line(entry["body"])}, indent=2))
    return 0


def cmd_status(root: Path) -> int:
    man_p = bank_root(root) / "manifest.json"
    if not man_p.is_file():
        print(f"ask_bank {VERSION_ID}: not split yet (no manifest)")
        return 0
    man = json.loads(man_p.read_text(encoding="utf-8"))
    ledger = load_jsonl(hidden_dir(root) / "draws.jsonl")
    print(json.dumps({"bank": man["version_id"], "counts": man["counts"],
                      "draws_total": len(ledger),
                      "draws_hidden": sum(1 for r in ledger
                                          if r.get("half") == "hidden"),
                      "last_draw": ledger[-1]["draw_id"] if ledger else None,
                      "convention": man["convention"]}, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="versioned hidden ask bank (AJ2)")
    p.add_argument("--root", type=Path, default=ESTATE_ROOT)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("seed"); s.add_argument("--force", action="store_true")
    s = sub.add_parser("split"); s.add_argument("--force", action="store_true")
    s.add_argument("--ratio", type=float, default=RATIO)
    sub.add_parser("verify")
    d = sub.add_parser("draw")
    half = d.add_mutually_exclusive_group()
    half.add_argument("--hidden", action="store_true", help="draw from hidden half")
    half.add_argument("--train", action="store_true", help="draw from train half")
    d.add_argument("--id", dest="ask_id", help="draw this exact ask_id")
    d.add_argument("--reveal", action="store_true",
                   help="print the full rendered ask (stdout; citation to stderr)")
    d.add_argument("--note", default="", help="recorded in the draw ledger")
    sub.add_parser("status")
    args = p.parse_args(argv)
    root = args.root.resolve()
    if args.cmd == "seed":
        return cmd_seed(root, args.force)
    if args.cmd == "split":
        return cmd_split(root, args.ratio, args.force)
    if args.cmd == "verify":
        return cmd_verify(root)
    if args.cmd == "draw":
        half = "hidden" if args.hidden else "train"
        return cmd_draw(root, half, args.ask_id, args.reveal, args.note)
    return cmd_status(root)


if __name__ == "__main__":
    sys.exit(main())
