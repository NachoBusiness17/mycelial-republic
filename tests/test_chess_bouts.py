"""The pre-training kill test: golden-vector pinning + 10 self-play chess
bouts on agent_arena's slot, python-chess as the legality referee, NO training.

Register: watch/inbox/ractor_engine/2026-10-06-stockfish-coding/accuracy.md:35
kill criterion 1 ("the oracle on the encoded slice is not deterministic across
10 reruns of a fixed bout seed ... kills the silent-expert premise"), fired by
break-accuracy.md:51 (A5: fold the golden-vector pattern into the encoding
card as the determinism gate) and SYNTHESIS.md:47+55 (determinism gate =
golden-vector pinning, the dungeon's refusal-to-run pattern,
tools/dungeon.py:12-13 and :137-145).

The card that owns this gate:
watch/inbox/ractor_engine/2026-10-07-stockfish-door/ENCODING_CARD_S2.md

Design (one breath): the actors are deterministic dice-law policies (sha256
preimage -> legal-move index, the dungeon's dice law shape), so "self-play"
means two deterministic instruments play 10 chess bouts through agent_arena's
real surface (new_game + apply_move + _parse_move referee). The bout ledger
verdict oracle is a pure function of the fixed bout seed; the kill test is
whether it STAYS pure across 10 reruns of the whole battery through the real
state-file IO path. All 10 run digests equal: the silent-expert premise LIVES.
Any divergence: the battery is flaky and the door KILLS. Whichever verdict is
true is what gets banked (memory/runs/selfplay/s8_bout_battery_verdict_20261007.json).

Isolation law (named in the card): the battery points agent_arena's and
arena_learning's write surfaces (STATE_PATH, TRAIL, PROFILES_PATH,
LEAGUE_PATH) at a run-scoped temp dir per battery run, so the live arena game
(memory/working/agent_arena.json) and the live league files
(memory/training/arena_*.json*) are never touched. The code path exercised is
byte-for-byte agent_arena's referee path; only the landing spots are isolated.

Usage:
  .venv/Scripts/python.exe -m pytest -q tests/test_chess_bouts.py
  .venv/Scripts/python.exe tests/test_chess_bouts.py --bank   # bank the receipt
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import chess  # noqa: E402  (python-chess 1.11.2, verified in-venv)

from mag import agent_arena as aa  # noqa: E402
from mag import arena_learning as al  # noqa: E402

# --- the fixed bout seed and the golden pin table (the determinism gate) ---

TIP = hashlib.sha256(b"stockfish-door-20261007 move-8 kill test").hexdigest()

GOLDEN_PREIMAGES = ((TIP, 0, 1, "white"), (TIP, 4, 7, "black"), (TIP, 9, 13, "white"))


def roll(pre: str) -> int:
    """Dungeon dice law verbatim in shape: tools/dungeon.py:133-134."""
    return int(hashlib.sha256(pre.encode("utf-8")).hexdigest()[:8], 16) % 20 + 1


def check_golden() -> dict[str, int]:
    """tools/dungeon.py:137-145 pattern: the pinned preimages, computed."""
    pins: dict[str, int] = {}
    for tip, bout, ply, seat in GOLDEN_PREIMAGES:
        pre = f"{tip}:{bout}:{ply}:{seat}"
        pins[pre] = roll(pre)
    return pins


# Frozen 2026-10-07 by lane s8-golden-bouts (probe output banked in the card):
# d0707ab1...51b9:0:1:white -> 1, :4:7:black -> 20, :9:13:white -> 10
GOLDEN_FROZEN = {
    f"{TIP}:0:1:white": 1,
    f"{TIP}:4:7:black": 20,
    f"{TIP}:9:13:white": 10,
}


def golden_gate() -> dict[str, int]:
    """Refusal to run: pins must reproduce or the battery refuses
    (the dungeon's startup gate, tools/dungeon.py:12-13)."""
    pins = check_golden()
    for pre, want in GOLDEN_FROZEN.items():
        got = pins.get(pre)
        if got != want:
            raise RuntimeError(
                f"golden vectors failed to reproduce ({pre} -> {got}, frozen {want}); "
                "the dice law moved under the battery: refusing to run"
            )
    return pins


# --- the deterministic self-play actors and the bout runner ---

N_BOUTS = 10
N_RERUNS = 10
PLY_CAP = 100
WHITE_SEAT = "s8-white"
BLACK_SEAT = "s8-black"


def seat_pick(legal_san: list[str], bout: int, ply: int, seat_role: str) -> str:
    """Dice-law seat policy: sha256 preimage -> legal-move index.
    Pure function of (seed, bout, ply, seat) and the legal-move list."""
    pre = f"{TIP}:{bout}:{ply}:{seat_role}"
    h = int(hashlib.sha256(pre.encode("utf-8")).hexdigest()[:16], 16)
    return legal_san[h % len(legal_san)]


def isolate(workdir: Path) -> None:
    """Point the four live write surfaces at run-scoped files (card: Isolation law)."""
    aa.STATE_PATH = workdir / "agent_arena_state.json"
    al.TRAIL = workdir / "arena_learning_trail.jsonl"
    al.PROFILES_PATH = workdir / "arena_profiles.jsonl"
    al.LEAGUE_PATH = workdir / "arena_league.json"
    # Perf-only memoize, verdict-neutral: mag/arena_strategies.py:13-21 reloads the
    # static configs/arena_strategies.yaml on every strategy lookup (cProfile on one
    # bout: 706 yaml.safe_load calls, 21.4s of 28.3s profiled), the battery's hot
    # spot at ~6s per 100-ply bout. The file is fixed for the life of the process,
    # so the cached dict is the same bytes; the referee path (apply_move legality)
    # never consults it for verdicts.
    import mag.arena_strategies as strategies

    cached = getattr(strategies, "_s8_memoized", None)
    if cached is None:
        cached = strategies._load()
        strategies._s8_memoized = cached
    strategies._load = lambda: cached


def run_bout(bout: int, workdir: Path) -> dict:
    """One self-play chess bout on agent_arena's slot. python-chess is the
    referee inside apply_move; the drivers only choose among legal moves."""
    st = aa.new_game(game="chess", white=WHITE_SEAT, black=BLACK_SEAT)
    if not st.get("ok"):
        raise RuntimeError(f"bout {bout}: new_game refused: {st.get('error')}")
    san_ledger: list[str] = []
    illegal = 0
    final: dict = {}
    role_of = {WHITE_SEAT: "white", BLACK_SEAT: "black"}
    for ply in range(PLY_CAP):
        snap = aa.status()
        if snap.get("status") != "ongoing":
            final = snap
            break
        board = chess.Board(snap["fen"])
        legal_san = [board.san(m) for m in board.legal_moves]
        if not legal_san:
            final = snap
            break
        seat = snap["turn_seat"]
        pick = seat_pick(legal_san, bout, ply, role_of.get(seat, seat))
        res = aa.apply_move(pick, seat=seat)
        if not res.get("ok"):
            # the referee rejected a pick drawn from the legal list: that is
            # a surface defect, banked in the bout row, never retried away
            illegal += 1
            final = snap | {"status": "referee_rejection", "rejected_pick": pick}
            break
        san_ledger.append(res["applied"])
        final = res
    else:
        fin = aa.status()
        if fin.get("status") == "ongoing":
            fin = dict(fin) | {"status": "ply_cap"}
        final = fin
    digest = hashlib.sha256(";".join(san_ledger).encode("utf-8")).hexdigest()
    return {
        "bout": bout,
        "status": final.get("status"),
        "winner": final.get("winner"),
        "plies": len(san_ledger),
        "ply_cap": PLY_CAP,
        "final_fen": final.get("fen"),
        "illegal_attempts": illegal,
        "ledger_sha256": digest,
    }


def battery_run(workdir: Path | None = None) -> dict:
    """One battery: golden gate + N_BOUTS bouts + the run digest.
    The run digest is the ledger verdict oracle's output for one rerun.
    Isolation is INSIDE this function (every caller gets it): the first
    suite draft let TestBouts/TestKill pass a raw temp dir without calling
    isolate(), so 11 batteries wrote the LIVE surfaces (agent_arena.json
    clobbered, 11,000 s8 test rows appended to arena_profiles.jsonl); cured
    2026-10-07 same sitting, evidence in the receipt erratum."""
    if workdir is None:
        tmp = fresh_workdir()
        try:
            return battery_run(tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    pins = golden_gate()
    bouts = [run_bout(b, workdir) for b in range(N_BOUTS)]
    payload = json.dumps(bouts, sort_keys=True, ensure_ascii=False)
    return {
        "pins": pins,
        "bouts": bouts,
        "run_digest": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }


def fresh_workdir() -> Path:
    d = Path(tempfile.mkdtemp(prefix="s8_bouts_"))
    isolate(d)
    return d


# --- the kill test and the gate, as pytest ---


class TestGoldenGate:
    def test_golden_vectors_reproduce(self):
        """The determinism gate itself: the frozen pin table must reproduce
        from the dice law before any bout runs (dungeon refusal-to-run)."""
        assert check_golden() == GOLDEN_FROZEN

    def test_tip_is_the_pinned_seed(self):
        assert TIP == "d0707ab1dbe2745f93841869fdaf7c37b69a3260f901ee582ab1ebbb8b2851b9"

    def test_seat_pick_is_pure(self):
        legal = ["e4", "d4", "Nf3", "c4"]
        a = seat_pick(legal, 3, 5, "white")
        b = seat_pick(legal, 3, 5, "white")
        assert a == b and a in legal


class TestBouts:
    def test_10_selfplay_bouts_referee_clean(self):
        """10 self-play bouts through agent_arena's real surface. The referee
        verdict: every pick drawn from the legal list must apply clean
        (illegal_attempts == 0 across all bouts); every bout lands a
        deterministic ledger verdict row."""
        run = battery_run()
        bouts = run["bouts"]
        assert len(bouts) == N_BOUTS
        assert all(b["illegal_attempts"] == 0 for b in bouts), bouts
        assert all(b["plies"] > 0 for b in bouts), bouts
        assert all(b["final_fen"] for b in bouts), bouts
        assert len({b["ledger_sha256"] for b in bouts}) == N_BOUTS


class TestKill:
    def test_determinism_across_10_reruns_of_fixed_bout_seed(self):
        """THE pre-training kill test (accuracy.md:35 criterion 1): 10 reruns
        of the whole battery on the fixed bout seed must land 10 equal run
        digests. All equal: silent-expert premise LIVES. Any divergence: the
        battery is flaky, the oracle is not a silent expert, the door KILLS.
        A red here is the kill verdict banked, not a flaky test to skip."""
        digests = []
        for _ in range(N_RERUNS):
            run = battery_run()
            digests.append(run["run_digest"])
        assert len(set(digests)) == 1, (
            "KILL VERDICT: the ledger verdict oracle is not deterministic "
            f"across {N_RERUNS} reruns of the fixed bout seed; digests {digests}"
        )


# --- banking mode: run the battery, bank the true verdict ---


def bank() -> dict:
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digests = []
    first_run = None
    for i in range(N_RERUNS):
        run = battery_run()
        digests.append(run["run_digest"])
        if i == 0:
            first_run = run
    all_equal = len(set(digests)) == 1
    verdict = "DETERMINISM_LIVES" if all_equal else "KILLED_FLAKY"
    receipt = {
        "receipt_class": "S2 bout-battery verdict (move 8, the pre-training kill test)",
        "run": "stockfish-door-20261007",
        "lane": "s8-golden-bouts",
        "writer": "tests/test_chess_bouts.py bank()",
        "command": ".venv/Scripts/python.exe tests/test_chess_bouts.py --bank",
        "created_at": started,
        "verdict": verdict,
        "decider": "10-rerun determinism of the ledger verdict oracle on the fixed bout seed (accuracy.md:35 criterion 1)",
        "n_bouts": N_BOUTS,
        "n_reruns": N_RERUNS,
        "ply_cap": PLY_CAP,
        "bout_seed_tip": TIP,
        "golden_frozen": {k.split(TIP)[1]: v for k, v in GOLDEN_FROZEN.items()},
        "run_digests": digests,
        "all_digests_equal": all_equal,
        "banking_run_bouts": first_run["bouts"],
        "referee": {
            "python_chess_version": chess.__version__,
            "surface": "mag/agent_arena.py new_game + apply_move (_parse_move referee, :81-105, :210-233)",
            "illegal_attempts_total": sum(b["illegal_attempts"] for b in first_run["bouts"]),
        },
        "training": "none: no model load, no network, no API call; actors are deterministic sha256 dice-law policies",
        "isolation": "run-scoped temp dirs for STATE_PATH/TRAIL/PROFILES_PATH/LEAGUE_PATH per battery run; live arena game and league files untouched (card: Isolation law)",
        "card": "watch/inbox/ractor_engine/2026-10-07-stockfish-door/ENCODING_CARD_S2.md",
        "register": [
            "watch/inbox/ractor_engine/2026-10-06-stockfish-coding/accuracy.md:35",
            "watch/inbox/ractor_engine/2026-10-06-stockfish-coding/break-accuracy.md:51",
            "watch/inbox/ractor_engine/2026-10-06-stockfish-coding/SYNTHESIS.md:47",
        ],
    }
    out_dir = ROOT / "memory" / "runs" / "selfplay"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "s8_bout_battery_verdict_20261007.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (out_dir / "s8_bout_ledger_20261007.jsonl").open("w", encoding="utf-8") as fh:
        for row in first_run["bouts"]:
            fh.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"verdict={verdict} digests={len(set(digests))} unique of {N_RERUNS} reruns")
    print(f"banked: {out_dir / 's8_bout_battery_verdict_20261007.json'}")
    return receipt


if __name__ == "__main__":
    if "--bank" in sys.argv:
        bank()
    else:
        print("pass --bank to run the battery and bank the receipt")
