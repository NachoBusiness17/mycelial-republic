"""social_rsi tests (2026-10-04, X_INTEL_PAPERS_20261004.md section 6 v0).

Fixture contract for tools/social_rsi.py: the tool is a QUERY + PACKET
surface over existing ledgers (wired-organ law, no new store), so every
fixture is a tmp-path mag root - fake queue/lanes/*/trail.jsonl, a fake
logs/failure_kb.jsonl, a fake watch/inbox - and the tool's --root points
at it. Count assertions are normalizer-arm-independent: rows meant to
share a bucket carry byte-identical detail strings, rows meant to split
carry structurally different details, so counts hold whether the keying
arm is mag.lane_runner.normalize_detail or the fallback tokenizer.

What is proven here:
- roll-up counts group windowed CYCLE_FAIL rows by detail class with
  per-lane breakdown, first/last-seen from bytes, and out-of-window rows
  (older than --days) excluded from counts;
- the failure_kb join counts a windowed known sig whose detail matches
  the pattern class (same raw string => same bucket in any arm);
- evidence pairs detect a CYCLE_FAIL followed later in the SAME lane by
  a green CYCLE (gap in seconds from the ts delta) and by a FIX-family
  event, and lanes with no later recovery row yield no pair;
- --check writes nothing (stdout only); --packets writes
  watch/inbox/social_rsi/packet_<slug>_<date>.md containing the pattern
  with its instrument named, the SYNTHESIS ASK citing
  watch/inbox/IMAGE_BLASTER_GO_20261003.md and the
  .agents/skills/image-blast/SKILL.md template with all five card rules,
  and the promote-gate footer (mag.cmd promote --apply stays the commit,
  autonomously drafted, humanly promoted);
- text law: zero em/en dashes in any packet byte even when a quoted
  trail detail carries one (scrubbed on the way out);
- CLI exits 2 on no action flag and on a root with no queue/lanes.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

# Module import, not from-imports: keeps tool helpers out of this
# module's test-prefixed collection namespace (house rule from
# tests/test_census_drift_patrol.py).
import tools.social_rsi as sr

NOW = datetime.now(timezone.utc)
EMDASHES = ("\u2014", "\u2013", "\u2012", "\u2015")

OSERR_DETAIL = ("EXC OSError: [Errno 22] Invalid argument retry runner path: "
                "'/app/queue/lanes/builder/runner_state.json'")
RATE_DETAIL = "lane-down: HTTP Error 429: Too Many Requests"


def z(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def row(event: str, ts: datetime, detail: str) -> dict:
    return {"ts": z(ts), "actor": "fixture-cage", "event": event,
            "detail": detail, "artifacts": []}


def write_trail(root: Path, lane: str, rows: list) -> Path:
    d = root / "queue" / "lanes" / lane
    d.mkdir(parents=True, exist_ok=True)
    path = d / "trail.jsonl"
    with path.open("w", encoding="utf-8") as h:
        for r in rows:
            h.write(json.dumps(r) + "\n")
    return path


def build_root(tmp_path: Path) -> Path:
    """Fake mag root. builder: 3 OSERR fails then a green CYCLE (the
    before/after pair). research: 2 OSERR fails, nothing after (no
    pair). elder: 2 RATE fails then a FIX-family row, plus one RATE fail
    20d old (outside the default 14d window). The third builder fail
    carries a trailing em-dash note that lands past both normalizer
    arms' first-6-token window, so it stays in the OSERR bucket and
    proves outbound scrubbing without splitting the class."""
    root = tmp_path / "mag"
    root.mkdir()
    t0 = NOW - timedelta(days=1)

    fails_builder = [row("CYCLE_FAIL", t0 + timedelta(seconds=i * 60),
                         OSERR_DETAIL) for i in range(3)]
    fails_builder[2]["detail"] = OSERR_DETAIL + " \u2014 retries exhausted"
    write_trail(root, "builder", fails_builder + [
        row("CYCLE", t0 + timedelta(seconds=600), "drops gated=0; queue on surface")])

    write_trail(root, "research", [
        row("CYCLE_FAIL", t0 + timedelta(minutes=5), OSERR_DETAIL),
        row("CYCLE_FAIL", t0 + timedelta(minutes=6), OSERR_DETAIL)])

    write_trail(root, "elder", [
        row("CYCLE_FAIL", NOW - timedelta(days=20), RATE_DETAIL),  # out of window
        row("CYCLE_FAIL", t0 + timedelta(minutes=10), RATE_DETAIL),
        row("CYCLE_FAIL", t0 + timedelta(minutes=11), RATE_DETAIL),
        row("LEASE_LAW_FIX_APPLIED", t0 + timedelta(minutes=30),
            "fix applied: backoff lane-down guard")])

    fkb = root / "logs"
    fkb.mkdir(parents=True)
    with (fkb / "failure_kb.jsonl").open("w", encoding="utf-8") as h:
        h.write(json.dumps({"ts": (NOW - timedelta(days=20)).isoformat(),
                            "kind": "crash_loop", "sig": "old:out-of-window",
                            "detail": OSERR_DETAIL}) + "\n")
        h.write(json.dumps({"ts": (NOW - timedelta(days=2)).isoformat(),
                            "kind": "crash_loop", "sig": "crash_loop:ab12",
                            "detail": OSERR_DETAIL}) + "\n")
        h.write(json.dumps({"ts": (NOW - timedelta(days=2)).isoformat(),
                            "kind": "swarm_health", "sig": "_:zz99",
                            "detail": "no live seats"}) + "\n")

    inbox = root / "watch" / "inbox"
    inbox.mkdir(parents=True)
    (inbox / "OSERR_RECEIPT_20261004.md").write_text(
        "# errno 22 receipt\n\nThe lane cage crashed on OSError errno 22 "
        "Invalid argument writing runner_state.json. Cure: path guard.\n",
        encoding="utf-8")
    (inbox / "NOMATCH.md").write_text(
        "# unrelated\n\nNothing about lane cages here.\n", encoding="utf-8")
    return root


def rollup_fixture(root: Path, days: int = 14):
    normalize, _name = sr._load_normalize_detail()
    lanes, _summary = sr.load_trails(root)
    cutoff = NOW - timedelta(days=days)
    fkb = sr.load_fkb_window(root, cutoff)
    return sr.rollup(lanes, cutoff, normalize, fkb), lanes, normalize


def test_rollup_counts_lanes_and_window(tmp_path):
    root = build_root(tmp_path)
    patterns, _lanes, _normalize = rollup_fixture(root)

    # two classes only: OSERR (builder 3 + research 2) and RATE (elder 2;
    # the 20d-old row is outside the 14d window and uncounted)
    assert len(patterns) == 2
    top, second = patterns
    assert top.count == 5
    assert top.lanes == {"builder": 3, "research": 2}
    assert second.count == 2
    assert list(second.lanes) == ["elder"]

    # first/last-seen come from the fixture bytes (t0 family; z() drops
    # microseconds so equality is exact), and the example detail proves
    # the em-dash-carrying variant was seen
    t0 = (NOW - timedelta(days=1)).replace(microsecond=0)
    assert top.first_seen == t0
    assert top.last_seen >= top.first_seen
    assert "runner_state.json" in top.example_detail

    # determinism: same tree, same ranking (count desc, key asc)
    again, _l, _n = rollup_fixture(root)
    assert [(p.key, p.count) for p in again] == [(p.key, p.count) for p in patterns]


def test_failure_kb_join_counts_windowed_known_sig(tmp_path):
    root = build_root(tmp_path)
    patterns, _lanes, _normalize = rollup_fixture(root)
    top = patterns[0]
    # one in-window fkb row carries the identical detail (same bucket in
    # any arm); the 20d-old row and the unrelated sig do not join
    assert top.fkb_count == 1
    assert top.fkb_sigs == ["crash_loop:ab12"]
    assert patterns[1].fkb_count == 0


def test_evidence_pairs_green_cycle_and_fix_row(tmp_path):
    root = build_root(tmp_path)
    patterns, lanes, normalize = rollup_fixture(root)
    top, rate = patterns

    # builder: last OSERR fail at t0+120s, first later green CYCLE at
    # t0+600s => one pair, gap 480s; research has no row after its fails
    pairs = sr.evidence_pairs(top, lanes, normalize)
    assert len(pairs) == 1
    assert pairs[0].lane == "builder"
    assert pairs[0].recovery_event == "CYCLE"
    assert pairs[0].gap_s == pytest.approx(480.0)

    # elder: RATE fails then LEASE_LAW_FIX_APPLIED => FIX-family recovery
    rate_pairs = sr.evidence_pairs(rate, lanes, normalize)
    assert len(rate_pairs) == 1
    assert rate_pairs[0].lane == "elder"
    assert rate_pairs[0].recovery_event == "LEASE_LAW_FIX_APPLIED"
    assert sr.is_fix_event("LEASE_LAW_FIX_APPLIED")
    assert not sr.is_fix_event("CYCLE")


def test_check_prints_table_and_writes_nothing(tmp_path, capsys):
    root = build_root(tmp_path)
    rc = sr.main(["--check", "--root", str(root)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "PATTERN ROLL-UP" in out
    assert "queue/lanes/*/trail.jsonl" in out
    assert "failure_kb window rows scanned: 2" in out
    # stdout only: no packet dir created
    assert not (root / "watch" / "inbox" / "social_rsi").exists()


def test_packets_content_shape_and_footer(tmp_path, capsys):
    root = build_root(tmp_path)
    rc = sr.main(["--packets", "--top", "1", "--root", str(root)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "packet written:" in out

    packet_dir = root / "watch" / "inbox" / "social_rsi"
    packets = sorted(packet_dir.glob("packet_*.md"))
    assert len(packets) == 1
    name = packets[0].name
    assert name.endswith(f"_{NOW.date().isoformat()}.md")
    text = packets[0].read_text(encoding="utf-8")

    # the pattern with its instrument named
    assert "CYCLE_FAIL rows" in text
    assert "queue/lanes/*/trail.jsonl" in text
    assert "logs/failure_kb.jsonl" in text
    assert "lanes affected: builder(3), research(2)" in text

    # the evidence pair with before/after timestamps
    assert "CYCLE" in text and "LEASE_LAW" not in text  # top-1 packet only
    assert "gap 480s" in text

    # the receipt grep landed (cap 3, path cited)
    assert "OSERR_RECEIPT_20261004.md" in text
    assert "NOMATCH.md" not in text

    # the SYNTHESIS ASK block: template + receipt cited, all five rules
    assert "SYNTHESIS ASK" in text
    assert "watch/inbox/IMAGE_BLASTER_GO_20261003.md" in text
    assert ".agents/skills/image-blast/SKILL.md" in text
    for rule in ("argument-hint", "one verb", "runnable command",
                 "gates", "Final response:"):
        assert rule in text

    # the promote-gate footer: human commit named (the phrase wraps
    # across the packet's line width, so assert its fragments)
    assert "mag.cmd promote" in text
    assert "--apply" in text
    assert "the commit stays human" in text
    assert "autonomously drafted" in text
    assert "humanly" in text and "promoted" in text


def test_packet_text_law_zero_emdashes_even_with_dirty_detail(tmp_path):
    root = build_root(tmp_path)
    sr.main(["--packets", "--top", "2", "--root", str(root)])
    packets = sorted((root / "watch" / "inbox" / "social_rsi").glob("packet_*.md"))
    assert len(packets) == 2  # both classes got packets
    for packet in packets:
        text = packet.read_text(encoding="utf-8")
        for ch in EMDASHES:
            assert ch not in text, f"{ch!r} leaked into {packet.name}"


def test_cli_usage_and_missing_root(tmp_path, capsys):
    assert sr.main([]) == 2  # no action flag
    empty = tmp_path / "empty"
    empty.mkdir()
    assert sr.main(["--check", "--root", str(empty)]) == 2
