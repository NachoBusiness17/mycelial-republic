"""SQLite capability ledger for gps-mcp.

Schema (the documented contract):

    CREATE TABLE capability (
        model_id          TEXT NOT NULL,
        task_shape        TEXT NOT NULL,
        pass_rate         REAL NOT NULL,        -- running mean, 0.0..1.0
        sample_size       INTEGER NOT NULL,     -- verdict count backing the mean
        cost_usd_per_call REAL,                 -- last known cost, nullable
        last_measured     TEXT NOT NULL,        -- ISO-8601 UTC of last verdict
        updated_at        TEXT NOT NULL,        -- ISO-8601 UTC of any row write
        PRIMARY KEY (model_id, task_shape)
    );

    CREATE TABLE verdict_log (
        ts               TEXT NOT NULL,
        model_id         TEXT NOT NULL,
        task_shape       TEXT NOT NULL,
        verdict          INTEGER NOT NULL,     -- 1 pass, 0 fail
        evidence_hash    TEXT NOT NULL DEFAULT '',
        evidence_resolved INTEGER NOT NULL DEFAULT 0,  -- 1 = recomputed from bytes at append
        evidence_source  TEXT NOT NULL DEFAULT '',     -- 'file:<path>' | caller-named provenance
        evidence_bytes   BLOB                            -- retained bytes (cap 64 KiB) for re-audit
    );

    -- Dedupe gate (gap-analysis a04, 2026-10-03): one evidence hash is one
    -- measurement. UNIQUE over (model_id, task_shape, evidence_hash) with a
    -- partial predicate so hash-less verdicts (evidence_hash = '') stay
    -- legal: they are distinct observations by definition and the gate
    -- never collapses them.
    CREATE UNIQUE INDEX IF NOT EXISTS ux_verdict_log_evidence_triple
        ON verdict_log (model_id, task_shape, evidence_hash)
        WHERE evidence_hash <> '';

verdict_log is an audit side table so record_verdict evidence hashes are
retained without touching the capability schema above. Routing decisions
read capability; audits read verdict_log.

Duplicate gate (a04#1/a04#2/a04#4/a04#6, MASTER_MICKEY17_V2.md section 9
GO item 2): record_verdict INSERT-that-skips on a repeated
(model_id, task_shape, evidence_hash) triple. Cause: the gwap double-bank
mints fresh ts rows and the whole-file feed re-fed them, so the arena
capability means rode 259 observations over 178 distinct measurements
(a04-arena-gwap-gps lane, evidence rows 2-3). A repeat returns the pair's
unchanged standing flagged evidence_status "duplicate-skipped"; no new
verdict_log row, no capability movement. Enforcement is two-layer: a
SELECT fast path in record_verdict, and the partial UNIQUE index above
as the backstop that makes a concurrent double insert (hourly cron plus
a manual backfill) refuse at the storage layer instead of racing past
the SELECT.

Evidence-resolution gate (Q28, 2026-10-01; citation-resolution-gate-at-
landing law, receipt watch/inbox/ractor50/accuracy.md incident 1: "each
id must resolve to fetched bytes in the same session, else the row lands
as UNVERIFIED, never LANDED" -- applied to evidence hashes): an
evidence_hash is never stored on trust. At record time, when evidence
bytes are available (evidence_path to a readable file, or evidence_bytes
inline), the sha256 is recomputed from those bytes in the same call and
compared against the claimed hash:

    bytes + claim agree (or no claim)  -> evidence_resolved = 1
    bytes + claim disagree             -> evidence_resolved = 0, the row
                                          is UNVERIFIED-class, and the
                                          retained bytes keep the
                                          disagreement auditable
    no bytes obtainable (hash only, or
    a cited path that does not read)   -> evidence_resolved = 0, the row
                                          is UNVERIFIED-class, source
                                          still names what was cited

audit_evidence() re-walks verdict_log, recomputes every hash it can
resolve (file: sources re-read; retained blobs re-hash), and reports
agreed / mismatch / unresolved counts. Legacy rows written before the
gate have no source and no bytes: they count unresolved, which is the
honest reading of a self-attested hash.

Positive arm (LM7, 2026-09-30; operator positive-steering law, receipt
watch/inbox/last_mile_20260930/LM7_POSITIVE_GPS.md): the meter does not
only fail cold. Momentum is derived from the verdict_log window (last
MOMENTUM_WINDOW verdicts, oldest half vs newest half) per
(model_id, task_shape):

    badge          RISING (delta > MOMENTUM_RISING_DELTA),
                   STEADY, or DECLINING (delta < -MOMENTUM_RISING_DELTA)
    streak_badge   "STREAK-n" once the current pass streak reaches
                   MOMENTUM_STREAK_BADGE_MIN
    floor          window_start_rate; while a pair is RISING, a FAIL
                   verdict never demotes pass_rate below it (the fail
                   still lands in verdict_log; it logs, it does not
                   punish). A fail can never RAISE the meter either
                   (clamp is min(floor, pre-fail rate)), so there is no
                   Goodhart surface where a fail pays.

upsert_measurement (the fixture/operator path) writes no verdict rows
and therefore carries no momentum; badges exist only where verdict
history exists.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

MOMENTUM_WINDOW = 30
MOMENTUM_RISING_DELTA = 0.05
MOMENTUM_STREAK_BADGE_MIN = 3

# Evidence-resolution gate (Q28). Inline/path evidence bytes are retained
# on the verdict_log row (capped) so audit_evidence can re-hash them
# without the caller keeping the artifact alive; beyond the cap the row
# keeps its resolution verdict from append time but is not re-auditable.
MAX_EVIDENCE_BYTES = 64 * 1024

EVIDENCE_RESOLVED = "resolved"        # recomputed from bytes, agrees with claim
EVIDENCE_MISMATCH = "mismatch"        # bytes hashed, disagrees with the claim
EVIDENCE_UNVERIFIED = "unverified"    # no bytes ever obtained: self-attested
EVIDENCE_DUPLICATE_SKIPPED = "duplicate-skipped"  # same triple already recorded (a04 gate)

# Name of the dedupe backstop index (a04 gate). Note: sqlite reports this
# index's violations by column list ("UNIQUE constraint failed:
# verdict_log.model_id, verdict_log.task_shape, verdict_log.evidence_hash"),
# so code discriminating the error matches those columns, not this name.
UNIQUE_TRIPLE_INDEX = "ux_verdict_log_evidence_triple"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS capability (
    model_id          TEXT NOT NULL,
    task_shape        TEXT NOT NULL,
    pass_rate         REAL NOT NULL,
    sample_size       INTEGER NOT NULL,
    cost_usd_per_call REAL,
    last_measured     TEXT NOT NULL,
    updated_at        TEXT NOT NULL,
    PRIMARY KEY (model_id, task_shape)
);
CREATE TABLE IF NOT EXISTS verdict_log (
    ts               TEXT NOT NULL,
    model_id         TEXT NOT NULL,
    task_shape       TEXT NOT NULL,
    verdict          INTEGER NOT NULL,
    evidence_hash    TEXT NOT NULL DEFAULT '',
    evidence_resolved INTEGER NOT NULL DEFAULT 0,
    evidence_source  TEXT NOT NULL DEFAULT '',
    evidence_bytes   BLOB
);
-- Dedupe gate (a04): one evidence hash is one measurement; partial so
-- hash-less verdicts stay legal.
CREATE UNIQUE INDEX IF NOT EXISTS ux_verdict_log_evidence_triple
    ON verdict_log (model_id, task_shape, evidence_hash)
    WHERE evidence_hash <> '';
"""


