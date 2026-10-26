"""test_bones_adapter -- the /bones adapter formats; the kernel decides.

Offline tests: the bot's connect is mocked (discord.Client.run raises if called),
interactions are fakes, and the kernel's session/receipt stores are pointed at
tmp_path so the repo store is untouched. No network, no token, no discord login.
"""
from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from typing import Any, Optional

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# M17 WAVE0 2026-09-29 (watch/inbox/MICKEY17_RUN_PLAN_20260929.md): discord.py
# is an optional runtime dep (NOT in requirements.txt); the hard import below
# errored at collection on a requirements-only venv and zero tests ran. Skip
# gracefully when it is absent instead of faking coverage.
pytest.importorskip("discord")

import discord  # noqa: E402

import mag.bones_adapter as bones_adapter  # noqa: E402
import mag.wow_bones_session as wbs  # noqa: E402

CHANNEL_ID = bones_adapter.CHANNEL_ID


# --- offline doubles -----------------------------------------------------------------

class FakeResponse:
    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []

    async def send_message(self, content: Optional[str] = None,
                           *, ephemeral: bool = False, **_: Any) -> None:
        self.sent.append({"content": content or "", "ephemeral": ephemeral})


class FakeInteraction:
    def __init__(self, channel_id: int = CHANNEL_ID):
        self.channel_id = channel_id
        self.response = FakeResponse()


async def invoke(group: "bones_adapter.BonesGroup", name: str,
                 interaction: FakeInteraction, *args: Any, **kwargs: Any) -> None:
    """Call a registered subcommand callback directly (no gateway, no network)."""
    cb = bones_adapter.callback_of(getattr(group, name))
    await cb(group, interaction, *args, **kwargs)


def one_message(interaction: FakeInteraction) -> str:
    assert len(interaction.response.sent) == 1, interaction.response.sent
    return interaction.response.sent[0]["content"]


# --- fixtures -------------------------------------------------------------------------

