"""FW-14 ghost-ref noise sampler (2026-09-28, fifty_wide_20260917).

Recomputes the census ghost-ref set with the 09-28-fixed instrument
(mag.prose_census._REF_RE: mdx/jsonl alternation order + URL strip), then draws a
deterministic systematic sample of 50 (file, ref) pairs — every Nth ref in
path-sorted order — and prints the referencing line for eyeball classification.

Run: ./.venv/Scripts/python.exe watch/inbox/fifty_wide_20260917/FW14_sample50.py
"""

import re
from pathlib import Path

import mag.prose_census as pc

ROOT = Path(__file__).resolve().parents[3]
SAMPLE_N = 50


def all_dead():
    files = []
    for p in ROOT.glob("*.md"):
        files.append(p)
    for top in pc.WALK_TOPS:
        d = ROOT / top
        if not d.is_dir():
            continue
        for p in d.rglob("*.md"):
            if any(part in pc.SKIP_DIRS for part in p.parts[len(ROOT.parts):]):
                continue
            files.append(p)

    pairs = []
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        text = re.sub(r"https?://\S+", "", text)
        rel = str(p.relative_to(ROOT))
        for line_no, line in enumerate(text.splitlines(), 1):
            for ref in pc._REF_RE.findall(line):
                if not (ROOT / ref).exists():
                    pairs.append((rel, ref, line_no, line.strip()[:200]))
    return pairs


def main():
    pairs = all_dead()
    # refs are line-scoped here (may duplicate across lines); dedupe per (file,ref,context)
    seen, uniq = set(), []
    for t in pairs:
        k = (t[0], t[1], t[2])
        if k not in seen:
            seen.add(k)
            uniq.append(t)
    step = max(1, len(uniq) // SAMPLE_N)
    sample = uniq[::step][:SAMPLE_N]
    print(f"population: {len(uniq)} dead (file,line,ref) hits across {len({t[0] for t in uniq})} files; "
          f"step={step}; sample={len(sample)}")
    for rel, ref, line_no, line in sample:
        print(f"\n--- {rel}:{line_no} ref=`{ref}`\n    {line}")


if __name__ == "__main__":
    main()
