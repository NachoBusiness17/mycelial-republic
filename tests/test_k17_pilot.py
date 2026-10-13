"""Tests for scripts/k17_pilot.py — the K.17 pilot skeleton (contract v0).

Wave-required invariants, on a disposable fixture state dir per test:
  1. normal run  -> EXACTLY one ledger effect for the operation id
  2. crash-after-intent + replay -> still EXACTLY one effect
  3. double replay -> zero new effects (B.09 idempotent dedup)
  4. same operation id + different intent bytes -> OPERATION_ID_CONFLICT,
     no dispatch (B.07 binding)
  5. verifier rejects a deliberately duplicated effect row (broken-dedup
     calibration, B.14) and reports PENDING for a crashed-unreplayed op.

Stdlib only: unittest driving the real CLI via subprocess.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "k17_pilot.py"
LEDGER_NAME = "fixture_ledger.jsonl"

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


def ledger_effects(state_dir: Path, op_id: str) -> list[dict]:
    ledger = state_dir / LEDGER_NAME
    if not ledger.exists():
        return []
    rows = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("operation_id") == op_id:
            rows.append(row)
    return rows


class K17PilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="k17_pilot_test_")
        self.addCleanup(self._tmp.cleanup)
        self.state = Path(self._tmp.name) / "state"

    # -- 1. normal run = exactly one effect ---------------------------------

    def test_normal_run_commits_exactly_one_effect(self) -> None:
        r = run_cli("run", "--normal", "--state-dir", str(self.state))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["status"], "APPLIED")
        self.assertTrue(out["executed"])
        op_id = out["operation_id"]
        self.assertRegex(op_id, r"^op_[0-9a-f]{64}$")

        effects = ledger_effects(self.state, op_id)
        self.assertEqual(len(effects), 1, "normal run must commit exactly one effect")
        self.assertEqual(effects[0]["effect"], "ledger_insert")
        self.assertEqual(effects[0]["operation_id"], op_id)

        # intent record exists, stores the exact bytes, and predates the effect
        intent_path = self.state / "intents" / f"{op_id}.json"
        self.assertTrue(intent_path.exists())
        record = json.loads(intent_path.read_text(encoding="utf-8"))
        self.assertEqual(record["intent_sha256"], hashlib.sha256(
            record["intent"].encode("utf-8")).hexdigest())
        self.assertEqual(
            "op_" + hashlib.sha256(record["intent"].encode("utf-8")).hexdigest(), op_id)

        v = run_cli("verify", "--state-dir", str(self.state))
        self.assertEqual(v.returncode, 0, v.stderr)
        vout = json.loads(v.stdout)
        self.assertEqual(vout["status"], "OK")
        self.assertEqual(vout["totals"]["effects"], 1)
        self.assertEqual(vout["operations"][0]["knowledge"], "APPLIED")

    # -- 2. crash run + replay = still exactly one effect -------------------

    def test_crash_then_replay_commits_exactly_one_effect(self) -> None:
        r1 = run_cli("run", "--crash-after-intent", "--state-dir", str(self.state))
        self.assertEqual(r1.returncode, 3, "simulated death must exit 3")
        out1 = json.loads(r1.stdout)
        self.assertEqual(out1["status"], "SIMULATED_DEATH_AFTER_INTENT")
        op_id = out1["operation_id"]
        self.assertEqual(ledger_effects(self.state, op_id), [],
                         "crash mode must not commit the effect")
        # intent survived the crash
        self.assertTrue((self.state / "intents" / f"{op_id}.json").exists())

        # replay: rerun with the same state + intent -> re-issue exactly once
        r2 = run_cli("run", "--normal", "--state-dir", str(self.state))
        self.assertEqual(r2.returncode, 0, r2.stderr)
        out2 = json.loads(r2.stdout)
        self.assertEqual(out2["status"], "APPLIED")
        self.assertEqual(out2["operation_id"], op_id, "replay must reuse the op id")

        effects = ledger_effects(self.state, op_id)
        self.assertEqual(len(effects), 1,
                         "crash + replay must still commit exactly one effect")

        v = run_cli("verify", "--state-dir", str(self.state))
        self.assertEqual(v.returncode, 0, v.stderr)
        vout = json.loads(v.stdout)
        self.assertEqual(vout["status"], "OK")
        op_row = vout["operations"][0]
        self.assertEqual(op_row["knowledge"], "APPLIED")
        self.assertEqual(op_row["effects"], 1)
        self.assertGreaterEqual(op_row["attempts"], 2,
                                "evidence needs at least two attempts (B.14)")

    # -- 3. double replay = zero new effects --------------------------------

    def test_double_replay_adds_no_effects(self) -> None:
        r1 = run_cli("run", "--normal", "--state-dir", str(self.state))
        self.assertEqual(r1.returncode, 0)
        op_id = json.loads(r1.stdout)["operation_id"]
        count_after_first = len(ledger_effects(self.state, op_id))
        self.assertEqual(count_after_first, 1)

        for _ in range(2):  # double replay
            r = run_cli("run", "--normal", "--state-dir", str(self.state))
            self.assertEqual(r.returncode, 0, r.stderr)
            out = json.loads(r.stdout)
            self.assertEqual(out["status"], "DEDUP_APPLIED")
            self.assertFalse(out["executed"], "replay must not execute again")
            self.assertEqual(out["operation_id"], op_id)

        self.assertEqual(len(ledger_effects(self.state, op_id)), count_after_first,
                         "double replay must add zero new effects")

        v = run_cli("verify", "--state-dir", str(self.state))
        self.assertEqual(v.returncode, 0)
        self.assertEqual(json.loads(v.stdout)["totals"]["effects"], 1)

    # -- 4. same operation id, different intent -> conflict, no dispatch ----

    def test_same_id_different_payload_conflicts_without_dispatch(self) -> None:
        forced = "op_" + hashlib.sha256(b"forced-identity").hexdigest()
        r1 = run_cli("run", "--normal", "--state-dir", str(self.state),
                     "--operation-id", forced, "--payload", "alpha")
        self.assertEqual(r1.returncode, 0)
        self.assertEqual(len(ledger_effects(self.state, forced)), 1)

        r2 = run_cli("run", "--normal", "--state-dir", str(self.state),
                     "--operation-id", forced, "--payload", "beta")
        self.assertEqual(r2.returncode, 2, "conflict must exit 2 without dispatch")
        self.assertEqual(json.loads(r2.stdout)["status"], "OPERATION_ID_CONFLICT")
        self.assertEqual(len(ledger_effects(self.state, forced)), 1,
                         "conflict must not dispatch a second effect")

    # -- 5. verifier catches a broken dedup adapter --------------------------

    def test_verify_rejects_duplicated_effect_row(self) -> None:
        r = run_cli("run", "--normal", "--state-dir", str(self.state))
        self.assertEqual(r.returncode, 0)
        op_id = json.loads(r.stdout)["operation_id"]

        # simulate a broken dedup adapter committing a second row
        broken = dict(ledger_effects(self.state, op_id)[0])
        broken["attempt_id"] = "att_" + "0" * 32  # a second, forged attempt
        with open(self.state / LEDGER_NAME, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(broken, sort_keys=True) + "\n")

        v = run_cli("verify", "--state-dir", str(self.state))
        self.assertEqual(v.returncode, 4, "verifier must reject duplicate effects")
        vout = json.loads(v.stdout)
        self.assertEqual(vout["status"], "VIOLATION")
        self.assertTrue(vout["violations"])

    # -- 6. crash-only state reports PENDING, not a violation ---------------

    def test_verify_reports_pending_for_crashed_unreplayed_op(self) -> None:
        r = run_cli("run", "--crash-after-intent", "--state-dir", str(self.state))
        self.assertEqual(r.returncode, 3)
        op_id = json.loads(r.stdout)["operation_id"]

        v = run_cli("verify", "--state-dir", str(self.state))
        self.assertEqual(v.returncode, 0)
        vout = json.loads(v.stdout)
        self.assertEqual(vout["status"], "OK")
        self.assertEqual(vout["operations"][0]["knowledge"], "PENDING")
        self.assertEqual(vout["operations"][0]["effects"], 0)
        self.assertEqual(vout["totals"]["intents"], 1)


if __name__ == "__main__":
    unittest.main()
