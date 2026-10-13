"""Find legal full line closest to desk canonical."""
from __future__ import annotations

import chess
import itertools

OPENING = [
    "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7",
    "O-O", "O-O", "h3", "Ne8", "Nbd2", "d6",
]

MID_OPTIONS = [
    ["Nf6", "Re1", "d5", "Nxd5", "Qxd1+", "Rxd1"],
    ["Nf6", "Re1", "Qxd1+", "Rxd1"],
    ["Nf6", "Re1", "d5", "Re1", "Qxd1+", "Rxd1"],  # bad
    ["Nf6", "Re1", "Be6", "Qxd1+", "Rxd1"],
    ["Nf6", "Re1", "d5", "c4", "Qxd1+", "Rxd1"],
]

TAIL = [
    "Kd8", "Bf4", "Be6", "Bxc7", "Bxc7", "Re2", "Kc8", "Bxc7", "Kxc7",
    "Rxd1", "Rxd1+", "Kxd1", "Nf6", "Bf4", "Ke7", "Re1", "Rd8", "Rxd8+",
    "Kxd8", "Rd1+", "Ke7", "Bf4",
]


def replay(moves: list[str]) -> tuple[bool, chess.Board | None, str]:
    b = chess.Board()
    for m in moves:
        try:
            mv = b.parse_san(m)
        except Exception as exc:
            return False, b, f"{m!r}: {exc}"
        if mv not in b.legal_moves:
            return False, b, f"illegal {m!r}"
        b.push(mv)
    return True, b, "ok"


def main() -> None:
    for i, mid in enumerate(MID_OPTIONS):
        ok, board, err = replay(OPENING + mid + TAIL)
        print(i, err if not ok else f"OK {board.fen() if board else ''}")


if __name__ == "__main__":
    main()
