# help_screen.py

import pygame
from boxes import *

class HelpScreen(object): 
    def __init__(self, game): 
        # basic setup
        self.game = game
        self.width = game.width
        self.height = game.height
        # texboxes and buttons
        self.boxesGroup = pygame.sprite.Group()
        self.initScreenObjects()

    def initScreenObjects(self): 
        # buttons
        fontSize = 80
        title = TextBox(self.game.width/2, self.game.height*1/10, 'Help', 
        fontSize)
        self.splashButton = Button(fontSize/2, self.height-fontSize/2, '', 
        fontSize/2, url='image/icon/home.png')
        # instructions
        fontSize = int(self.width/40)
        line1 = TextBox(self.game.width/2, title.rect.bottom+fontSize*2, 
        'Click the table to put down a puck before the green line', 
        fontSize, url='image/icon/cursor.png')
        line2 = TextBox(self.game.width/2, line1.rect.bottom+fontSize*1.5, 
        'Select and drag the puck to determine direction and speed', 
        fontSize, url='image/icon/mouse.png')
        line3 = TextBox(self.game.width/2, line2.rect.bottom+fontSize*1.5, 
        'Avoid falling of the table while approaching scoring region', 
        fontSize, url='image/icon/bell.png')
        line4 = TextBox(self.game.width/2, line3.rect.bottom+fontSize*1.5, 
        'You may knock out other pucks on the table', 
        fontSize, url='image/icon/check.png')
        line5 = TextBox(self.game.width/2, line4.rect.bottom+fontSize*1.5, 
        'Player who receives higher points will win the game', 
        fontSize, url='image/icon/stat.png')
        self.boxesGroup.add([title, self.splashButton, line1, line2, line3, 
        line4, line5])

    def mouseMoved(self, x, y): 
        self.boxesGroup.update(x, y)

    def mousePressed(self, x, y): 
        if (self.splashButton.isSelected(x, y)): 
            self.game.isHelpScreen = False
            self.game.isSplashScreen = True

    def redrawAll(self, screen): 
        self.boxesGroup.draw(screen)