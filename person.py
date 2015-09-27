'''Person Class'''


class Person(object):

    """ Definition of a Person in the Game."""

    def __init__(self, x, y):
        self.posX = x
        self.posY = y

    def moveUp(self):
        '''Move Person up'''
        self.posX = (self.posX - 1)

    def moveDown(self):
        '''Move Person down'''
        self.posX = (self.posX + 1)

    def moveLeft(self):
        '''Move Person left'''
        self.posY = (self.posY - 1)

    def moveRight(self):
        '''Move Person Right'''
        self.posY = (self.posY + 1)

    def setPos(self, x, y):
        '''Set Position'''
        self.posX = x
        self.posY = y

    def getPosition(self):
        '''Get Position'''
        return [self.x, self.y]
