"""Dead-hand watchdog — the succession contract's trigger, as code.

Contract: watch/inbox/SUCCESSION_CONTRACT_20260912.md (Articles 3-5).

DESIGN LAW (Article 2 of the contract): this tool can NEVER exercise a
reserved authority. It has no spend, key, credential, publication, or
beacon capability — it only reads operator-voice surfaces, writes state
files, seals evidence, and makes noise. Watchdog, not coronation.

DEFAULT STATE: DISARMED. Arming requires an explicit operator act
(`--arm --i-am-operator --interval-h 72`). Per Article 5 the contract is
DORMANT until the operator signs AND the 24h dead-hand drill passes once;
the drill drives THIS tool (arm -> go silent -> fire -> return -> revert).

Voice surfaces (audited against real row shapes 2026-09-12):
  - watch/steers.jsonl rows whose authority starts with "operator"
    (and is not a FORGED row) — real field, verified
  - state/operator_pulse.json {"ts", "via"} — THE capture point for the
    operator's actual channels (X, seat pastes, Telegram/steering helm):
    any seat that receives operator input stamps it. Seats: stamp on
    every operator message. Without this file the watchdog sees only
    steers, which under-counts his voice (fail-safe: holds fire).
Dropped as surfaces (audit finding): hermes_dispatch rows carry no
author field; m12_baseline rows are daily aggregates, not live words.

Witnesses (2-of-3 distinct within the last 6h, Article 3):
  - a fleet seat attests via state/dead_hand_witnesses.json rows
  - a named human attests the same way (witness_id = their name)

Trigger actions (Article 4, all reversible): SEAL (state snapshot +
manifest of key surfaces), HOLD (state/hold_queue/ opened; reserved
routing marked HOLD), LOUD (card + ack-queue row — a succession trigger
must never be silent). REVERT on the operator's word presents the HOLD
queue oldest-first and restores WATCHING.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
HOLD_DIR = STATE / "hold_queue"
STATE_PATH = STATE / "dead_hand_state.json"
WITNESSES_PATH = STATE / "dead_hand_witnesses.json"

VOICE_SURFACES = [
    ("steers", ROOT / "watch" / "steers.jsonl", "steers_operator_authority"),
    ("operator_pulse", None, None),  # resolved lazily: STATE / operator_pulse.json
]
WITNESS_WINDOW_H = 6
WITNESSES_REQUIRED = 2
WATCH_EVERY_H = 1  # liveness: state file must be ticked at least this often


def _voice_surfaces():
    """Resolve surfaces lazily so tests/sandboxes can redirect STATE."""
    resolved = []
    for name, path, marker in VOICE_SURFACES:
        if path is None:
            path = STATE / f"{name}.json"
        resolved.append((name, path, marker))
    return resolved


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ts(doc: dict) -> datetime | None:
    raw = doc.get("ts") or doc.get("timestamp") or doc.get("time")
    if not isinstance(raw, str) or not raw:
        return None
    try:
        ts = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)


def _candidate_docs(text: str) -> list[dict]:
    """Parse a voice surface: JSONL rows newest-last, or one pretty JSON doc."""
    docs: list[dict] = []
    for line in text.splitlines()[::-1]:
        line = line.strip()
        if not line:
            continue
        try:
            doc = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(doc, dict):
            docs.append(doc)
    if not docs:  # whole-file fallback (single pretty-printed doc)
        try:
            doc = json.loads(text)
            if isinstance(doc, dict):
                docs.append(doc)
        except json.JSONDecodeError:
            pass
    return docs


def _is_operator_row(doc: dict, marker: str | None) -> bool:
    if marker is None:
        return True
    if marker == "steers_operator_authority":
        authority = str(doc.get("authority") or "")
        return (authority.lower().startswith("operator")
                and not authority.upper().startswith("FORGED"))
    who = str(doc.get("initiated_by") or doc.get("source")
              or doc.get("claimed_by") or doc.get("author") or "")
    return who.lower() == str(marker).lower()


def last_operator_word() -> tuple[datetime | None, str]:
    """Newest timestamp + surface across all operator-voice surfaces."""
    best: tuple[datetime | None, str] = (None, "none")
    for name, path, marker in _voice_surfaces():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for doc in _candidate_docs(text):
            if not _is_operator_row(doc, marker):
                continue
            ts = _ts(doc)
            if ts and (best[0] is None or ts > best[0]):
                best = (ts, name)
            break  # newest candidate per surface carries its latest word
    return best


def _load_state() -> dict:
    default = {
        "armed": False,
        "armed_by": None,
        "armed_ts": None,
        "interval_hours": None,
        "status": "DISARMED",  # DISARMED | WATCHING | TRIGGERED | REVERTED
        "last_tick": None,
        "triggered_ts": None,
        "drill_passed": False,
    }
    try:
        doc = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return {**default, **doc} if isinstance(doc, dict) else default
    except (OSError, json.JSONDecodeError):
        return default


def _save_state(st: dict) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def _witness_count(now: datetime) -> tuple[int, list[str]]:
    try:
        rows = json.loads(WITNESSES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0, []
    fresh: dict[str, str] = {}
    cutoff = now - timedelta(hours=WITNESS_WINDOW_H)
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict) or not row.get("silence_confirmed"):
            continue
        ts = _ts(row)
        wid = str(row.get("witness_id") or "")[:40]
        if ts and ts >= cutoff and wid:
            if wid not in fresh or ts > _ts({"ts": fresh[wid]}):
                fresh[wid] = row.get("ts")
    return len(fresh), sorted(fresh)


def _loud(title: str, body: str) -> Path:
    """A succession event must never be silent — write the card + ack row."""
    card = ROOT / "watch" / "inbox" / f"DEAD_HAND_{_now().strftime('%Y%m%dT%H%MZ')}.md"
    card.write_text(
        f"# {title}\n\n{body}\n\n— dead_hand.py (auto), {_now().isoformat()}\n",
        encoding="utf-8",
    )
    alert = ROOT / "watch" / "inbox" / "ACK_REAPER_QUEUE.md"
    try:
        with alert.open("a", encoding="utf-8") as fh:
            fh.write(f"- {_now().isoformat()} dead_hand {title}: {body[:200]}\n")
    except OSError:
        pass
    return card


def _seal() -> dict:
    """SEAL: snapshot the succession-relevant state, hash-bound."""
    surfaces = {}
    for _, p, _ in _voice_surfaces():
        if p.is_file():
            try:
                name = str(p.relative_to(ROOT))
            except ValueError:  # sandbox path outside ROOT (tests/drill rigs)
                name = f"sandbox/{p.name}"
            surfaces[name] = hashlib.sha256(p.read_bytes()).hexdigest()
    STATE.mkdir(parents=True, exist_ok=True)
    seal_path = STATE / f"dead_hand_seal_{_now().strftime('%Y%m%dT%H%MZ')}.json"
    seal = {"ts": _now().isoformat(), "surfaces": surfaces,
            "contract": "watch/inbox/SUCCESSION_CONTRACT_20260912.md"}
    seal_path.write_text(json.dumps(seal, indent=2), encoding="utf-8")
    # Fix 2026-09-29 (gala ball3 live-state): the two display paths below raise
    # ValueError for sandbox paths outside ROOT (the same class the surface
    # names above already guard (tests/drill rigs; the wave5 full-suite run
    # with an external --basetemp failed test_trigger_fires_seal_hold_loud on
    # exactly this line,
    # watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt).
    # Display only: seal bytes and trigger semantics unchanged.
    try:
        seal_shown = str(seal_path.relative_to(ROOT))
    except ValueError:  # sandbox path outside ROOT (tests/drill rigs)
        seal_shown = f"sandbox/{seal_path.name}"
    return {"seal": seal_shown, "surfaces_hashed": len(surfaces)}


def _open_hold(st: dict) -> str:
    HOLD_DIR.mkdir(parents=True, exist_ok=True)
    readme = HOLD_DIR / "README.md"
    if not readme.is_file():
        readme.write_text(
            "# HOLD QUEUE\n\nReserved-authority decisions accumulate here "
            "(oldest first) while succession is active. They are NEVER "
            "executed by the watchdog. On the operator's word everything "
            "reverts and this queue is presented to him.\n",
            encoding="utf-8",
        )
    # Same sandbox guard as _seal (gala ball3 live-state 2026-09-29): hold-queue
    # paths live in the sandbox under tests/drill rigs, not under ROOT.
    try:
        return str(HOLD_DIR.relative_to(ROOT))
    except ValueError:  # sandbox path outside ROOT (tests/drill rigs)
        return f"sandbox/{HOLD_DIR.name}"


def watch(dry_run: bool = False) -> dict:
    """One tick. The cron/seat loop calls this; a missing tick is itself the alarm."""
    now = _now()
    st = _load_state()
    st["last_tick"] = now.isoformat()
    result: dict = {"tick_ts": st["last_tick"], "status": st["status"]}

    if not st["armed"] or st["status"] in ("TRIGGERED", "REVERTED"):
        _save_state(st)
        result["action"] = "none (not armed or already triggered/reverted)"
        return result

    st["status"] = "WATCHING"
    word_ts, surface = last_operator_word()
    result["last_operator_word"] = {"ts": word_ts.isoformat() if word_ts else None,
                                    "surface": surface}
    n_wit, wit_ids = _witness_count(now)
    result["witnesses"] = {"count": n_wit, "ids": wit_ids}

    if word_ts is None:
        _save_state(st)
        result["action"] = "none (no operator-voice surface readable; fail-safe)"
        return result

    silence = now - word_ts
    result["silence_hours"] = round(silence.total_seconds() / 3600, 2)
    interval = timedelta(hours=float(st["interval_hours"] or 72))
    if silence < interval or n_wit < WITNESSES_REQUIRED:
        result["action"] = ("hold (silence below interval)" if silence < interval
                            else "hold (witnesses below 2-of-3)")
        _save_state(st)
        return result

    # TRIGGER — Article 4: seal, hold, continue, and be LOUD about it.
    st["status"] = "TRIGGERED"
    st["triggered_ts"] = now.isoformat()
    if not dry_run:
        seal = _seal()
        hold = _open_hold(st)
        card = _loud(
            "SUCCESSION TRIGGER FIRED",
            f"Operator silent {result['silence_hours']}h (interval "
            f"{st['interval_hours']}h), {n_wit} witnesses confirmed. State "
            f"sealed to {seal['seal']}; HOLD queue open at {hold}. "
            "Reserved authorities (spend/keys/personhood/voice/beacon) were "
            "NOT and will NOT be exercised. Everything else continues on the "
            "standing laws. One word from the Operator reverts all of this.",
        )
        result["action"] = {"seal": seal, "hold": hold, "card": str(card.name)}
    else:
        result["action"] = "DRY-RUN would trigger (seal+hold+loud)"
    _save_state(st)
    return result


def revert(note: str = "") -> dict:
    """The operator's word. Everything reverts; HOLD queue presented oldest first."""
    st = _load_state()
    st["status"] = "REVERTED"
    st["reverted_ts"] = _now().isoformat()
    holds = []
    if HOLD_DIR.is_dir():
        holds = sorted(p.name for p in HOLD_DIR.glob("*") if p.name != "README.md")
    _save_state(st)
    _loud("SUCCESSION REVERTED",
          f"Operator word received{': ' + note if note else ''}. HOLD queue "
          f"({len(holds)} items, oldest first): {holds}. Status REVERTED — "
          "clock reset; re-arm is the operator's call.")
    st["armed"] = False
    st["status"] = "WATCHING" if False else "DISARMED"  # revert disarms; re-arm is explicit
    _save_state(st)
    return {"status": "REVERTED", "hold_items_oldest_first": holds}


