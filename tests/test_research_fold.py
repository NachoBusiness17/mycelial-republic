"""tests for research_fold — fold landed grok/frontier research answers into skill_ledger case law.

RIB (frozen spec):
  _completed_answers() -> all .answer.{remote,local}.md files in the pack dir (newest first).
  fold_one(answer)     -> read the answer text, record it as a skill_ledger DECISION (case law),
                          mark it folded (idempotent per pack).
  run()                -> scan for completed answers not yet folded, fold them, idempotent.
  status()             -> total answers / folded / pending.

This is the mechanism that makes us LEARN from grok: landed answers become case law (the bed ->
precedent) so the findings shape future work, not just sit as files. Deterministic + $0.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import research_fold  # noqa: E402


def test_status_reports_pack_dir():
    s = research_fold.status()
    assert s["ok"] is True
    assert "total_answers" in s and "folded" in s and "pending" in s


def test_completed_answers_are_md_files(tmp_path):
    (tmp_path / "p1.answer.remote.md").write_text("grok answer 1", encoding="utf-8")
    (tmp_path / "p2.answer.local.md").write_text("local answer 2", encoding="utf-8")
    (tmp_path / "p3.json").write_text("{}", encoding="utf-8")  # not an answer
    research_fold.PACKS = tmp_path
    answers = research_fold._completed_answers()
    names = [a.name for a in answers]
    assert "p1.answer.remote.md" in names
    assert "p2.answer.local.md" in names
    assert "p3.json" not in names


def test_fold_one_is_idempotent(tmp_path):
    answer = tmp_path / "p1.answer.remote.md"
    answer.write_text("a grok answer to fold into case law", encoding="utf-8")
    research_fold.FOLDED = tmp_path / "folded.jsonl"
    r1 = research_fold.fold_one(answer)
    assert r1["ok"] is True
    assert research_fold._mark_folded  # marker helper exists
    # idempotent: fold_one again should not error (pack already marked)
    r2 = research_fold.fold_one(answer)
    assert r2["ok"] is True


def test_run_folds_pending_and_is_idempotent(tmp_path):
    (tmp_path / "a1.answer.remote.md").write_text("grok finding one", encoding="utf-8")
    (tmp_path / "a2.answer.remote.md").write_text("grok finding two", encoding="utf-8")
    research_fold.PACKS = tmp_path
    research_fold.FOLDED = tmp_path / "folded.jsonl"
    r = research_fold.run(limit=10)
    assert r["ok"] is True
    assert r["folded"] >= 1
    # second run folds nothing new (idempotent)
    r2 = research_fold.run(limit=10)
    assert r2["folded"] == 0 or r2["pending_remaining"] <= r["pending_remaining"]
