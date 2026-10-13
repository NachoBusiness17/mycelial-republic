#!/usr/bin/env python3
"""Calcifer backlog receipt feed.

Receipts INTAKE cards (watch/INTAKE_*20260903*.md, watch/INTAKE_*20260904*.md)
that were never mentioned in watch/room.jsonl, closing the consumption-starved
corpus found by memory/audit/aud_research.json (101 of 189 cards unreceipted).

Stdlib only. $0. No model calls. Never echoes secrets. Never modifies the cards.
Honesty: cards without a parseable score line are receipted as "unscored";
scores are extracted verbatim from the card, never fabricated.
"""
import json
import re
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / "watch"
ROOM = WATCH / "room.jsonl"
STATS = ROOT / "memory" / "audit" / "calcifer_feed_stats.json"
CAP = 120
DAYS = ("20260904", "20260903")

SCORE_RE = re.compile(r"(\d{1,2})\s*/\s*25\b")
BAND_RE = re.compile(r"\b(BUILD|CALIBRATE|REMEMBER|REJECT)\b")
INNER_SLUG_RE = re.compile(r"Slug\s+`?([A-Z0-9_]{12,})")
DATE_SUFFIX_RE = re.compile(r"_20\d{6}[a-z]?$")


def parse_card(path):
    """Return (score_str_or_None, first_gist_able_line, inner_slug_or_None)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, "", None
    lines = text.splitlines()

    # Prefer lines that talk about SCORE, then any line carrying N/25.
    cand = [i for i, l in enumerate(lines) if "score" in l.lower()]
    cand += [i for i, l in enumerate(lines) if SCORE_RE.search(l) and i not in cand]
    score = None
    bandless = False
    for i in cand:
        m = SCORE_RE.search(lines[i])
        if not m:
            continue
        n = int(m.group(1))
        if n > 25:
            continue
        bm = BAND_RE.search(lines[i], m.end()) or BAND_RE.search(lines[i])
        if bm is None and i + 1 < len(lines):
            bm = BAND_RE.search(lines[i + 1])
        score = f"{n}/25 {bm.group(1)}" if bm else f"{n}/25"
        bandless = bm is None
        break

    # First gist-able line: first non-empty line that is not the H1 title.
    gist = ""
    for l in lines:
        s = l.strip()
        if not s or s.startswith("# "):
            continue
        gist = s
        break

    slug_m = INNER_SLUG_RE.search(text)
    return score, bandless, gist[:160], (slug_m.group(1) if slug_m else None)


def card_keys(stem, inner_slug):
    keys = {stem.lower()}
    base = DATE_SUFFIX_RE.sub("", stem)
    if base and base != stem:
        keys.add(base.lower())
        unprefixed = base[7:] if base.upper().startswith("INTAKE_") else base
        if len(unprefixed) >= 12:
            keys.add(unprefixed.lower())
    if inner_slug and len(inner_slug) >= 12:
        keys.add(inner_slug.lower())
    return keys


def main():
    if not ROOM.exists():
        raise SystemExit(f"missing {ROOM}")

    # 1. Scan the cards.
    cards = []
    for day in DAYS:
        cards.extend(sorted(WATCH.glob(f"INTAKE_*{day}*.md")))
    scanned = []
    for path in cards:
        score, bandless, gist, inner = parse_card(path)
        scanned.append({"path": path, "stem": path.stem, "score": score,
                        "bandless": bandless, "gist": gist, "inner": inner})

    # 2. Slugs already mentioned in room rows (item + file fields only).
    mentioned = []
    rows_before = 0
    with ROOM.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows_before += 1
            try:
                row = json.loads(line)
            except ValueError:
                continue
            for k in ("item", "file"):
                v = row.get(k)
                if isinstance(v, str) and v:
                    mentioned.append(v.lower())
    blob = "\n".join(mentioned)

    already, new = [], []
    for c in scanned:
        keys = card_keys(c["stem"], c["inner"])
        if any(k in blob for k in keys):
            already.append(c)
        else:
            new.append(c)

    # 3. Receipt rows for unmentioned cards (cap 120), batch-appended in one write.
    rows = []
    for c in new[:CAP]:
        if c["score"] is None:
            rows.append({"ts": "2026-09-04", "thread": "intake", "seat": "calcifer",
                         "type": "receipt", "item": c["stem"], "score": "unscored",
                         "file": f"watch/{c['path'].name}",
                         "gist": "backlog consumption — no score line found"})
        else:
            rows.append({"ts": "2026-09-04", "thread": "intake", "seat": "calcifer",
                         "type": "receipt", "item": c["stem"], "score": c["score"],
                         "file": f"watch/{c['path'].name}",
                         "gist": "backlog consumption — card receipted late by Calcifer feed"})

    unscored = sum(1 for r in rows if r["score"] == "unscored")
    bandless_ct = sum(1 for c in new[:CAP] if c["bandless"] and c["score"] is not None)

    # 5. Stats (+ 6. the feed's own room receipt rides the same single append).
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    feed_row = {"ts": "2026-09-04", "thread": "audit", "seat": "calcifer",
                "type": "receipt", "item": "CALCIFER_BACKLOG_FEED",
                "gist": (f"scanned={len(scanned)} already={len(already)} "
                         f"new={len(rows)} unscored={unscored} bandless={bandless_ct} "
                         f"cap={CAP} days={'+'.join(DAYS)}")}
    with ROOM.open("a", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
        f.write(json.dumps(feed_row, ensure_ascii=False, separators=(",", ":")) + "\n")

    record = {"ts": now, "scanned": len(scanned), "already_receipted": len(already),
              "newly_receipted": len(rows), "unscored": unscored,
              "bandless_score_no_band": bandless_ct, "cap": CAP,
              "days": list(DAYS), "room_rows_before": rows_before,
              "room_rows_after": rows_before + len(rows) + 1,
              "room": "watch/room.jsonl",
              "cards": [{"item": c["stem"], "score": c["score"] or "unscored",
                         "file": f"watch/{c['path'].name}", "gist_line": c["gist"]}
                        for c in new[:CAP]]}
    STATS.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if STATS.exists():
        try:
            cur = json.loads(STATS.read_text(encoding="utf-8"))
            existing = cur if isinstance(cur, list) else [cur]
        except ValueError:
            existing = []
    existing.append(record)
    STATS.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")

    # 5. Print stats (ASCII-safe for the console).
    print(f"scanned={len(scanned)}")
    print(f"already_receipted={len(already)}")
    print(f"newly_receipted={len(rows)} (unscored={unscored}, bandless={bandless_ct})")
    print(f"room={ROOM}")
    print(f"stats={STATS}")


if __name__ == "__main__":
    main()