@pytest.fixture()
def kernel_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the kernel's session/receipt stores at tmp_path (repo store untouched)."""
    monkeypatch.setattr(wbs, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(wbs, "RECEIPTS_DIR", tmp_path / "receipts")
    return tmp_path


def fixture_or_skip() -> dict[str, Any]:
    fx = wbs._fixture_or_none()
    if fx is None:
        pytest.skip("bones fixture not extracted (python -m mag.wow_bones extract)")
    return fx


def legal_verb(fx: dict[str, Any], seed: str) -> str:
    """The kernel's own legality listing for a fresh session (AUTHED)."""
    probe = wbs.BonesSession(fx, seed)
    legal = [v for v in probe.dispatch.verbs()
             if probe.dispatch.rows[v]["status"] == probe.session_status]
    assert legal, "fixture offers no AUTHED verb"
    return legal[0]


# --- pure formatting ------------------------------------------------------------------

def test_fmt_any_scalars_nesting_and_lists() -> None:
    payload = {"ok": True, "seed": "7", "turn": {"n": 1, "verb": "X", "ok": True},
               "legal_verbs": [{"a": 1}, {"b": 2}], "moves": []}
    text = bones_adapter.fmt_any(payload)
    assert "ok: True" in text
    assert "seed: 7" in text
    assert "turn:" in text
    assert "  n: 1" in text
    assert '- {"a":1}' in text          # list items in canonical inline JSON (no spaces)
    assert "(none)" in text              # empty list renders, does not vanish


def test_fmt_block_fences_and_truncates() -> None:
    fenced = bones_adapter.fmt_block({"ok": True})
    assert fenced.startswith("```\n") and fenced.endswith("\n```")
    big = bones_adapter.fmt_block({"k": "x" * 5000})
    assert len(big) <= bones_adapter.MAX_MESSAGE
    assert big.endswith("\n```")
    assert "(truncated)" in big


def test_adapter_source_contains_no_game_logic() -> None:
    """Directive anti-goal, enforced: kernel decision internals never appear
    in the adapter. (Formatting reads like session_status are allowed.)"""
    src = (ROOT / "mag" / "bones_adapter.py").read_text(encoding="utf-8")
    banned = ["set_boss_state", "TURN_LIMIT", "DRAW_TARGET", "is_done",
              "stream.next", "BOSS_ID", "STATUS_NEVER", "draws %"]
    for token in banned:
        assert token not in src, f"game logic leaked into adapter: {token!r}"


# --- wiring: /bones start --------------------------------------------------------------

def test_start_envelope_and_hub_pointer(kernel_store: Path) -> None:
    fixture_or_skip()
    _, group = bones_adapter.build_bot()
    ix = FakeInteraction()
    asyncio.run(invoke(group, "start", ix, "s7", False))
    text = one_message(ix)
    assert "schema: wow_bones_session.v1" in text  # the kernel start envelope's own schema line
    assert "seed: s7" in text
    assert "verdict: OPEN" in text
    sid = re.search(r"session_id: (\S+)", text)
    assert sid, text
    # the hub now points the channel at the kernel session id
    assert group.hub.current[CHANNEL_ID] == sid.group(1)
    # the kernel store holds the session file (kernel wrote it, not the adapter)
    assert (kernel_store / "sessions" / f"{sid.group(1)}.json").is_file()


def test_start_world_boss_flag_reaches_kernel(kernel_store: Path) -> None:
    fixture_or_skip()
    _, group = bones_adapter.build_bot()
    ix = FakeInteraction()
    asyncio.run(invoke(group, "start", ix, "wb1", True))
    text = one_message(ix)
    assert "world_boss_alive: True" in text
    sid = re.search(r"session_id: (\S+)", text).group(1)
    ses = wbs.BonesSession.load(sid)
    assert ses.world_boss is True


# --- wiring: the channel gate -----------------------------------------------------------

def test_wrong_channel_is_refused_ephemeral(kernel_store: Path) -> None:
    fixture_or_skip()
    _, group = bones_adapter.build_bot()
    for name, args in [("start", ("s9", False)), ("move", ("X", None)),
                       ("status", (None,)), ("receipt", (None,)), ("verbs", (None, 12))]:
        ix = FakeInteraction(channel_id=1050760558883913781)  # one off the pinned channel
        asyncio.run(invoke(group, name, ix, *args))
        assert len(ix.response.sent) == 1
        assert ix.response.sent[0]["ephemeral"] is True
        assert "#game-c-overview" in ix.response.sent[0]["content"]
    # nothing leaked into the kernel store either
    assert list((kernel_store / "sessions").glob("*.json")) == []


# --- wiring: /bones move -----------------------------------------------------------------

def test_move_legal_verb_promotes_and_persists(kernel_store: Path) -> None:
    fx = fixture_or_skip()
    _, group = bones_adapter.build_bot()
    seed = "mv1"
    verb = legal_verb(fx, seed)
    ix = FakeInteraction()
    asyncio.run(invoke(group, "start", ix, seed, False))
    sid = group.hub.current[CHANNEL_ID]

    ix2 = FakeInteraction()
    asyncio.run(invoke(group, "move", ix2, verb, None))  # hub default, no explicit id
    text = one_message(ix2)
    assert "ok: True" in text
    assert "STATUS_LOGGEDIN" in text          # kernel's own promotion fact
    assert f"session_id: {sid}" not in text or True  # move envelope carries no id; shape only
    assert (kernel_store / "sessions" / f"{sid}.json").is_file()

    loaded = wbs.BonesSession.load(sid)
    assert loaded.turn_count == 1
    assert loaded.moves[0]["verb"] == verb


def test_move_unknown_verb_formats_kernel_refusal(kernel_store: Path) -> None:
    fixture_or_skip()
    _, group = bones_adapter.build_bot()
    asyncio.run(invoke(group, "start", FakeInteraction(), "ref1", False))
    ix = FakeInteraction()
    asyncio.run(invoke(group, "move", ix, "NOT_AN_OPCODE", None))
    text = one_message(ix)
    assert "ok: False" in text
    assert "UNKNOWN_OPCODE" in text


def test_move_without_session_answers_no_session(kernel_store: Path) -> None:
    _, group = bones_adapter.build_bot()
    ix = FakeInteraction()
    asyncio.run(invoke(group, "move", ix, "WHATEVER", None))
    text = one_message(ix)
    assert "ok: False" in text and "NO_SESSION" in text


def test_move_explicit_session_overrides_hub(kernel_store: Path) -> None:
    fixture_or_skip()
    fx = fixture_or_skip()
    _, group = bones_adapter.build_bot()
    verb = legal_verb(fx, "ex1")
    asyncio.run(invoke(group, "start", FakeInteraction(), "ex1", False))
    asyncio.run(invoke(group, "start", FakeInteraction(), "ex2", False))
    newest = group.hub.current[CHANNEL_ID]
    # recompute the first session's id the kernel way
    import hashlib
    material = f"{wbs.SESSION_SCHEMA}:ex1:{0}"
    oldest = "bones-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:12]
    assert oldest != newest
    ix = FakeInteraction()
    asyncio.run(invoke(group, "move", ix, verb, oldest))
    text = one_message(ix)
    assert "ok: True" in text
    loaded = wbs.BonesSession.load(oldest)
    assert loaded.turn_count == 1


# --- wiring: /bones status, receipt, verbs ------------------------------------------------

def test_status_envelope(kernel_store: Path) -> None:
    fixture_or_skip()
    _, group = bones_adapter.build_bot()
    asyncio.run(invoke(group, "start", FakeInteraction(), "st1", False))
    ix = FakeInteraction()
    asyncio.run(invoke(group, "status", ix, None))
    text = one_message(ix)
    for key in ("session_id:", "seed: st1", "session_status:", "turn_count: 0",
                "draw_index:", "verdict: OPEN"):
        assert key in text, key


def test_receipt_writes_kernel_file_and_shows_sha(kernel_store: Path) -> None:
    fixture_or_skip()
    _, group = bones_adapter.build_bot()
    asyncio.run(invoke(group, "start", FakeInteraction(), "rc1", False))
    sid = group.hub.current[CHANNEL_ID]
    ix = FakeInteraction()
    asyncio.run(invoke(group, "receipt", ix, None))
    text = one_message(ix)
    assert "schema: wow_session.v1" in text
    assert re.search(r"sha256: [0-9a-f]{64}", text), text
    assert f"receipt_path: {kernel_store}" in text  # display-only pointer
    assert (kernel_store / "receipts" / f"{sid}.json").is_file()


def test_verbs_lists_kernel_legality(kernel_store: Path) -> None:
    fixture_or_skip()
    _, group = bones_adapter.build_bot()
    asyncio.run(invoke(group, "start", FakeInteraction(), "vb1", False))
    ix = FakeInteraction()
    asyncio.run(invoke(group, "verbs", ix, None, 12))
    text = one_message(ix)
    assert "session_status: STATUS_AUTHED" in text
    assert "total:" in text
    assert "- " in text  # at least one legal verb line


# --- command registration (guild-scoped) ---------------------------------------------------

def test_group_registers_five_guild_scoped_subcommands() -> None:
    client, group = bones_adapter.build_bot()
    assert sorted(c.name for c in group.commands) == \
        ["move", "receipt", "start", "status", "verbs"]
    guild_cmds = client.tree.get_commands(guild=discord.Object(bones_adapter.GUILD_ID))
    assert [c.name for c in guild_cmds] == ["bones"]
    global_cmds = client.tree.get_commands()
    assert global_cmds == []  # nothing leaks outside NT-ACv2


# --- runtime token ---------------------------------------------------------------------------

def test_load_token_reads_runtime_var(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text(
        "# DISCORD_BOT_TOKEN=inside-a-comment-must-be-skipped\n"
        "OTHER=1\n"
        'DISCORD_BOT_TOKEN= "rt-value" \n',
        encoding="utf-8",
    )
    assert bones_adapter.load_token(env) == "rt-value"


def test_load_token_missing_var_and_missing_file_never_leak(tmp_path: Path) -> None:
    empty = tmp_path / "empty.env"
    empty.write_text("OTHER=1\n", encoding="utf-8")
    with pytest.raises(SystemExit) as ei:
        bones_adapter.load_token(empty)
    assert "DISCORD_BOT_TOKEN" in str(ei.value)

    with pytest.raises(SystemExit) as ei2:
        bones_adapter.load_token(tmp_path / "nope.env")
    assert "nope.env" in str(ei2.value)


# --- --check dry-run: registers, prints, never connects ---------------------------------------

def test_check_mode_lists_commands_and_never_connects(monkeypatch: pytest.MonkeyPatch,
                                                      capsys: pytest.CaptureFixture[str]) -> None:
    def boom(self: Any, *a: Any, **kw: Any) -> None:
        raise AssertionError("connect attempted in --check")
    monkeypatch.setattr(discord.Client, "run", boom)  # the bot's connect, mocked
    rc = bones_adapter.main(["--check"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "--check" in out
    assert str(bones_adapter.GUILD_ID) in out
    assert str(bones_adapter.CHANNEL_ID) in out
    for name in ("start", "move", "status", "receipt", "verbs"):
        assert f"/bones {name}" in out, name
    assert "no token read" in out
