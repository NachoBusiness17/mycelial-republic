"""Provider-error tally for a ZCode agent session family.

Closes the B2-25 falsifier 1 blind spot (watch/inbox/burn_wave_20260926/
B2_25_envelope_remeasure_20260926.md): a main-session retry (maxAttempts 11)
absorbs 429/1302 provider errors silently, so a receipt that greps agent
outputs for "1302" can only ever prove "zero surfaced into lane bytes", never
"zero occurred". The driver logs every attempt it sees to the daily CLI log
(log/zcode-YYYY-MM-DD.jsonl) as model.network.failed and
model.network.completed events; this tool counts those events for one session
family and writes a session error tally file (provider_errors.json) next to
the agent metadata.json files, so envelope probes read the counter from the
same directory they already read durations and tokens from.

Counts, all derived only from log bytes:
- network_failed_events: model.network.failed events (driver-visible failures,
  including retries that later succeed).
- absorbed_retries: for completed events with context.attempt > 1, the sum of
  (attempt - 1). These are failures the retry layer absorbed before any lane
  byte could see them.
- terminal_failed_turns: turns that logged at least one failure and never
  completed (the failures that actually surfaced as errors).
- statusCode_counts / reason_counts / count_1302_statusmessage: the 429 vs
  1302 split taken from context.statusCode and the "[1302]" marker inside
  context.statusMessage.
- maxAttempts_counts / querySource_counts: documents the retry asymmetry
  (main-session family maxAttempts 11, workflow children maxAttempts 0).

Usage:
  python tools/provider_error_tally.py --session sess_fd5ec147
  python tools/provider_error_tally.py --session sess_fd5ec147 --since 2026-09-26T11:24:00Z --until 2026-09-26T11:46:00Z

ENVELOPE LAW (B2-441, 2026-09-26): any wave receipt claiming a 1302 count
("zero 1302", "N x 1302") is INVALID unless it cites a provider_errors.json
(or equivalent per-wave tally JSON) written in the SAME session as the wave.
Post-wave one-liner (the dispatcher flow runs this after every wave lands):

  python tools/provider_error_tally.py --session <wave-session-id> --out <session-dir>/provider_errors.json

Falsifier: a receipt claiming "zero 1302" whose session dir holds no tally
file, or whose tally shows a nonzero network_failed_events count, is invalid
by this law (B2-25 measured 287 absorbed 1302 retries across three waves the
B2-25 receipt had called clean with zero surfaced bytes).
  python tools/provider_error_tally.py --session sess_fd5ec147 --out D:/elsewhere/tally.json

Defaults: --log is today's log under <cli>/log, --out is
<cli>/agents/<session>/provider_errors.json. Attribution: a log line belongs
to the session family when its sessionId equals the session id or extends it
(sess_subagent_agent_* children, sess_dwf-* actor children) or when
context.parentSessionId equals it.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

NETWORK_EVENTS = {"model.network.failed", "model.network.completed"}


def _default_cli_root() -> str:
    return os.path.join(os.path.expanduser("~"), ".zcode", "cli")


def _default_log_path(cli_root: str, day: Optional[str] = None) -> str:
    if day is None:
        day = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
    return os.path.join(cli_root, "log", "zcode-%s.jsonl" % day)


def _belongs(line_session_id: str, parent_session_id: Any, session: str) -> bool:
    if not isinstance(line_session_id, str):
        return False
    if line_session_id == session or line_session_id.startswith(session + "-"):
        return True
    return isinstance(parent_session_id, str) and parent_session_id == session


def _load_agent_registry(session_dir: str) -> Dict[str, Dict[str, Any]]:
    """Map childSessionId -> {agentId, description, createdAt} from metadata.json files."""
    registry: Dict[str, Dict[str, Any]] = {}
    if not os.path.isdir(session_dir):
        return registry
    for name in sorted(os.listdir(session_dir)):
        meta_path = os.path.join(session_dir, name, "metadata.json")
        if not os.path.isfile(meta_path):
            continue
        try:
            with open(meta_path, "r", encoding="utf-8") as fh:
                meta = json.load(fh)
        except (OSError, ValueError):
            continue
        child = meta.get("childSessionId")
        if isinstance(child, str):
            registry[child] = {
                "agentId": meta.get("agentId", ""),
                "description": meta.get("description", ""),
                "createdAt": meta.get("createdAt", ""),
            }
    return registry


def _wave_clusters(agents: Dict[str, Dict[str, Any]], gap_minutes: float = 10.0) -> List[Dict[str, Any]]:
    """B2-442 (2026-09-26): cluster the session's agents by createdAt gaps.

    Replaces the hand-drawn per-wave --since/--until windows (B2-98, B2-25
    both drew them by hand from metadata createdAt clusters). Waves are the
    maximal runs of agent createdAt values where consecutive agents start
    within `gap_minutes` of each other; each wave becomes a [since, until)
    window (until = next wave's start, last wave open-ended).
    """
    created = sorted(
        a.get("createdAt", "") for a in agents.values() if a.get("createdAt")
    )
    if not created:
        return []
    from datetime import datetime as _dt

    def _parse(ts: str) -> _dt:
        return _dt.fromisoformat(ts.replace("Z", "+00:00"))

    clusters: List[List[str]] = [[created[0]]]
    for ts in created[1:]:
        try:
            gap = (_parse(ts) - _parse(clusters[-1][-1])).total_seconds()
        except ValueError:
            continue
        if gap <= gap_minutes * 60:
            clusters[-1].append(ts)
        else:
            clusters.append([ts])
    waves: List[Dict[str, Any]] = []
    for i, c in enumerate(clusters):
        waves.append({
            "since": c[0],
            "until": clusters[i + 1][0] if i + 1 < len(clusters) else "",
            "agents_started": len(c),
            "first_created": c[0],
            "last_created": c[-1],
        })
    return waves


def tally_session(
    session: str,
    log_paths: Iterable[str],
    session_dir: str = "",
    since: str = "",
    until: str = "",
) -> Dict[str, Any]:
    """Count provider-error events for one session family from log bytes."""
    registry = _load_agent_registry(session_dir) if session_dir else {}

    completed = 0
    failed_events = 0
    other_network_events = 0
    status_codes: Counter = Counter()
    reasons: Counter = Counter()
    count_1302 = 0
    max_attempts: Counter = Counter()
    query_sources: Counter = Counter()
    turn_failures: Counter = Counter()
    turn_completed: set = set()
    per_agent: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "completed": 0,
            "failed_events": 0,
            "absorbed_retries": 0,
            "max_attempt_seen": 0,
            "terminal_failed_turns": 0,
        }
    )
    first_ts = ""
    last_ts = ""
    matched = 0

    for log_path in log_paths:
        if not os.path.isfile(log_path):
            continue
        with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                # Cheap prefilters before parsing: the event name and the
                # session id must both appear in the raw line.
                if "model.network" not in raw:
                    continue
                if session not in raw:
                    continue
                try:
                    line = json.loads(raw)
                except ValueError:
                    continue
                event = line.get("event", "")
                if event not in NETWORK_EVENTS:
                    if event.startswith("model.network"):
                        other_network_events += 1
                    continue
                ctx = line.get("context") or {}
                if not _belongs(line.get("sessionId", ""), ctx.get("parentSessionId"), session):
                    continue
                ts = str(line.get("timestamp", ""))
                if since and ts < since:
                    continue
                if until and ts > until:
                    continue
                matched += 1
                if not first_ts:
                    first_ts = ts
                if ts > last_ts:
                    last_ts = ts

                child_id = str(line.get("sessionId", ""))
                turn_id = str(line.get("turnId", ""))
                attempt = ctx.get("attempt")
                attempt = attempt if isinstance(attempt, int) else 0
                bucket = per_agent[child_id]

                if event == "model.network.completed":
                    completed += 1
                    bucket["completed"] += 1
                    turn_completed.add((child_id, turn_id))
                    if attempt > 1:
                        absorbed = attempt - 1
                        bucket["absorbed_retries"] += absorbed
                        bucket["max_attempt_seen"] = max(bucket["max_attempt_seen"], attempt)
                else:
                    failed_events += 1
                    bucket["failed_events"] += 1
                    turn_failures[(child_id, turn_id)] += 1
                    code = ctx.get("statusCode")
                    status_codes[str(code)] += 1
                    reason = ctx.get("reason")
                    if isinstance(reason, str) and reason:
                        reasons[reason] += 1
                    message = ctx.get("statusMessage")
                    if isinstance(message, str) and "[1302]" in message:
                        count_1302 += 1
                max_att = ctx.get("maxAttempts")
                if isinstance(max_att, int):
                    max_attempts[str(max_att)] += 1
                source = ctx.get("querySource")
                if isinstance(source, str) and source:
                    query_sources[source] += 1
                bucket["max_attempt_seen"] = max(bucket["max_attempt_seen"], attempt)

    terminal_failed_turns = 0
    for (child_id, _turn_id), fails in turn_failures.items():
        if (child_id, _turn_id) not in turn_completed:
            terminal_failed_turns += 1
            per_agent[child_id]["terminal_failed_turns"] += 1
        _ = fails

    absorbed_total = sum(b["absorbed_retries"] for b in per_agent.values())

    per_agent_rows: List[Dict[str, Any]] = []
    for child_id, counts in sorted(per_agent.items()):
        row: Dict[str, Any] = {"childSessionId": child_id}
        row.update(registry.get(child_id, {}))
        row.update(counts)
        per_agent_rows.append(row)

    return {
        "tool": "tools/provider_error_tally.py",
        "session": session,
        "session_dir": session_dir,
        "logs_scanned": [p for p in log_paths if os.path.isfile(p)],
        "window": {"since": since, "until": until, "first_event_ts": first_ts, "last_event_ts": last_ts},
        "totals": {
            "matched_events": matched,
            "network_completed": completed,
            "network_failed_events": failed_events,
            "absorbed_retries": absorbed_total,
            "terminal_failed_turns": terminal_failed_turns,
            "statusCode_counts": dict(sorted(status_codes.items())),
            "reason_counts": dict(sorted(reasons.items())),
            "count_1302_statusmessage": count_1302,
            "maxAttempts_counts": dict(sorted(max_attempts.items())),
            "querySource_counts": dict(sorted(query_sources.items())),
            "other_network_events": other_network_events,
        },
        "per_agent": per_agent_rows,
        "notes": [
            "network_failed_events counts every model.network.failed event the driver logged, including retries that later completed.",
            "absorbed_retries counts failures the retry layer absorbed before completion: completions with attempt > 1 contribute attempt - 1 each.",
            "terminal_failed_turns counts turns with at least one failure and no completed event; those are the failures that surfaced as errors.",
            "count_1302_statusmessage counts failed events whose statusMessage carries the [1302] rate-limit marker.",
        ],
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Provider-error tally for one agent session family.")
    parser.add_argument("--session", required=True, help="Session id or unambiguous prefix, e.g. sess_fd5ec147")
    parser.add_argument("--log", action="append", default=[], help="Log file to scan; repeatable. Default: today's CLI log.")
    parser.add_argument("--since", default="", help="ISO timestamp lower bound (inclusive string compare).")
    parser.add_argument("--until", default="", help="ISO timestamp upper bound (inclusive string compare).")
    parser.add_argument("--out", default="", help="Output tally JSON path. Default: <agents>/<session>/provider_errors.json")
    parser.add_argument("--cli-root", default=_default_cli_root(), help="ZCode CLI root (default ~/.zcode/cli).")
    parser.add_argument("--waves", action="store_true", help="B2-442: cluster the session's agents by createdAt gaps and emit one totals block per wave into the same output JSON, plus the combined block.")
    parser.add_argument("--wave-gap-minutes", type=float, default=10.0, help="createdAt gap that starts a new wave (default 10).")
    parser.add_argument("--quiet", action="store_true", help="Print only the output path.")
    args = parser.parse_args(argv)

    cli_root = args.cli_root
    session = args.session
    agents_root = os.path.join(cli_root, "agents")
    session_dir = ""
    if os.path.isdir(agents_root):
        for name in sorted(os.listdir(agents_root)):
            if name == session or name.startswith(session):
                session_dir = os.path.join(agents_root, name)
                session = name
                break

    log_paths = args.log or [_default_log_path(cli_root)]
    result = tally_session(session, log_paths, session_dir=session_dir, since=args.since, until=args.until)

    if args.waves:
        agents = _load_agent_registry(session_dir) if session_dir else {}
        waves = _wave_clusters(agents, gap_minutes=args.wave_gap_minutes)
        wave_blocks: List[Dict[str, Any]] = []
        for i, w in enumerate(waves):
            wr = tally_session(session, log_paths, session_dir=session_dir,
                               since=w["since"], until=w["until"])
            wave_blocks.append({
                "wave": i + 1,
                "since": w["since"], "until": w["until"],
                "agents_started": w["agents_started"],
                "window": wr.get("window"),
                "totals": wr.get("totals"),
            })
        result["schema"] = "provider_error_tally.waves.v1"
        result["wave_gap_minutes"] = args.wave_gap_minutes
        result["agent_count"] = len(agents)
        result["waves"] = wave_blocks

    out_path = args.out or (os.path.join(session_dir, "provider_errors.json") if session_dir else "provider_errors.json")
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    totals = result["totals"]
    if args.quiet:
        print(out_path)
    else:
        print(
            "session %s: failed=%d absorbed=%d terminal_turns=%d 1302=%d status429=%s -> %s"
            % (
                session,
                totals["network_failed_events"],
                totals["absorbed_retries"],
                totals["terminal_failed_turns"],
                totals["count_1302_statusmessage"],
                totals["statusCode_counts"].get("429", 0),
                out_path,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
