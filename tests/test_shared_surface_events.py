"""tests for the events-log hygiene gate in mag/shared_surface.py (B2-42, 2026-09-26).

Spec under test (module docstring, "Events-log hygiene"):
  - malformed line = non-blank line (trailing CRLF stripped) failing strict
    json.loads with NaN/Infinity rejected, mirroring JSON.parse in the fold;
  - lines whose content sha256 is registered in
    configs/events_malformed_baseline.json are grandfathered debt (no-erase
    law: the log is append-only, the lines stay);
  - a NEW (unregistered) malformed line is an ERROR, so `validate` exits 1;
  - a missing baseline is an ERROR; a missing events log is a WARNING;
  - a registered line that no longer exists in the log is a WARNING so debt
    can be reclaimed from the registry.

All tests run against a throwaway inbox; the durable watch/inbox is never
touched. The real baseline file is read only by test_missing_real_baseline,
which asserts the registry that ships with the repo parses and carries the
three 2026-09-01 legacy lines.
"""
import hashlib
import json
from pathlib import Path

import pytest

import mag.shared_surface as ss

VALID = json.dumps({"seq": 1, "ts": "2026-09-26T00:00:00Z", "op": "note", "writer": "t", "nonce": 1})


def _line_sha(content: bytes) -> str:
    return hashlib.sha256(content.rstrip(b"\r\n")).hexdigest()


@pytest.fixture
def surface(tmp_path, monkeypatch):
    """Point every module constant at a throwaway surface."""
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    configs = tmp_path / "configs"
    configs.mkdir()
    monkeypatch.setattr(ss, "ROOT", tmp_path)
    monkeypatch.setattr(ss, "WATCH", tmp_path / "watch")
    monkeypatch.setattr(ss, "INBOX", inbox)
    monkeypatch.setattr(ss, "INDEX", inbox / "INDEX.json")
    monkeypatch.setattr(ss, "CONTRACT", inbox / "SHARED_SURFACE_CONTRACT.json")
    monkeypatch.setattr(ss, "WARM_PACK", tmp_path / "watch" / "WARM_PACK.json")
    monkeypatch.setattr(ss, "EVENTS_LOG", inbox / "index_events.jsonl")
    monkeypatch.setattr(ss, "MALFORMED_BASELINE", configs / "events_malformed_baseline.json")
    monkeypatch.setattr(ss, "LINKS_LEDGER", inbox / "LINKS.jsonl")
    monkeypatch.setattr(ss, "LINKS_KIND_BASELINE", configs / "links_kind_baseline.json")
    return {"inbox": inbox, "configs": configs, "log": inbox / "index_events.jsonl",
            "baseline": configs / "events_malformed_baseline.json"}


def _write_baseline(path, entries):
    path.write_text(json.dumps({"schema": "events_malformed_baseline.v1",
                                "grandfathered": entries}), encoding="utf-8")


def _malformed_errors(result):
    # prefix match: tmp_path fixture names contain the word "malformed", so a
    # bare substring filter would catch unrelated "missing index" errors
    return [e for e in result["errors"] if e.startswith("NEW malformed line")]


def test_new_malformed_line_is_an_error(surface):
    surface["log"].write_text(VALID + "\n" + "{'seq':NEXT,'op':'register'}\n", encoding="utf-8")
    _write_baseline(surface["baseline"], [])
    result = ss.inspect_surface()
    bad = _malformed_errors(result)
    assert len(bad) == 1 and "NEW malformed line" in bad[0]
    assert result["events_log_malformed"] == {"total": 1, "grandfathered": 0, "new": 1}
    assert result["ok"] is False


def test_grandfathered_line_is_not_an_error(surface):
    bad = "{'seq':NEXT,'op':'register'}"
    surface["log"].write_text(VALID + "\n" + bad + "\n", encoding="utf-8")
    _write_baseline(surface["baseline"],
                    [{"line": 2, "sha256": _line_sha(bad.encode()), "why": "test debt"}])
    result = ss.inspect_surface()
    assert _malformed_errors(result) == []
    assert result["events_log_malformed"]["grandfathered"] == 1
    assert result["events_log_malformed"]["new"] == 0


def test_crlf_and_blank_lines_are_not_malformed(surface):
    surface["log"].write_bytes((VALID + "\r\n" + "\n" + VALID + "\r\n").encode())
    _write_baseline(surface["baseline"], [])
    result = ss.inspect_surface()
    assert _malformed_errors(result) == []
    assert result["events_log_malformed"]["total"] == 0


