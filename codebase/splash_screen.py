# splash_screen.py
# view citations in __shuffleboard__.py

import pygame
import os, pickle
from main_game import MainGame
from boxes import *

class SplashScreen(object): 
    def __init__(self, game): 
        # basic setup
        self.game = game
        self.width = game.width
        self.height = game.height
        # texboxes and buttons
        self.boxesGroup = pygame.sprite.Group()
        self.initScreenObjects()

    def initScreenObjects(self): 
        fontSize = 100
        titleBox = TextBox(self.game.width/2, self.game.height*1/8, 
        'SHUFFLEBOARD', fontSize, True)
        authorBox = TextBox(titleBox.rect.right-fontSize/2, 
        titleBox.rect.bottom+fontSize/4, 'Created by Ethan Wu', fontSize/3)
        self.recordButton = Button(titleBox.rect.centerx, 
        authorBox.rect.bottom+fontSize/2, 'Record', fontSize/2, 
        url='image/icon/flag.png')
        self.pveButton = Button(self.recordButton.rect.centerx, 
        self.recordButton.rect.bottom+fontSize/2, 'PVE Mode', fontSize/2, 
        url='image/icon/play.png')
        self.pvpButton = Button(self.pveButton.rect.centerx, 
        self.pveButton.rect.bottom+fontSize/2, 'PVP Mode', fontSize/2, 
        url='image/icon/play.png')
        self.helpButton = Button(self.pvpButton.rect.centerx, 
        self.pvpButton.rect.bottom+fontSize/2, 'Help', fontSize/2, 
        url='image/icon/key.png')
        self.settingButton = Button(self.helpButton.rect.centerx, 
        self.helpButton.rect.bottom+fontSize/2, 'Settings', fontSize/2, 
        url='image/icon/settings.png')
        self.boxesGroup.add([titleBox, authorBox, self.recordButton, 
        self.pveButton, self.pvpButton, self.helpButton, self.settingButton])

    def mouseMoved(self, x, y): 
        self.boxesGroup.update(x, y)

    def mousePressed(self, x, y): 
        self.game.isSplashScreen = False
        if (self.recordButton.isSelected(x, y)): 
            self.game.isRecordScreen = True
            self.game.recordScreen.initScreenObjects()
        elif (self.pveButton.isSelected(x, y)): 
            tempSettings = self.game.settings
            self.game.settings['pve'] = True
            self.game.isMainGame = True
            self.game.mainGame = MainGame(self.game) # update MainGame
            self.game.settings = tempSettings
        elif (self.pvpButton.isSelected(x, y)): 
            tempSettings = self.game.settings
            self.game.settings['pve'] = False
            self.game.isMainGame = True
            self.game.mainGame = MainGame(self.game) # update MainGame
            self.game.settings = tempSettings
        elif (self.helpButton.isSelected(x, y)): 
            self.game.isHelpScreen = True
        elif (self.settingButton.isSelected(x, y)): 
            self.game.isSettingsScreen = True
        else: # does not select any button
            self.game.isSplashScreen = True

    def redrawAll(self, screen): 
        self.boxesGroup.draw(screen)
