"""Tests for the standing thought quantizer (v0.3 two-pass classifier).

The v0.2 fossil lesson: a compile with no tests and no consumers fossilized
for 9 days unseen. These pin the two-pass law: pure telemetry refuses,
error-quoting LAWS keep, and the pack shapes stay drop-in.

v0.4 additions (ball-20260929 quantizer-hygiene): the three verified losses
get regression pins - shell-error fragments refuse unless genuinely
imperative (L1), the decay constant is defined once and imported at all
three sites (L3), and the linker law kept==packed holds (L4).

v0.5 additions (ouroboros R4-L1, 2026-10-05): the min-rows assertion pins -
an empty compile is refused before any pack file is touched, so the previous
good packs keep serving and no fresh stamp can un-hide zero law.

v0.6 additions (ouroboros R4b move 1, 2026-10-06): the two-law-stacks-merge
pins - the percolator-side tests below inject rib_rows={} so their exact
census pins stay pinned (the v0.3-v0.5 laws are unchanged), while the vault
feed gets its own pins: a mounted amendment rides band 1 into the flash
pack beside a full court of fresh imperative percolator rows, the REAL
vault's d4-era law lands in the real-sized flash band, and a law rib that
fails to mount refuses the compile instead of packing without the vault.

v0.7 additions (run ml-moonshot-20261007 lane ml7, 2026-10-07): the
propagation-bridge pins - the percolator-side tests below also inject
classical_rows={} (the live classical feed reads real run artifacts, so
uninjected compiles are no longer hermetic), while the classical feed gets
its own pins: injected classical-model rows head the flash band structurally
against a full court of fresh imperatives, absent artifacts are a census
zero (never a refuser, the artifacts are run-scoped), the law-text
composers carry artifact path + fitted weights inside the flash budget, and
the REAL ml3/ml4 artifacts pin into the real flash band.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import thought_quantizer as tq  # noqa: E402


def test_pure_telemetry_refuses():
    v, _ = tq.classify("backend not reachable at http://127.0.0.1:8080 started 3 processes")
    assert v == "refuse-telemetry", "machine facts with no instruction must refuse"


def test_error_quoting_law_keeps():
    v, shape = tq.classify("When the fold reports hash mismatch, rerun the fold and quote the bytes before declaring drift")
    assert v == "keep", "error-quoting law must KEEP (the v0.3 heal)"
    assert shape in ("imperative-lead", "imperative")


def test_fragment_refuses():
    v, _ = tq.classify("ok done now")
    assert v == "refuse-fragment"


def test_plain_imperative_keeps_with_lead_shape():
    v, shape = tq.classify("Verify with git diff before declaring done")
    assert v == "keep" and shape == "imperative-lead"


def test_recency_orders_weights():
    now = 1_800_000_000.0  # fixed epoch "now" (2027-ish)
    day = 86400.0
    from datetime import datetime, timezone
    def iso(ts):
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    fresh = tq.recency_score(iso(now - day), now)        # 1 day old
    ancient = tq.recency_score(iso(now - 40 * day), now)  # 40 days old
    assert fresh == 1.0
    assert ancient == 0.15
    assert fresh > ancient


def test_flash_and_local_shapes():
    text = ("[steer] Elevate with a deliberate ask: frozen prefix + tight ask "
            "+ output contract. Evidence links follow at length. More words.")
    f = tq.to_flash(text)
    l = tq.to_local(text)
    assert len(f) <= tq.FLASH_MAX_CHARS
    assert len(l.split()) <= tq.LOCAL_MAX_WORDS
    assert not f.startswith("["), "tier tags strip from derived tiers"


def test_compile_end_to_end(tmp_path):
    import json
    inv = {
        "invariants": {
            "aaaa111111111111": {"text": "backend not reachable at http://x.y error",
                                  "count": 50, "last_seen": "2026-09-27T00:00:00Z"},
            "bbbb222222222222": {"text": "Verify with git diff before declaring done",
                                  "count": 900, "last_seen": "2026-09-27T00:00:00Z"},
            "cccc333333333333": {"text": "Verify with git diff before declaring done",
                                  "count": 10, "last_seen": "2026-09-26T00:00:00Z"},
            "dddd444444444444": {"text": "when the gate exits 2, rerun it and name the error in the receipt",
                                  "count": 5, "last_seen": "2026-09-27T00:00:00Z"},
        }
    }
    src = tmp_path / "invariants.json"
    src.write_text(json.dumps(inv), encoding="utf-8")
    rep = tq.compile_packs(src, tmp_path / "out",
                           {"frontier": 2, "flash": 2, "local": 2},
                           rib_rows={}, classical_rows={}, now=None)
    st = rep["stats"]
    assert st["refused_telemetry"] == 1
    assert st["dedupes"] == 1
    assert st["error_quoting_laws_kept"] == 1
    rows = [json.loads(x) for x in
            (tmp_path / "out" / "instructions_flash.jsonl").read_text(
                encoding="utf-8").splitlines()]
    assert rows and rows[0]["status"] == "compiled-v0.7"
    assert all(len(r["flash"]) <= tq.FLASH_MAX_CHARS for r in rows)


# --- v0.4 L1: verbatim shell-error fragments are machine events, not laws ----

@pytest.mark.parametrize("text", [
    "[Errno 2] No such file or directory: 'Get-ChildItem'",
    "[Errno 2] No such file or directory: 'type'",
    "[Errno 2] No such file or directory: 'powershell'",
    "The term 'powershell' is not recognized as the name of a cmdlet",
    "powershell: command not found",
])
def test_shell_error_fragment_refuses(text):
    v, _ = tq.classify(text)
    assert v == "refuse-telemetry", (
        "a verbatim shell-error quote is an event, never a norm (L1)")


def test_shell_error_with_genuine_norm_keeps():
    v, shape = tq.classify(
        "when you see No such file or directory, fix the path and rerun the "
        "gate before declaring done")
    assert v == "keep", "genuinely imperative error-quoting law must keep"
    assert shape in ("imperative-lead", "imperative")


# --- v0.4 L3: one decay constant, defined once, imported at all three sites --

def test_decay_constant_defined_once_and_imported_at_three_sites():
    from mag.constants import PACK_STALE_DAYS as DEFINED
    from mag import context_pack as cp
    assert tq.PACK_STALE_DAYS is DEFINED
    assert cp.PACK_STALE_DAYS is DEFINED
    assert DEFINED == 7, "the shared bar is the estate-wide 7d decay"
    spec = importlib.util.spec_from_file_location(
        "freshness_check_l3", ROOT / "tools" / "freshness_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.STALE_DAYS is DEFINED, (
        "the boot meter must read the shared constant, not its own 7")


# --- v0.4 L4: the linker law, kept == packed ---------------------------------

def _seed(tmp_path, n: int) -> Path:
    inv = {"invariants": {
        # keys distinct within the first 12 chars: pack ids are key[:12]
        f"{i:012x}": {"text": f"Verify with git diff variant {i} before "
                              "declaring done",
                      "count": 1,
                      "last_seen": "2026-09-27T00:00:00Z"}
        for i in range(n)}}
    src = tmp_path / "invariants.json"
    src.write_text(json.dumps(inv), encoding="utf-8")
    return src


def test_linker_kept_equals_packed_with_remainder(tmp_path):
    src = _seed(tmp_path, 5)
    rep = tq.compile_packs(src, tmp_path / "out",
                           {"frontier": 2, "flash": 2, "local": 0},
                           rib_rows={}, classical_rows={}, now=None)
    assert rep["stats"]["kept"] == 5
    assert rep["stats"]["packed"] == 5, "cap <= 0 takes the remainder"
    assert rep["packs"] == {"frontier": 2, "flash": 2, "local": 1}
    # disjoint bands: no law lands in two packs
    seen: set[str] = set()
    for tier in ("frontier", "flash", "local"):
        rows = [json.loads(x) for x in
                (tmp_path / "out" / f"instructions_{tier}.jsonl")
                .read_text(encoding="utf-8").splitlines() if x.strip()]
        for r in rows:
            assert r["id"] not in seen, "tiers must be disjoint bands"
            seen.add(r["id"])
    assert len(seen) == 5


def test_linker_fails_loud_when_caps_undercover(tmp_path):
    src = _seed(tmp_path, 5)
    with pytest.raises(SystemExit, match="linker error"):
        tq.compile_packs(src, tmp_path / "out",
                         {"frontier": 1, "flash": 1, "local": 1},
                         rib_rows={}, classical_rows={}, now=None)


def test_linker_flash_takes_top_rank(tmp_path):
    """flash is the consumer seam: it must keep the top-ranked laws."""
    src = _seed(tmp_path, 4)
    tq.compile_packs(src, tmp_path / "out",
                     {"frontier": 1, "flash": 2, "local": 0},
                     rib_rows={}, classical_rows={}, now=None)
    flash_ids = [json.loads(x)["id"] for x in
                 (tmp_path / "out" / "instructions_flash.jsonl")
                 .read_text(encoding="utf-8").splitlines() if x.strip()]
    frontier_ids = [json.loads(x)["id"] for x in
                    (tmp_path / "out" / "instructions_frontier.jsonl")
                    .read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(flash_ids) == 2
    assert flash_ids[0] != frontier_ids[0], "bands are disjoint"
    assert len(flash_ids) + len(frontier_ids) + 1 == 4


# --- v0.5 min-rows assertion (R4-L1, 2026-10-05) ------------------------------
# An empty compile must never serve as law: it writes empty packs plus a
# FRESH report stamp, and the fresh stamp un-hides the consumer debt pointer
# so seats boot zero law with a green freshness face.

def test_min_rows_refuses_empty_compile(tmp_path):
    src = tmp_path / "invariants.json"
    src.write_text(json.dumps({"invariants": {
        "aaaa111111111111": {"text": "backend not reachable at http://x.y error",
                             "count": 50, "last_seen": "2026-09-27T00:00:00Z"},
    }}), encoding="utf-8")  # every row refuses: nothing kept
    with pytest.raises(SystemExit, match="never serve as law"):
        tq.compile_packs(src, tmp_path / "out",
                         {"frontier": 2, "flash": 2, "local": 0},
                         rib_rows={}, classical_rows={}, now=None)
    assert not (tmp_path / "out" / "instructions_flash.jsonl").exists(), (
        "the refusal must fire BEFORE any pack file is written")


def test_min_rows_keeps_previous_good_packs(tmp_path):
    src = _seed(tmp_path, 3)
    tq.compile_packs(src, tmp_path / "out",
                     {"frontier": 1, "flash": 1, "local": 0},
                     rib_rows={}, classical_rows={}, now=None)
    good = (tmp_path / "out" / "instructions_flash.jsonl").read_text(encoding="utf-8")
    empty = tmp_path / "invariants.json"
    empty.write_text(json.dumps({"invariants": {
        "bbbb222222222222": {"text": "traceback (most recent call last): error",
                             "count": 9, "last_seen": "2026-09-27T00:00:00Z"},
    }}), encoding="utf-8")
    with pytest.raises(SystemExit, match="never serve as law"):
        tq.compile_packs(empty, tmp_path / "out",
                         {"frontier": 1, "flash": 1, "local": 0},
                         rib_rows={}, classical_rows={}, now=None)
    assert (tmp_path / "out" / "instructions_flash.jsonl").read_text(
        encoding="utf-8") == good, (
        "a refused empty compile must not clobber the packs already serving readers")


def test_min_kept_laws_constant_is_the_honest_floor():
    assert tq.MIN_KEPT_LAWS == 1


# --- v0.6 (R4b move 1, 2026-10-06): the two law stacks merge at the compile --

def _amend_feed(marker: str = "MEASURED ON") -> dict[str, dict]:
    return {f"rib0:RIB_TEST_20261006#1": {
        "text": f"POST-DATUM AMENDMENT 2026-10-04: the d4 three-arm probe "
                f"{marker} thinking-off losing to thinking-mode on every "
                "workhorse row; route judgment asks with thinking ON",
        "count": 0, "last_seen": "2026-10-06T00:00:00Z",
        "vault_amendment": True}}


def test_rib_amendment_rides_band_one_into_flash(tmp_path):
    """A mounted amendment must reach the FLASH pack even against a full
    court of fresh imperative percolator rows at the same recency - the fold
    S1 disease was fresh-stale law under a fresh stamp, not a small pool."""
    from datetime import datetime, timezone
    now = datetime(2026, 10, 6, tzinfo=timezone.utc).timestamp()
    inv = {"invariants": {
        f"{i:012x}": {"text": f"Verify with git diff variant {i} before "
                              "declaring done",
                      "count": 3, "last_seen": "2026-10-05T00:00:00Z"}
        for i in range(20)}}
    src = tmp_path / "invariants.json"
    src.write_text(json.dumps(inv), encoding="utf-8")
    rep = tq.compile_packs(src, tmp_path / "out",
                           {"frontier": 12, "flash": 12, "local": 0},
                           rib_rows=_amend_feed(), now=now)
    flash = [json.loads(x) for x in
             (tmp_path / "out" / "instructions_flash.jsonl")
             .read_text(encoding="utf-8").splitlines() if x.strip()]
    assert rep["stats"]["rib_amendments_kept"] == 1
    rib_rows = [r for r in flash if r["id"].startswith("rib")]
    assert rib_rows, "the vault amendment must sit in the flash band"
    assert "MEASURED ON" in rib_rows[0]["frontier"]
    assert rib_rows[0]["shape"] == "vault-amendment"


def test_real_vault_law_reaches_the_real_flash_pack(tmp_path):
    """The demanded pin (SYNTHESIS row 1): compile the REAL percolator feed
    with the REAL vault mounted and at least one flash row carries a d4-era
    amendment string. Before the cure this read 0/12 rows, fold finding S1."""
    src = ROOT / "memory" / "percolator" / "invariants.json"
    if not src.is_file():
        pytest.skip("no percolator invariants on this seat")
    rep = tq.compile_packs(src, tmp_path / "out",
                           {"frontier": 24, "flash": 12, "local": 0})
    assert rep["rib_feed"]["source"] == "mag.rib_boot.mount_vault"
    assert rep["stats"]["rib_amendments_kept"] >= 1, (
        "the vault feed mounted zero amendments - law packs would compile "
        "without the vault again")
    flash = [json.loads(x) for x in
             (tmp_path / "out" / "instructions_flash.jsonl")
             .read_text(encoding="utf-8").splitlines() if x.strip()]
    markers = ("MEASURED ON", "max_concurrency")
    assert any(any(m in r["frontier"] for m in markers) for r in flash), (
        "no flash row carries a d4-era amendment string; POST-DATUM rib law "
        "is not reaching the seat band")
    assert rep["stats"]["kept"] == rep["stats"]["packed"]


def test_unmounted_law_rib_refuses_the_compile(tmp_path, monkeypatch):
    """A renamed/missing law rib must refuse the compile (loud), never pack
    quietly without the vault - mag.rib_boot's own fail-loud contract,
    inherited by the producer."""
    import mag.rib_boot as rb
    monkeypatch.setattr(rb, "mount_vault", lambda: {
        "md_count": 1, "law_ribs": [{"file": "RIB_GONE.md", "mounted": False,
                                     "note": "missing"}],
        "mounted_count": 0, "amendments_mounted": 0})
    src = _seed(tmp_path, 3)
    with pytest.raises(SystemExit, match="failed to mount"):
        tq.compile_packs(src, tmp_path / "out",
                         {"frontier": 1, "flash": 1, "local": 0})
    assert not (tmp_path / "out" / "compile_report.json").exists()


# --- v0.7 (run ml-moonshot-20261007 lane ml7): the propagation bridge --------
# Classical models are LAWS too: ml3's router + ml4's forecaster ride as pack
# rows whose law text names the artifact path + the fitted weights, pinned to
# the head of the flash band so every seat inherits the classical layer.

def _classical_feed() -> dict[str, dict]:
    return {
        "bridge_ml3_router": {
            "text": "CLASSICAL LAW ml3-gps-router: route (animal x task_shape) "
                    "by the fitted model watch/inbox/ml_moonshot_20261007/"
                    "ml3_router_model.joblib; top importances "
                    "task_shape_tavern-turn 0.5675, "
                    "animal_anthropic/claude-haiku-4.5 0.1045; GB acc 0.8722 "
                    "AUC 0.9434 on 3753 rows.",
            "count": 3753, "last_seen": "2026-10-07T00:00:00Z"},
        "bridge_ml4_forecast": {
            "text": "CLASSICAL LAW ml4-lane-forecaster: lane remaining-rows "
                    "forecast by Ridge(alpha=1.0) refit on all 1236 "
                    "checkpoints of memory/runs/mickey17_v2/runs/"
                    "ml-moonshot-20261007/lanes/ml4_checkpoints.jsonl; "
                    "standardized coefs log_rows_so_far +0.8125, frac -2.3108.",
            "count": 1236, "last_seen": "2026-10-07T00:00:00Z"},
    }


def test_classical_rows_head_the_flash_band(tmp_path):
    """The propagation-bridge pin: classical-model rows must sit at the HEAD
    of the flash band against a full court of fresh percolator imperatives -
    inheritance is structural, not rank luck."""
    from datetime import datetime, timezone
    now = datetime(2026, 10, 7, tzinfo=timezone.utc).timestamp()
    inv = {"invariants": {
        f"{i:012x}": {"text": f"Verify with git diff variant {i} before "
                              "declaring done",
                      "count": 3, "last_seen": "2026-10-06T00:00:00Z"}
        for i in range(20)}}
    src = tmp_path / "invariants.json"
    src.write_text(json.dumps(inv), encoding="utf-8")
    rep = tq.compile_packs(src, tmp_path / "out",
                           {"frontier": 12, "flash": 12, "local": 0},
                           rib_rows={}, classical_rows=_classical_feed(),
                           now=now)
    st = rep["stats"]
    assert st["classical_models_in"] == 2 and st["classical_rows_kept"] == 2
    assert st["kept"] == st["packed"], "the linker law holds under the pin"
    flash = [json.loads(x) for x in
             (tmp_path / "out" / "instructions_flash.jsonl")
             .read_text(encoding="utf-8").splitlines() if x.strip()]
    assert [r["shape"] for r in flash[:2]] == ["classical-model"] * 2, (
        "the classical layer must head the flash band structurally")
    assert all(r["shape"] != "classical-model" for r in flash[2:])
    # disjoint bands: every kept row lands in exactly one tier pack
    seen = []
    for tier in ("frontier", "flash", "local"):
        seen += [json.loads(x)["id"] for x in
                 (tmp_path / "out" / f"instructions_{tier}.jsonl")
                 .read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(seen) == len(set(seen)), "tiers must stay disjoint under the pin"
    assert rep["classical_feed"]["source"] == "caller-injected (test)"


def test_classical_feed_absent_artifacts_count_zero(tmp_path):
    """No classical artifacts -> census zero, compile still serves: the
    artifacts are run-scoped, so their absence is a counted fact, never a
    silent skip and never the vault's fail-loud refuser."""
    src = _seed(tmp_path, 3)
    rep = tq.compile_packs(src, tmp_path / "out",
                           {"frontier": 1, "flash": 1, "local": 0},
                           rib_rows={}, classical_rows={}, now=None)
    assert rep["stats"]["classical_models_in"] == 0
    assert rep["stats"]["classical_rows_kept"] == 0
    assert rep["stats"]["kept"] == rep["stats"]["packed"] == 3