def test_nan_and_infinity_rejected_like_json_parse(surface):
    surface["log"].write_text('{"seq":NaN,"op":"amend"}\n', encoding="utf-8")
    _write_baseline(surface["baseline"], [])
    result = ss.inspect_surface()
    assert len(_malformed_errors(result)) == 1


def test_missing_baseline_is_an_error_and_stale_entry_warns(surface):
    bad = "{'seq':NEXT,'op':'register'}"
    surface["log"].write_text(bad + "\n", encoding="utf-8")
    result = ss.inspect_surface()  # no baseline file written
    assert any("missing malformed-line baseline" in e for e in result["errors"])
    # now register debt for a line that is not in the log: stale warning
    _write_baseline(surface["baseline"],
                    [{"line": 94, "sha256": "f" * 64, "why": "already fixed"}])
    result = ss.inspect_surface()
    assert any("no longer in the log" in w for w in result["warnings"])


def test_missing_events_log_is_a_warning(surface):
    _write_baseline(surface["baseline"], [])
    result = ss.inspect_surface()
    assert any("events log not found" in w for w in result["warnings"])
    assert _malformed_errors(result) == []


def test_real_baseline_carries_the_three_legacy_lines():
    baseline = Path(ss.__file__).resolve().parents[1] / "configs" / "events_malformed_baseline.json"
    data = json.loads(baseline.read_text(encoding="utf-8"))
    shas = {e["sha256"] for e in data["grandfathered"]}
    assert shas == {
        "325c9ea76971007fe89a5a4ce508096c7e44ed22084b6c6bc47a7ed9fe341c18",  # line 94
        "db87cd15ad3378a8c677f43c9024b8d48d67abd7fc53c4e14b6c11a347dbafdc",  # line 95
        "bfa769b3b7fd35675aab204edcb3cf4ba1c483f932348de356fe5a8d304072e8",  # line 96
    }


def test_real_log_has_only_the_three_grandfathered_lines():
    log = Path(ss.__file__).resolve().parents[1] / "watch" / "inbox" / "index_events.jsonl"
    found = ss.scan_events_log(log)
    assert {r["sha256"] for r in found} == {
        "325c9ea76971007fe89a5a4ce508096c7e44ed22084b6c6bc47a7ed9fe341c18",
        "db87cd15ad3378a8c677f43c9024b8d48d67abd7fc53c4e14b6c11a347dbafdc",
        "bfa769b3b7fd35675aab204edcb3cf4ba1c483f932348de356fe5a8d304072e8",
    }
    assert [r["line"] for r in found] == [94, 95, 96]


# ---------------------------------------------------------------------------
# B2-156 living-file law (spec: watch/inbox/LIVING_HASH_LAW_20260926.md):
# an item registered living:true + size:N seals only its first N bytes.
# ---------------------------------------------------------------------------

def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest().upper()


def _mk_surface(surface, items):
    """Minimal valid INDEX + CONTRACT so item-level checks are the only signals."""
    (surface["inbox"] / "SHARED_SURFACE_CONTRACT.json").write_text(
        json.dumps({"canonical": {"container": "/board/inbox"}}), encoding="utf-8")
    (surface["inbox"] / "INDEX.json").write_text(
        json.dumps({"root": "/board/inbox", "items": items}), encoding="utf-8")


def test_living_item_growth_is_not_an_error(surface):
    sealed = b"row one\nrow two\n"
    f = surface["inbox"] / "QUEUE.md"
    f.write_bytes(sealed + b"row three appended later\n")
    _mk_surface(surface, [{"path": "QUEUE.md", "sha256": _sha(sealed),
                           "living": True, "size": len(sealed)}])
    result = ss.inspect_surface()
    assert not any("mismatch" in e for e in result["errors"]), result["errors"]
    assert result["living_files"]["ok"] == 1
    rec = next(r for r in result["indexed_items"] if r["path"] == "QUEUE.md")
    assert rec["living_prefix_match"] is True


def test_living_item_prefix_mutation_is_an_error(surface):
    sealed = b"sealed history\n"
    f = surface["inbox"] / "LEDGER.jsonl"
    f.write_bytes(b"TAMPERED history\nappended\n")
    _mk_surface(surface, [{"path": "LEDGER.jsonl", "sha256": _sha(sealed),
                           "living": True, "size": len(sealed)}])
    result = ss.inspect_surface()
    assert any(e.startswith("living prefix mismatch: LEDGER.jsonl") for e in result["errors"])
    assert result["ok"] is False


