"""Find opening where 12. exd5 is legal after 11... d5."""
from __future__ import annotations

import chess

TAIL_FROM_10 = [
    "Nf6",
    "Re1",
    "d5",
    "exd5",
]


def try_prefix(moves: list[str]) -> bool:
    board = chess.Board()
    for m in moves:
        mv = board.parse_san(m)
        if mv not in board.legal_moves:
            return False
        board.push(mv)
    return True


def dfs(prefix: list[str], depth: int = 0, max_depth: int = 18) -> list[str] | None:
    if try_prefix(prefix + TAIL_FROM_10):
        return prefix
    if depth >= max_depth:
        return None
    board = chess.Board()
    for m in prefix:
        board.push(board.parse_san(m))
    if board.is_game_over():
        return None
    # limit branching: prefer main line moves
    cands = []
    for mv in board.legal_moves:
        san = board.san(mv)
        score = 0
        for key in ("e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "c3", "b5", "Bb3", "Nxe4", "O-O", "Be7", "d3", "Nbd2", "d6", "h3", "Re1"):
            if san == key or san.endswith(key):
                score += 1
        cands.append((score, san))
    cands.sort(reverse=True)
    for _, san in cands[:8]:
        found = dfs(prefix + [san], depth + 1, max_depth)
        if found is not None:
            return found
    return None


def main() -> None:
    found = dfs([])
    if not found:
        print("no prefix found")
        return
    print("prefix plies:", len(found))
    print(" ".join(found))
    board = chess.Board()
    for m in found + TAIL_FROM_10:
        board.push(board.parse_san(m))
    print("FEN after 12. exd5:", board.fen())


if __name__ == "__main__":
    main()
