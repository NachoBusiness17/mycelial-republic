"""
Tic-Tac-Toe — Forged in the Quiet Forge (campaign-3c3f7e375550)
Party: cartographer(planner), forgesmith(executor/gemma:2b), mirrorseer(critic), scribe(scribe_file)
Forged: 2026-08-08 · The map IS the territory · 3x3 · X/O alternating · three-in-a-line wins · draw honored
"""
from __future__ import annotations


class TicTacToe:
    """A 3x3 tic-tac-toe game. Two players (X and O) alternate.
    Three in a row/column/diagonal wins. Full board with no winner = draw."""

    def __init__(self) -> None:
        self.board: list[list[str]] = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player: str = "X"
        self.winner: str | None = None
        self.moves: int = 0

    def display(self) -> str:
        """Return a string representation of the board."""
        lines: list[str] = []
        for i, row in enumerate(self.board):
            lines.append(" | ".join(row))
            if i < 2:
                lines.append("--+---+--")
        return "\n".join(lines)

    def move(self, row: int, col: int) -> bool:
        """Place current player's token at (row, col). Returns True if valid."""
        if self.winner is not None:
            return False
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.board[row][col] != " ":
            return False
        self.board[row][col] = self.current_player
        self.moves += 1
        if self._check_win(row, col):
            self.winner = self.current_player
        elif self.moves == 9:
            self.winner = "draw"
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def _check_win(self, row: int, col: int) -> bool:
        """Check if the last move at (row, col) produced three-in-a-line."""
        p = self.current_player
        # Row
        if all(self.board[row][c] == p for c in range(3)):
            return True
        # Column
        if all(self.board[r][col] == p for r in range(3)):
            return True
        # Diagonal (top-left to bottom-right)
        if row == col and all(self.board[i][i] == p for i in range(3)):
            return True
        # Diagonal (top-right to bottom-left)
        if row + col == 2 and all(self.board[i][2 - i] == p for i in range(3)):
            return True
        return False

    def is_over(self) -> bool:
        """True if the game has ended (win or draw)."""
        return self.winner is not None

    def result(self) -> str:
        """Return 'X', 'O', 'draw', or empty string if still playing."""
        return self.winner or ""


def play_cli() -> None:
    """Command-line two-player game loop."""
    game = TicTacToe()
    print("=== Tic-Tac-Toe — The Quiet Forge ===\n")
    print("Board positions (row col):")
    print("  0 0 | 0 1 | 0 2")
    print("  ----+-----+----")
    print("  1 0 | 1 1 | 1 2")
    print("  ----+-----+----")
    print("  2 0 | 2 1 | 2 2\n")

    while not game.is_over():
        print(game.display())
        print(f"\nPlayer {game.current_player}'s turn.")
        try:
            inp = input("Enter row and column (e.g. '1 1'): ").strip()
            if not inp:
                continue
            parts = inp.split()
            if len(parts) != 2:
                print("Enter two numbers: row col")
                continue
            row, col = int(parts[0]), int(parts[1])
            if not game.move(row, col):
                print("Invalid move. Try again.")
        except (ValueError, EOFError):
            print("Invalid input. Try again.")
            continue

    print(game.display())
    result = game.result()
    if result == "draw":
        print("\n=== The forge honors the deadlock — it's a DRAW! ===")
    else:
        print(f"\n=== Player {result} binds three-in-a-line and WINS! ===")


if __name__ == "__main__":
    play_cli()