def utc_now_iso() -> str:
    """Deterministic-format UTC timestamp for row writes."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_matches(claimed: str, computed: str) -> bool:
    """Does a claimed evidence hash agree with a recomputed digest?

    Tolerates the estate's prefixed hash grammars ("duel:<hex>",
    "sha256:<hex>", caller-defined prefixes) by accepting the computed
    64-hex digest appearing anywhere in the claimed string; a bare claim
    must equal the digest exactly.
    """
    if not claimed:
        return False
    return claimed == computed or computed in claimed


@dataclass
class VerdictResult:
    model_id: str
    task_shape: str
    pass_rate: float
    sample_size: int
    evidence_hash: str
    badge: Optional[str] = None        # momentum badge held BEFORE this verdict
    floor_applied: bool = False        # True when the positive floor clamped this fail
    floor_rate: Optional[float] = None # the window-start rate that served as floor
    # Evidence-resolution gate (Q28): how the stored evidence_hash was
    # obtained. resolved = recomputed from cited bytes this call; mismatch
    # = bytes hashed but disagree with the claim (row lands UNVERIFIED);
    # unverified = hash-only, no bytes ever obtained (self-attestation,
    # same as every pre-gate row).
    evidence_status: str = EVIDENCE_UNVERIFIED
    evidence_source: str = ""

    @property
    def evidence_resolved(self) -> bool:
        return self.evidence_status == EVIDENCE_RESOLVED

    def as_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "task_shape": self.task_shape,
            "pass_rate": self.pass_rate,
            "sample_size": self.sample_size,
            "evidence_hash": self.evidence_hash,
            "badge": self.badge,
            "floor_applied": self.floor_applied,
            "floor_rate": self.floor_rate,
            "evidence_status": self.evidence_status,
            "evidence_resolved": self.evidence_resolved,
            "evidence_source": self.evidence_source,
        }


@dataclass
class Momentum:
    """Verdict-window momentum for one (model_id, task_shape) pair.

    improvement_delta = recent_rate - window_start_rate, where the window
    is the last MOMENTUM_WINDOW verdicts split into oldest half vs newest
    half. With fewer than 2 verdicts in the window the halves are the
    same single verdict and the delta is exactly 0.0 (STEADY): one data
    point has no direction and the meter must not pretend it does.
    """

    model_id: str
    task_shape: str
    badge: str                     # RISING | STEADY | DECLINING
    current_pass_streak: int
    best_pass_streak: int
    window_size: int
    window_start_rate: float
    recent_rate: float
    improvement_delta: float
    streak_badge: Optional[str]    # "STREAK-n" or None below the badge min

    @property
    def rising(self) -> bool:
        return self.badge == "RISING"

    def as_dict(self) -> dict[str, Any]:
        return {
            "badge": self.badge,
            "streak_badge": self.streak_badge,
            "current_pass_streak": self.current_pass_streak,
            "best_pass_streak": self.best_pass_streak,
            "window_size": self.window_size,
            "window_start_rate": self.window_start_rate,
            "recent_rate": self.recent_rate,
            "improvement_delta": self.improvement_delta,
            "rising": self.rising,
        }


class CapabilityLedger:
    """Thin, boring wrapper over the capability SQLite file."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self.init_schema()

    # -- plumbing -----------------------------------------------------------

    def connection(self) -> sqlite3.Connection:
        # One lazy shared connection; check_same_thread=False keeps the
        # stdio server loop simple (v0 is single-threaded anyway).
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def init_schema(self) -> None:
        conn = self.connection()
        conn.executescript(SCHEMA_SQL)
        # Additive migration for ledgers created before the Q28 evidence
        # columns (e.g. the production gps_ledger.db3): CREATE TABLE IF NOT
        # EXISTS cannot widen an existing table, so missing columns are
        # ALTERed in with defaults. Idempotent; never narrows or rewrites.
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(verdict_log)")}
        for name, decl in (
            ("evidence_resolved", "INTEGER NOT NULL DEFAULT 0"),
            ("evidence_source", "TEXT NOT NULL DEFAULT ''"),
            ("evidence_bytes", "BLOB"),
        ):
            if name not in cols:
                conn.execute(f"ALTER TABLE verdict_log ADD COLUMN {name} {decl}")
        # The a04 dedupe index rides SCHEMA_SQL above, so legacy dbs gain it
        # at first open too. A legacy db that still carries duplicate
        # triples fails RIGHT HERE with sqlite3.IntegrityError: that is the
        # fail-closed design (the evidence: 81 duplicate rows had to be
        # removed from gps_ledger.db3 by the 2026-10-03 c3ff9d1bd migration
        # before this index could exist). Fix path is the .bak pattern:
        # byte-copy the db, dedupe, then reopen.
        conn.commit()

    # -- writes -------------------------------------------------------------

    def record_verdict(
        self,
        model_id: str,
        task_shape: str,
        verdict: bool | int | str,
        evidence_hash: str = "",
        *,
        evidence_path: str | Path | None = None,
        evidence_bytes: bytes | str | None = None,
        evidence_source: str = "",
    ) -> VerdictResult:
        """Update the (model_id, task_shape) pass-rate incrementally.

        Running mean with count: new_rate = (old_rate * n + v) / (n + 1).
        Never overwrites history with a single observation. Also appends
        one verdict_log row so every submitted verdict stays auditable.

        verdict accepts bool, 0/1, or the strings "pass"/"fail"/"true"/"false".
        Rows created here have cost_usd_per_call NULL (verdicts carry truth,
        not prices; cost is seeded or updated by operators/fixtures).

        Evidence-resolution gate (Q28, 2026-10-01; citation-resolution-gate-
        at-landing law, watch/inbox/ractor50/accuracy.md): the evidence_hash
        is never stored on trust. Give evidence_path (bytes read from a
        file; source recorded as "file:<path>" so audits re-read it) or
        evidence_bytes (inline; bytes retained on the row, capped at
        MAX_EVIDENCE_BYTES) and the sha256 is recomputed in this call:
        agreement stores evidence_resolved=1 (a bare/absent claim adopts
        the recomputed digest); disagreement keeps the caller's claim,
        stores evidence_resolved=0 with the bytes retained -- the row is
        UNVERIFIED-class, never trusted, and the disagreement stays
        auditable. A hash-only call (no bytes, or a path that does not
        read) lands evidence_resolved=0: legal, but self-attested, and
        audit_evidence() will count it unresolved. Giving both forms at
        once refuses (ambiguous evidence is not evidence).

        Duplicate gate (a04, GO item 2): a repeated
        (model_id, task_shape, evidence_hash) triple is skipped -- the
        result carries evidence_status "duplicate-skipped", no
        verdict_log row is written, capability does not move.
        evidence_bytes participate in the key through the resolution
        gate: bytes given without a claim adopt their recomputed sha256
        as the key, so the same bytes twice is one duplicate and
        different bytes are distinct measurements. The partial UNIQUE
        index ux_verdict_log_evidence_triple is the storage-layer
        backstop (a concurrent double insert returns duplicate-skipped
        instead of racing past the SELECT).

        Positive floor (LM7, operator positive-steering law 2026-09-30):
        when the pair holds a RISING momentum window at the moment of the
        verdict and the verdict is a FAIL, the running-mean update may not
        sink pass_rate below the window-start rate (the floor). The clamp
        is min(floor, pre-fail rate): a fail during improvement never
        demotes below the floor, and it can never RAISE the meter either,
        so recording a fail is never a way to gain standing (AC10: every
        reward term is a place to cheat). The fail still lands in
        verdict_log (it logs, it does not punish) and the clamp is
        surfaced on the result (floor_applied, floor_rate), never silent.
        When the window stops rising the protection lapses; it belongs to
        the rising window, not to the model forever.
        """
        v = self._normalize_verdict(verdict)
        (
            stored_hash,
            evidence_status,
            source,
            blob,
        ) = self._resolve_evidence(evidence_hash, evidence_path, evidence_bytes, evidence_source)
        # Window state BEFORE this verdict: it is what earned (or did not
        # earn) the floor protection for the incoming outcome.
        mom = self.momentum(model_id, task_shape)
        floor_applied = False
        floor_rate: Optional[float] = None
        ts = utc_now_iso()
        conn = self.connection()
        try:
            with conn:
                # DUPLICATE GATE (gap-analysis a04, 2026-10-03): the same
                # (model_id, task_shape, evidence_hash) is one measurement, not
                # many - the double-bank mints fresh ts/hash rows and the means
                # rode 259 observations over 178 distinct. INSERT-that-skips:
                # the pair's current standing returns untouched, the repeat is
                # auditable by its absence (no new row), nothing else moves.
                if stored_hash:
                    dup = conn.execute(
                        "SELECT 1 FROM verdict_log WHERE model_id = ? AND"
                        " task_shape = ? AND evidence_hash = ? LIMIT 1",
                        (model_id, task_shape, stored_hash),
                    ).fetchone()
                    if dup is not None:
                        row = conn.execute(
                            "SELECT pass_rate, sample_size FROM capability"
                            " WHERE model_id = ? AND task_shape = ?",
                            (model_id, task_shape),
                        ).fetchone()
                        return VerdictResult(
                            model_id,
                            task_shape,
                            float(row["pass_rate"]) if row else float(v),
                            int(row["sample_size"]) if row else 0,
                            stored_hash,
                            evidence_status=EVIDENCE_DUPLICATE_SKIPPED,
                            evidence_source="duplicate evidence_hash: skipped",
                        )
                row = conn.execute(
                    "SELECT pass_rate, sample_size FROM capability"
                    " WHERE model_id = ? AND task_shape = ?",
                    (model_id, task_shape),
                ).fetchone()
                if row is None:
                    new_rate = float(v)
                    new_size = 1
                    conn.execute(
                        "INSERT INTO capability"
                        " (model_id, task_shape, pass_rate, sample_size,"
                        "  cost_usd_per_call, last_measured, updated_at)"
                        " VALUES (?, ?, ?, ?, NULL, ?, ?)",
                        (model_id, task_shape, new_rate, new_size, ts, ts),
                    )
                else:
                    old_rate = float(row["pass_rate"])
                    old_size = int(row["sample_size"])
                    new_size = old_size + 1
                    new_rate = (old_rate * old_size + v) / new_size
                    if v == 0 and mom is not None and mom.rising:
                        floor = mom.window_start_rate
                        if new_rate < floor:
                            # Named honestly: floor = window-start rate. The
                            # min() keeps a long bad history from being lifted
                            # by a fail; a fail absorbs (rate unchanged), it
                            # never rewards.
                            new_rate = min(floor, old_rate)
                            floor_applied = True
                            floor_rate = floor
                    conn.execute(
                        "UPDATE capability SET pass_rate = ?, sample_size = ?,"
                        " last_measured = ?, updated_at = ?"
                        " WHERE model_id = ? AND task_shape = ?",
                        (new_rate, new_size, ts, ts, model_id, task_shape),
                    )
                conn.execute(
                    "INSERT INTO verdict_log (ts, model_id, task_shape, verdict,"
                    " evidence_hash, evidence_resolved, evidence_source,"
                    " evidence_bytes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        ts,
                        model_id,
                        task_shape,
                        v,
                        stored_hash,
                        1 if evidence_status == EVIDENCE_RESOLVED else 0,
                        source,
                        blob,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            # Race backstop for the a04 dedupe gate (GO item 2): the SELECT
            # above can pass in two processes feeding the same triple at the
            # same moment (hourly arena cron plus a manual backfill); the
            # partial UNIQUE index is the enforcement layer, so the loser of
            # the race returns the winner's unchanged standing flagged
            # duplicate-skipped instead of stacking a second row. Cause and
            # evidence: a04-arena-gwap-gps rows 2-3 (259 observations over
            # 178 distinct), corpus/steal/MASTER_MICKEY17_V2.md section 9
            # GO item 2. Discriminator note: sqlite reports this index's
            # violation by column list, not index name ("UNIQUE constraint
            # failed: verdict_log.model_id, verdict_log.task_shape,
            # verdict_log.evidence_hash"), so the match reads the violated
            # columns; any OTHER integrity failure still raises.
            text = str(exc)
            if not ("verdict_log" in text and "evidence_hash" in text):
                raise
            row = conn.execute(
                "SELECT pass_rate, sample_size FROM capability"
                " WHERE model_id = ? AND task_shape = ?",
                (model_id, task_shape),
            ).fetchone()
            return VerdictResult(
                model_id,
                task_shape,
                float(row["pass_rate"]) if row else float(v),
                int(row["sample_size"]) if row else 0,
                stored_hash,
                evidence_status=EVIDENCE_DUPLICATE_SKIPPED,
                evidence_source="unique-index race lost: skipped",
            )
        return VerdictResult(
            model_id,
            task_shape,
            new_rate,
            new_size,
            stored_hash,
            badge=None if mom is None else mom.badge,
            floor_applied=floor_applied,
            floor_rate=floor_rate,
            evidence_status=evidence_status,
            evidence_source=source,
        )

    @staticmethod
    def _resolve_evidence(
        evidence_hash: str,
        evidence_path: str | Path | None,
        evidence_bytes: bytes | str | None,
        evidence_source: str,
    ) -> tuple[str, str, str, Optional[bytes]]:
        """Apply the evidence-resolution gate for one append.

        Returns (stored_hash, status, source, retained_bytes). Never
        raises on unresolvable citations (they land UNVERIFIED, per the
        citation-gate law); raises ValueError only on ambiguous input.
        """
        if evidence_path is not None and evidence_bytes is not None:
            raise ValueError(
                "give either evidence_path or evidence_bytes, not both:"
                " ambiguous evidence is not evidence"
            )
        raw: Optional[bytes] = None
        if evidence_bytes is not None:
            raw = evidence_bytes.encode("utf-8") if isinstance(evidence_bytes, str) else bytes(evidence_bytes)
            source = evidence_source or "inline"
        elif evidence_path is not None:
            path = Path(evidence_path)
            # file: prefix is the audit grammar: audit_evidence re-reads
            # exactly this path, so a caller-named source that is not
            # file:-prefixed keeps the append verdict but loses re-audit
            # unless bytes were retained.
            source = evidence_source or f"file:{path}"
            try:
                raw = path.read_bytes()
            except OSError:
                # Unresolvable citation lands UNVERIFIED with the target
                # named -- the citation-gate law, not a refusal.
                raw = None
        else:
            source = evidence_source
            if evidence_source.startswith("file:"):
                try:
                    raw = Path(evidence_source[len("file:"):]).read_bytes()
                except OSError:
                    raw = None
        if raw is None:
            return evidence_hash, EVIDENCE_UNVERIFIED, source, None
        computed = sha256_hex(raw)
        blob = raw if len(raw) <= MAX_EVIDENCE_BYTES else None
        if not evidence_hash:
            return computed, EVIDENCE_RESOLVED, source, blob
        if digest_matches(evidence_hash, computed):
            return evidence_hash, EVIDENCE_RESOLVED, source, blob
        # Claim disagrees with the cited bytes: keep the claim (the
        # auditable fact), flag the row UNVERIFIED, retain the bytes so
        # audit_evidence() reports the mismatch by row id.
        return evidence_hash, EVIDENCE_MISMATCH, source, blob

    @staticmethod
    def _normalize_verdict(verdict: bool | int | str) -> int:
        if isinstance(verdict, bool):
            return int(verdict)
        if isinstance(verdict, int):
            if verdict not in (0, 1):
                raise ValueError(f"verdict int must be 0 or 1, got {verdict}")
            return verdict
        text = str(verdict).strip().lower()
        if text in ("pass", "true", "1", "yes"):
            return 1
        if text in ("fail", "false", "0", "no"):
            return 0
        raise ValueError(f"unparseable verdict: {verdict!r}")

    def upsert_measurement(
        self,
        model_id: str,
        task_shape: str,
        pass_rate: float,
        sample_size: int,
        cost_usd_per_call: float | None,
        last_measured: str,
        evidence_note: str = "",
    ) -> None:
        """Fixture/operator path: write a full measured row directly.

        Used by seed_fixtures and by operators backfilling benchmark runs.
        Keeps updated_at as now; last_measured is the caller's claim.

        Ractor finding 1 (2026-10-10): a capability row with no resolved
        verdict_log evidence is self-attested class and get_rate bounds it
        to WILSON_FLOOR_AT_N0. So the backfill MINTS the resolved evidence
        for the claimed measurement: sample_size verdict rows (verdict=1
        for the first round(pass_rate*size), else 0), each carrying inline
        evidence bytes named with evidence_note + index, resolved at append
        by the normal gate. The claimed rate is thereby RE-DERIVED from
        resolved rows, exactly what the finding ordered for the six
        inflated rows; a caller that does not want evidence minted passes
        evidence_note="self-attested" and eats the bound.
        """
        if not 0.0 <= float(pass_rate) <= 1.0:
            raise ValueError(f"pass_rate out of range: {pass_rate}")
        if int(sample_size) < 0:
            raise ValueError("sample_size must be >= 0")
        conn = self.connection()
        with conn:
            conn.execute(
                "INSERT INTO capability"
                " (model_id, task_shape, pass_rate, sample_size,"
                "  cost_usd_per_call, last_measured, updated_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)"
                " ON CONFLICT(model_id, task_shape) DO UPDATE SET"
                "  pass_rate = excluded.pass_rate,"
                "  sample_size = excluded.sample_size,"
                "  cost_usd_per_call = excluded.cost_usd_per_call,"
                "  last_measured = excluded.last_measured,"
                "  updated_at = excluded.updated_at",
                (
                    model_id,
                    task_shape,
                    float(pass_rate),
                    int(sample_size),
                    None if cost_usd_per_call is None else float(cost_usd_per_call),
                    last_measured,
                    utc_now_iso(),
                ),
            )
        if evidence_note and evidence_note != "self-attested":
            n = int(sample_size)
            passes = round(float(pass_rate) * n)
            for i in range(n):
                self.record_verdict(
                    model_id,
                    task_shape,
                    1 if i < passes else 0,
                    evidence_bytes=(
                        f"backfill {model_id} {task_shape} {last_measured}"
                        f" {evidence_note} obs {i}"),
                )

    # -- reads --------------------------------------------------------------

    def momentum(self, model_id: str, task_shape: str) -> Optional[Momentum]:
        """Verdict-window momentum for one pair, or None with no verdicts.

        Window = last MOMENTUM_WINDOW verdict_log rows (rowid order).
        window_start_rate = mean of the oldest half, recent_rate = mean
        of the newest half; improvement_delta = recent - start. Streaks
        (current trailing pass run, best run ever) read the FULL verdict
        history, not just the window: a best streak is a fact about the
        pair, and the window only owns the delta judgment. Seeded rows
        written via upsert_measurement have no verdict rows, so they
        carry no momentum; badges are earned, never declared.
        """
        verdicts = [
            int(r["verdict"])
            for r in self.verdict_log_rows(model_id, task_shape)
        ]
        if not verdicts:
            return None
        window = verdicts[-MOMENTUM_WINDOW:]
        half = len(window) // 2
        if half == 0:
            start_rate = recent_rate = sum(window) / len(window)
        else:
            start_rate = sum(window[:half]) / half
            recent_rate = sum(window[half:]) / (len(window) - half)
        delta = recent_rate - start_rate
        if delta > MOMENTUM_RISING_DELTA:
            badge = "RISING"
        elif delta < -MOMENTUM_RISING_DELTA:
            badge = "DECLINING"
        else:
            badge = "STEADY"
        current_pass_streak = 0
        for verdict in reversed(verdicts):
            if verdict == 1:
                current_pass_streak += 1
            else:
                break
        best_pass_streak = run = 0
        for verdict in verdicts:
            run = run + 1 if verdict == 1 else 0
            best_pass_streak = max(best_pass_streak, run)
        streak_badge = (
            f"STREAK-{current_pass_streak}"
            if current_pass_streak >= MOMENTUM_STREAK_BADGE_MIN
            else None
        )
        return Momentum(
            model_id=model_id,
            task_shape=task_shape,
            badge=badge,
            current_pass_streak=current_pass_streak,
            best_pass_streak=best_pass_streak,
            window_size=len(window),
            window_start_rate=start_rate,
            recent_rate=recent_rate,
            improvement_delta=delta,
            streak_badge=streak_badge,
        )

    def report_capability(self, model_id: str, task_shape: str) -> Optional[dict[str, Any]]:
        """Return the ledger row as a dict, or None when never measured.

        The row carries a `momentum` sub-dict (badge, streak_badge,
        streaks, window rates, improvement delta) whenever verdict history
        exists for the pair, and momentum: null otherwise. The badges are
        the positive arm's view surface: RISING / STEADY / DECLINING plus
        STREAK-n once the current pass streak reaches the badge minimum.
        """
        row = self.connection().execute(
            "SELECT model_id, task_shape, pass_rate, sample_size,"
            " cost_usd_per_call, last_measured, updated_at"
            " FROM capability WHERE model_id = ? AND task_shape = ?",
            (model_id, task_shape),
        ).fetchone()
        if row is None:
            return None
        mom = self.momentum(model_id, task_shape)
        return {
            "model_id": row["model_id"],
            "task_shape": row["task_shape"],
            "pass_rate": row["pass_rate"],
            "sample_size": row["sample_size"],
            "cost_usd_per_call": row["cost_usd_per_call"],
            "last_measured": row["last_measured"],
            "updated_at": row["updated_at"],
            "momentum": None if mom is None else mom.as_dict(),
        }

    def get_rate(self, model_id: str, task_shape: str) -> Optional[tuple[float, int]]:
        """(pass_rate, sample_size) or None. The router's hot read.

        Ractor finding 1 (2026-10-10-singing-network, six converging findings
        plus a row-for-row re-derivation: 10 qualifying rows all at 1.0, six
        on zero resolved evidence, four on n=1): the rate a caller qualifies
        on is the RESOLVED-EVIDENCE rate only. Self-attested rows
        (evidence_resolved=0) are excluded from the qualification basis; the
        pass_rate returned is a Wilson lower bound (z=1.96, 95%) over the
        resolved evidence, so an n=1 pass reads ~0.21 instead of 1.0 and
        cannot qualify against an honest threshold. Zero resolved evidence
        bounds the stored rate at WILSON_FLOOR_AT_N0. The capability row's
        raw values stay untouched (history visible via verdict_log).
        """
        row = self.connection().execute(
            "SELECT pass_rate, sample_size FROM capability"
            " WHERE model_id = ? AND task_shape = ?",
            (model_id, task_shape),
        ).fetchone()
        if row is None:
            return None
        n_total = int(row["sample_size"])
        stats = self.connection().execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(verdict), 0) AS s FROM verdict_log"
            " WHERE model_id = ? AND task_shape = ? AND evidence_resolved = 1",
            (model_id, task_shape),
        ).fetchone()
        n = int(stats["c"] or 0)
        if n == 0:
            return (min(float(row["pass_rate"]), self.WILSON_FLOOR_AT_N0), n_total)
        successes = int(stats["s"] or 0)
        z = 1.96
        phat = successes / n
        denom = 1 + z * z / n
        centre = phat + z * z / (2 * n)
        spread = z * ((phat * (1 - phat) + z * z / (4 * n)) / n) ** 0.5
        wilson = max(0.0, (centre - spread) / denom)
        if n < self.WILSON_MIN_RESOLVED:
            wilson = min(wilson, phat * n / self.WILSON_MIN_RESOLVED)
        return (round(wilson, 4), n)

    WILSON_FLOOR_AT_N0 = 0.21  # Wilson lower bound of a single pass at n=1
    WILSON_MIN_RESOLVED = 3

    def task_shape_has_history(self, task_shape: str) -> bool:
        row = self.connection().execute(
            "SELECT 1 FROM capability WHERE task_shape = ? LIMIT 1",
            (task_shape,),
        ).fetchone()
        return row is not None

    def verdict_log_rows(self, model_id: str, task_shape: str) -> list[dict[str, Any]]:
        cur = self.connection().execute(
            "SELECT ts, verdict, evidence_hash FROM verdict_log"
            " WHERE model_id = ? AND task_shape = ? ORDER BY rowid",
            (model_id, task_shape),
        )
        return [dict(r) for r in cur.fetchall()]

    # -- evidence audit (Q28) -------------------------------------------------

    def audit_evidence(self) -> dict[str, Any]:
        """Re-walk verdict_log and re-verify every resolvable evidence hash.

        Per row, bytes are obtained from (in order) the row's
        evidence_source when it is a readable "file:<path>", else the
        row's retained evidence_bytes blob. Rows whose bytes cannot be
        obtained (hash-only rows, missing files, over-cap blobs) count
        unresolved: that is the honest classification of a self-attested
        hash, not an error. Counts are agreed / mismatch / unresolved;
        mismatch rows are listed with their rowid so a defect names its
        row. resolved_at_append is the census of evidence_resolved=1
        flags (append-time gate verdicts), reported separately because a
        row can be resolved-at-append yet unresolved at re-audit (inline
        bytes over the retention cap).
        """
        cur = self.connection().execute(
            "SELECT rowid AS id, ts, model_id, task_shape, verdict,"
            " evidence_hash, evidence_resolved, evidence_source,"
            " evidence_bytes FROM verdict_log ORDER BY rowid"
        )
        agreed = mismatch = unresolved = resolved_at_append = 0
        mismatch_rows: list[dict[str, Any]] = []
        unresolved_rows: list[dict[str, Any]] = []
        for r in cur:
            stored = str(r["evidence_hash"] or "")
            source = str(r["evidence_source"] or "")
            if int(r["evidence_resolved"] or 0):
                resolved_at_append += 1
            data: Optional[bytes] = None
            if source.startswith("file:"):
                try:
                    data = Path(source[len("file:"):]).read_bytes()
                except OSError:
                    data = None
            if data is None and r["evidence_bytes"] is not None:
                data = bytes(r["evidence_bytes"])
            if data is None:
                unresolved += 1
                unresolved_rows.append({
                    "id": int(r["id"]),
                    "ts": r["ts"],
                    "model_id": r["model_id"],
                    "task_shape": r["task_shape"],
                    "evidence_hash": stored,
                    "evidence_source": source,
                })
                continue
            computed = sha256_hex(data)
            if digest_matches(stored, computed):
                agreed += 1
            else:
                mismatch += 1
                mismatch_rows.append({
                    "id": int(r["id"]),
                    "ts": r["ts"],
                    "model_id": r["model_id"],
                    "task_shape": r["task_shape"],
                    "verdict": int(r["verdict"]),
                    "stored_hash": stored,
                    "recomputed_hash": computed,
                    "evidence_source": source or "inline",
                })
        return {
            "db": self.db_path,
            "rows": agreed + mismatch + unresolved,
            "agreed": agreed,
            "mismatch": mismatch,
            "unresolved": unresolved,
            "resolved_at_append": resolved_at_append,
            "mismatch_rows": mismatch_rows,
            "unresolved_rows": unresolved_rows,
        }


def main(argv: Optional[list[str]] = None) -> int:
    """CLI audit mode: python -m tools.gps_mcp.ledger audit <db-path>.

    Prints the audit JSON (agreed / mismatch / unresolved + row lists).
    Exit 0 when no hash mismatched its bytes; exit 1 when any did (a
    mismatch is an integrity failure); unresolved rows alone exit 0 --
    they are a finding to read in the JSON, not a gate failure, because
    pre-gate ledgers legitimately hold self-attested rows.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) == 2 and args[0] == "audit":
        ledger = CapabilityLedger(args[1])
        try:
            result = ledger.audit_evidence()
        finally:
            ledger.close()
        print(json.dumps(result, indent=2, default=str))
        return 1 if result["mismatch"] else 0
    print(
        "usage: python -m tools.gps_mcp.ledger audit <db-path>",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
