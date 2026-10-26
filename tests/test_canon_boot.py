"""Crown Court tests (G1 lane i05-canon-tests, 2026-10-18).

Covers mag/canon_boot.py in six bands, following the ancestor house style of
tests/test_census_drift_patrol.py: pure cores in-process (frontmatter parser,
prose-default resolver, ADDENDUM ack matcher, claim checker), the election
rule against a synthetic tmp estate with pinned mtimes, and the E1-E4
SystemExit contracts exercised through run_check on throwaway trees ONLY.
Frozen-vector law (B2-274, carried via the gene g02/g17): every fixture
string below is pinned HERE, independent of the V_* vectors frozen inside
mag/canon_boot.py, so the two files are mutual witnesses - a grammar reword
on either side is caught by the other, and neither ever auto-syncs to the
live state/ tree. Every E-check case runs against a tmp root with its own
state/ and memory/rib/; the live tree is never read by this battery.

Exit taxonomy pinned per gene g02 section 4: E1-E4 structural SystemExit,
E5 warn-only this pour (printed, never raised), E7 a printed drift witness
that rewrites the beacon and never exits.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timedelta, timezone

import pytest

# Module import, not from-imports (ancestor discipline,
# tests/test_census_drift_patrol.py:32-36 note): call as cb.<name>.
import mag.canon_boot as cb

BASE = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)

# --- frozen vectors (owned by THIS file, never synced from the module) -------

FV_AUTHORED = (
    "canon-class: authored\n"
    "canon-writer: seat-i05\n"
    "canon-claims: hermes.tiering, soak.position\n"
    "canon-supersedes: state/NIGHT_LOOP_20261005.md\n"
    "canon-fresh-until: 2026-10-19\n"
    "\n"
    "# window page\n\nbody\n"
)
FV_MACHINERY = (
    "canon-class: machinery\n"
    "canon-writer: governor_autorun\n"
    "\n# regenerated page\n\nbody\n"
)
FV_PROSE_ONLY = "# a plain legacy doc\n\nprose body, no canon block\n"
FV_UNKNOWN_KEYS = (
    "canon-class: authored\n"
    "canon-some-future-key: whatever\n"
    "canon-writer: w\n\nbody\n"
)
FV_COMMENT = "canon-class: authored  # stamped by hand\n\nbody\n"
FV_AFTER_BLANK = "canon-class: authored\n\nsome prose\ncanon-class: machinery\n"
FV_AFTER_NONCANON = "canon-class: authored\ncanon-writer: w\nTitle line\n"
FV_ACK = (
    "canon-class: authored\n\n# crown\n\n"
    "## ADDENDUM 2026-10-17\n\n"
    "Read memory/rib/RIB_BOB_PRIMARY_20261017.md; position stands.\n"
)
FV_ACK_WRONG_RIB = (
    "canon-class: authored\n\n# crown\n\n"
    "## ADDENDUM 2026-10-17\n\n"
    "Read memory/rib/RIB_SOME_OTHER_RIB.md; position stands.\n"
)
FV_CLAIMS_CROWN = "canon-class: authored\ncanon-claims: hermes.tiering\n\nbody\n"
FV_FRESH_TIGHT = (
    "canon-class: authored\ncanon-fresh-until: 2026-10-18T13:00\n\nbody\n"
)
FV_FRESH_MALFORMED = (
    "canon-class: authored\ncanon-fresh-until: not-a-date\n\nbody\n"
)
RIB_NAME = "RIB_BOB_PRIMARY_20261017.md"


# --- helpers ------------------------------------------------------------------

def write_doc(root, name, text, mtime):
    p = root / "state" / name
    p.write_text(text, encoding="utf-8")
    os.utime(p, (mtime.timestamp(), mtime.timestamp()))
    return p


def write_rib(root, name, mtime):
    p = root / "memory" / "rib" / name
    p.write_text("# law rib\n", encoding="utf-8")
    os.utime(p, (mtime.timestamp(), mtime.timestamp()))
    return p


def write_ledger(root, rel, rows):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def expect_exit(fn, *needles):
    """SystemExit with every needle in the message; never a silent pass."""
    with pytest.raises(SystemExit) as ei:
        fn()
    msg = str(ei.value)
    for n in needles:
        assert n in msg, f"exit message missing {n!r}: {msg}"
    return msg


@pytest.fixture
def tree(tmp_path):
    """A throwaway estate: tmp root with state/ and memory/rib/ mounted."""
    (tmp_path / "state").mkdir()
    (tmp_path / "memory" / "rib").mkdir(parents=True)
    return tmp_path


def green(tree, mtime=BASE, doc_text=FV_AUTHORED, **kw):
    """A passing baseline tree: one authored crown, one older law rib."""
    write_doc(tree, "win.md", doc_text, mtime)
    write_rib(tree, "RIB_X.md", mtime - timedelta(hours=2))
    return cb.run_check(tree, writer="seat-i05", why="lane vote",
                        init=kw.pop("init", True), now=BASE, **kw)


# --- band 1: frontmatter parser (pure core) -----------------------------------

def test_authored_block_parses_all_five_keys():
    m = cb.parse_canon_frontmatter(FV_AUTHORED)
    assert m["present"] is True
    assert m["class"] == "authored"
    assert m["writer"] == "seat-i05"
    assert m["claims"] == ["hermes.tiering", "soak.position"]
    assert m["supersedes"] == ["state/NIGHT_LOOP_20261005.md"]
    assert m["fresh_until"] == "2026-10-19"


def test_machinery_block_parses():
    m = cb.parse_canon_frontmatter(FV_MACHINERY)
    assert m["present"] is True
    assert m["class"] == "machinery"
    assert m["writer"] == "governor_autorun"


def test_missing_block_prose_first_doc_reports_absent():
    m = cb.parse_canon_frontmatter(FV_PROSE_ONLY)
    assert m["present"] is False
    assert m["class"] is None


def test_empty_text_has_no_block():
    m = cb.parse_canon_frontmatter("")
    assert m["present"] is False
    assert m["class"] is None


def test_unknown_canon_keys_ignored():
    m = cb.parse_canon_frontmatter(FV_UNKNOWN_KEYS)
    assert m["present"] is True
    assert m["class"] == "authored"


def test_inline_comment_stripped_from_value():
    m = cb.parse_canon_frontmatter(FV_COMMENT)
    assert m["class"] == "authored"


def test_block_ends_at_first_blank_line():
    # a later canon-class line after the blank must NOT poison the block
    m = cb.parse_canon_frontmatter(FV_AFTER_BLANK)
    assert m["present"] is True
    assert m["class"] == "authored"


def test_block_ends_at_first_non_canon_line():
    m = cb.parse_canon_frontmatter(FV_AFTER_NONCANON)
    assert m["present"] is True
    assert m["class"] == "authored"
    assert m["writer"] == "w"


def test_defaults_for_optional_keys():
    m = cb.parse_canon_frontmatter("canon-class: authored\n\nbody\n")
    assert m["claims"] == []
    assert m["supersedes"] == []
    assert m["fresh_until"] is None
    assert m["writer"] is None


# --- band 2: prose-default resolver (row 0a fallback) --------------------------

def test_unstamped_plain_doc_defaults_authored_with_witness():
    cls, witness = cb.resolve_doc_class("SOME_WINDOW.md",
                                        cb.parse_canon_frontmatter(FV_PROSE_ONLY))
    assert cls == "authored"
    assert witness and "defaulted authored" in witness


@pytest.mark.parametrize("name", list(cb.PROSE_MACHINERY))
def test_named_machinery_pages_default_machinery(name):
    assert name in ("LIVE_REPORT.md", "REDBOARD.md", "START_BRIEF.md")
    cls, witness = cb.resolve_doc_class(name,
                                        cb.parse_canon_frontmatter(FV_PROSE_ONLY))
    assert cls == "machinery"
    assert witness and "prose rule" in witness


def test_stamped_doc_carries_no_witness():
    cls, witness = cb.resolve_doc_class("anything.md",
                                        cb.parse_canon_frontmatter(FV_AUTHORED))
    assert cls == "authored"
    assert witness is None


# --- band 3: election rule (synthetic estate, pinned mtimes) -------------------

def test_newest_authored_wins_and_machinery_never_crowns(tree):
    write_doc(tree, "a_machinery.md", FV_MACHINERY, BASE + timedelta(hours=3))
    write_doc(tree, "b_authored.md", FV_AUTHORED, BASE + timedelta(hours=1))
    write_doc(tree, "c_plain.md", FV_PROSE_ONLY, BASE)
    el = cb.elect(tree / "state")
    assert el["crown"]["path"] == "state/b_authored.md"
    assert el["authored_count"] == 2
    assert len(el["trace"]) == 3


def test_row0a_prose_machinery_newest_by_mtime_is_excluded(tree):
    # the LIVE_REPORT 2026-10-06 bug shape: the machine page is NEWEST
    write_doc(tree, "LIVE_REPORT.md", FV_PROSE_ONLY, BASE + timedelta(hours=5))
    write_doc(tree, "plain_window.md", FV_PROSE_ONLY, BASE + timedelta(hours=1))
    el = cb.elect(tree / "state")
    assert el["crown"]["path"] == "state/plain_window.md"
    by = {e["path"].rsplit("/", 1)[-1]: e for e in el["trace"]}
    assert by["LIVE_REPORT.md"]["excluded"] is True
    assert "prose rule" in by["LIVE_REPORT.md"]["excluded_by"]
    assert by["plain_window.md"]["excluded"] is False
    assert by["plain_window.md"]["witness"]


def test_stamped_machinery_excluded_by_frontmatter_in_trace(tree):
    write_doc(tree, "gen.md", FV_MACHINERY, BASE + timedelta(hours=5))
    write_doc(tree, "win.md", FV_AUTHORED, BASE)
    el = cb.elect(tree / "state")
    by = {e["path"].rsplit("/", 1)[-1]: e for e in el["trace"]}
    assert by["gen.md"]["excluded"] is True
    assert "frontmatter" in by["gen.md"]["excluded_by"]


def test_zero_authored_elects_no_crown(tree):
    write_doc(tree, "a.md", FV_MACHINERY, BASE)
    write_doc(tree, "REDBOARD.md", FV_PROSE_ONLY, BASE + timedelta(hours=1))
    el = cb.elect(tree / "state")
    assert el["crown"] is None
    assert el["authored_count"] == 0


# --- band 4: E1 / E2 / E3 guards -----------------------------------------------

def test_e1_missing_beacon_exits_on_check(tree):
    write_doc(tree, "win.md", FV_AUTHORED, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=1))
    msg = expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                           init=False, now=BASE),
                      "E1", "canon_beacon.json")
    assert "--init" in msg


def test_e1_init_mints_beacon_even_when_e4_fires(tree):
    # crown older than law: --init records the failed election, then exits loud
    write_doc(tree, "win.md", FV_AUTHORED, BASE - timedelta(hours=30))
    write_rib(tree, RIB_NAME, BASE - timedelta(hours=1))
    msg = expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                           init=True, now=BASE), "E4")
    beacon_path = tree / "state" / "canon_beacon.json"
    assert beacon_path.is_file()
    on_disk = json.loads(beacon_path.read_text(encoding="utf-8"))
    assert on_disk["law_anchor"]["crown_newer_than_law"] is False
    assert "recorded the failed election" not in msg  # that line is stdout, not exit


def test_e2_zero_authored_docs_exits(tree):
    write_doc(tree, "a.md", FV_MACHINERY, BASE)
    write_rib(tree, "RIB_X.md", BASE)
    msg = expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                           init=True, now=BASE), "E2")
    assert "zero authored" in msg


def test_e3_guard_exits_on_machinery_crown():
    bad = {"path": "state/gen.md", "doc_class": "machinery", "mtime_dt": BASE,
           "mtime_utc": BASE.isoformat()}
    msg = expect_exit(lambda: cb.guard_e3(bad), "E3")
    assert "machinery" in msg


def test_e3_guard_passes_authored_crown():
    good = {"path": "state/win.md", "doc_class": "authored", "mtime_dt": BASE,
            "mtime_utc": BASE.isoformat()}
    assert cb.guard_e3(good) is None


# --- band 5: E4 leg 1 - older crown vs newer law rib ---------------------------

def test_e4_older_crown_newer_rib_exits(tree):
    write_doc(tree, "win.md", FV_AUTHORED, BASE - timedelta(hours=30))
    write_rib(tree, RIB_NAME, BASE - timedelta(hours=1))
    msg = expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                           init=True, now=BASE),
                      "E4", "older than newest law rib", RIB_NAME)
    assert "ADDENDUM" in msg


def test_e4_addendum_ack_naming_the_rib_is_the_honest_cure(tree):
    write_doc(tree, "win.md", FV_ACK, BASE - timedelta(hours=30))
    write_rib(tree, RIB_NAME, BASE - timedelta(hours=1))
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    assert b["law_anchor"]["ack_found"] is True
    assert b["law_anchor"]["crown_newer_than_law"] is False


def test_e4_addendum_not_naming_the_rib_does_not_cure(tree):
    # the ack is content, not ritual: an ADDENDUM naming some OTHER rib fails
    write_doc(tree, "win.md", FV_ACK_WRONG_RIB, BASE - timedelta(hours=30))
    write_rib(tree, RIB_NAME, BASE - timedelta(hours=1))
    expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                     init=True, now=BASE), "E4")


def test_has_ack_after_requires_rib_name_inside_addendum_section():
    # a rib mention BEFORE the ADDENDUM heading is not an ack (section scoping)
    text = ("memory/rib/RIB_BOB_PRIMARY_20261017.md mentioned early\n\n"
            "## ADDENDUM\n\nnothing to do with that rib\n")
    assert cb.has_ack_after(text, "RIB_BOB_PRIMARY_20261017") is False
    assert cb.has_ack_after(FV_ACK, "RIB_BOB_PRIMARY_20261017") is True
    assert cb.has_ack_after(FV_AUTHORED, "RIB_BOB_PRIMARY_20261017") is False


def test_e4_crown_at_least_as_new_as_law_passes(tree):
    b = green(tree)
    assert b["law_anchor"]["crown_newer_than_law"] is True
    assert b["law_anchor"]["ack_found"] is False


def test_e4_empty_law_vault_is_cannot_verify_exit(tree):
    write_doc(tree, "win.md", FV_AUTHORED, BASE)
    expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                     init=True, now=BASE),
                "E4", "cannot verify")


# --- band 6: E4 leg 2 - registered-claim contradiction --------------------------

def test_e4_contradicted_claim_status_exits(tree):
    write_doc(tree, "win.md", FV_CLAIMS_CROWN, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    write_ledger(tree, "watch/claims.jsonl",
                 [{"id": "hermes.tiering", "status": "CONTRADICTED"}])
    expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                     init=True, now=BASE),
                "E4", "hermes.tiering", "contradicts a registered claim")


@pytest.mark.parametrize("status", ["falsified", "dead", "invalid"])
def test_e4_other_negative_statuses_also_contradict(tree, status):
    write_doc(tree, "win.md", FV_CLAIMS_CROWN, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    write_ledger(tree, "watch/claims.jsonl",
                 [{"id": "hermes.tiering", "status": status}])
    expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                     init=True, now=BASE),
                "E4", "contradicts a registered claim")


def test_e4_dangling_claim_id_exits(tree):
    write_doc(tree, "win.md", FV_CLAIMS_CROWN, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    write_ledger(tree, "watch/claims.jsonl", [{"id": "other.claim"}])
    expect_exit(lambda: cb.run_check(tree, writer="s", why="w",
                                     init=True, now=BASE),
                "E4", "dangling", "hermes.tiering")


def test_e4_absent_ledger_is_unchecked_witness_not_fake_pass(tree, capsys):
    write_doc(tree, "win.md", FV_CLAIMS_CROWN, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    out = capsys.readouterr().out
    assert "UNCHECKED" in out
    assert b["claims_checked"] == [
        {"id": "hermes.tiering", "status": "unchecked_ledger_absent",
         "ledger": None}]


def test_e4_fallback_ledger_logs_claims_row_verifies_clean(tree):
    # the dormant work_register shape: label id + nested claim.status
    write_doc(tree, "win.md", FV_CLAIMS_CROWN, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    write_ledger(tree, "logs/claims.jsonl", [
        {"ts": "2026-09-06T00:00:00Z", "kind": "panel",
         "label": "hermes.tiering",
         "claim": {"statement": "s", "status": "Unproven"}}])
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    assert b["claims_checked"][0]["status"] == "unproven"
    assert b["claims_checked"][0]["ledger"] == "logs/claims.jsonl"


def test_check_claims_no_ids_is_noop(tree):
    checked, violations, notes = cb.check_claims(tree, [])
    assert checked == [] and violations == [] and notes == []


# --- band 7: input contract ------------------------------------------------------

@pytest.mark.parametrize("writer,why", [
    (None, "w"), ("s", None), ("", "w"), ("s", ""), ("  ", "  "),
])
def test_writer_and_why_are_mandatory_free_text(tree, writer, why):
    write_doc(tree, "win.md", FV_AUTHORED, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    expect_exit(lambda: cb.run_check(tree, writer=writer, why=why,
                                     init=True, now=BASE), "INPUT")


# --- band 8: beacon schema round-trip --------------------------------------------

def test_beacon_schema_round_trips_through_disk(tree):
    p = write_doc(tree, "win.md", FV_AUTHORED, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    b = cb.run_check(tree, writer="seat-i05:lane", why="the founding vote",
                     init=True, now=BASE)
    for key in ("schema", "moment_utc", "writer", "crown", "election_trace",
                "freshness", "law_anchor", "claims_checked"):
        assert key in b, key
    assert b["schema"] == cb.SCHEMA == "canon_beacon.v1"
    c = b["crown"]
    assert c["path"] == "state/win.md"
    assert c["doc_class"] == "authored"
    assert c["why"] == "the founding vote"
    assert c["elected_by"] == ("newest-authored-after-frontmatter-"
                               "and-row0a-prose-exclusions")
    # the hash binds the crowned BYTES, not the name
    assert c["sha256"] == hashlib.sha256(p.read_bytes()).hexdigest()
    assert b["writer"] == "seat-i05:lane"
    assert b["moment_utc"] == BASE.isoformat()
    assert all(set(e) >= {"path", "mtime_utc", "doc_class", "excluded"}
               for e in b["election_trace"])
    # full round-trip: the bytes on disk read back equal to the returned vote
    on_disk = json.loads(
        (tree / "state" / "canon_beacon.json").read_text(encoding="utf-8"))
    assert on_disk == b


def test_second_check_run_passes_with_existing_beacon(tree):
    green(tree)
    # E1 satisfied now: a plain --check (init=False) must pass and rewrite
    b2 = cb.run_check(tree, writer="seat-i05", why="second vote",
                      init=False, now=BASE + timedelta(hours=1))
    assert b2["crown"]["why"] == "second vote"


# --- band 9: E7 drift witness (never an exit) ------------------------------------

def test_e7_election_move_prints_witness_and_rewrites_beacon(tree, capsys):
    green(tree)
    first = json.loads(
        (tree / "state" / "canon_beacon.json").read_text(encoding="utf-8"))
    assert first["crown"]["path"] == "state/win.md"
    # a newer authored doc lands; the election moves
    write_doc(tree, "newer_window.md", FV_AUTHORED, BASE + timedelta(hours=4))
    b2 = cb.run_check(tree, writer="seat-i05", why="re-vote after movement",
                      init=False, now=BASE + timedelta(hours=5))
    out = capsys.readouterr().out
    assert "E7-WARN" in out
    assert "state/win.md" in out and "state/newer_window.md" in out
    assert b2["crown"]["path"] == "state/newer_window.md"
    on_disk = json.loads(
        (tree / "state" / "canon_beacon.json").read_text(encoding="utf-8"))
    assert on_disk["crown"]["path"] == "state/newer_window.md"


def test_e7_no_movement_no_witness_line(tree, capsys):
    green(tree)
    cb.run_check(tree, writer="seat-i05", why="stable re-vote",
                 init=False, now=BASE + timedelta(hours=1))
    assert "E7-WARN" not in capsys.readouterr().out


# --- band 10: E5 warn-only freshness ----------------------------------------------

def test_e5_over_bound_age_warns_and_still_writes(tree, capsys):
    write_doc(tree, "win.md", FV_AUTHORED, BASE - timedelta(hours=100))
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=101))
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    out = capsys.readouterr().out
    assert "E5-WARN" in out
    assert b["freshness"]["age_hours_at_write"] > 72.0
    assert b["freshness"]["bound_hours"] == float(cb.DEFAULT_BOUND_HOURS)
    assert (tree / "state" / "canon_beacon.json").is_file()


def test_e5_doc_fresh_until_tightens_the_bound(tree, capsys):
    write_doc(tree, "win.md", FV_FRESH_TIGHT, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    assert b["freshness"]["bound_hours"] == 1.0
    assert b["freshness"]["age_hours_at_write"] == 0.0


def test_e5_tight_bound_breached_warns_only(tree, capsys):
    # mtime 10:30 with fresh-until 11:30 = a 1h doc bound, breached 0.5h
    # later (age 1.5h); WARN-only this pour
    mtime = BASE - timedelta(hours=1, minutes=30)
    write_doc(tree, "win.md", "canon-class: authored\n"
                              "canon-fresh-until: 2026-10-18T11:30\n\nbody\n",
              mtime)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=3))
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    out = capsys.readouterr().out
    assert "E5-WARN" in out
    assert b["freshness"]["bound_hours"] == 1.0
    assert (tree / "state" / "canon_beacon.json").is_file()


def test_e5_malformed_fresh_until_degrades_to_global_bound(tree, capsys):
    write_doc(tree, "win.md", FV_FRESH_MALFORMED, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    out = capsys.readouterr().out
    assert "E5-NOTE" in out
    assert b["freshness"]["bound_hours"] == float(cb.DEFAULT_BOUND_HOURS)


# --- band 11: assumption witnesses surface through run_check ----------------------

def test_unstamped_crown_prints_assumption_witness(tree, capsys):
    write_doc(tree, "win.md", FV_PROSE_ONLY, BASE)
    write_rib(tree, "RIB_X.md", BASE - timedelta(hours=2))
    b = cb.run_check(tree, writer="s", why="w", init=True, now=BASE)
    out = capsys.readouterr().out
    assert "CROWN-COURT ASSUMPTION" in out
    assert "defaulted authored" in out
    trace_row = next(e for e in b["election_trace"]
                     if e["path"] == "state/win.md")
    assert trace_row["witness"]
