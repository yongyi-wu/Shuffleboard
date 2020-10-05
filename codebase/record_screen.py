# record.py

import pygame
import os, pickle
from main_game import MainGame
from pucks import *
from boxes import *

class Record(object): 
    def __init__(self, game): 
        # basic setup
        self.game = game
        self.width = game.width
        self.height = game.height
        # texboxes and buttons
        self.boxesGroup = pygame.sprite.Group()
        self.initScreenObjects()

    def initScreenObjects(self): 
        fontSize = 80
        title = TextBox(self.game.width/2, self.game.height*1/10, 
        'Record', fontSize)
        temp = Button(0, 0, 'Record0', fontSize/2, url='image/icon/state.png')
        rows = int(self.height/temp.height/1.5)
        self.records = []
        count = 0
        for row in range(1, rows-1): 
            for col in [-1, 0, 1]: 
                count += 1
                if (count > len(os.listdir('record'))): 
                    break
                button = Button(title.rect.centerx+col*temp.width, 
                title.rect.bottom+1.5*row*temp.height, f'Record {count}', 
                fontSize/2, url='image/icon/state.png')
                self.records.append(button)
        fontSize = 100
        self.splashButton = Button(fontSize/2, self.height-fontSize/2, '', 
        fontSize/2, url='image/icon/home.png')
        self.boxesGroup.add([title, self.splashButton]+self.records)

    def unpackGameState(self, gameState): 
        game = self.game.mainGame
        game.settings = gameState['settings']
        print(game.settings)
        Puck.loadImage(game.settings)
        Puck3D.loadImage(game.settings)
        game.puckId = gameState['puckId']
        for id in gameState['pucks']: 
            puck = gameState['pucks'][id]
            x, y = puck['coordinate']
            newPuck = Puck(game, x, y, id)
            newPuck.t = puck['t']
            newPuck.ax, newPuck.ay = puck['acceleration']
            newPuck.vxMax, newPuck.vyMax = puck['speed'][0]
            newPuck.vx, newPuck.vy = puck['speed'][1]
            game.pucksGroup.add(newPuck)
            newPuck3D = Puck3D(game, newPuck)
            game.pucks3DGroup.add(newPuck3D)
            game.pucksDict[newPuck.id] = newPuck3D
        if (gameState['selected']): 
            game.selected = gameState['selected']
            game.newPuck = newPuck
        self.game.mainGame.initBoxes() # update boxes content

    def loadGameState(self, count): 
        filename = f'record/game_state{count}.txt'
        file1 = open(filename, 'rb')
        gameState = pickle.load(file1)
        self.unpackGameState(gameState)

    def mouseMoved(self, x, y): 
        self.boxesGroup.update(x, y)

    def mousePressed(self, x, y): 
        count = 0
        for record in self.records: 
            count += 1
            if (record.isSelected(x, y)): 
                self.game.isRecordScreen = False
                self.game.isMainGame = True
                self.game.mainGame = MainGame(self.game)
                self.loadGameState(count)
        if (self.splashButton.isSelected(x, y)): 
            self.game.isRecordScreen = False
            self.game.isSplashScreen = True

    def redrawAll(self, screen): 
        self.boxesGroup.draw(screen)