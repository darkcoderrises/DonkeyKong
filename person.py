class Person(object):
    """ Definition of a Person in the Game."""
    def __init__(self, x, y):
        self.posX = x
        self.posY = y

    def moveUp(self):
        self.posX = (self.posX - 1) 

    def moveDown(self):
        self.posX = (self.posX + 1) 

    def moveLeft(self):
        self.posY = (self.posY - 1) 

    def moveRight(self):
        self.posY = (self.posY + 1) 

    def setPos(self, x, y):
        self.posX = x
        self.posY = y
