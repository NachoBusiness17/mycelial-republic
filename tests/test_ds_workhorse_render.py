"""Render-law tests for tools/ds_workhorse.py (rails law 2, GO item 9).

Cause: the hollow-batch incident 2026-10-03 - gapfold v1 fabricated from the
prompt schema and the frontier-delta v1 arm refused on every row, while all 30
rows banked ok:true, because ok measured API success only. Evidence:
memory/runs/ds_batches/gapfold_results.jsonl + frontier_delta_results.jsonl
(void-stamped 2026-10-04), queue/STANDING_RAILS.md law 2, and
memory/runs/mickey17_v2/runs/run-0/lanes/a10-ds-batches.json rows 0-3.

Law under test: material must render; empty text is not success. A 200 with an
empty completion banks ok_api true and ok_material false; a template without
{text} or an item whose text renders empty fails the batch before any spend.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools import ds_workhorse as dw  # noqa: E402


@pytest.fixture()
def no_sleep(monkeypatch):
    monkeypatch.setattr(dw.time, "sleep", lambda _s: None)


def _batch(tmp_path, items, template):
    items_path = tmp_path / "items.jsonl"
    items_path.write_text(
        "\n".join(json.dumps(i) for i in items) + "\n", encoding="utf-8")
    prompt_path = tmp_path / "prompt.md"
    prompt_path.write_text(template, encoding="utf-8")
    out_path = tmp_path / "results.jsonl"
    return items_path, prompt_path, out_path


def _rows(out_path):
    return [json.loads(l) for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()]


def test_empty_completion_banks_ok_material_false(tmp_path, monkeypatch, no_sleep):
    # a 200 with an empty completion is an API success and a material failure
    calls = []

    def fake_ask(key, prompt):
        calls.append(prompt)
        return "", 0.001, 100  # empty text, real spend, real prompt_tokens

    monkeypatch.setattr(dw, "ask", fake_ask)
    monkeypatch.setattr(dw, "load_key", lambda: "k")
    items_path, prompt_path, out_path = _batch(
        tmp_path,
        [{"id": "delta-x", "text": "CONTRACT:\nreal material here"}],
        "Judge this: {text}",
    )
    dw.run(items_path, prompt_path, out_path)
    (row,) = _rows(out_path)
    assert row["ok_api"] is True
    assert row["ok_material"] is False
    assert row["prompt_tokens"] == 100
    assert row["model"] == dw.MODEL
    assert len(calls) == 2  # the gopher cure: retry-once on empty


def test_real_completion_banks_ok_material_true(tmp_path, monkeypatch, no_sleep):
    monkeypatch.setattr(dw, "ask", lambda k, p: ("DELIVERABLE BYTES", 0.002, 4200))
    monkeypatch.setattr(dw, "load_key", lambda: "k")
    items_path, prompt_path, out_path = _batch(
        tmp_path,
        [{"id": "delta-y", "text": "CONTRACT:\nreal material here"}],
        "Judge this: {text}",
    )
    dw.run(items_path, prompt_path, out_path)
    (row,) = _rows(out_path)
    assert row["ok_api"] is True
    assert row["ok_material"] is True
    assert row["prompt_tokens"] == 4200
    assert "DELIVERABLE BYTES" in row["out"]


def test_template_without_text_slot_fails_batch_before_spend(tmp_path, monkeypatch, no_sleep):
    calls = []

    def fake_ask(key, prompt):
        calls.append(prompt)
        return "DELIVERABLE BYTES", 0.002, 4200

    monkeypatch.setattr(dw, "ask", fake_ask)
    monkeypatch.setattr(dw, "load_key", lambda: "k")
    items_path, prompt_path, out_path = _batch(
        tmp_path,
        [{"id": "delta-z", "text": "real material here"}],
        "A prompt that never renders its material",
    )
    with pytest.raises(SystemExit, match="render guard"):
        dw.run(items_path, prompt_path, out_path)
    assert calls == []  # refused before a cent was spent
    assert not out_path.exists()


def test_empty_item_text_fails_render_guard(tmp_path, monkeypatch, no_sleep):
    calls = []

    def fake_ask(key, prompt):
        calls.append(prompt)
        return "DELIVERABLE BYTES", 0.002, 4200

    monkeypatch.setattr(dw, "ask", fake_ask)
    monkeypatch.setattr(dw, "load_key", lambda: "k")
    items_path, prompt_path, out_path = _batch(
        tmp_path,
        [{"id": "delta-ok", "text": "real material here"},
         {"id": "delta-hollow", "text": "   "}],
        "Judge this: {text}",
    )
    with pytest.raises(SystemExit, match="delta-hollow"):
        dw.run(items_path, prompt_path, out_path)
    assert calls == []  # the guard fires before any API call, not after one
    assert not out_path.exists()
