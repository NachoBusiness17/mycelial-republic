"""Seed law tests — stdlib unittest, zero installs: python -m unittest discover -s tests"""
import sys, unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engines"))


class CookerWindow(unittest.TestCase):
    """The month-edge case that crashed cooker.py:55 in V1 (ractor probe)."""

    def test_daily_hour0_rolls_back_across_month(self):
        import cooker
        now = datetime(2026, 10, 1, 0, 30, tzinfo=timezone.utc)
        ws = cooker.window_start({"kind": "daily_utc", "hour": 0}, now)
        self.assertEqual((ws.month, ws.day, ws.hour), (10, 1, 0))

    def test_daily_hour1_before_open_rolls_back_month_edge(self):
        """The V1 crash regression: hour=1 at 00:30 on the 1st must roll back
        to the previous day WITHOUT 'day is out of range'."""
        import cooker
        now = datetime(2026, 10, 1, 0, 30, tzinfo=timezone.utc)
        ws = cooker.window_start({"kind": "daily_utc", "hour": 1}, now)
        self.assertEqual((ws.month, ws.day, ws.hour), (9, 30, 1))

    def test_daily_hour1_month_edge(self):
        import cooker
        now = datetime(2026, 10, 1, 1, 30, tzinfo=timezone.utc)
        ws = cooker.window_start({"kind": "daily_utc", "hour": 1}, now)
        self.assertEqual((ws.month, ws.day, ws.hour), (10, 1, 1))

    def test_weekly_backwards_and_forwards(self):
        import cooker
        r = {"kind": "weekly_utc", "weekday": 5, "hour": 2, "minute": 19}  # Sat
        thu = datetime(2026, 9, 24, 12, 0, tzinfo=timezone.utc)
        self.assertEqual((cooker.window_start(r, thu).weekday(), cooker.window_start(r, thu).day), (5, 19))
        nxt = cooker.next_reset(r, thu)
        self.assertEqual((nxt.weekday(), nxt.day), (5, 26))


class RelayDecisions(unittest.TestCase):
    """Exact-token law: 'deny' must never approve (it contains 'y')."""

    def test_decisions(self):
        from phone_relay import _decide
        cases = {"deny": "deny", "no": "deny", "n": "deny", "y": "approve",
                 "yes": "approve", "approve": "approve", "maybe later": None,
                 "are you sure?": None, "why not": None, "yes no": "deny"}
        for words, want in cases.items():
            self.assertEqual(_decide(words), want, words)


class Seal(unittest.TestCase):
    def test_manifest_covers_itself_and_files(self):
        rows = [r for r in (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines() if r.strip()]
        import hashlib
        for row in rows:
            want, _, rel = row.partition("  ")
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), want, rel)


if __name__ == "__main__":
    unittest.main()
