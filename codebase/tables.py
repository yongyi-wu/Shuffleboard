# tables.py
# view citations in __shuffleboard__.py

import pygame
from pucks import *

class Table(pygame.sprite.Sprite): 
    WIDTH = 100
    HEIGHT = 600
    LINE1 = HEIGHT/24
    LINE2 = HEIGHT/12
    LINE3 = HEIGHT/5
    EDGE1 = HEIGHT/40
    EDGE2 = EDGE1+WIDTH/10
    EDGEFILL = (180, 150, 125)
    BOTTOMFILL = (105, 105, 105)
    LINEFILL = (20, 20, 20)
    SERVEFILL = (0, 130, 0)

    @staticmethod
    def loadImage(): 
        Table.image = pygame.transform.scale(
        pygame.image.load('image/shuffleboard.jpg'), 
        (Table.WIDTH, Table.HEIGHT)).convert_alpha()
        # lines to indicate points
        for dist in ([Table.LINE1, Table.LINE2, Table.LINE3]): 
            pygame.draw.line(Table.image, Table.LINEFILL, 
            (0, dist), (Table.WIDTH, dist), 3)
        pygame.draw.line(Table.image, Table.SERVEFILL, (0, 
        Table.HEIGHT-Table.LINE2), (Table.WIDTH, Table.HEIGHT-Table.LINE2), 3)
        # number to indicate points
        pointObject = pygame.font.SysFont('Points', int(Table.LINE1*4/5))
        point1 = pointObject.render('1', True, Table.LINEFILL)
        point1Rect = point1.get_rect(center=(Table.WIDTH/2, 
        (Table.LINE2+Table.LINE3)/2))
        Table.image.blit(point1, point1Rect)
        point2 = pointObject.render('2', True, Table.LINEFILL)
        point2Rect = point1.get_rect(center=(Table.WIDTH/2, 
        (Table.LINE1+Table.LINE2)/2))
        Table.image.blit(point2, point2Rect)
        point3 = pointObject.render('3', True, Table.LINEFILL)
        point3Rect = point1.get_rect(center=(Table.WIDTH/2, Table.LINE1/2))
        Table.image.blit(point3, point3Rect)

    def __init__(self, game, x, y): 
        super().__init__()
        x = x
        y = y
        self.image = Table.image
        w, h = self.image.get_size() # size may change if add paddings
        self.rect = pygame.Rect(x, y, w, h)
        # size may change if add paddings
        self.marginTop = self.rect.top
        self.marginBottom = game.height-self.rect.bottom

    # reversely solving the convertTo3D() method in Table class
    def convertTo2D(self, game, x3D, y3D): 
        d = game.table3D.cameraD
        yc = game.table3D.cameraY
        yp = 1-(game.table3D.rect.bottom-y3D)/yc
        xp = 2*(x3D-game.table3D.rect.centerx)/(game.table3D.scale*
        self.rect.width)
        zc = d/yp
        xc = (xp*zc*self.rect.width)/(2*d)
        x2D = xc+game.table3D.cameraX
        y2D = game.height+game.table3D.cameraZ-zc
        return x2D, y2D

    def isOutofBound(self, x, y): 
        return (x < self.rect.left or x > self.rect.right or 
        y < self.rect.top or y > self.rect.bottom)

    def updateScore(self, pucks): 
        player1 = 0
        player2 = 0
        for puck in pucks: 
            score = 0
            if (self.rect.top+Table.LINE2 < puck.y <= 
                self.rect.top+Table.LINE3): 
                score = 1
            elif (self.rect.top+Table.LINE1 < puck.y <= 
                  self.rect.top+Table.LINE2): 
                score = 2
            elif (self.rect.top < puck.y <= self.rect.top+Table.LINE1): 
                score = 3
            if (puck.id%2 == 0): 
                player1 += score
            else: 
                player2 += score
        return player1, player2





class Table3D(pygame.sprite.Sprite): 
    WIDTH = 400
    HEIGHT = 300
    SIDEFILL = (160, 130, 100)
    EDGEFILL = Table.EDGEFILL
    BOTTOMFILL = Table.BOTTOMFILL
    LINEFILL = Table.LINEFILL
    SERVEFILL = Table.SERVEFILL

    @staticmethod
    def loadImage(): 
        Table3D.image = pygame.transform.scale(
        pygame.image.load('image/shuffleboard3D.png'), 
        (Table3D.WIDTH, Table3D.HEIGHT)).convert_alpha()
        Table3D.frontImage = pygame.transform.scale(
        pygame.image.load('image/shuffleboard3D_front.jpg'), 
        (Table3D.WIDTH, int(Table3D.WIDTH/8))).convert_alpha()

    def __init__(self, game, x, y): 
        super().__init__()
        x = x
        y = y
        self.image = Table3D.image
        w, h = self.image.get_size()
        self.rect = pygame.Rect(x, y, w, h)
        self.topX = 145/400*self.rect.width+self.rect.x # table3D topLeft corner
        self.setCamera(game)
        self.drawLines(game)

    def convertPoint(self, game, x, y): 
        x, y, _ = self.convertTo3D(game, game.table.rect.x+x, 
        game.table.rect.y+y)
        x -= self.rect.x-1 # -1: manual adjustment 
        y -= self.rect.y
        return x, y

    def drawLines(self, game): 
        for dist in [Table.LINE1, Table.LINE2, Table.LINE3]: 
            x0, y0 = self.convertPoint(game, 0, dist)
            x1, y1 = self.convertPoint(game, Table.WIDTH, dist)
            pygame.draw.line(self.image, Table3D.LINEFILL, (x0, y0), 
            (x1, y1), 1)
        x3, y3 = self.convertPoint(game, 0, Table.HEIGHT-Table.LINE2)
        x4, y4 = self.convertPoint(game, Table.WIDTH, Table.HEIGHT-Table.LINE2)
        pygame.draw.line(self.image, Table3D.SERVEFILL, (x3, y3), (x4, y4), 4)

    # calculate observation point (CAMERA) for table based on table3D image
    def setCamera(self, game): 
        margins = game.table.marginTop+game.table.marginBottom
        self.scale = self.rect.width/game.table.rect.width
        # horizontal perspective effect
        kx = (self.rect.centerx-self.topX)/(self.scale*game.table.rect.width/2)
        self.cameraD = (game.height-margins)*kx/(1-kx)
        self.cameraX = game.table.rect.x+game.table.rect.width/2
        # vertical perspective effect
        ky = self.cameraD/(game.height-margins+self.cameraD)
        self.cameraY = (self.rect.bottom-self.rect.top)/(1-ky)
        self.cameraZ = self.cameraD-game.table.marginBottom

    def convertTo3D(self, game, x, y): 
        # position relative to camera
        d = self.cameraD
        xc = x-self.cameraX
        yc = self.cameraY
        zc = game.height-y+self.cameraZ
        # project to a normalized plane
        xp = (d*xc/(game.table.rect.width/2))/zc
        yp = d/zc
        # resize according to the table surface
        x3D = self.rect.centerx+self.scale*game.table.rect.width/2*xp
        y3D = self.rect.bottom-yc*(1-yp)
        return x3D, y3D, yp