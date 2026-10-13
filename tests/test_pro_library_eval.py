"""Pro library EVAL — is it worthwhile? precision/recall/over-fire + right-sizing.

Designed to answer:
  1. PRECISION  — when it fires, is it the RIGHT move?
  2. RECALL     — when a winning move exists, does it find it?
  3. OVER-FIRE  — does it fire on irrelevant states (noise)?
  4. THRESHOLD  — is there a confidence line below which we should NOT fire?
  5. SPECIFICITY— can a too-generic signature (stopwords) be rejected?
  6. PLUMBING   — does an injected steer actually reach the agent (seam)?
  7. LEARNING   — does an outcome update wins/tries and fold into the stack?
  8. GRACE      — empty/corrupt state degrades safely.
"""
from __future__ import annotations

import pytest

import mag.pro_library as pl
import mag.operator_inbox as oi
import mag.skill_ledger as sl
import mag.tesuji_shell as ts


@pytest.fixture
def pro(isolated_pl):
    pl.seed_default_moves()
    return isolated_pl


@pytest.fixture
def isolated_pl(tmp_path, monkeypatch):
    monkeypatch.setattr(pl, "LIB_PATH", tmp_path / "pro_library.json")
    monkeypatch.setattr(oi, "INBOX_PATH", tmp_path / "operator_inbox.json")
    monkeypatch.setattr(sl, "DECISIONS_PATH", tmp_path / "skill_ledger.jsonl")
    monkeypatch.setattr(sl, "LABELED_PATH", tmp_path / "rows.jsonl")
    monkeypatch.setattr(ts, "SHELLS_PATH", tmp_path / "tesuji_shells.jsonl")
    return tmp_path


# labeled dataset: (state_text, expected maps_to prefix)
POSITIVES = [
    ("agent claimed it updated llm.py but no write_file ran, no file change on disk, tool result empty, done with no diff", "steer"),
    ("about to apply a spec but the base fingerprint may have drifted", "spec"),
    ("the task is vague, the cheap executor will probably fake it", "spec"),
    ("model is looping, repeating the same tool 5x, burning tokens", "steer"),
    ("reached a decision point and need to steer mid-round", "tip"),
]
NEGATIVES = [
    "the weather is nice and I wrote a poem about the sunset",
    "the refactor is complete, all tests pass, committed and pushed",
    "incremented the version number and released a new build",
]


def test_1_precision_and_recall(pro):
    """When it fires, is it the right move? When a win exists, does it find it?"""
    correct = 0
    found = 0
    for text, expected in POSITIVES:
        ms = pl.match({"text": text}, limit=1)
        if not ms:
            continue
        found += 1
        if ms[0]["move"]["maps_to"].startswith(expected):
            correct += 1
    precision = correct / max(1, found)
    recall = found / len(POSITIVES)
    print(f"  precision={precision:.2f} recall={recall:.2f} (found {found}/{len(POSITIVES)})")
    assert recall == 1.0, "every positive should surface a match"
    assert precision >= 0.8, f"top match should be right, got {precision:.2f}"


def test_2_no_overfire_on_negatives(pro):
    """Irrelevant states must NOT produce a fire-worthy match (score >= threshold)."""
    overfires = 0
    for text in NEGATIVES:
        ms = pl.match({"text": text})
        for m in ms:
            if m["score"] >= 0.4:  # the intended fire threshold
                overfires += 1
                print(f"  OVERFIRE on {text[:40]} score={m['score']} -> {m['move']['maps_to']}")
    assert overfires == 0, f"negatives must not clear the fire threshold ({overfires} overfires)"


def test_3_aim_respects_fire_threshold(pro):
    """aim_once must not inject low-confidence moves (the right-size fix)."""
    # a weakly-matched positive (score below threshold) must NOT be injected
    out = pl.aim_once({"text": "the model is looping, repeating the same tool 5x, burning tokens"})
    for f in out["fired"]:
        assert f["score"] >= 0.4, f"fired at {f['score']} < 0.4 threshold — over-fire"
    assert len(out["fired"]) >= 1  # the strong match still fires


def test_4_generic_signature_rejected(pro):
    """A stopword-only signature (agent/tool/file/model/task) matches everything —
    the library must reject it at add time to avoid a 'fires on anything' move."""
    before = len(pl._load()["moves"])
    r = pl.add_move(["agent", "tool", "file", "model", "task"], "steer", "generic advice")
    after = len(pl._load()["moves"])
    assert r.get("ok") is False, "generic stopword signature must be rejected"
    assert after == before, "rejected move must not be stored"


def test_5_injection_plumbing_reaches_the_seam(pro):
    """A fired steer must land in the inbox AND drain into the agent's messages."""
    text = "agent claimed it updated llm.py but no write_file ran, no file change, tool result empty, done with no diff"
    out = pl.aim_once({"text": text})
    assert out["fired"], "should have fired the false-success steer"
    assert out["fired"][0]["injected"] is True
    # drains at checkpoint into a real user-message steer
    actions = oi.drain_pending_at_checkpoint(task_hint="verify llm.py")
    assert actions, "steer should drain at the next checkpoint"
    msgs = [{"role": "user", "content": "goal"}]
    msgs = oi.apply_actions_to_messages(msgs, actions)
    joined = " ".join(str(m.get("content") or "") for m in msgs).lower()
    assert "git diff" in joined or "verify" in joined or "trust bytes" in joined


def test_6_learning_folds(pro):
    data = pl._load()
    mid = data["moves"][0]["id"]
    r = pl.learn(mid, outcome="ok", goal="aim test", detail="worked")
    assert r["ok"] is True and r["win"] is True
    st = pl.stats()
    assert st["total_tries"] == 1 and st["total_wins"] == 1 and st["win_rate"] == 100.0
    assert sl.progress()["decisions"] >= 1
    assert ts.read_shells()  # captured on add


def test_7_graceful_empty_state(pro):
    out = pl.aim_once({}, fire_moves=False)
    assert out["ok"] is True
    assert out["matches"] == [] and out["fired"] == []
