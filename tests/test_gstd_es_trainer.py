"""tests for the gstd es mesh trainer skeleton (run ml-moonshot-20261007, lane
ml6-es-mesh-trainer): the no-gradient wire contract (only fitness scores enter
the update and only scores bank), the antithetic sampler, the score-only mean
update, the deterministic cue render, the byte-cost model, and the inherited
fail-closed wallet gate. Spec: docs/ref/GSTD_ES_MESH_TRAINER_SPEC.md; drop:
watch/inbox/LINKS.jsonl seq 1791377243089599; pattern parent:
tools/gstd_fleet_provider.py.

No test touches the network: every wire verb is tools.gstd_fleet_provider's,
and the tests stub it at the module boundary; the gate-closed test asserts
zero submit attempts.
"""
from __future__ import annotations

import hashlib
import json

import pytest

from tools import gstd_es_trainer as ges
from tools import gstd_fleet_provider as gfp


@pytest.fixture(autouse=True)
def _offline_home(tmp_path, monkeypatch):
    # Default world: gate closed (P0 wallets owed), ledgers in tmp.
    monkeypatch.setattr(gfp, "_env", lambda name: "")
    monkeypatch.setattr(ges, "ES_RUNS", tmp_path)
    monkeypatch.setattr(ges, "STATE_PATH", tmp_path / "state.json")
    monkeypatch.setattr(ges, "ROUNDS_LEDGER", tmp_path / "es_rounds.jsonl")


# -- the gate ---------------------------------------------------------------

def test_round_blocked_when_gate_closed_and_never_submits(monkeypatch):
    calls = {"n": 0}

    def boom(*a, **k):
        calls["n"] += 1
        raise AssertionError("network touched behind a closed gate")

    monkeypatch.setattr(gfp, "submit_task", boom)
    out = ges.es_round("What is 17 x 23?", "391")
    assert out.get("blocked") is True and not out.get("ok")
    assert "WALLET GATE BLOCKED" in out["why"]
    assert calls["n"] == 0


def test_main_round_returns_gate_exit_when_closed():
    assert ges.main(["--round", "--task", "t", "--answer", "a"]) == ges.GATE_EXIT == 3


def test_status_and_cost_run_offline(capsys):
    assert ges.main(["--status"]) == 0
    assert "WALLET GATE: BLOCKED" in capsys.readouterr().out
    assert ges.main(["--cost"]) == 0
    cost = json.loads(capsys.readouterr().out)
    assert cost["round_total_bytes"] > 0


# -- genome render + routing -------------------------------------------------

def test_render_prompt_deterministic_positive_weights_only():
    v = [0.9, -1.0, 0.3, 0.5, 0.0, 0.0, 0.0, 0.0]
    a = ges.render_prompt("What is 17 x 23?", v)
    b = ges.render_prompt("What is 17 x 23?", list(v))
    assert a == b  # same vector, same bytes
    assert "Think step by step" in a      # heaviest positive first
    assert "Verify your answer" in a      # mid weight included
    assert "maximally terse" not in a     # negative weight excluded
    assert a.index("Think step by step") > len("What is 17 x 23?")


def test_route_device_is_stable_argmax():
    assert ges.route_device(["bob", "desktop", "pixel"], [0.1, 2.0, -1.0]) == "desktop"
    assert ges.route_device(["bob", "desktop", "pixel"], [0.0, 0.0, 0.0]) == "bob"


# -- the ES core -------------------------------------------------------------

def test_sample_perturbations_antithetic_deterministic_paired():
    e1 = ges.sample_perturbations(7, dim=8, pop=6)
    e2 = ges.sample_perturbations(7, dim=8, pop=6)
    assert e1 == e2
    assert ges.sample_perturbations(8, dim=8, pop=6) != e1
    assert len(e1) == 6 and all(len(x) == 8 for x in e1)
    for i in range(0, 6, 2):
        assert e1[i] == [-x for x in e1[i + 1]]  # antithetic pair
        pair_sum = [a + b for a, b in zip(e1[i], e1[i + 1])]
        assert all(x == 0.0 for x in pair_sum)   # pair cancels per dim
    assert sum(sum(x) for x in e1) == pytest.approx(0.0)  # population sums zero
    with pytest.raises(ValueError):
        ges.sample_perturbations(7, dim=8, pop=5)


def test_update_mean_moves_toward_high_fitness_perturbation():
    mean, delta = ges.update_mean([0.0, 0.0], [[1.0, 0.0], [-1.0, 0.0]],
                                  [1.0, 0.0])
    # centered fitness [0.5, -0.5]: grad dim0 = 0.5*1 + (-0.5)*(-1) = 1.0
    # step = alpha/(n*sigma) * 1.0 = 0.25/(2*0.5) = 0.25
    assert mean[0] == pytest.approx(0.25)
    assert mean[1] == 0.0
    assert delta == pytest.approx(0.25)


