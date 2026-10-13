from __future__ import annotations


def test_meter_captures_dedupes_and_reports(tmp_path):
    from mag.honest_cache_meter import CacheMeter

    meter = CacheMeter(str(tmp_path / "meter.db"))
    payload = {
        "id": "resp-1",
        "usage": {
            "prompt_tokens": 100,
            "prompt_tokens_details": {"cached_tokens": 40},
            "completion_tokens": 10,
        },
    }
    first = meter.capture("openai", "gpt-5", payload, ts="2026-09-01T01:02:03Z")
    second = meter.capture("openai", "gpt-5", payload, ts="2026-09-01T01:02:04Z")
    report = meter.report("2026-09-01")
    meter.close()

    assert first["ok"] and not first["deduped"]
    assert second["deduped"]
    assert report["responses"] == 1
    assert report["cache_read_tokens"] == 40
    assert report["output_tokens"] == 10


def test_agent_state_commit_hash_excludes_its_own_field(tmp_path, monkeypatch):
    import mag.agent_state as ast

    monkeypatch.setattr(ast, "STATE_DIR", tmp_path / "agent_state")
    monkeypatch.setattr(ast, "VERSIONS", tmp_path / "agent_state" / "versions")
    monkeypatch.setattr(ast, "CHAIN", tmp_path / "agent_state" / "chain.jsonl")
    monkeypatch.setattr(ast, "TIP", tmp_path / "agent_state" / "tip.json")
    monkeypatch.setattr(ast, "LATEST_JSON", tmp_path / "agent_state" / "LATEST.json")
    monkeypatch.setattr(ast, "LATEST_MD", tmp_path / "agent_state" / "LATEST.md")
    result = ast.commit_state({"one_line": "lock test"}, label="test")
    state = ast.load_latest()

    assert result["ok"]
    assert ast.content_commit_hex(state) == state["content_commit"]["hex"]
