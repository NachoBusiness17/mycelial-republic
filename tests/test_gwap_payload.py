"""tests for mag/gwap_payload.py -- rung B3 falsifiers.

Determinism law: identical inputs produce byte-identical payloads (canonical
equality) and byte-identical ledger files across independent stores. Chain law:
rows are hash-chained from a 64-zero genesis; editing, deleting, or corrupting a
row must be detected with the 1-based index of the first bad row, and a broken
chain is never extended. Blocker law: the scene's top-5 common words are taboo
(alphabetical tie-break, no RNG) and any taboo token inside an intent/report
verdicts the incident BLOCKED regardless of agreement. Verdict ladder law: exact
claim-set fractions hit each band edge (0.6 inclusive, 0.3 inclusive). Collusion
law: copied order fires between different authors, shuffled order never does,
one lone claim carries no order signal, same-author structs are not independent.
v1 laws: a fired fingerprint demotes VERIFIED_AGREE to CHALLENGE (BLOCKED
precedence and the other bands untouched) and taints the CHALLENGE rarity;
ed25519 signatures seal the canonical payload bytes (minus the signature
block itself) and any post-signing byte change anywhere fails offline
verification. Zero-argument v0 call shapes keep their exact v0 behavior.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import mag.gwap_payload as gw
from mag.gwap_payload import (
    SCHEMA, BLOCKED, CHALLENGE, DISPUTE, VERIFIED_AGREE, GwapError,
    SessionLedger, agreement_score, anon_id, build_payload, build_taboo_list,
    canonical, check_taboos, collusion_fingerprint, decide_verdict,
    verify_chain_file,
)

UTC = "2026-09-29T12:00:00Z"
TAPE = {"sha256": "0" * 64, "engine_version": "test-engine-0"}
PARTS = [
    {"anon_id": "r1", "role": "robber"},
    {"anon_id": "c1", "role": "cop"},
    {"anon_id": "w1", "role": "witness"},
]


def claim(s: str, v: str, o: str, q: str = "") -> dict[str, str]:
    return {"subject": s, "verb": v, "object": o, "qualifier": q}


def intent(claims, author="r1"):
    return {"author": author, "claims": list(claims)}


def report(claims, author="c1"):
    return {"author": author, "claims": list(claims)}


def build(**over):
    args = dict(
        scene_id="scene-042",
        intent_struct=intent([claim("a", "did", "x"), claim("b", "did", "y")]),
        report_struct=report([claim("a", "did", "x")]),
        participants=PARTS,
        consent=True,
        created_utc=UTC,
        replay_tape_ref=TAPE,
    )
    args.update(over)
    return build_payload(**args)


@pytest.fixture()
def store(tmp_path, monkeypatch):
    monkeypatch.setattr(gw, "STORE", tmp_path)
    return tmp_path


# -- schema shape ------------------------------------------------------------------


def test_payload_shape_extends_paper_schema():
    p = build()
    paper_keys = {
        "scene_id", "intent_struct", "report_struct", "agreement_score",
        "blocker_taboo_list", "witness_clue_chain", "verdict",
    }
    extension_keys = {
        "schema", "participants", "consent", "meter_credit", "replay_tape_ref",
        "signature", "created_utc", "taboo_violations", "collusion_fingerprint",
    }
    assert p["schema"] == SCHEMA == "mag_gwap_payload.v1"
    assert set(p) == paper_keys | extension_keys
    assert set(p["meter_credit"]) == {"artifact_rarity", "byte_backed",
                                      "receipt_sha256"}
    assert p["meter_credit"]["byte_backed"] is True
    assert p["signature"] == {"scheme": "unsigned-v0", "signed_by": []}
    # claim normalization: qualifier always present, order preserved as authored
    assert p["intent_struct"]["claims"][0] == {
        "subject": "a", "verb": "did", "object": "x", "qualifier": ""
    }


def test_participants_and_consent_round_trip():
    p = build(consent=False)
    assert p["consent"] is False
    assert p["participants"] == PARTS


# -- determinism -------------------------------------------------------------------


def test_determinism_byte_identical_payload():
    p1, p2 = build(), build()
    assert canonical(p1) == canonical(p2)
    assert p1["meter_credit"]["receipt_sha256"] == p2["meter_credit"]["receipt_sha256"]
    p3 = build(created_utc="2026-09-29T13:00:00Z")
    assert canonical(p3) != canonical(p1)
    assert p3["meter_credit"]["receipt_sha256"] != p1["meter_credit"]["receipt_sha256"]


def test_receipt_sha256_hashes_the_body():
    p = build()
    body = {k: v for k, v in p.items() if k != "meter_credit"}
    import hashlib
    expected = hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()
    assert p["meter_credit"]["receipt_sha256"] == expected


def test_anon_id_deterministic_secret_free():
    assert anon_id("robber-1") == anon_id("robber-1")
    assert anon_id("robber-1") != anon_id("robber-2")
    import hashlib
    assert anon_id("robber-1") == "gw-" + hashlib.sha256(
        b"mag_gwap_payload.v1:robber-1").hexdigest()[:12]


# -- agreement engine --------------------------------------------------------------


def test_agreement_full_match_scores_one():
    claims = [claim("a", "did", "x"), claim("b", "did", "y", "at night")]
    assert agreement_score(intent(claims), report(claims)) == 1.0


def test_agreement_empty_union_scores_zero():
    assert agreement_score(intent([]), report([])) == 0.0


def test_verdict_bands_exact_fractions():
    a, b, c = claim("a", "did", "1"), claim("b", "did", "2"), claim("c", "did", "3")
    d, e = claim("d", "did", "4"), claim("e", "did", "5")

    # 3 shared of a 5-triple union: exactly 0.6, the inclusive lower edge
    s = agreement_score(intent([a, b, c, d, e]), report([a, b, c]))
    assert s == 0.6
    assert decide_verdict(s) == VERIFIED_AGREE

    # 2 shared of 5: 0.4 mid band
    s = agreement_score(intent([a, b, c, d, e]), report([a, b]))
    assert s == 0.4
    assert decide_verdict(s) == CHALLENGE

    # 0 shared: 0.0 floor
    s = agreement_score(intent([a, b, c, d, e]), report([]))
    assert s == 0.0
    assert decide_verdict(s) == DISPUTE


def test_witness_claims_count_at_half_weight():
    a, b = claim("a", "did", "1"), claim("b", "did", "2")
    chain = [{"witness": "w1", "prompt": "what happened?",
              "answer": "b did 2", "claims": [b]}]
    # cop alone reconstructs half the intent: 0.5
    assert agreement_score(intent([a, b]), report([a])) == 0.5
    # the witness corroborates the missed claim at 0.5: 1.5/2 = 0.75
    assert agreement_score(intent([a, b]), report([a]), chain) == 0.75
    # witness can never out-credit the cop's own claim
    assert agreement_score(intent([a, b]), report([a, b]), chain) == 1.0


def test_claim_stuffing_is_worthless():
    a, b = claim("a", "did", "1"), claim("b", "did", "2")
    stuffed = [a] * 7 + [b]
    assert agreement_score(intent(stuffed), report([a, b])) == 1.0
    assert agreement_score(intent([a, b]), report(stuffed)) == 1.0


# -- blocker -----------------------------------------------------------------------


def test_taboo_list_top5_alphabetical_ties():
    corpus = [
        claim("p1", "v1", "vault"),                  # vault 4
        claim("p2", "v2", "vault"),
        claim("p3", "v3", "vault"),
        claim("p4", "v4", "vault"),
        claim("p5", "v5", "cash"),                   # cash 3
        claim("p6", "v6", "cash"),
        claim("p7", "v7", "cash"),
        claim("p8", "v8", "grab"),                   # grab 3
        claim("p9", "v9", "grab"),
        claim("p10", "v10", "grab"),
        claim("p11", "v11", "mask"),                 # mask 2
        claim("p12", "v12", "mask"),
        claim("p13", "v13", "safe"),                 # safe 2
        claim("p14", "v14", "safe"),
        claim("p15", "v15", "key"),                  # key 1, drill 1
        claim("p16", "v16", "drill"),
    ]
    taboo = build_taboo_list(corpus)
    assert taboo == ["vault", "cash", "grab", "mask", "safe"]
    assert build_taboo_list(corpus) == taboo  # deterministic, no RNG


def test_check_taboos_is_token_level():
    taboo = ["vault"]
    assert check_taboos([claim("mole", "opened", "the vault")], taboo) == ["vault"]
    assert check_taboos([claim("mole", "opened", "VAULT!")], taboo) == ["vault"]
    assert check_taboos([claim("mole", "opened", "the vaulted case")], taboo) == []
    assert check_taboos([claim("mole", "opened", "deposit boxes")], taboo) == []


def test_blocked_verdict_outranks_agreement():
    taboo = ["vault"]
    claims = [claim("mole", "opened", "vault"), claim("b", "did", "y")]
    p = build(
        intent_struct=intent(claims),
        report_struct=report(claims),
        taboo_list=taboo,
    )
    assert p["agreement_score"] == 1.0          # they agree perfectly
    assert p["verdict"] == BLOCKED              # on a banned word
    assert p["taboo_violations"] == ["vault"]
    assert p["meter_credit"]["artifact_rarity"] == "void"
    # a taboo in the REPORT alone is equally fatal
    p2 = build(
        intent_struct=intent([claim("a", "did", "x")]),
        report_struct=report([claim("mole", "opened", "vault")]),
        taboo_list=taboo,
    )
    assert p2["verdict"] == BLOCKED


# -- collusion fingerprint ----------------------------------------------------------


def test_collusion_fires_on_copied_order_not_shuffled():
    a, b, c = claim("a", "did", "1"), claim("b", "did", "2"), claim("c", "did", "3")
    # copied verbatim, order included, different authors: fires
    fp = collusion_fingerprint(intent([a, b, c]), report([a, b, c]))
    assert fp["suspected_collusion"] is True
    # same set, different order: honest independent reconstruction: never fires
    fp = collusion_fingerprint(intent([a, b, c]), report([c, b, a]))
    assert fp["suspected_collusion"] is False
    assert fp["evidence"] == "claim orders differ"
    # a single matching claim carries no order information
    fp = collusion_fingerprint(intent([a]), report([a]))
    assert fp["suspected_collusion"] is False
    assert fp["compared_claims"] == 1
    # same author on both structs is not independent authorship
    fp = collusion_fingerprint(intent([a, b, c]), report([a, b, c], author="r1"))
    assert fp["suspected_collusion"] is False


def test_collusion_auto_downgrades_verified_agree_to_challenge():
    # v1 change (amends v0 design decision 2): a fired order fingerprint no
    # longer lets a copied round bank as VERIFIED_AGREE -- judgment is owed
    # first, so the ladder demotes it to CHALLENGE and the rarity carries the
    # taint ("tainted", not a clean "uncommon").
    claims = [claim("a", "did", "1"), claim("b", "did", "2"), claim("c", "did", "3")]
    p = build(intent_struct=intent(claims), report_struct=report(claims))
    assert p["agreement_score"] == 1.0
    assert p["verdict"] == CHALLENGE                 # downgraded from VERIFIED_AGREE
    assert p["collusion_fingerprint"]["suspected_collusion"] is True
    assert p["meter_credit"]["artifact_rarity"] == "tainted"

    # an honest shuffled reconstruction keeps its clean verdict and rarity
    p2 = build(intent_struct=intent(claims),
               report_struct=report([claims[2], claims[0], claims[1]]))
    assert p2["verdict"] == VERIFIED_AGREE
    assert p2["meter_credit"]["artifact_rarity"] == "rare"


def test_decide_verdict_collusion_downgrade_path():
    # BLOCKED still outranks everything, collusion flag or not
    assert decide_verdict(1.0, ["vault"], True) == BLOCKED
    # the demotion applies on the whole VERIFIED_AGREE band, edge included
    assert decide_verdict(1.0, (), True) == CHALLENGE
    assert decide_verdict(0.6, (), True) == CHALLENGE
    # CHALLENGE and DISPUTE rows are unchanged by the flag
    assert decide_verdict(0.4, (), True) == CHALLENGE
    assert decide_verdict(0.0, (), True) == DISPUTE
    # v0 API stability: the two-argument call keeps its exact v0 behavior
    assert decide_verdict(1.0) == VERIFIED_AGREE
    assert decide_verdict(0.6, []) == VERIFIED_AGREE
    assert decide_verdict(0.4) == CHALLENGE
    assert decide_verdict(0.2) == DISPUTE


def test_rarity_taint_follows_the_downgrade():
    # the v0 taint (VERIFIED_AGREE + collusion) is defensively kept for direct
    # ladder calls, but through build_payload the downgrade routes collusion
    # rows to CHALLENGE, where the taint now lands instead of "uncommon".
    assert gw.default_artifact_rarity(VERIFIED_AGREE, True) == "tainted"
    assert gw.default_artifact_rarity(VERIFIED_AGREE, False) == "rare"
    assert gw.default_artifact_rarity(CHALLENGE, True) == "tainted"
    assert gw.default_artifact_rarity(CHALLENGE, False) == "uncommon"
    assert gw.default_artifact_rarity(DISPUTE, False) == "common"
    assert gw.default_artifact_rarity(BLOCKED, True) == "void"


# -- signatures (v1) --------------------------------------------------------------------

needs_crypto = pytest.mark.skipif(
    not gw.HAS_CRYPTO, reason="cryptography package not installed in this venv"
)


@needs_crypto
def test_author_keypair_deterministic_and_distinct():
    priv_a1, pub_a1 = gw.author_keypair("secret-seed-a")
    priv_a2, pub_a2 = gw.author_keypair("secret-seed-a")
    priv_b, pub_b = gw.author_keypair("secret-seed-b")
    assert (priv_a1, pub_a1) == (priv_a2, pub_a2)   # deterministic, no RNG
    assert priv_a1 != priv_b and pub_a1 != pub_b    # seeds part ways
    assert len(priv_a1) == 64 and len(pub_a1) == 64  # 32-byte hex bodies


@needs_crypto
def test_sign_verify_roundtrip():
    p = build()
    priv_hex, pub_hex = gw.author_keypair("robber-key-1")
    signed = gw.sign_payload(p, "r1", priv_hex)
    block = signed["signature"]
    assert set(block) == {"algo", "pubkey", "sig", "signed_by"}
    assert block["algo"] == gw.SIG_ALGO == "ed25519-v1"
    assert block["pubkey"] == pub_hex
    assert block["signed_by"] == ["r1"]
    assert gw.verify_signature(signed) is True
    # the input payload is never mutated: v0 bytes stay v0
    assert p["signature"] == {"scheme": "unsigned-v0", "signed_by": []}
    # unsigned payloads never verify
    assert gw.verify_signature(p) is False
    # the build-time receipt is preserved; the signature commits to it
    assert (signed["meter_credit"]["receipt_sha256"]
            == p["meter_credit"]["receipt_sha256"])
    # Ed25519 is deterministic (RFC 8032): same bytes, same signature
    again = gw.sign_payload(p, "r1", priv_hex)
    assert again["signature"]["sig"] == block["sig"]


@needs_crypto
def test_sign_then_tamper_fails_offline():
    priv_hex, _pub = gw.author_keypair("robber-key-2")
    signed = gw.sign_payload(build(), "r1", priv_hex)
    assert gw.verify_signature(signed) is True

    def tampered(*path):
        broken = json.loads(canonical(signed))
        node = broken
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = "forged"
        return broken

    # a claim object, the score, the verdict, the receipt: any byte change
    # anywhere (the signature covers everything but its own block)
    assert gw.verify_signature(tampered("scene_id")) is False
    assert gw.verify_signature(
        tampered("intent_struct", "claims", 0, "object")) is False
    assert gw.verify_signature(tampered("agreement_score")) is False
    assert gw.verify_signature(tampered("verdict")) is False
    assert gw.verify_signature(
        tampered("meter_credit", "receipt_sha256")) is False
    # and the signature block itself: a swapped pubkey or mangled sig
    swapped = json.loads(canonical(signed))
    other_priv, other_pub = gw.author_keypair("robber-key-3")
    swapped["signature"]["pubkey"] = other_pub
    assert gw.verify_signature(swapped) is False
    mangled = json.loads(canonical(signed))
    mangled["signature"]["sig"] = "0" * 128
    assert gw.verify_signature(mangled) is False


@needs_crypto
def test_sign_payload_wiring_and_key_validation():
    p = build()
    priv_hex, _pub = gw.author_keypair("robber-key-4")
    # the signer must be a declared participant (same wiring law as claims)
    with pytest.raises(GwapError) as exc:
        gw.sign_payload(p, "ghost", priv_hex)
    assert exc.value.reason == "SIGNATURE"
    # private key material must be a 32-byte hex seed
    with pytest.raises(GwapError) as exc:
        gw.sign_payload(p, "r1", "nothex")
    assert exc.value.reason == "BAD_KEY"
    # only engine payloads are signed
    with pytest.raises(GwapError) as exc:
        gw.sign_payload({"schema": "other.v1"}, "r1", priv_hex)
    assert exc.value.reason == "BAD_SCHEMA"


def test_verify_signature_never_raises_on_junk():
    assert gw.verify_signature(None) is False
    assert gw.verify_signature("row") is False
    assert gw.verify_signature({}) is False
    assert gw.verify_signature(
        {"signature": {"algo": "ed25519-v1"}}) is False


# -- session ledger ------------------------------------------------------------------


def three_rows(store):
    ledger = SessionLedger("sess-1")
    ids = []
    for scene in ("s1", "s2", "s3"):
        row = ledger.append(build(scene_id=scene), ts_utc=UTC)
        ids.append(row)
    return ledger, ids


def test_ledger_genesis_and_chain(store):
    ledger, rows = three_rows(store)
    assert [r["seq"] for r in rows] == [1, 2, 3]
    assert rows[0]["prev_sha256"] == "0" * 64
    assert rows[1]["prev_sha256"] == rows[0]["row_sha256"]
    assert rows[2]["prev_sha256"] == rows[1]["row_sha256"]
    assert ledger.verify_chain() == (True, None)
    # reopening the file sees the same intact chain
    reopened = SessionLedger("sess-1")
    assert reopened.verify_chain() == (True, None)
    assert len(reopened.rows) == 3


def test_ledger_tamper_edit_detected(store):
    ledger, _ = three_rows(store)
    lines = ledger.path.read_text(encoding="utf-8").splitlines()
    row2 = json.loads(lines[1])
    row2["payload"]["scene_id"] = "forged"          # edit without rehashing
    lines[1] = canonical(row2)
    ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert verify_chain_file(ledger.path) == (False, 2)
    with pytest.raises(GwapError) as exc:
        SessionLedger("sess-1")                     # construction fails closed
    assert exc.value.reason == "BROKEN_CHAIN"


def test_ledger_tamper_delete_and_garbage_detected(store):
    ledger, _ = three_rows(store)
    lines = ledger.path.read_text(encoding="utf-8").splitlines()
    del lines[1]                                    # delete a middle row
    ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert verify_chain_file(ledger.path) == (False, 2)

    # corrupt a line into unparseable bytes
    ledger3 = SessionLedger("sess-2")
    ledger3.append(build(scene_id="s1"), ts_utc=UTC)
    ledger3.append(build(scene_id="s2"), ts_utc=UTC)
    lines = ledger3.path.read_text(encoding="utf-8").splitlines()
    lines[0] = "{not json"
    ledger3.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert verify_chain_file(ledger3.path) == (False, 1)


def test_append_refuses_broken_chain_and_foreign_schema(store):
    ledger, _ = three_rows(store)
    lines = ledger.path.read_text(encoding="utf-8").splitlines()
    lines[2] = lines[2].replace('"seq":3', '"seq":9')
    ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(GwapError) as exc:
        SessionLedger("sess-1").append(build(), ts_utc=UTC)
    assert exc.value.reason == "BROKEN_CHAIN"

    clean = SessionLedger("sess-3")
    with pytest.raises(GwapError) as exc:
        clean.append({"schema": "something.else"})
    assert exc.value.reason == "BAD_SCHEMA"


def test_ledger_bytes_identical_across_stores(tmp_path):
    payloads = [build(scene_id=s) for s in ("s1", "s2")]
    paths = []
    for i in range(2):
        ledger = SessionLedger("sess-x", store=tmp_path / f"store{i}")
        for p in payloads:
            ledger.append(p, ts_utc=UTC)
        paths.append(ledger.path)
    assert paths[0].read_bytes() == paths[1].read_bytes()


# -- validation ----------------------------------------------------------------------


def test_validation_rejects_bad_inputs():
    with pytest.raises(GwapError) as exc:
        build(created_utc="yesterday")
    assert exc.value.reason == "BAD_TS"

    with pytest.raises(GwapError) as exc:
        build(replay_tape_ref={"sha256": "nothex", "engine_version": "e"})
    assert exc.value.reason == "BAD_TAPE"

    with pytest.raises(GwapError) as exc:
        build(consent="yes")
    assert exc.value.reason == "BAD_CONSENT"

    # role wiring: the intent author must be a declared robber
    with pytest.raises(GwapError) as exc:
        build(intent_struct=intent([claim("a", "did", "x")], author="c1"))
    assert exc.value.reason == "ROLE_WIRING"

    # an undeclared witness is a wiring error too
    with pytest.raises(GwapError) as exc:
        build(witness_clue_chain=[{
            "witness": "ghost", "prompt": "p", "answer": "a",
            "claims": [claim("a", "did", "x")],
        }])
    assert exc.value.reason == "ROLE_WIRING"

    with pytest.raises(GwapError) as exc:
        build(participants=[{"anon_id": "r1", "role": "wizard"}])
    assert exc.value.reason == "BAD_PARTICIPANTS"