def test_update_mean_no_scores_means_no_move():
    mean, delta = ges.update_mean([0.1, 0.2], [[1.0, 1.0]], [])
    assert mean == [0.1, 0.2] and delta == 0.0
    mean2, delta2 = ges.update_mean([0.1, 0.2], [], [1.0])
    assert mean2 == [0.1, 0.2] and delta2 == 0.0


def test_fitness_success_and_cost_term():
    assert ges.fitness("391", "391") == 1.0
    assert ges.fitness("The answer is 391.", "391") == 1.0
    assert ges.fitness("I do not know", "391") == 0.0
    assert ges.fitness("391", "391", cost_norm=0.2) == pytest.approx(0.8)


# -- the byte-cost model ------------------------------------------------------

def test_round_cost_bytes_matches_construction():
    c = ges.round_cost_bytes()
    assert c["tasks"] == 6 and c["nodes"] == 3
    assert c["per_task_bytes"] == (c["submit_bytes_per_task"]
                                   + c["poll_bytes_per_task"]
                                   + c["status_bytes_per_task"])
    assert c["round_total_bytes"] == c["per_task_bytes"] * c["tasks"]
    assert c["bytes_per_node"] == c["round_total_bytes"] // 3


def test_round_cost_bytes_pinned_defaults():
    # Pinned so the spec's headline number cannot drift silently (values read
    # off the module's own --cost output, 2026-10-07): cue render = 119
    # expected chars (238 fragment+separator chars, halved); completion
    # default 276 per the fleet spec example
    # (docs/ref/GSTD_FLEET_LANE_SPEC.md section 5).
    assert ges.cue_chars_expected() == 119
    c = ges.round_cost_bytes()
    assert c["submit_bytes_per_task"] == 323
    assert c["poll_bytes_per_task"] == 372
    assert c["status_bytes_per_task"] == 222
    assert c["per_task_bytes"] == 917
    assert c["round_total_bytes"] == 5502


# -- the gated round over stubbed wire ----------------------------------------

def _wire(monkeypatch, completions_by_call=None):
    """Stub the fleet provider's wire: submit assigns ids, poll returns the
    canned completion. Records every submit prompt for the wire contract."""
    sent = {"prompts": [], "devices": [], "n": 0}
    ev = hashlib.sha256(b"391").hexdigest()

    def fake_submit(*, work_id, prompt, task_shape, device):
        sent["n"] += 1
        sent["prompts"].append(prompt)
        sent["devices"].append(device)
        return {"ok": True, "task_id": "tid-" + work_id, "http": 200,
                "device": device}

    def fake_poll(task_id, **k):
        return {"ok": True, "task_id": task_id, "http": 200,
                "completion": "391", "evidence_hash": ev,
                "model": "gemma:2b"}

    monkeypatch.setattr(gfp, "submit_task", fake_submit)
    monkeypatch.setattr(gfp, "poll_task", fake_poll)
    monkeypatch.setattr(gfp, "_env",
                        lambda name: "gstdwallet1" if name == "GSTD_WALLET_DESKTOP" else "")
    return sent, ev


def test_round_happy_path_scores_only_banks_and_advances(tmp_path, monkeypatch):
    sent, ev = _wire(monkeypatch)
    monkeypatch.setattr(gfp, "MESH_RUNS", tmp_path / "mesh")
    monkeypatch.setattr(gfp, "MESH_LEDGER", tmp_path / "mesh" / "mesh_ledger.jsonl")
    out = ges.es_round("What is 17 x 23?", "391")
    assert out["ok"] and out["n_fired"] == 6 and out["n_scored"] == 6
    # wire contract: every outbound prompt carried the rendered genome
    assert len(sent["prompts"]) == 6 and all("17 x 23" in p for p in sent["prompts"])
    # devices round-robin over wallet devices
    assert set(sent["devices"]) == {"desktop"}
    # round row banks scores + evidence hashes, never completions
    lines = (tmp_path / "es_rounds.jsonl").read_text(encoding="utf-8").splitlines()
    row = json.loads(lines[-1])
    assert row["schema"] == "es_round_row.v1" and row["gen"] == 0
    assert row["n_scored"] == 6 and len(row["scores"]) == 6
    assert all(s["evidence_hash"] == ev for s in row["scores"])
    assert all(s["fitness"] == 1.0 for s in row["scores"])
    row_text = lines[-1]
    assert "completion" not in row_text and "391" not in row_text
    # the mesh ledger got the gps rows (completion lives THERE, once)
    mesh_lines = (tmp_path / "mesh" / "mesh_ledger.jsonl") \
        .read_text(encoding="utf-8").splitlines()
    assert len(mesh_lines) == 6
    mesh_row = json.loads(mesh_lines[-1])
    assert mesh_row["provider"] == "gstd-mesh:desktop"
    # state advanced
    st = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert st["gen"] == 1 and len(st["mean"]) == 8
    # all six fitnesses equal (no variance): centered scores are zero,
    # so the mean must not move (the honest no-signal no-move property)
    assert all(abs(x) < 1e-9 for x in st["mean"])


