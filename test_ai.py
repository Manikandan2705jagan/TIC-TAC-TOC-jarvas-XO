"""Tests for the Tic-Tac-Toe AI.

Run with:  python -m unittest test_ai -v
"""

import unittest

import ai
import tictactoe as ttt


def board_from(template):
    mapping = {"x": ttt.PLAYER_X, "o": ttt.PLAYER_O, ".": None}
    cells = [mapping[ch] for ch in template.replace(" ", "")]
    assert len(cells) == 9, template
    return cells


class GameLogicTests(unittest.TestCase):
    def test_new_board_is_empty(self):
        self.assertEqual(available := ttt.available_moves(ttt.empty_board()),
                         list(range(9)))

    def test_winner_rows(self):
        self.assertEqual(ttt.winner(board_from("xxx......")), ttt.PLAYER_X)
        self.assertEqual(ttt.winner(board_from("...ooo...")), ttt.PLAYER_O)

    def test_winner_columns(self):
        self.assertEqual(ttt.winner(board_from("xo.xo.x..")), ttt.PLAYER_X)

    def test_winner_diagonals(self):
        self.assertEqual(ttt.winner(board_from("x.o.x.o.x")), ttt.PLAYER_X)
        self.assertEqual(ttt.winner(board_from("o.xox.x..")), ttt.PLAYER_X)

    def test_no_winner_on_partial(self):
        self.assertIsNone(ttt.winner(board_from("x.o......")))

    def test_draw_detection(self):
        draw = board_from("xxoooxxxo")  # X X O / O O X / X X O
        self.assertTrue(ttt.is_terminal(draw))
        self.assertEqual(ttt.terminal_score(draw), 0)


class MinimaxTests(unittest.TestCase):
    def test_plain_minimax_on_empty_board_is_draw(self):
        score, _ = ai.minimax(ttt.empty_board(), ttt.PLAYER_X)
        self.assertEqual(score, 0, "perfect play from the empty board is a draw")

    def test_alpha_beta_matches_plain_minimax(self):
        for template in ("......... ", "x........", "...o...x.",
                         "xo.......", "xxo.o....", "xox.o.ox."):
            board = board_from(template)
            if ttt.is_terminal(board):
                continue
            plain_score, plain_move = ai.minimax(board, ttt.PLAYER_X)
            pruned_score, pruned_move = ai.minimax_ab(
                board, ttt.PLAYER_X, -ai.INF, ai.INF)
            self.assertEqual(plain_move, pruned_move, template)
            self.assertEqual(plain_score, pruned_score, template)

    def test_alpha_beta_takes_immediate_win(self):
        board = board_from("xx.o.....")
        score, move = ai.minimax_ab(board, ttt.PLAYER_X, -ai.INF, ai.INF)
        self.assertEqual(move, 2)
        self.assertGreater(score, 0)

    def test_alpha_beta_blocks_opponent_win(self):
        board = board_from("oo.x.....")
        score, move = ai.minimax_ab(board, ttt.PLAYER_X, -ai.INF, ai.INF)
        self.assertEqual(move, 2, "X must block O's winning row")
        self.assertNotEqual(score, -9, "X must not lose instantly")

    def test_best_move_interface(self):
        self.assertIn(ai.best_move(ttt.empty_board(), ttt.PLAYER_X),
                      range(9))
        self.assertIn(ai.best_move(ttt.empty_board(), ttt.PLAYER_O,
                                   alpha_beta=False), range(9))

    def test_score_on_empty_board_is_draw(self):
        score, _ = ai.minimax(ttt.empty_board(), ttt.PLAYER_X)
        self.assertEqual(score, 0, "perfect play from the empty board is a draw")
        move = ai.best_move(ttt.empty_board(), ttt.PLAYER_X)
        self.assertIn(move, range(9))

    def test_alpha_beta_never_loses_on_its_turn(self):
        """X to move: score must never be negative (AI never forced to lose)."""
        board = board_from("x..o.....")
        score, _ = ai.minimax_ab(board, ttt.PLAYER_X, -ai.INF, ai.INF)
        self.assertGreaterEqual(score, 0)


class PruningComparisonTests(unittest.TestCase):
    def test_pruning_explores_fewer_nodes(self):
        result = ai.compare_searches(ttt.empty_board(), ttt.PLAYER_X)
        self.assertEqual(result["plain_move"], result["pruned_move"])
        self.assertGreater(result["plain_nodes"], result["pruned_nodes"])

    def test_pruning_does_not_change_move_on_late_game(self):
        board = board_from("xox.ox.xx")
        result = ai.compare_searches(board, ttt.PLAYER_X)
        self.assertEqual(result["plain_move"], result["pruned_move"])


if __name__ == "__main__":
    unittest.main()