"""grounding_wave v4 — the evidence-ADMISSION boundary (stone 1, A2 design).

Covers, per the wave_20260916 mission:
  1. the row-122 shape (hashless fragment, prev != tip) is REFUSED AT WRITE;
  2. void requires a cross-signature (named second seat + its witness row
     in the chain before the void COUNTS);
  3. tampered rows are detected (hash mismatch FAILs verify);
  4. view shows the status ladder RECORDED/CORROBORATED/CONTESTED/VOID;
  5. planted-failure propagation: a false premise descendant, once the premise
     is voided, is chain-visible (child-of-void / witness-of-void flags);
  plus: G2 source binding (identity, not existence), G3 warrant exit codes,
  contest, void-of-void reversal, re-anchor past a voided stretch, and NO
  auto-migration (v1-v3 rows keep their verdicts; old tapes still FAIL).

Every test runs against a synthetic ledger in a tmp dir — the live tape
(watch/GROUNDING_WAVE.jsonl, incl. row 122) is never touched.
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from mag import grounding_wave as gw  # noqa: E402


@pytest.fixture()
def wave(tmp_path, monkeypatch):
    """Redirect every module-level surface to a tmp dir (live tape untouched)."""
    led = tmp_path / "GROUNDING_WAVE.jsonl"
    monkeypatch.setattr(gw, "LEDGER", led)
    monkeypatch.setattr(gw, "LOCK", tmp_path / "GROUNDING_WAVE.lock")
    monkeypatch.setattr(gw, "VIEW_MD", tmp_path / "view.md")
    monkeypatch.setattr(gw, "VIEW_STATIC", tmp_path / "view_static.md")
    return gw


def _evidence(tmp_path: Path, name: str = "evidence.md", body: str = "premise bytes") -> str:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p.as_posix()  # forward slashes: shlex/posix and Path both happy


def _rows(wave) -> list[dict]:
    return gw._rows()


# ---------------------------------------------------------------- 1. row-122
class TestG1WriteGate:
    def test_row122_shape_refused_if_reposted(self, wave):
        """The exact defect class of live row 122 — {prev, ts, claim}, no hash,
        prev != tip — must be refused at WRITE time by the admission gate."""
        wave.post("first claim", "UNPROVEN", "AGENTS.md", seat="a")
        rows = _rows(wave)
        forged = {"prev": "8ccd3924b908e8ca2f8c57d0deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
                  "ts": "2026-09-16T04:17:37Z", "claim": "bypass attempt"}
        with pytest.raises(gw.GateRefusal) as ei:
            gw._admit(forged, rows, gw._admission(rows))
        assert ei.value.code == "MALFORMED_ROW"
        # and it never reached the tape
        assert len(_rows(wave)) == 1

    def test_missing_prev_refused(self, wave):
        wave.post("first claim", "UNPROVEN", "AGENTS.md", seat="a")
        rows = _rows(wave)
        no_prev = {"prev": "", "ts": "t", "kind": "claim", "claim": "c",
                   "verdict": "UNPROVEN", "evidence": "", "note": "",
                   "seat": "a", "witness": "", "src_sha256_12": {}, "warrant": ""}
        no_prev["hash"] = gw._row_hash(no_prev)
        with pytest.raises(gw.GateRefusal) as ei:
            gw._admit(no_prev, rows, gw._admission(rows))
        assert ei.value.code == "MALFORMED_ROW"

    def test_prev_not_tip_refused(self, wave):
        wave.post("first claim", "UNPROVEN", "AGENTS.md", seat="a")
        rows = _rows(wave)
        bad_chain = {"prev": "b" * 64, "ts": "t", "kind": "claim", "claim": "c",
                     "verdict": "UNPROVEN", "evidence": "", "note": "",
                     "seat": "a", "witness": "", "src_sha256_12": {}, "warrant": ""}
        bad_chain["hash"] = gw._row_hash(bad_chain)
        with pytest.raises(gw.GateRefusal) as ei:
            gw._admit(bad_chain, rows, gw._admission(rows))
        assert ei.value.code == "PREV_MISMATCH"

    def test_post_roundtrip_always_admissible(self, wave):
        """Anything the write path emits must pass its own gate (the physical
        impossibility, proven in the happy direction)."""
        for n in range(3):
            wave.post(f"claim {n}", "UNPROVEN", "AGENTS.md", seat="a")
        rows = _rows(wave)
        assert len(rows) == 3
        for i, r in enumerate(rows, 1):
            assert gw._row_hash(r) == r["hash"]
            assert r["prev"] == (rows[i - 2]["hash"] if i > 1 else gw.GENESIS)
        ok, msg = wave.verify()
        assert ok, msg

    def test_supported_without_seat_refused(self, wave):
        with pytest.raises(gw.GateRefusal) as ei:
            wave.post("claim", "SUPPORTED", "AGENTS.md", seat="  ")
        assert ei.value.code == "UNSUPPORTED_UNSEEDED"

    def test_supported_latest_evidence_refused(self, wave, tmp_path):
        ev = tmp_path / "x_latest.md"
        ev.write_text("mutable", encoding="utf-8")
        with pytest.raises(gw.GateRefusal) as ei:
            wave.post("claim", "SUPPORTED", ev.as_posix(), seat="a", witness="b")
        assert ei.value.code == "EVIDENCE_MUTABLE"

    def test_dead_path_evidence_refused_at_post(self, wave):
        with pytest.raises(gw.GateRefusal) as ei:
            wave.post("claim", "UNPROVEN", "watch/inbox/_no_such_file_v4_probe.md")
        assert ei.value.code == "EVIDENCE_DEAD"


# ------------------------------------------------------- 2. cross-signature
class TestVoidCrossSignature:
    def test_void_requires_second_seat(self, wave, tmp_path):
        wave.post("claim", "UNPROVEN", "AGENTS.md", seat="a")
        n0 = len(_rows(wave))
        with pytest.raises(gw.GateRefusal) as ei:
            wave.void("#1", "MALFORMED", "no second seat", seat="a")
        assert ei.value.code == "VOID_UNSIGNED"
        assert len(_rows(wave)) == n0, "refused void must not land"

    def test_void_second_seat_must_differ(self, wave):
        wave.post("claim", "UNPROVEN", "AGENTS.md", seat="a")
        with pytest.raises(gw.GateRefusal) as ei:
            wave.void("#1", "MALFORMED", "self-signature", seat="a", witness="a")
        assert ei.value.code == "VOID_UNSIGNED"

    def test_void_counts_only_once_cross_signed_in_chain(self, wave, tmp_path):
        ev = _evidence(tmp_path)
        wave.post("claim", "UNPROVEN", ev, seat="a")
        v = wave.void("#1", "MALFORMED", "staged", seat="z", witness="b")
        adm = gw._admission(_rows(wave))
        assert v["hash"] in adm["pending_voids"], "unsigned void lands PENDING"
        assert adm["statuses"][1] == "RECORDED", "target not VOID until signed"
        # the named second hand executes: their witness row enters the chain
        wave.witness(v["hash"], seat="b")
        adm = gw._admission(_rows(wave))
        assert adm["statuses"][1] == "VOID"
        assert _rows(wave)[0]["hash"] in adm["voided_keys"]

    def test_void_reason_code_enum(self, wave):
        wave.post("claim", "UNPROVEN", "AGENTS.md", seat="a")
        with pytest.raises(gw.GateRefusal) as ei:
            wave.void("#1", "BECAUSE_I_SAID_SO", "not in the enum", seat="z", witness="b")
        assert ei.value.code == "BAD_REASON_CODE"

    def test_void_of_void_reversal(self, wave, tmp_path):
        ev = _evidence(tmp_path)
        wave.post("claim", "UNPROVEN", ev, seat="a")
        v1 = wave.void("#1", "MALFORMED", "staged", seat="z", witness="b")
        wave.witness(v1["hash"], seat="b")
        assert gw._admission(_rows(wave))["statuses"][1] == "VOID"
        # reversal: same verb, targets the void itself, own cross-signature
        v2 = wave.void(v1["hash"], "CONTEST_SUSTAINED", "contest sustained",
                       seat="y", witness="c")
        wave.witness(v2["hash"], seat="c")
        assert gw._admission(_rows(wave))["statuses"][1] == "RECORDED", \
            "a voided void un-voids its target"
        ok, msg = wave.verify()
        assert ok, msg

    def test_already_voided_refused(self, wave, tmp_path):
        wave.post("claim", "UNPROVEN", "AGENTS.md", seat="a")
        v = wave.void("#1", "MALFORMED", "once", seat="z", witness="b")
        wave.witness(v["hash"], seat="b")
        with pytest.raises(gw.GateRefusal) as ei:
            wave.void("#1", "DUPLICATE", "twice", seat="z", witness="b")
        assert ei.value.code == "ALREADY_VOIDED"


# ------------------------------------------------------------- 3. tampering
class TestTamperDetection:
    def test_tampered_hash_detected(self, wave, tmp_path):
        ev = _evidence(tmp_path)
        wave.post("claim one", "UNPROVEN", ev, seat="a")
        wave.post("claim two", "UNPROVEN", "AGENTS.md", seat="a")
        led = gw.LEDGER
        lines = led.read_text(encoding="utf-8").splitlines()
        row = json.loads(lines[0])
        row["claim"] = row["claim"] + " TAMPERED"  # edit in place
        lines[0] = json.dumps(row, ensure_ascii=False)
        led.write_text("\n".join(lines) + "\n", encoding="utf-8")
        ok, msg = wave.verify()
        assert not ok
        assert "row 1: hash mismatch" in msg

    def test_evidence_mutation_detected_identity_not_existence(self, wave, tmp_path):
        ev = _evidence(tmp_path, name="binding.md", body="original bytes")
        wave.post("bound claim", "UNPROVEN", ev, seat="a")
        ok, msg = wave.verify()
        assert ok, msg
        row = _rows(wave)[0]
        # T1W1 ticket 11 (2026-10-01): new bindings carry the FULL sha256
        # (was the 48-bit [:12] cut); read sides accept both widths.
        assert list(row["src_sha256_12"].values()) == [
            __import__("hashlib").sha256(b"original bytes").hexdigest()]
        # mutate the evidence bytes AFTER the post: existence holds, identity breaks
        Path(ev).write_text("mutated bytes", encoding="utf-8")
        ok, msg = wave.verify()
        assert not ok
        assert "EVIDENCE-MUTATED" in msg

    def test_g3_warrant_recorded_and_run_by_witness(self, wave, tmp_path):
        exe = Path(sys.executable).as_posix()
        good = wave.post("warranted claim", "UNPROVEN", "AGENTS.md", seat="a",
                         warrant=f'"{exe}" -c "import sys; sys.exit(0)"')
        w = wave.witness(good["hash"], seat="b")
        assert w["checks"]["g1"] is True
        assert w["checks"]["g3_exit"] == 0
        bad = wave.post("failing warrant", "UNPROVEN", "AGENTS.md", seat="a",
                        warrant=f'"{exe}" -c "import sys; sys.exit(1)"')
        w2 = wave.witness(bad["hash"], seat="b")
        assert w2["checks"]["g3_exit"] == 1

    def test_corroboration_blocked_by_failing_warrant(self, wave):
        # Lineage-prefixed seats (A3 law) so this test exercises the WARRANT
        # gate, not the seat gate: without prefixes it passed vacuously
        # because unprefixed witnesses can never corroborate (2026-10-01).
        exe = Path(sys.executable).as_posix()
        bad = wave.post("failing warrant", "UNPROVEN", "AGENTS.md", seat="alpha/a",
                        warrant=f'"{exe}" -c "import sys; sys.exit(1)"')
        wave.witness(bad["hash"], seat="beta/b")
        wave.witness(bad["hash"], seat="gamma/c")
        assert gw._admission(_rows(wave))["statuses"][1] == "RECORDED", \
            "two distinct lineages cannot corroborate a claim whose warrant exits 1"

    def test_witness_cannot_self_sign(self, wave):
        r = wave.post("claim", "UNPROVEN", "AGENTS.md", seat="a")
        with pytest.raises(gw.GateRefusal) as ei:
            wave.witness(r["hash"], seat="a")
        assert ei.value.code == "SELF_SIGNED"


# ------------------------------------------------------------ 4. the ladder
class TestLadderAndView:
    def _corroborated_row(self, wave, tmp_path, claim="the finding"):
        ev = _evidence(tmp_path, name=f"{claim[:8].replace(' ', '_')}.md")
        # A3 lineage-law fixtures (2026-10-01 owed): CORROBORATED counts
        # distinct LINEAGES (seat = <lineage>/<instance>), so the author
        # rides one lineage and the two hands ride two OTHER lineages.
        r = wave.post(claim, "UNPROVEN", ev, seat="alpha/a")
        wave.witness(r["hash"], seat="beta/b")
        wave.witness(r["hash"], seat="gamma/c")
        return r

    def test_full_ladder_in_view(self, wave, tmp_path):
        rec = wave.post("just recorded", "UNPROVEN", "AGENTS.md", seat="alpha/a")
        cor = self._corroborated_row(wave, tmp_path, "corroborated finding")
        con = self._corroborated_row(wave, tmp_path, "contested finding")
        wave.contest(con["hash"], "i dispute the binding", seat="delta/d")
        voy = self._corroborated_row(wave, tmp_path, "voided finding")
        v = wave.void(voy["hash"], "FORGED", "the evidence was staged",
                      seat="zeta/z", witness="beta/b")
        wave.witness(v["hash"], seat="beta/b")
        out = wave.view()
        # the ladder itself is named
        assert "RECORDED -> CORROBORATED -> CONTESTED -> VOID" in out
        # and every rung is shown on its row
        assert f"[RECORDED]" in out and f"[CORROBORATED]" in out
        assert "[CONTESTED]" in out and "[VOID]" in out
        # effective ledger excludes VOID from standing; voids section carries the reason code
        assert "reason_code=FORGED" in out
        adm = gw._admission(_rows(wave))
        assert adm["statuses"][1] == "RECORDED"
        assert adm["statuses"][2] == "CORROBORATED" or adm["statuses"][2] == "CONTESTED"
        statuses = list(adm["statuses"].values())
        assert statuses.count("CORROBORATED") >= 1
        assert statuses.count("CONTESTED") == 1
        assert statuses.count("VOID") == 1

    def test_corroboration_needs_two_distinct_non_author_seats(self, wave, tmp_path):
        # Upgraded to the A3 lineage law (2026-10-01 owed): "distinct seats"
        # means distinct LINEAGES. Same lineage under two instance names is
        # the puppet shape and must stay one hand.
        ev = _evidence(tmp_path)
        r = wave.post("claim", "UNPROVEN", ev, seat="alpha/a")
        wave.witness(r["hash"], seat="beta/b1")
        assert gw._admission(_rows(wave))["statuses"][1] == "RECORDED", \
            "one witness is not corroboration"
        wave.witness(r["hash"], seat="beta/b2")  # same lineage, new instance: one hand
        assert gw._admission(_rows(wave))["statuses"][1] == "RECORDED", \
            "two rows from ONE lineage are still one hand (the puppet kill)"
        wave.witness(r["hash"], seat="gamma/c")
        assert gw._admission(_rows(wave))["statuses"][1] == "CORROBORATED"

    def test_verify_reports_admission_summary(self, wave, tmp_path):
        self._corroborated_row(wave, tmp_path)
        ok, msg = wave.verify()
        assert ok
        assert "ADMISSION:" in msg and "1 corroborated" in msg

    def test_contest_marks_and_stale_counter_renders(self, wave):
        r = wave.post("claim", "UNPROVEN", "AGENTS.md", seat="a")
        wave.contest(r["hash"], "disputed", seat="d")
        assert gw._admission(_rows(wave))["statuses"][1] == "CONTESTED"
        out = wave.view()
        assert "[pending]" in out or "STALE" in out


# ----------------------------------------------- 5. planted-failure propagation
class TestPlantedFailurePropagation:
    def test_false_premise_void_propagates_chain_visible(self, wave, tmp_path):
        """Plant a false premise, grow a descendant on it, corroborate it, then
        void the premise: the collapse must be visible from the chain alone."""
        premise = _evidence(tmp_path, name="false_premise.md", body="fabricated data")
        f = wave.post("FALSE PREMISE: the repo has 9 seats", "UNPROVEN",
                      premise, seat="alpha/f")
        # descendant physically chained on the premise (prev = premise hash)
        d = wave.post("descendant: therefore 9-seat rotation is proven", "UNPROVEN",
                      "AGENTS.md", seat="alpha/f")
        assert d["prev"] == f["hash"], "descendant stands on the premise"
        # two other hands (distinct lineages, A3 law) corroborate the false premise
        wave.witness(f["hash"], seat="beta/b")
        wave.witness(f["hash"], seat="gamma/c")
        assert gw._admission(_rows(wave))["statuses"][1] == "CORROBORATED", \
            "pre-corruption state: the false premise reads CORROBORATED"
        # an outside catch voids the premise (cross-signed)
        v = wave.void(f["hash"], "EVIDENCE_DEAD", "the premise evidence was "
                      "fabricated; descendant inherits the defect", seat="zeta/z",
                      witness="beta/b")
        wave.witness(v["hash"], seat="beta/b")
        adm = gw._admission(_rows(wave))
        assert adm["statuses"][1] == "VOID"
        # propagation is CHAIN-VISIBLE: the child and both witnesses are flagged
        props = {i: why for i, why in adm["propagation"]}
        assert props.get(2) == "child-of-void", "the descendant is flagged"
        witness_idxs = [i for i, r in enumerate(_rows(wave), 1)
                        if r.get("kind") == "witness" and r.get("signs") == f["hash"]]
        assert witness_idxs and all(props.get(i) == "witness-of-void"
                                    for i in witness_idxs), \
            "every signature on the dead premise is flagged"
        out = wave.view()
        assert "propagation" in out and "child-of-void" in out
        assert "witness-of-void" in out
        # and the tape itself stays LINKAGE-PASS: void is append-only containment
        ok, msg = wave.verify()
        assert ok, msg
        assert "1 voided" in msg

    def test_no_migration_legacy_tape_still_fails_and_rows_stay(self, wave):
        """A v1-v3-shaped tape with a row-122 clone keeps failing verify until a
        human voids it — v4 must not rewrite or forgive history on its own."""
        v3_row = {"prev": gw.GENESIS, "ts": "2026-09-13T12:49:28Z",
                  "claim": "legacy claim", "verdict": "UNPROVEN",
                  "evidence": "AGENTS.md", "note": "", "seat": "zcode",
                  "witness": ""}
        v3_row["hash"] = gw._row_hash(v3_row)
        clone122 = {"prev": "8ccd3924b908e8ca2f8c57d0deadbeefdeadbeefdeadbeefdeadbeefde",
                    "ts": "2026-09-16T04:17:37Z", "claim": "bypassed fragment"}
        with gw.LEDGER.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(v3_row, ensure_ascii=False) + "\n")
            fh.write(json.dumps(clone122, ensure_ascii=False) + "\n")
        ok, msg = wave.verify()
        assert not ok
        assert "MALFORMED_ROW" in msg and "row 2" in msg
        # legacy row keeps v3 semantics: readable, RECORDED, untouched
        rows = _rows(wave)
        assert rows[0]["verdict"] == "UNPROVEN" and "kind" not in rows[0]
        assert gw._row_hash(rows[0]) == rows[0]["hash"], "v1-v3 rows still hash valid"

    def test_legacy_void_repair_then_reanchor(self, wave):
        """The operator path A2 §5.4 describes, on a synthetic twin: void the
        hashless fragment AND the row chained past it; the tape then passes and
        the survivor stands — all by append, bytes untouched."""
        r1 = {"prev": gw.GENESIS, "ts": "t1", "claim": "good root",
              "verdict": "UNPROVEN", "evidence": "AGENTS.md", "note": "",
              "seat": "zcode", "witness": ""}
        r1["hash"] = gw._row_hash(r1)
        frag = {"prev": "8ccd3924b908e8ca2f8c57d0deadbeefdeadbeefdeadbeefdeadbeefde",
                "ts": "t2", "claim": "bypassed fragment"}
        r3 = {"prev": "", "ts": "t3", "claim": "unparented correction",
              "verdict": "SUPPORTED", "evidence": "AGENTS.md", "note": "n",
              "hash": ""}
        r3.pop("hash")  # unparented + chain-broken like live row 123
        r3["hash"] = gw._row_hash(r3)
        r4 = {"prev": r3["hash"], "ts": "t4", "claim": "chained after the break",
              "verdict": "UNPROVEN", "evidence": "AGENTS.md", "note": "",
              "seat": "zcode", "witness": ""}
        r4["hash"] = gw._row_hash(r4)
        with gw.LEDGER.open("a", encoding="utf-8") as fh:
            for r in (r1, frag, r3, r4):
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        ok, msg = wave.verify()
        assert not ok, "pre-void: the break is honestly visible"
        # containment: void the fragment (by line) and the unparented row (by hash)
        v1 = wave.void("#2", "MALFORMED", "hashless fragment", seat="z", witness="b")
        wave.witness(v1["hash"], seat="b")
        v2 = wave.void(r3["hash"], "MALFORMED", "empty prev", seat="z", witness="c")
        wave.witness(v2["hash"], seat="c")
        ok, msg = wave.verify()
        assert ok, f"post-void the tape passes: {msg}"
        assert "contained by void" in msg
        assert "2 voided" in msg
        # row 4 stands via direct chain; its bytes were never touched
        rows = _rows(wave)
        assert rows[3] == r4
        assert gw._admission(rows)["statuses"][4] == "RECORDED"

    def test_v3_hash_compat_with_legacy_key_sets(self, wave):
        """v1/v2/v3 rows must hash exactly as before (no auto-migration of the
        canonical form) — the wave_driver contract."""
        v1 = {"prev": "a" * 64, "ts": "t", "claim": "c", "verdict": "UNPROVEN",
              "evidence": "e", "note": "n"}
        v2 = dict(v1, seat="s")
        v3 = dict(v2, witness="w")
        core1 = json.dumps({k: v1.get(k, "") for k in gw._V1_KEYS},
                           sort_keys=True, ensure_ascii=False)
        core2 = json.dumps({k: v2.get(k, "") for k in gw._V2_KEYS},
                           sort_keys=True, ensure_ascii=False)
        core3 = json.dumps({k: v3.get(k, "") for k in gw._V3_KEYS},
                           sort_keys=True, ensure_ascii=False)
        import hashlib
        assert gw._row_hash(v1) == hashlib.sha256(core1.encode("utf-8")).hexdigest()
        assert gw._row_hash(v2) == hashlib.sha256(core2.encode("utf-8")).hexdigest()
        assert gw._row_hash(v3) == hashlib.sha256(core3.encode("utf-8")).hexdigest()
        # extra keys ride outside the hashed set (ttl_s contract)
        assert gw._row_hash(dict(v3, ttl_s=900)) == gw._row_hash(v3)
