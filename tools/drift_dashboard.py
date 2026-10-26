"""drift_dashboard -- render the teleo drift verdict history panel (B2-64).

Spec: docs/DRIFT_BOARD_SPEC.md (filed before this code). Reads
memory/runs/adv_arc_50/teleo_drift_stamps.jsonl (the T1-T6 weekly ledger of
tools/drift_pairs_stamp.py) and renders:

  dashboard/static/drift_board.html   the lab-UI panel (/static/, :8765)
  stdout                              the same table as markdown (receipts)

Per pair: verdict history over weeks, current corr, live referent age, and
the DRIFTING-days counter (spec section 1 for the exact definitions).

Honesty laws (spec section 3): undated v1 rows are displayed but never
counted in day math; referent ages are recomputed live from the referent
sources with the same filters as tools/drift_pairs_stamp.py; an unreadable
source renders n/a, never a guess; no em-dash in any output.

Usage:
  .venv\\Scripts\\python.exe tools\\drift_dashboard.py           # build + print table
  .venv\\Scripts\\python.exe tools\\drift_dashboard.py --check   # exit 0 if fresh
  .venv\\Scripts\\python.exe tools\\drift_dashboard.py --alarm   # exit 2 + inbox row on breach

--alarm (spec docs/DRIFT_BOARD_SPEC.md section 4b, B2-225): fires when a
DRIFTING streak crosses 14d or a live referent age crosses 30d; writes the
dated inbox row watch/inbox/DRIFT_ALARM_<date>.md and exits 2; quiet writes
nothing and exits 0. Proposal surface only, never mutates the ledger.
"""
from __future__ import annotations

import glob
import html
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ratchet receipt: the original `except Exception: pass` guard here was NEW debt
# (ratchet run 2026-09-26, sig 59b703f590d8c52a, filed by lane B2-216); replaced
# with an explicit capability check so exotic stdout (pytest capture) skips
# reconfigure silently by design, never by swallowed error.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER = ROOT / "memory" / "runs" / "adv_arc_50" / "teleo_drift_stamps.jsonl"
OUT_HTML = ROOT / "dashboard" / "static" / "drift_board.html"
SPEC = "docs/DRIFT_BOARD_SPEC.md"
LAW = ("a rate metric answers 'is it moving'; only corr(delta-M, delta-R) "
       "answers 'is it moving north'")

# spec section 2: pair_id -> (referent root-relative path(s), ts key, filter)
REFERENTS: dict[str, dict] = {
    "T1": {"paths": ["memory/corpus/LINKS.jsonl"], "key": "ts"},
    "T2": {"paths": ["watch/inbox/mrpool_export/ledger.jsonl"], "key": "date"},
    "T3": {"paths": ["queue/lanes/*/trail.jsonl"], "key": "ts"},
    "T4": {"paths": ["memory/improve/releases/gates.jsonl"], "key": "ts"},
    "T5": {"paths": ["memory/training/events.jsonl"], "key": "ts",
           "line_filter": '"pattern": "release_milestone"'},
    "T6": {"paths": ["memory/burns/LEDGER.jsonl"], "key": "ts"},
}

_TS_DATE_RE = re.compile(r'"(?:ts|date)": "(\d{4})-(\d{2})-(\d{2})')


def _utc_date(v) -> date | None:
    if not v or not isinstance(v, str):
        return None
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00")).astimezone(timezone.utc).date()
    except ValueError:
        return None


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


# --------------------------------------------------------------- ledger side

def load_stamps() -> list[dict]:
    """All ledger rows, tagged: v1 = undated legacy, v2 = teleo_drift_stamp.v2.

    v1 rows carry no pair_id field, only label "teleological drift pair Tn";
    the pair id is derived from that label so the v1(undated) history marker
    lands on the right pair (spec section 3.1)."""
    rows = _read_jsonl(LEDGER)
    out = []
    for r in rows:
        if r.get("schema") == "teleo_drift_stamp.v2":
            r = dict(r, _gen="v2")
        elif r.get("tool") == "drift_check":
            m = re.match(r"teleological drift pair (\S+)", r.get("label", ""))
            r = dict(r, _gen="v1", pair_id=m.group(1) if m else "?")
        else:
            continue
        out.append(r)
    return out


