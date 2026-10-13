"""verkle_boot_view - read-only boot view of REAL operator sessions in the verkle chain.

The chain (memory/biography/verkle_chain.jsonl) is dominated by machine output:
janitor knots, mag-agent-orc re-knots of old filenames, law/memlang knots,
work:seat rows, and a daily scheduled survey prompt. This script filters that
noise with explicit, tunable rules and prints the last N real sessions,
newest first, with the residual title/tldr when one exists.

Self-steal: reads the chain through mag.chain_query.chain (the canonical read
surface; chain law says no module reads the chain file directly) and resolves
residuals with mag.registry.residual_path. Nothing is written.

Usage:
  python scripts/verkle_boot_view.py [--n 20] [--window 2500] [--json] [--show-noise-stats]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# NOISE_RULES - operator-tunable. Evaluated in order; the first rule that
# matches classifies the leaf (counted as "first_match"). Every matching rule
# is also counted under "any_match" so overlaps stay visible.
# ---------------------------------------------------------------------------
JANITOR_THEMES = {"autonomous_janitor"}
JANITOR_SESSION_PREFIXES = ("autonomous-",)
ORC_SESSION_PREFIXES = ("mag-agent-orc-",)
MACHINE_SESSION_PREFIXES = (
    "memlang-", "law-", "work:", "q-knot-", "rib_bus_", "castle-foundation-", "water_computer",
    "doctor-rightsize:", "feedback:", "grok-hub:", "mem-weave-dist:", "steal_pack-",
    "dwf-",  # 2026-10-03: ZCode workflow-subagent actors (task_type=workflow_child), not operator sessions
)
# 2026-10-03: knot_at_close backfill knots carry dominant_theme "backfill-<title slug>".
# They are FIRST knots of old sessions (filename date = session date, ts = knot time),
# so the age gap is expected and must not read as an orc re-knot.
BACKFILL_THEME_PREFIX = "backfill-"
REKNOT_MAX_AGE_DAYS = 2.0       # filename date older than ts by more than this = re-knot
REPEAT_PROMPT_MAX = 3           # same residual title/tldr seen more than this = repeated prompt
PROMPT_FINGERPRINT_CHARS = 80   # chars of normalized tldr/title used as the fingerprint
STALE_REAL_DAYS = 3.0           # newest real session older than this = knotting has stalled

NOISE_RULES: list[dict[str, Any]] = [
    {"name": "janitor_theme",
     "desc": f"dominant_theme in {sorted(JANITOR_THEMES)} or session_id starts with {JANITOR_SESSION_PREFIXES}"},
    {"name": "orc_session_prefix",
     "desc": f"session_id starts with {ORC_SESSION_PREFIXES}"},
    {"name": "machine_session_prefix",
     "desc": f"session_id starts with one of {MACHINE_SESSION_PREFIXES}"},
    {"name": "reknot_old_filename",
     "desc": f"filename date older than leaf ts by > {REKNOT_MAX_AGE_DAYS} days "
             f"(exempt: knot_at_close backfill leaves, theme '{BACKFILL_THEME_PREFIX}*')"},
    {"name": "duplicate_session_id",
     "desc": "session_id already seen in a newer leaf of the window"},
    {"name": "repeated_prompt",
     "desc": f"residual title or tldr fingerprint (digits stripped, first {PROMPT_FINGERPRINT_CHARS} chars) "
             f"appears more than {REPEAT_PROMPT_MAX} times in the window"},
]

try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
except Exception:  # noqa: BLE001 - tzdata missing: fall back to fixed EDT
    from datetime import timedelta
    ET = timezone(timedelta(hours=-4), "ET")


def _read_chain(window: int) -> list[dict[str, Any]]:
    try:
        from mag.chain_query import chain
        return chain.tail(window)
    except Exception:  # noqa: BLE001 - read-only fallback, same file, logged to stderr
        print("[boot_view] chain_query import failed; falling back to direct read", file=sys.stderr)
        p = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
        rows = []
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines()[-window:]:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return rows


def _residual_path(session_id: str) -> Path:
    try:
        from mag.registry import residual_path
        return residual_path(session_id)
    except Exception:  # noqa: BLE001
        return ROOT / "memory" / "biography" / "residual" / f"{session_id}.json"


_residual_cache: dict[str, dict[str, str] | None] = {}


def residual_summary(session_id: str) -> dict[str, str] | None:
    if session_id in _residual_cache:
        return _residual_cache[session_id]
    out = None
    p = _residual_path(session_id) if session_id else None
    if p and p.is_file():
        try:
            r = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            title = ((r.get("time") or {}).get("title") or (r.get("session_card") or {}).get("title") or "")
            tldr = r.get("tldr") or ""
            out = {"title": _nodash(str(title).strip()), "tldr": _nodash(str(tldr).strip())}
        except (OSError, json.JSONDecodeError):
            out = None
    _residual_cache[session_id] = out
    return out


def _nodash(text: str) -> str:
    """Repo law: no em-dashes in output. En/em dashes from source text become ' - '."""
    return text.replace("\u2014", " - ").replace("\u2013", "-")


def _fingerprint(text: str) -> str:
    t = re.sub(r"\d+", "", (text or "").lower())
    t = re.sub(r"\s+", " ", t).strip()
    return t[:PROMPT_FINGERPRINT_CHARS]


def _parse_ts(ts: str) -> datetime | None:
    try:
        d = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _filename_date(fn: str) -> datetime | None:
    m = re.match(r"(\d{4}-\d{2}-\d{2})_(\d{4})", fn or "")
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1) + m.group(2), "%Y-%m-%d%H%M").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _theme(k: dict[str, Any]) -> str:
    return str(k.get("dominant_theme") or (k.get("theme_vector") or {}).get("dominant") or "")


def classify(rows_newest_first: list[dict[str, Any]]) -> list[tuple[dict[str, Any], list[str]]]:
    # pre-pass for repeated prompts across the whole window;
    # count each session once per fingerprint (duplicates must not inflate repeats)
    fp_counts: Counter[str] = Counter()
    seen_for_fp: set[str] = set()
    for k in rows_newest_first:
        sid = str(k.get("session_id") or "")
        if sid in seen_for_fp:
            continue
        seen_for_fp.add(sid)
        res = residual_summary(sid)
        if res:
            for f in {_fingerprint(res["title"]), _fingerprint(res["tldr"])}:
                if f:
                    fp_counts[f] += 1

    checks: dict[str, Callable[[dict[str, Any], set[str]], bool]] = {
        "janitor_theme": lambda k, s: _theme(k) in JANITOR_THEMES
        or str(k.get("session_id") or "").startswith(JANITOR_SESSION_PREFIXES),
        "orc_session_prefix": lambda k, s: str(k.get("session_id") or "").startswith(ORC_SESSION_PREFIXES),
        "machine_session_prefix": lambda k, s: str(k.get("session_id") or "").startswith(MACHINE_SESSION_PREFIXES),
        "reknot_old_filename": lambda k, s: _is_reknot(k),
        "duplicate_session_id": lambda k, s: str(k.get("session_id") or "") in s,
        "repeated_prompt": lambda k, s: _is_repeat(k, fp_counts),
    }
    out = []
    seen: set[str] = set()
    for k in rows_newest_first:
        hits = [r["name"] for r in NOISE_RULES if checks[r["name"]](k, seen)]
        seen.add(str(k.get("session_id") or ""))
        out.append((k, hits))
    return out


def _is_reknot(k: dict[str, Any]) -> bool:
    if _theme(k).startswith(BACKFILL_THEME_PREFIX):
        return False  # 2026-10-03: first knot of an old session (knot_at_close), not a re-knot
    ts, fd = _parse_ts(k.get("ts", "")), _filename_date(k.get("filename", ""))
    return bool(ts and fd and (ts - fd).total_seconds() > REKNOT_MAX_AGE_DAYS * 86400)


def _is_repeat(k: dict[str, Any], fp_counts: Counter[str]) -> bool:
    res = residual_summary(str(k.get("session_id") or ""))
    if not res:
        return False
    return any(fp_counts.get(f, 0) > REPEAT_PROMPT_MAX
               for f in {_fingerprint(res["title"]), _fingerprint(res["tldr"])} if f)


def _session_date(k: dict[str, Any]) -> datetime | None:
    """2026-10-03: the session's OWN date (start_minute, else filename date, else ts),
    so backfilled sessions sort where they happened, not where they were knotted."""
    return _parse_ts(k.get("start_minute") or "") or _filename_date(k.get("filename", "")) or _parse_ts(k.get("ts", ""))


def _row(k: dict[str, Any]) -> dict[str, Any]:
    sd = _session_date(k)
    ts = _parse_ts(k.get("ts", ""))
    sid = str(k.get("session_id") or "")
    res = residual_summary(sid) or {}
    return {
        "session_et": sd.astimezone(ET).strftime("%Y-%m-%d %H:%M ET") if sd else None,
        "ts_et": ts.astimezone(ET).strftime("%Y-%m-%d %H:%M ET") if ts else str(k.get("ts")),
        "index": k.get("index"),
        "session_id": sid,
        "dominant_theme": _theme(k) or None,
        "filename": k.get("filename"),
        "title": res.get("title") or None,
        "tldr": (res.get("tldr") or "")[:200] or None,
        "has_residual": bool(res),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Read-only boot view of real operator sessions in the verkle chain.")
    ap.add_argument("--n", type=int, default=20, help="real sessions to show (default 20)")
    ap.add_argument("--window", type=int, default=2500, help="chain leaves to scan from the tail (default 2500)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--show-noise-stats", action="store_true", help="counts per noise rule over the window")
    a = ap.parse_args(argv)

    rows = list(reversed(_read_chain(a.window)))
    classified = classify(rows)
    real = [k for k, hits in classified if not hits]
    # 2026-10-03: newest-first by the session's own date, not chain ts
    _epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    real.sort(key=lambda k: _session_date(k) or _epoch, reverse=True)
    first, anym = Counter(), Counter()
    for _, hits in classified:
        if hits:
            first[hits[0]] += 1
            anym.update(hits)
    stats = {
        "window_leaves": len(rows),
        "oldest_ts_et": _row(rows[-1])["ts_et"] if rows else None,
        "newest_ts_et": _row(rows[0])["ts_et"] if rows else None,
        "real_sessions": len(real),
        "noise_leaves": len(rows) - len(real),
        "first_match": {r["name"]: first.get(r["name"], 0) for r in NOISE_RULES},
        "any_match": {r["name"]: anym.get(r["name"], 0) for r in NOISE_RULES},
        "rules": NOISE_RULES,
    }
    shown = [_row(k) for k in real[: a.n]]
    finding = None
    newest_real = _session_date(real[0]) if real else None
    age_days = ((datetime.now(timezone.utc) - newest_real).total_seconds() / 86400) if newest_real else None
    stats["newest_real_age_days"] = round(age_days, 1) if age_days is not None else None
    if len(real) < max(5, a.n // 2):
        finding = (f"Only {len(real)} real operator sessions in the last {len(rows)} leaves. "
                   "Real sessions are not being knotted; the chain tail is machine output.")
    elif age_days is not None and age_days > STALE_REAL_DAYS:
        finding = (f"{len(real)} real sessions survive the filter, but the newest is {age_days:.1f} days old "
                   f"({len(rows) - len(real)} of {len(rows)} leaves are noise). Real sessions have stopped being knotted.")
    if a.json:
        payload: dict[str, Any] = {"schema": "verkle_boot_view.v1", "sessions": shown, "finding": finding}
        if a.show_noise_stats:
            payload["noise_stats"] = stats
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(f"VERKLE BOOT VIEW - last {len(shown)} real sessions (of {len(real)} in {len(rows)} leaves), newest first")
    for i, r in enumerate(shown, 1):
        print(f"{i:>2}. {r['session_et']} (knotted {r['ts_et']})  #{r['index']}  {r['session_id']}  theme={r['dominant_theme']}")
        print(f"    file: {r['filename']}")
        if r["has_residual"]:
            print(f"    title: {(r['title'] or '')[:110]}")
            print(f"    tldr:  {(r['tldr'] or '')[:150]}")
        else:
            print("    (no residual)")
    if finding:
        print(f"\nFINDING: {finding}")
    if a.show_noise_stats:
        print(f"\nNOISE STATS over {stats['window_leaves']} leaves ({stats['oldest_ts_et']} .. {stats['newest_ts_et']})")
        print(f"  real={stats['real_sessions']}  noise={stats['noise_leaves']}")
        print(f"  {'rule':<24}{'first_match':>12}{'any_match':>11}")
        for r in NOISE_RULES:
            print(f"  {r['name']:<24}{stats['first_match'][r['name']]:>12}{stats['any_match'][r['name']]:>11}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
