"""zknot_alarm.py - zknot support + alarm layer (lane d05-meter-alarm,
dogfood-100m-20261006).

Extracted from tools/zknot.py so the runner stays under the ratchet's
file-length bar (violation_ratchet file-too-long fired NEW at 535 lines on
the first in-file landing; the file was already 401 at HEAD, over the 400
cap unregistered). Everything here is re-exported by tools/zknot.py, so
callers and tests ride zknot.<name> unchanged.

Holds three concerns, all pure or append-only:
  meter math       meter_nums / meter_line / meter: last 7d vs prior 7d,
                   (self-steal + forgot) prompts per 1000 non-template human
                   prompts, plus the template filters they need.
  meter alarm      meter_alarm_verdict / meter_alert_block / append_attention
                   / meter_alarm_step: the week-over-week worsening check
                   that appends one deduped alert row to memory/attention.md
                   (estate block + key convention, tools/gate_age_patrol.py
                   shape). Two legs, fire when EITHER holds; quiet only when
                   both are clear:
                     WORSENED - last 7d rate > prior 7d rate (the 2026-10-06
                                LATEST line read 126 vs prior 108 with no
                                alarm at all; this leg is that check).
                     BASELINE - last 7d rate >= the dive baseline ~148 (the
                                126->148-shaped drift).
                   Improvement (last <= prior AND last < baseline) stays
                   quiet. WARN-only: never blocks a zknot run, never changes
                   its exit codes, never edits LATEST.md; a failed append is
                   stamped on the receipt, never swallowed.
  S1 gate          s1_gate: fail-closed check that a [:3] LATEST rewrite
                   named every qualifying session it dropped (R4-L1).

Numbers ride in as the meter_nums dict {last, prior, baseline, target, ...},
so the alarm never re-parses the meter line string.
"""
from __future__ import annotations

import datetime as dt
import re
from collections import Counter
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
ATTENTION = ROOT / "memory" / "attention.md"
ET = ZoneInfo("America/New_York")
OMIT_MARK = "qualifying sessions not carded above"
METER_BASELINE = 148  # dive baseline (watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md)
METER_TARGET = 75
SELF_STEAL_RE = re.compile(r"self[\s_-]*ste[a]?l", re.I)
FORGOT_RE = re.compile(r"\bforg[oe]t|already have|\bremember\b", re.I)


def template_prefixes(prompts: dict[str, list[dict]]) -> set[str]:
    c = Counter(" ".join(p["text"].split())[:40] for ps in prompts.values() for p in ps
                if len(p["text"]) > 150)
    return {k for k, n in c.items() if n >= 8}


def is_template(p: dict, tmpl: set[str]) -> bool:
    return len(p["text"]) > 150 and " ".join(p["text"].split())[:40] in tmpl


def meter_nums(prompts: dict[str, list[dict]], tmpl: set[str], now_ms: int) -> dict:
    """Meter math, numbers first (lane d05-meter-alarm, 2026-10-06).

    Same windows and rate the meter line always carried: last 7d vs prior 7d,
    (self-steal + forgot) prompts per 1000 non-template human prompts, rounded.
    The numbers dict feeds both the LATEST.md line and the meter alarm, so the
    alarm reads the same computation that wrote the line (no string parsing).
    """
    wk = 7 * 86400 * 1000
    def window(lo: int, hi: int) -> tuple[int, int, int]:
        hs = [p["text"] for ps in prompts.values() for p in ps
              if lo <= p["t"] < hi and not is_template(p, tmpl)]
        ss = sum(1 for t in hs if SELF_STEAL_RE.search(t))
        fg = sum(1 for t in hs if FORGOT_RE.search(t))
        return len(hs), ss, fg
    n1, s1, f1 = window(now_ms - wk, now_ms + 1)
    n0, s0, f0 = window(now_ms - 2 * wk, now_ms - wk)
    r = lambda s, f, n: round(1000 * (s + f) / n) if n else 0  # noqa: E731
    return {"last": r(s1, f1, n1), "prior": r(s0, f0, n0),
            "s1": s1, "f1": f1, "n1": n1, "s0": s0, "f0": f0, "n0": n0,
            "baseline": METER_BASELINE, "target": METER_TARGET}