def pair_rows(stamps: list[dict], pid: str) -> list[dict]:
    return [s for s in stamps if s.get("pair_id") == pid]


def history_cell(rows: list[dict]) -> str:
    """Verdict history: v1 marker + one cell per v2 week, oldest first."""
    v1 = [r for r in rows if r["_gen"] == "v1"]
    v2 = sorted((r for r in rows if r["_gen"] == "v2"),
                key=lambda r: (r.get("stamped_at", ""), r.get("week_key", "")))
    parts = []
    if v1:
        parts.append("v1(undated)")
    last_week = v2[-1].get("week_key", "") if v2 else ""
    for r in v2:
        wk = r.get("week_key", "?")
        vd = r.get("verdict", {}).get("verdict", "?")
        mark = "*" if wk == last_week else ""
        parts.append(f"{wk}={vd}{mark}")
    return " ".join(parts) if parts else "no stamps"


def current(rows: list[dict]) -> dict | None:
    v2 = [r for r in rows if r["_gen"] == "v2"]
    if not v2:
        return None
    return max(v2, key=lambda r: (r.get("stamped_at", ""), r.get("week_key", "")))


def drifting_days(rows: list[dict], today: date) -> tuple[int, str]:
    """(days, streak_start) of the current unbroken trailing DRIFTING v2 run."""
    v2 = sorted((r for r in rows if r["_gen"] == "v2"),
                key=lambda r: (r.get("stamped_at", ""), r.get("week_key", "")))
    if not v2 or v2[-1].get("verdict", {}).get("verdict") != "DRIFTING":
        return 0, ""
    # walk backwards from the newest stamp until a non-DRIFTING stamp;
    # the earliest DRIFTING stamp in that trailing run starts the streak
    start = None
    for r in reversed(v2):
        if r.get("verdict", {}).get("verdict") != "DRIFTING":
            break
        d = _utc_date(r.get("stamped_at"))
        if d and (start is None or d < start):
            start = d
    if start is None:
        return 0, ""
    return (today - start).days, start.isoformat()


# --------------------------------------------------------------- referent side

def referent_age(pid: str, today: date) -> tuple[str, str]:
    """(age_str, newest_date_str) recomputed live per spec section 2."""
    spec = REFERENTS.get(pid)
    if not spec:
        return "n/a", ""
    files: list[str] = []
    for pat in spec["paths"]:
        hits = glob.glob(str(ROOT / pat))
        files.extend(hits if hits else [])
    if not files:
        return "n/a", ""
    newest: date | None = None
    try:
        if spec.get("line_filter"):
            # 241 MB class file (T5): one regex pass, never per-row json.loads
            with open(files[0], encoding="utf-8", errors="replace") as f:
                for line in f:
                    if spec["line_filter"] not in line:
                        continue
                    m = _TS_DATE_RE.search(line)
                    if m:
                        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                        if newest is None or d > newest:
                            newest = d
        else:
            for fp in files:
                for r in _read_jsonl(Path(fp)):
                    d = _utc_date(r.get(spec["key"]))
                    if d and (newest is None or d > newest):
                        newest = d
    except OSError:
        return "n/a", ""
    if newest is None:
        return "n/a", ""
    return f"{(today - newest).days}d", newest.isoformat()


# --------------------------------------------------------------- rendering

def _verdict_color(verdict: str) -> str:
    # FRAGILE-ALIGNED: provisional ALIGNED per tools/drift_pairs_stamp.py
    # _apply_aging_guard (aging-guard docstring: consumers must treat it as
    # ALIGNED's provisional form); styled amber-green, never default-gray.
    return {"ALIGNED": "#6ee7a0", "FRAGILE-ALIGNED": "#b9e77a",
            "DRIFTING": "#e8c96a",
            "INVERTED": "#ff7a7a", "VACUOUS": "#8aa0b4",
            "DEGENERATE": "#c58aff", "INSUFFICIENT": "#8aa0b4"}.get(verdict, "#ddd")


