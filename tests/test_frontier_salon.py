"""tests for frontier_salon — the three frontier seats (ChatGPT + SuperGrok + V4-Pro) as ONE tandem
surface, saloning our own system into a new version. Deterministic $0 coordinator.

RIB (frozen spec):
  salon(question) -> dispatch the SAME question to each witness (chatgpt / supergrok / v4-pro),
      collect their answers, roshomon-combine into ONE new_version + consensus_invariant. Per-witness
      HONEST ok flags — a down/unreachable witness is reported, never fabricated. n_available+n_down.
  salon_project() -> the test: salon OUR OWN system as the subject. Always ok-shaped (ok may be
      False if all witnesses down, but never fabricates).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import frontier_salon as fs  # noqa: E402


def test_status_witnesses_and_honest_gate():
    st = fs.status()
    assert st["ok"] is True
    assert st["schema"] == "frontier_salon.v1"
    for w in ("chatgpt", "supergrok", "v4-pro"):
        assert w in st["witnesses"]
    # the honest gate is explicit: live salon needs the seats reachable (CDP/login)
    assert "CDP" in st["honest_gate"] or "login" in st["honest_gate"]


def test_salon_reports_honest_witnesses_never_fabricates(tmp_path, monkeypatch):
    monkeypatch.setattr(fs, "OUT", tmp_path)
    monkeypatch.setattr(
        fs,
        "_query_witness",
        lambda label, surface, question: {
            "surface": label, "seat": surface, "ok": False, "answer": "",
            "error": f"{label} intentionally down",
        },
    )
    r = fs.salon("salon this project", surface_filter=["chatgpt"])
    # n_witnesses matches the filter; ok reflects reachability (may be False if the seat is down)
    assert r["n_witnesses"] == 1
    assert r["ok"] in (True, False)
    assert r["n_available"] + r["n_down"] == r["n_witnesses"]
    for w in r["witnesses"]:
        assert w["ok"] in (True, False)
        # an unreachable witness has an error/empty answer; a reachable one has an answer
        if w["ok"]:
            assert w["answer"]
        else:
            assert w["error"] or not w["answer"]
    # the salon always produces a new_version shape (never crashes even with no witnesses)
    assert "new_version" in r and "consensus_invariant" in r


def test_salon_project_is_the_self_test(tmp_path, monkeypatch):
    monkeypatch.setattr(fs, "OUT", tmp_path)
    monkeypatch.setattr(
        fs,
        "_query_witness",
        lambda label, surface, question: {
            "surface": label, "seat": surface, "ok": True,
            "answer": f"{label} says build the shared transcript", "error": "",
        },
    )
    r = fs.salon_project()
    assert "consensus_invariant" in r and "new_version" in r
    assert "n_witnesses" in r


def test_salon_consensus_deterministic():
    # given the same fake witnesses, the shared-invariant is deterministic (token overlap)
    a = fs._shared_invariant([
        {"ok": True, "answer": "the swarm must evolve with the chain and the wave"},
        {"ok": True, "answer": "the chain evolves with the swarm toward the wave"},
    ])
    assert "evolve" in a or "chain" in a or "swarm" in a


def test_roundtable_shares_prior_turns_preserves_provenance_and_files(
        tmp_path, monkeypatch):
    from mag import agent_corpus, party_subchain, seat_steer

    out = tmp_path / "roundtables"
    corpus = tmp_path / "corpus"
    monkeypatch.setattr(fs, "OUT", out)
    monkeypatch.setattr(agent_corpus, "CORPUS_DIR", corpus)
    monkeypatch.setattr(agent_corpus, "AGENT_INDEX", corpus / "agents.json")
    monkeypatch.setattr(agent_corpus, "LEDGERS", corpus / "ledgers")
    monkeypatch.setattr(
        party_subchain, "mount", lambda **_kwargs: {"ok": True, "transcript": "nothing yet"}
    )
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})
    prompts = []

    def fake_send(surface, message, *, max_wait_s=90, record_subchain=True):
        prompts.append((surface, message, max_wait_s))
        assert record_subchain is False
        n = len(prompts)
        return {
            "ok": True,
            "requested_surface": surface,
            "surface": seat_steer.resolve_surface(surface),
            "driver": "fake-driver",
            "answer": (
                f"POSITION: position {n}\n"
                f"CHALLENGE: challenge {n}\n"
                f"NOVEL DELTA: mechanism {n}\n"
                f"TEST: falsify mechanism {n}"
            ),
            "report": f"fake-{n}.json",
        }

    monkeypatch.setattr(seat_steer, "send", fake_send)
    r = fs.roundtable(
        "How should the seats communicate?",
        why="one seat stalled on the transcript mechanism",
        baseline={"surface": "chatgpt", "answer": "use the shared transcript"},
        participants=["chatgpt", "supergrok", "v4-pro"],
        rounds=2,
    )

    assert r["ok"] is True
    assert r["n_contributions"] == 6
    assert r["n_available"] == 6 and r["n_down"] == 0
    assert [row["label"] for row in r["contributions"][:3]] == [
        "chatgpt", "supergrok", "v4-pro"
    ]
    assert len({row["message_id"] for row in r["contributions"]}) == 6
    assert {row["context_id"] for row in r["contributions"]} == {r["roundtable_id"]}
    assert r["contributions"][1]["surface"] == "grok"
    assert "POSITION: position 1" in prompts[1][1]
    assert "POSITION: position 3" in prompts[3][1]
    assert len(r["novel_deltas"]) == 6 and len(r["tests"]) == 6
    assert Path(r["artifact"]).is_file()
    assert (corpus / "ledgers" / "gpt.jsonl").is_file()
    assert (corpus / "ledgers" / "grokbot.jsonl").is_file()
    assert (corpus / "ledgers" / "deepseek.jsonl").is_file()


def test_roundtable_keeps_down_seat_and_continues(tmp_path, monkeypatch):
    from mag import party_subchain, seat_steer

    monkeypatch.setattr(fs, "OUT", tmp_path)
    monkeypatch.setattr(
        party_subchain, "mount", lambda **_kwargs: {"ok": True, "transcript": "nothing yet"}
    )
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})

    def fake_send(surface, message, *, max_wait_s=90, record_subchain=True):
        assert record_subchain is False
        if surface == "grok":
            return {"ok": False, "surface": "grok", "error": "window unavailable"}
        return {"ok": True, "surface": seat_steer.resolve_surface(surface),
                "answer": "POSITION: proceed\nNOVEL DELTA: relay\nTEST: visible prior turn"}

    monkeypatch.setattr(seat_steer, "send", fake_send)
    monkeypatch.setattr("mag.agent_corpus.log_chat", lambda *_args, **_kwargs: {"ok": True})
    r = fs.roundtable("Keep dissent", why="dissent stress-test",
                      baseline={"surface": "chatgpt", "answer": "proceed"},
                      participants=["chatgpt", "supergrok", "v4-pro"],
                      rounds=1)
    assert r["ok"] is True
    assert r["n_available"] == 2 and r["n_down"] == 1
    down = r["contributions"][1]
    assert down["label"] == "supergrok" and down["ok"] is False
    assert down["error"] == "window unavailable"
    assert "supergrok | grok | round 1 | down" in r["contributions"][2]["prompt"]


def test_roundtable_huang_gate_blocks_escalation(tmp_path, monkeypatch):
    """Q-011 huang gate: a roundtable escalation requires a stated why plus a single-seat
    baseline; each refusal fires BEFORE any seat is dispatched (sends stays empty), and a
    gated call that satisfies the gate dispatches and echoes the audit fields."""
    from mag import party_subchain, seat_steer

    monkeypatch.setattr(fs, "OUT", tmp_path)
    monkeypatch.setattr(
        party_subchain, "mount", lambda **_kwargs: {"ok": True, "transcript": "nothing yet"}
    )
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})
    sends: list[tuple[str, str]] = []

    def fail_send(surface, message, *, max_wait_s=90, record_subchain=True):
        sends.append((surface, message))
        raise AssertionError("huang gate must block before any seat dispatch")

    monkeypatch.setattr(seat_steer, "send", fail_send)

    no_why = fs.roundtable("escalate this", record=False)
    assert no_why["ok"] is False
    assert "huang gate" in no_why["error"] and "why" in no_why["error"]
    assert no_why["gate"] == "huang.v1" and sends == []

    why_only = fs.roundtable("escalate this", why="one seat stalled on the mechanism",
                             record=False)
    assert why_only["ok"] is False
    assert "huang gate" in why_only["error"] and "baseline" in why_only["error"]
    assert why_only["gate"] == "huang.v1" and sends == []

    partial = fs.roundtable("escalate this", why="one seat stalled",
                            baseline={"surface": "chatgpt"}, record=False)
    assert partial["ok"] is False
    assert "huang gate" in partial["error"] and "baseline" in partial["error"]
    assert "seat_steer.send" in partial["error"]
    assert sends == []

    # gate satisfied -> dispatch happens; the result echoes the why + baseline for the artifact
    monkeypatch.setattr(seat_steer, "send", lambda surface, message, *, max_wait_s=90,
                        record_subchain=True: {
                            "ok": True, "surface": surface,
                            "answer": "POSITION: proceed\nNOVEL DELTA: relay\nTEST: prior turn"})
    monkeypatch.setattr("mag.agent_corpus.log_chat", lambda *_args, **_kwargs: {"ok": True})
    ok = fs.roundtable("escalate this", why="one seat stalled on the mechanism",
                       baseline={"surface": "chatgpt", "answer": "use the relay"},
                       participants=["chatgpt"], rounds=1, record=False)
    assert ok["ok"] is True and ok["n_contributions"] == 1
    assert ok["why"] == "one seat stalled on the mechanism"
    assert ok["baseline"] == {"surface": "chatgpt", "answer": "use the relay"}
    assert ok["gate"] == "huang.v1"


def test_roundtable_is_bounded():
    r = fs.roundtable("x", participants=[], rounds=99, record=False)
    assert r["ok"] is False and "participant" in r["error"]
