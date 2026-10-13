"""Find legal prefix ending at 13. Rxd1 then replay tail."""
from __future__ import annotations

import chess
from collections import deque

TAIL_FROM_13 = [
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

TRADE = ["Qxd1+"]  # black move before Rxd1


def replay(moves: list[str]) -> tuple[bool, chess.Board | None]:
    b = chess.Board()
    for m in moves:
        mv = b.parse_san(m)
        if mv not in b.legal_moves:
            return False, b
        b.push(mv)
    return True, b


def main() -> None:
    q: deque[tuple[list[str], chess.Board]] = deque()
    q.append(([], chess.Board()))
    seen: set[str] = set()
    while q:
        moves, board = q.popleft()
        if len(moves) > 24:
            continue
        key = board.fen()
        if key in seen:
            continue
        seen.add(key)
        if board.turn == chess.BLACK and len(moves) >= 8:
            for mv in board.legal_moves:
                if board.san(mv) != "Qxd1+":
                    continue
                pre = moves + ["Qxd1+"]
                ok, _ = replay(pre + TAIL_FROM_13)
                if ok:
                    _, final = replay(pre + TAIL_FROM_13)
                    print("FOUND at ply", len(pre))
                    print(" ".join(pre + TAIL_FROM_13))
                    print("FEN", final.fen() if final else "?")
                    return
        if len(moves) >= 24:
            continue
        for mv in list(board.legal_moves)[:35]:
            san = board.san(mv)
            if len(moves) < 10 and san not in {
                "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3",
                "Be7", "d3", "O-O", "Re1", "Ne8", "Nxe4", "h3", "d6", "exd5", "d5",
            }:
                continue
            b2 = board.copy()
            b2.push(mv)
            q.append((moves + [san], b2))
    print("not found")


if __name__ == "__main__":
    main()
