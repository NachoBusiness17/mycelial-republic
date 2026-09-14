"""Find any legal line matching tail from Qxd1+."""
from __future__ import annotations

import chess
from collections import deque

TAIL = [
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

# prefix ending with Re1 d5 exd5
PREFIX_END = ["Re1", "d5", "exd5"]


def main() -> None:
    q: deque[tuple[list[str], chess.Board]] = deque()
    q.append(([], chess.Board()))
    seen: set[str] = set()
    while q:
        moves, board = q.popleft()
        if len(moves) > 22:
            continue
        key = board.fen()
        if key in seen:
            continue
        seen.add(key)
        if len(moves) >= len(PREFIX_END):
            if moves[-3:] == PREFIX_END:
                ok = True
                b2 = board.copy()
                for m in TAIL:
                    try:
                        mv = b2.parse_san(m)
                    except Exception:
                        ok = False
                        break
                    if mv not in b2.legal_moves:
                        ok = False
                        break
                    b2.push(mv)
                if ok:
                    print("FOUND prefix len", len(moves))
                    print(" ".join(moves))
                    print("FEN", b2.fen())
                    return
        if len(moves) >= 22:
            continue
        for mv in list(board.legal_moves):
            san = board.san(mv)
            if len(moves) < 8:
                if san not in {
                    "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3",
                    "Be7", "d3", "O-O", "Nbd2", "d6", "h3", "Ne8", "Re1", "Qe2", "Be3", "Nxe4",
                }:
                    continue
            b2 = board.copy()
            b2.push(mv)
            q.append((moves + [san], b2))
    print("not found")


if __name__ == "__main__":
    main()
