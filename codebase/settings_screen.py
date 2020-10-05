# settings_screen.py

import pygame
from main_game import MainGame
from boxes import *

class SettingsScreen(object): 
    def __init__(self, game): 
        # basic setup
        self.game = game
        self.width = game.width
        self.height = game.height
        # texboxes and buttons
        self.boxesGroup = pygame.sprite.Group()
        self.pucksList = []
        self.initScreenObjects()

    def initScreenObjects(self): 
        # title
        fontSize = 80
        title = TextBox(self.game.width/2, self.game.height*1/10, 
        'Settings', fontSize)
        # "choose color" section
        player = TextBox(self.game.width/5, title.rect.bottom+fontSize/2, 
        '* Choose color: ', fontSize/2, True)
        player1 = TextBox(self.game.width/5, player.rect.bottom+fontSize/1.5, 
        'Player 1', fontSize/2)
        self.player1Box = TextBox(player1.rect.right+fontSize, 
        player1.rect.centery, '', fontSize*1.5, url='image/icon/box.png')
        player2 = TextBox(self.game.width*3/5, player.rect.bottom+fontSize/1.5, 
        'Player 2', fontSize/2)
        self.player2Box = TextBox(player2.rect.right+fontSize, 
        player2.rect.centery, '', fontSize*1.5, url='image/icon/box.png')
        self.boxList = []
        self.pucksList = []
        x = self.game.width/8
        for color in self.game.colors: 
            box = TextBox(x, self.player1Box.rect.bottom+fontSize/1.5, 
            '', fontSize*1.5, url='image/icon/box.png')
            boxName = TextBox(box.rect.centerx, box.rect.bottom, 
            color, fontSize/3)
            puck = Option(x, self.player1Box.rect.bottom+fontSize/1.5, 
            fontSize, color)
            self.boxList.append([box, boxName])
            self.pucksList.append(puck)
            x += fontSize*2
        # "audio" section
        audio = TextBox(self.game.width/5, boxName.rect.bottom+fontSize/2, 
        '* Audio effect: ', fontSize/2, True)
        self.audioTrue = Button(audio.rect.right+fontSize/2, 
        audio.rect.centery, '', fontSize/2, url='image/icon/sound_plus.png')
        self.audioFalse = Button(audio.rect.right+fontSize/2, 
        audio.rect.centery, '', fontSize/2, url='image/icon/sound_minus.png')
        fontSize = 100
        self.splashButton = Button(fontSize/2, self.height-fontSize/2, 
        '', fontSize/2, url='image/icon/home.png')
        self.boxesGroup.add(self.boxList+[self.player1Box, self.player2Box]+
        [title, player, player1, player2, audio, self.splashButton]+
        self.pucksList)
        # display according to the settings
        self.showSettings()

    def showSettings(self): 
        for i in range(len(self.pucksList)): 
            puck = self.pucksList[i]
            if (self.game.settings['player1'] == puck.color): 
                puck.rect.center = self.player1Box.rect.center
            elif (self.game.settings['player2'] == puck.color): 
                puck.rect.center = self.player2Box.rect.center
            else: 
                puck.rect.center = self.boxList[i][0].rect.center
        if (self.game.settings['audio']): 
            self.boxesGroup.add(self.audioTrue)
            self.boxesGroup.remove(self.audioFalse)
        else: 
            self.boxesGroup.add(self.audioFalse)
            self.boxesGroup.remove(self.audioTrue)
            
    def mouseMoved(self, x, y): 
        self.boxesGroup.update(x, y)

    def mousePressed(self, x, y): 
        for option in self.pucksList[::-1]: 
            if (option.isSelected(x, y)): 
                option.selected = True
                return
        if (self.audioTrue.isSelected(x, y) or 
            self.audioFalse.isSelected(x, y)): 
            self.game.settings['audio'] = not self.game.settings['audio']
        elif (self.splashButton.isSelected(x, y)): 
            self.game.isSettingsScreen = False
            self.game.isSplashScreen = True

    def mouseDragged(self, x, y): 
        for option in self.pucksList[::-1]: 
            if (option.selected): 
                option.updateRect(x, y)
                return

    def mouseReleased(self, x, y): 
        for option in self.pucksList[::-1]: 
            if (option.selected and 
                pygame.sprite.collide_rect(option, self.player1Box)): 
                self.game.settings['player1'] = option.color
            elif (option.selected and 
                  pygame.sprite.collide_rect(option, self.player2Box)): 
                self.game.settings['player2'] = option.color
            option.selected = False
        self.showSettings()

    def redrawAll(self, screen): 
        self.boxesGroup.draw(screen)