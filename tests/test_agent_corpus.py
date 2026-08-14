"""tests for agent_corpus — durable per-agent knowledge base, pure stdlib, no deps, feeds the world.

RIB (frozen spec):
  register_agent() -> add an agent or version to the index (bare-metal file write).
  log_chat()       -> log one agent chat (with version) as a content-addressed knot in the agent's
                      ledger. Idempotent: same agent+version+text -> same leaf -> never duplicated.
  corpus()         -> read the durable per-agent knowledge base (per-agent counts + chats).
  fold_into_world() -> fold NEW per-agent knowledge into the game world as verkle knots (idempotent).

Contract: PURE STDLIB (json/Path/hashlib/datetime only) — the "prepare to have nothing" rule. Runs on
a machine with nothing but Python. Content-addressed, portable, survives losing all remote compute.

Stateless-correct: point module paths at tmp_path and exercise the real functions; no monkeypatch.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import agent_corpus  # noqa: E402


def test_registers_agent_and_version(tmp_path):
    agent_corpus.CORPUS_DIR = tmp_path
    agent_corpus.LEDGERS = tmp_path / "ledgers"
    agent_corpus.AGENT_INDEX = tmp_path / "agents.json"
    r = agent_corpus.register_agent("newagent", version="v1")
    assert r["ok"] is True
    assert "v1" in r["versions"]


def test_log_chat_idempotent(tmp_path):
    agent_corpus.CORPUS_DIR = tmp_path
    agent_corpus.LEDGERS = tmp_path / "ledgers"
    agent_corpus.AGENT_INDEX = tmp_path / "agents.json"
    r1 = agent_corpus.log_chat("grokbot", "grok-4.5", "hello grok")
    assert r1["logged"] is True
    assert r1["leaf"]
    # same chat again -> deduped, not logged twice
    r2 = agent_corpus.log_chat("grokbot", "grok-4.5", "hello grok")
    assert r2["deduped"] is True
    assert r2["logged"] is False
    # different version -> different leaf -> logged
    r3 = agent_corpus.log_chat("grokbot", "grok-desktop", "hello grok")
    assert r3["logged"] is True


def test_log_requires_text():
    r = agent_corpus.log_chat("grokbot", "grok-4.5", "   ")
    assert r["ok"] is False


def test_corpus_counts_per_agent(tmp_path):
    agent_corpus.CORPUS_DIR = tmp_path
    agent_corpus.LEDGERS = tmp_path / "ledgers"
    agent_corpus.AGENT_INDEX = tmp_path / "agents.json"
    agent_corpus.log_chat("gpt", "gpt-4o", "chat one")
    agent_corpus.log_chat("gpt", "gpt-4o", "chat two")
    agent_corpus.log_chat("cursor", "cursor-agent", "cursor chat")
    c = agent_corpus.corpus()
    assert c["ok"] is True
    assert c["total_chats"] == 3
    assert c["per_agent_chat_count"]["gpt"] == 2
    assert c["per_agent_chat_count"]["cursor"] == 1


def test_fold_into_world_idempotent(tmp_path):
    agent_corpus.CORPUS_DIR = tmp_path
    agent_corpus.LEDGERS = tmp_path / "ledgers"
    agent_corpus.AGENT_INDEX = tmp_path / "agents.json"
    # point game_world at a tmp world file so we don't touch the real world during tests
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    agent_corpus.log_chat("grokbot", "grok-4.5", "the world learns about grok")
    f1 = agent_corpus.fold_into_world(agent="grokbot", limit=8)
    assert f1["ok"] is True
    assert f1["n_folded"] >= 1
    # fold again -> nothing new (idempotent, world already holds the knots)
    f2 = agent_corpus.fold_into_world(agent="grokbot", limit=8)
    assert f2["n_folded"] == 0


def test_seed_major_players_grounded_and_idempotent(tmp_path):
    agent_corpus.CORPUS_DIR = tmp_path
    agent_corpus.LEDGERS = tmp_path / "ledgers"
    agent_corpus.AGENT_INDEX = tmp_path / "agents.json"
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    r = agent_corpus.seed_major_players(fold=True)
    assert r["ok"] is True
    assert r["seeded"] >= 5  # the major players are in the corpus
    assert r["logged_new"] >= 1
    assert r["honesty"]  # honesty field present
    # every major player has a verified-log source (grounded, not invented)
    for p in agent_corpus.MAJOR_PLAYERS:
        assert p.get("source") == "verified-log"
        assert "VERIFIED" in p.get("text", "")  # grounded markers, never fabricated
