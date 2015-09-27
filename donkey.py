'''Donkey Class'''
from person import Person
from fireball import Fireball
import random


class Donkey(Person):

    '''Donkey present in the Game '''

    def emit(self):
        '''Protocol to emit a new FireBall'''
        Direction = random.randint(0, 1)
        fireball = Fireball(self.posX, self.posY, 1 - 2 * Direction)

        self.Fireballs.append(fireball)
        self.times = 0

    def times(self):
        '''Times of movement after last fireball was fired'''
        return self.times

    def reset(self):
        '''Reset value of firing of fireball'''
        return self.reset

    def addTime(self):
        '''Add one to time'''
        self.times += 1

    def __init__(self, x, y, times=0, reset=15, Fireballs=[]):
        Person.__init__(self, x, y)

        self.Fireballs = Fireballs
        self.times = times
        self.reset = reset