def test_round_zero_variance_keeps_mean_put(tmp_path, monkeypatch):
    # Same completion everywhere = no signal: ES must not move the mean.
    sent, _ = _wire(monkeypatch)
    out = ges.es_round("q", "391")
    assert out["mean_delta_l2"] == 0.0


def test_round_mixed_fitness_moves_mean_toward_winner(tmp_path, monkeypatch):
    ev = hashlib.sha256(b"391").hexdigest()
    sent = {"n": 0}

    def fake_submit(*, work_id, prompt, task_shape, device):
        sent["n"] += 1
        return {"ok": True, "task_id": "tid-" + work_id, "http": 200,
                "device": device}

    def fake_poll(task_id, **k):
        # pair 0 eps (even index) correct, its antithetic twin wrong:
        # only evals e00 and e01 differ; the rest neutral 0.5-text (wrong)
        idx = int(task_id.split("-e")[-1])
        text = "391" if idx == 0 else "nope"
        return {"ok": True, "task_id": task_id, "http": 200,
                "completion": text, "evidence_hash":
                    hashlib.sha256(text.encode()).hexdigest(),
                "model": "gemma:2b"}

    monkeypatch.setattr(gfp, "submit_task", fake_submit)
    monkeypatch.setattr(gfp, "poll_task", fake_poll)
    monkeypatch.setattr(gfp, "_env",
                        lambda name: "gstdwallet1" if name == "GSTD_WALLET_DESKTOP" else "")
    out = ges.es_round("q", "391")
    assert out["ok"] and out["n_scored"] == 6 and out["mean_delta_l2"] > 0.0
    lines = (tmp_path / "es_rounds.jsonl").read_text(encoding="utf-8").splitlines()
    row = json.loads(lines[-1])
    fits = {s["eps_index"]: s["fitness"] for s in row["scores"]}
    assert fits[0] == 1.0 and fits[1] == 0.0
    # st carries the moved mean
    st = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert any(abs(x) > 0 for x in st["mean"])


def test_round_failure_banks_eval_row_never_retries(tmp_path, monkeypatch):
    ev = hashlib.sha256(b"391").hexdigest()
    calls = {"submit": 0, "poll": 0}

    def fake_submit(*, work_id, prompt, task_shape, device):
        calls["submit"] += 1
        if work_id == "es-g000-e00":
            return {"ok": False, "why": "submit failed: HTTP 500 boom"}
        return {"ok": True, "task_id": "tid-" + work_id, "http": 200,
                "device": device}

    def fake_poll(task_id, **k):
        calls["poll"] += 1
        if task_id == "tid-es-g000-e01":
            return {"ok": False, "task_id": task_id, "why": "poll window expired"}
        return {"ok": True, "task_id": task_id, "http": 200,
                "completion": "391", "evidence_hash": ev, "model": "gemma:2b"}

    monkeypatch.setattr(gfp, "submit_task", fake_submit)
    monkeypatch.setattr(gfp, "poll_task", fake_poll)
    monkeypatch.setattr(gfp, "_env",
                        lambda name: "gstdwallet1" if name == "GSTD_WALLET_DESKTOP" else "")
    out = ges.es_round("q", "391")
    assert out["ok"] and out["n_fired"] == 6 and out["n_scored"] == 4
    assert calls["submit"] == 6 and calls["poll"] == 5  # one submit per eval, no retries
    lines = (tmp_path / "es_rounds.jsonl").read_text(encoding="utf-8").splitlines()
    eval_rows = [json.loads(l) for l in lines[:-1]]
    assert len(eval_rows) == 2
    assert all(r["class"] == "eval" and r["ok"] is False for r in eval_rows)
    assert "HTTP 500 boom" in eval_rows[0]["why"] or "expired" in eval_rows[0]["why"] \
        or "HTTP 500 boom" in eval_rows[1]["why"] or "expired" in eval_rows[1]["why"]


def test_state_roundtrip_and_fresh_state():
    st = ges.fresh_state()
    assert st["schema"] == "es_state.v1" and len(st["mean"]) == len(ges.GENOME)
    ges.save_state(st)
    assert ges.load_state()["gen"] == 0
    # corrupt state falls back to fresh
    ges.STATE_PATH.write_text("{broken", encoding="utf-8")
    assert ges.load_state()["schema"] == "es_state.v1"
