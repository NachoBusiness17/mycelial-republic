"""tests for scripts/wave_driver.py v0 skeleton (stdlib only).

Covers: (1) ground-row hash matches mag.grounding_wave._row_hash exactly
(schema match); (2) halt-not-hammer escalation on a lane with 2 falls, with
zero dispatch; (3) the steer verify-gate LOUD failure on a tampered COPY of
steers.jsonl (real steers.jsonl never touched); (4) single-tick subprocess
runs clean and appends a chain-valid row.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER = os.path.join(ROOT, "scripts", "wave_driver.py")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import wave_driver  # noqa: E402


class TestGroundRowSchema(unittest.TestCase):
    def test_hash_matches_canonical_module(self):
        from mag.grounding_wave import _row_hash as canonical
        row = {"prev": "a" * 64, "ts": "2026-09-11T00:00:00Z", "claim": "c",
               "verdict": "SUPPORTED", "evidence": "watch/steers.jsonl",
               "note": "n", "seat": wave_driver.SEAT, "witness": "w",
               "ttl_s": 900}
        self.assertEqual(wave_driver._row_hash_local(row), canonical(row))

    def test_extra_ttl_field_outside_hashed_keys(self):
        a = wave_driver._row_hash_local(
            {"prev": "b" * 64, "ts": "t", "claim": "c", "verdict": "UNPROVEN",
             "evidence": "e", "note": "", "seat": "s", "witness": "w"})
        b = wave_driver._row_hash_local(
            {"prev": "b" * 64, "ts": "t", "claim": "c", "verdict": "UNPROVEN",
             "evidence": "e", "note": "", "seat": "s", "witness": "w",
             "ttl_s": 900})
        self.assertEqual(a, b, "ttl_s must sit outside the v3 hashed key set")


class TestJudge(unittest.TestCase):
    def test_two_falls_escalates_no_dispatch(self):
        tele = {"lanes": [{"lane": 0, "falls": 2}, {"lane": 1, "falls": 0}]}
        esc = wave_driver.judge(tele, [], [])
        self.assertEqual(len(esc), 1)
        self.assertEqual(esc[0]["lane"], 0)
        self.assertEqual(esc[0]["reason"], "halt-not-hammer")
        self.assertIn("no dispatch", esc[0]["action"])

    def test_clean_telemetry_no_escalation(self):
        tele = {"lanes": [{"lane": 0, "falls": 1}, {"lane": 1, "falls": 0}]}
        self.assertEqual(wave_driver.judge(tele, [], []), [])


class TestVerifyGate(unittest.TestCase):
    def _clean_copy(self, src: str, tmpdir: str) -> str:
        dst = os.path.join(tmpdir, "steers_clean.jsonl")
        with open(src, "r", encoding="utf-8") as fh, \
                open(dst, "w", encoding="utf-8", newline="\n") as out:
            for line in fh:
                if "FORGED-TEST" not in line:
                    out.write(line)
        return dst

    def test_gate_fails_loud_on_tampered_copy(self):
        real = os.path.join(ROOT, "watch", "steers.jsonl")
        with tempfile.TemporaryDirectory() as tmp:
            clean = self._clean_copy(real, tmp)
            with open(clean, "r", encoding="utf-8") as fh:
                rows = [json.loads(l) for l in fh if l.strip()]
            self.assertTrue(all("sig" in r for r in rows), "precondition: clean copy all signed")
            rows[0]["text"] = rows[0]["text"] + " TAMPERED-BY-LANE-3-TEST"
            tam = os.path.join(tmp, "steers_tampered.jsonl")
            with open(tam, "w", encoding="utf-8", newline="\n") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False,
                                        separators=(",", ":")) + "\n")
            ok, out = wave_driver.verify_gate(tam, os.path.join(ROOT, "state", ".steer_key"))
            self.assertFalse(ok, "tampered copy must fail the gate")
            self.assertIn("FAIL", out)

    def test_gate_passes_on_clean_copy(self):
        real = os.path.join(ROOT, "watch", "steers.jsonl")
        with tempfile.TemporaryDirectory() as tmp:
            clean = self._clean_copy(real, tmp)
            ok, out = wave_driver.verify_gate(clean, os.path.join(ROOT, "state", ".steer_key"))
            self.assertTrue(ok, f"clean copy should pass: {out}")


class TestSingleTickSubprocess(unittest.TestCase):
    def test_tick_appends_chain_valid_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            ground = os.path.join(tmp, "GROUNDING_WAVE.jsonl")
            state = os.path.join(tmp, "state.json")
            for _ in range(2):  # run --tick semantics twice against a fresh ledger
                proc = subprocess.run(
                    [sys.executable, DRIVER, "--tick", "--ground", ground,
                     "--state", state],
                    capture_output=True, text=True, cwd=ROOT, timeout=120)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn("[RECORD] ground row posted", proc.stdout)
                self.assertIn("WAVE_DRIVER v0 TICK", proc.stdout)
            rows = [json.loads(l) for l in open(ground, encoding="utf-8") if l.strip()]
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1]["prev"], rows[0]["hash"], "row 2 chains to row 1")
            self.assertEqual(rows[0]["seat"], wave_driver.SEAT)
            self.assertEqual(rows[0]["ttl_s"], wave_driver.HEARTBEAT_TTL_S)
            from mag.grounding_wave import _row_hash
            for r in rows:
                self.assertEqual(_row_hash(r), r["hash"], "hash must match canonical v3 formula")


if __name__ == "__main__":
    unittest.main()
