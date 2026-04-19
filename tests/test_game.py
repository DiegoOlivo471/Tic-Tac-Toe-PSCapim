import unittest
import sys
import os

# To run the tests, run on the root directory:
# 
# python -m unittest tests.test_game -v

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import terminal.game as game

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        """Resets global state before each test."""
        game.board = ["-"] * 9
        game.currentPlayer = "X"
        game.gameRunning = True

    # --- Win conditions ---
    def test_win_top_row(self):
        game.board = ["X","X","X", "-","-","-", "-","-","-"]
        game.check_win()
        self.assertFalse(game.gameRunning)

    def test_win_middle_row(self):
        game.board = ["-","-","-", "X","X","X", "-","-","-"]
        game.check_win()
        self.assertFalse(game.gameRunning)

    def test_win_left_column(self):
        game.board = ["X","-","-", "X","-","-", "X","-","-"]
        game.check_win()
        self.assertFalse(game.gameRunning)

    def test_win_middle_column(self):
        game.board = ["-","X","-", "-","X","-", "-","X","-"]
        game.check_win()
        self.assertFalse(game.gameRunning)

    def test_win_main_diagonal(self):
        game.board = ["X","-","-", "-","X","-", "-","-","X"]
        game.check_win()
        self.assertFalse(game.gameRunning)

    def test_win_anti_diagonal(self):
        game.board = ["-","-","X", "-","X","-", "X","-","-"]
        game.check_win()
        self.assertFalse(game.gameRunning)

    def test_no_win_incomplete(self):
        game.board = ["X","X","-", "-","-","-", "-","-","-"]
        game.check_win()
        self.assertTrue(game.gameRunning)

    # --- Tie ---
    def test_tie_detected(self):
        game.board = ["X","O","X", "X","O","O", "O","X","X"]
        game.check_tie()
        self.assertFalse(game.gameRunning)

    def test_no_tie_with_empty_cells(self):
        game.board = ["X","O","X", "X","O","O", "O","X","-"]
        game.check_tie()
        self.assertTrue(game.gameRunning)

    # --- Invalid moves ---
    def test_occupied_cell_not_empty(self):
        game.board[4] = "O"
        self.assertNotEqual(game.board[4], "-")

    def test_computer_random_never_plays_occupied(self):
        game.board = ["X","O","X", "X","O","O", "O","X","-"]
        game.currentPlayer = "O"
        game.computer_move_random()
        self.assertEqual(game.board[8], "O")

    # --- Minimax behavior ---
    def test_minimax_blocks_player_win(self):
        # X is about to win on position 2 — computer must block
        game.board = ["X","X","-", "-","O","-", "-","-","-"]
        game.currentPlayer = "O"
        game.computer_move_smart()
        self.assertEqual(game.board[2], "O")

    def test_minimax_only_one_move(self):
        # Only one empty cell, computer must take it
        game.board = ["X","O","X", "O","X","O", "X","O","-"]
        game.currentPlayer = "O"
        game.computer_move_smart()
        self.assertEqual(game.board[8], "O")

    # --- Player switching ---
    def test_switch_x_to_o(self):
        game.currentPlayer = "X"
        game.switch_players()
        self.assertEqual(game.currentPlayer, "O")

    def test_switch_o_to_x(self):
        game.currentPlayer = "O"
        game.switch_players()
        self.assertEqual(game.currentPlayer, "X")


if __name__ == "__main__":
    unittest.main()