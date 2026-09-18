"""Core game logic for Tic-Tac-Toe.

The board is a list of 9 cells indexed 0-8:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

Players are identified by the single characters "X" and "O".
An empty cell holds None.
"""

import copy

BOARD_SIZE = 9

PLAYER_X = "X"
PLAYER_O = "O"

ROWS = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
COLS = ((0, 3, 6), (1, 4, 7), (2, 5, 8))
DIAGS = ((0, 4, 8), (2, 4, 6))
LINES = ROWS + COLS + DIAGS


def empty_board():
    """Return a fresh empty board as a list of nine None cells."""
    return [None] * BOARD_SIZE


def available_moves(board):
    """Return the list of indices of empty cells on the board."""
    return [i for i, cell in enumerate(board) if cell is None]


def other_player(player):
    """Return the opponent of the given player."""
    return PLAYER_O if player == PLAYER_X else PLAYER_X


def make_move(board, move, player):
    """Return a new board with `player` placed at `move`.

    The original board is not modified.
    """
    new_board = copy.copy(board)
    new_board[move] = player
    return new_board


def winner(board):
    """Return the winning player, or None if there is no winner yet."""
    for line in LINES:
        cells = [board[i] for i in line]
        if cells[0] is not None and cells[0] == cells[1] == cells[2]:
            return cells[0]
    return None


def is_full(board):
    """Return True when every cell is occupied."""
    return None not in board


def is_terminal(board):
    """Return True when the game is over (win or draw)."""
    return winner(board) is not None or is_full(board)


def terminal_score(board):
    """Return the outcome of a finished game.

    +1 if X won, -1 if O won, 0 for a draw. Behavior is undefined
    when the board is not terminal.
    """
    win = winner(board)
    if win is PLAYER_X:
        return 1
    if win is PLAYER_O:
        return -1
    return 0


def render(board):
    """Return a human-readable string representation of the board."""
    markers = {None: " ", PLAYER_X: PLAYER_X, PLAYER_O: PLAYER_O}
    rows = []
    for row in ROWS:
        rows.append(" | ".join(markers[board[i]] for i in row))
    return "\n---+---+---\n".join(rows)