def meter_line(m: dict) -> str:
    return (f"METER self-steal+forgot per 1000 human prompts: last 7d {m['last']} "
            f"({m['s1']} self-steal + {m['f1']} forgot of {m['n1']}) vs prior 7d {m['prior']} "
            f"({m['s0']} + {m['f0']} of {m['n0']}); dive baseline ~{m['baseline']}, "
            f"target <{m['target']}")


def meter(prompts: dict[str, list[dict]], tmpl: set[str], now_ms: int) -> str:
    return meter_line(meter_nums(prompts, tmpl, now_ms))


def meter_alarm_verdict(m: dict) -> dict:
    """Pure alarm core over the meter numbers (lane d05-meter-alarm)."""
    legs = []
    if m["last"] > m["prior"]:
        legs.append(f"WORSENED week-over-week (last 7d {m['last']} vs prior 7d {m['prior']})")
    if m["last"] >= m["baseline"]:
        legs.append(f"AT-OR-ABOVE dive baseline (last 7d {m['last']} vs ~{m['baseline']})")
    return {"fire": bool(legs), "legs": legs}


def meter_alert_block(m: dict, verdict: dict, now: dt.datetime) -> tuple[str, str]:
    """Render the attention.md alert (estate convention, gate_age_patrol.py
    shape) plus its dedup key line (same numbers + same ET day appends once)."""
    stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    day = now.strftime("%Y-%m-%d")
    legs = "; ".join(verdict["legs"])
    key = f"- key: meter-alarm last7d-{m['last']} prior7d-{m['prior']} {day}"
    lines = [
        "",
        "---",
        "",
        f"### zknot self-steal meter alarm fired ({stamp} ET)",
        "",
        f"- verdict: METER-ALARM: {legs}; target <{m['target']} "
        "(meter line: memory/zknot/LATEST.md, math tools/zknot.py meter_nums)",
        "- response: the meter counts self-steal+forgot prompts per 1000 human prompts;",
        "  a WORSENED leg means recent prompts re-asked law the estate already holds - read",
        "  the newest cards under memory/zknot/ for which asks re-taught known law, then",
        "  tighten the ribs/boot rows they name; a BASELINE leg means the dive-era rate is",
        "  back. WARN-only: nothing is blocked by this row.",
        key,
        "",
    ]
    return "\n".join(lines), key


def append_attention(attention_path: Path, block: str, key_line: str) -> bool:
    """Append the alert once per key (dedup on the key line, gate_age_patrol
    convention). Returns True if written, False when already present."""
    existing = ""
    if attention_path.is_file():
        existing = attention_path.read_text(encoding="utf-8", errors="replace")
    if key_line in existing:
        return False
    with attention_path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(block)
    return True


def meter_alarm_step(mnums: dict, attention_path: Path | None = None,
                     write: bool = True, now: dt.datetime | None = None) -> dict:
    """Evaluate the meter alarm and land the alert row. Receipt-shaped return:
    {fire, legs, last7d, prior7d, appended[, dry_run|error]}. write=False is
    the dry-run contract: evaluate, append nothing."""
    attention_path = attention_path or ATTENTION
    verdict = meter_alarm_verdict(mnums)
    out = {"fire": verdict["fire"], "legs": verdict["legs"],
           "last7d": mnums["last"], "prior7d": mnums["prior"], "appended": False}
    if not verdict["fire"]:
        return out
    if not write:
        out["dry_run"] = True
        return out
    now = now or dt.datetime.now(ET)
    block, key = meter_alert_block(mnums, verdict, now)
    try:
        out["appended"] = append_attention(attention_path, block, key)
    except OSError as exc:
        out["error"] = str(exc)
    return out


def s1_gate(dropped: int, latest: str) -> bool:
    """True = FAIL CLOSED: the [:3] rewrite dropped qualifying sessions
    without naming them (S1 no-silent-truncation, R4-L1 2026-10-05).

    The 2026-10-05 run row measured the disease: 18 qualifying sessions, 3
    cards in LATEST, zero omission tokens. A recap that truncates silently
    is worse than no recap - a booting seat cannot even ask what it was not
    shown. main() returns 2 and keeps the previous LATEST when this fires.
    """
    return bool(dropped) and OMIT_MARK not in latest
