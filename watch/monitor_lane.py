#!/usr/bin/env python3
"""monitor_lane.py — the $0 keyless standing research poller (MONITOR organ).

Adopt-now build from watch/STEAL_RESEARCH_PIPELINES_20260904.md (pattern 2+7
fused): poll THREE keyless public APIs against the fleet's watch terms, diff
against a last-seen store, spool NEW items into the scout spool, and post ONE
typed room.jsonl row per run. Kills the deck as a single point of harvest
failure. No keys, no auth, no secrets.

  Sources (polite: 1 req/sec, User-Agent set):
    1. HN Algolia  https://hn.algolia.com/api/v1/search_by_date
    2. arXiv       http://export.arxiv.org/api/query  (Atom XML)
    3. OpenAlex    https://api.openalex.org/works

  State : watch/monitor_lane.state      (json: term -> seen-id list, cap 500/term;
                                         reserved keys "_cooldown" -> per-source
                                         box-until epochs, "_rotation" -> the
                                         rotation ledger below)
  Terms : watch/monitor_terms.json      (auto-seeded on first run)
  Pool  : watch/monitor_term_pool.json  (auto-seeded on first run; superset)
  Spool : watch/scout/MONITOR_LANE_<UTC-date>.md  (append, grouped by term)
  Room  : one row per run, kind "monitor.lane"

TERM ROTATION (2026-10-04, dedup-saturation blindness cure; receipt
watch/inbox/night_shift_20261004/research_rotation_cured.md): a term that
returns 0 new items for ROTATE_AFTER_BLANK consecutive runs rotates OUT of the
active window and the pool term least-recently-used (never-used first) rotates
IN; the active window stays ACTIVE_TERMS wide; a term's seen-id list survives
rotation so it dedups cleanly when it returns. The used-ledger and the
rotation epoch (one per swap event) live in state["_rotation"] and the epoch
is mirrored to the research lane runner_state as rotation_epoch by
mag/lane_runner.cycle_research. Terms hand-added via --add that are not pool
members are never rotated out (the operator's word outranks the law).

Usage:
  python monitor_lane.py --once          # one poll cycle (default)
  python monitor_lane.py --terms         # list watch terms
  python monitor_lane.py --add "term"    # add a watch term
  python monitor_lane.py --remove "term" # remove a watch term

Fail-open per source: one API down = log to stderr + continue, exit stays 0.
Stdlib only.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WATCH = ROOT / "watch"
TERMS_FILE = WATCH / "monitor_terms.json"
POOL_FILE = WATCH / "monitor_term_pool.json"
STATE_FILE = WATCH / "monitor_lane.state"
SPOOL_DIR = WATCH / "scout"
ROOM = WATCH / "room.jsonl"

SEAT = "zcode"
UA = "monitor_lane/1.0 (local_sovereign_agent fleet watch; keyless research poller; polite 1rps)"
CAP = 500          # seen-ids kept per term
TIMEOUT_S = 20
POLL_SLEEP_S = 1.0   # politeness: 1 req/sec default
# arXiv asks for >=3s between requests (measured 2026-09-04: 1s pacing earns
# HTTP 429 + read timeouts from export.arxiv.org — fail-open held, lane starved)
SOURCE_SLEEP_S = {"hn": POLL_SLEEP_S, "arxiv": 3.0, "openalex": POLL_SLEEP_S}
# OpenAlex polite pool (measured 2026-09-05: keyless requests 429 every pass for hours —
# the shared IP sat in the impolite pool; mailto= is OpenAlex's documented polite door).
OPENALEX_MAILTO = "local-sovereign-agent@localhost"
# per-source cooldown: a source that keeps failing gets a longer box than the default
SOURCE_COOLDOWN_S = {"openalex": 3600}
# Circuit breaker (measured 2026-09-04: arXiv runs a per-IP penalty box; retrying
# INTO the box extends it). A source that fails even after in-run retry is skipped
# for this long. Nightly cadence never notices; sub-hourly cadence stops feeding the box.
COOLDOWN_KEY = "_cooldown"
COOLDOWN_S = 900
ABSTRACT_MAX = 240

# ------------------------------------------------------------- term rotation
# The rotation law (see module docstring): 0 new items for
# ROTATE_AFTER_BLANK consecutive runs = rotate out; least-recently-used pool
# term rotates in; epoch counts swap events. The active window stays
# ACTIVE_TERMS wide; seen-id state survives rotation (dedup continuity).
ROTATION_KEY = "_rotation"
ACTIVE_TERMS = 7
ROTATE_AFTER_BLANK = 3

DEFAULT_TERMS = [
    "agent swarm concurrency",
    "speculative decoding MLX",
    "image to 3D WebGPU",
    "GLM-5.3",
    "KV cache economics",
    "fixed point refinement reasoning",
    "AI game building agents",
]

# The candidate superset: the 7 standing terms first (they return by rotation),
# then estate-interest phrases derived from mag/arxiv_harvest.py INTEREST_MAP
# (orchestration/stigmergy, verification harnesses, caching economics, game
# benchmarks, provenance/receipts, trace distillation, concurrency serving).
DEFAULT_POOL = DEFAULT_TERMS + [
    "multi-agent orchestration",
    "LLM agent evaluation harness",
    "stigmergy swarm coordination",
    "prompt caching inference cost",
    "LLM inference serving concurrency",
    "agent trace distillation",
    "reasoning distillation small models",
    "open world agent benchmark",
    "game environments agent evaluation",
    "provenance audit trail agents",
    "verifiable agent actions",
    "local LLM inference",
    "agent tool use planning",
    "KV cache compression",
]

ATOM = "{http://www.w3.org/2005/Atom}"


# ---------------------------------------------------------------- helpers

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def clean(text: str, cap: int = ABSTRACT_MAX) -> str:
    """Collapse whitespace, unescape HTML entities (HN story_text is escaped),
    truncate to one line."""
    s = re.sub(
        r"\s+", " ", html.unescape(text or "").replace("<", " ").replace(">", " ")
    ).strip()
    if len(s) > cap:
        s = s[: cap - 1].rstrip() + "…"
    return s


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        return resp.read()


def fetch_with_retry(url: str, retries: int = 1, backoff_s: float = 10.0) -> bytes:
    """One bounded retry on 429/transport errors (measured: arXiv boxes hot IPs
    with 429 'Rate exceeded.'; a transient 429 should not starve a whole run)."""
    try:
        return fetch(url)
    except urllib.error.HTTPError as exc:
        if exc.code in (429, 503) and retries > 0:  # measured: both transient on arXiv
            time.sleep(backoff_s)
            return fetch(url)
        raise
    except (urllib.error.URLError, TimeoutError, OSError):
        if retries > 0:
            time.sleep(backoff_s)
            return fetch(url)
        raise


def fetch_json(url: str):
    return json.loads(fetch(url).decode("utf-8", "replace"))


# ---------------------------------------------------------------- sources

def poll_hn(term: str) -> list[dict]:
    """HN Algolia search_by_date, stories only."""
    url = "https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode(
        {"query": term, "tags": "story", "hitsPerPage": 10}
    )
    data = fetch_json(url)
    out = []
    for h in data.get("hits", []):
        hid = str(h.get("objectID") or "").strip()
        if not hid:
            continue
        title = h.get("title") or h.get("story_title") or "(untitled)"
        link = h.get("url") or f"https://news.ycombinator.com/item?id={hid}"
        abstract = h.get("story_text") or ""
        if not abstract:
            abstract = (
                f"HN story: points={h.get('points') or 0} "
                f"comments={h.get('num_comments') or 0} by={h.get('author') or '?'}"
            )
        out.append(
            {"id": f"hn:{hid}", "source": "hn", "title": clean(title, 160),
             "url": link, "abstract": clean(abstract)}
        )
    return out


def poll_arxiv(term: str) -> list[dict]:
    """arXiv Atom API, newest submissions matching the term as a phrase.
    https directly (measured 2026-09-04: http endpoint is a 301 to this)."""
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {
            "search_query": f'all:"{term}"',
            "sortBy": "submittedDate",
            "max_results": 8,
        }
    )
    root = ET.fromstring(fetch_with_retry(url).decode("utf-8", "replace"))
    out = []
    for entry in root.findall(ATOM + "entry"):
        aid = (entry.findtext(ATOM + "id") or "").strip()
        if not aid:
            continue
        title = clean(entry.findtext(ATOM + "title") or "(untitled)", 160)
        summary = clean(entry.findtext(ATOM + "summary") or "")
        out.append(
            {"id": f"arxiv:{aid}", "source": "arxiv", "title": title,
             "url": aid, "abstract": summary}
        )
    return out


def poll_openalex(term: str) -> list[dict]:
    """OpenAlex works, newest first. Abstract arrives as an inverted index."""
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": term, "sort": "publication_date:desc", "per-page": 8,
         "mailto": OPENALEX_MAILTO}
    )
    data = fetch_json(url)
    out = []
    for w in data.get("results", []):
        wid = str(w.get("id") or "").strip()
        if not wid:
            continue
        title = w.get("display_name") or "(untitled)"
        link = w.get("doi") or wid
        inv = w.get("abstract_inverted_index")
        abstract = ""
        if inv:
            pos: dict[int, str] = {}
            for word, idxs in inv.items():
                for i in idxs:
                    pos[i] = word
            abstract = " ".join(pos[i] for i in sorted(pos))
        if not abstract:
            abstract = f"OpenAlex work, {w.get('publication_date') or w.get('publication_year') or 'date unknown'}"
        out.append(
            {"id": f"openalex:{wid}", "source": "openalex", "title": clean(title, 160),
             "url": link, "abstract": clean(abstract)}
        )
    return out


SOURCES = [("hn", poll_hn), ("arxiv", poll_arxiv), ("openalex", poll_openalex)]


# ---------------------------------------------------------------- state / terms / spool / room

def load_terms() -> list[str]:
    if TERMS_FILE.exists():
        try:
            terms = json.loads(TERMS_FILE.read_text(encoding="utf-8"))
            if isinstance(terms, list) and terms:
                return [str(t).strip() for t in terms if str(t).strip()]
        except (json.JSONDecodeError, OSError):
            pass
    save_terms(DEFAULT_TERMS)
    return list(DEFAULT_TERMS)


def save_terms(terms: list[str]) -> None:
    TERMS_FILE.write_text(
        json.dumps(terms, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def load_pool() -> list[str]:
    """The rotation candidate superset (auto-seeded like the terms file)."""
    if POOL_FILE.exists():
        try:
            pool = json.loads(POOL_FILE.read_text(encoding="utf-8"))
            if isinstance(pool, list) and pool:
                return [str(t).strip() for t in pool if str(t).strip()]
        except (json.JSONDecodeError, OSError):
            pass
    save_pool(DEFAULT_POOL)
    return list(DEFAULT_POOL)


def save_pool(pool: list[str]) -> None:
    POOL_FILE.write_text(
        json.dumps(pool, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def load_state() -> tuple[dict, dict, dict]:
    """-> (term -> seen-id list, source -> cooldown-until epoch, rotation
    ledger {epoch, ledger: term -> last-rotation-out stamp, blank: term ->
    consecutive blank runs}). Corrupt state = start fresh (fail-open)."""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cooldown = data.pop(COOLDOWN_KEY, {})
                rotation = data.pop(ROTATION_KEY, {})
                if not isinstance(cooldown, dict):
                    cooldown = {}
                if not isinstance(rotation, dict):
                    rotation = {}
                return (
                    {k: list(v) for k, v in data.items() if isinstance(v, list)},
                    {k: float(v) for k, v in cooldown.items()},
                    {
                        "epoch": int(rotation.get("epoch") or 0),
                        "ledger": {str(k): int(v) for k, v
                                   in (rotation.get("ledger") or {}).items()},
                        "blank": {str(k): int(v) for k, v
                                  in (rotation.get("blank") or {}).items()},
                    },
                )
        except (json.JSONDecodeError, OSError, ValueError, AttributeError, TypeError):
            print("[monitor_lane] state unreadable, starting fresh", file=sys.stderr)
    return {}, {}, {"epoch": 0, "ledger": {}, "blank": {}}


def save_state(state: dict, cooldown: dict, rotation: dict) -> None:
    tmp = STATE_FILE.with_suffix(".state.tmp")
    payload = {COOLDOWN_KEY: cooldown, ROTATION_KEY: rotation}
    payload.update({k: v[-CAP:] for k, v in state.items()})
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, STATE_FILE)


def rotate_terms(terms: list[str], pool: list[str], blank: dict, ledger: dict,
                 epoch: int, yields: dict) -> tuple[list[str], list, dict, dict, int]:
    """Pure rotation step (no IO; the test surface). Blank streaks advance from
    this run's per-term yields, pool members past ROTATE_AFTER_BLANK rotate
    out (ledger-stamped), the least-recently-used pool terms (never-used first,
    then oldest stamp, then pool order for determinism) rotate in until the
    window is ACTIVE_TERMS wide. Hand-added terms outside the pool never
    rotate out. Returns (new_terms, [(out, in), ...], blank', ledger', epoch').
    """
    blank = {t: (0 if (yields.get(t) or 0) > 0 else int(blank.get(t, 0)) + 1)
             for t in terms}
    new_terms = list(terms)
    rotations: list[tuple[str, str]] = []
    pool_set = set(pool)
    for term in list(new_terms):
        if int(blank.get(term, 0)) < ROTATE_AFTER_BLANK:
            continue
        if term not in pool_set:
            continue  # hand-added (--add): the operator's word outranks the law
        active = set(new_terms)
        candidates = [p for p in pool if p not in active]
        if not candidates:
            break  # pool exhausted: keep the term rather than shrink the window
        candidates.sort(key=lambda p: (int(ledger.get(p, 0)), pool.index(p)))
        replacement = candidates[0]
        idx = new_terms.index(term)
        new_terms[idx] = replacement
        epoch += 1
        ledger = {**ledger, term: epoch}
        blank.pop(term, None)
        blank[replacement] = 0
        rotations.append((term, replacement))
    return new_terms, rotations, blank, ledger, epoch


def write_spool(new_items: list[tuple[str, dict]], run_ts: str) -> Path:
    """Append this run's new items, grouped by term."""
    SPOOL_DIR.mkdir(parents=True, exist_ok=True)
    date = run_ts[:10]
    spool = SPOOL_DIR / f"MONITOR_LANE_{date}.md"
    by_term: dict[str, list[dict]] = {}
    for term, item in new_items:
        by_term.setdefault(term, []).append(item)
    lines = [f"## monitor_lane run {run_ts} — {len(new_items)} new items across {len(by_term)} terms", ""]
    for term, items in by_term.items():
        lines.append(f"### term: \"{term}\" ({len(items)} new)")
        for it in items:
            lines.append(f"- [{it['source']}] {it['title']}")
            lines.append(f"  {it['url']}")
            if it["abstract"]:
                lines.append(f"  {it['abstract']}")
        lines.append("")
    with spool.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return spool


def post_room_row(detail: str) -> None:
    row = {
        "ts": now_iso(),
        "kind": "monitor.lane",
        "seat": SEAT,
        "verb": "monitor-poll",
        "detail": detail,
    }
    with ROOM.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- run

def run_once() -> int:
    run_ts = now_iso()
    terms = load_terms()
    pool = load_pool()
    state, cooldown, rotation = load_state()
    new_items: list[tuple[str, dict]] = []
    per_source = {"hn": 0, "arxiv": 0, "openalex": 0}
    yields: dict[str, int] = {}
    source_fails: list[str] = []
    source_skipped: list[str] = []

    for t_i, term in enumerate(terms):
        seen = set(state.get(term, []))
        fresh_ids: list[str] = []
        for s_i, (source, fn) in enumerate(SOURCES):
            if t_i or s_i:
                time.sleep(SOURCE_SLEEP_S.get(source, POLL_SLEEP_S))
            if time.time() < cooldown.get(source, 0):
                # boxed from an earlier run: skip, do not extend the penalty
                if source not in source_skipped:
                    source_skipped.append(source)
                continue
            try:
                items = fn(term)
            except Exception as exc:  # fail-open per source + trip the breaker
                cooldown[source] = time.time() + SOURCE_COOLDOWN_S.get(source, COOLDOWN_S)
                if source not in source_fails:
                    source_fails.append(source)
                print(f"[monitor_lane] source down: {source} for '{term}': {exc}", file=sys.stderr)
                continue
            for it in items:
                if it["id"] not in seen:
                    seen.add(it["id"])
                    fresh_ids.append(it["id"])
                    new_items.append((term, it))
                    per_source[it["source"]] += 1
        if fresh_ids:
            state[term] = (state.get(term, []) + fresh_ids)[-CAP:]
        yields[term] = len(fresh_ids)

    # TERM ROTATION: advance blank streaks, swap saturated pool terms for
    # least-recently-used pool terms, persist the new window + ledger.
    terms, rotations, blank, ledger, epoch = rotate_terms(
        terms, pool, rotation.get("blank") or {}, rotation.get("ledger") or {},
        int(rotation.get("epoch") or 0), yields)
    rotation = {"epoch": epoch, "ledger": ledger, "blank": blank}
    if rotations:
        save_terms(terms)

    save_state(state, cooldown, rotation)
    spool_path = write_spool(new_items, run_ts) if new_items else SPOOL_DIR / f"MONITOR_LANE_{run_ts[:10]}.md"
    terms_hit = len({t for t, _ in new_items})
    extras = ""
    if source_fails:
        extras += f", sources_down={','.join(source_fails)}"
    if source_skipped:
        extras += f", sources_boxed_skip={','.join(source_skipped)}"
    rot = (f" rotated={'/'.join(f'{o}>{i}' for o, i in rotations)}"
           if rotations else "")
    detail = (
        f"{len(new_items)} new items across {terms_hit}/{len(terms)} terms "
        f"(hn={per_source['hn']}, arxiv={per_source['arxiv']}, openalex={per_source['openalex']}{extras}); "
        f"spool {spool_path.relative_to(ROOT).as_posix()}"
    )
    post_room_row(f"epoch={epoch}{rot} | {detail}")
    print(detail)
    # last line out (stderr rides after stdout in the runner's captured buffer,
    # so the lane trail's tail keeps this): the rotation fact of the run.
    if rotations:
        print(f"[monitor_lane] rotation epoch={epoch}: "
              + "; ".join(f"OUT '{o}' (blank>={ROTATE_AFTER_BLANK}) IN '{i}'"
                          for o, i in rotations), file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="$0 keyless research poller (MONITOR organ)",
        epilog="Terms live in watch/monitor_terms.json; the rotation pool in "
               "watch/monitor_term_pool.json; state in watch/monitor_lane.state.",
    )
    ap.add_argument("--once", action="store_true", help="one poll cycle (default)")
    ap.add_argument("--terms", action="store_true", help="list watch terms and exit")
    ap.add_argument("--add", metavar="TERM", help="add a watch term and exit")
    ap.add_argument("--remove", metavar="TERM", help="remove a watch term and exit")
    args = ap.parse_args(argv)

    if args.terms:
        for t in load_terms():
            print(t)
        return 0
    if args.add is not None:
        terms = load_terms()
        if args.add.strip() and args.add.strip() not in terms:
            terms.append(args.add.strip())
            save_terms(terms)
        print("\n".join(terms))
        return 0
    if args.remove is not None:
        terms = [t for t in load_terms() if t.lower() != args.remove.strip().lower()]
        save_terms(terms)
        print("\n".join(terms))
        return 0

    return run_once()


if __name__ == "__main__":
    sys.exit(main())
