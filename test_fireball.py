__author__ = "harshil"

import game
import random
from fireball import Fireball

class Test_Fireball:
    def get_genericchar(self,board):
        L=[]
        ROWS = game.ROWS
        COLUMNS = game.COLUMNS
        for i in range(3, ROWS):
            for j in range(3, COLUMNS):
                if board.checkGravity(i, j) and not (board.checkBlocking(i,j) or board.checkBlocking(i-1,j)):
                    L.append((i, j))
        return L[random.randint(0,len(L)-1)]

    def get_fireball(self,board):
        ROWS = game.ROWS
        COLUMNS = game.COLUMNS
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board.board[i][j] == game.FIREBALLCHAR:
                    return (i,j)
    
    def get_blocking(self,board):
        L = []
        ROWS = game.ROWS
        COLUMNS = game.COLUMNS
        for i in range(3,ROWS):
            for j in range(3,COLUMNS):
                if board.checkBlocking(i,j):
                    L.append((i,j))
        return L[random.randint(0,len(L)-1)]

    def test_gravityfall(self):
        for test in range(30):
            board = game.Board(0,3,1)
            pos = self.get_genericchar(board)
            pos_x = pos[0]
            pos_y = pos[1]

            fireball = Fireball(pos_x-1,pos_y,1)
            board.moveFireball(fireball)

            new = self.get_fireball(board)
            if not new:
                continue

            new_x = new[0]
            new_y = new[1]

            assert pos_y == new_y-1
            assert board.board[new_x+1][new_y] != game.GENERICCHAR

    def test_blocking(self):
        for test in range(30):
            board = game.Board(0,3,1)
            pos = self.get_blocking(board)
            pos_x = pos[0]
            pos_y = pos[1]

            fireball = Fireball(pos_x-1, pos_y, 1)
            #print pos, self.get_fireball(board)
            board.moveFireball(fireball)
            #raw_input()


if __name__ == "__main__":
    T = Test_Fireball()

    T.test_gravityfall()
    T.test_blocking()
