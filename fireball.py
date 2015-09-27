'''Fireball Class'''
from person import Person


class Fireball():

    '''Fireballs emmited by donkey'''

    def __init__(self, x, y, dir):
        self.posX = x
        self.posY = y
        self.dir = dir

    def setPos(self, X, Y):
        '''Set Position of Fireball'''
        self.posX = X
        self.posY = Y

    def changeDir(self):
        '''Change Direction of movement of Fireball'''
        self.dir *= -1
