#!/usr/bin/env python3
"""tools/zknot.py - knot the operator's REAL ZCode sessions into boot cards.

DFHack-style named tool (verb: knot). Change #1 of
watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md: 0 of 152 ZCode sessions were
knotted, and the self-steal / "you forgot" loops (469 + 219 prompts) are the
cold-start cost. This writes one compact markdown card per real session and a
boot recap the next seat reads first.

  memory/zknot/<date>_<session_id>.md   one card per session (date = ET start)
  memory/zknot/LATEST.md                last 3 cards + the self-steal meter
  memory/runs/zknot/runs.jsonl          one receipt row per run

Selection: task_type not subagent_child/workflow_child, no parent, >=5 real
user prompts (message.semantics.origin == real_user). Templated cron prompts
are dropped with the dive's rule (same 40-char prefix seen >=8 times and longer
than 150 chars). Deterministic extraction only, no LLM calls. The db opens
mode=ro, always. Idempotent: an existing card is rewritten only when the
session grew (more user prompts than the card header records).

Self-steal: DB path and the mode=ro open come from mag/knot_at_close.py; secret
patterns come from mag/mind_window.py (_SECRET_PATTERNS, _is_content_hash).
Stop: create state/zknot.off (the run exits 0 and logs a receipt row).

  .venv/Scripts/python.exe tools/zknot.py [--since YYYY-MM-DD] [--n 20] [--dry-run]

S1 no-silent-truncation gate (ouroboros R4-L1, 2026-10-05): LATEST.md carded
only the newest 3 qualifying sessions and the [:3] rewrite dropped the rest
WITHOUT naming them (2026-10-05 row: qualifying 18, LATEST carried 3 cards,
zero omission tokens). LATEST now names every qualifying session the card cut
(omission block, newest first), and if a rewrite ever drops qualifying
sessions unnamed the run exits 2 and leaves the previous LATEST in place
(fail-closed, the day-4 mine's no-silent-truncation demand).

Meter alarm (lane d05-meter-alarm, dogfood-100m-20261006): the meter was
computed week-over-week with no consumer - the 2026-10-06 LATEST line read
last 7d 126 vs prior 7d 108 (a worsening) and nothing alerted. Every
non-dry-run run now evaluates two legs and appends one deduped alert row to
memory/attention.md (gate_age_patrol.py convention) when either fires:
WORSENED (last 7d > prior 7d) or BASELINE (last 7d >= dive baseline ~148);
improvement stays quiet. The verdict rides the receipt row as meter_alarm.
WARN-only: never blocks, never changes exit codes, never edits LATEST.md; a
failed append is stamped on the receipt, not swallowed. Meter math, the S1
gate and the alarm layer live in tools/zknot_alarm.py, re-exported here.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DB = Path.home() / ".zcode" / "cli" / "db" / "db.sqlite"  # same db as mag/knot_at_close.py
OUT = ROOT / "memory" / "zknot"
LATEST = OUT / "LATEST.md"
RUNS = ROOT / "memory" / "runs" / "zknot" / "runs.jsonl"
STOP = ROOT / "state" / "zknot.off"
INBOX = ROOT / "watch" / "inbox"
ET = ZoneInfo("America/New_York")
CHILD_TYPES = ("subagent_child", "workflow_child")
MIN_PROMPTS = 5
HEADER_RE = re.compile(r"<!-- zknot v1 session=(\S+) user_msgs=(\d+)")
LATEST_MAX_CARDS = 3

try:  # self-steal: the estate's secret patterns, not a new list
    from mag.mind_window import _SECRET_PATTERNS, _is_content_hash  # type: ignore
except Exception:  # noqa: BLE001
    _SECRET_PATTERNS = [(r"sk-[A-Za-z0-9_-]{16,}", "key")]
    _is_content_hash = lambda tok: False  # noqa: E731
_SECRET_RES = [re.compile(p) for p, _ in _SECRET_PATTERNS]

# Meter math, template filters, S1 gate and the meter alarm (lane
# d05-meter-alarm, 2026-10-06) live in tools/zknot_alarm.py so this runner
# stays under the ratchet's file-length bar; re-exported so callers and
# tests ride zknot.<name> unchanged.
from zknot_alarm import (  # noqa: E402,F401
    FORGOT_RE, METER_BASELINE, METER_TARGET, OMIT_MARK, SELF_STEAL_RE,
    append_attention, is_template, meter, meter_alarm_step, meter_alarm_verdict,
    meter_alert_block, meter_line, meter_nums, s1_gate, template_prefixes)


def redact(s: str) -> str:
    s = re.sub("[\u2013\u2014\ufffd]+", "-", s)  # no em-dashes law; mojibake collapses too
    for pat in _SECRET_RES:
        s = pat.sub(lambda m: m.group(0) if _is_content_hash(m.group(0).strip()) else "[redacted]", s)
    return s


def et(ms: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(ms / 1000, tz=ET)


def fmt_dur(ms: int) -> str:
    m = max(0, ms) // 60000
    return f"{m // 60}h {m % 60:02d}m"


def first_line(text: str, width: int = 150) -> str:
    for ln in (text or "").splitlines():
        ln = " ".join(ln.split())
        if ln:
            return redact(ln if len(ln) <= width else ln[: width - 3] + "...")
    return ""


def load(conn: sqlite3.Connection, since_ms: int) -> tuple[list[dict], dict[str, list[dict]]]:
    sessions = []
    for sid, title, tc, tu, ttype, directory in conn.execute(
        "SELECT id, title, time_created, time_updated, task_type, directory FROM session "
        "WHERE parent_id IS NULL AND task_type NOT IN (?, ?) AND time_updated >= ? "
        "ORDER BY time_updated ASC", (*CHILD_TYPES, since_ms)):
        sessions.append({"id": sid, "title": title or "", "tc": int(tc), "tu": int(tu),
                         "task_type": ttype, "dir": directory or ""})
    prompts: dict[str, list[dict]] = {s["id"]: [] for s in sessions}
    if not sessions:
        return sessions, prompts
    q = ("SELECT m.session_id, m.time_created, "
         " (SELECT group_concat(json_extract(p.data,'$.text'), char(10)) FROM part p "
         "  WHERE p.message_id = m.id AND json_extract(p.data,'$.type') = 'text') "
         "FROM message m WHERE m.session_id = ? AND json_extract(m.data,'$.role') = 'user' "
         "AND coalesce(json_extract(m.data,'$.semantics.origin'),'real_user') = 'real_user' "
         "ORDER BY m.time_created ASC")
    for s in sessions:
        for _sid, t, text in conn.execute(q, (s["id"],)):
            if text and text.strip():
                prompts[s["id"]].append({"t": int(t), "text": text})
    return sessions, prompts


def git_commits(since_ms: int) -> list[tuple[int, str, str]]:
    since = dt.datetime.fromtimestamp(since_ms / 1000, tz=dt.timezone.utc).isoformat()
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "log", f"--since={since}", "--format=%ct|%h|%s"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except Exception:  # noqa: BLE001
        return []
    out = []
    for ln in r.stdout.splitlines():
        parts = ln.split("|", 2)
        if len(parts) == 3 and parts[0].isdigit():
            out.append((int(parts[0]) * 1000, parts[1], redact(parts[2])))
    return out


def inbox_files(since_ms: int) -> list[tuple[int, str]]:
    out = []
    floor = since_ms / 1000
    for dirpath, dirnames, filenames in os.walk(INBOX):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                m = os.stat(p).st_mtime
            except OSError:
                continue
            if m >= floor:
                out.append((int(m * 1000), os.path.relpath(p, ROOT).replace("\\", "/")))
    return out


def pending(conn: sqlite3.Connection, sid: str) -> list[str]:
    rows = conn.execute("SELECT status, priority, content FROM todo WHERE session_id = ? "
                        "AND status IN ('pending','in_progress') ORDER BY position", (sid,)).fetchall()
    return [f"[{st}|{pr}] {first_line(c, 160)}" for st, pr, c in rows]


def card(s: dict, human: list[dict], n_user: int, n_tmpl: int, todo: list[str],
         commits: list, receipts: list) -> str:
    a, b = et(s["tc"]), et(s["tu"])
    seen, lines = set(), []
    for p in human:
        fl = first_line(p["text"])
        k = fl.lower()
        if fl and k not in seen:
            seen.add(k)
            lines.append(f"- {et(p['t']).strftime('%m-%d %H:%M')} {fl}")
    shown = lines[-30:]  # most recent 30: the boot recap needs where he ended, not where he began
    L = [f"# zknot {a.strftime('%Y-%m-%d')} {s['id'][5:13] if s['id'].startswith('sess_') else s['id'][:8]}: "
         f"{first_line(s['title'], 90) or '(untitled)'}",
         f"<!-- zknot v1 session={s['id']} user_msgs={n_user} updated_ms={s['tu']} -->",
         "",
         f"- When: {a.strftime('%Y-%m-%d %H:%M')} ET to {b.strftime('%Y-%m-%d %H:%M')} ET ({fmt_dur(s['tu'] - s['tc'])})",
         f"- Prompts: {len(human)} human ({n_tmpl} templated cron dropped), {len(lines)} distinct first lines; type {s['task_type']}",
         f"- Session: `{s['id']}`",
         "", "## His prompts (first lines, deduped, latest 30)"]
    if len(lines) > len(shown):
        L.append(f"- ... {len(lines) - len(shown)} earlier prompts omitted")
    L += shown or ["- (none)"]
    L += ["", f"## Pending (ZCode todo table, {len(todo)})"]
    L += [f"- {t}" for t in todo[:15]] or ["- (none stored)"]
    if len(todo) > 15:
        L.append(f"- ... +{len(todo) - 15} more")
    L += ["", f"## Commits in window ({len(commits)})"]
    L += [f"- {h} {et(t).strftime('%m-%d %H:%M')} {subj[:110]}" for t, h, subj in commits[:15]] or ["- (none)"]
    if len(commits) > 15:
        L.append(f"- ... +{len(commits) - 15} more (git log --since/--until on the window)")
    L += ["", f"## Receipts written in window ({len(receipts)} under watch/inbox)"]
    L += [f"- {et(t).strftime('%m-%d %H:%M')} {p}" for t, p in receipts[:15]] or ["- (none)"]
    if len(receipts) > 15:
        L.append(f"- ... +{len(receipts) - 15} more")
    return "\n".join(L) + "\n"


def _short_sid(sid: str) -> str:
    return sid[5:13] if sid.startswith("sess_") else sid[:8]


def name_omitted(dropped: list[dict], cap: int = 10) -> list[str]:
    """S1 omission block: NAME every qualifying session the [:3] card cut.

    The 2026-10-05 row measured the disease: 18 qualifying sessions, 3 cards
    in LATEST, zero omission tokens anywhere - a booting seat could not even
    ask what it was not shown. Names carry date + short id + title first line
    so the omission is actionable (the full cards live under memory/zknot/
    or can be regenerated with --n).
    """
    if not dropped:
        return []
    lines = [f"- ... {len(dropped)} {OMIT_MARK} (newest first; cards under memory/zknot/):"]
    for s in dropped[:cap]:
        lines.append(f"  - {et(s['tc']).strftime('%Y-%m-%d')} {_short_sid(s['id'])}: "
                     f"{first_line(s['title'], 80) or '(untitled)'}")
    if len(dropped) > cap:
        lines.append(f"  - ... +{len(dropped) - cap} more (rerun tools/zknot.py --n 40 to card them)")
    return lines


def build_latest(real: list[dict], cards: dict[str, str], mline: str,
                 written_at: str) -> tuple[str, int]:
    """Build LATEST.md text + the count of qualifying sessions the card cut.

    Returns (latest_md, dropped_count). dropped_count > 0 means the [:3]
    rewrite truncated; the caller MUST verify the omission block landed
    (the S1 gate) before serving or writing the recap.
    """
    last3 = [cards[s["id"]] for s in real[:LATEST_MAX_CARDS] if s["id"] in cards]
    dropped = real[LATEST_MAX_CARDS:]
    omit = name_omitted(dropped)
    body = "\n---\n\n".join(re.sub(r"^(#+) ", r"#\1 ", c, flags=re.M) for c in last3)
    if omit:
        body += ("\n\n## Not carded above (the [:3] cut, named per the S1 "
                 f"no-silent-truncation gate)\n\n" + "\n".join(omit))
    # R4-L2 (2026-10-05 memory fold): the recap points at the demotion register
    # beside the meter, so a booting seat can ask what the estate stopped
    # believing and why - promotion is automatic everywhere; demotion must be
    # wired or it stays a memory of whoever was in the room.
    sup = ROOT / "memory" / "fold_history" / "SUPERSEDED.md"
    sup_line = ("Demotion register (what the estate stopped believing and why): "
                "memory/fold_history/SUPERSEDED.md"
                + ("" if sup.is_file() else " (MISSING - mint it)"))
    latest = ("# zknot LATEST (boot recap: last 3 real ZCode sessions)\n\n"
              f"{mline}\n\n"
              f"{sup_line}\n\n"
              f"_Written {written_at} ET by tools/zknot.py "
              "(deterministic, no LLM). Stop: state/zknot.off._\n\n"
              + body)
    return latest, len(dropped)


def receipt(row: dict) -> None:
    RUNS.parent.mkdir(parents=True, exist_ok=True)
    with RUNS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since", help="YYYY-MM-DD (ET); sessions updated on/after. Default: 7 days ago")
    ap.add_argument("--n", type=int, default=20, help="max cards to (re)write this run, newest first")
    ap.add_argument("--dry-run", action="store_true", help="print what would be written; write nothing")
    ap.add_argument("--actor", default=os.environ.get("ZKNOT_ACTOR", ""),
                    help="who fired this run; stamped on the runs.jsonl receipt row "
                         "(default env ZKNOT_ACTOR, else manual)")
    ap.add_argument("--trigger", default=os.environ.get("ZKNOT_TRIGGER", ""),
                    help="what fired this run (mag.boot_regen chain, MagBootRegenDaily "
                         "task, mag.cmd context-pack, manual); stamped on the receipt row")
    a = ap.parse_args(argv)
    ts = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    # R4b move 2 (2026-10-06, fold S3): every receipt row names its actor and
    # trigger - the 2026-10-05/06 regen burst wrote actor null / trigger null
    # because the caller never rode down to the organ. mag/boot_regen.py
    # passes --actor mag.boot_regen --trigger <its caller>; a bare hand run
    # reads manual/manual instead of null.
    stamp = {"actor": (a.actor or "").strip() or "manual",
             "trigger": (a.trigger or "").strip() or "manual"}
    if STOP.exists():
        print("zknot: stop file state/zknot.off present, exiting")
        if not a.dry_run:
            receipt({**stamp, "ts": ts, "tool": "zknot", "status": "stopped",
                     "stop_file": "state/zknot.off"})
        return 0
    now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
    if a.since:
        since_ms = int(dt.datetime.strptime(a.since, "%Y-%m-%d").replace(tzinfo=ET).timestamp() * 1000)
    else:
        since_ms = now_ms - 7 * 86400 * 1000
    load_ms = min(since_ms, now_ms - 30 * 86400 * 1000)  # 30d floor so the template rule has volume
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    try:
        sessions, prompts = load(conn, load_ms)
        tmpl = template_prefixes(prompts)
        real = [s for s in sessions if s["tu"] >= since_ms and len(prompts[s["id"]]) >= MIN_PROMPTS]
        real.sort(key=lambda s: s["tu"], reverse=True)
        earliest = min((s["tc"] for s in real), default=now_ms)
        commits = git_commits(earliest)
        files = inbox_files(earliest)
        written, skipped, cards = [], 0, {}
        for s in real:
            n_user = len(prompts[s["id"]])
            path = OUT / f"{et(s['tc']).strftime('%Y-%m-%d')}_{s['id']}.md"
            old = None
            if path.exists():
                m = HEADER_RE.search(path.read_text(encoding="utf-8", errors="replace")[:600])
                old = int(m.group(2)) if m else 0
            if old is not None and old >= n_user:
                skipped += 1
                cards[s["id"]] = path.read_text(encoding="utf-8", errors="replace")
                continue
            if len(written) >= a.n:
                continue
            human = [p for p in prompts[s["id"]] if not is_template(p, tmpl)]
            text = card(s, human, n_user, n_user - len(human), pending(conn, s["id"]),
                        [c for c in commits if s["tc"] <= c[0] <= s["tu"]],
                        sorted([f for f in files if s["tc"] <= f[0] <= s["tu"]], reverse=True))
            cards[s["id"]] = text
            written.append(path.relative_to(ROOT).as_posix())
            if a.dry_run:
                print(f"would write {path.relative_to(ROOT).as_posix()} ({len(text)} chars)")
            else:
                OUT.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
        mnums = meter_nums(prompts, tmpl, now_ms)
        mline = meter_line(mnums)
        latest, dropped = build_latest(real, cards, mline,
                                       dt.datetime.now(ET).strftime("%Y-%m-%d %H:%M"))
        if a.dry_run:
            print(mline)
            av = meter_alarm_verdict(mnums)
            print("dry-run: meter alarm " + (f"WOULD FIRE: {'; '.join(av['legs'])}" if av["fire"]
                                             else "quiet (no worsening, below baseline)"))
            print(f"dry-run: {len(written)} card(s) would be written, {skipped} up to date, "
                  f"{len(real)} qualifying sessions, {len(tmpl)} cron templates, "
                  f"{dropped} would be named as the [:3] cut")
        else:
            # S1 no-silent-truncation gate (R4-L1, 2026-10-05): the [:3]
            # rewrite dropped qualifying sessions; the omission block MUST
            # name them or the recap is silently truncated. Fail closed:
            # keep the previous LATEST, file the receipt, exit 2 so the
            # context-pack regen chain (mag/boot_regen.py) surfaces it.
            # Cause: build_latest dropped sessions without an omission
            # block; evidence: tests/test_zknot_gate.py.
            if s1_gate(dropped, latest):
                receipt({**stamp, "ts": ts, "tool": "zknot", "status": "truncated-unnamed",
                         "qualifying": len(real), "dropped_unnamed": dropped})
                print(f"zknot: S1 GATE - {dropped} qualifying sessions dropped by the "
                      "[:3] rewrite without naming; previous LATEST kept, exit 2")
                return 2
            OUT.mkdir(parents=True, exist_ok=True)
            LATEST.write_text(latest, encoding="utf-8")
            alarm = meter_alarm_step(mnums)
            receipt({**stamp, "ts": ts, "tool": "zknot", "status": "ok", "qualifying": len(real),
                     "written": written, "skipped_up_to_date": skipped, "templates": len(tmpl),
                     "dropped_named": dropped, "meter": mline, "meter_alarm": alarm})
            print(f"zknot: {len(written)} card(s) written, {skipped} up to date, {len(real)} qualifying; "
                  f"LATEST.md refreshed ({dropped} dropped sessions named)")
            print(mline)
            if alarm["fire"]:
                if alarm.get("error"):
                    print(f"zknot: METER ALARM fired but attention append failed: {alarm['error']}")
                elif alarm["appended"]:
                    print(f"zknot: METER ALARM - {'; '.join(alarm['legs'])}; "
                          "alert row appended to memory/attention.md")
                else:
                    print("zknot: METER ALARM - alert row already present today (dedup on key line)")
            else:
                print("zknot: meter quiet (no worsening, below baseline)")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