def build_table(today: date) -> tuple[str, list[dict]]:
    stamps = load_stamps()
    pids = sorted({s.get("pair_id", "?") for s in stamps})
    rows_out = []
    for pid in pids:
        rows = pair_rows(stamps, pid)
        cur = current(rows)
        v = cur.get("verdict", {}) if cur else {}
        age, newest = referent_age(pid, today)
        dd, start = drifting_days(rows, today)
        rows_out.append({
            "pair_id": pid,
            "pair": cur.get("pair", "") if cur else "",
            "teleo": cur.get("teleo", "") if cur else "",
            "history": history_cell(rows),
            "verdict": v.get("verdict", "n/a"),
            "corr": v.get("corr_dm_dr"),
            "deltas": v.get("deltas_used"),
            "ref_age": age,
            "ref_newest": newest,
            "window_end": (cur.get("window", {}) or {}).get("end", "") if cur else "",
            "drifting_days": dd,
            "streak_start": start,
            "weeks_drifting": sum(
                1 for r in rows if r["_gen"] == "v2"
                and r.get("verdict", {}).get("verdict") == "DRIFTING"),
            "weeks_stamped": sum(1 for r in rows if r["_gen"] == "v2"),
        })
    return history_cell(stamps and pair_rows(stamps, pids[0]) or []), rows_out


