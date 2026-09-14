"""Find legal opening + full canonical tail."""
from __future__ import annotations

import chess

FULL_TAIL = [
    "Nf6",
    "Re1",
    "d5",
    "exd5",
    "Qxd1+",
    "Rxd1",
    "Kd8",
    "Bf4",
    "Be6",
    "Bxc7",
    "Bxc7",
    "O-O",
    "Kc8",
    "Bxc7",
    "Kxc7",
    "Rxd1",
    "Rxd1+",
    "Kxd1",
    "Nf6",
    "Bf4",
    "Ke7",
    "O-O",
    "Rd8",
    "Rxd8+",
    "Kxd8",
    "Rd1+",
    "Ke7",
    "Bf4",
]

# Openings to try — Ruy Lopez variants keeping e4 pawn for exd5
CANDIDATES = [
    # Delayed Nxe4: knight retreats from e4 before d5
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "Ne5", "Nxe5", "Bxe5", "O-O", "d6", "Bxc6", "bxc6", "O-O"],
    # No Nxe4 — classical c3 Ruy
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "O-O", "c3", "d6", "h3", "Nb8", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "O-O", "h3", "Re8", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "O-O", "Nbd2", "d6", "O-O", "Nb8", "Re1"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "O-O", "Nbd2", "d6", "O-O", "Nb8", "Re1", "Nbd7"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "O-O", "Nbd2", "d6", "O-O", "Re8", "Re1", "Nb8"],
    # Marshall-style d5 break
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "O-O", "c3", "d5"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Nxe4", "Re1", "Nf6"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Nxe4", "d4", "Nf6", "Re1", "b5", "Bb3", "Be7", "c3", "O-O", "O-O"],
]


def replay(moves: list[str]) -> tuple[bool, chess.Board | None, str, int]:
    board = chess.Board()
    for i, m in enumerate(moves):
        try:
            mv = board.parse_san(m)
        except Exception as exc:
            return False, board, f"{i+1}:{m!r} parse {exc}", i
        if mv not in board.legal_moves:
            return False, board, f"{i+1}:{m!r} illegal (fen={board.fen()})", i
        board.push(mv)
    return True, board, "ok", len(moves)


def main() -> None:
    for i, prefix in enumerate(CANDIDATES):
        ok, _, err, _ = replay(prefix + FULL_TAIL)
        if ok:
            _, board, _, _ = replay(prefix + FULL_TAIL)
            print(f"=== WINNER {i} ===")
            print("OPENING:", " ".join(prefix))
            print("FULL:", len(prefix) + len(FULL_TAIL), "plies")
            print("FEN:", board.fen() if board else "?")
            return
        print(f"{i}: fail at {err}")
    print("none found")


if __name__ == "__main__":
    main()
