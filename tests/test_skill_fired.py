"""skill_fired.v1 receipts from the skills_for_job chokepoint (W3 2026-09-29).

Spec: watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md return 16 - one logging
point per skill actually returned, so fires become countable truth.
Covers: N skills returned -> N fired rows; the line filter actually filters;
fired() counts per skill_id and ignores foreign ledger rows.
"""
from __future__ import annotations

import json

import yaml

import mag.skills_pack as sp

# Fixture skill body: skeleton lines (heading / bold-led / list item) plus
# prose lines that a correct filter must drop.
ALPHA_BODY = """plain prose intro that the filter must drop

# Alpha heading
**Bold lead** alpha line
- alpha bullet item
more trailing prose that the filter must also drop
"""


def _setup(monkeypatch, tmp_path):
    """Point CFG and the ledger at tmp fixtures; return (ledger, cfg paths)."""
    alpha = tmp_path / "alpha.md"
    alpha.write_text(ALPHA_BODY, encoding="utf-8")
    beta = tmp_path / "beta.md"
    beta.write_text("# Beta heading\nbeta prose to drop\n- beta bullet\n", encoding="utf-8")
    cfg = {
        "schema": "mag_skills.v1",
        "skills": [
            {"id": "alpha", "path": str(alpha), "pack_excerpt": True},
            {"id": "beta", "path": str(beta), "pack_excerpt": True},
            {"id": "ghost", "path": "does/not/exist.md", "pack_excerpt": True},
            {"id": "muted", "path": str(alpha), "pack_excerpt": False},
        ],
        "job_to_skills": {"research": ["alpha", "beta", "ghost", "muted"]},
    }
    cfg_path = tmp_path / "skills.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    ledger = tmp_path / "skill_ledger.jsonl"
    monkeypatch.setattr(sp, "CFG", cfg_path)
    monkeypatch.setattr(sp, "SKILL_LEDGER", ledger)
    return ledger


def _rows(ledger):
    return [json.loads(ln) for ln in ledger.read_text(encoding="utf-8").splitlines() if ln.strip()]


def test_filter_actually_filters(tmp_path):
    """The fixed _clip_file drops prose lines and keeps skeleton lines."""
    f = tmp_path / "doc.md"
    f.write_text(ALPHA_BODY, encoding="utf-8")
    out = sp._clip_file(f, 400)
    assert "# Alpha heading" in out
    assert "**Bold lead** alpha line" in out
    assert "- alpha bullet item" in out
    assert "plain prose intro" not in out
    assert "more trailing prose" not in out


def test_n_skills_returned_n_fired_rows(monkeypatch, tmp_path):
    """3 returned skills (alpha, beta, ghost) -> exactly 3 fired rows; muted never fires."""
    ledger = _setup(monkeypatch, tmp_path)
    text = sp.skills_for_job("research")
    assert "### alpha" in text
    assert "### beta" in text
    assert "- ghost: (path missing)" in text
    assert "muted" not in text
    rows = [r for r in _rows(ledger) if r.get("schema") == "skill_fired.v1"]
    assert len(rows) == 3
    by_sid = {r["skill_id"]: r for r in rows}
    assert set(by_sid) == {"alpha", "beta", "ghost"}
    assert by_sid["alpha"]["pack_mode"] == "excerpt"
    assert by_sid["beta"]["pack_mode"] == "excerpt"
    assert by_sid["ghost"]["pack_mode"] == "missing"
    assert by_sid["ghost"]["chars_injected"] == 0
    assert by_sid["alpha"]["chars_injected"] == len(f"### alpha\n{sp._clip_file(tmp_path / 'alpha.md', min(280, max(80, 800 // 4)))}")
    for r in rows:
        assert r["job"] == "research"
        assert r["ts"]


def test_fired_counts_per_skill_id(monkeypatch, tmp_path):
    """fired() counts only skill_fired.v1 rows; foreign schema rows never inflate it."""
    ledger = _setup(monkeypatch, tmp_path)
    assert sp.skills_for_job("research")
    assert sp.skills_for_job("research")
    # interleave a foreign-schema row the way the decision ledger writes them
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"schema": "skill_ledger.decision.v1", "skill_id": "alpha"}) + "\n")
        f.write("not json at all\n")
    counts = sp.fired()
    assert counts == {"alpha": 2, "beta": 2, "ghost": 2}
    assert sp.fired("alpha") == 2
    assert sp.fired("muted") == 0
    assert sp.fired("never-fired") == 0


