"""A2 context freeze: system prompt + tool schemas byte-identical per session.

Two consecutive repack_messages() outputs must carry an IDENTICAL frozen
prefix hash — live values (fresh pack text, residual crumbs, goal) ride in a
small evolving tail after the prefix, never inside it. No remote calls.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mag.agent_cli as ac  # noqa: E402
from mag.context_pack import (  # noqa: E402
    EVOLVING_TAIL_MARKER,
    _FROZEN_PROMPTS,
    evolving_tail,
    freeze_system_prompt,
)

SID = "test-context-freeze-session"


def _fat_history(goal: str, crumbs: str) -> list[dict]:
    return [
        {"role": "system", "content": "old system"},
        {"role": "user", "content": goal},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "c1",
                    "type": "function",
                    "function": {"name": "list_dir", "arguments": "{}"},
                }
            ],
        },
        {"role": "tool", "tool_call_id": "c1", "content": crumbs},
    ]


def _repack(goal: str, crumbs: str) -> list[dict]:
    return ac.repack_messages(
        _fat_history(goal, crumbs),
        user_text=goal,
        traces=["list_dir: ok=True"],
        provider="deepseek",
        session_id=SID,
    )


def test_two_consecutive_repack_outputs_share_prefix_hash():
    out1 = _repack("goal A", '{"ok": true, "note": "' + "a" * 300 + '"}')
    out2 = _repack(
        "goal B — different live values entirely", '{"ok": false, "note": "' + "b" * 300 + '"}'
    )
    assert out1[0]["role"] == "system" and out2[0]["role"] == "system"
    sys1, sys2 = out1[0]["content"], out2[0]["content"]

    # The frozen prefix is everything before the evolving-tail marker.
    prefix1 = sys1.split(EVOLVING_TAIL_MARKER)[0]
    prefix2 = sys2.split(EVOLVING_TAIL_MARKER)[0]
    hash1 = hashlib.sha256(prefix1.encode("utf-8")).hexdigest()
    hash2 = hashlib.sha256(prefix2.encode("utf-8")).hexdigest()
    assert hash1 == hash2, f"prefix hash drifted across consecutive repacks: {hash1} != {hash2}"

    # It must also match the freeze registry's recorded bytes for the session.
    # (Registry hash = sha256(prefix + NUL seam + canonical schema bytes).)
    frozen = _FROZEN_PROMPTS[SID]
    seam_hash = hashlib.sha256()
    seam_hash.update(frozen["prefix_text"].encode("utf-8"))
    seam_hash.update(b"\x00--tool-schemas--\x00")
    seam_hash.update(frozen["tool_schemas_text"].encode("utf-8"))
    assert frozen["prefix_hash"] == seam_hash.hexdigest(), "registry hash does not cover prefix+schemas"
    assert prefix1 == prefix2 == frozen["prefix_text"], "prefix bytes not byte-identical"

    # Live values actually moved to the tail: whole system messages differ
    # (fresh pack/goal per repack) while the prefix stayed identical.
    assert sys1 != sys2, "tail did not evolve — live values still frozen into the prefix"
    assert EVOLVING_TAIL_MARKER in sys1 and EVOLVING_TAIL_MARKER in sys2
    print("PASS test_two_consecutive_repack_outputs_share_prefix_hash")
    print("  prefix_hash:", hash1)
    print("  prefix_chars:", frozen["prefix_chars"], "· sys1 chars:", len(sys1), "· sys2 chars:", len(sys2))


def test_freeze_returns_identical_bytes_despite_input_drift():
    f1 = freeze_system_prompt("stable body v1", tool_schemas=[{"a": 1}], session_id="drift-sid")
    f2 = freeze_system_prompt("stable body CHANGED", tool_schemas=[{"a": 999}], session_id="drift-sid")
    assert f1 is f2 or f1["prefix_text"] == f2["prefix_text"]
    assert f1["prefix_hash"] == f2["prefix_hash"]
    assert f2["prefix_text"] == "stable body v1", "frozen bytes mutated by drifted input"
    print("PASS test_freeze_returns_identical_bytes_despite_input_drift")


def test_refreeze_starts_new_prefix():
    f1 = freeze_system_prompt("prefix one", session_id="refreeze-sid")
    f2 = freeze_system_prompt("prefix two", session_id="refreeze-sid", refreeze=True)
    assert f1["prefix_hash"] != f2["prefix_hash"]
    assert f2["prefix_text"] == "prefix two"
    print("PASS test_refreeze_starts_new_prefix")


def test_tool_schemas_hash_covers_bytes():
    s = [{"type": "function", "function": {"name": "list_dir", "parameters": {"b": 2, "a": 1}}}]
    f1 = freeze_system_prompt("p", tool_schemas=s, session_id="schema-sid")
    # same schemas, different key order in the dict → canonical bytes identical
    s_reordered = [{"function": {"parameters": {"a": 1, "b": 2}, "name": "list_dir"}, "type": "function"}]
    f2 = freeze_system_prompt("other prefix", tool_schemas=s_reordered, session_id="schema-sid2")
    assert f1["tool_schemas_text"] == f2["tool_schemas_text"], "canonical schema serialization drifted"
    assert f1["prefix_hash"] != f2["prefix_hash"], "different prefixes must hash differently"
    print("PASS test_tool_schemas_hash_covers_bytes")


def test_evolving_tail_stays_small_and_marks_itself():
    big_pack = "x" * 20_000
    tail = evolving_tail(goal="g", pack_text=big_pack, residual="r", repacked=True, max_chars=3000)
    assert tail.startswith(EVOLVING_TAIL_MARKER)
    assert len(tail) <= 3000, f"tail not capped: {len(tail)} > 3000"
    assert "Auto-repack" in tail
    print("PASS test_evolving_tail_stays_small_and_marks_itself len:", len(tail))


def test_new_instructions_ride_as_trailing_developer_messages():
    """openai-week fold: new instructions arrive as trailing developer messages.

    The frozen system prefix must not move a byte because of them — new
    instructions append at the END of the payload, never splice into the
    prefix (a mid-prefix insert re-prices the whole context).
    """
    instr1 = "NEW INSTRUCTION v1: prefer run_shell for probes"
    hist1 = _fat_history("goal C", '{"ok": true}')
    hist1.append({"role": "developer", "content": instr1})
    out1 = ac.repack_messages(
        hist1, user_text="goal C", traces=[], provider="deepseek", session_id=SID
    )

    instr2 = "NEW INSTRUCTION v2: switch to audit mode"
    hist2 = _fat_history("goal D — different live values", '{"ok": false}')
    hist2.append({"role": "developer", "content": instr2})
    out2 = ac.repack_messages(
        hist2, user_text="goal D", traces=[], provider="deepseek", session_id=SID
    )

    # Prefix byte-stable across both instruction-bearing repacks — and still
    # equal to the registry bytes frozen by the earlier (instruction-free) test.
    prefix1 = out1[0]["content"].split(EVOLVING_TAIL_MARKER)[0]
    prefix2 = out2[0]["content"].split(EVOLVING_TAIL_MARKER)[0]
    assert prefix1 == prefix2 == _FROZEN_PROMPTS[SID]["prefix_text"], (
        "system prefix moved under new instructions"
    )

    # Each instruction survives verbatim as a TRAILING developer message that
    # sits AFTER the frozen system prefix — and never leaked into the prefix.
    for out, needle in ((out1, instr1), (out2, instr2)):
        dev = [m for m in out if m.get("role") == "developer"]
        assert dev, f"no developer message in repack output: {[m.get('role') for m in out]}"
        assert dev[-1]["content"] == needle, "instruction lost or mutated in transit"
        assert out.index(dev[-1]) > out.index(
            next(m for m in out if m.get("role") == "user")
        ), "developer instruction not trailing the payload"
        assert needle not in out[0]["content"], "instruction leaked into the frozen prefix"

    # The explicit instructions argument rides the same trailing path.
    out3 = ac.repack_messages(
        _fat_history("goal E", "{}"),
        user_text="goal E",
        traces=[],
        provider="deepseek",
        session_id=SID,
        instructions="NEW INSTRUCTION v3: cap rounds at 6",
    )
    assert out3[-1] == {"role": "developer", "content": "NEW INSTRUCTION v3: cap rounds at 6"}
    assert out3[0]["content"].split(EVOLVING_TAIL_MARKER)[0] == prefix1, (
        "explicit-instruction repack moved the prefix"
    )
    print("PASS test_new_instructions_ride_as_trailing_developer_messages")


if __name__ == "__main__":
    test_two_consecutive_repack_outputs_share_prefix_hash()
    test_freeze_returns_identical_bytes_despite_input_drift()
    test_refreeze_starts_new_prefix()
    test_tool_schemas_hash_covers_bytes()
    test_evolving_tail_stays_small_and_marks_itself()
    test_new_instructions_ride_as_trailing_developer_messages()
    print("ALL test_context_freeze PASS")
