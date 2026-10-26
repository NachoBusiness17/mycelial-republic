"""tests/test_inference_budget.py - the class-kill tests (2026-10-01).

Pins mag/inference_budget.py (the RIB_MODEL_GATES harness-table leg) and
its wiring into both carriers against the paid-for burn shapes:

  fable B1/B5  empty content + finish=length + reasoning tokens ->
               EMPTY_REASONING, terminal marker, no refire at same params
  kimi cold    visible content despite 17.6k reasoning tokens -> NOT_EMPTY
  deepseek     thinking-off param injection (forbidden keys stripped)
  floors       max_tokens floor per ask shape (review 18KB+ vs small)
  carriers     hermes_burn + model_garden plan their fires through
               plan_call and guard through guard_terminal (mocked transports)

No real API fire anywhere: every execute path monkeypatches _call.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from mag import inference_budget as ib  # noqa: E402
from tools import hermes_burn as hb  # noqa: E402
from tools import model_garden as mg  # noqa: E402

FABLE = "anthropic/claude-fable-5.1"


# --- the classifier: the three verdicts --------------------------------------

def test_fable_shape_is_empty_reasoning():
    # FABLE1.md B1/B5: 12000/12000 reasoning tokens, empty content, length
    usage = {"completion_tokens": 12000,
             "completion_tokens_details": {"reasoning_tokens": 12000}}
    assert ib.classify_empty("length", usage, "") == ib.EMPTY_REASONING
    assert ib.classify_empty("length", usage, None) == ib.EMPTY_REASONING


def test_kimi_cold_shape_is_not_empty():
    # KIMI1_RUN.md B1: 17,617 reasoning tokens but 354 visible tokens
    usage = {"completion_tokens": 17971,
             "completion_tokens_details": {"reasoning_tokens": 17617}}
    assert ib.classify_empty("stop", usage, "visible deliverable") == ib.NOT_EMPTY


def test_opus_cap_shape_is_empty_reasoning_without_reasoning_detail():
    # 14,960 billed/empty: no reasoning detail, but completion burn + length
    assert ib.classify_empty("length", {"completion_tokens": 14960}, "") == \
        ib.EMPTY_REASONING


def test_empty_without_burn_evidence_is_other():
    # both channels empty, no tokens: transport/provider weirdness, not burn
    assert ib.classify_empty("stop", {}, "") == ib.EMPTY_OTHER
    assert ib.classify_empty(None, {"completion_tokens": 3}, None) == ib.EMPTY_OTHER


def test_whitespace_content_counts_as_empty():
    assert ib.classify_empty("length", {"completion_tokens": 5000,
                                        "completion_tokens_details":
                                        {"reasoning_tokens": 5000}},
                             "   \n") == ib.EMPTY_REASONING


# --- plan_call: per-family recipe, floors, thinking control ------------------

def test_deepseek_thinking_off_injection_strips_forbidden_params():
    plan = ib.plan_call(model="deepseek-chat", family="deepseek",
                        prompt_chars=500, requested_max_tokens=2000,
                        ask_extra={"thinking": {"type": "enabled"},
                                   "reasoning_effort": "high",
                                   "temperature": 0.3})
    # D3 2026-10-04: omission is measured ON; the recipe overrides any ask
    # thinking key with the explicit off switch and strips reasoning params
    assert plan.extra_body == {"temperature": 0.3,
                               "thinking": {"type": "disabled"}}
    assert "reasoning_effort" not in plan.extra_body
    assert plan.recipe_key == "deepseek"


def test_floor_per_shape_review_vs_small():
    # fable at 18KB+ review shape: 12000 was the burn, 24000 is the floor
    plan = ib.plan_call(model=FABLE, prompt_chars=20_000,
                        requested_max_tokens=12_000)
    assert plan.shape == "review" and plan.max_tokens == 24_000
    # small asks are fine at what the ask staged (never lowered)
    plan = ib.plan_call(model=FABLE, prompt_chars=2_000,
                        requested_max_tokens=12_000)
    assert plan.shape == "small" and plan.max_tokens == 12_000
    # below the small floor gets raised (a crumb budget is the burn trap)
    plan = ib.plan_call(model=FABLE, prompt_chars=2_000,
                        requested_max_tokens=4_000)
    assert plan.max_tokens == 8_000
    # opus review floor rides the 64000 rail (RIB_MODEL_GATES)
    plan = ib.plan_call(model="anthropic/claude-opus-5.5",
                        prompt_chars=25_000, requested_max_tokens=32_000)
    assert plan.max_tokens == 64_000 and plan.recipe_key == "claude-opus-5.5"


def test_glm_flash_uncapped_with_effort_low():
    plan = ib.plan_call(model="glm-5.3-flash", family="zai",
                        prompt_chars=20_000, requested_max_tokens=9000)
    assert plan.max_tokens is None  # any cap yields empty finish=length
    assert plan.extra_body == {"thinking": {"type": "enabled"},
                               "reasoning_effort": "low"}


def test_qwen_flash_strips_reasoning_params():
    plan = ib.plan_call(model="qwen/qwen3.7-flash", prompt_chars=100,
                        ask_extra={"reasoning": {"max_tokens": 800}})
    assert plan.extra_body == {}
    assert plan.recipe_key == "qwen-flash"


def test_nous_primes_lessig_rail_and_default_recipe():
    plan = ib.plan_call(model="glm-5.3-prime", prompt_chars=1000)
    assert plan.recipe_key == "nous-primes"
    assert plan.extra_body == {"reasoning": {"max_tokens": 6000}}
    plan = ib.plan_call(model="totally/unknown-model", prompt_chars=1000,
                        requested_max_tokens=1000)
    assert plan.recipe_key == "default" and plan.max_tokens == 8_000


def test_family_fallback_and_no_nous_host_trap():
    # deepseek host serves one animal class: fallback applies
    assert ib.recipe_for(model="", family="deepseek").key == "deepseek"
    # the nous host serves many animals: family alone must NOT pick primes
    assert ib.recipe_for(model="some/new-nous-model", family="nous").key == \
        "default"


# --- react + marker mechanics -------------------------------------------------

def test_react_marker_names_both_recoveries(tmp_path):
    marker = ib.react("A1", "claude-fable-5.1", "cause bytes here", tmp_path)
    assert marker == tmp_path / "EMPTY_REASONING" and marker.is_file()
    text = marker.read_text(encoding="utf-8")
    assert "re-stage the ask with this" in text and "switch family" in text
    assert "operator edit of the ask bytes AND deleting" in text
    row = ib.skip_terminal(tmp_path, "A1")
    assert row["skipped"].startswith("EMPTY_REASONING")
    assert ib.skip_terminal(tmp_path / "elsewhere", "A1") is None


# --- behavioral sync (the distillability law) --------------------------------

def test_sync_to_behavioral_is_idempotent(tmp_path, monkeypatch):
    from tools import animal_profiles as ap
    monkeypatch.setattr(ap, "BEHAV_DIR", tmp_path)
    written = ib.sync_to_behavioral()
    assert len(written) == len(ib.FAMILY_TABLE)
    rows = []
    for p in sorted(tmp_path.glob("*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            rows.append(json.loads(line))
    assert all(r["kind"] == "rail" and r["source"] for r in rows)
    deepseek = [r for r in rows if r["model"] == "deepseek"]
    assert deepseek and "small_floor=2000" in deepseek[0]["detail"]
    assert ib.sync_to_behavioral() == []  # dedup: no duplicate rows


# --- carrier wiring: hermes_burn ---------------------------------------------

@pytest.fixture()
def carrier(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(hb, "ROOT", tmp_path)
    monkeypatch.setattr(hb, "OUT_DIR", tmp_path / "watch" / "inbox" / "hermes_burn")
    monkeypatch.setattr(hb, "USAGE", tmp_path / "usage.jsonl")
    (tmp_path / "materials").mkdir()
    return tmp_path


def _ask_dir(root: Path, ask_id: str, **over) -> Path:
    d = root / "queues" / ask_id
    d.mkdir(parents=True, exist_ok=True)
    meta = {"id": ask_id, "model": FABLE, "max_tokens": 12000,
            "contract": "review the code", "evidence": ["materials/ev.md"],
            "revision": False, "turn2_only": False}
    meta.update(over)
    (d / "ask.json").write_text(json.dumps(meta), encoding="utf-8")
    (root / "materials" / "ev.md").write_text(
        "material head bytes\n" + "filler " * 300, encoding="utf-8")
    return d


def _burn_resp() -> dict:
    return {"usage": {"prompt_tokens": 9000, "completion_tokens": 12000,
                      "completion_tokens_details":
                      {"reasoning_tokens": 12000}},
            "choices": [{"finish_reason": "length",
                         "message": {"content": "", "reasoning":
                                     "I'm counting through the source..."}}]}


def test_hermes_fable_burn_is_terminal_no_refire(carrier, monkeypatch):
    fired = []

    def fake_call(model, messages, max_tokens, key, retries=1, extra_body=None):
        fired.append(max_tokens)
        return _burn_resp()

    monkeypatch.setattr(hb, "_call", fake_call)
    d = _ask_dir(carrier, "FABLE_B1")
    with pytest.raises(RuntimeError, match="EMPTY_REASONING"):
        hb.run_ask(d, "k")
    marker = d / "EMPTY_REASONING"
    assert marker.is_file() and "claude-fable-5.1" in marker.read_text(encoding="utf-8")
    led = [json.loads(l) for l in hb.USAGE.read_text(encoding="utf-8").splitlines()]
    assert led[-1]["empty_reasoning"] is True and led[-1]["ok"] is False
    # the reasoning-channel ramble must NOT land as a deliverable
    assert not (hb.OUT_DIR / "FABLE_B1.md").exists()
    row = hb.run_ask(d, "k")  # next cycle: skip on sight, never refire
    assert row["skipped"].startswith("EMPTY_REASONING")
    assert len(fired) == 1


def test_hermes_planned_fire_uses_recipe_floor(carrier, monkeypatch):
    seen = {}

    def fake_call(model, messages, max_tokens, key, retries=1, extra_body=None):
        seen["max_tokens"] = max_tokens
        return {"usage": {"prompt_tokens": 10, "completion_tokens": 20,
                          "completion_tokens_details": {"reasoning_tokens": 5}},
                "choices": [{"finish_reason": "stop",
                             "message": {"content": "the deliverable"}}]}

    monkeypatch.setattr(hb, "_call", fake_call)
    d = _ask_dir(carrier, "FABLE_OK", max_tokens=4000)
    row = hb.run_ask(d, "k")
    assert row["ok"] is True
    assert seen["max_tokens"] == 8000  # small-shape floor raised the crumb ask


def test_hermes_kimi_cold_content_lands(carrier, monkeypatch):
    def fake_call(model, messages, max_tokens, key, retries=1, extra_body=None):
        return {"usage": {"prompt_tokens": 12000, "completion_tokens": 17971,
                          "completion_tokens_details":
                          {"reasoning_tokens": 17617}},
                "choices": [{"finish_reason": "stop",
                             "message": {"content": "cold but real deliverable"}}]}

    monkeypatch.setattr(hb, "_call", fake_call)
    monkeypatch.setitem(hb.PRICING, "moonshotai/kimi-k2", (0.0000006, 0.0000023))
    d = _ask_dir(carrier, "KIMI_B1", model="moonshotai/kimi-k2")
    row = hb.run_ask(d, "k")
    assert row["ok"] is True and not row.get("skipped")
    assert not (d / "EMPTY_REASONING").exists()
    assert "cold but real deliverable" in \
        (hb.OUT_DIR / "KIMI_B1.md").read_text(encoding="utf-8")


# --- carrier wiring: model_garden --------------------------------------------

@pytest.fixture()
def garden(tmp_path, monkeypatch):
    monkeypatch.setattr(mg, "ROOT", tmp_path)
    monkeypatch.setattr(mg, "OUT_DIR", tmp_path / "watch" / "inbox" / "model_garden")
    monkeypatch.setattr(mg, "USAGE", tmp_path / "memory" / "runs" / "model_garden" / "usage.jsonl")
    return tmp_path


def _garden_ask(root, ask_id="G1", **over):
    d = root / ask_id
    d.mkdir(parents=True, exist_ok=True)
    (root / "ev.txt").write_text("MATERIAL-BYTES 123\n" + "filler " * 100,
                                 encoding="utf-8")
    meta = {"id": ask_id, "model": "deepseek-chat", "base_env": "K",
            "base_url": "https://api.deepseek.com/v1",
            "contract": "Deliver one spec.", "evidence": ["ev.txt"],
            "max_tokens": 64}
    meta.update(over)
    (d / "ask.json").write_text(json.dumps(meta), encoding="utf-8")
    return d


def test_garden_burn_is_terminal_no_refire(garden, monkeypatch):
    fired = []

    def fake(model, messages, max_tokens, key, base_url, retries=1,
             extra_body=None):
        fired.append(extra_body)
        return _burn_resp()

    monkeypatch.setattr(mg, "_call", fake)
    d = _garden_ask(garden, "G_BURN")
    with pytest.raises(RuntimeError, match="EMPTY_REASONING"):
        mg.run_ask(d, key="k", execute=True)
    assert (d / "EMPTY_REASONING").is_file()
    row = mg.run_ask(d, key="k", execute=True)
    assert row["skipped"].startswith("EMPTY_REASONING")
    assert len(fired) == 1


def test_garden_fire_rides_recipe_params(garden, monkeypatch):
    seen = {}

    def fake(model, messages, max_tokens, key, base_url, retries=1,
             extra_body=None):
        seen.update(max_tokens=max_tokens, extra_body=extra_body)
        return {"usage": {"prompt_tokens": 100, "completion_tokens": 42,
                          "completion_tokens_details": {"reasoning_tokens": 7}},
                "choices": [{"finish_reason": "stop",
                             "message": {"content": "DELIVERABLE BYTES"}}]}

    monkeypatch.setattr(mg, "_call", fake)
    # nous primes: the LESSIG reasoning rail reaches the wire; body_extra
    # thinking-on is stripped for deepseek... here primes keep their rail
    d = _garden_ask(garden, "G_PRIME", model="glm-5.3-prime",
                    base_url="https://inference-api.nousresearch.com/v1",
                    body_extra={"temperature": 0.4})
    row = mg.run_ask(d, key="k", execute=True)
    assert row["ok"] is True
    assert seen["extra_body"] == {"reasoning": {"max_tokens": 6000},
                                  "temperature": 0.4}
    assert seen["max_tokens"] == 8000  # small-shape floor beat the 64 ask


def test_garden_deepseek_strips_ask_thinking_on(garden, monkeypatch):
    seen = {}

    def fake(model, messages, max_tokens, key, base_url, retries=1,
             extra_body=None):
        seen.update(max_tokens=max_tokens, extra_body=extra_body)
        return {"usage": {"prompt_tokens": 100, "completion_tokens": 42},
                "choices": [{"finish_reason": "stop",
                             "message": {"content": "ok"}}]}

    monkeypatch.setattr(mg, "_call", fake)
    # an ask that tries to re-enable thinking on the AH10 animal: overridden
    # by the explicit off switch (D3 2026-10-04: omission is measured ON)
    d = _garden_ask(garden, "G_DS", body_extra={"thinking": {"type": "enabled"},
                                                "reasoning_effort": "high"})
    row = mg.run_ask(d, key="k", execute=True)
    assert row["ok"] is True
    assert seen["extra_body"] == {"thinking": {"type": "disabled"}}
    assert seen["max_tokens"] == 2000  # deepseek small floor (ds_workhorse)
