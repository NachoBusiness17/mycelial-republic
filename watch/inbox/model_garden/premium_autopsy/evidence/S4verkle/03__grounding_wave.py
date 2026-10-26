"""grounding_wave — the GROUND circuit's ledger (operator algebra: GROUND primitive).

A wave post = ONE ground-truth claim with a tri-state verdict + an evidence
pointer, hash-chained to the previous post. Append-only: corrections are new
posts that cite the old hash (delete-as-append). Doctrine rides the standing
wave; the grounding wave carries only what we can point at.

LAW CITATION: files not processes; chain-side append, nothing scheduled.

wave v4 (2026-09-16, stone 1 of the EPISTEMOLOGY ENGINE — design receipt
watch/inbox/wave_20260916/receipts/A2_EPISTEMOLOGY_ENGINE.md): an
evidence-ADMISSION boundary on top of the v3 truth-gate. RECORDED is no longer
the top of the ladder:

    RECORDED -> CORROBORATED -> CONTESTED -> VOID

  G1 STRUCTURAL — canonical versioned hash + prev chain, enforced at WRITE
     time (`_admit` gate runs inside the append lock on every verb): a row
     missing its hash or prev is REFUSED AT APPEND, never at verify. The
     row-122 bypass path (a 3-key fragment with no hash, prev != tip) is
     physically closed for every v4 writer.
  G2 BINDING - path-shaped evidence gets its sha256 recorded in the row AT
     POST TIME (`src_sha256_12`, bones-style re-derivable; the key keeps its
     legacy name but T1W1 ticket 11, 2026-10-01 widened NEW bindings from the
     48-bit [:12] cut to the full digest, with the read sides accepting both
     widths for legacy rows). verify re-hashes
     the bytes: identity, not mere existence. Evidence edited after the fact
     stops corroborating (EVIDENCE-MUTATED FAIL). `*_latest` mutable refs are
     refused for SUPPORTED (v3's warning became a gate). Dead path-shaped
     evidence is refused at post (EVIDENCE_DEAD) — same law v3 applied at
     verify, applied earlier.
  G3 WARRANT — a claim may carry `warrant`: a command that exits 0/1, hashed
     into the row. Witness rows run it and record `checks.g3_exit`. Strike S8
     law stands: a Claim whose Check is "the author agrees" is a notary, not
     knowledge. Software never auto-truths: CORROBORATED means the warrant
     exited 0 under two independent hands, not "true".
  DELETE-AS-APPEND — `void` buries a row under a cross-signed kind:"void" row
     naming the target's hash (`voids`) + a reason_code from the enum.
     `contest` holds a row at CONTESTED. `witness` is a separate appended row
     by a DIFFERENT seat (two-eyes law; the author never picks their own
     second eye). A void requires a named second seat at write time and only
     COUNTS once that seat's witness row is in the chain signing the void.
     Nothing is ever edited or deleted. NO AUTO-MIGRATION: legacy rows keep
     v1-v3 semantics; row 122 stays in history; only new rows carry v4 keys.

Reader law (v3 kept, extended): verify() reports LINKAGE over the physical
tape AND the ADMISSION summary (effective ledger = rows - voided, plus
VOIDED/pending/propagation). Readers quote the admission view, never bare
PASS. `view` prints the effective ledger with the ladder status per row.

Status ladder per row (admission semantics):
  RECORDED      G1 pass (append)
  CORROBORATED  >=2 witness rows from >=2 DISTINCT LINEAGES (A3 F1: seat =
                <lineage>/<instance>, lineage = vendor/weights family or
                "human"; fine-tunes/quantizations/prompts/keys/seat renames do
                NOT create a lineage), no counted witness in the author's
                lineage, all checks pass. Unprefixed seats do not count;
                an unprefixed author cannot corroborate (A3 §4, 2026-10-01).
  CONTESTED     an effective kind:"contest" row targets it
  VOID          an effective (cross-signed) kind:"void" row targets it

Corroboration raises confidence, never grants permission; effects stay
switchboard-only.

CLI:
  python -m mag.grounding_wave post --claim "..." --verdict SUPPORTED \
      --evidence path-or-pointer [--note "..."] [--warrant "cmd"] [--dry]
  python -m mag.grounding_wave void --row <hash-prefix|#line> \
      --reason-code MALFORMED --reason "..." --witness <second-seat> [--dry]
  python -m mag.grounding_wave contest --row <hash-prefix|#line> \
      --reason "..." [--seat ...] [--dry]
  python -m mag.grounding_wave witness --row <hash-prefix> [--seat ...] [--dry]
  python -m mag.grounding_wave verify
  python -m mag.grounding_wave view
  python -m mag.grounding_wave render
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "watch" / "GROUNDING_WAVE.jsonl"
VIEW_MD = ROOT / "watch" / "GROUNDING_WAVE.md"
VIEW_STATIC = ROOT / "dashboard" / "static" / "grounding_wave.md"
GENESIS = "0" * 64
VERDICTS = ("SUPPORTED", "DISPUTED", "UNPROVEN")
LADDER = ("RECORDED", "CORROBORATED", "CONTESTED", "VOID")

# wave v2 (salon 20260906, astra catch): rows carry a `seat` (poster identity,
# hashed — attribution is provable, forks are attributable) and verify() audits
# EVIDENCE, not just linkage — a hash-valid post whose evidence path is dead
# FAILS the chain check. Hashing uses .get defaults so v1 rows stay valid.
#
# wave v3 (20260908, astra witness #5 + salon-audit catch): the FALSE-RECEIPT
# attack passed verify() with a fabricated SUPPORTED row (0/1 rejected) —
# linkage-PASS was being read as truth-PASS. Three teeth, forward-applied:
#   1. SUPPORTED requires a second witness (v3 rows); unwitnessed SUPPORTED is
#      auto-demoted to UNPROVEN with a demotion note (delete-as-append: a later
#      witnessed post upgrades it).
#   2. post() holds an append lock (concurrent writers were a named liability).
#   3. verify() reports LINKAGE-PASS (hashes+evidence) separately from the
#      admission audit (witnessed vs legacy-unwitnessed SUPPORTED rows) — no
#      reader may quote bare "PASS" again.
#
# wave v4 (20260916, A2 stone 1): see module docstring. Versioned key sets per
# row `kind`; .get defaults keep v1-v3 rows valid (no auto-migration).
_PATH_RE = re.compile(r"(?:[\w.-]+/)+[\w.-]+\.[\w]+")  # file-like paths only (ext required)
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
LOCK = LEDGER.parent / "GROUNDING_WAVE.lock"

_V1_KEYS = ("prev", "ts", "claim", "verdict", "evidence", "note")
_V2_KEYS = ("prev", "ts", "claim", "verdict", "evidence", "note", "seat")
_V3_KEYS = ("prev", "ts", "claim", "verdict", "evidence", "note", "seat", "witness")

# v4 key sets, per row kind (A2 §5.1: versioned key set gains `kind` +
# `src_sha256_12` + kind-specific keys; hash excluded, canonical JSON).
_KIND_KEYS: dict[str, tuple[str, ...]] = {
    "claim": ("prev", "ts", "kind", "claim", "verdict", "evidence", "note",
              "seat", "witness", "src_sha256_12", "warrant"),
    "void": ("prev", "ts", "kind", "voids", "reason_code", "reason", "evidence",
             "seat", "witness"),
    "contest": ("prev", "ts", "kind", "contests", "reason", "evidence", "seat"),
    "witness": ("prev", "ts", "kind", "signs", "checks", "seat"),
}
_ACT_KINDS = ("void", "contest", "witness")

# void reason_code enum (A2 §2)
VOID_REASONS = ("MALFORMED", "FORGED", "EVIDENCE_DEAD", "EVIDENCE_MUTATED",
                "WARRANT_FAILED", "DUPLICATE", "SUPERSEDED", "CONTEST_SUSTAINED")

STALE_CONTEST_DAYS = 7  # closure counter (A2 §4.3)


class GateRefusal(Exception):
    """Typed admission refusal (A2 G1-G3). Never a crash: the caller gets a
    reason code. main() turns this into exit 2."""

    def __init__(self, code: str, detail: str = ""):
        self.code, self.detail = code, detail
        super().__init__(f"GATE-{code}: {detail}")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _rows() -> list[dict[str, Any]]:
    if not LEDGER.is_file():
        return []
 
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 47041 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
p.add_argument("--note", default="")
    ap.add_argument("--seat", default="zcode")
    ap.add_argument("--witness", default="",
                    help="second witness identity (required for SUPPORTED; "
                         "for void: the second seat whose signature counts)")
    ap.add_argument("--warrant", default="",
                    help="command that exits 0/1, hashed into the row (G3)")
    ap.add_argument("--row", default="",
                    help="target row: hash prefix or #N (1-based tape line)")
    ap.add_argument("--reason-code", default="", dest="reason_code",
                    help="one of " + "|".join(VOID_REASONS))
    ap.add_argument("--reason", default="")
    ap.add_argument("--dry", action="store_true",
                    help="show the row that would be appended; write nothing")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    try:
        if args.cmd == "post":
            row = post(args.claim, args.verdict, args.evidence, args.note,
                       args.seat, args.witness, args.warrant, dry=args.dry)
            ok, msg = verify()
            print(f"POSTED #{row['hash'][:12]} ({row.get('verdict')}) — {msg}")
        elif args.cmd == "void":
            row = void(args.row, args.reason_code, args.reason, args.seat,
                       args.evidence, args.witness, dry=args.dry)
            if not args.dry:
                ok, msg = verify()
                print(f"VOID POSTED #{row['hash'][:12]} (voids {str(row.get('voids'))[:12]}) — {msg}")
        elif args.cmd == "contest":
            row = contest(args.row, args.reason, args.seat, args.evidence, dry=args.dry)
            if not args.dry:
                ok, msg = verify()
                print(f"CONTEST POSTED #{row['hash'][:12]} — {msg}")
        elif args.cmd == "witness":
            row = witness(args.row, args.seat, dry=args.dry)
            if not args.dry:
                ok, msg = verify()
                print(f"WITNESS POSTED #{row['hash'][:12]} (signs {str(row.get('signs'))[:12]}) — {msg}")
        elif args.cmd == "verify":
            ok, msg = verify()
            print(("PASS " if ok else "FAIL ") + msg)
            sys.exit(0 if ok else 1)
        elif args.cmd == "view":
            print(view())
        elif args.cmd == "render":
            render()
            print(f"rendered {VIEW_MD.name} + {VIEW_STATIC.name}")
    except GateRefusal as e:
        print(f"REFUSED {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
