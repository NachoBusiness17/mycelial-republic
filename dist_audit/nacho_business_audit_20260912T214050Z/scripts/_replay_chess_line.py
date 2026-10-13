"""One-off: derive and validate desk chess line."""
from __future__ import annotations

import chess

MOVES_10_24 = [
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

OPENING_CANDIDATES = [
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Nxe4", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "O-O", "Nbd2", "d6", "h3", "Nxe4", "O-O"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Nxe4", "d4", "b5", "Bb3", "d5", "dxe5", "Be6", "Nbd2", "Nc5", "c3", "Nf6"],
    ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "O-O", "h3", "Nxe4", "Nxe4"],
    ["e4", "e5", "Nf3", "Nc6", "Nc3", "Nf6", "Bb5", "a6", "Ba4", "Be7", "O-O", "O-O", "Re1", "b5", "Bb3", "d6", "c3", "Nxe4", "Nxe4"],
]


def try_line(opening: list[str], tail: list[str]) -> tuple[bool, list[str], chess.Board | None]:
    board = chess.Board()
    applied: list[str] = []
    for m in opening + tail:
        try:
            mv = board.parse_san(m)
        except Exception as exc:
            return False, applied, None if not applied else board
        if mv not in board.legal_moves:
            print(f"  fail {m!r} ply={len(applied)+1} after {applied[-4:]}")
            return False, applied, board
        board.push(mv)
        applied.append(m)
    return True, applied, board


def main() -> None:
    for i, opening in enumerate(OPENING_CANDIDATES):
        ok, applied, board = try_line(opening, MOVES_10_24)
        print(f"candidate {i}: ok={ok} moves={len(applied)}")
        if ok and board:
            print("  opening:", " ".join(opening))
            print("  FEN:", board.fen())
            print("  turn:", "black" if board.turn == chess.BLACK else "white")


if __name__ == "__main__":
    main()