def main() -> int:
    ap = argparse.ArgumentParser(description="Dead-hand watchdog (succession trigger)")
    ap.add_argument("--watch", action="store_true", help="one watchdog tick")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--arm", action="store_true",
                    help="ARM (operator act; requires --i-am-operator --interval-h)")
    ap.add_argument("--i-am-operator", action="store_true")
    ap.add_argument("--interval-h", type=float, choices=[48, 72, 168],
                    help="trigger interval per contract Article 3")
    ap.add_argument("--witness", help="attest silence as this witness id")
    ap.add_argument("--revert", action="store_true", help="operator word: revert")
    ap.add_argument("--note", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.arm:
        if not args.i_am_operator or not args.interval_h:
            print("REFUSED: arming requires --i-am-operator and --interval-h (48/72/168).")
            return 2
        st = _load_state()
        st.update(armed=True, armed_by="operator-explicit", armed_ts=_now().isoformat(),
                  interval_hours=args.interval_h, status="WATCHING")
        _save_state(st)
        print(json.dumps({"armed": True, "interval_hours": args.interval_h,
                          "note": "dormant until contract signed + drill passed (Article 5)"},
                         indent=2))
        return 0
    if args.witness:
        rows = []
        try:
            rows = json.loads(WITNESSES_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            rows = []
        rows.append({"witness_id": args.witness[:40], "ts": _now().isoformat(),
                     "silence_confirmed": True})
        WITNESSES_PATH.parent.mkdir(parents=True, exist_ok=True)
        WITNESSES_PATH.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(json.dumps({"witness": args.witness[:40], "attested": True}))
        return 0
    if args.revert:
        print(json.dumps(revert(args.note), indent=2))
        return 0
    if args.status:
        print(json.dumps(_load_state(), indent=2))
        return 0
    if args.watch:
        print(json.dumps(watch(dry_run=args.dry_run), indent=2))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
