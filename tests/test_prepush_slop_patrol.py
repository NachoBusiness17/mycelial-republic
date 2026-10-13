"""Tests for tools.prepush_slop_patrol (the no-slop steal, 2026-10-07).

The founding law: a slop fixture tripping EVERY detector class must WARN,
clean estate prose must pass, fenced/backticked banned words must be exempt
(quoting a banned word as an example is the skill's own sanctioned move),
and the baseline must accept findings by fingerprint without a line shift
resurrecting them. Receipt: watch/inbox/NO_SLOP_STEAL_20261007.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.prepush_slop_patrol import (  # noqa: E402
    colon_reveal_hit,
    fingerprint,
    main,
    scan_text,
)

# --- the slop fixture: one line per class, every class represented ---------

SLOP_MD = """# Build notes

Let me delve into the robust harness so we can leverage the tapestry of
tools. This is huge.

This is not just a linter but a lifestyle. It's not the model, it's the
eval. The question isn't the tool.

Here's the thing, the build broke at 03:00Z again. What nobody tells you is
that the disk was full.

The best part: it learns from every run.

The future isn't coming. It's already here. That's it. That's the whole thing.

The honest note: `delve` in backticks is exempt, and so is this:

```
leverage the realm inside a fence
```
"""

CLEAN_MD = """# Patrol notes

The census read 4,358 tests across 518 files at 2026-10-04T09:25Z. Three
full runs agreed within 61 items, so the count stood.

Spec: the brief says cut, and the rename landed (12 files moved).

- Fixed: the entrypoint collected 2,757 ghost items, now zero.
- The mirror: https://example.com/mirror stays a value row, never a reveal.

| Column | Value |
| --- | --- |
| The table row | lowercase cell |