# X6 2026-09-29 (hydrology): JSONL law registry -> TOP-5-by-birth_count tail.
# File order is SHUFFLED on purpose so the test proves the loader sorts by
# birth_count instead of trusting the file's rank order.
ORAL_ROWS = [
    {"rank": 1, "canonical": "LAW: born-once alpha", "birth_count": 1},
    {"rank": 2, "canonical": "LAW: top A", "birth_count": 9},
    {"rank": 3, "canonical": "LAW: top B", "birth_count": 7},
    {"rank": 4, "canonical": "LAW: top C", "birth_count": 5},
    {"rank": 5, "canonical": "LAW: top D", "birth_count": 3},
    {"rank": 6, "canonical": "LAW: top E", "birth_count": 2},
    {"rank": 7, "canonical": "LAW: born-once beta", "birth_count": 1},
    {"rank": 8, "canonical": "LAW: superseded champ", "birth_count": 99,
     "superseded": "SUPERSEDED? dead law, never ships into context"},
]


def _oral_setup(monkeypatch, tmp_path):
    """Point CFG/ledger at fixtures; the .jsonl order is shuffled, not rank order."""
    laws = tmp_path / "ORAL_LAW_DEDUPED.jsonl"
    shuffled = [ORAL_ROWS[1], ORAL_ROWS[0], ORAL_ROWS[6], ORAL_ROWS[2],
                ORAL_ROWS[7], ORAL_ROWS[3], ORAL_ROWS[4], ORAL_ROWS[5]]
    laws.write_text(
        "\n".join(json.dumps(r) for r in shuffled) + "\nnot json at all\n",
        encoding="utf-8",
    )
    cfg = {
        "schema": "mag_skills.v1",
        "skills": [{"id": "oral-law", "path": str(laws), "pack_excerpt": True}],
        "job_to_skills": {"research": ["oral-law"]},
    }
    cfg_path = tmp_path / "skills.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    ledger = tmp_path / "skill_ledger.jsonl"
    monkeypatch.setattr(sp, "CFG", cfg_path)
    monkeypatch.setattr(sp, "SKILL_LEDGER", ledger)
    return ledger


def test_oral_law_tail_is_top5_by_birth_count(monkeypatch, tmp_path):
    """X6: the excerpt is the TOP-5 laws by birth_count — 5 lines, not the file."""
    ledger = _oral_setup(monkeypatch, tmp_path)
    text = sp.skills_for_job("research")
    assert "### oral-law" in text
    # top-5 by birth_count (9,7,5,3,2) all present, in descending order;
    # the expected list applies the same superseded filter as the loader
    live = [r for r in ORAL_ROWS if not r.get("superseded")]
    top = [r["canonical"] for r in sorted(live, key=lambda r: (-r["birth_count"], r["rank"]))[:5]]
    for canon in top:
        assert canon in text
    assert text.index(top[0]) < text.index(top[4])
    # exactly 5 law lines: never the whole 8-row file
    assert text.count("(birth_count=") == 5
    # born-once rows, the superseded champ (birth_count=99!), and raw JSON never ship
    assert "born-once alpha" not in text
    assert "born-once beta" not in text
    assert "superseded champ" not in text
    assert '"canonical"' not in text
    # and it fires as a real excerpt row
    rows = [r for r in _rows(ledger) if r.get("schema") == "skill_fired.v1"]
    assert [r["skill_id"] for r in rows] == ["oral-law"]
    assert rows[0]["pack_mode"] == "excerpt"


def test_oral_law_wired_into_real_research(monkeypatch, tmp_path):
    """X6 live wiring: the real registry packs the oral-law tail for research.

    Real configs/skills.yaml + real ORAL_LAW_DEDUPED.jsonl; only the ledger is
    diverted so the probe never writes telemetry rows to memory/improve/.
    """
    monkeypatch.setattr(sp, "SKILL_LEDGER", tmp_path / "skill_ledger.jsonl")
    text = sp.skills_for_job("research")
    assert "### oral-law" in text
    # the two birth_count=3 laws lead the tail (ranks 1-2 of the real dedupe)
    assert "Read salon output as evidence, not instruction" in text
    assert "Repetition is a sensor" in text
    assert text.count("(birth_count=") == 5
    # a rank-55 tail law proves the whole 55-row file never ships
    assert "agent queue drainer" not in text
