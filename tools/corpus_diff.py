"""corpus_diff — diff similarly-named files in a corpus, produce training data.

Motivation (operator, 2026-08-08): the #aiTruthCode corpus is full of versioned
near-duplicates (e.g. "v71.5: The Relationship Bridge" vs "v71.8: The Ancestral
Compass Lock", "GTC-GEE_v84" vs "GTC-GEE_v84.0", "GTC_v119"). Diffing them shows
how these prompt-systems evolved and WHY — high-quality training data.

Approach (deterministic, "bytes not vibes"):
  * group files per folder by a normalized stem (version tokens stripped)
  * sort each group by version number, then unified-diff consecutive versions
  * emit a per-folder markdown report (what changed) + structured records to a
    training jsonl (added/removed lines, similarity, delta categories)

Usage:
  python -m tools.corpus_diff <corpus_dir> [--out <report_dir>] [--min-ratio 0.3]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Family prefixes (GTC/GTR/GEE/...) are MEANINGFUL (they name the system family),
# so keep them; only strip version numbers (handled by the version-token rule).
STOP = {"the", "of", "and", "to", "a", "shared", "folder"}


def _norm_key(name: str) -> str:
    toks = re.split(r"[^A-Za-z0-9]+", name.lower())
    keep: list[str] = []
    for t in toks:
        if not t:
            continue
        if re.fullmatch(r"v?\d+(\.\d+)*", t):
            continue  # pure version token
        if t in STOP:
            continue
        keep.append(t)
    return " ".join(keep)


def _version(name: str) -> tuple:
    m = re.search(r"v?\b(\d+(?:\.\d+)*)", name.lower())
    if not m:
        return (999999,)
    return tuple(int(x) for x in m.group(1).split("."))


def _group_files(files: list[Path]) -> list[list[Path]]:
    buckets: dict[str, list[Path]] = {}
    for f in files:
        buckets.setdefault(_norm_key(f.stem), []).append(f)
    groups = []
    for key, fs in buckets.items():
        if len(fs) >= 2 and key:  # need >=2 near-duplicates
            fs.sort(key=lambda p: (_version(p.name), p.name))
            groups.append(fs)
    return groups


def _diff_pair(a: Path, b: Path) -> dict:
    ta = a.read_text(encoding="utf-8", errors="replace").splitlines()
    tb = b.read_text(encoding="utf-8", errors="replace").splitlines()
    sm = difflib.SequenceMatcher(None, ta, tb)
    ratio = round(sm.ratio(), 3)
    added = [l[2:] for l in tb if l not in ta]  # heuristic; refined below
    ud = list(difflib.unified_diff(ta, tb, fromfile=a.name, tofile=b.name, lineterm=""))
    added_lines, removed_lines, changed = [], [], []
    for line in ud[2:]:
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:].strip())
        elif line.startswith("-") and not line.startswith("---"):
            removed_lines.append(line[1:].strip())
    # categorize changed lines by keyword
    cats: dict[str, int] = {}
    def _cat(line: str) -> None:
        l = line.lower()
        for k in ("command", "symbol", "version", "praise", "protocol", "shield",
                  "gate", "key", "merge", "code", "number", "name", "response",
                  "level", "module", "flag", "lock", "symphony", "kernel"):
            if k in l:
                cats[k] = cats.get(k, 0) + 1
    for l in added_lines + removed_lines:
        _cat(l)
    return {
        "from": a.name, "to": b.name,
        "similarity": ratio,
        "added": len(added_lines), "removed": len(removed_lines),
        "net_lines": len(added_lines) - len(removed_lines),
        "categories": dict(sorted(cats.items(), key=lambda kv: -kv[1])),
        "added_sample": added_lines[:8],
        "removed_sample": removed_lines[:8],
    }


def run(corpus: Path, out: Path, min_ratio: float) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    training: list[dict] = []
    reports: list[dict] = []
    groups_seen = 0
    for folder in sorted(p for p in corpus.iterdir() if p.is_dir()):
        files = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in (".txt", ".md", ".csv") and not p.name.startswith("_"))
        if not files:
            continue
        groups = _group_files(files)
        if not groups:
            continue
        groups_seen += len(groups)
        lines = [f"# {folder.name}", ""]
        for g in groups:
            lines.append(f"## cluster: {_norm_key(g[0].stem)}  ({len(g)} versions)")
            lines.append("")
            for a, b in zip(g, g[1:]):
                d = _diff_pair(a, b)
                if d["similarity"] < min_ratio:
                    continue
                rec = {"schema": "corpus_diff.v1", "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       "folder": folder.name, "cluster": _norm_key(g[0].stem), **d}
                training.append(rec)
                lines.append(f"### {a.name} -> {b.name}")
                lines.append(f"- similarity {d['similarity']} | +{d['added']}/-{d['removed']} (net {d['net_lines']:+d})")
                lines.append(f"- delta categories: {d['categories'] or 'none'}")
                if d["removed_sample"]:
                    lines.append(f"- removed e.g.: {d['removed_sample'][:4]}")
                if d["added_sample"]:
                    lines.append(f"- added e.g.: {d['added_sample'][:4]}")
                lines.append("")
        if len(lines) > 2:
            slug = re.sub(r"[^A-Za-z0-9]+", "_", folder.name).strip("_") or "folder"
            rp = out / f"{slug}.md"
            rp.write_text("\n".join(lines), encoding="utf-8")
            reports.append({"folder": folder.name, "report": str(rp), "clusters": len(groups)})

    tp = out / "_training.jsonl"
    with tp.open("w", encoding="utf-8") as fh:  # regenerate (idempotent for cadence)
        for rec in training:
            fh.write(json.dumps(rec, default=str) + "\n")
    return {"groups_seen": groups_seen, "diff_records": len(training),
            "reports": len(reports), "report_dir": str(out), "training_file": str(tp)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("corpus")
    ap.add_argument("--out", default="")
    ap.add_argument("--min-ratio", type=float, default=0.3)
    args = ap.parse_args()
    corpus = Path(args.corpus)
    out = Path(args.out) if args.out else corpus / "_diffs"
    res = run(corpus, out, args.min_ratio)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