def test_living_item_truncation_is_an_error(surface):
    sealed = b"0123456789\n"
    (surface["inbox"] / "BOARD.md").write_bytes(b"01234")
    _mk_surface(surface, [{"path": "BOARD.md", "sha256": _sha(sealed),
                           "living": True, "size": len(sealed)}])
    result = ss.inspect_surface()
    assert any(e.startswith("living prefix mismatch: BOARD.md") for e in result["errors"])


def test_living_item_without_size_warns_but_does_not_fail(surface):
    (surface["inbox"] / "LEGACY.md").write_bytes(b"bytes\n")
    _mk_surface(surface, [{"path": "LEGACY.md", "sha256": "DEADBEEF", "living": True}])
    result = ss.inspect_surface()
    assert not any("mismatch" in e for e in result["errors"]), result["errors"]
    assert result["living_files"]["unverified"] == 1
    assert any("living item without size seal" in w for w in result["warnings"])


def test_open_living_item_inserts_are_never_an_error(surface):
    # edit-shaped board: bytes change anywhere by design (QUEUE.md inserts under
    # ## Open), so there is no byte seal to break; integrity is the log's job.
    (surface["inbox"] / "QUEUE.md").write_bytes(b"rewritten in place, mid-file insert and all\n")
    _mk_surface(surface, [{"path": "QUEUE.md", "sha256": "DEADBEEF",
                           "living": True, "seal": "open"}])
    result = ss.inspect_surface()
    assert not any("mismatch" in e for e in result["errors"]), result["errors"]
    assert result["living_files"]["open"] == 1
    assert result["living_files"]["unverified"] == 0


def test_static_item_mismatch_still_errors(surface):
    (surface["inbox"] / "DOC.md").write_bytes(b"changed bytes\n")
    _mk_surface(surface, [{"path": "DOC.md", "sha256": _sha(b"original\n")}])
    result = ss.inspect_surface()
    assert any(e.startswith("hash mismatch: DOC.md") for e in result["errors"])
    # rebased (B2-297): the living_files summary gained the downgraded counter
    assert result["living_files"] == {"ok": 0, "open": 0, "unverified": 0,
                                      "downgraded": 0}


# --- B2-168 (2026-09-26): LINKS.jsonl event-split gate -------------------
# Spec (mag/shared_surface.py docstring, "LINKS event split"): LINKS.jsonl
# holds link rows only past the B2-28 migration marker (schema
# "migration-marker.v1", writer "b2-28-schema-split"). Any row AFTER the
# marker carrying a "kind" field is judged against
# configs/links_kind_baseline.json (content-sha keyed, B2-42 pattern); an
# unregistered one is an ERROR pointing at EVENTS.jsonl. Rows before the
# marker are grandfathered (the 51 legacy event rows, append-only law).
# A missing marker is a WARNING (the split cannot be enforced without its
# anchor); a missing LINKS.jsonl is a WARNING; a missing baseline registry
# is an ERROR.

LINK_MARKER = json.dumps({"seq": 7, "ts": "2026-09-26T12:31:49Z",
                          "schema": "migration-marker.v1",
                          "writer": "b2-28-schema-split",
                          "note": "split marker"})
LINK_ROW = json.dumps({"seq": 8, "ts": "2026-09-26T13:00:00Z",
                       "op": "register", "canonical": "https://x.com/a",
                       "url": "https://x.com/a", "writer": "t"})
LEGACY_EVENT = json.dumps({"ts": "2026-09-20T13:10:00Z", "writer": "scout",
                           "id": "ALERT-X", "kind": "ALERT", "title": "t"})
NEW_EVENT = json.dumps({"ts": "2026-09-26T20:00:00Z", "writer": "scout",
                        "id": "ALERT-Y", "kind": "finding", "title": "t"})


def _links_errors(result):
    return [e for e in result["errors"] if e.startswith("NEW event-kind row in LINKS.jsonl")]


def test_links_new_kind_row_after_marker_is_an_error(surface):
    surface["inbox"].joinpath("LINKS.jsonl").write_text(
        LEGACY_EVENT + "\n" + LINK_MARKER + "\n" + LINK_ROW + "\n" + NEW_EVENT + "\n",
        encoding="utf-8")
    result = ss.inspect_surface()
    bad = _links_errors(result)
    assert len(bad) == 1 and "line 4" in bad[0]
    assert "EVENTS.jsonl" in bad[0] and "event.v1" in bad[0]
    assert result["ok"] is False


