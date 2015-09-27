__author__ = "harshil"
import pytest

import game

class Test_Princess:
    def test_princess(self):
        for test in range(30):
            number = 0
            board = game.Board(0,3,1)
            for i in range(game.ROWS):
                for j in range(game.COLUMNS):
                    number += (board.board[i][j] == game.PRINCESSCHAR)
            assert number == 1

if __name__ == "__main__":
    T = Test_Princess()

    T.test_princess()
