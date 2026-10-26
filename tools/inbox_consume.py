"""Consume verb for the shared-inbox event log (Mickey17 wave 3, 2026-09-29).

The edge-miner census (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md return 5)
found the event log 96 percent write-only: register/autoseal/amend/invalidate
all assert bytes onto the surface, but NO op ever recorded that anyone read a
receipt back. This tool is that read op. It appends exactly one line to
watch/inbox/index_events.jsonl:

    {"ts": "...", "op": "consume", "file": "<inbox-relative posix path>",
     "consumer": "<who read it>", "note": "<why>"}

Contract notes, verified against scripts/index_fold_host.mjs and the log
bytes (do not take these on faith, the fold is the law):
- The fold lifts only register/invalidate into INDEX items; every other op is
  a log-only marker (the `note` op precedent), so a consume line never
  mutates INDEX.json and never needs a refold.
- `consumer` is a NEW top-level event key. The B2-342 closed-vocabulary law
  (configs/events_key_schema.json) names unknown keys in the fold warning
  channel and in mag.shared_surface validate, so the key is registered there
  by name with this tool's first append as first-seen evidence. `note`,
  `file`, `op` and `ts` were already registered.
- The target file must exist under the inbox: consuming a ghost would mint a
  path the disk-walk join (tools/orphan_census.py) then has to reconcile
  against disk, which is exactly the dangling class that census exists to
  count, not to create.
- No seq and no writer/nonce are appended: the md_record_seal.py hook
  precedent writes ts-keyed lines and the fold's B2-279 total order places
  them below every exact-seq event, which is correct for a read marker.

Scope: the single append below is this tool's only write. Everything else,
including INDEX.json, stays untouched (wave-3 lane fence, 2026-09-29).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "watch" / "inbox"
EVENTS = INBOX / "index_events.jsonl"


def resolve_target(file_ref: str, inbox: Path = INBOX) -> Path | None:
    """Resolve any accepted path spelling to the real file under `inbox`.

    Accepts the spellings writers actually minted into the log (census
    2026-09-29): inbox-relative, host-absolute with either slash style, and
    the /board/inbox/ container alias from SHARED_SURFACE_CONTRACT.json.
    Returns None when the reference does not name an existing file under the
    inbox (outside the surface, or a ghost).
    """
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from mag.surface_rebuild import _norm  # the fold's canonical path normalizer

    rel = _norm(file_ref, inbox)
    if not rel or rel.startswith(".."):
        return None
    candidate = (inbox / rel).resolve()
    try:
        candidate.relative_to(inbox.resolve())
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def consume(
    events_log: Path,
    inbox: Path,
    file_ref: str,
    consumer: str,
    note: str = "",
    dry_run: bool = False,
) -> dict | None:
    """Append one consume event for `file_ref`; return the event, or None on refusal.

    Refusals (return None, CLI exit 2): empty consumer name, missing event
    log, or a target that does not resolve to an existing file under the
    inbox. The refusal is loud on stderr so a scripted consumer cannot
    silently believe it logged a read.
    """
    if not consumer.strip():
        print("consume refused: consumer name is required", file=sys.stderr)
        return None
    if not events_log.is_file():
        print(f"consume refused: event log missing at {events_log}", file=sys.stderr)
        return None
    target = resolve_target(file_ref, inbox)
    if target is None:
        print(
            f"consume refused: {file_ref!r} is not an existing file under {inbox}",
            file=sys.stderr,
        )
        return None
    rel = target.resolve().relative_to(inbox.resolve()).as_posix()
    event = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
        "op": "consume",
        "file": rel,
        "consumer": consumer.strip(),
        "note": note.strip(),
    }
    if dry_run:
        return event
    with events_log.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
        fh.flush()
    return event


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Append a consume (read) event for one inbox receipt."
    )
    ap.add_argument("file", help="inbox file: relative, host-absolute, or /board/inbox/ alias")
    ap.add_argument("--consumer", required=True, help="who is reading the receipt")
    ap.add_argument("--note", default="", help="why it was read")
    ap.add_argument("--dry-run", action="store_true", help="print the event, append nothing")
    args = ap.parse_args(argv)
    event = consume(EVENTS, INBOX, args.file, args.consumer, args.note, args.dry_run)
    if event is None:
        return 2
    print(json.dumps(event, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