def test_compose_ml4_law_carries_artifact_path_and_coefficients():
    report = {"models": {"ridge": {"spearman": 0.9742},
                         "hgb": {"spearman": 0.9804},
                         "mean": {"spearman": -0.1094}}}
    coefs = {"log_rows_so_far": 0.8125, "frac": -2.3108,
             "elapsed_sofar_min": 0.0011, "family_code": 0.1493,
             "log_run_lanes_started": -0.0151}
    text = tq.compose_ml4_law(report, coefs, 1236,
                              "memory/runs/x/ml4_checkpoints.jsonl")
    assert "ml4_checkpoints.jsonl" in text, "artifact path is the law text"
    for f in coefs:
        assert f in text, f"coefficient name {f} missing from the law text"
    assert "0.9742" in text and "0.9804" in text and "-0.1094" in text
    head = tq.to_flash(text)
    assert "ml4_checkpoints.jsonl" in head, "flash head must carry the path"
    assert len(head) <= tq.FLASH_MAX_CHARS


def test_compose_ml3_law_carries_artifact_path_and_importances():
    metrics = {"n_rows": 3753, "splits": {"time_75_25": {
        "gradient_boosting": {"accuracy": 0.8722, "roc_auc": 0.9434},
        "baseline_percolator": {"accuracy": 0.7135, "roc_auc": 0.5012}}}}
    importances = [("task_shape_tavern-turn", 0.5675),
                   ("animal_anthropic/claude-haiku-4.5", 0.1045)]
    text = tq.compose_ml3_law(
        metrics, importances,
        "watch/inbox/ml_moonshot_20261007/ml3_router_model.joblib")
    assert "ml3_router_model.joblib" in text, "artifact path is the law text"
    assert "task_shape_tavern-turn 0.5675" in text
    assert "AUC 0.9434" in text and "AUC 0.5012" in text
    assert "5+ training rows" in text, "the evidence gate is part of the law"
    head = tq.to_flash(text)
    assert "ml3_router_model.joblib" in head, "flash head must carry the path"
    assert len(head) <= tq.FLASH_MAX_CHARS


