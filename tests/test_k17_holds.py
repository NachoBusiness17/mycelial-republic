"""Tests for K.17 HOLD-STATE VISIBILITY (scripts/k17_pilot.py hold mode).

Chair 3's finding: "hold with no TTL, no owner, and no ack is burial with
paperwork." These tests pin the fix:
  1. run --hold records intent + dispatch, effect knowledge stays UNKNOWN,
     and a hold row {op_id, state: UNKNOWN, opened_ts, ttl_hours, owner}
     lands in holds.jsonl — no ledger effect is claimed.
  2. The `holds` report lists open holds with age; a fresh hold is quiet.
  3. Aging past TTL prints LOUD: "HOLD EXPIRED: <op_id> age <h>h — needs
     owner or NOT_APPLIED_FINAL" (the reaper; deterministic via --now).
  4. UNKNOWN survives restarts (every invocation is a fresh process) and
     replay that verifies the effect closes the hold (ack path).

Stdlib only: unittest driving the real CLI via subprocess.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "k17_pilot.py"
HOLDS_NAME = "holds.jsonl"
LEDGER_NAME = "fixture_ledger.jsonl"
FAR_FUTURE = "2027-01-01T00:00:00+00:00"

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=HEADLESS,
    )


def hold_rows(state_dir: Path) -> list[dict]:
    path = state_dir / HOLDS_NAME
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class K17HoldTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="k17_hold_test_")
        self.addCleanup(self._tmp.cleanup)
        self.state = Path(self._tmp.name) / "state"

    # -- 1. hold mode: intent + dispatch, UNKNOWN effect, hold row ----------

    def test_hold_mode_opens_hold_row_without_effect(self) -> None:
        r = run_cli("run", "--hold", "--state-dir", str(self.state))
        self.assertEqual(r.returncode, 5, "hold open must exit 5")
        out = json.loads(r.stdout)
        self.assertEqual(out["status"], "HOLD_OPEN")
        self.assertEqual(out["hold"]["state"], "UNKNOWN")
        self.assertEqual(out["hold"]["owner"], "unassigned")
        self.assertFalse(out["executed"])
        op_id = out["operation_id"]

        # no effect was committed (no APPLIED claim for an unverifiable op)
        ledger = self.state / LEDGER_NAME
        if ledger.exists():
            self.assertNotIn(
                op_id, ledger.read_text(encoding="utf-8"),
                "hold mode must not commit a ledger effect")

        # intent persisted BEFORE dispatch, hold row persisted AFTER
        self.assertTrue((self.state / "intents" / f"{op_id}.json").exists())
        rows = hold_rows(self.state)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["event"], "hold_open")
        self.assertEqual(row["op_id"], op_id)
        self.assertEqual(row["state"], "UNKNOWN")
        self.assertEqual(row["owner"], "unassigned")
        self.assertEqual(row["ttl_hours"], 24)
        self.assertIn("opened_ts", row)

        # the independent verifier sees the open hold and no false APPLIED
        v = run_cli("verify", "--state-dir", str(self.state))
        self.assertEqual(v.returncode, 0, v.stderr)
        vout = json.loads(v.stdout)
        self.assertEqual(vout["status"], "OK")
        self.assertEqual(vout["totals"]["holds_open"], 1)
        self.assertTrue(vout["operations"][0]["hold_open"])
        self.assertNotEqual(vout["operations"][0]["knowledge"], "APPLIED")

    # -- 2. holds report lists an open hold with age, fresh = quiet ---------

    def test_holds_report_lists_open_hold_quiet_when_fresh(self) -> None:
        r = run_cli("run", "--hold", "--state-dir", str(self.state))
        self.assertEqual(r.returncode, 5)
        op_id = json.loads(r.stdout)["operation_id"]

        h = run_cli("holds", "--state-dir", str(self.state))
        self.assertEqual(h.returncode, 0, h.stderr)
        hout = json.loads(h.stdout)
        self.assertEqual(hout["status"], "OK")
        self.assertEqual(hout["totals"]["open"], 1)
        entry = hout["holds"][0]
        self.assertEqual(entry["op_id"], op_id)
        self.assertEqual(entry["state"], "UNKNOWN")
        self.assertFalse(entry["expired"])
        self.assertLessEqual(entry["age_hours"], 24)
        self.assertNotIn("HOLD EXPIRED", h.stdout)

        # second independent process reads the same persisted UNKNOWN state
        h2 = run_cli("holds", "--state-dir", str(self.state))
        self.assertEqual(json.loads(h2.stdout)["holds"][0]["state"], "UNKNOWN")

    # -- 3. aging past TTL prints LOUD (deterministic via --now) ------------

    def test_hold_older_than_ttl_prints_loud_expired(self) -> None:
        r = run_cli("run", "--hold", "--state-dir", str(self.state))
        self.assertEqual(r.returncode, 5)
        op_id = json.loads(r.stdout)["operation_id"]

        h = run_cli("holds", "--state-dir", str(self.state), "--now", FAR_FUTURE)
        self.assertEqual(h.returncode, 5, "expired hold must exit 5")
        self.assertIn(
            f"HOLD EXPIRED: {op_id} age ", h.stdout,
            "expired hold must print the LOUD line")
        self.assertIn("needs owner or NOT_APPLIED_FINAL", h.stdout)
        json_payload = "\n".join(
            line for line in h.stdout.splitlines()
            if not line.startswith("HOLD EXPIRED")
        )
        hout = json.loads(json_payload)
        self.assertEqual(hout["status"], "HOLD_EXPIRED")
        self.assertEqual(hout["totals"]["expired"], 1)
        self.assertTrue(hout["holds"][0]["expired"])
        self.assertGreater(hout["holds"][0]["age_hours"], 24)

    # -- 4. hold idempotence + replay-closes-hold (ack path) ----------------

    def test_replay_verifying_effect_closes_hold(self) -> None:
        r1 = run_cli("run", "--hold", "--state-dir", str(self.state))
        self.assertEqual(r1.returncode, 5)
        op_id = json.loads(r1.stdout)["operation_id"]

        # re-run hold with the same intent: one op, one open hold, no dupes
        r2 = run_cli("run", "--hold", "--state-dir", str(self.state))
        self.assertEqual(r2.returncode, 5)
        self.assertEqual(json.loads(r2.stdout)["operation_id"], op_id)
        opens = [x for x in hold_rows(self.state) if x["event"] == "hold_open"]
        self.assertEqual(len(opens), 1, "must not duplicate the hold row")

        # replay verifies the effect -> hold closes with resolved_as=APPLIED
        r3 = run_cli("run", "--normal", "--state-dir", str(self.state))
        self.assertEqual(r3.returncode, 0, r3.stderr)
        self.assertEqual(json.loads(r3.stdout)["status"], "APPLIED")

        closes = [x for x in hold_rows(self.state) if x["event"] == "hold_close"]
        self.assertEqual(len(closes), 1)
        self.assertEqual(closes[0]["resolved_as"], "APPLIED")
        self.assertEqual(closes[0]["op_id"], op_id)

        h = run_cli("holds", "--state-dir", str(self.state), "--now", FAR_FUTURE)
        self.assertEqual(h.returncode, 0,
                         "closed hold must not trip the reaper")
        self.assertEqual(json.loads(h.stdout)["totals"]["open"], 0)

    # -- 5. holds report on an empty state dir is quiet ----------------------

    def test_holds_report_empty_state_is_ok(self) -> None:
        h = run_cli("holds", "--state-dir", str(self.state))
        self.assertEqual(h.returncode, 0, h.stderr)
        hout = json.loads(h.stdout)
        self.assertEqual(hout["status"], "OK")
        self.assertEqual(hout["totals"]["open"], 0)


if __name__ == "__main__":
    unittest.main()
