#!/usr/bin/env python3
"""compile_seats - deterministic recompiler for memory/improve/SEATS.md.

Self-steal: the 2026-09-27 content was a one-shot hand refresh (ATLAS_SELF_STEAL
Q2, watch/inbox/ATLAS_SELF_STEAL_20260927.md GAP 2) appended under the August
seat matrix. This tool keeps that structure:

  1. the hand doctrine (August matrix, janitor doctrine, invariants, commands,
     CODE TEAM) is carried VERBATIM from the current file,
  2. the dated 2026-09-27 REALITY REFRESH section is carried VERBATIM (history),
  3. a COMPILED SEAT REALITY section is regenerated from real sources only,
     every bullet tagged [src: path]. Drift between the hand matrix and the
     live config is reported, never silently rewritten.

Deterministic: no wall clock; time windows anchor on the newest timestamp found
in the sources. Same inputs give the same bytes.

Usage:
  python tools/compile_seats.py            # write memory/improve/SEATS.md.new
  python tools/compile_seats.py --swap     # write .new, then replace SEATS.md (backup .bak-<date>)
  python tools/compile_seats.py --check    # exit 1 if SEATS.md differs from a fresh compile
Never reads secret files (.env, configs/keys.json, state/keys, *.key).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEATS = ROOT / "memory" / "improve" / "SEATS.md"
LANES = ROOT / "configs" / "lanes.yaml"
PROVIDERS = ROOT / "configs" / "providers.yaml"
MATES = ROOT / "configs" / "mates.yaml"
LANE_DIR = ROOT / "queue" / "lanes"
ORCH = ROOT / "memory" / "runs" / "orchestrator_trail.jsonl"
ZKNOT = ROOT / "memory" / "zknot"
CURRENT = ROOT / "state" / "CURRENT.md"

REFRESH_MARK = "## 2026-09-27 REALITY REFRESH"
COMPILED_MARK = "## COMPILED SEAT REALITY"


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def parse_ts(s: str) -> dt.datetime | None:
    try:
        t = dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)


def split_existing(text: str) -> tuple[str, str]:
    """Return (hand_doctrine, refresh_section) carried verbatim."""
    if COMPILED_MARK in text:
        text = text.split(COMPILED_MARK, 1)[0]
    if REFRESH_MARK not in text:
        return text.rstrip() + "\n", ""
    head, tail = text.split(REFRESH_MARK, 1)
    return head.rstrip() + "\n", (REFRESH_MARK + tail).rstrip() + "\n"


def lanes_facts(out: list[str], drift: list[str], hand: str) -> None:
    d = yaml.safe_load(LANES.read_text(encoding="utf-8")) or {}
    src = rel(LANES)
    out.append(f"- Default lane: {d.get('default_lane')} [src: {src}]")
    for k, v in (d.get("lanes") or {}).items():
        out.append(f"- Lane {k}: {v.get('name')} via {v.get('backend')} [src: {src}]")
    lm = d.get("local_models") or {}
    if lm:
        pairs = ", ".join(f"{k}={v}" for k, v in lm.items())
        out.append(f"- Local models: {pairs} [src: {src}]")
    lp = d.get("load_policy") or {}
    if lp:
        out.append(f"- Load policy: mode {lp.get('mode')}, max_resident {lp.get('max_resident')} [src: {src}]")
    h = d.get("hermes") or {}
    if h:
        out.append(f"- Hermes: parked={h.get('parked')}, role={h.get('role')}, not_router={h.get('not_router')} [src: {src}]")
    gb = d.get("grok_budget") or {}
    if gb:
        out.append(f"- Grok budget: max_escalations_per_day={gb.get('max_escalations_per_day')}, require_priority={gb.get('require_priority')} [src: {src}]")
    # drift: the hand matrix vs live config
    worker = lm.get("worker")
    if worker and "**L0 worker** | Ollama **`gemma4`**" in hand and worker != "gemma4":
        drift.append(f"- Hand matrix says L0 worker = gemma4; live config local_models.worker = {worker} [src: {src}]")
    if h.get("parked") is False and "| **L2-Hermes** | **Parked.**" in hand:
        drift.append(f"- Hand matrix says L2-Hermes = Parked; live config hermes.parked = false (role {h.get('role')}) [src: {src}]")
    clerk = lm.get("clerk")
    if clerk and "Ollama **`gemma:2b`** (clerk/router)" in hand and clerk != "gemma:2b":
        drift.append(f"- Hand matrix says clerk = gemma:2b; live config local_models.clerk = {clerk} [src: {src}]")


def providers_facts(out: list[str]) -> None:
    d = yaml.safe_load(PROVIDERS.read_text(encoding="utf-8")) or {}
    src = rel(PROVIDERS)
    order = (d.get("defaults") or {}).get("prefer_order") or []
    out.append(f"- Provider prefer_order ({len(order)}): {', '.join(order)} [src: {src}]")
    provs = d.get("providers") or {}
    dormant = sorted(k for k, v in provs.items() if isinstance(v, dict) and v.get("dormant"))
    live = sorted(k for k, v in provs.items() if isinstance(v, dict) and not v.get("dormant"))
    out.append(f"- Provider blocks: {len(provs)} declared, {len(live)} not dormant, {len(dormant)} dormant ({', '.join(dormant)}) [src: {src}]")


def mates_facts(out: list[str]) -> None:
    if not MATES.is_file():
        return
    d = yaml.safe_load(MATES.read_text(encoding="utf-8")) or {}
    ids = [m.get("id") for m in d.get("mates") or [] if isinstance(m, dict)]
    out.append(f"- Leave-protocol mates ({len(ids)}): {', '.join(map(str, ids))}; schema {d.get('schema')} v{d.get('version')} [src: {rel(MATES)}]")


def lane_runner_facts(out: list[str]) -> list[dt.datetime]:
    stamps: list[dt.datetime] = []
    if not LANE_DIR.is_dir():
        return stamps
    for lane in sorted(p for p in LANE_DIR.iterdir() if p.is_dir()):
        f = lane / "runner_state.json"
        if not f.is_file():
            continue
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            out.append(f"- Lane runner {lane.name}: runner_state unreadable [src: {rel(f)}]")
            continue
        t = parse_ts(s.get("last_run", ""))
        if t:
            stamps.append(t)
        res = str(s.get("last_result", "?")).replace("\n", " ")
        res = re.sub(r"[A-Za-z0-9_]*KEY[A-Za-z0-9_]*", "<key-name>", res)
        if len(res) > 110:
            res = res[:107] + "..."
        out.append(f"- Lane runner {lane.name} (seat {s.get('seat', lane.name)}): last_run {s.get('last_run', '?')}, last_result `{res}` [src: {rel(f)}]")
    return stamps


def orch_facts(out: list[str]) -> list[dt.datetime]:
    if not ORCH.is_file():
        return []
    rows = []
    with ORCH.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            t = parse_ts(r.get("timestamp", ""))
            if t:
                rows.append((t, str(r.get("event", "?"))))
    if not rows:
        return []
    newest = max(t for t, _ in rows)
    lo = newest - dt.timedelta(days=7)
    counts: dict[str, int] = {}
    for t, ev in rows:
        if t > lo:
            counts[ev] = counts.get(ev, 0) + 1
    cs = ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    out.append(f"- Orchestrator (DeepSeek drain) events in the 7d before {newest.isoformat(timespec='seconds')}: {cs} [src: {rel(ORCH)}]")
    return [newest]


def zknot_facts(out: list[str]) -> None:
    if not ZKNOT.is_dir():
        return
    cards = sorted(p for p in ZKNOT.iterdir() if p.suffix == ".md" and p.name[:4].isdigit())
    if not cards:
        return
    last = cards[-1]
    when = ""
    for line in last.read_text(encoding="utf-8", errors="replace").splitlines()[:12]:
        if line.startswith("- When:"):
            when = line[len("- When:"):].strip()
            break
    out.append(f"- Operator session cards: {len(cards)} zknot cards; newest {last.name} ({when}) [src: {rel(ZKNOT)}/]")


def current_fact(out: list[str]) -> None:
    if CURRENT.is_file():
        out.append(f"- Live brief present: state/CURRENT.md (load-order truth per the 2026-09-27 refresh) [src: {rel(CURRENT)}]")


def compile_text() -> str:
    hand, refresh = split_existing(SEATS.read_text(encoding="utf-8").replace("\r\n", "\n"))
    facts: list[str] = []
    drift: list[str] = []
    lanes_facts(facts, drift, hand)
    providers_facts(facts)
    mates_facts(facts)
    stamps = lane_runner_facts(facts)
    stamps += orch_facts(facts)
    zknot_facts(facts)
    current_fact(facts)
    anchor = max(stamps).isoformat(timespec="seconds") if stamps else "unknown"
    parts = [hand.rstrip(), ""]
    if refresh:
        parts += [refresh.rstrip(), ""]
    parts += [
        f"{COMPILED_MARK} (tools/compile_seats.py; regenerated, do not hand-edit below this line)",
        "",
        f"Source anchor (newest source timestamp): {anchor}. Every bullet names its source file.",
        "",
        "### Seats and lanes as configured",
        "",
        *facts,
        "",
        "### Drift: hand matrix vs live config",
        "",
        *(drift or ["- none detected"]),
        "",
        "Rebuild: `python tools/compile_seats.py --swap` (registered in configs/fossil_registry.json).",
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description="recompile memory/improve/SEATS.md from sources")
    ap.add_argument("--swap", action="store_true", help="replace SEATS.md after writing .new (backs up old)")
    ap.add_argument("--check", action="store_true", help="exit 1 if SEATS.md is not a fresh compile")
    a = ap.parse_args()
    text = compile_text()
    if a.check:
        same = SEATS.read_bytes().decode("utf-8").replace("\r\n", "\n") == text
        print("COMPILE-SEATS: fresh" if same else "COMPILE-SEATS: drifted from sources")
        return 0 if same else 1
    new = SEATS.with_name("SEATS.md.new")
    eol = "\r\n" if b"\r\n" in SEATS.read_bytes() else "\n"
    new.write_text(text, encoding="utf-8", newline=eol)
    print(f"COMPILE-SEATS: wrote {rel(new)} ({len(text)} chars)")
    if a.swap:
        bak = SEATS.with_name("SEATS.md.bak-" + dt.date.today().strftime("%Y%m%d"))
        if not bak.exists():
            shutil.copy2(SEATS, bak)
        new.replace(SEATS)
        print(f"COMPILE-SEATS: swapped in, backup {rel(bak)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
