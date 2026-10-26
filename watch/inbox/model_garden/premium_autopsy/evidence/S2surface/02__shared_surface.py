"""Validate and expose the cross-client Mag shared surface.

This module is deliberately read-only in its inspect/status/validate verbs: it
does not move files or grant effects; it gives host, container, WSL, editor,
and CLI workers one deterministic way to find the durable inbox and detect
drift in its discovery pointers. The one exception is the rebuild verb
(WO-10, 2026-09-29), the standing INDEX fold repair: it heals the surface
strictly through the fold's own writer verbs (see mag/surface_rebuild.py,
its implementation module per the file-too-long law).

CLI::
    python -m mag.shared_surface path
    python -m mag.shared_surface status
    python -m mag.shared_surface validate
    python -m mag.shared_surface rebuild [--dry]

Living-file law (B2-156, 2026-09-26; spec watch/inbox/LIVING_HASH_LAW_20260926.md):
a SEALED living item (living:true + size:N) seals only its first N bytes.
validate hashes that sealed prefix: append-only growth past the seal is counted
(living_files.ok) and never an error, while mutation or truncation of the sealed
prefix is a hard error. An OPEN living item (living:true + seal:"open") is an
edit-shaped board with no byte seal: counted in living_files.open, never an
error. A living item with neither is a WARNING and counts in
living_files.unverified (steady state is empty; it is migration residue).

Events-log hygiene (B2-42, 2026-09-26): validate also scans
watch/inbox/index_events.jsonl, the append-only log that INDEX.json is folded
from (scripts/index_fold_host.mjs). The fold's reader is tolerant: it warns and
skips lines that fail JSON.parse, so a writer that starts appending garbage
would otherwise never fail a gate. Spec here:

- A line is malformed when it is non-blank (after stripping trailing CRLF) and
  fails strict json.loads with NaN/Infinity rejected, matching the fold's
  JSON.parse semantics.
- Lines whose content sha256 is registered in
  configs/events_malformed_baseline.json are grandfathered debt: the no-erase
  law keeps them in the log verbatim, so they stay warnings-free and folded
  over. Registration is keyed on content bytes, not line numbers, because the
  log is append-only and legacy lines keep their positions anyway.
- Any malformed line NOT in the registry is an ERROR: a NEW malformed line
  fails validate (exit 1). Fix the writer and register debt by name if a new
  one must land.
- A missing or unreadable baseline is an ERROR (the debt registry must exist);
  a missing events log is a WARNING (container surfaces may not mount the
  repo); a registered line that no longer exists in the log is a WARNING so
  fixed or pruned debt can be reclaimed from the registry.

Events key schema (B2-342, 2026-09-26): the B2-329 dump purity law made the
writer-key vocabulary load-bearing (a strict downstream consumer of the
`events` dump rejects any key outside it), but no spec owned the vocabulary.
The spec is now configs/events_key_schema.json: every key any writer ever
appended, each with first-seen line, seq (decimal string per the B2-40
scheme), ts and owning writer, censused at a recorded log sha256. The
gate implementation lives in mag/events_key_schema.py (re-exported here,
where inspect_surface wires it). The
registry is a CLOSED VOCABULARY, not a required-fields spec: any registered
key may be omitted on any line. The gate:

- An event key NOT in the registry is an ERROR, one per distinct key, naming
  the key, occurrence count, first line, seq and owning writer: register it
  by name (with first-seen evidence and a carries note) or fix the writer.
  The fold's warning channel names the same keys (WARN + exit 2).
- The underscore prefix is reserved for fold-internal fields (B2-329 dump
  purity); underscore keys are exempt from the scan and must never be
  written to the log.
- A missing or unreadable registry is an ERROR (the spec must exist).
- Census counts and first-seen lines are point-in-time facts at the recorded
  sha256; appends never invalidate an entry, only NEW keys do.

Env-redirect tripwire (B2-358, 2026-09-26): validate also warns when
MAG_SEAT_CRASH_LOG or MAG_GAPS_LOG is set outside a test run. These are the
test isolation seams (mag.agent_cli._log_seat_crash,
mag.temperature_stack._gaps_log) whose writers report ok either way, so a
shell export leaked past its test run silently redirects the production crash
or gap log. The warning names the variable and the redirect target and never
fails validate (a warning, not an error); the operator response is in
mag/env_redirect.py and receipt
watch/inbox/burn_wave_20260926/B2_358_env_tripwire_20260926.md.

LINKS event split (B2-168): LINKS.jsonl link-rows-only past its B2-28
marker; gate spec + debt registry live in mag/links_split_gate.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from mag.env_redirect import env_redirect_warnings
# B2-342 events key schema gate: implementation lives in its own module (the
# ratchet's file-too-long law); names are re-exported here because
# mag.shared_surface.validate is the wiring surface and tests address them
# through this module.
from mag.events_key_schema import (  # noqa: F401  (re-export)
    EVENTS_KEY_SCHEMA,
    load_event_key_registry,
    reject_json_constant as _reject_constant,
    scan_event_keys,
)
from mag.links_split_gate import (  # noqa: F401  (B2-168 re-export; spec in mag/links_split_gate.py)
    LINKS_KIND_BASELINE,
    LINKS_LEDGER,
    links_split_check,
    scan_links_kind_rows,
)
from mag.links_sha_ratchet import (  # noqa: F401  (B2-173 re-export; spec in mag/links_sha_ratchet.py)
    LINKS_SHA_BASELINE,
    links_sha_ratchet_check,
    scan_same_sha_unflagged,
)
# WO-10 (2026-09-29) rebuild verb: implementation lives in mag/surface_rebuild.py
# (the file-too-long law module-split pattern); re-exported here because
# mag.shared_surface is the wiring surface and the CLI below dispatches it.
from mag.surface_rebuild import rebuild_surface  # noqa: F401


ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / "watch"
INBOX = WATCH / "inbox"
INDEX = INBOX / "INDEX.json"
CONTRACT = INBOX / "SHARED_SURFACE_CONTRACT.json"
WARM_PACK = WATCH / "WARM_PACK.json"
EVENTS_LOG = INBOX / "index_events.jsonl"
MALFORMED_BASELINE = ROOT / "configs" / "events_malformed_baseline.json"
CONTROL_FILES = {"INDEX.json", "INDEX.md", "SHARED_SURFACE_CONTRACT.json"}

# B2-297 (2026-09-26) living-downgrade watchlist: the three paths the
# LIVING_HASH_LAW_20260926.md names as living-by-design. A plain `add`
# re-register legally drops the living flag (last-register-wins, law
# section 5), so one stale whole-file refresh silently reverts any of
# these to a whole-file seal that hard-fails on the next append. validate
# warns (never errors) when one of them folds to an item without
# item.living, so the downgrade is named at the next validate instead of
# surfacing as an append failure later.
KNOWN_LIVING_PATHS = (
    "LINKS.jsonl",
    "burn_wave_20260926/QUEUE.md",
    "phone_relay_log.jsonl",
)

# B2-399 (2026-09-26): scan_events_log moved to mag/events_scan.py per the
# B2-248 module-split precedent (file-too-long law); the file sat at exactly
# the 400-line cap after the B2-342/B2-358 landings. Re-exported here because
# mag.shared_surface.validate is the wiring surface and tests address the
# scanner through this module (same re-export pattern as mag/events_key_schema.py).
from mag.events_scan import scan_events_log  # noqa: E402  (B2-399 re-export)


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 20963 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
register-wins); "
                f"re-register with add --living or --living-open before the "
                f"next append hard-fails"
            )

    return {
        "schema": "shared_surface.status.v1",
        "ok": not errors,
        "root": str(ROOT),
        "paths": {
            "host": str(INBOX),
            "container": "/board/inbox",
            "wsl": "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox",
            "index": "/board/inbox/INDEX.json",
            "contract": "/board/inbox/SHARED_SURFACE_CONTRACT.json"
        },
        "files": files,
        "indexed_items": indexed_items,
        "unindexed_items": unindexed,
        "events_log_malformed": {
            "total": len(malformed),
            "grandfathered": len(malformed) - sum(
                1 for r in malformed if r["sha256"] not in grandfathered),
            "new": sum(1 for r in malformed if r["sha256"] not in grandfathered),
        },
        "events_log_keys": {
            "lines_scanned": key_scan["lines"],
            "unknown_keys": len(key_scan["unknown"]),
        },
        "living_files": {
            "ok": living_ok,
            "open": living_open,
            "unverified": living_unverified,
            "downgraded": living_downgraded,
        },
        "errors": errors,
        "warnings": warnings
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m mag.shared_surface")
    parser.add_argument(
        "command",
        choices=("path", "status", "validate", "rebuild"),
        nargs="?",
        default="status",
    )
    parser.add_argument("--dry", action="store_true", help="rebuild: census only, no heals")
    args = parser.parse_args()
    if args.command == "path":
        print(json.dumps({
            "schema": "shared_surface.path.v1",
            "host": str(INBOX),
            "container": "/board/inbox",
            "wsl": "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox",
            "read_first": "/board/inbox/INDEX.json"
        }, indent=2))
        return 0
    if args.command == "rebuild":
        # WO-10 standing repair: fold rebuild + register heals via the fold's
        # own verbs; exit 1 only when the post-run census still has deltas.
        result = rebuild_surface(dry_run=bool(args.dry))
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok") else 1
    result = inspect_surface()
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] or args.command == "status" else 1


if __name__ == "__main__":
    raise SystemExit(main())