def markdown_table(rows: list[dict]) -> str:
    lines = [
        "| pair | verdict history | corr | verdict | ref age | window end | DRIFTING-days |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        corr = "n/a" if r["corr"] is None else f"{r['corr']:+.4f}"
        dd = f"{r['drifting_days']}d (since {r['streak_start']})" if r["drifting_days"] \
            else ("0d" if r["verdict"] != "DRIFTING"
                  else f"0d (since {r['streak_start']})")
        lines.append(
            f"| {r['pair_id']} {r['pair']} | {r['history']} | {corr} | "
            f"{r['verdict']} | {r['ref_age']} ({r['ref_newest']}) | "
            f"{r['window_end']} | {dd} |")
    return "\n".join(lines)


def html_page(rows: list[dict], today: date, generated_at: str) -> str:
    e = html.escape
    drifting_now = [r for r in rows if r["verdict"] == "DRIFTING"]
    longest = max((r["drifting_days"] for r in rows), default=0)

    def stalest(r: dict):
        try:
            return int(r["ref_age"].rstrip("d"))
        except (ValueError, AttributeError):
            return -1
    stale = max(rows, key=stalest) if rows else None

    body_rows = []
    for r in rows:
        corr = "n/a" if r["corr"] is None else f"{r['corr']:+.4f}"
        dd = f"{r['drifting_days']}d (since {r['streak_start']})" if r["drifting_days"] else "0d"
        if r["verdict"] == "DRIFTING" and r["streak_start"]:
            dd_label = f"{r['drifting_days']}d (since {r['streak_start']})"
        else:
            dd_label = "0d"
        body_rows.append(
            f"<tr><td><b>{e(r['pair_id'])}</b> {e(r['pair'])}<br>"
            f"<span style='color:#8aa0b4'>{e(r['teleo'])}</span></td>"
            f"<td>{e(r['history'])}</td>"
            f"<td style='color:{_verdict_color(r['verdict'])}'>{e(r['verdict'])}"
            f"<br>{e(corr)} ({e(str(r['deltas']))} deltas)</td>"
            f"<td>{e(r['ref_age'])} (newest {e(r['ref_newest'])};"
            f" stamp window end {e(r['window_end'])})</td>"
            f"<td>{e(dd_label)}<br>"
            f"<span style='color:#8aa0b4'>{r['weeks_drifting']}/{r['weeks_stamped']} weeks</span></td></tr>")

    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Teleo Drift Board</title>
<style>body{{background:#111;color:#ddd;font-family:monospace;margin:2em}}
table{{border-collapse:collapse;margin-top:1em}} td,th{{padding:6px 14px;border:1px solid #333;
text-align:left;vertical-align:top}} .big{{font-size:1.4em}} .mut{{color:#8aa0b4}}</style></head><body>
<h1>TELEO DRIFT BOARD (T1-T6)</h1>
<p>weekly teleological drift verdict history &middot; ledger:
<code>{e(str(LEDGER.relative_to(ROOT)))}</code> &middot; spec: <code>{e(SPEC)}</code></p>
<p class="big">{len(drifting_now)}/{len(rows)} pairs currently DRIFTING &middot;
longest DRIFTING streak {longest}d &middot;
stalest referent: {e(stale['pair_id'] + ' ' + stale['ref_age']) if stale else 'n/a'}</p>
<table><tr><th>pair (teleo)</th><th>verdict history</th><th>current verdict / corr</th>
<th>referent age (live)</th><th>DRIFTING-days</th></tr>
{''.join(body_rows)}
</table>
<p class="mut">{e(LAW)}<br>
verdict colors per tools/drift.py: ALIGNED &ge; +0.5, INVERTED &le; -0.5, DRIFTING between,
VACUOUS = referent never moved. Undated v1 rows are shown but never counted in day math
(their dates are receipt-attested, not row-attested). * marks the current week.</p>
<p class="mut">generated {e(generated_at)} (UTC) by tools/drift_dashboard.py &middot;
static build: rerun the tool to refresh; the artifact (jsonl) is the sovereign record.</p>
</body></html>"""


def _ref_age_days(ref_age: str) -> int | None:
    """B2-225: parse "51d" -> 51; n/a or unparseable never fires."""
    if not ref_age or not ref_age.endswith("d"):
        return None
    try:
        return int(ref_age[:-1])
    except ValueError:
        return None


def alarm_breaches(rows: list[dict]) -> list[dict]:
    """B2-225: rows crossing the streak 14d or referent 30d thresholds."""
    out = []
    for r in rows:
        streak = r.get("drifting_days") or 0
        age = _ref_age_days(r.get("ref_age", ""))
        if streak >= 14 or (age is not None and age >= 30):
            out.append(r)
    return out


def run_alarm(rows: list[dict], today: date, generated_at: str) -> int:
    """Spec section 4b: one dated inbox row on breach, exit 2; quiet exits 0
    and writes nothing. Proposal surface only (never mutates the ledger)."""
    breaches = alarm_breaches(rows)
    if not breaches:
        print("alarm: quiet (no streak >= 14d, no referent >= 30d)")
        return 0
    lines = [f"# DRIFT ALARM {generated_at}", "",
             f"{len(breaches)} breach(es): streak >= 14d or referent >= 30d.", ""]
    for r in breaches:
        age = r.get("ref_age", "n/a")
        lines.append(
            f"- {r['pair_id']} ({r.get('pair', '')}): verdict {r.get('verdict', 'n/a')}, "
            f"DRIFTING streak {r.get('drifting_days', 0)}d (since {r.get('streak_start', 'n/a')}), "
            f"referent age {age} (newest {r.get('ref_newest', 'n/a')})")
    lines += ["", "Proposal surface only (B2-225): model text proposes; the "
              "switchboard/effect broker authorizes effects. Ledger untouched."]
    out = ROOT / "watch" / "inbox" / f"DRIFT_ALARM_{today.isoformat()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nalarm row: {out.relative_to(ROOT)}")
    return 2


def main(argv: list[str]) -> int:
    today = datetime.now(timezone.utc).date()
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _, rows = build_table(today)

    if "--alarm" in argv:
        return run_alarm(rows, today, generated_at)

    if "--check" in argv:
        if not OUT_HTML.exists() or not LEDGER.exists():
            print("check: FAIL (missing output or ledger)")
            return 2
        if OUT_HTML.stat().st_mtime < LEDGER.stat().st_mtime:
            print("check: FAIL (panel older than ledger)")
            return 2
        print("check: OK (panel at least as fresh as ledger)")
        return 0

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_page(rows, today, generated_at), encoding="utf-8")
    print(markdown_table(rows))
    print(f"\npanel: {OUT_HTML.relative_to(ROOT)} (generated {generated_at})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