We renamed the script and every disk candidate collects items now.
"""


def classes_of(findings: list[dict]) -> set[str]:
    return {f["name"] for f in findings}


def test_slop_fixture_trips_every_class():
    findings = scan_text(SLOP_MD, "slop.md")
    got = classes_of(findings)
    assert got == {
        "BANNED-WORD", "BINARY-CONTRAST", "THROAT-CLEAR",
        "COLON-REVEAL", "FAKE-PROFOUND",
    }
    banned_words_found = {f["detail"] for f in findings
                          if f["name"] == "BANNED-WORD"}
    assert any("delve" in d for d in banned_words_found)
    assert any("robust" in d for d in banned_words_found)
    assert any("leverage" in d for d in banned_words_found)
    assert any("tapestry" in d for d in banned_words_found)
    assert any("this is huge" in d for d in banned_words_found)


def test_binary_contrast_all_three_shapes():
    findings = scan_text(SLOP_MD, "slop.md")
    details = [f["detail"] for f in findings
               if f["name"] == "BINARY-CONTRAST"]
    assert len(details) == 3  # not-just-but, it's-not-it's, the-question-isn't


def test_fake_profound_both_kickers_and_cross_sentence():
    findings = scan_text(SLOP_MD, "slop.md")
    details = [f["detail"] for f in findings
               if f["name"] == "FAKE-PROFOUND"]
    assert len(details) == 2  # future-isn't-coming + that's-the-whole-thing


def test_clean_prose_passes():
    findings = scan_text(CLEAN_MD, "clean.md")
    assert findings == []


def test_fenced_and_backticked_banned_words_exempt():
    findings = scan_text(SLOP_MD, "slop.md")
    # the only banned words in the fixture outside exemptions are the four
    # prose ones; the fenced `realm` and the backticked `delve` never fire
    hits = [f for f in findings if f["name"] == "BANNED-WORD"]
    assert not any("realm" in f["detail"] for f in hits)


def test_colon_reveal_exclusions():
    # single-word label rows are estate rows, not reveals
    assert colon_reveal_hit("Spec: the brief says cut") is None
    # markdown structure (list, heading) and table pipes are exempt
    assert colon_reveal_hit("- The best part: it learns") is None
    assert colon_reveal_hit("## The best part: it learns") is None
    assert colon_reveal_hit("| The best part | it learns |") is None
    # URL values are not reveals
    assert colon_reveal_hit("The mirror: https://example.com/x") is None
    # the canonical reveal fires
    hit = colon_reveal_hit("The best part: it learns from every run.")
    assert hit is not None and "colon reveal" in hit


def test_colon_reveal_two_word_prefix_required():
    assert colon_reveal_hit("The best part: it learns.") is not None
    # a reveal clause needs a space: values like "Mode: dev" stay rows
    assert colon_reveal_hit("Mode: dev") is None


def test_fingerprint_stable_under_line_shift():
    a = {"name": "BANNED-WORD", "file": "a.md", "line": 3,
         "detail": "", "line_text": "we leverage the tool"}
    b = dict(a, line=17)
    assert fingerprint(a) == fingerprint(b)
    c = dict(a, line_text="we use the tool")
    assert fingerprint(a) != fingerprint(c)


def test_cli_files_warn_and_ok(tmp_path, capsys):
    slop = tmp_path / "slop.md"
    slop.write_text(SLOP_MD, encoding="utf-8")
    clean = tmp_path / "clean.md"
    clean.write_text(CLEAN_MD, encoding="utf-8")
    rc_warn = main(["check", "--files", str(slop),
                    "--baseline", str(tmp_path / "absent.json")])
    out_warn = capsys.readouterr().out
    assert rc_warn == 1
    assert out_warn.splitlines()[0].startswith("SLOP-PATROL: WARN")
    # exact per-class counts from the fixture: delve/robust/leverage/
    # tapestry/this-is-huge = 5 banned; 3 contrast shapes; 2 throat-clears;
    # 1 colon reveal; 2 kickers
    assert "BANNED-WORD=5" in out_warn
    assert "BINARY-CONTRAST=3" in out_warn
    assert "THROAT-CLEAR=2" in out_warn
    assert "COLON-REVEAL=1" in out_warn
    assert "FAKE-PROFOUND=2" in out_warn
    rc_ok = main(["check", "--files", str(clean),
                  "--baseline", str(tmp_path / "absent.json")])
    out_ok = capsys.readouterr().out
    assert rc_ok == 0
    assert out_ok.splitlines()[0].startswith("SLOP-PATROL: ok")


def test_cli_baseline_accepts_by_fingerprint(tmp_path, capsys):
    slop = tmp_path / "slop.md"
    slop.write_text(SLOP_MD, encoding="utf-8")
    baseline = tmp_path / "base.json"
    assert main(["check", "--files", str(slop), "--root", str(tmp_path),
                 "--baseline", str(baseline)]) == 1
    capsys.readouterr()  # drain the WARN run before the accepted run
    findings = scan_text(SLOP_MD, "slop.md")
    accepted = {fingerprint(f): "triaged" for f in findings}
    baseline.write_text(json.dumps({"accepted": accepted}), encoding="utf-8")
    rc = main(["check", "--files", str(slop), "--root", str(tmp_path),
               "--baseline", str(baseline)])
    out = capsys.readouterr().out
    assert rc == 0
    assert out.splitlines()[0].startswith("SLOP-PATROL: ok")
    assert "accepted by fingerprint" in out.splitlines()[0]


def test_cli_jsonl_title_scan(tmp_path, capsys):
    rows = [
        {"title": "How to leverage the cave for robust dispatch"},
        {"title": "plain concrete row about the 03:00Z drain"},
        {"title": "The quiet part: nobody audits the auditor"},
        "not json at all",
    ]
    jl = tmp_path / "links.jsonl"
    jl.write_text("\n".join(json.dumps(r) if isinstance(r, dict) else r
                            for r in rows), encoding="utf-8")
    rc = main(["check", "--files", str(jl),
               "--baseline", str(tmp_path / "absent.json")])
    out = capsys.readouterr().out
    assert rc == 1
    assert "links.jsonl:1" in out      # the banned-word title
    assert "links.jsonl:2" not in out  # clean title absent
    assert "links.jsonl:3" in out      # colon-reveal title
    assert "malformed jsonl row(s) skipped" in out


def test_cli_cannot_verify_shapes(tmp_path, capsys):
    assert main(["check", "--files", str(tmp_path / "nope.md")]) == 2
    assert "ERROR" in capsys.readouterr().out
    weird = tmp_path / "weird.py"
    weird.write_text("x = 1", encoding="utf-8")
    assert main(["check", "--files", str(weird)]) == 2
    assert "not a prose or jsonl suffix" in capsys.readouterr().out


def test_no_em_dash_in_tool_or_skill_bytes():
    # the estate em-dash law, held on the surfaces this lane owns
    tool = (REPO / "tools" / "prepush_slop_patrol.py").read_text(
        encoding="utf-8")
    skill = (REPO / ".agents" / "skills" / "no-slop" / "SKILL.md").read_text(
        encoding="utf-8")
    assert "\u2014" not in tool
    assert "\u2014" not in skill
