import random
import sys
import os
import time
import threading,thread

try:
    import tty, termios
except ImportError:
    try:
        import msvcrt
    except ImportError:
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        '''Input'''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch

# Globals
ROWS = 30
COLUMNS = 80
VALIDINPUTS = ["w","a","s","d","q"," "]
PLAYERCHAR = "P"
DONKEYCHAR = "D"
PRINCESSCHAR = "Q"
WALLCHAR = "X"
FIREBALLCHAR = "O"
COINCHAR = "C"
STAIRCHAR = "H"
COINCOUNT = 20 
GENERICCHAR = " "
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

class Person(object):
    """ Definition of a Person in the Game."""
    def __init__(self,x,y):
        self.posX = x
        self.posY = y

    def moveUp(self):
            self.posX = (self.posX - 1)%ROWS

    def moveDown(self):
            self.posX = (self.posX + 1)%ROWS 

    def moveLeft(self):
            self.posY = (self.posY - 1)%COLUMNS

    def moveRight(self):
            self.posY = (self.posY + 1)%COLUMNS

    def setPos(self,x,y):
        self.posX = x
        self.posY = y

class Player(Person):
    ''' Player present in the game '''
    def __init__(self,x,y,score=0,life=3):
        '''Initialise The Player'''
        Person.__init__(self,x,y)
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


class Donkey(Person):
    '''Donkey present in the Game '''

    def emit(self,board):
        '''Protocol to emit a new FireBall'''
        Direction = random.randint(0,1) 
        fireball = Fireball(self.posX, self.posY, 1-2*Direction)
        
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

    def __init__(self,x,y,times=0,reset=15,Fireballs = []):
        Person.__init__(self,x,y)
        self.Fireballs = Fireballs
        
        self.times = times
        self.reset = reset


class Fireball():
    '''Fireballs emmited by donkey'''
    def __init__(self,x,y,dir):
        self.posX=x
        self.posY=y
        self.dir = dir

    def setPos(self,X,Y):
        '''Set Position of Fireball'''
        self.posX = X
        self.posY = Y

    def changeDir(self):
        '''Change Direction of movement of Fireball'''
        self.dir *= -1


