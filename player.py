from person import Person

class Player(Person):
    ''' Player present in the game '''
    def __init__(self, x, y, score=0, life=3):
        '''Initialise The Player'''
        Person.__init__(self, x, y)
        self.coins = 0
        self.life = life
        self.score = score
        self.alive = True

    def coinsCollected(self):
        '''Coins Collected'''
        return self.coins

    def returnScore(self):
        '''Returns the score'''
        return self.score

    def dies(self):
        '''Protocol of when the Player Dies'''
        self.alive = False
        self.score -= 25

    def isAlive(self):
        '''Function To check if player is alive'''
        return self.alive

    def gotCoin(self):
        '''Protocol of when The Player gets a coin'''
        self.coins += 1
        self.score += 5


