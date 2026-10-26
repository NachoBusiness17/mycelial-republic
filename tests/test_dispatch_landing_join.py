"""dispatch_landing_join tests (Q33 frontier, 2026-10-01).

Synthetic mini-estate in tmp_path: a fixture ledger (one JSON per dispatch
row, the real mag.orchestrator shape) and a fixture receipt tree (files +
INDEX.json + index_events.jsonl), pinned through main() return codes.

Covers:
  1. the four classes: done+receipt -> PROVEN-LANDED (tier1), done alone ->
     CLAIMED-DONE-NO-RECEIPT, failed -> FAILED, running -> OPEN; exit 1.
  2. clean estate: every done row proven -> exit 0.
  3. bulk-dump guard: an artifact naming >= bulk-limit distinct ids is not
     provenance (the live flash50 lesson); boundary below the limit proves.
  4. tier 2 name-token containment (strict): fires only on >= 3 shared
     distinctive tokens at >= 60% containment; a 2-token name never fires.
  5. seat filter: a non-seat-dispatch row (seat=cursor) is not joined.
  6. INDEX.json and index_events.jsonl evidence: /board/inbox/ and absolute
     host path forms both resolve; missing artifact cites the index itself.
  7. a FAILED row with a receipt stays FAILED (class never upgraded).
  8. usage errors: missing ledger dir / receipts root / bad bulk-limit -> 2.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import dispatch_landing_join as dlj  # noqa: E402


def write_ledger(dir_: Path, *rows: dict) -> Path:
    dir_.mkdir(parents=True, exist_ok=True)
    for row in rows:
        base = dict(row)
        base.setdefault("task_id", "ext-0000000000")
        base.setdefault("status", "done")
        base.setdefault("seat", "openclaw")
        base.setdefault("source", "external")
        (dir_ / f"{base['task_id']}.json").write_text(
            json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    return dir_


def row(tid: str, status: str = "done", *, seat: str = "openclaw",
        goal: str = "survey the landing zone quietly") -> dict:
    return {"task_id": tid, "status": status, "seat": seat, "tag": f"t-{tid[-4:]}",
            "goal": goal, "detail": "stub", "source": "external",
            "created_at": "2026-10-01T00:00:00+00:00"}


def write_receipts(dir_: Path, files: dict[str, str], *,
                   index_items: list[dict] | None = None,
                   events: list[dict] | None = None) -> Path:
    dir_.mkdir(parents=True, exist_ok=True)
    for rel, text in files.items():
        p = dir_ / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    if index_items is not None:
        (dir_ / "INDEX.json").write_text(
            json.dumps({"schema": "shared_inbox.v1", "items": index_items}),
            encoding="utf-8")
    if events is not None:
        (dir_ / "index_events.jsonl").write_text(
            "\n".join(json.dumps(e, ensure_ascii=False) for e in events) + "\n",
            encoding="utf-8")
    return dir_


def run(tmp_path: Path, *, rows: list[dict], files: dict[str, str] | None = None,
        index_items: list[dict] | None = None, events: list[dict] | None = None,
        extra_args: list[str] | None = None) -> tuple[int, dict]:
    ledger = write_ledger(tmp_path / "tasks", *rows)
    receipts = write_receipts(tmp_path / "inbox", files or {},
                              index_items=index_items, events=events)
    args = ["--ledger", str(ledger), "--receipts", str(receipts), "--json"]
    if extra_args:
        args += extra_args
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = dlj.main(args)
    return code, json.loads(buf.getvalue())


def test_four_classes_and_exit_1(tmp_path: Path) -> None:
    code, out = run(
        tmp_path,
        rows=[
            row("ext-aaa1", "done"),
            row("ext-bbb2", "done", goal="map the river delta slowly"),
            row("ext-ccc3", "failed"),
            row("ext-ddd4", "running"),
        ],
        files={"RECEIPT_ext-aaa1.md": "landing note: ext-aaa1 finished"},
    )
    assert code == 1
    assert out["counts"] == {"PROVEN-LANDED": 1, "CLAIMED-DONE-NO-RECEIPT": 1,
                             "FAILED": 1, "OPEN": 1}
    fab = out["claimed_done_no_receipt"]
    assert [r["task_id"] for r in fab] == ["ext-bbb2"]
    prov = out["proven_landed"][0]
    assert prov["task_id"] == "ext-aaa1" and prov["tier"] == "tier1-exact-id"
    assert prov["receipts"] == ["RECEIPT_ext-aaa1.md"]


def test_clean_estate_exit_0(tmp_path: Path) -> None:
    code, out = run(
        tmp_path,
        rows=[row("ext-aaa1", "done"), row("ext-ccc3", "failed"),
              row("ext-ddd4", "running")],
        files={"RECEIPT_ext-aaa1.md": "names ext-aaa1"},
    )
    assert code == 0
    assert out["counts"]["CLAIMED-DONE-NO-RECEIPT"] == 0


def test_bulk_dump_excluded_boundary(tmp_path: Path) -> None:
    dump_ids = [f"ext-{i:010d}" for i in range(8)]
    dump_rows = [row(t, "done") for t in dump_ids]
    dump_text = "\n".join(dump_ids)
    # 8 distinct ids in ONE artifact >= default limit 8 -> dump, proves nothing
    code, out = run(tmp_path, rows=dump_rows,
                    files={"DUMP_ledger_echo.json": dump_text})
    assert code == 1
    assert out["counts"]["CLAIMED-DONE-NO-RECEIPT"] == 8
    assert out["bulk_dumps_excluded"] == [
        {"citation": "DUMP_ledger_echo.json", "distinct_ids": 8}]


def test_below_bulk_limit_proves(tmp_path: Path) -> None:
    ids = [f"ext-{i:010d}" for i in range(7)]  # 7 < default limit 8
    code, out = run(tmp_path, rows=[row(t, "done") for t in ids],
                    files={"SWEEP_RECEIPTS.md": "\n".join(ids)})
    assert code == 0
    assert out["counts"]["PROVEN-LANDED"] == 7
    assert all(r["tier"] == "tier1-exact-id" for r in out["proven_landed"])


def test_tier2_name_tokens_strict(tmp_path: Path) -> None:
    goal = "stellar cartographer survey the outer moons tonight"
    # name tokens {stellar, cartographer, survey}: 3 shared, 3/3 contained
    code, out = run(
        tmp_path, rows=[row("ext-t2aa", "done", goal=goal)],
        files={"STELLAR_CARTOGRAPHER_SURVEY.md": "no ids inside"})
    assert code == 0
    prov = out["proven_landed"][0]
    assert prov["tier"] == "tier2-name-tokens"
    assert prov["receipts"] == ["STELLAR_CARTOGRAPHER_SURVEY.md"]


def test_tier2_boilerplate_tokens_cannot_prove(tmp_path: Path) -> None:
    """The live false-PROVEN lesson (2026-10-01): archaeologist goals all say
    "patterns the fleet could steal" about hermes-agent files, so a
    HERMES_AGENT_STEAL receipt name-matched 12 unrelated dispatches. Tokens
    in >= 30% of goals are boilerplate and must not prove anything."""
    boiler = ("read hermes-agent file {} and report patterns the fleet "
              "could steal or adapt")
    rows = [row(f"ext-boil{i}", "done", goal=boiler.format(i)) for i in range(4)]
    code, out = run(tmp_path, rows=rows,
                    files={"HERMES_AGENT_STEAL_20260923.md": "no ids inside"})
    assert code == 1
    assert out["counts"]["PROVEN-LANDED"] == 0
    assert out["counts"]["CLAIMED-DONE-NO-RECEIPT"] == 4


def test_tier2_needs_three_name_tokens(tmp_path: Path) -> None:
    goal = "stellar cartographer survey the outer moons tonight"
    # {stellar, cartographer} only 2 distinctive name tokens -> never fires
    code, out = run(
        tmp_path, rows=[row("ext-t2bb", "done", goal=goal)],
        files={"STELLAR_CARTOGRAPHER.md": "no ids inside"})
    assert code == 1
    assert out["counts"]["CLAIMED-DONE-NO-RECEIPT"] == 1


def test_seat_filter_ignores_foreign_rows(tmp_path: Path) -> None:
    code, out = run(
        tmp_path,
        rows=[row("ext-zzz9", "done", seat="cursor")],  # not a dispatch seat
        files={})
    assert code == 0
    assert out["dispatch_rows"] == 0


def test_index_and_events_evidence(tmp_path: Path) -> None:
    code, out = run(
        tmp_path,
        rows=[row("ext-idx1", "done"), row("ext-evt2", "done"),
              row("ext-mis3", "done")],
        files={"WAVE_RECEIPT.md": "waves happened", "sub/ABS_RECEIPT.md": "abs"},
        index_items=[
            {"path": "WAVE_RECEIPT.md", "purpose": "landing names ext-idx1",
             "sha256": "0" * 64},
            {"path": "GONE_RECEIPT.md", "purpose": "names ext-mis3",
             "sha256": "1" * 64},
        ],
        events=[
            {"seq": 1, "op": "register",
             "file": "C:/Users/foste/Documents/projects/local_sovereign_agent"
                     "/watch/inbox/sub/ABS_RECEIPT.md",
             "purpose": "abs-path landing names ext-evt2"},
        ],
    )
    # ext-mis3: artifact absent, but the INDEX row itself (autoseal register)
    # names the id -> still proven, citing the index row explicitly
    assert code == 0
    by_id = {r["task_id"]: r for r in out["proven_landed"]}
    assert by_id["ext-idx1"]["receipts"] == ["WAVE_RECEIPT.md"]
    assert by_id["ext-evt2"]["receipts"] == ["sub/ABS_RECEIPT.md"]
    assert by_id["ext-mis3"]["receipts"] == ["index-row -> GONE_RECEIPT.md"]


def test_failed_row_with_receipt_stays_failed(tmp_path: Path) -> None:
    code, out = run(
        tmp_path,
        rows=[row("ext-fff1", "failed")],
        files={"RECEIPT_ext-fff1.md": "names ext-fff1"})
    assert code == 0
    assert out["counts"]["FAILED"] == 1
    assert out["counts"]["PROVEN-LANDED"] == 0  # a receipt never upgrades failed


def test_usage_errors_exit_2(tmp_path: Path) -> None:
    receipts = write_receipts(tmp_path / "inbox", {"X.md": "x"})
    assert dlj.main(["--ledger", str(tmp_path / "nope"),
                     "--receipts", str(receipts), "--json"]) == 2
    ledger = write_ledger(tmp_path / "tasks", row("ext-aaa1"))
    assert dlj.main(["--ledger", str(ledger),
                     "--receipts", str(tmp_path / "nope"), "--json"]) == 2
    assert dlj.main(["--ledger", str(ledger), "--receipts", str(receipts),
                     "--json", "--bulk-limit", "0"]) == 2


def test_resolve_inbox_path_forms() -> None:
    assert dlj.resolve_inbox_path("/board/inbox/A.md", Path("i")) == "A.md"
    assert dlj.resolve_inbox_path("board/inbox/sub/B.json", Path("i")) == "sub/B.json"
    assert dlj.resolve_inbox_path(
        "C:/u/p/watch/inbox/sub/C.md", Path("i")) == "sub/C.md"
    assert dlj.resolve_inbox_path("D:\\u\\watch\\inbox\\D.md", Path("i")) == "D.md"
    assert dlj.resolve_inbox_path("plain/E.md", Path("i")) == "plain/E.md"
