"""Brute search opening prefix for desk chess line."""
from __future__ import annotations

import chess

TAIL = [
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

# Dialogue-derived Ruy Lopez skeleton ending 9... Nxe4, 10. O-O
PREFIXES = [
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "O-O", "Nbd2", "d6", "h3", "Nxe4", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "d6", "Nbd2", "O-O", "h3", "Nxe4", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Bb7", "d3", "d6", "Nbd2", "O-O", "h3", "Nxe4", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "Nbd2", "O-O", "d3", "d6", "Re1", "Nxe4", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "O-O", "h3", "Nxe4", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Nxe4", "Re1", "Nf6"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Nxe4", "d4", "b5", "Bb3", "d5", "dxe5", "Be6", "Nbd2", "Nc5", "c3", "Nf6"],
]


def replay(moves: list[str]) -> tuple[bool, chess.Board | None, str]:
    board = chess.Board()
    for m in moves:
        try:
            mv = board.parse_san(m)
        except Exception as exc:
            return False, board, f"parse {m!r}: {exc}"
        if mv not in board.legal_moves:
            return False, board, f"illegal {m!r} at ply {board.fullmove_number}"
        board.push(mv)
    return True, board, "ok"


def main() -> None:
    for i, prefix in enumerate(PREFIXES):
        ok, _, err = replay(prefix + TAIL)
        print(f"{i}: {err}" if not ok else f"{i}: OK ({len(prefix)+len(TAIL)} plies)")
        if ok:
            _, board, _ = replay(prefix + TAIL)
            assert board
            print("  prefix:", " ".join(prefix))
            print("  FEN:", board.fen())


if __name__ == "__main__":
    main()
