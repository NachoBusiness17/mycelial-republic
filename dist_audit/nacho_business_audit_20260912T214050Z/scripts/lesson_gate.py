#!/usr/bin/env python3
"""lesson_gate.py — Build 3.5's lesson admission gate. Schema lesson_gate.v1. $0 stdlib.

Every fold produces lessons (amendments, corrections, patterns) that feed the
next generation's prompts. The gate decides which ones pass:

  1. PROVENANCE  — which lane/run produced it (required, else REJECT)
  2. EVIDENCE    — must cite the receipt/diff that earned it (required, else REJECT)
  3. DUPLICATION — an identical lesson already registered is BUMPED (count+1),
                   never re-added
  4. CONFLICT    — a lesson contradicting a registered lesson goes to the
                   conflict queue for operator review; never auto-promoted
  5. EXPIRY      — ttl_days (default 90); lessons expire silently out of the
                   active view unless re-earned (re-admission revives, count+1)

Conflict detection is a DETERMINISTIC HEURISTIC, not a judge: explicit
``contradicts`` ids, or same subject key with flipped polarity (negation
token present/absent). False conflicts fail CLOSED to the operator queue —
nothing auto-promotes, matching the no-auto-promote law.

State: memory/lesson_gate/registry.json (override: LESSON_GATE_REGISTRY env).
Writes are atomic (tmp + os.replace) under an O_EXCL lockfile with stale-lock
theft. No daemons, no schedulers.

CLI:
  python scripts/lesson_gate.py admit --file L.json | --stdin
  python scripts/lesson_gate.py sweep
  python scripts/lesson_gate.py show [--all]
  python scripts/lesson_gate.py selftest

Lesson input fields:
  statement   (req) the lesson text
  provenance  (req) {"lane": "...", "run": "..."} or "lane/run" string
  evidence    (req) citation of the receipt/diff that earned it
  subject     (opt) conflict-matching key; derived from statement if absent
  contradicts (opt) explicit lesson ids this lesson opposes -> conflict queue
  tags        (opt) list of strings
  ttl_days    (opt) default 90
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO / "memory" / "lesson_gate" / "registry.json"
SCHEMA = "lesson_gate.v1"
DEFAULT_TTL_DAYS = 90
LOCK_TIMEOUT_S = 5.0
STALE_LOCK_S = 30.0

for _p in (DEFAULT_REGISTRY,):
    if REPO not in _p.resolve().parents:
        raise ValueError(f"write target escapes repo: {_p}")

NEG_RE = re.compile(
    r"\b(never|not|no|none|don'?t|does ?not|cannot|can'?t|avoid|without|"
    r"except|must not|fail(?:s|ed)? to)\b"
)
_WS_RE = re.compile(r"\s+")


# ---------------------------------------------------------------- time / text
def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def normalize(text: str) -> str:
    t = (text or "").lower().strip()
    t = re.sub(r"[.!?;:,]+$", "", t)
    return _WS_RE.sub(" ", t)


def polarity(stmt_norm: str) -> str:
    return "negate" if NEG_RE.search(stmt_norm) else "affirm"


def subject_key(lesson: dict, stmt_norm: str) -> str:
    """Deterministic heuristic conflict key. Derived keys keep the first 3
    tokens of the negation-stripped statement (trailing modifiers stripped so
    'never X' vs 'X freely' collide); explicit subjects are trusted verbatim.
    False conflicts fail CLOSED to the operator queue, never auto-promoted."""
    explicit = lesson.get("subject")
    if explicit:
        return normalize(str(explicit)) or stmt_norm
    key = _WS_RE.sub(" ", NEG_RE.sub(" ", stmt_norm)).strip()
    tokens = re.sub(r"[^\w\s-]", " ", key).split()
    return " ".join(tokens[:3]) if tokens else stmt_norm


def lesson_id(stmt_norm: str) -> str:
    return hashlib.sha1(stmt_norm.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------- registry io
def registry_path() -> Path:
    env = os.environ.get("LESSON_GATE_REGISTRY")
    p = Path(env) if env else DEFAULT_REGISTRY
    p.resolve()  # raises on malformed path
    return p


def empty_registry() -> dict:
    return {
        "schema": SCHEMA,
        "updated_at": now_iso(),
        "lessons": [],
        "conflicts": [],
        "stats": {"accepted": 0, "bumped": 0, "rejected": 0,
                  "conflicted": 0, "expired": 0, "reearned": 0},
    }


class _Lock:
    """O_EXCL lockfile with stale-lock theft. Context manager."""

    def __init__(self, path: Path):
        self.path = path.with_suffix(path.suffix + ".lock")

    def __enter__(self):
        deadline = time.monotonic() + LOCK_TIMEOUT_S
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > STALE_LOCK_S:
                        self.path.unlink(missing_ok=True)
                        continue
                except OSError:
                    pass
                if time.monotonic() > deadline:
                    self.path.unlink(missing_ok=True)  # last resort: steal
                    continue
                time.sleep(0.05)

    def __exit__(self, *exc):
        self.path.unlink(missing_ok=True)
        return False


class Gate:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else registry_path()

    # -- io --
    def load(self) -> dict:
        if not self.path.exists():
            return empty_registry()
        with self.path.open("r", encoding="utf-8") as f:
            reg = json.load(f)
        if reg.get("schema") != SCHEMA:
            raise ValueError(f"registry schema mismatch: {reg.get('schema')!r}")
        return reg

    def save(self, reg: dict) -> None:
        reg["updated_at"] = now_iso()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with _Lock(self.path):
            tmp = self.path.with_suffix(".json.tmp")
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(reg, f, indent=2, ensure_ascii=False)
                f.write("\n")
            os.replace(tmp, self.path)

    # -- views --
    def active(self, reg: dict | None = None) -> list[dict]:
        reg = reg if reg is not None else self.load()
        return [l for l in reg["lessons"] if l["status"] == "active"]

    # -- gates --
    def admit(self, lesson: dict, now: str | None = None) -> dict:
        """Run one lesson through the five gates. Returns a decision dict."""
        ts = now or now_iso()
        self._validate_schema_version(lesson)

        # Gates 1+2: PROVENANCE and EVIDENCE (required fields)
        prov = self._coerce_provenance(lesson.get("provenance"))
        evidence = lesson.get("evidence")
        evidence_ok = (isinstance(evidence, str) and evidence.strip()) or \
                      (isinstance(evidence, dict) and any(evidence.values()))
        stmt = lesson.get("statement")
        stmt_ok = isinstance(stmt, str) and stmt.strip()
        early = None
        if not prov:
            early = ("no_provenance", "provenance (lane/run) is required")
        elif not evidence_ok:
            early = ("no_evidence",
                     "evidence citation (receipt/diff) is required")
        elif not stmt_ok:
            early = ("no_statement", "statement is required")
        if early:
            with _Lock(self.path):
                reg = self.load()
                self._stat(reg, "rejected")
                self.save(reg)
            return {"decision": "REJECT", "reason": early[0], "why": early[1]}

        norm = normalize(stmt)
        lid = lesson_id(norm)
        with _Lock(self.path):
            reg = self.load()
            by_id = {l["id"]: l for l in reg["lessons"]}

            # Gate 3: DUPLICATION (also the re-earn path for Gate 5)
            if lid in by_id:
                held = by_id[lid]
                held["count"] += 1
                held["last_seen"] = ts
                event = "bumped"
                if held["status"] == "expired":  # re-earned: silent expiry undone
                    held["status"] = "active"
                    held["expires_at"] = self._expiry(held, ts)
                    event = "reearned"
                held.setdefault("history", []).append({"at": ts, "event": event})
                self._stat(reg, event if event == "reearned" else "bumped")
                self.save(reg)
                return {"decision": "BUMP" if event == "bumped" else "REEARNED",
                        "id": lid, "count": held["count"]}

            # Gate 4: CONFLICT — never auto-promoted; fails closed to the queue
            against = None
            for declared in lesson.get("contradicts") or []:
                if declared in by_id and by_id[declared]["status"] == "active":
                    against = by_id[declared]
                    reason = "declared"
                    break
            if against is None:
                key = subject_key(lesson, norm)
                pol = polarity(norm)
                for held in self.active(reg):
                    if held["subject_key"] == key and held["polarity"] != pol:
                        against = held
                        reason = "polarity_flip"
                        break
            if against is not None:
                cid = hashlib.sha1(
                    f"{lid}:{against['id']}".encode()).hexdigest()[:12]
                reg["conflicts"].append({
                    "id": cid, "at": ts, "status": "pending_operator_review",
                    "reason": reason,
                    "incoming": {"id": lid, "statement": stmt.strip(),
                                 "provenance": prov, "evidence": evidence},
                    "against": {"id": against["id"],
                                "statement": against["statement"]},
                })
                self._stat(reg, "conflicted")
                self.save(reg)
                return {"decision": "CONFLICT", "id": lid, "conflict_id": cid,
                        "against": against["id"]}

            # Gate 1+2 passed, 3+4 clear -> ACCEPT
            record = {
                "id": lid,
                "statement": stmt.strip(),
                "statement_norm": norm,
                "subject_key": subject_key(lesson, norm),
                "polarity": polarity(norm),
                "provenance": prov,
                "evidence": evidence,
                "tags": list(lesson.get("tags") or []),
                "ttl_days": int(lesson.get("ttl_days") or DEFAULT_TTL_DAYS),
                "admitted_at": ts,
                "last_seen": ts,
                "expires_at": None,
                "count": 1,
                "status": "active",
                "history": [{"at": ts, "event": "admitted"}],
            }
            record["expires_at"] = self._expiry(record, ts)
            reg["lessons"].append(record)
            self._stat(reg, "accepted")
            self.save(reg)
            return {"decision": "ACCEPT", "id": lid}

    def sweep(self, now: str | None = None) -> dict:
        """Gate 5: expire silently — status flips, active view drops them."""
        ts = now or now_iso()
        now_dt = parse_iso(ts)
        with _Lock(self.path):
            reg = self.load()
            n = 0
            for held in reg["lessons"]:
                if held["status"] != "active":
                    continue
                if held["expires_at"] and parse_iso(held["expires_at"]) <= now_dt:
                    held["status"] = "expired"
                    held.setdefault("history", []).append(
                        {"at": ts, "event": "expired"})
                    self._stat(reg, "expired")
                    n += 1
            if n:
                self.save(reg)
        return {"decision": "SWEEP", "expired": n, "at": ts}

    # -- helpers --
    @staticmethod
    def _validate_schema_version(lesson: dict) -> None:
        v = lesson.get("schema")
        if v is not None and v != SCHEMA:
            raise ValueError(f"lesson schema {v!r} != {SCHEMA}")

    @staticmethod
    def _coerce_provenance(raw) -> dict | None:
        if isinstance(raw, dict):
            lane, run = str(raw.get("lane") or "").strip(), \
                        str(raw.get("run") or "").strip()
            if lane or run:
                return {"lane": lane, "run": run}
            return None
        if isinstance(raw, str) and raw.strip():
            parts = raw.strip().split("/", 1)
            return {"lane": parts[0].strip(),
                    "run": parts[1].strip() if len(parts) > 1 else ""}
        return None

    @staticmethod
    def _expiry(record: dict, ts: str) -> str:
        dt = parse_iso(ts) + timedelta(days=record["ttl_days"])
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _stat(reg: dict, key: str) -> None:
        reg["stats"][key] = reg["stats"].get(key, 0) + 1


# ---------------------------------------------------------------- cli
def _read_lesson(args) -> dict:
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.stdin:
        return json.load(sys.stdin)
    raise SystemExit("admit needs --file or --stdin")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="lesson admission gate (lesson_gate.v1)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_admit = sub.add_parser("admit")
    p_admit.add_argument("--file")
    p_admit.add_argument("--stdin", action="store_true")
    sub.add_parser("sweep")
    p_show = sub.add_parser("show")
    p_show.add_argument("--all", action="store_true",
                        help="include expired lessons")
    sub.add_parser("selftest")
    args = ap.parse_args(argv)

    gate = Gate()
    if args.cmd == "admit":
        print(json.dumps(gate.admit(_read_lesson(args)), indent=2))
    elif args.cmd == "sweep":
        print(json.dumps(gate.sweep(), indent=2))
    elif args.cmd == "show":
        reg = gate.load()
        lessons = reg["lessons"] if args.all else gate.active(reg)
        print(json.dumps({"schema": reg["schema"], "stats": reg["stats"],
                          "active": len(gate.active(reg)),
                          "conflicts_pending": sum(
                              1 for c in reg["conflicts"]
                              if c["status"] == "pending_operator_review"),
                          "lessons": lessons,
                          "conflicts": reg["conflicts"]},
                         indent=2))
    elif args.cmd == "selftest":
        import subprocess
        test = REPO / "tests" / "lesson_gate_test.py"
        r = subprocess.run([sys.executable, str(test)])
        return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
