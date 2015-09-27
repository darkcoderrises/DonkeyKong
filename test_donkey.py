__author__ = "harshil"

import game

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

if __name__ == "__main__":
    T = Test_Donkey()
    T.test_movement()
    T.test_donkey_number()
