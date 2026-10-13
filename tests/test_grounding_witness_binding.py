"""grounding_wave — A3 lineage-distinct corroboration (witness identity binding).

Spec: watch/inbox/hermes_burn/A3_corroboration_bootstrap.md §1 (F1 lineage) and
§4 (migration). The pre-patch CORROBORATED rule counted DISTINCT SEAT STRINGS
(`len(seats) >= 2`), and a seat is an unauthenticated free string (default
"zcode") — so the author plus any second string could mint the first
CORROBORATED row. A puppet is a renamed seat, not a second mind.

Covered here, per the descent brief:
  (a) the puppet kill — two same-lineage witnesses do NOT corroborate
      (spec §1 Pairs A/B/C NEG: same-family seat farms, the renamed self,
      two keys over one model family);
  (b) human + one distinct lineage DOES corroborate (spec §1 Pair B POS);
  (c) backward compat — every row of the LIVE ledger still admits exactly as
      before: statuses computed under the new rule are compared against an
      embedded replay of the PRE-patch rule on the same tape (falsifier 3,
      the null-change check, on a fixture copy — the live file is only read);
  (d) the gate-leak falsifier (spec §5 item 4): whenever a row reads
      CORROBORATED, no counted witness carries an unprefixed seat or the
      author's lineage; the warrant/checks gate stays in force.

Out of scope for a unit test, by the spec's own design: falsifier 1 (10
off-ledger canary packets judged by real lineage-distinct panels — needs live
dispatches), falsifier 2 (the 7-day bootstrap to `ADMISSION: 1 corroborated`),
and the D1-D5 detectors (transcript presence, vendor cross-check, timing,
unanimity, stranger audit — §3 declares them detect-at-best against a
deliberate single-owner fabricator; the lineage law prevents only honest
mistakes and casual seat renaming).

Every synthetic tape runs in a tmp dir — the live tape
(watch/GROUNDING_WAVE.jsonl) is never written.
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from mag import grounding_wave as gw  # noqa: E402

LIVE_LEDGER = REPO_ROOT / "watch" / "GROUNDING_WAVE.jsonl"


@pytest.fixture()
def wave(tmp_path, monkeypatch):
    """Redirect every module-level surface to a tmp dir (live tape untouched)."""
    led = tmp_path / "GROUNDING_WAVE.jsonl"
    monkeypatch.setattr(gw, "LEDGER", led)
    monkeypatch.setattr(gw, "LOCK", tmp_path / "GROUNDING_WAVE.lock")
    monkeypatch.setattr(gw, "VIEW_MD", tmp_path / "view.md")
    monkeypatch.setattr(gw, "VIEW_STATIC", tmp_path / "view_static.md")
    return gw


def _evidence(tmp_path: Path, name: str, body: str = "witness binding bytes") -> str:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p.as_posix()  # forward slashes: shlex/posix and Path both happy


def _rows(wave) -> list[dict]:
    return gw._rows()


def _status_of_target(wave, target_hash: str) -> str:
    """Ladder status of the claim row whose hash is target_hash."""
    rows = _rows(wave)
    adm = gw._admission(rows)
    for i, r in enumerate(rows, 1):
        if r.get("hash") == target_hash:
            return adm["statuses"].get(i, "RECORDED")
    raise AssertionError("target row not found on tape")


# ------------------------------------------------- (a) the puppet kill
class TestSameLineageIsOneWitness:
    def test_same_family_seat_farm_is_one_witness(self, wave, tmp_path):
        """Spec §1 Pair B NEG — the real seat strings from the M1 census: author
        zcode-family plus zcode-desk and zcode-wave-driver-v0 are ONE lineage,
        i.e. zero distinct witnesses."""
        ev = _evidence(tmp_path, "farm.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="zai/zcode-desk")
        wave.witness(r["hash"], seat="zai/zcode-wave-driver-v0")
        assert _status_of_target(wave, r["hash"]) == "RECORDED", \
            "three seats of one lineage are one mind, not corroboration"

    def test_renamed_string_of_author_lineage_does_not_count(self, wave, tmp_path):
        """Spec §1 Pair A NEG — the C3 hole: SELF_SIGNED compares full strings,
        so a RENAMED same-lineage seat passes the write gate; the admission rule
        must still refuse to count it."""
        ev = _evidence(tmp_path, "renamed.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="zai/mate3-review")  # same lineage, new name
        wave.witness(r["hash"], seat="zai/zcode-r2")
        assert _status_of_target(wave, r["hash"]) == "RECORDED", \
            "renaming a puppet seat is not a second mind"

    def test_two_keys_over_one_model_family_are_one_witness(self, wave, tmp_path):
        """Spec §1 Pair C NEG — keys are attribution, not lineage: grok-4.7 via
        two xAI keys, posted as xai/grok-a and xai/grok-b, counts once."""
        ev = _evidence(tmp_path, "keys.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="xai/grok-a")
        wave.witness(r["hash"], seat="xai/grok-b")
        assert _status_of_target(wave, r["hash"]) == "RECORDED"

    def test_author_lineage_plus_one_other_is_still_one_distinct(self, wave, tmp_path):
        """A witness INSIDE the author's lineage must not count even next to a
        genuinely distinct one — two distinct non-author lineages are required."""
        ev = _evidence(tmp_path, "mixed.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="zai/mate3-review")   # author lineage: not counted
        wave.witness(r["hash"], seat="human/operator")     # one distinct lineage
        assert _status_of_target(wave, r["hash"]) == "RECORDED", \
            "1 distinct lineage + 1 same-lineage echo is not corroboration"

    def test_unprefixed_seats_do_not_count(self, wave, tmp_path):
        """Spec §3: unprefixed legacy seats cannot contribute at all — the old
        rule's `operator` + any string puppet path is closed."""
        ev = _evidence(tmp_path, "unprefixed.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="operator")
        wave.witness(r["hash"], seat="grok")
        assert _status_of_target(wave, r["hash"]) == "RECORDED"

    def test_unprefixed_author_cannot_corroborate(self, wave, tmp_path):
        """Spec §3: unprefixed authors cannot reach the rung, so there is no
        unknown-lineage author for a witness to differ from by default."""
        ev = _evidence(tmp_path, "unprefixed_author.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zcode")  # legacy, unprefixed
        wave.witness(r["hash"], seat="human/operator")
        wave.witness(r["hash"], seat="xai/grok-4.7")
        assert _status_of_target(wave, r["hash"]) == "RECORDED", \
            "an author of unknown lineage can never be corroborated"

    def test_same_lineage_pair_with_failing_checks_still_not_corroborated(self, wave, tmp_path):
        """The lineage law composes with the existing gates: same-lineage pair
        AND a failing warrant stays RECORDED (belt under braces)."""
        exe = Path(sys.executable).as_posix()
        r = wave.post("claim", "UNPROVEN", "AGENTS.md", seat="zai/zcode",
                      warrant=f'"{exe}" -c "import sys; sys.exit(1)"')
        wave.witness(r["hash"], seat="zai/zcode-desk")
        wave.witness(r["hash"], seat="zai/zcode-driver")
        assert _status_of_target(wave, r["hash"]) == "RECORDED"


# ------------------------------------------- (b) the positive rung
class TestLineageDistinctCorroboration:
    def test_human_plus_one_distinct_lineage_corroborates(self, wave, tmp_path):
        """Spec §1 Pair B POS / §2 witness picks: author <L>/zcode with
        human/operator + xai/grok-4.7 (L != xai) — two distinct lineages, both
        outside the author's."""
        ev = _evidence(tmp_path, "bootstrap.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        w1 = wave.witness(r["hash"], seat="human/operator")
        w2 = wave.witness(r["hash"], seat="xai/grok-4.7")
        assert w1["checks"]["g1"] is True and w2["checks"]["g1"] is True
        assert _status_of_target(wave, r["hash"]) == "CORROBORATED"
        ok, msg = wave.verify()
        assert ok, msg
        assert "ADMISSION:" in msg and "1 corroborated" in msg

    def test_three_distinct_lineages_corroborate(self, wave, tmp_path):
        ev = _evidence(tmp_path, "three.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="human/operator")
        wave.witness(r["hash"], seat="xai/grok-4.7")
        wave.witness(r["hash"], seat="deepseek/r1")
        assert _status_of_target(wave, r["hash"]) == "CORROBORATED"

    def test_failing_warrant_still_blocks_corroboration(self, wave, tmp_path):
        """The neighbouring conditions (spec §4: 'not-author, all checks
        passing stay unchanged') keep their teeth under lineage seats."""
        exe = Path(sys.executable).as_posix()
        ev = _evidence(tmp_path, "warrant.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode",
                      warrant=f'"{exe}" -c "import sys; sys.exit(1)"')
        wave.witness(r["hash"], seat="human/operator")
        wave.witness(r["hash"], seat="xai/grok-4.7")
        assert _status_of_target(wave, r["hash"]) == "RECORDED", \
            "two distinct lineages cannot corroborate a warrant that exits 1"

    def test_human_lineage_operator_pair_collapses(self, wave, tmp_path):
        """human/operator + human/mate are ONE lineage (human) — the operator
        cannot be duplicated by another human-prefixed string."""
        ev = _evidence(tmp_path, "human_pair.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="human/operator")
        wave.witness(r["hash"], seat="human/mate2")
        assert _status_of_target(wave, r["hash"]) == "RECORDED"


# ---------------------------------- (c) legacy tape: grandfathered, null change
def _pre_patch_statuses(rows: list[dict], adm: dict) -> dict[int, str]:
    """Replay of the PRE-patch CORROBORATED rule (`len(seats) >= 2`, distinct
    seat strings) over the patched module's structural admission outputs
    (voided/contests/witnesses — none of which the §4 patch touches). This is
    the oracle for the null-change falsifier: the live tape must admit
    identically under old rule and new rule."""
    statuses: dict[int, str] = {}
    for i, r in enumerate(rows, 1):
        if r.get("kind") in gw._ACT_KINDS:
            continue
        key = r.get("hash") or f"line:{i}"
        if key in adm["voided_keys"]:
            statuses[i] = "VOID"
        elif key in adm["contests"]:
            statuses[i] = "CONTESTED"
        else:
            ws = [w for w in adm["witnesses"].get(r.get("hash"), [])
                  if w.get("seat") != r.get("seat")]
            seats = {w.get("seat") for w in ws}
            checks_ok = all(
                w.get("checks", {}).get("g1") is True
                and w.get("checks", {}).get("g2") is not False
                and w.get("checks", {}).get("g3_exit") in (None, 0)
                for w in ws)
            statuses[i] = ("CORROBORATED"
                           if r.get("hash") and len(seats) >= 2 and checks_ok
                           else "RECORDED")
    return statuses


@pytest.mark.skipif(not LIVE_LEDGER.is_file(), reason="live ledger not present")
class TestLiveTapeGrandfathered:
    @pytest.fixture()
    def fixture_tape(self, tmp_path, monkeypatch):
        """Copy the live ledger to tmp and point the module at the COPY: verify()
        runs read-only against fixture bytes; the live file is never touched."""
        before = LIVE_LEDGER.read_bytes()
        led = tmp_path / "GROUNDING_WAVE.jsonl"
        led.write_bytes(before)
        monkeypatch.setattr(gw, "LEDGER", led)
        monkeypatch.setattr(gw, "LOCK", tmp_path / "GROUNDING_WAVE.lock")
        monkeypatch.setattr(gw, "VIEW_MD", tmp_path / "view.md")
        monkeypatch.setattr(gw, "VIEW_STATIC", tmp_path / "view_static.md")
        yield led
        assert LIVE_LEDGER.read_bytes() == before, \
            "the live tape must be byte-identical after the test (read-only)"

    def test_every_existing_row_still_verifies_unchanged(self, fixture_tape):
        """Backward compat (spec §5 falsifier 3, the null change): all 137 live
        rows (at the 2026-10-01 M1 re-run: 5 witness rows, all seat=operator,
        0 corroborated, all seats unprefixed) admit IDENTICALLY under the new
        lineage rule and the pre-patch string rule — grandfathered, no
        rewrites. If this ever fails, a prefixed-seat row landed on the live
        tape and the two rules legitimately diverge: refresh this fixture."""
        rows = gw._rows()
        adm = gw._admission(rows)
        new = adm["statuses"]
        old = _pre_patch_statuses(rows, adm)
        assert new == old, (
            "null change violated — statuses differ under the lineage rule: "
            f"{ {i: (old[i], new[i]) for i in old if old.get(i) != new.get(i)} }")
        assert sum(1 for v in new.values() if v == "CORROBORATED") == 0, \
            "M1 ground truth: the live tape has 0 corroborated rows"

    def test_verify_on_fixture_copy_reports_same_admission(self, fixture_tape):
        """The brief's (c): run verify() itself on the fixture copy. The
        pre-existing EVIDENCE-MISSING failure (dead v2-era evidence, rows
        75/76/86 at the 2026-10-01 re-run) is a LIVE-tape condition older than
        this patch — what must hold is the admission segment and that nothing
        new fails."""
        rows = gw._rows()
        ok, msg = gw.verify()
        assert f"LINKAGE-PASS: {len(rows)} posts intact" in msg
        assert "ADMISSION:" in msg and "0 corroborated" in msg
        assert "row 1: MALFORMED_ROW" not in msg and "hash mismatch" not in msg, \
            "the patch must not introduce linkage failures"
        # pre-existing, unrelated to the lineage law (dead evidence files):
        if ok:
            assert "EVIDENCE-MISSING" not in msg
        else:
            assert "EVIDENCE-MISSING" in msg or "EVIDENCE-MUTATED" in msg, \
                f"a NEW verify failure appeared: {msg}"


# --------------------------------------- (d) the gate-leak falsifier (§5.4)
class TestGateLeakFalsifier:
    """Spec §5 item 4: 'Corroborated rises above 0 while any counted witness
    row carries an unprefixed seat, the author's lineage, or no D1 transcript'
    falsifies the rib. The unprefixed/author-lineage halves are machine-checkable
    here; the D1 transcript and D3/D4 heuristics stay protocol-level."""

    def _counted_lineages(self, rows, adm, target_hash, author):
        ws = [w for w in adm["witnesses"].get(target_hash, [])
              if w.get("seat") != author]
        seats = {w.get("seat") for w in ws}
        author_lineage = str(author or "").split("/", 1)[0]
        return ({str(s).split("/", 1)[0]
                 for s in seats if isinstance(s, str) and "/" in s}
                - {author_lineage}), seats

    def test_positive_rung_counts_only_distinct_prefixed_lineages(self, wave, tmp_path):
        ev = _evidence(tmp_path, "leak.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat="zai/echo")          # author lineage: must not count
        wave.witness(r["hash"], seat="human/operator")
        wave.witness(r["hash"], seat="xai/grok-4.7")
        rows = _rows(wave)
        adm = gw._admission(rows)
        assert _status_of_target(wave, r["hash"]) == "CORROBORATED"
        lineages, seats = self._counted_lineages(rows, adm, r["hash"], "zai/zcode")
        assert lineages == {"human", "xai"}, \
            "the author-lineage echo and any unprefixed seat must not be counted"
        assert "zai/echo" in seats and "human/operator" in seats

    @pytest.mark.parametrize("w1,w2", [
        ("zai/zcode-desk", "zai/zcode-wave-driver-v0"),  # Pair B NEG (M1 census seats)
        ("zai/mate3-review", "zai/mate4-review"),        # Pair A NEG (renamed echo)
        ("xai/grok-a", "xai/grok-b"),                    # Pair C NEG (keys != lineage)
        ("human/operator", "human/mate2"),               # one human, two strings
        ("operator", "grok-4.7"),                        # unprefixed legacy seats
    ])
    def test_no_puppet_pair_leaks_the_rung(self, wave, tmp_path, w1, w2):
        """The gate must read 0 corroborated for every same-lineage or
        unprefixed pair — the row-0 lock is now hard, not volunteered."""
        ev = _evidence(tmp_path, "leak.md")
        r = wave.post("claim", "UNPROVEN", ev, seat="zai/zcode")
        wave.witness(r["hash"], seat=w1)
        wave.witness(r["hash"], seat=w2)
        adm = gw._admission(_rows(wave))
        assert sum(1 for v in adm["statuses"].values()
                   if v == "CORROBORATED") == 0, \
            f"gate LEAK: {w1} + {w2} minted a CORROBORATED row"
