from __future__ import annotations

import mag.lm_studio as lm_studio


def test_bionic_uses_configured_localhost_server() -> None:
    assert lm_studio.BASE == "http://127.0.0.1:1234/v1"


def test_models_reads_openai_compatible_payload(monkeypatch) -> None:
    monkeypatch.setattr(
        lm_studio,
        "_req",
        lambda method, path, body=None, timeout=10: {
            "object": "list",
            "data": [{"id": "text-embedding-nomic-embed-text-v1.5"}],
        },
    )

    result = lm_studio.models()

    assert result["ok"] is True
    assert result["models"] == ["text-embedding-nomic-embed-text-v1.5"]


def test_chat_does_not_guess_an_embedding_model(monkeypatch) -> None:
    monkeypatch.setattr(
        lm_studio,
        "_req",
        lambda method, path, body=None, timeout=10: {
            "object": "list",
            "data": [{"id": "text-embedding-nomic-embed-text-v1.5"}],
        },
    )

    result = lm_studio.chat("hello")

    assert result["ok"] is False
    assert "no loaded chat model" in result["error"]
