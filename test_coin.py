__author__ = "harshil"

import game

class Test_Coin:
    def test_coin(self):
        for test in range(30):
            number = 0
            board = game.Board(0,3,1)
            for i in range(game.ROWS):
                for j in range(game.COLUMNS):
                    number += (board.board[i][j] == game.COINCHAR)
            assert number == 20

if __name__ == "__main__":
    T = Test_Coin()

    T.test_coin()
