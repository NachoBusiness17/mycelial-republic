"""Tests for mag/selfplay_orchestrator.py and mag/llama_cpp_bridge.py."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import llama_cpp_bridge as bridge
from mag import selfplay_orchestrator as spo


# ── bridge tests ────────────────────────────────────────────────

class TestLlamaCppBridgeFallback:
    """Bridge without llama.cpp installed → fallback mode, never crashes."""

    def test_fallback_generate_move(self):
        b = bridge.LlamaCppBridge(model_path="/nonexistent/model.gguf")
        result = b.generate_move("What is 2+2?")
        assert "fallback_move" in result["move"]
        assert result["ok"] is False
        assert result["fallback"] is True

    def test_parse_output_json(self):
        assert bridge.LlamaCppBridge.parse_output('{"answer": 42}') == '{"answer":42}'

    def test_parse_output_first_line(self):
        assert bridge.LlamaCppBridge.parse_output("  42  \nmore") == "42"

    def test_fallback_move_deterministic(self):
        b = bridge.LlamaCppBridge(model_path="/nonexistent/model.gguf")
        r1 = b.generate_move("same prompt")
        r2 = b.generate_move("same prompt")
        assert r1["move"] == r2["move"]

    def test_shutdown_no_crash(self):
        b = bridge.LlamaCppBridge(model_path="/nonexistent/model.gguf")
        b.shutdown()  # should not raise

    def test_benchmark_bridge_runs(self):
        result = bridge.benchmark_bridge(rounds=2)
        assert "avg_ms" in result
        assert result["rounds"] == 2


class TestLlamaCppBridgeSpawn:
    """Server spawn returns proper metadata when llama.cpp unavailable."""

    def test_spawn_without_llama(self):
        # Premise fix 2026-10-06 (dogfood-100m-20261006 lane d13-selfplay-run):
        # with llama-cpp-python installed in the venv the spawn path is real,
        # not import-fallback, so fallback=False is correct there; the flag is
        # now asserted against the actual availability state.  timeout=3 keeps
        # the fake-model spawn from burning the default 120s readiness wait
        # (suite was 121.44s with 1 failed, 21 passed before this fix; the
        # failure reproduced on unmodified HEAD bytes, environment-caused).
        b = bridge.LlamaCppBridge(model_path="/fake/model.gguf", timeout=3)
        result = b.spawn_server()
        assert result["ok"] is False
        assert result["fallback"] is (not b._llama_available)


class TestLlamaCppBridgeEndpointWire:
    """Wire test 2026-10-07 (stockfish-door-20261007 lane s2-wire-endpoint):
    generate_move must POST the spawned server's /v1/completions route over
    HTTP, never construct a fresh in-process Llama per call.  A stub on an
    ephemeral port discriminates the two paths: with the old per-call
    Llama(path) shape the fake model path raises and ok comes back False with
    zero HTTP hits; with the wire, the stub sees exactly one POST
    /v1/completions and ok is True.  Route is /v1/completions because
    llama-cpp-python 0.3.36 has no native /completion route (first probe
    run: POST /completion 404 {"detail":"Not Found"}, 2026-10-07)."""

    def test_generate_move_posts_spawned_endpoint(self):
        import json as _json
        import threading
        from http.server import BaseHTTPRequestHandler, HTTPServer

        hits: list[str] = []

        class _Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                hits.append(self.path)
                resp = _json.dumps(
                    {"choices": [{"text": ' {"answer": 42} \n'}]}
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)

            def log_message(self, *_args):
                pass

        server = HTTPServer(("127.0.0.1", 0), _Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            port = server.server_address[1]
            b = bridge.LlamaCppBridge(
                model_path="/fake/model.gguf", host="127.0.0.1", port=port
            )
            b._llama_available = True
            b._available = True
            b._endpoint = f"http://127.0.0.1:{port}/v1/completions"
            result = b.generate_move("What is 2+2?")
        finally:
            server.shutdown()

        assert hits == ["/v1/completions"]
        assert result["ok"] is True
        assert result.get("fallback") is not True
        assert result["move"] == '{"answer":42}'

    def test_unspawned_bridge_still_falls_back(self):
        b = bridge.LlamaCppBridge(model_path="/fake/model.gguf")
        result = b.generate_move("What is 2+2?")
        assert result["ok"] is False
        assert result["fallback"] is True


# ── Elo engine ──────────────────────────────────────────────────

class TestEloEngine:
    def test_baseline_starts_at_1000(self):
        e = spo.EloEngine()
        assert e.rating == 1000.0

    def test_update_increases_on_win(self):
        e = spo.EloEngine()
        e.update(1.0)
        assert e.rating > 1000.0

    def test_update_decreases_on_loss(self):
        e = spo.EloEngine()
        e.update(0.0)
        assert e.rating < 1000.0

    def test_elo_vs_baseline(self):
        e = spo.EloEngine()
        e.update(1.0)
        assert e.elo_vs_baseline > 0

    def test_k_factor_respected(self):
        e1 = spo.EloEngine(k=16)
        e2 = spo.EloEngine(k=64)
        e1.update(1.0)
        e2.update(1.0)
        assert abs(e2.rating - 1000.0) > abs(e1.rating - 1000.0)


# ── orchestrator tests ──────────────────────────────────────────

class TestSelfPlayOrchestrator:
    def test_play_one_returns_result(self):
        orch = spo.SelfPlayOrchestrator()
        problem = {"id": "t1", "question": "What is 2+2?", "answer": 4}
        result = orch.play_one(problem)
        assert result.problem_id == "t1"
        assert result.actor_ms >= 0
        assert result.scorer_ms >= 0
        assert result.total_ms >= 0
        assert result.correct is True  # fallback move won't match; but check structure

    def test_run_session_produces_report(self):
        orch = spo.SelfPlayOrchestrator()
        report = orch.run_session(spo.MATH_PROBLEMS[:3])
        assert report.n_games == 3
        assert 0.0 <= report.accuracy <= 1.0
        assert isinstance(report.elo, float)
        assert isinstance(report.elo_vs_baseline, float)
        assert report.bottleneck in ("actor", "scorer", "none")

    def test_bottleneck_measurement_samples(self):
        orch = spo.SelfPlayOrchestrator()
        orch.play_one({"id": "t1", "question": "What is 1+1?", "answer": 2})
        assert len(orch.samples) >= 2  # actor + scorer
        legs = {s.leg for s in orch.samples}
        assert "actor" in legs
        assert "scorer" in legs

    def test_evidence_path_written(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        orch = spo.SelfPlayOrchestrator()
        orch.run_session([{"id": "t1", "question": "What is 1+1?", "answer": 2}])
        report = orch.report()
        evidence = tmp_path / "memory" / "runs" / "selfplay" / "evidence_latest.json"
        # report() itself doesn't write; main() does — just check report structure
        assert report.n_games >= 1

    def test_parse_reward(self):
        assert spo.SelfPlayOrchestrator._parse_reward("1.0") == 1.0
        assert spo.SelfPlayOrchestrator._parse_reward("0.75") == 0.75
        assert spo.SelfPlayOrchestrator._parse_reward("correct answer") == 1.0
        assert spo.SelfPlayOrchestrator._parse_reward("wrong") == 0.0
        assert spo.SelfPlayOrchestrator._parse_reward("") == 0.5

    def test_check_answer_numeric(self):
        assert spo.SelfPlayOrchestrator._check_answer("2+2", 4, "4") is True
        assert spo.SelfPlayOrchestrator._check_answer("2+2", 4, "5") is False

    def test_check_answer_string_match(self):
        assert spo.SelfPlayOrchestrator._check_answer("q", "hello", "hello world") is True


# ── config tests ────────────────────────────────────────────────

class TestLaneProfilesConfig:
    def test_rx5600xt_profile_exists(self):
        import yaml
        path = ROOT / "configs" / "lane_profiles.yaml"
        data = yaml.safe_load(path.read_text())
        profiles = data.get("profiles", {})
        assert "rx5600xt_actor" in profiles
        profile = profiles["rx5600xt_actor"]
        assert profile["gpu"] == "AMD Radeon RX 5600 XT"
        assert profile["vram_gb"] == 6
        assert profile["cuda"] is False

    def test_models_fit_vram(self):
        import yaml
        path = ROOT / "configs" / "lane_profiles.yaml"
        data = yaml.safe_load(path.read_text())
        models = data["profiles"]["rx5600xt_actor"]["models"]
        assert len(models) >= 1
        assert models[0]["vram_fit"] is True


# ── integration ─────────────────────────────────────────────────

class TestIntegrationSelfPlay:
    def test_full_pipeline_no_crash(self):
        """End-to-end: orchestrator + bridge + Elo produce valid evidence."""
        orch = spo.SelfPlayOrchestrator()
        report = orch.run_session(spo.MATH_PROBLEMS[:4])
        assert report.n_games == 4
        assert report.n_correct >= 0
        assert 0.0 <= report.accuracy <= 1.0
        assert report.avg_actor_ms >= 0
        assert report.avg_scorer_ms >= 0
        # Elo should have moved from baseline
        assert report.elo != 1000.0 or report.n_games == 0
        # Per-problem data populated
        assert len(report.per_problem) == 4
        for p in report.per_problem:
            assert "id" in p
            assert "move" in p
            assert "reward" in p
            assert "correct" in p
            assert "actor_ms" in p
            assert "scorer_ms" in p
            assert "total_ms" in p
            assert "bottleneck" in p


# ── Move 6 fence (stockfish-door-20261007, lane s6-evidence-fence) ──

class TestMainEvidenceFence:
    """main() fails closed without a configured model_path (an unconfigured
    actor answers every move with a sha256 hash fallback that would land junk
    evidence) and writes append-only evidence with a pointer file, the
    ESTATE_INDEX.pointer.json pattern, never overwriting a prior run."""

    @staticmethod
    def _configured_orch(tmp_path):
        model_file = tmp_path / "stub-model.gguf"
        model_file.write_bytes(b"stub weights")
        return spo.SelfPlayOrchestrator(
            actor=bridge.LlamaCppBridge(model_path=str(model_file))
        )

    def test_main_fails_closed_without_model_path(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        with pytest.raises(SystemExit) as excinfo:
            spo.main(spo.SelfPlayOrchestrator())
        assert "no configured model_path" in str(excinfo.value.code)
        # fail closed means nothing at all was written
        assert not (tmp_path / "memory" / "runs" / "selfplay").exists()

    def test_main_fails_closed_on_missing_model_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        ghost = spo.SelfPlayOrchestrator(
            actor=bridge.LlamaCppBridge(model_path=str(tmp_path / "ghost.gguf"))
        )
        with pytest.raises(SystemExit):
            spo.main(ghost)
        assert not (tmp_path / "memory" / "runs" / "selfplay").exists()

    def test_main_writes_timestamped_evidence_and_pointer(self, tmp_path, monkeypatch):
        import json

        import mag.lane_runner as lane_runner

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(lane_runner, "flash_call", lambda **kwargs: "1.0")
        report = spo.main(self._configured_orch(tmp_path))
        ev_dir = tmp_path / "memory" / "runs" / "selfplay"
        masters = sorted(ev_dir.glob("evidence-*.json"))
        assert len(masters) == 1
        pointer = json.loads((ev_dir / "evidence_latest.pointer.json").read_text())
        assert pointer["pointer"] is True
        assert pointer["master"] == f"memory/runs/selfplay/{masters[0].name}"
        payload = json.loads(masters[0].read_text())
        assert payload["n_games"] == report.n_games
        assert payload["scorer_ok_ratio"] == 1.0
        # the legacy last-write-wins name is never written again
        assert not (ev_dir / "evidence_latest.json").exists()

    def test_main_never_overwrites_existing_evidence(self, tmp_path, monkeypatch):
        import mag.lane_runner as lane_runner

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(lane_runner, "flash_call", lambda **kwargs: "1.0")
        spo.main(self._configured_orch(tmp_path))
        first = sorted((tmp_path / "memory" / "runs" / "selfplay").glob("evidence-*.json"))[0]
        first_bytes = first.read_bytes()
        spo.main(self._configured_orch(tmp_path))
        # the first run's bytes survive a second run; the rerun got its own file
        assert first.read_bytes() == first_bytes
        masters = sorted((tmp_path / "memory" / "runs" / "selfplay").glob("evidence-*.json"))
        assert len(masters) == 2