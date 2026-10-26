"""Doctrine arbiter tests (R10, 2026-09-30).

Fixture contract for tools/doctrine_arbiter.py: the pre-registration law
voids any item whose four-tuple {id, source_verdict, predicted_outcome,
deadline} is broken (missing/empty/uncheckable prediction, unparseable
deadline, missing source) and VOID items are never checked; duplicate ids
refuse hard; the check pass reads the four estate instruments (gps
ledger pass_rate, duel table win_rate, parity gate latest.json, anomaly
counts) and scores VINDICATED / EXPIRED / PENDING with the deadline
deciding expiry; terminal statuses freeze (a second check adds no rows);
EXPIRED flags a retire candidate and nothing is ever auto-removed - only
the explicit retire subcommand closes an item, and only a terminal one;
the ledger is append-only (registrations are never edited; state is a
fold); exit codes 0 ok / 1 attention (expired or void registration) /
2 error (duplicate id, retire on non-terminal, dark instrument).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Module import, not from-imports: keeps tool helpers out of this
# module's test-prefixed collection namespace (house rule from
# tests/test_census_drift_patrol.py).
import tools.doctrine_arbiter as da


# ------------------------------------------------------------- helpers -----

def register(tmp_path: Path, item_id: str, *, instrument: str = "",
             metric: str = "", op: str = "", value: str = None,
             selector: dict | None = None, deadline: str = "2099-01-01",
             source: str = "watch/inbox/some_receipt.md", kind: str = "rib",
             claim: str = "doctrine claim") -> int:
    argv = ["register", "--ledger", str(tmp_path / "LEDGER.jsonl"),
            "--id", item_id, "--kind", kind, "--source-verdict", source,
            "--claim", claim, "--deadline", deadline]
    if instrument:
        argv += ["--instrument", instrument]
    if metric:
        argv += ["--metric", metric]
    if op:
        argv += ["--op", op]
    if value is not None:
        argv += ["--value", value]
    for key, val in (selector or {}).items():
        argv += ["--sel", f"{key}={val}"]
    return da.main(argv)


def ledger_rows(tmp_path: Path) -> list[dict]:
    return da.read_rows(tmp_path / "LEDGER.jsonl")


def folded(tmp_path: Path) -> dict[str, da.DoctrineItem]:
    return da.fold_ledger(ledger_rows(tmp_path))


def check(tmp_path: Path, **paths: Path) -> int:
    argv = ["check", "--ledger", str(tmp_path / "LEDGER.jsonl"),
            "--scorecard-out", str(tmp_path / "scorecard.json")]
    flag_for = {"gps_db": "--gps-db", "duels": "--duels",
                "parity_latest": "--parity-latest",
                "anomaly_steps": "--anomaly-steps",
                "anomaly_oral": "--anomaly-oral",
                "anomaly_ledger": "--anomaly-ledger",
                "anomaly_enum_map": "--anomaly-enum-map"}
    for key, path in paths.items():
        argv += [flag_for[key], str(path)]
    return da.main(argv)


def gps_db(tmp_path: Path, model: str, shape: str, rate: float, n: int) -> Path:
    from tools.gps_mcp.ledger import CapabilityLedger
    db = tmp_path / "gps.db3"
    ledger = CapabilityLedger(db)
    ledger.upsert_measurement(model, shape, rate, n, None, "2026-09-30T00:00:00Z")
    ledger.close()
    return db


def duels(tmp_path: Path, rows: list[dict]) -> Path:
    path = tmp_path / "duels.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    return path


def duel(a: str, b: str, winner: str) -> dict:
    return {"ask_id": "x", "a_model": a, "b_model": b, "winner": winner,
            "ts": "2026-09-30T00:00:00Z"}


def parity_latest(tmp_path: Path, parity: bool, mode: str = "full",
                  diverged: int = 0) -> Path:
    path = tmp_path / "latest.json"
    path.write_text(json.dumps({
        "mode": mode, "parity": parity, "per_family": {
            "mountain": {"diverged_seqs": diverged, "sequences": 20}},
    }), encoding="utf-8")
    return path


def anomaly_streams(tmp_path: Path, *, steps_rows: list | None = None,
                    oral_rows: list | None = None,
                    burns_rows: list | None = None,
                    census: dict | None = None) -> dict[str, Path]:
    steps_rows = steps_rows if steps_rows is not None else [
        {"ts": "2026-09-30T00:00:00Z", "step_hash": "a" * 16},
        {"ts": "2026-09-30T00:00:01Z", "step_hash": "b" * 16},
    ]
    oral_rows = oral_rows if oral_rows is not None else [
        {"thread_id": "t1", "ts": "2026-09-30T00:00:00Z"},
    ]
    receipt = tmp_path / "receipt.md"
    receipt.write_text("ok", encoding="utf-8")
    burns_rows = burns_rows if burns_rows is not None else [
        {"ts": "t", "slug": "a", "verdict": "steal", "landing": str(receipt)},
    ]
    census = census if census is not None else {
        "steal": {"enum": "LANDED", "review": False}}
    steps = tmp_path / "steps.jsonl"
    oral = tmp_path / "oral.jsonl"
    ledger = tmp_path / "burns.jsonl"
    enum_map = tmp_path / "map.json"
    for path, rows in ((steps, steps_rows), (oral, oral_rows),
                       (ledger, burns_rows)):
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")
    enum_map.write_text(json.dumps({"census": census}), encoding="utf-8")
    return {"anomaly_steps": steps, "anomaly_oral": oral,
            "anomaly_ledger": ledger, "anomaly_enum_map": enum_map}


# ----------------------------------------------- pre-registration law ------

class TestPreRegistrationLaw:
    def test_no_prediction_is_void_at_registration(self, tmp_path, capsys):
        code = register(tmp_path, "d1", source="watch/inbox/r.md")
        assert code == 1
        rows = ledger_rows(tmp_path)
        assert len(rows) == 1
        assert rows[0]["status"] == "VOID"
        assert any("pre-registration law" in r for r in rows[0]["void_reasons"])
        assert folded(tmp_path)["d1"].status == "VOID"

    def test_missing_deadline_and_source_void(self, tmp_path):
        assert register(tmp_path, "d1", deadline="") == 1
        assert register(tmp_path, "d2", source="") == 1
        assert register(tmp_path, "d3", deadline="not-a-date") == 1
        items = folded(tmp_path)
        assert {i.status for i in items.values()} == {"VOID"}
        reasons = {i: items[i].void_reasons for i in items}
        assert any("deadline" in r for rs in reasons.values() for r in rs)
        assert any("source_verdict" in r for rs in reasons.values() for r in rs)

    def test_uncheckable_predictions_void(self, tmp_path):
        # unknown instrument / metric / op, missing selector key, junk
        # selector key, bad anomaly surface: none can ever be measured,
        # so none are doctrine.
        assert register(tmp_path, "d1", instrument="tarot", metric="vibes",
                        op=">=", value="0.5") == 1
        assert register(tmp_path, "d2", instrument="gps_ledger",
                        metric="vibes", op=">=", value="0.5") == 1
        assert register(tmp_path, "d3", instrument="duel_table",
                        metric="win_rate", op="~=", value="0.5",
                        selector={"model": "m"}) == 1
        assert register(tmp_path, "d4", instrument="gps_ledger",
                        metric="pass_rate", op=">=", value="0.5",
                        selector={"model_id": "m"}) == 1
        assert register(tmp_path, "d5", instrument="anomaly_counts",
                        metric="anomaly_count", op="<=", value="0",
                        selector={"surface": "dreams"}) == 1
        assert {i.status for i in folded(tmp_path).values()} == {"VOID"}

    def test_void_items_are_never_checked(self, tmp_path):
        register(tmp_path, "d1", instrument="gps_ledger", metric="pass_rate",
                 op=">=", value="0.5", selector={"model_id": "m",
                                                 "task_shape": "s"})
        # d1 above is VALID; now a void twin with no instrument streams
        # wired at all - check must not touch any instrument for VOID ids
        register(tmp_path, "d2", instrument="", metric="", op="", value="0")
        rows_before = len(ledger_rows(tmp_path))
        # check with the gps stream deliberately dark: only d1 (PENDING)
        # forces the read, so this is exit 2 - proving VOID d2 was skipped
        # would need d1 gone; instead prove by folding: no check rows for d2
        assert check(tmp_path, gps_db=tmp_path / "missing.db3") == 2
        assert not any(r.get("id") == "d2" and r["type"] == "check"
                       for r in ledger_rows(tmp_path))
        assert len([r for r in ledger_rows(tmp_path)]) == rows_before

    def test_duplicate_id_refuses_and_writes_nothing(self, tmp_path, capsys):
        assert register(tmp_path, "d1", instrument="parity_gate",
                        metric="parity_ok", op="==", value="true") == 0
        rows_before = len(ledger_rows(tmp_path))
        assert register(tmp_path, "d1", instrument="parity_gate",
                        metric="parity_ok", op="==", value="true") == 2
        assert len(ledger_rows(tmp_path)) == rows_before

    def test_valid_registration_is_pending(self, tmp_path, capsys):
        code = register(tmp_path, "d1", instrument="parity_gate",
                        metric="parity_ok", op="==", value="true",
                        kind="spec_amendment")
        assert code == 0
        rows = ledger_rows(tmp_path)
        assert rows[0]["status"] == "PENDING"
        assert rows[0]["predicted_outcome"]["value"] is True
        item = folded(tmp_path)["d1"]
        assert item.status == "PENDING"
        assert item.predicted_outcome["instrument"] == "parity_gate"


# --------------------------------------------------------- instruments -----

class TestGpsLedgerInstrument:
    def pred(self, tmp_path, value: str, deadline: str = "2099-01-01") -> None:
        register(tmp_path, "g1", instrument="gps_ledger", metric="pass_rate",
                 op=">=", value=value,
                 selector={"model_id": "gemma:2b", "task_shape": "refactor"},
                 deadline=deadline)

    def test_vindicated_when_rate_meets_prediction(self, tmp_path):
        self.pred(tmp_path, "0.6")
        db = gps_db(tmp_path, "gemma:2b", "refactor", 0.75, 40)
        assert check(tmp_path, gps_db=db) == 0
        item = folded(tmp_path)["g1"]
        assert item.status == "VINDICATED"
        row = item.checks[-1]
        assert row["measured"] == 0.75 and row["satisfies"] is True
        assert row["instrument_saw"]["sample_size"] == 40

    def test_expired_when_deadline_passes_unmet(self, tmp_path):
        self.pred(tmp_path, "0.9", deadline="2026-01-01")
        db = gps_db(tmp_path, "gemma:2b", "refactor", 0.75, 40)
        assert check(tmp_path, gps_db=db) == 1
        item = folded(tmp_path)["g1"]
        assert item.status == "EXPIRED"
        assert item.expired_ts
        assert item.retire_candidate

    def test_unmeasured_pair_is_pending_not_error(self, tmp_path):
        self.pred(tmp_path, "0.6")
        db = gps_db(tmp_path, "other-model", "refactor", 0.9, 5)
        assert check(tmp_path, gps_db=db) == 0
        assert folded(tmp_path)["g1"].status == "PENDING"

    def test_missing_db_is_instrument_error(self, tmp_path):
        self.pred(tmp_path, "0.6")
        assert check(tmp_path, gps_db=tmp_path / "dark.db3") == 2


class TestDuelTableInstrument:
    def test_win_rate_uses_logical_sides(self, tmp_path):
        register(tmp_path, "q1", instrument="duel_table", metric="win_rate",
                 op=">=", value="0.5",
                 selector={"model": "z-ai/glm-5.3-prime"})
        path = duels(tmp_path, [
            duel("z-ai/glm-5.3-prime", "qwen/qwen3.7-flash", "A"),   # win
            duel("qwen/qwen3.7-flash", "z-ai/glm-5.3-prime", "B"),   # glm is B: win
            duel("z-ai/glm-5.3-prime", "qwen/qwen3.7-flash", "B"),   # loss
            duel("z-ai/glm-5.3-prime", "qwen/qwen3.7-flash", "TIE"),
            duel("deepseek/x", "qwen/qwen3.7-flash", "A"),           # not ours
        ])
        assert check(tmp_path, duels=path) == 0
        item = folded(tmp_path)["q1"]
        assert item.status == "VINDICATED"
        saw = item.checks[-1]["instrument_saw"]
        assert saw["decided"] == 3 and saw["win_rate"] == 2 / 3
        assert saw["ties"] == 1

    def test_no_decided_duels_is_no_data_not_vindication(self, tmp_path):
        register(tmp_path, "q1", instrument="duel_table", metric="win_rate",
                 op=">=", value="0.5", selector={"model": "m"},
                 deadline="2026-01-01")
        path = duels(tmp_path, [duel("m", "x", "TIE"), duel("m", "x", "UNPARSED")])
        # no decided duels and deadline long past: prediction never
        # materialized -> EXPIRED (win_rate undefined is not vindication)
        assert check(tmp_path, duels=path) == 1
        item = folded(tmp_path)["q1"]
        assert item.status == "EXPIRED"
        assert item.checks[-1]["measured"] is None

    def test_decided_count_metric_checks_zero(self, tmp_path):
        register(tmp_path, "q0", instrument="duel_table", metric="decided",
                 op="<=", value="0", selector={"model": "never-fought"})
        path = duels(tmp_path, [duel("a", "b", "A")])
        assert check(tmp_path, duels=path) == 0
        assert folded(tmp_path)["q0"].status == "VINDICATED"

    def test_missing_duels_ledger_is_instrument_error(self, tmp_path):
        register(tmp_path, "q1", instrument="duel_table", metric="win_rate",
                 op=">=", value="0.5", selector={"model": "m"})
        assert check(tmp_path, duels=tmp_path / "dark.jsonl") == 2


class TestParityGateInstrument:
    def register_parity(self, tmp_path, op="==", value="true",
                        selector=None, deadline="2099-01-01"):
        register(tmp_path, "p1", instrument="parity_gate", metric="parity_ok",
                 op=op, value=value, selector=selector, deadline=deadline)

    def test_parity_true_vindicates(self, tmp_path):
        self.register_parity(tmp_path)
        latest = parity_latest(tmp_path, parity=True)
        assert check(tmp_path, parity_latest=latest) == 0
        assert folded(tmp_path)["p1"].status == "VINDICATED"

    def test_parity_false_expires_past_deadline(self, tmp_path):
        self.register_parity(tmp_path, deadline="2026-01-01")
        latest = parity_latest(tmp_path, parity=False)
        assert check(tmp_path, parity_latest=latest) == 1
        assert folded(tmp_path)["p1"].status == "EXPIRED"

    def test_mode_selector_mismatch_is_no_data(self, tmp_path):
        self.register_parity(tmp_path, deadline="2026-01-01",
                             selector={"mode": "quick"})
        latest = parity_latest(tmp_path, parity=False, mode="full")
        # wrong profile for the claim: not an error, and parity_false on a
        # full run must not be read as evidence about the quick claim
        assert check(tmp_path, parity_latest=latest) == 1
        item = folded(tmp_path)["p1"]
        assert item.status == "EXPIRED"
        assert item.checks[-1]["measured"] is None

    def test_diverged_seqs_metric(self, tmp_path):
        register(tmp_path, "p2", instrument="parity_gate",
                 metric="diverged_seqs", op="<=", value="0")
        latest = parity_latest(tmp_path, parity=True, diverged=0)
        assert check(tmp_path, parity_latest=latest) == 0
        assert folded(tmp_path)["p2"].status == "VINDICATED"

    def test_missing_latest_json_is_instrument_error(self, tmp_path):
        self.register_parity(tmp_path)
        assert check(tmp_path, parity_latest=tmp_path / "dark.json") == 2


class TestAnomalyCountsInstrument:
    def register_anomaly(self, tmp_path, op="<=", value="0", selector=None,
                         deadline="2099-01-01", item_id="a1"):
        register(tmp_path, item_id, instrument="anomaly_counts",
                 metric="anomaly_count", op=op, value=value,
                 selector=selector, deadline=deadline)

    def test_clean_streams_vindicate_zero(self, tmp_path):
        self.register_anomaly(tmp_path)
        assert check(tmp_path, **anomaly_streams(tmp_path)) == 0
        assert folded(tmp_path)["a1"].status == "VINDICATED"

    def test_anomalous_rows_count_and_expire(self, tmp_path):
        self.register_anomaly(tmp_path, deadline="2026-01-01")
        streams = anomaly_streams(
            tmp_path,
            steps_rows=[  # one descent (1 anomalous row)
                {"ts": "2026-09-30T00:00:05Z", "step_hash": "a" * 16},
                {"ts": "2026-09-30T00:00:01Z", "step_hash": "b" * 16},
            ],
            burns_rows=[  # one fallback_unknown verdict (1 anomalous row)
                {"ts": "t", "slug": "z", "verdict": "zzz-nothing-matches",
                 "landing": str(tmp_path / "receipt.md")},
            ],
        )
        assert check(tmp_path, **streams) == 1
        item = folded(tmp_path)["a1"]
        assert item.status == "EXPIRED"
        assert item.checks[-1]["measured"] == 2  # rows, not classes

    def test_surface_selector_scopes_the_count(self, tmp_path):
        self.register_anomaly(tmp_path, selector={"surface": "oral_law_index"})
        streams = anomaly_streams(
            tmp_path,
            steps_rows=[  # anomaly lives on steps, claim watches oral
                {"ts": "2026-09-30T00:00:05Z", "step_hash": "a" * 16},
                {"ts": "2026-09-30T00:00:01Z", "step_hash": "b" * 16},
            ],
        )
        assert check(tmp_path, **streams) == 0
        assert folded(tmp_path)["a1"].status == "VINDICATED"

    def test_missing_stream_is_instrument_error(self, tmp_path):
        self.register_anomaly(tmp_path)
        assert check(tmp_path, anomaly_steps=tmp_path / "dark.jsonl",
                     anomaly_oral=tmp_path / "dark2.jsonl",
                     anomaly_ledger=tmp_path / "dark3.jsonl",
                     anomaly_enum_map=tmp_path / "dark4.json") == 2


# ---------------------------------------------------- lifecycle + gates ----

class TestLifecycle:
    def seed(self, tmp_path, deadline: str = "2099-01-01"):
        register(tmp_path, "life", instrument="parity_gate",
                 metric="parity_ok", op="==", value="true",
                 deadline=deadline)

    def test_pending_records_evidence_each_pass(self, tmp_path):
        self.seed(tmp_path)
        latest = parity_latest(tmp_path, parity=False)
        assert check(tmp_path, parity_latest=latest) == 0
        assert check(tmp_path, parity_latest=latest) == 0
        item = folded(tmp_path)["life"]
        assert item.status == "PENDING"
        assert len(item.checks) == 2  # each pass banks what it saw

    def test_vindicated_freezes_no_further_rows(self, tmp_path):
        self.seed(tmp_path)
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, True)) == 0
        rows_after_win = len(ledger_rows(tmp_path))
        # later drift to parity=False must NOT un-vindicate or even look
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, False)) == 0
        assert len(ledger_rows(tmp_path)) == rows_after_win
        assert folded(tmp_path)["life"].status == "VINDICATED"

    def test_expired_freezes_and_flags_retire_candidate(self, tmp_path):
        self.seed(tmp_path, deadline="2026-01-01")
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, False)) == 1
        rows_after_expiry = len(ledger_rows(tmp_path))
        # a second pass (now even parity=True, too late) changes nothing:
        # never auto-removed, never un-expired
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, True)) == 1
        assert len(ledger_rows(tmp_path)) == rows_after_expiry
        item = folded(tmp_path)["life"]
        assert item.status == "EXPIRED" and item.retire_candidate

    def test_late_truth_is_not_vindication(self, tmp_path):
        # prediction holds TODAY but the deadline passed yesterday: the
        # pre-registered claim was "holds by <deadline>", and no check
        # ran inside the term -> EXPIRED, not VINDICATED
        self.seed(tmp_path, deadline="2026-01-01")
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, True)) == 1
        item = folded(tmp_path)["life"]
        assert item.status == "EXPIRED"
        assert item.checks[-1]["satisfies"] is True  # true now, late

    def test_retire_operator_gate(self, tmp_path, capsys):
        self.seed(tmp_path, deadline="2026-01-01")
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, False)) == 1
        # PENDING refusal needs a pending item: register a second one
        register(tmp_path, "still-live", instrument="parity_gate",
                 metric="parity_ok", op="==", value="true")
        assert da.main(["retire", "--ledger", str(tmp_path / "LEDGER.jsonl"),
                        "--id", "still-live", "--note", "early"]) == 2
        assert da.main(["retire", "--ledger", str(tmp_path / "LEDGER.jsonl"),
                        "--id", "ghost"]) == 2
        assert da.main(["retire", "--ledger", str(tmp_path / "LEDGER.jsonl"),
                        "--id", "life", "--note", "operator: superseded"]) == 0
        items = folded(tmp_path)
        assert items["life"].status == "RETIRED"
        assert items["life"].retire_note == "operator: superseded"
        assert items["still-live"].status == "PENDING"  # untouched
        # retired stays retired under further checks
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, True)) == 0
        assert folded(tmp_path)["life"].status == "RETIRED"

    def test_registration_row_never_edited(self, tmp_path):
        self.seed(tmp_path, deadline="2026-01-01")
        reg_line_before = None
        path = tmp_path / "LEDGER.jsonl"
        with path.open(encoding="utf-8") as handle:
            reg_line_before = handle.readline()
        check(tmp_path, parity_latest=parity_latest(tmp_path, False))
        da.main(["retire", "--ledger", str(path), "--id", "life", "--note", "x"])
        with path.open(encoding="utf-8") as handle:
            assert handle.readline() == reg_line_before  # append-only


# ------------------------------------------------------------ scorecard ----

class TestScorecard:
    def test_check_writes_artifact_and_orders_expired_first(self, tmp_path,
                                                             capsys):
        register(tmp_path, "win", instrument="parity_gate",
                 metric="parity_ok", op="==", value="true")
        register(tmp_path, "lose", instrument="parity_gate",
                 metric="parity_ok", op="==", value="true",
                 deadline="2026-01-01")
        assert check(tmp_path, parity_latest=parity_latest(tmp_path, True)) == 1
        out = tmp_path / "scorecard.json"
        doc = json.loads(out.read_text(encoding="utf-8"))
        assert doc["schema"] == "doctrine_scorecard.v1"
        assert doc["summary"] == {"PENDING": 0, "VINDICATED": 1, "EXPIRED": 1,
                                  "VOID": 0, "RETIRED": 0}
        assert doc["retire_candidates"] == ["lose"]
        assert doc["items"][0]["id"] == "lose"
        printed = capsys.readouterr().out
        assert "DOCTRINE SCORECARD" in printed
        assert "RETIRE CANDIDATE" in printed
        assert "lose" in printed and "win" in printed

    def test_scorecard_subcommand_writes_nothing(self, tmp_path, capsys):
        register(tmp_path, "win", instrument="parity_gate",
                 metric="parity_ok", op="==", value="true")
        rows_before = ledger_rows(tmp_path)
        code = da.main(["scorecard", "--ledger", str(tmp_path / "LEDGER.jsonl")])
        assert code == 0
        assert ledger_rows(tmp_path) == rows_before
        assert "PENDING" in capsys.readouterr().out

    def test_scorecard_exit_one_with_expired(self, tmp_path):
        register(tmp_path, "lose", instrument="parity_gate",
                 metric="parity_ok", op="==", value="true",
                 deadline="2026-01-01")
        check(tmp_path, parity_latest=parity_latest(tmp_path, False))
        assert da.main(["scorecard", "--ledger",
                        str(tmp_path / "LEDGER.jsonl")]) == 1

    def test_void_shown_with_reason(self, tmp_path, capsys):
        register(tmp_path, "dud")
        da.main(["scorecard", "--ledger", str(tmp_path / "LEDGER.jsonl")])
        out = capsys.readouterr().out
        assert "VOID" in out and "pre-registration law" in out

    def test_empty_ledger_is_clean_exit(self, tmp_path, capsys):
        assert da.main(["scorecard", "--ledger",
                        str(tmp_path / "none.jsonl")]) == 0
        assert "NO DOCTRINE" in capsys.readouterr().out


# ------------------------------------------------------------- from-json ---

class TestFromJson:
    def test_register_from_json_document(self, tmp_path):
        doc = {
            "id": "rib-x", "kind": "rib", "source_verdict": "memory/rib/X.md",
            "claim": "route pitches must win duels",
            "deadline": "2099-01-01",
            "predicted_outcome": {
                "instrument": "duel_table", "metric": "win_rate",
                "selector": {"model": "m"}, "op": ">=", "value": 0.55},
        }
        src = tmp_path / "item.json"
        src.write_text(json.dumps(doc), encoding="utf-8")
        code = da.main(["register", "--ledger", str(tmp_path / "LEDGER.jsonl"),
                        "--from-json", str(src)])
        assert code == 0
        item = folded(tmp_path)["rib-x"]
        assert item.status == "PENDING"
        assert item.predicted_outcome["value"] == 0.55

    def test_from_json_voids_without_prediction(self, tmp_path):
        doc = {"id": "dud", "source_verdict": "s", "deadline": "2099-01-01"}
        src = tmp_path / "item.json"
        src.write_text(json.dumps(doc), encoding="utf-8")
        code = da.main(["register", "--ledger", str(tmp_path / "LEDGER.jsonl"),
                        "--from-json", str(src)])
        assert code == 1
        assert folded(tmp_path)["dud"].status == "VOID"


# --------------------------------------------------------------- units -----

class TestUnits:
    def test_compare_ops_and_kinds(self):
        assert da.compare(0.75, ">=", 0.6)
        assert not da.compare(0.5, ">=", 0.6)
        assert da.compare(True, "==", True)
        assert da.compare(3, "<", 4)
        assert da.compare("a", "==", "a")
        assert not da.compare("a", "<", 1)  # TypeError arm: False, not crash

    def test_parse_deadline(self):
        assert da.parse_deadline("2026-10-15") is not None
        assert da.parse_deadline("soon") is None
        assert da.parse_deadline("") is None

    def test_fold_ignores_orphan_and_rogue_rows(self):
        items = da.fold_ledger([
            {"type": "check", "id": "orphan", "verdict": "VINDICATED"},
            {"type": "registration", "id": "v", "status": "VOID",
             "void_reasons": ["pre-registration law: no predicted_outcome"]},
            {"type": "check", "id": "v", "verdict": "VINDICATED",
             "measured": 1, "satisfies": True, "ts": "t"},
            {"type": "retirement", "id": "orphan"},
        ])
        # VOID can never be check-rowed into doctrine
        assert items["v"].status == "VOID"
        assert "orphan" not in items
