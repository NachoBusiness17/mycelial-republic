"""Tests for the shared-verkle trigger language (memlang)."""
import mag.memlang as ml


def test_vocab_has_expected_opcodes():
    v = ml.vocab()
    assert v["opcodes"]["handoff_build"] == 2
    assert v["opcodes"]["rib_elevate"] == 1
    assert v["opcodes"]["memo"] == 0


def test_compile_token_is_binary_and_reveals_no_spec():
    c = ml.compile_token("handoff_build", "grok writes a compact spec -> cheap agent executes", {"budget": "free"})
    assert c["ok"]
    assert c["token_len"] > 0
    # the binary token must NOT contain the readable spec
    assert b"grok writes" not in bytes.fromhex(c["token_hex"])
    assert c["anchor_hex"]


def test_decode_roundtrips_opcode_and_anchor():
    c = ml.compile_token("research_pack", "run the corpus pack")
    d = ml.decode(c["token_hex"])
    assert d["ok"]
    assert d["action"] == "research_pack"
    assert d["anchor_hex"] == c["anchor_hex"]


def test_resolve_reconstructs_intent_from_shared_state():
    spec = "grok writes a compact spec -> cheap agent executes"
    c = ml.compile_token("handoff_build", spec, {"budget": "free"})
    r = ml.resolve(c["token_hex"])
    assert r["ok"]
    assert r["action"] == "handoff_build"
    assert r["spec"] == spec  # reconstructed from shared registry, not the token


def test_trigger_without_execute_resolves_only():
    c = ml.compile_token("memo", "log only")
    t = ml.trigger(c["token_hex"], execute=False)
    assert t["ok"] and t["executed"] is False


def test_trigger_executes_memo():
    c = ml.compile_token("memo", "log this")
    t = ml.trigger(c["token_hex"], execute=True)
    assert t["executed"] is True


def test_roundtrip_proves_token_only_trigger():
    rt = ml.roundtrip("trigger action from a bare token", "handoff_build")
    assert rt["ok"]
    assert rt["reveals_spec_in_token"] is False  # the token alone reveals nothing readable


def test_bad_magic_rejected():
    d = ml.decode("00" * 40)
    assert not d.get("ok")
