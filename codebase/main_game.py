# main_game.py
# view citations in __shuffleboard__.py

import pygame
import os, pickle, random
from tables import *
from pucks import *
from boxes import *

class MainGame(object): 
    def __init__(self, game): 
        # basic setup
        self.game = game
        self.settings = game.settings
        self.width = game.width
        self.height = game.height
        # objects and settings
        self.loadGame()

    def initGameObjects(self): 
        # Table
        Table.loadImage()
        self.table = Table(self, 900, 40)
        self.loadTable()
        # Table3D
        Table3D.loadImage()
        self.table3D = Table3D(self, 250, 275)
        self.loadTable3D()
        # Puck
        Puck.loadImage(self.settings)
        self.pucksGroup = pygame.sprite.Group()
        self.staticPucks = pygame.sprite.Group()
        self.movingPucks = pygame.sprite.Group()
        self.collidedList = []
        self.regroupPucks()
        # Puck3D
        Puck3D.loadImage(self.settings)
        self.pucks3DGroup = pygame.sprite.Group()
        self.pucksDict = dict()

    def initBoxes(self): 
        self.boxesGroup = pygame.sprite.Group()
        # player information
        fontSize = 45
        if (self.settings['pve']): 
            self.player1 = TextBox(self.table3D.rect.centerx-2*fontSize, 
            fontSize, 'You', fontSize/2, True)
            self.player2 = TextBox(self.table3D.rect.centerx+2*fontSize, 
            fontSize, 'Computer', fontSize/2, True)
        else: 
            self.player1 = TextBox(self.table3D.rect.centerx-2*fontSize, 
            fontSize, 'Player1', fontSize/2, True)
            self.player2 = TextBox(self.table3D.rect.centerx+2*fontSize, 
            fontSize, 'Player2', fontSize/2, True)
        self.player1Points = TextBox(self.player1.rect.centerx, 
        self.player1.rect.bottom+fontSize/2, '0', fontSize/2)
        self.player2Points = TextBox(self.player2.rect.centerx, 
        self.player2.rect.bottom+fontSize/2, '0', fontSize/2)
        player1 = self.settings['player1']
        player2 = self.settings['player2']
        self.player1Remaining = TextBox(self.player1.rect.centerx, 
        self.player1Points.rect.bottom+fontSize/2, f' * {self.maxPucks//2}', 
        fontSize/2, url=f'image/puck_{player1}.png')
        self.player2Remaining = TextBox(self.player2.rect.centerx, 
        self.player2Points.rect.bottom+fontSize/2, f' * {self.maxPucks//2}', 
        fontSize/2, url=f'image/puck_{player2}.png')
        # buttons
        fontSize = 40
        self.splashButton = Button(fontSize, self.height-fontSize, '', 
        fontSize, url='image/icon/home.png')
        self.resetButton = Button(fontSize, self.height-3*fontSize, '', 
        fontSize, url='image/icon/reset.png')
        self.saveButton = Button(fontSize, self.height-5*fontSize, '', 
        fontSize, url='image/icon/save.png')
        self.boxesGroup.add([self.resetButton, self.splashButton, 
        self.saveButton, self.player1, self.player2, self.player1Points, 
        self.player2Points, self.player1Remaining, self.player2Remaining])

    def loadGame(self): 
        # miscellaneous
        self.free = False
        self.isOver = False
        self.puckId = 0
        self.maxPucks = 8 # must be even number
        self.newPuck = None
        self.selected = False
        self.charging = False
        self.fileNumbers = len(os.listdir('record'))
        # tables and pucks
        self.initGameObjects()
        # audio
        self.audios = {
            'shuffle': 'audio/shuffle.mp3', 
            'collide': 'audio/collide.mp3'
        }
        # textboxes and buttons
        self.initBoxes()

    def loadTable(self): 
        edge1 = Table.EDGE1
        self.tableEdge1 = pygame.Rect(self.table.rect.x-edge1, 
        self.table.rect.y-edge1, 
        self.table.rect.width+2*edge1, self.table.rect.height+2*edge1)
        edge2 = Table.EDGE2
        self.tableEdge2 = pygame.Rect(self.table.rect.x-edge2, 
        self.table.rect.y-edge2, 
        self.table.rect.width+2*edge2, self.table.rect.height+2*edge2)

    def loadTable3D(self): 
        self.table3D.drawLines(self)
        x2, y2, _ = self.table3D.convertTo3D(self, self.tableEdge2.left, 
        self.tableEdge2.top)
        x3, y3, _ = self.table3D.convertTo3D(self, self.tableEdge2.right, 
        self.tableEdge2.top)
        backW = x3-x2
        backH = backW/20
        x0, y0 = x2, y2-backH
        x1, y1 = x3, y3-backH
        y2, y3 = y2+backH, y3+backH
        x6, y6, _ = self.table3D.convertTo3D(self, self.tableEdge2.left, 
        self.tableEdge2.bottom)
        x7, y7, _ = self.table3D.convertTo3D(self, self.tableEdge2.right, 
        self.tableEdge2.bottom)
        frontW = x7-x6
        frontH = backH*frontW/backW
        x4, y4 = x6, y6-frontH
        x5, y5 = x7, y7-frontH
        y6, y7 = y6+frontH, y7+frontH
        self.table3DXs = [x0, x1, x2, x3, x4, x5, x6, x7]
        self.table3DYs = [y0, y1, y2, y3, y4, y5, y6, y7]
    
    def packGameState(self): 
        gameState = {}
        gameState['settings'] = self.settings
        gameState['selected'] = self.selected
        gameState['puckId'] = self.puckId
        gameState['pucks'] = {}
        for puck in self.pucksGroup: 
            puckState = {}
            puckState['t'] = puck.t
            puckState['coordinate'] = (puck.x, puck.y)
            puckState['acceleration'] = (puck.ax, puck.ay)
            puckState['speed'] = [(puck.vxMax, puck.vyMax), (puck.vx, puck.vy)]
            gameState['pucks'][puck.id] = puckState
        return gameState

    def storeGameState(self): 
        gameState = self.packGameState()
        fileNumbers = len(os.listdir('record'))
        filename = f'record/game_state{fileNumbers+1}.txt'
        file1 = open(filename, 'wb')
        pickle.dump(gameState, file1)
        file1.close()

    def isServable(self, x, y): 
        return (not self.table.isOutofBound(x, y) and 
                y > self.table.rect.bottom-Table.LINE2 and 
                len(self.movingPucks) == 0)

    def mouseMoved(self, x, y): 
        self.boxesGroup.update(x, y)

    def mousePressed(self, x, y): 
        if (self.splashButton.isSelected(x, y)): 
            self.game.isMainGame = False
            self.game.isSplashScreen = True
        elif (self.resetButton.isSelected(x, y)): 
            self.loadGame()
        elif (self.saveButton.isSelected(x, y) and self.fileNumbers <= 12): 
            self.storeGameState()
            print('Saved!')
        if (self.isOver): 
            return

    def mouseDragged(self, x, y): 
        if (self.isOver): 
            return
        if (self.newPuck != None): 
            self.charging = True
            self.finalX3D, self.finalY3D = x, y
            self.finalX2D, self.finalY2D = self.table.convertTo2D(self, x, y)
            (self.dx, self.dy) = (self.finalX2D-self.prevX2D, 
            self.finalY2D-self.prevY2D)
            self.force = (self.dx**2+self.dy**2)**0.5

    def mouseReleased(self, x, y): 
        if (self.isOver): 
            return
        if (self.newPuck == None): 
            x2D, y2D = self.table.convertTo2D(self, x, y)
            if (self.free or self.isServable(x2D, y2D)): # create a new puck
                self.newPuck = Puck(self, x2D, y2D, self.puckId)
                newPuck3D = Puck3D(self, self.newPuck)
                self.pucksGroup.add(self.newPuck)
                self.pucks3DGroup.add(newPuck3D)
                self.pucksDict[self.newPuck.id] = newPuck3D
                self.puckId += 1
                self.prevX2D, self.prevY2D = self.newPuck.rect.center
                self.finalX3D, self.finalY3D = x, y
                self.finalX2D, self.finalY2D = self.prevX2D, self.prevY2D
        elif (self.charging and self.force > 40): 
            if (self.force < 75): 
                self.force = 75
            elif (self.force > 150): 
                self.force = 150
            vx = self.dx*self.force/(self.dx**2+self.dy**2)**0.5/15
            vy = self.dy*self.force/(self.dx**2+self.dy**2)**0.5/15
            newPuck = self.pucksGroup.sprites()[-1] # get latest puck object
            newPuck.updateMovement(vx, -vy, 10)
            self.newPuck, self.selected = None, False
            if (self.settings['audio']): 
                pygame.mixer.music.load(self.audios['shuffle'])
                pygame.mixer.music.play()
        self.charging, self.force = False, 0

    def keyPressed(self, keyCode, modifier): 
        if (keyCode == pygame.K_SPACE): 
            self.free = not self.free
            print('Shortcut activated!')

    @staticmethod
    def isCollided(puck1, puck2): 
        distance = ((puck1.x-puck2.x)**2+(puck1.y-puck2.y)**2)**0.5
        return distance <= Puck.SIZE

    def checkCollision(self): 
        seen = set()
        dict = pygame.sprite.groupcollide(self.movingPucks, self.pucksGroup, 
        False, False, MainGame.isCollided)
        for movingPuck in dict: 
            for other in dict[movingPuck]: 
                if (other != movingPuck and 
                    {movingPuck, other} not in self.collidedList): 
                    self.collidedList.append({movingPuck, other})
                    movingPuck.doCollision(other)
                    if (self.settings['audio']): 
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(self.audios['collide'])
                        pygame.mixer.music.play()

    def pucks3DUpdate(self): 
        for puck in self.pucksGroup: 
            puck3D = self.pucksDict[puck.id]
            puck3D.update(self, puck)

    def regroupPucks(self): 
        self.staticPucks.empty()
        self.movingPucks.empty()
        for puck in self.pucksGroup: 
            if (self.table.isOutofBound(puck.x, puck.y)): 
                self.pucksDict[puck.id].kill()
                puck.kill()
            elif (puck.ax != 0 or puck.ay != 0): 
                self.movingPucks.add(puck)
            else: 
                self.staticPucks.add(puck)

    def updatePlayers(self): 
        player1Score, player2Score = self.table.updateScore(self.pucksGroup)
        player1Pucks, player2Pucks = 0, 0
        for i in range(self.puckId, self.maxPucks): 
            if (i%2 == 0): 
                player1Pucks += 1
            else: 
                player2Pucks += 1
        self.redrawPlayerBoxes(player1Score, player2Score, 
        player1Pucks, player2Pucks)
        if (player1Pucks+player2Pucks == 0 and self.newPuck == None): 
            self.isOver = True
            self.drawGameOver(player1Score, player2Score)

    def selectPosition(self): 
        dx = random.randrange(-int(self.table3D.rect.width/3), 
        int(self.table3D.rect.width/3))
        _, minY = self.table3D.convertPoint(self, 0, Table.HEIGHT-Table.LINE2)
        x = self.table3D.rect.centerx+dx
        y = random.randrange(int(self.table3D.rect.top+minY+5), 
        int(self.table3D.rect.bottom-5))
        self.mouseReleased(x, y)

    def selectDirection(self): 
        newPuck = self.pucksGroup.sprites()[-1]
        x0, y0 = newPuck.x, newPuck.y
        if (random.choice([True, False])): 
            for puck in self.pucksGroup: 
                if (puck.id%2 == 0): # player's puck
                    self.dx = puck.x-x0+random.randrange(-int(Puck.SIZE), 
                    int(Puck.SIZE))
                    self.dy = puck.y-y0+random.randrange(-int(Puck.SIZE/8), 
                    int(Puck.SIZE/8))
                    self.force = random.randint(120, 140)
                    return
        # no player's puck on table or randomly choose False
        self.dx = self.table.rect.centerx-x0+random.randint(-int(2*Puck.SIZE), 
        int(2*Puck.SIZE))
        self.dy = self.table.rect.top-random.randint(0, int(Table.LINE2))-y0
        self.force = random.randint(100, 110)
        
    def shufflePuck(self): 
        self.charging = True
        self.mouseReleased(0, 0)

    def timerFired(self, dt): 
        if (self.isOver): 
            return
        self.regroupPucks()
        if (len(self.movingPucks) != 0): 
            self.checkCollision()
            self.movingPucks.update()
            self.pucks3DUpdate()
        else: 
            if (self.settings['audio']): 
                pygame.mixer.music.stop()
            self.collidedList = []
            self.updatePlayers()
            if (self.settings['pve'] and 
                self.puckId%2 == 1 and self.newPuck == None): 
                self.selectPosition()
                self.selectDirection()
                self.shufflePuck()            

    def redrawPlayerBoxes(self, score1, score2, pucks1, pucks2): 
        self.player1Points.updateText(str(score1))
        self.player2Points.updateText(str(score2))
        self.player1Remaining.updateText(f' * {pucks1}')
        self.player2Remaining.updateText(f' * {pucks2}')

    def drawGameOver(self, player1Score, player2Score): 
        if (player1Score > player2Score): 
            if (self.settings['pve']): 
                text = 'You Win'
            else: 
                text = 'Player1 Wins'     
        elif (player1Score < player2Score): 
            if (self.settings['pve']): 
                text = 'Computer Wins'
            else: 
                text = 'Player2 Wins'
        else: 
            text = 'Tie'
        fontSize = 60
        result = TextBox((self.player1.rect.centerx+
        self.player2.rect.centerx)/2, 
        self.player1Remaining.rect.bottom+fontSize, text, fontSize, True)
        self.boxesGroup.add(result)

    def draw2DArrow(self, screen): 
        fill = (255, max(255-self.force*2, 0), max(255-self.force*2, 0))
        table2DArrow = [
            (self.newPuck.rect.left, self.newPuck.rect.centery), 
            (self.newPuck.rect.right, self.newPuck.rect.centery), 
            (self.finalX2D, self.finalY2D)
        ]
        pygame.draw.polygon(screen, fill, table2DArrow)

    def draw3DArrow(self, screen): 
        fill = (255, max(255-self.force*2, 0), max(255-self.force*2, 0))
        newPuck3D = self.pucksDict[self.newPuck.id]
        table3DArrow = [
            (newPuck3D.rect.left, newPuck3D.rect.centery), 
            (newPuck3D.rect.right, newPuck3D.rect.centery), 
            (self.finalX3D, self.finalY3D)
        ]
        pygame.draw.polygon(screen, fill, table3DArrow)

    def drawTable(self, screen): 
        # edge
        pygame.draw.rect(screen, Table.EDGEFILL, self.tableEdge2)
        # botom
        pygame.draw.rect(screen, Table.BOTTOMFILL, self.tableEdge1)
        # table
        screen.blit(self.table.image, self.table.rect)
        # arrow
        if (self.charging): 
            self.draw2DArrow(screen)
        # pucks
        self.pucksGroup.draw(screen)

    def drawTable3D(self, screen): 
        [x0, x1, x2, x3, x4, x5, x6, x7] = self.table3DXs
        [y0, y1, y2, y3, y4, y5, y6, y7] = self.table3DYs
        backW, backH = x1-x0, y3-y1
        frontW, frontH = x7-x6, y7-y5
        # back edge
        pygame.draw.rect(screen, Table3D.EDGEFILL, 
        pygame.Rect(x0, y0, backW+1, backH+1))
        # bottom
        pygame.draw.polygon(screen, Table3D.BOTTOMFILL, 
        [(x2, y2), (x3, y3), (x7, y7), (x6, y6)])
        # table
        screen.blit(self.table3D.image, self.table3D.rect)
        screen.blit(self.table3D.frontImage, 
        (self.table3D.rect.left, self.table3D.rect.bottom))
        # left, right edges
        pygame.draw.polygon(screen, Table3D.SIDEFILL, 
        [(x0, y0), (x2, y2), (x6, y6), (x4, y4)])
        pygame.draw.polygon(screen, Table3D.SIDEFILL, 
        [(x1, y1), (x3, y3), (x7, y7), (x5, y5)])
        # arrow
        if (self.charging): 
            self.draw3DArrow(screen)
        # puck
        pucks3DList = sorted(self.pucks3DGroup.sprites(), 
        key = lambda puck3D: puck3D.y) 
        for puck3D in pucks3DList: # draw from farthest to closest
            screen.blit(puck3D.image, puck3D.rect) 
        # front edge
        pygame.draw.rect(screen, Table3D.EDGEFILL, pygame.Rect(x4, y4, 
        frontW+1, frontH+1))

    def redrawAll(self, screen): 
        # draw tables
        self.drawTable(screen)
        self.drawTable3D(screen)
        # draw buttons
        self.boxesGroup.draw(screen)