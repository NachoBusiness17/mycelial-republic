#!/usr/bin/env python3
"""session_cards.py - one .card.json per human session under memory/biography/cards/ (Q-003, 2026-09-28).

The disease this fixes: the cards dir held only 8 dossier cards (plus a degenerate
latest.card.json with session_id "latest" and zero themes) against 104 dossier
sessions, so docs/DNA.md:114's "latest card" answer to "What was I doing?" was
empty and 96 human sessions had no card.

Sources, in priority order:

  1. memory/biography/*.dossier.json (schema session_dossier.v4_chord_knot).
     Each dossier embeds a session_card.v1 (keys: schema, title, one_liner,
     blurb, bullets, themes, dominant_theme, ask_count). A dossier counts as a
     HUMAN session when seat.source is not "mag_agent" AND (operator_prompts is
     non-empty or ask_count > 0). Ground truth (2026-09-28 scan): 77 dossiers
     carry seat {"source": "mag_agent"} (orc-* janitor/orchestrator tapes and
     seat tests, agent asks like "[janitor] FKB signal ..."), 19 UUID dossiers
     carry seat {"source": "grok"} of which 5 hold operator prompts, and 8
     early UUID dossiers have no seat at all but real operator prompts.
     Dossiers that fail the human test are skipped and reported, never
     silently dropped.
  2. memory/sessions/*.json (schema session_record.v1). Daily build records;
     carded with strictly factual fields read from the record itself.

Excluded on purpose: memory/agent_sessions/* seat tapes and the mag_agent rows
of memory/biography/index.jsonl (orc-* orchestrator tapes) - those are agent
sessions, not human sessions.

Card content is copied from the embedded session_card verbatim except:
  - session_id, source, generated_by, generated_at are attached;
  - em-dashes/en-dashes are normalized to "-" per the repo no-em-dash law.

Additive by default: an existing <session_id>.card.json is never clobbered
unless --force (the 8 pre-existing cards use an older scored-themes shape and
are preserved as-is). latest.card.json is refreshed to mirror the newest
carded human session when the current file is degenerate; docs/DNA.md:114
makes that file the "What was I doing?" lookup.

Usage: python tools/session_cards.py [--root PATH] [--force] [--dry-run]
Exit codes: 0 = ensure pass ran (writes done, skipped, or nothing to do);
            2 = cannot verify (cards dir could not be ensured, or no source
            files found at all under the root).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DEFAULT = Path(__file__).resolve().parent.parent
GENERATED_BY = "tools/session_cards.py"
DASHES = {"\u2014": "-", "\u2013": "-", "\u2212": "-"}


def _clean(text: Any) -> Any:
    """Normalize dash characters per the repo no-em-dash law; recurse containers."""
    if isinstance(text, str):
        for bad, good in DASHES.items():
            text = text.replace(bad, good)
        return text
    if isinstance(text, list):
        return [_clean(x) for x in text]
    if isinstance(text, dict):
        return {k: _clean(v) for k, v in text.items()}
    return text


def _public(card: dict[str, Any]) -> dict[str, Any]:
    """Strip internal keys (underscore-prefixed) before serialization."""
    return {k: v for k, v in card.items() if not k.startswith("_")}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def dossier_card(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Build a card dict from one dossier file. Returns (card, error)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, f"unreadable dossier {path.name}: {exc}"
    sid = str(data.get("session_id") or path.name[: -len(".dossier.json")])
    seat = data.get("seat")
    seat_source = seat.get("source") if isinstance(seat, dict) else None
    if seat_source == "mag_agent":
        return None, "agent seat session (seat.source=mag_agent)"
    embedded = data.get("session_card")
    if not isinstance(embedded, dict):
        return None, f"dossier {sid} has no embedded session_card"
    prompts = data.get("operator_prompts")
    ask_count = int(data.get("ask_count") or 0)
    is_human = bool(prompts) or ask_count > 0
    card = _clean(dict(embedded))
    card["session_id"] = sid
    card["ask_count"] = card.get("ask_count", ask_count)
    card["source"] = f"memory/biography/{path.name}#session_card"
    card["generated_by"] = GENERATED_BY
    card["generated_at"] = _now_iso()
    time_unix = 0
    try:
        time_unix = int(((data.get("time") or {}).get("updated_at") or {}).get("unix") or 0)
    except (TypeError, ValueError):
        time_unix = 0
    card["_sort_unix"] = time_unix or int(path.stat().st_mtime)
    return (card if is_human else None), (None if is_human else "no operator prompts (ask_count 0)")


def session_record_card(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Build a factual card from a memory/sessions/*.json session_record.v1 file."""
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, f"unreadable session record {path.name}: {exc}"
    sid = str(rec.get("session_id") or path.stem)
    bits: list[str] = [f"session record ({rec.get('schema') or 'unknown schema'})"]
    built = rec.get("modules_built_today")
    if isinstance(built, list) and built:
        bits.append(f"{len(built)} modules built")
    pre = rec.get("preflight")
    if isinstance(pre, dict) and pre.get("score"):
        bits.append(f"preflight {pre['score']}")
    if rec.get("boot_command"):
        bits.append(f"boot: {rec['boot_command']}")
    line = "; ".join(bits)
    card: dict[str, Any] = {
        "schema": "session_card.v1",
        "session_id": sid,
        "title": sid,
        "one_liner": line,
        "blurb": line,
        "themes": [],
        "source": f"memory/sessions/{path.name}",
        "generated_by": GENERATED_BY,
        "generated_at": _now_iso(),
    }
    ts = str(rec.get("ts") or "")
    card["_sort_unix"] = int(path.stat().st_mtime)
    if ts:
        card["record_ts"] = ts
    return card, None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Ensure one .card.json per human session.")
    ap.add_argument("--root", default=str(ROOT_DEFAULT), help="repo root (default: script parent)")
    ap.add_argument("--force", action="store_true", help="overwrite existing session cards")
    ap.add_argument("--dry-run", action="store_true", help="plan writes, touch nothing")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    cards_dir = root / "memory" / "biography" / "cards"
    if not args.dry_run:
        try:
            cards_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            print(f"CANNOT ENSURE cards dir {cards_dir}: {exc}", file=sys.stderr)
            return 2

    dossier_files = sorted((root / "memory" / "biography").glob("*.dossier.json"))
    record_files = sorted((root / "memory" / "sessions").glob("*.json"))
    if not dossier_files and not record_files:
        print(f"CANNOT VERIFY: no dossiers and no session records under {root}", file=sys.stderr)
        return 2

    written: list[str] = []
    skipped_existing: list[str] = []
    skipped_not_human: list[tuple[str, str]] = []
    errors: list[str] = []
    newest: tuple[int, str, dict[str, Any] | None] = (0, "", None)

    for path in dossier_files:
        card, err = dossier_card(path)
        if card is None:
            if err and err.startswith("unreadable"):
                errors.append(err)
            else:
                sid = path.name[: -len(".dossier.json")]
                skipped_not_human.append((sid, err or "unknown"))
            continue
        sid = str(card["session_id"])
        if card["_sort_unix"] > newest[0]:
            newest = (int(card["_sort_unix"]), sid, card)
        out = cards_dir / f"{sid}.card.json"
        if out.is_file() and not args.force:
            skipped_existing.append(sid)
            continue
        if not args.dry_run:
            out.write_text(json.dumps(_clean(_public(card)), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written.append(sid)

    for path in record_files:
        card, err = session_record_card(path)
        if card is None:
            errors.append(err or f"unreadable session record {path.name}")
            continue
        sid = str(card["session_id"])
        if card["_sort_unix"] > newest[0]:
            newest = (int(card["_sort_unix"]), sid, card)
        out = cards_dir / f"{sid}.card.json"
        if out.is_file() and not args.force:
            skipped_existing.append(sid)
            continue
        if not args.dry_run:
            out.write_text(json.dumps(_clean(_public(card)), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written.append(sid)

    latest_path = cards_dir / "latest.card.json"
    latest_action = "kept"
    latest_body = newest[2]
    if latest_body is not None:
        degenerate = True
        if latest_path.is_file():
            try:
                cur = json.loads(latest_path.read_text(encoding="utf-8"))
                degenerate = not (cur.get("title") or "").strip() or not cur.get("themes")
            except (json.JSONDecodeError, OSError):
                degenerate = True
        if degenerate or args.force:
            if not args.dry_run:
                latest_path.write_text(
                    json.dumps(_clean(_public(latest_body)), indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
            latest_action = f"refreshed from {newest[1]}"

    total_cards = len(list(cards_dir.glob("*.card.json"))) if cards_dir.is_dir() else 0
    summary = {
        "root": str(root),
        "dry_run": args.dry_run,
        "cards_on_disk_after": total_cards,
        "written": written,
        "skipped_existing": skipped_existing,
        "skipped_not_human": skipped_not_human,
        "errors": errors,
        "latest": latest_action,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