class Board(object):
    ''' Class for the Actual Board to printed '''

    def checkCoin(self, x, y):
        ''' Checks Coin '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return False
        return self.board[x][y] == COINCHAR

    def checkWall(self, x, y):
        ''' Checks Wall '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return False
        return self.orign[x][y] == 1

    def checkDonkey(self, x, y):
        ''' Checks Wall '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return False
        return self.board[x][y] == DONKEYCHAR

    def checkStair(self, x, y):
        ''' Checks Wall '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return False
        return self.orign[x][y] == 2

    def checkFireball(self, x, y):
        ''' Checks Wall '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return False
        return self.board[x][y] == FIREBALLCHAR

    def checkGravity(self, x, y):
        ''' Checks if it is freefall or not '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return False

        if self.checkWall(x+1,y) or self.checkStair(x,y):
            return True
        elif self.checkWall(x,y)==True and self.checkStair(x+1,y)==True:
            return True

        return False

    def checkPrincess(self, x, y):
        ''' checks Princess '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return False
        return self.board[x][y] == PRINCESSCHAR

    def checkBlocking(self, x, y):
        ''' checks blockage '''
        if x>=ROWS or y>=COLUMNS or x<0 or y<0:
            return True
        return self.checkWall(x,y) or self.checkDonkey(x,y) 

    def checkDeath(self, x, y):
        ''' checks Death '''
        return self.checkFireball(x, y)

    def checkPlayer(self, x, y):
        ''' checks player'''
        return self.Player.posX == x and self.Player.posY == y

    def placePlayer(self,score = 0):
        ''' Places Player on the map initially with the score'''

        self.Player = Player(ROWS-2,1,score)
        self.board[self.Player.posX][self.Player.posY] = PLAYERCHAR

    def placeDonkey(self):
        ''' Places Donkey on the map initially '''

        donkeyi = self.floor[-2:-1][0]-1
        donkeyj = 0
        PLACED = False

        while not PLACED:
            donkeyj = random.randint(1,COLUMNS-1)
            if self.orign[donkeyi][donkeyj] == 0 and self.orign[donkeyi+1][donkeyj] == 1:
                PLACED = True
                self.board[donkeyi][donkeyj] = DONKEYCHAR
        self.Donkey.append(Donkey(donkeyi, donkeyj))

    def placePrincess(self):
        ''' Places Princess on the map initially '''

        princessi = self.floor[-1:][0]-1
        princessj = 0
        PLACED = False

        while not PLACED:
            princessj = random.randint(1,COLUMNS-1)
            if self.orign[princessi][princessj] == 0 and self.orign[princessi+1][princessj] == 1:
                PLACED = True
                self.board[princessi][princessj] = PRINCESSCHAR

    def placeMap(self):
        '''Creates a Empty Map i.e. basic framework of stairs and floors'''

        def set(self,i,j):
            self.board[i][j] = WALLCHAR
            self.orign[i][j] = 1

        FLOOR=ROWS-1
        for i in reversed(xrange(ROWS)):
            set(self,i,0)
            set(self,i,COLUMNS-1)

            if i!=FLOOR:
                continue
            if FLOOR==2:
                FLOOR=0
            else:
                FLOOR=max(FLOOR-4,2)
            
            if i:
                self.floor.append(i)
            if i==0 or i==ROWS-1:
                for j in xrange(COLUMNS):
                    set(self,i,j)
                
            else :
                colX = random.randint(0,COLUMNS/2-1)
                colY = random.randint(COLUMNS/2,COLUMNS-1)

                for j in xrange(colX,colY+1):
                    set(self,i,j)

                if i==2:
                    set(self,1,colX)
                    set(self,1,colY)

                STAIR = True

                while STAIR:
                    stairPos = random.randint(colX,colY-1)
                    I = i+1

                    while self.orign[I][stairPos]!= 1:
                        I+=1

                    if I-i>5:
                        continue
                    
                    else:
                        I=i+1
                        while self.orign[I][stairPos]!= 1:
                            self.board[I][stairPos] = STAIRCHAR
                            self.orign[I][stairPos] = 2
                            I+=1

                        STAIR = False
                        

    def placeCoin(self):
        '''Places coin in the map initially'''

        PLACED = False
        while not PLACED:
            Floori = self.floor[random.randint(0,len(self.floor)-2)]
            Floorj = random.randint(2,COLUMNS-2)

            if self.board[Floori][Floorj] == WALLCHAR and self.orign[Floori-1][Floorj] not in [1,2,3]:
                self.orign[Floori-1][Floorj] = 3
                self.board[Floori-1][Floorj] = COINCHAR
                PLACED = True

    def moveFireball(self, Fireball):
        '''Controls Movement Of Fireball'''

        prevX = Fireball.posX
        prevY = Fireball.posY

        newX  = Fireball.posX 
        newY  = Fireball.posY + Fireball.dir

        rand = random.randint(0,1)

        if self.checkBlocking(newX, newY) or self.checkFireball(newX,newY):
            if rand: 
                Fireball.changeDir()
            return Fireball

        if self.board[newX+1][newY] == GENERICCHAR:
            while self.board[newX+1][newY] == GENERICCHAR:
                newX+=1
            if rand:
                Fireball.changeDir()

        if self.board[newX+1][newY] == WALLCHAR and newX+2<ROWS:
            if self.board[newX+2][newY] == STAIRCHAR:
                newX+=1
                if rand:
                    Fireball.changeDir()
            while self.board[newX+1][newY] != WALLCHAR:
                newX+=1
        
        self.board[prevX][prevY] = self.abc[self.orign[prevX][prevY]]
        if newX == ROWS-2 and newY == 1:
            return None

        if self.checkPlayer(newX, newY):
            self.Player.dies()

        self.board[newX][newY] = FIREBALLCHAR

        Fireball.setPos(newX,newY)
        return Fireball


    def moveFireballs(self, FireballsList):
        ''' Places Fireballs into Map '''
        L = []
        for Fireball in FireballsList:
            new = self.moveFireball(Fireball)
            if new:
                L.append(new)
        return L

    def movePerson(self, person, choice):
        '''Moves a Person according to will'''
        if choice == "w":
            person.moveUp()
        if choice == "s":
            person.moveDown()
        if choice == "a":
            person.moveLeft()
        if choice == "d":
            person.moveRight()

    def moveDonkey(self):
        '''Moves all Donkey according to will'''
    
        print "Donkey"
        for i in xrange(len(self.Donkey)):
            prevX = self.Donkey[i].posX
            prevY = self.Donkey[i].posY
            
            k=0
            PLACED = False
            while not PLACED:
                L = random.randint(-1,1)
                k+=1
                if k==3:
                    L=0
                if self.board[prevX+1][prevY+L] == WALLCHAR and self.board[prevX][prevY+L] not in [DONKEYCHAR] and not self.checkBlocking(prevX,prevY+L): 
                    PLACED = True
                    self.Donkey[i].setPos(prevX,prevY+L)

            self.board[prevX][prevY] = self.abc[self.orign[prevX][prevY]]
            self.board[self.Donkey[i].posX][self.Donkey[i].posY] = DONKEYCHAR

            self.Donkey[i].addTime()
            if self.Donkey[i].times==self.Donkey[i].reset:
                self.Donkey[i].emit(self)

            self.Donkey[i].Fireballs = self.moveFireballs(self.Donkey[i].Fireballs )


    def movePlayer(self,jump=0):
        '''Moves a Player according to will'''

        if jump == 2:
            while 1:
                prevX = self.Player.posX
                prevY = self.Player.posY

                if self.board[prevX+1][prevY] in self.abc[1:] :
                    break

                self.Player.setPos(prevX+1,prevY)
                self.board[prevX][prevY] = self.abc[self.orign[prevX][prevY]]
                self.board[self.Player.posX][self.Player.posY] = PLAYERCHAR
                self.printBoard()
                time.sleep(1)
            return


        prevX = self.Player.posX
        prevY = self.Player.posY

        self.movePerson(self.Player, self.input)

        if self.checkPrincess(self.Player.posX, self.Player.posY):
            b = Board(self.Player.score+50, self.life, self.level+1)
            b.play()

        if jump:
            if not self.checkGravity(self.Player.posX, self.Player.posY):
                if self.checkWall(prevX+1,prevY) and self.input in ["a" , "d"]:
                    ## FREEFALL
                    self.board[prevX][prevY] = self.abc[self.orign[prevX][prevY]]
                    while not self.checkWall(self.Player.posX+1, self.Player.posY):
                        prevX = self.Player.posX
                        prevY = self.Player.posY
                        self.movePerson(self.Player,"s")
                        self.board[prevX][prevY] = self.abc[self.orign[prevX][prevY]]
                        self.board[self.Player.posX][self.Player.posY] = PLAYERCHAR
                        self.printBoard()
                        time.sleep(0.1)

                else:
                    self.Player.setPos(prevX, prevY)
                    return 

        if self.checkBlocking(self.Player.posX, self.Player.posY) :
            if not self.checkStair(prevX, prevY) :
                self.Player.setPos(prevX,prevY)
                return 

        if self.checkDeath(self.Player.posX, self.Player.posY) :
            self.Player.dies()
            return 

        if self.checkCoin(self.Player.posX, self.Player.posY):
            self.Player.gotCoin()
            self.orign[self.Player.posX][self.Player.posY] = 0


        
        self.board[prevX][prevY] = self.abc[self.orign[prevX][prevY]]
        self.board[self.Player.posX][self.Player.posY] = PLAYERCHAR

        
    def printBoard(self):
        ''' Prints the Board'''
        os.system("clear")
        for i in xrange(0,ROWS):
            for j in xrange(0,COLUMNS):
                if (not (i == self.Player.posX and j == self.Player.posY )) and self.board[i][j] == PLAYERCHAR:
                    self.board[i][j] = self.abc[self.orign[i][j]]
                if self.board[i][j] == COINCHAR:
                    print( OKBLUE + self.board[i][j]  + ENDC),
                elif self.board[i][j] ==  WALLCHAR :
                    print( OKGREEN + self.board[i][j]  + ENDC),
                elif self.board[i][j] == STAIRCHAR : 
                    print( HEADER + self.board[i][j] + ENDC),
                elif self.board[i][j] == FIREBALLCHAR:
                    print( FAIL + self.board[i][j]  + ENDC),
                elif self.board[i][j] == PLAYERCHAR:
                    print( WARNING + self.board[i][j]  + ENDC),
                elif self.board[i][j] == DONKEYCHAR:
                    print( FAIL + self.board[i][j]  + ENDC),
                else:
                    print( self.board[i][j] ),
            print

        print "\nCoins Collected :"+str(self.Player.coinsCollected())
        print "Score : " + str(self.Player.returnScore())
        print "Lifes : " + str(self.life)
        print "Level : " + str(self.level)
        print "w,a,s,d to move, space followed by a or d to jump in eighter direction, q to quit"


    def empty(self):
        ''' Removes all the Fireballs from the code '''

        for Donkey in self.Donkey:
            Donkey.Fireball = []

    def playerDies(self):
        ''' Protocol to as when the player dies'''

        if self.life == 1:
            os.system("clear")
            print "You Lose"
            sys.exit()

        self.life -= 1
        
        prevX = self.Player.posX
        prevY = self.Player.posY

        self.Player.setPos(ROWS-2,1)

        self.Player.alive = True

        self.board[prevX][prevY] = self.abc[self.orign[prevX][prevY]]
        self.board[ROWS-2][1] = PLAYERCHAR

        self.printBoard()


    def play(self):
        ''' Driver Function of the Game '''
        
        self.empty()
        
        while True:
            self.printBoard()
            self.input = getch()

            if self.input not in VALIDINPUTS:
               continue

            if self.input == "q":
                sys.exit()

            if self.input == " ":
                
                self.input = getch()
                while self.input not in ["a","d"]:
                    self.input = getch()
                movement = self.input
                
                L=["w","s"]
                for i in range(4):
                    self.input = L[i/2]
                    self.moveDonkey()
                    self.movePlayer()
                    self.input = movement
                    self.movePlayer()
                    self.printBoard()
                    time.sleep(0.2) 

                self.movePlayer(2)
                self.printBoard()


            else:
                self.moveDonkey()
                self.movePlayer(1)

            if not self.Player.isAlive():
                self.playerDies()
    
    def setMap(self, COIN=COINCOUNT, score = 0):
        ''' Sets the Complete Map, one by one. Orgin if filled on this perticular order:
            0. Generic char (blank space)
            1. Wall
            2. Stair
            3. Coin
        '''
        self.placeMap()

        for i in xrange(self.level*5):
            x = random.randint(4,ROWS-2)
            y = random.randint(2,COLUMNS-2)
            
            if self.board[x][y] == STAIRCHAR:
                continue
            
            self.board[x][y] = GENERICCHAR
            self.orign[x][y] = 0


        while COIN:
            self.placeCoin()
            COIN-=1

        self.placePlayer(score)
        self.placePrincess()
        
        for i in xrange(self.level):
            self.placeDonkey()


    def __init__(self,score=0,life=3,level=1):
        ''' Initializes the boerd. Place elements on the board. '''
        self.board = [[GENERICCHAR for i in xrange(COLUMNS)] for j in xrange(ROWS)]
        self.orign = [[          0 for i in xrange(COLUMNS)] for j in xrange(ROWS)]
        self.floor = []
        
        self.Donkey = []
        self.Player = None
        self.life = life
        self.level = level
        self.input=""
        self.abc = [GENERICCHAR, WALLCHAR, STAIRCHAR, COINCHAR]

        self.setMap(COINCOUNT, score)

if __name__ == "__main__":        
    b = Board()
    b.play()
