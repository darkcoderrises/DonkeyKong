__author__ = "harshil"

import game
import random

class Test_Donkey:

    def test_movement(self):
        for level in xrange(1,5):
            board = game.Board(0,3,level)
            donkeyPosition = [[] for i in range(level)]
            for i in range(5):
                board.moveDonkey()
                for i,donkey in enumerate(board.Donkey):
                   donkeyPosition[i].append([donkey.posX, donkey.posY])

            for donkeyPos in donkeyPosition:
                prevy = None
                for pos in donkeyPos:
                    x = pos[0]
                    y = pos[1]
                    prevy = y

                    assert x==4 
                    assert prevy-y in range(-1,2)

    def test_donkey_number(self):
        for level in xrange(1,5):
            board = game.Board(0,3,level)
            assert(len(board.Donkey) == level)

    def test_check_donkey(self):
        for level in xrange(1,5):
            board = game.Board(0,3,level)
            for i,donkey in enumerate(board.Donkey):
                assert board.checkDonkey(donkey.posX, donkey.posY)
                assert board.board[donkey.posX][donkey.posY] == game.DONKEYCHAR
                assert board.checkBlocking(donkey.posX, donkey.posY)

    def donkeys(self, board):
        ROWS = game.ROWS
        COLUMNS = game.COLUMNS 
        
        NUM = 0
        for i in range(ROWS):
            for j in range(COLUMNS):
                NUM += (board[i][j] == game.DONKEYCHAR)
        return NUM

    def test_place_donkey(self):
        for test in range(30):
            for level in range(1,2):
                board = game.Board(0,3,level)
                for i in range(5):
                    board.placeDonkey()
                    assert i+level+1 == self.donkeys(board.board)
                    assert i+level+1 == len(board.Donkey)

    def test_check_donkey(self):
        for test in range(30):
            level = random.randint(1,7)
            board = game.Board(0,3,level)
            for i in range(game.ROWS):
                for j in range(game.COLUMNS):
                    if board.board[i][j] == game.DONKEYCHAR:
                        assert board.checkDonkey(i,j)
                    


if __name__ == "__main__":
    T = Test_Donkey()
    T.test_movement()
    T.test_donkey_number()
    T.test_check_donkey()
    T.test_place_donkey()
    T.test_check_donkey()
