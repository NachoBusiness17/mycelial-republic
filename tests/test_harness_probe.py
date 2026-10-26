"""harness_probe: the Harness2 loop on the leave-protocol mates (2026-10-17).

Pins the organ end to end on tmp trees with tmp keys (MAG_SEAT_KEY_DIR), no
model and no runner: blinded A/B packs that differ only by the delta, the
opt-in switch, 13 packs at k=1, composer verdicts signed with the composer's
own key, mate reviews signed with each mate's own key, the non-GLM gate, and
append-only, evidence-tied lessons that rib_boot mounts.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import tools.leave_dispatcher as ld
from mag import harness_probe as H
from mag import proposals as P
from mag import rib_boot
from mag import seat_handshake as sh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import seat_keygen as KG  # noqa: E402

MATES = ["cartographer", "locksmith", "archaeologist", "innkeeper", "jester", "lamplighter",
         "mariner", "gambiter"]
ROLES = ["editor_inv", "editor_dom", "composer"]


def _cfg(enabled=True):
    mk = lambda i: {"id": i, "persona": f"P {i}", "hunting_ground": f"G {i}", "seed_thread": f"S {i}"}  # noqa: E731
    return {"laws": "LAW ONE", "mates": [mk(m) for m in MATES],
            "harness_probe": {"enabled": enabled, "k": 1, "lesson_rib": "RIB_TEST.md",
                              "roles": [mk(r) for r in ROLES]}}


@pytest.fixture
def env(tmp_path, monkeypatch):
    keys = tmp_path / "keys"
    monkeypatch.setenv(sh.ENV_KEY_DIR, str(keys))
    # pytest's tmp tree sits inside this repo on the PC; the outside-repo guard is
    # pinned separately (test_keygen_refuses_a_repo_path), so tmp is allowed here.
    monkeypatch.setattr(KG, "_inside_repo", lambda p: False)
    rows = KG.keygen_mates(MATES + ROLES)
    grok = sh.generate_seed()
    seats = {r["seat_id"]: {"public_hex": r["public_hex"], "kind": "mate", "model_family": "glm"} for r in rows}
    seats["grok"] = {"public_hex": sh.public_from_seed(grok).hex()}
    al = {"schema": "seat_allowlist.v1", "skew_s": 60, "operator_seats": [],
          "quorum": {"default": 2, "require_non_glm_approval": True}, "seats": seats}
    d = {k: tmp_path / k for k in ("receipts", "state", "work", "proposals", "rib", "missions")}
    for p in d.values():
        p.mkdir()
    (d["rib"] / "RIB_TEST.md").write_text("# RIB TEST\n\n## The law\nold line one\nold line two\n", encoding="utf-8")
    kw = dict(receipts_dir=d["receipts"], state_dir=d["state"], work_dir=d["work"],
              proposals_root=d["proposals"], allowlist=al, rib_dir=d["rib"], log=lambda _m: None)
    return {"al": al, "grok": grok, "d": d, "kw": kw, "rows": rows, "keys": keys}


def _packs(env, today, cfg=None):
    kw = env["kw"]
    return H.write_round_packs(today, cfg or _cfg(), start_index=9, missions_dir=env["d"]["missions"],
                               template=ld.MISSION_TEMPLATE, cap=8, seed="t", **kw)


def _receipt(env, name, lines):
    (env["d"]["receipts"] / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _candidate(env, name, target="jester", cite="receipt_20261019_jester.md:3"):
    (env["d"]["work"] / "candidates").mkdir(exist_ok=True)
    (env["d"]["work"] / "candidates" / name).write_text(
        f"SCOPE: DOM\nTARGET_MATE: {target}\nDECISION: DELTA\n## HARNESS DELTA\n"
        f"Before walking, list the three files you will open first.\n## EVIDENCE\n- {cite} wandered\n",
        encoding="utf-8")


# ------------------------------------------------------------------ keys

def test_every_mate_gets_its_own_key_outside_the_repo(env, capsys):
    rows = env["rows"]
    assert len(rows) == 11 and {r["status"] for r in rows} == {"created"}
    assert len({r["public_hex"] for r in rows}) == 11
    for r in rows:
        p = Path(r["key_path"])
        assert p.parent == env["keys"] / "mates" and p.name == f"{sh.seat_slug(r['seat_id'])}.key"
    again = KG.keygen_mates(MATES + ROLES, allowlist=env["al"])
    assert {r["status"] for r in again} == {"exists"}  # never overwritten, never read
    assert [r["public_hex"] for r in again] == [r["public_hex"] for r in rows]


def test_keygen_refuses_a_repo_path_and_default_lives_outside(monkeypatch):
    target = ROOT / "configs" / "never_written.key"
    with pytest.raises(SystemExit, match="OUTSIDE"):
        KG.keygen("mate:jester", out=target)
    assert not target.exists()
    monkeypatch.delenv(sh.ENV_KEY_DIR, raising=False)
    p = sh.default_key_path("mate:jester")
    assert p.parts[-3:] == (".mag_seat", "mates", "mate__jester.key") and not KG._inside_repo(p)


def test_keygen_cli_prints_public_only(env, capsys, monkeypatch):
    monkeypatch.setenv(sh.ENV_KEY_DIR, str(env["keys"].parent / "keys2"))
    assert KG.main(["--mates"]) == 0
    out = capsys.readouterr().out
    for kf in (env["keys"].parent / "keys2" / "mates").glob("*.key"):
        seed_hex = json.loads(kf.read_text(encoding="utf-8"))["private_seed_hex"]  # tmp test key
        assert seed_hex not in out
    assert "fp=" in out and "mate:composer" in out


def test_merge_allowlist_adds_public_mate_rows(env, tmp_path):
    p = tmp_path / "allow.json"
    p.write_text(json.dumps({"schema": "seat_allowlist.v1", "quorum": {"default": 2}, "seats": {}}), encoding="utf-8")
    res = KG.merge_allowlist(env["rows"], p, today="2026-10-17")
    al = json.loads(p.read_text(encoding="utf-8"))
    assert len(res["added"]) == 11 and al["quorum"]["require_non_glm_approval"] is True
    assert al["seats"]["mate:jester"]["model_family"] == "glm"
    assert "private" not in json.dumps(al["seats"])
    bad = [dict(env["rows"][0], public_hex="00" * 32)]
    assert KG.merge_allowlist(bad, p)["conflicts"] == [env["rows"][0]["seat_id"]]


def test_each_mate_signs_with_its_own_key_and_cross_key_fails(env):
    al = env["al"]
    for mid in MATES + ROLES:
        msg = P.sign_message("proposal", {"title": "t", "targets": ["a.txt"], "diff": "d\n", "rationale": ""},
                             key_path=H.mate_key_path(mid))
        assert P.verify_message(msg, al) == f"mate:{mid}"
    seat, seed = sh.load_key(H.mate_key_path("jester"))
    forged = P.sign_message("proposal", {"title": "t", "targets": ["a.txt"], "diff": "d\n", "rationale": ""},
                            seed=seed, seat_id="mate:mariner")
    with pytest.raises(ValueError):
        P.verify_message(forged, al)
    with pytest.raises(ValueError, match="does not belong"):
        H.file_review("mariner", "p_20261017T000000Z_000000000000", "approve", "x",
                      key_path=H.mate_key_path("jester"), allowlist=al, proposals_root=env["d"]["proposals"])


# ------------------------------------------------------------------ probe

def test_blind_ids_are_distinct_labelled_and_seedable():
    a, b = H.assign_blind("s"), H.assign_blind("s")
    assert a == b and sorted(a.values()) == ["base", "cand"]
    assert all(H.BLIND_RE.fullmatch(i) for i in a)
    assert len({tuple(H.assign_blind().items()) for _ in range(20)}) > 1


def test_pair_differs_only_by_the_delta():
    blind = H.assign_blind(7)
    mate = {"persona": "P", "hunting_ground": "G", "seed_thread": "S"}
    pair = H.build_pair(ld.MISSION_TEMPLATE, "20261018", mate, "LAW", "- steer", "Do X first.", blind)
    cand = next(i for i in blind if blind[i] == "cand")
    base = next(i for i in blind if blind[i] == "base")
    n = {i: pair[i].replace(i, "<ID>") for i in pair}
    assert n[cand] == n[base] + H.DELTA_BLOCK.format(delta="Do X first.")
    assert "HARNESS DELTA" not in pair[base] and f"receipt_20261018_{base}.md" in pair[base]


def test_parse_candidate_demands_real_evidence(env):
    r = env["d"]["receipts"]
    _receipt(env, "receipt_20261019_jester.md", ["a", "b", "c"])
    ok = "DECISION: DELTA\n## HARNESS DELTA\nx\n## EVIDENCE\n- receipt_20261019_jester.md:3\n"
    assert H.parse_candidate(ok, r)["status"] == "delta"
    assert H.parse_candidate("DECISION: KEEP_BASE\n", r)["status"] == "keep_base"
    assert H.parse_candidate("DECISION: DELTA\n## HARNESS DELTA\nx\n", r)["status"] == "invalid"
    past = ok.replace(":3", ":99")
    assert "3 lines" in H.parse_candidate(past, r)["reason"]


def test_disabled_mode_adds_nothing():
    assert ld._harness_packs("20261020", _cfg(enabled=False), 9) == []
    assert ld._harness_packs("20261020", {"mates": []}, 9) == []
    import yaml
    shipped = yaml.safe_load(ld.CONFIG_PATH.read_text(encoding="utf-8"))
    assert shipped["harness_probe"]["enabled"] is False  # ships OFF
    assert [r["id"] for r in shipped["harness_probe"]["roles"]] == ROLES
    assert len(shipped["mates"]) == 8  # roles stay out of the daily mates list


# ------------------------------------------------------------------ full round

def test_full_round_thirteen_packs_signed_verdict_gate_and_lesson(env):
    d, al = env["d"], env["al"]
    _receipt(env, "receipt_20261019_jester.md", ["# r", "FINDINGS", "wandered three hours", "COUNTS 0"])
    _candidate(env, "candidate_20261019_editor_dom.md")

    day1 = _packs(env, "20261020")  # 2 editors + 1 probe pair; nothing to compose yet
    assert [p.name.split("_", 3)[3] for p in day1][:2] == ["editor_inv.md", "editor_dom.md"]
    assert len(day1) == 4 and day1[0].name == "mission_20261020_09_editor_inv.md"
    rnd = json.loads((d["state"] / "rounds" / "r_20261020_01.json").read_text(encoding="utf-8"))
    assert rnd["target_mate"] == "jester" and sorted(rnd["blind"].values()) == ["base", "cand"]
    cand = next(i for i in rnd["blind"] if rnd["blind"][i] == "cand")
    base = next(i for i in rnd["blind"] if rnd["blind"][i] == "base")
    assert {p.name for p in day1[2:]} == {f"mission_20261020_{n}_{i}.md" for n, i in
                                          zip(("11", "12"), sorted(rnd["blind"]))}
    for pid in rnd["blind"]:
        _receipt(env, f"receipt_20261020_{pid}.md", ["# r", "listed three files first", "found it", "COUNTS 1"])
    _receipt(env, "receipt_20261020_mariner.md", ["# r", "lost the map", "x"])
    _candidate(env, "candidate_20261020_editor_inv.md", target="mariner", cite="receipt_20261020_mariner.md:2")

    day2 = _packs(env, "20261021")  # 2 editors + pair for the new candidate + composer
    assert len(day2) == 5 and 8 + len(day2) == 13 <= ld.MAX_PARALLEL
    assert day2[-1].name == "mission_20261021_13_composer.md"
    comp = day2[-1].read_text(encoding="utf-8")
    assert "r_20261020_01" in comp and f"receipt_20261020_{cand}.md" in comp and "base" not in comp.split("Rounds:")[1]
    assert _packs(env, "20261021") == day2  # idempotent, no new round
    assert len(list((d["state"] / "rounds").glob("*.json"))) == 2

    (d["work"] / "verdicts" / "verdict_20261021_composer.md").write_text(
        f"ROUND: r_20261020_01\nCHOICE: {cand}\nACTION: adopt\nTARGET: configs/mates.yaml\n"
        "## DIFF\n--- a/configs/mates.yaml\n+++ b/configs/mates.yaml\n@@ -1 +1 @@\n-x\n+y\n"
        f"## EXPERIENCE\ncue: a mate starts a broad walk\nlesson: name the first three files before walking\n"
        f"evidence: receipt_20261020_{cand}.md:2; receipt_20261020_{base}.md:3\nconfidence: medium\n",
        encoding="utf-8")
    H.advance("20261022", _cfg(), **env["kw"])
    rec = json.loads((d["state"] / "verdicts" / "r_20261020_01.json").read_text(encoding="utf-8"))
    assert rec["outcome"] == "propose" and rec["label"] == "cand"
    pid = rec["proposal_id"]
    prop = json.loads((d["proposals"] / pid / "proposal.json").read_text(encoding="utf-8"))
    assert prop["payload"]["seat"] == "mate:composer"  # composer's own key

    # mates review through receipt lines; the host signs with each mate's own key
    _receipt(env, "receipt_20261022_jester.md", ["FINDINGS", f"REVIEW: {pid} approve held up at line 2"])
    _receipt(env, "receipt_20261022_mariner.md", ["FINDINGS", f"REVIEW: {pid} approve fine"])
    rib = d["rib"] / "RIB_TEST.md"
    old = rib.read_bytes()
    H.advance("20261023", _cfg(), **env["kw"])
    t = P.tally(pid, root=d["proposals"], allowlist=al)
    assert t["approvers"] == ["mate:jester", "mate:mariner"] and t["ready"] is False  # GLM room alone
    assert rib.read_bytes() == old

    P.submit(P.sign_message("review", {"proposal_id": pid, "verdict": "approve", "reason": "ok"},
                            seed=env["grok"], seat_id="grok"), root=d["proposals"], allowlist=al)
    H.advance("20261023", _cfg(), **env["kw"])
    t = P.tally(pid, root=d["proposals"], allowlist=al)
    assert t["ready"] and t["promoted"]
    new = rib.read_bytes()
    assert new.startswith(old) and f"harness2 lesson {pid}".encode() in new
    mounted = rib_boot._amendment_sections(new.decode("utf-8"))
    assert any(pid in s and "name the first three files" in s for s in mounted)
    H.advance("20261024", _cfg(), **env["kw"])
    assert rib.read_bytes() == new  # idempotent


def test_keep_base_and_unevidenced_verdicts_file_nothing(env):
    blind = H.assign_blind(3)
    rnd = {"round_id": "r_20261020_01", "date": "20261020", "blind": blind}
    for pid in blind:
        _receipt(env, f"receipt_20261020_{pid}.md", ["a", "b"])
    base = next(i for i in blind if blind[i] == "base")
    cand = next(i for i in blind if blind[i] == "cand")
    exp = {"cue": "c", "lesson": "l", "evidence": f"receipt_20261020_{base}.md:2", "confidence": "low"}
    v = {"choice": base, "action": "adopt", "experience": exp}
    assert H.judge(v, rnd, env["d"]["receipts"])["outcome"] == "keep_base"
    v = {"choice": cand, "action": "adopt", "experience": dict(exp, evidence="it felt better")}
    assert H.judge(v, rnd, env["d"]["receipts"])["outcome"] == "invalid"
    v = {"choice": cand, "action": "adopt", "experience": dict(exp, evidence=f"receipt_20261020_{cand}.md:9")}
    assert H.judge(v, rnd, env["d"]["receipts"])["outcome"] == "invalid"
    v = {"choice": "probe-000000", "action": "adopt", "experience": exp}
    assert H.judge(v, rnd, env["d"]["receipts"])["outcome"] == "invalid"


def test_lesson_refused_unless_adopted(env):
    rib = env["d"]["rib"] / "RIB_TEST.md"
    old = rib.read_bytes()
    exp = {"cue": "c", "lesson": "l", "evidence": "receipt_20261020_probe-aaaaaa.md:1", "confidence": "low"}
    t = {"ready": True, "promoted": False, "author": "mate:composer", "approvers": []}
    assert H.append_lesson("p_20261017T000000Z_000000000000", exp, rib, t, "r")["ok"] is False
    t = {"ready": True, "promoted": True, "author": "mate:composer", "approvers": ["grok"]}
    assert H.append_lesson("p_20261017T000000Z_000000000000", dict(exp, evidence="none"), rib, t, "r")["ok"] is False
    assert rib.read_bytes() == old
