"""Brute search for legal prefix ending before queen trade."""
from __future__ import annotations

import chess

# suffix starting at 13. Rxd1 (after queen trade)
SUFFIX = [
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

# queen trade pair
TRADE = ["Re1", "d5", "exd5", "Qxd1+"]


def replay(moves: list[str]) -> tuple[bool, chess.Board | None, str]:
    board = chess.Board()
    for m in moves:
        try:
            mv = board.parse_san(m)
        except Exception as exc:
            return False, board, f"{m!r}: {exc}"
        if mv not in board.legal_moves:
            return False, board, f"illegal {m!r} fen={board.fen()}"
        board.push(mv)
    return True, board, "ok"


def main() -> None:
    prefixes = [
        ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "O-O", "Nbd2", "d6", "h3", "Ne8", "O-O", "Nf6"],
        ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Be7", "Re1", "b5", "Bb3", "O-O", "c3", "d6", "h3", "Nb8", "Nbd2", "Nbd7"],
    ]
    for i, pre in enumerate(prefixes):
        ok, _, err = replay(pre + TRADE + SUFFIX)
        print(i, "trade path:", err if not ok else "OK")
        if ok:
            _, b, _ = replay(pre + TRADE + SUFFIX)
            print("FEN", b.fen() if b else "?")


if __name__ == "__main__":
    main()
