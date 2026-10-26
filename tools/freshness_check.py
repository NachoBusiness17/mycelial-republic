#!/usr/bin/env python3
"""freshness_check.py — boot-doc stale-trap gate.

The estate's boot reads memory first; a stale boot doc is the known disease
(load-prewarm law names BOOT_4_7.md + state/CURRENT.md as the classic traps).
This meter states the bar in numbers BEFORE reading anything:

  a freshness-critical doc is STALE when its last commit is older than the
  (heartbeat-scaled) bar while the repo itself has heartbeat (a commit within
  HEARTBEAT_DAYS).

  HEARTBEAT-SCALED BAR (R4b, 2026-10-06, ouroboros R4 memory fold S9): the old
  flat STALE_DAYS=7 bar PASSED a 1.7d-stale state/CURRENT.md on the estate's
  biggest day (last commit hours old) because a fixed week says nothing about a
  repo that commits hourly. A live repo demands fresher docs than a quiet one:
  the effective bar is min(STALE_DAYS, max(STALE_FLOOR_DAYS, head_age *
  STALE_SCALE)) -- it tightens toward STALE_FLOOR_DAYS as the heartbeat
  quickens and never exceeds the one decay constant. A dead repo (no heartbeat)
  still checks nothing, as before.

  STALE_DAYS = 7, HEARTBEAT_DAYS = 2, STALE_SCALE = 4, STALE_FLOOR_DAYS = 1.

  CANON ADJUDICATION (R5, 2026-10-06, dogfood-100m; register row: the R5
  logic-lens amendment's CANON SELECTOR RESIDUAL, state/NIGHT_LOOP_20261005.md):
  machinery-regenerated pages (state/LIVE_REPORT.md, state/REDBOARD.md,
  state/START_BRIEF.md) are excluded from the mtime crown exactly as AGENTS.md
  load-order row 0a rules in prose: their mtime moves on automation cadence,
  not window authorship, so a touch can neither crown them live truth nor read
  them STALE. See MACHINERY_REGEN below.
  Exit 1 when any doc is stale - the fix is to
refresh the doc (with today's truth) or re-register it as deliberately frozen by
adding it to FROZEN_OK below with a reason and date. Frozen docs must say so in
their own header.

Usage: python tools/freshness_check.py [--self-test]

Second half of this meter (agentcheck fold row: tool timeouts and stale
values are under-evaluated failure modes): per-tool-result freshness
receipts. Every tool result carries receipt(observed_at, source_hash) and
downstream code gates claims through stale_claim() instead of trusting them.
Fail-closed by construction: a timed-out tool call mints no receipt at all,
and stale_claim(None) is stale for exactly that reason.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

ESTATE_ROOT = Path(__file__).resolve().parent.parent
if str(ESTATE_ROOT) not in sys.path:
    sys.path.insert(0, str(ESTATE_ROOT))  # mag.constants import below; tools/ is not self-contained

from mag.constants import PACK_STALE_DAYS  # noqa: E402  (the one decay bar, L3)

CRITICAL_DOCS = [
    "BOOT_4_7.md",
    "state/CURRENT.md",
    "state/START_BRIEF.md",
    "state/HANDOFF.md",
]
# Deliberately-frozen docs with the date + reason they are allowed to age.
FROZEN_OK = {
    # Header self-declares: "SUPERSEDED 2026-09-23 — no longer boots anything.
    # Kept only as lineage." The live boot path is MEMORY.md + state/CURRENT.md.
    "BOOT_4_7.md": "2026-09-25: lineage doc, superseded by its own header",
    # Session-maze contract snapshot from 2026-08-31; live state lives in
    # state/CURRENT.md (monitored above). Kept as lineage.
    "state/HANDOFF.md": "2026-09-25: session-maze snapshot 08-31, lineage; live state = state/CURRENT.md",
}

# R5 canon adjudication (2026-10-06, dogfood-100m lane d06; register row: the
# R5 logic-lens amendment's CANON SELECTOR RESIDUAL, state/NIGHT_LOOP_20261005.md).
# Machinery-regenerated pages are EXCLUDED from the mtime crown exactly as
# AGENTS.md load-order row 0a rules in prose: their mtime moves on automation
# cadence, not window authorship (the governor regenerates LIVE_REPORT.md every
# MAG_LIVE_REPORT_EVERY ticks per mag/governor_autorun.py; mag/state_brief.py
# owns START_BRIEF.md; the patrol owns REDBOARD.md), so a sibling touch can
# neither crown them live truth nor read them STALE. mtime is the channel
# sibling seats churn; the meter stops reading it for these pages.
# START_BRIEF.md stays in CRITICAL_DOCS so the meter prints its exclusion
# instead of silently dropping a listed doc; LIVE_REPORT.md and REDBOARD.md
# are named here so a future CRITICAL_DOCS addition is covered by the same
# clause without a new incident.
MACHINERY_REGEN = (
    "state/LIVE_REPORT.md",
    "state/REDBOARD.md",
    "state/START_BRIEF.md",
)

# STALE_DAYS is the estate's ONE decay constant (mag/constants.py), imported
# here rather than redefined (L3 unification, ball-20260929): boot docs and
# compiled law age on the same bar, so no surface can call the family fresh
# while another calls it stale (w4-27 L3 found three uncoordinated TTLs:
# this file's 7, the quantizer probe's 24h, the render seam's 7d). The 7
# value itself is unchanged - only its definition site moved.
STALE_DAYS = PACK_STALE_DAYS
# HEARTBEAT_DAYS is a liveness window, not a decay bar: it stays a local
# constant because it has exactly one site (this meter).
HEARTBEAT_DAYS = 2
# R4b heartbeat scaling (2026-10-06, ouroboros R4 fold S9): a doc may lag the
# repo's own heartbeat by at most STALE_SCALE x, but the bar never tightens past
# STALE_FLOOR_DAYS (docs are not churned sub-daily by law) and never widens past
# the one decay constant STALE_DAYS. Fast heartbeat tonight (hours): bar 1.0d ->
# the 1.7d-stale CURRENT.md the flat bar waved through now reads STALE.
STALE_SCALE = 4.0
STALE_FLOOR_DAYS = 1.0


def effective_stale_days(head_age_days: float | None) -> float:
    """The staleness bar a doc is judged against, scaled by the repo's heartbeat.

    head_age_days: age of HEAD's last commit (the heartbeat itself); None when
    unknown, which falls back to the un-scaled decay constant (fail-open only on
    the measurement being impossible, never on the doc being old)."""
    if head_age_days is None:
        return float(STALE_DAYS)
    return float(min(STALE_DAYS, max(STALE_FLOOR_DAYS, head_age_days * STALE_SCALE)))


def _git(args: list[str]) -> str:
    out = subprocess.run(["git"] + args, cwd=ESTATE_ROOT, capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        print(f"FRESHNESS: git {' '.join(args[:2])} failed — refusing to guess (exit 2)")
        sys.exit(2)
    return out.stdout.strip()


def last_commit_age_days(path: str | None = None) -> float | None:
    args = ["log", "-1", "--format=%cI"]
    if path:
        args += ["--", path]
    iso = _git(args)
    if not iso:
        return None  # never committed
    then = datetime.fromisoformat(iso)
    return (datetime.now(timezone.utc) - then).total_seconds() / 86400.0


# ---------------------------------------------------------------------------
# Per-tool-result freshness receipts.
#
# The fold row this extends: tool timeouts and stale values are under-
# evaluated failure modes. A tool result is not a fact, it is an observation
# made at a moment against bytes that can move. receipt() stamps the moment
# and the bytes; stale_claim() gates any later claim against both.
# ---------------------------------------------------------------------------

DEFAULT_MAX_AGE_SECONDS = 900.0  # 15 min: default bar before a tool result counts as stale
CLOCK_SKEW_SECONDS = 300.0       # receipts dated further in the future than this are corrupt


class ClaimVerdict(NamedTuple):
    stale: bool
    reason: str

    def __bool__(self) -> bool:  # gate-friendly: `if stale_claim(rec): block`
        return self.stale


def hash_text(text: str) -> str:
    """sha256 hex of a tool result's exact text (the receipt's source_hash)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_file(path: str | Path) -> str:
    """sha256 hex of a file's exact bytes, streamed (safe for large files)."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def receipt(observed_at: str | datetime, source_hash: str, *, tool: str | None = None,
            max_age_seconds: float | None = None) -> dict:
    """Mint the freshness receipt for ONE tool result.

    observed_at: when the tool actually observed the world (datetime, or
        ISO-8601 string; a naive datetime is treated as UTC).
    source_hash: sha256 hex of the exact content the result describes:
        hash_text(result_text) for in-memory results, hash_file(path) for
        file-backed ones. stale_claim() re-verifies this against the world.
    tool: optional tool name for triage in the fleet memory (watch/inbox).
    max_age_seconds: optional per-result bar; defaults to
        DEFAULT_MAX_AGE_SECONDS and is carried in the receipt so the gate
        stays self-contained across a JSON round trip.
    """
    then = _parse_iso(observed_at if isinstance(observed_at, str) else observed_at.isoformat())
    if then is None:
        raise ValueError(f"receipt observed_at unparseable: {observed_at!r}")
    return {
        "observed_at": then.astimezone(timezone.utc).isoformat(),
        "source_hash": str(source_hash),
        "max_age_seconds": float(DEFAULT_MAX_AGE_SECONDS if max_age_seconds is None else max_age_seconds),
        **({"tool": tool} if tool else {}),
    }


def receipt_to_json(rec: dict) -> str:
    """Serialize a receipt for filing (watch/inbox JSONL are the fleet memory)."""
    return json.dumps(rec, sort_keys=True)


def receipt_from_json(raw: str) -> dict:
    """Rehydrate a receipt; raises on garbage rather than inventing one."""
    rec = json.loads(raw)
    if not isinstance(rec, dict):
        raise ValueError("receipt json is not an object")
    return rec


def _parse_iso(value: object) -> datetime | None:
    """Parse ISO-8601 to aware UTC; None when unparseable (callers fail closed)."""
    try:
        parsed = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def stale_claim(rec: dict | None, *, now: datetime | None = None, source_path: str | Path | None = None,
                max_age_seconds: float | None = None) -> ClaimVerdict:
    """Gate helper: is a claim backed by this receipt stale?

    Stale (fail-closed) when the receipt is missing, malformed, older than
    the bar, dated implausibly in the future (corrupt clock), or when
    source_path is given and its current hash no longer matches the observed
    source_hash (the world moved on after the observation). An explicit
    max_age_seconds here overrides the bar carried in the receipt.
    """
    if not isinstance(rec, dict):
        return ClaimVerdict(True, "no receipt: tool result carried none (timeout or exception path?)")
    if not rec.get("source_hash"):
        return ClaimVerdict(True, "receipt missing source_hash")
    then = _parse_iso(rec.get("observed_at", ""))
    if then is None:
        return ClaimVerdict(True, f"receipt observed_at unparseable: {rec.get('observed_at')!r}")
    moment = now or datetime.now(timezone.utc)
    age = (moment - then).total_seconds()
    if age < -CLOCK_SKEW_SECONDS:
        return ClaimVerdict(True, f"receipt observed_at {-age / 3600.0:.1f}h in the future (corrupt clock)")
    bar = float(max_age_seconds) if max_age_seconds is not None else float(
        rec.get("max_age_seconds", DEFAULT_MAX_AGE_SECONDS))
    if age > bar:
        return ClaimVerdict(True, f"receipt age {age:.0f}s exceeds bar {bar:.0f}s")
    if source_path is not None:
        try:
            current = hash_file(source_path)
        except OSError as exc:
            return ClaimVerdict(True, f"source unreadable for re-hash: {exc}")
        if current != rec["source_hash"]:
            return ClaimVerdict(True, f"source drifted since observation ({rec['source_hash'][:12]} -> {current[:12]})")
        return ClaimVerdict(False, f"fresh: age {age:.0f}s of {bar:.0f}s bar, source hash verified")
    return ClaimVerdict(False, f"fresh: age {age:.0f}s of {bar:.0f}s bar")


def self_test() -> int:
    """Self-test for the receipt layer. No network, no repo writes. 0=pass, 1=fail."""
    import tempfile

    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if condition:
            print(f"  ok: {name}")
        else:
            failures.append(name)
            print(f"  FAIL: {name}" + (f" [{detail}]" if detail else ""))

    text = "sensor reads 42"
    rec = receipt(datetime.now(timezone.utc), hash_text(text), tool="self_test")
    check("receipt carries observed_at + source_hash", bool(rec.get("observed_at")) and bool(rec.get("source_hash")))
    check("hash_text is sha256 of utf-8 bytes",
          rec["source_hash"] == hashlib.sha256(text.encode("utf-8")).hexdigest())
    check("fresh receipt passes gate", not stale_claim(rec).stale)
    check("gate truthiness: fresh is falsy", not bool(stale_claim(rec)))

    old = receipt(datetime.now(timezone.utc) - timedelta(hours=2), hash_text(text))
    verdict = stale_claim(old)
    check("2h-old receipt stale under default bar", verdict.stale and "exceeds bar" in verdict.reason, verdict.reason)
    check("gate override widens bar to 3h", not stale_claim(old, max_age_seconds=3 * 3600).stale)
    carried = receipt(datetime.now(timezone.utc) - timedelta(hours=2), hash_text(text), max_age_seconds=3 * 3600)
    check("receipt-carried bar respected", not stale_claim(carried).stale)

    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "source.txt"
        source.write_text("v1", encoding="utf-8")
        file_rec = receipt(datetime.now(timezone.utc), hash_file(source))
        check("fresh file receipt passes with re-hash", not stale_claim(file_rec, source_path=source).stale)
        source.write_text("v2 changed", encoding="utf-8")
        verdict = stale_claim(file_rec, source_path=source)
        check("drifted source fails gate", verdict.stale and "drifted" in verdict.reason, verdict.reason)

    check("None receipt fails closed (timeout path)", stale_claim(None).stale)
    check("non-dict receipt fails closed", stale_claim("nope").stale)
    check("missing source_hash fails closed",
          stale_claim({"observed_at": datetime.now(timezone.utc).isoformat()}).stale)
    check("unparseable observed_at fails closed",
          stale_claim({"source_hash": "ab", "observed_at": "not-a-time"}).stale)
    check("future-dated receipt fails closed",
          stale_claim(receipt(datetime.now(timezone.utc) + timedelta(hours=2), hash_text(text))).stale)
    naive = datetime(2026, 9, 25, 12, 0, 0)
    check("naive observed_at treated as UTC",
          receipt(naive, "ab")["observed_at"] == receipt(naive.replace(tzinfo=timezone.utc), "ab")["observed_at"])

    round_trip = receipt_from_json(receipt_to_json(rec))
    check("json round trip preserves hash and verdict",
          round_trip["source_hash"] == rec["source_hash"]
          and stale_claim(round_trip).stale == stale_claim(rec).stale)
    try:
        receipt_from_json("[1, 2]")
        check("receipt_from_json rejects non-object", False)
    except ValueError:
        check("receipt_from_json rejects non-object", True)
    try:
        receipt("garbage", "ab")
        check("receipt() rejects unparseable observed_at", False)
    except ValueError:
        check("receipt() rejects unparseable observed_at", True)

    if failures:
        print(f"RECEIPT SELF-TEST: FAIL - {len(failures)} failure(s): {', '.join(failures)}")
        return 1
    print("RECEIPT SELF-TEST: PASS")
    return 0


def main() -> int:
    head_age = last_commit_age_days()
    if head_age is None:
        print("FRESHNESS: HEAD has no commits — nothing to measure")
        return 2
    heartbeat = head_age <= HEARTBEAT_DAYS
    bar = effective_stale_days(head_age)  # R4b: heartbeat-scaled, see module docstring
    print(
        f"FRESHNESS: repo heartbeat {head_age:.1f}d since last commit "
        f"(alive={'yes' if heartbeat else 'no'}; bar: stale={bar:.1f}d heartbeat-scaled "
        f"[floor {STALE_FLOOR_DAYS:.0f}d, scale x{STALE_SCALE:.0f}, cap {STALE_DAYS}d], "
        f"heartbeat={HEARTBEAT_DAYS}d)"
    )
    stale: list[str] = []
    for doc in CRITICAL_DOCS:
        if doc in MACHINERY_REGEN:
            # R5 canon adjudication (2026-10-06): excluded from the mtime crown
            # per AGENTS.md load-order row 0a; see MACHINERY_REGEN above. The
            # page prints its adjudication instead of an age so a reader sees
            # the crown was decided, not forgotten.
            print(f"  {doc}: [machinery-regen] excluded from the mtime crown (AGENTS.md row 0a)")
            continue
        age = last_commit_age_days(doc)
        frozen = doc in FROZEN_OK
        if age is None:
            disk = ESTATE_ROOT / doc
            if disk.exists():
                mtime = datetime.fromtimestamp(disk.stat().st_mtime, tz=timezone.utc)
                age = (datetime.now(timezone.utc) - mtime).total_seconds() / 86400.0
                is_stale = heartbeat and age > bar and not frozen
                state = f"{age:.1f}d old [untracked-mtime]" + ("  [frozen-ok]" if frozen else ("  STALE" if is_stale else "  ok"))
            else:
                is_stale = True
                state = "MISSING (not committed, not on disk)"
        else:
            is_stale = heartbeat and age > bar and not frozen
            state = f"{age:.1f}d old" + ("  [frozen-ok]" if frozen else ("  STALE" if is_stale else "  ok"))
        if is_stale:
            stale.append(doc)
        print(f"  {doc}: {state}")
    if stale:
        print(f"FRESHNESS: FAIL — {len(stale)} stale/missing boot doc(s): {', '.join(stale)}")
        print("  Fix: refresh the doc with today's truth, or register it in FROZEN_OK with reason+date.")
        return 1
    print("FRESHNESS: PASS — boot docs inside the bar.")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
