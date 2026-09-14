"""BFS search for position where exd5 then Qxd1+ are legal."""
from __future__ import annotations

import chess
from collections import deque

TARGET_AFTER_EXD5 = "Qxd1+"


def main() -> None:
    q: deque[tuple[list[str], chess.Board]] = deque()
    q.append(([], chess.Board()))
    seen: set[str] = set()
    found = 0
    while q and found < 5:
        moves, board = q.popleft()
        if len(moves) >= 20:
            continue
        key = board.fen()
        if key in seen:
            continue
        seen.add(key)
        if len(moves) >= 10:
            if board.turn == chess.WHITE:
                for mv in board.legal_moves:
                    san = board.san(mv)
                    if not san.startswith("exd5"):
                        continue
                    b2 = board.copy()
                    b2.push(mv)
                    for mv2 in b2.legal_moves:
                        if b2.san(mv2) == TARGET_AFTER_EXD5:
                            found += 1
                            seq = moves + [san, TARGET_AFTER_EXD5]
                            print("FOUND", " ".join(moves[:12]), "->", san, TARGET_AFTER_EXD5)
                            print("FEN", b2.fen())
                            break
        if len(moves) >= 18:
            continue
        for mv in list(board.legal_moves)[:40]:
            san = board.san(mv)
            # bias toward main line
            if len(moves) < 6 and san not in {"e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Be7", "d3", "O-O", "Nbd2", "d6", "Re1", "Ne8", "h3"}:
                continue
            b2 = board.copy()
            b2.push(mv)
            q.append((moves + [san], b2))
    print("done, found", found)


if __name__ == "__main__":
    main()