def test_real_classical_layer_reaches_the_real_flash_pack(tmp_path):
    """The demanded proof (run ml-moonshot-20261007): compile with the real
    artifacts and the flash band's head rows carry the model artifact paths."""
    if not (tq.ML3_METRICS.is_file() and tq.ML4_CHECKPOINTS.is_file()):
        pytest.skip("ml-moonshot classical artifacts absent on this seat")
    src = ROOT / "memory" / "percolator" / "invariants.json"
    if not src.is_file():
        pytest.skip("no percolator invariants on this seat")
    rep = tq.compile_packs(src, tmp_path / "out",
                           {"frontier": 24, "flash": 12, "local": 0})
    assert rep["stats"]["classical_rows_kept"] == 2, (
        "the live classical feed mounted zero rows - the bridge is dark")
    flash = [json.loads(x) for x in
             (tmp_path / "out" / "instructions_flash.jsonl")
             .read_text(encoding="utf-8").splitlines() if x.strip()]
    assert [r["shape"] for r in flash[:2]] == ["classical-model"] * 2
    assert "ml3_router_model.joblib" in flash[0]["frontier"]
    assert "ml4_checkpoints.jsonl" in flash[1]["frontier"]
    assert rep["stats"]["kept"] == rep["stats"]["packed"]
