# pucks.py
# view citations in __shuffleboard__.py

import pygame
import math, random

class Puck(pygame.sprite.Sprite): 
    SIZE = 20
    FRICTION = 0.05
    ELASTIC = 0.8

    def loadImage(settings): 
        Puck.images = []
        for color in [settings['player1'], settings['player2']]: 
            image = pygame.transform.scale(
            pygame.image.load(f'image/puck_{color}.png'), 
            (Puck.SIZE, Puck.SIZE)).convert_alpha()
            Puck.images.append(image)

    def __init__(self, game, x, y, id): 
        super().__init__()
        self.x, self.y = x, y
        self.id = id
        self.image = None # None
        self.updateRect()
        self.t = 10 # acceleration times
        self.ax, self.ay = 0, 0 # acceleration
        self.vxMax, self.vyMax = 0, 0
        self.vx, self.vy = 0, 0

    def updateRect(self): # self.image = 
        if (self.image == None): 
            self.image = Puck.images[self.id%2]
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x-w/2, self.y-h/2, w, h)

    def updateMovement(self, vx, vy, t): # need to deal with t
        self.t = t
        if (self.ax == 0 and self.ay == 0): # static puck
            self.vxMax = vx
            self.vyMax = vy
            self.ax = (self.vxMax-self.vx)/self.t
            self.ay = (self.vyMax-self.vy)/self.t
        else: # decelerate
            self.vx, self.vy = vx, vy
            self.decelerate('X')
            self.decelerate('Y')
        self.update()

    def decelerate(self, direction): 
        if (self.vy > 0): 
            theta = math.atan(self.vx/self.vy)
        elif (self.vy < 0): 
            theta = math.atan(self.vx/self.vy)-math.pi
        else: 
            theta = math.pi/2
        if (direction == 'X'): 
            self.vxMax = 0
            self.ax = -Puck.FRICTION*math.sin(theta)
        elif (direction == 'Y'): 
            self.vyMax = 0
            self.ay = -Puck.FRICTION*math.cos(theta)

    def stop(self, direction): 
        if (direction == 'X'): 
            self.ax = 0
            self.vx = 0
        elif (direction == 'Y'): 
            self.vy = 0
            self.ay = 0

    # deal with thresholds in puck's movement (acceleration->decleration->stop)
    def updateSpeed(self): 
        if (self.ax != 0): 
            if (self.vxMax != 0 and abs(self.vx) >= abs(self.vxMax)): 
                self.decelerate('X')
            elif (self.vxMax == 0 and (self.vx+self.ax)*self.vx <= 0): 
                self.stop('X')
            self.vx += self.ax
        if (self.ay != 0): 
            if (self.vyMax != 0 and abs(self.vy) >= abs(self.vyMax)): 
                self.decelerate('Y')
            elif (self.vyMax == 0 and (self.vy+self.ay)*self.vy <= 0): 
                self.stop('Y')
            self.vy += self.ay

    def update(self): 
        self.updateSpeed()
        self.x += self.vx
        self.y -= self.vy
        self.updateRect()

    # reverse triangle rule in vector decomposition
    @staticmethod
    def getRemainingSpeed(oldV, decomposedV): 
        if (oldV == 0): 
            return 0
        else: 
            sign = round(oldV/abs(oldV))
            return sign*(oldV**2-decomposedV**2)**0.5

    def doCollision(self, other): # "other" is another Puck object
        # angle in respect to vertical line
        if (self.y-other.y == 0): 
            theta = math.pi/2
        else: 
            theta = -math.atan((self.x-other.x)/(self.y-other.y))
        # speed to be transferred to another puck
        vx1 = self.vx*math.sin(theta)
        vy1 = self.vy*math.cos(theta)
        vx2 = other.vx*math.cos(theta)
        vy2 = other.vy*math.sin(theta)
        v1 = vx1+vy1
        v2 = vx2+vy2
        # remaining speed on x, y directions
        oldVx1 = Puck.getRemainingSpeed(self.vx, vx1)
        oldVy1 = Puck.getRemainingSpeed(self.vy, vy1)
        oldVx2 = Puck.getRemainingSpeed(other.vx, vx2)
        oldVy2 = Puck.getRemainingSpeed(other.vy, vy2)
        # new speed on x, y directions
        newVx1 = oldVx1+v2*math.cos(theta)*Puck.ELASTIC
        newVy1 = oldVy1+v2*math.sin(theta)*Puck.ELASTIC
        newVx2 = oldVx2+v1*math.sin(theta)*Puck.ELASTIC
        newVy2 = oldVy2+v1*math.cos(theta)*Puck.ELASTIC
        # update pucks
        self.updateMovement(newVx1, newVy1, 1)
        other.updateMovement(newVx2, newVy2, 1)





class Puck3D(pygame.sprite.Sprite): 
    SIZE = 80

    @staticmethod
    def loadImage(settings): 
        Puck3D.images = []
        for color in [settings['player1'], settings['player2']]: 
            image = pygame.image.load(f'image/puck3D_{color}.png'
            ).convert_alpha()
            Puck3D.images.append(image)

    def __init__(self, game, puck): 
        super().__init__()
        self.x, self.y, self.prop = game.table3D.convertTo3D(game, 
        puck.x, puck.y)
        self.id = puck.id # need exact match
        self.image0 = None
        self.resizeImage()
        self.updateRect()

    def updateRect(self): 
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x-w/2, self.y-h/2, w, h)

    def resizeImage(self): 
        if (self.image0 == None): 
            self.image0 = Puck3D.images[self.id%2]
        newSize = max(0, int(self.prop*Puck3D.SIZE))
        self.image = pygame.transform.scale(self.image0, 
        (newSize, int(newSize*2/3))).convert_alpha()
        self.y -= newSize/6 # manually offesting perspective effects

    def update(self, game, puck): 
        self.x, self.y, self.prop = game.table3D.convertTo3D(game, 
        puck.x, puck.y)
        self.resizeImage()
        self.updateRect()