def test_links_legacy_kind_rows_before_marker_pass(surface):
    surface["inbox"].joinpath("LINKS.jsonl").write_text(
        LEGACY_EVENT + "\n" + LEGACY_EVENT.replace("ALERT-X", "ALERT-X2") + "\n"
        + LINK_MARKER + "\n" + LINK_ROW + "\n", encoding="utf-8")
    result = ss.inspect_surface()
    assert _links_errors(result) == []


def test_links_register_rows_after_marker_pass(surface):
    surface["inbox"].joinpath("LINKS.jsonl").write_text(
        LINK_MARKER + "\n" + LINK_ROW + "\n" + LINK_ROW.replace('"seq": 8', '"seq": 9')
        + "\n", encoding="utf-8")
    result = ss.inspect_surface()
    assert _links_errors(result) == []


def test_links_missing_marker_warns_not_errors(surface):
    surface["inbox"].joinpath("LINKS.jsonl").write_text(NEW_EVENT + "\n", encoding="utf-8")
    result = ss.inspect_surface()
    assert _links_errors(result) == []
    assert any("links schema-split marker missing" in w for w in result["warnings"])


def test_links_missing_file_warns(surface):
    result = ss.inspect_surface()  # no LINKS.jsonl written
    assert _links_errors(result) == []
    assert any("links ledger not found" in w for w in result["warnings"])


def test_links_grandfathered_post_marker_row_passes(surface):
    surface["inbox"].joinpath("LINKS.jsonl").write_text(
        LINK_MARKER + "\n" + NEW_EVENT + "\n", encoding="utf-8")
    surface["configs"].joinpath("links_kind_baseline.json").write_text(
        json.dumps({"schema": "links_kind_baseline.v1",
                    "grandfathered": [{"line": 2, "sha256": _line_sha(NEW_EVENT.encode()),
                                       "id": "ALERT-Y", "why": "registered debt"}]}),
        encoding="utf-8")
    result = ss.inspect_surface()
    assert _links_errors(result) == []


def test_real_links_jsonl_matches_the_registered_baseline():
    root = Path(ss.__file__).resolve().parents[1]
    links = root / "watch" / "inbox" / "LINKS.jsonl"
    baseline = json.loads(
        (root / "configs" / "links_kind_baseline.json").read_text(encoding="utf-8"))
    registered = {e["sha256"] for e in baseline["grandfathered"]}
    found = ss.scan_links_kind_rows(links)
    assert {r["sha256"] for r in found} == registered, (
        "NEW unregistered kind rows past the B2-28 marker: "
        + repr([r for r in found if r["sha256"] not in registered]))
    assert len(found) == len(registered)  # every registered row still present


# ---------------------------------------------------------------------------
# B2-297 living-downgrade detector: a known living path whose INDEX item
# carries no living flag (a plain re-register dropped it, law section 5
# last-register-wins) is named by a WARNING and the downgraded counter.
# ---------------------------------------------------------------------------

def test_known_living_path_without_living_flag_warns_downgrade(surface):
    # the real path lives under burn_wave_20260926/, the shape the watchlist
    # keys on (a flat QUEUE.md registration is not the production shape)
    sub = surface["inbox"] / "burn_wave_20260926"
    sub.mkdir()
    row = b"# board\n- row\n"
    (sub / "QUEUE.md").write_bytes(row)
    _mk_surface(surface, [{"path": "burn_wave_20260926/QUEUE.md",
                           "sha256": _sha(row)}])
    result = ss.inspect_surface()
    assert any(w.startswith("living downgrade: burn_wave_20260926/QUEUE.md")
               for w in result["warnings"])
    assert result["living_files"]["downgraded"] == 1


def test_known_living_path_still_living_does_not_warn(surface):
    sub = surface["inbox"] / "burn_wave_20260926"
    sub.mkdir()
    sealed = b"# board\n"
    (sub / "QUEUE.md").write_bytes(sealed + b"- appended\n")
    _mk_surface(surface, [{"path": "burn_wave_20260926/QUEUE.md",
                           "sha256": _sha(sealed),
                           "living": True, "size": len(sealed)}])
    result = ss.inspect_surface()
    assert not any(w.startswith("living downgrade:") for w in result["warnings"])
    assert result["living_files"]["downgraded"] == 0
