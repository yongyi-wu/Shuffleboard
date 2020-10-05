# __shuffleboard__.py

'''                               CITATION

0. pygame_framework.py is created by Lukas Peraza for 15-112 F15 Pygame Optional Lecture, 11/11/2015
1. Shuffleboard class imitates behaviors of ModalApp class in cmu_112_graphics.py
2. Puck images come from https://www.mccluretables.com/p-667-weights-2-516-custom-pucks-aluminum-caps-only.aspx
3. Table image comes from http://fotobg.ru/download/3200
4. Icon images come from https://www.iconfont.cn/collections/detail?spm=a313x.7781069.0.da5a778a4&cid=652
5. Audio comes from https://www.youtube.com/watch?v=jlAp96DRch8
6. Image and video processing was completed in Microsoft Powerpoint, Windows Paint 3D and Windows Video Editor
7. Audio processing was completed in https://www.mp3louder.com/ and https://audio-joiner.com/
8. I determined the dimension of shuffleboard table in accordance to https://www.shuffleboard.net/blog/how-to-build-a-shuffleboard-table/
9. The "projection equations" in https://codeincomplete.com/posts/javascript-racer-v1-straight/ 
    inspires convertTo3D() method in Table3D class. However, the "project" equations are actually
    problematic, but I debugged it. Also, I did not read ANY code on that website

'''


import pygame
from pygame_framework import PyGameFramework
from record_screen import Record
from main_game import MainGame
from splash_screen import SplashScreen
from help_screen import HelpScreen
from settings_screen import SettingsScreen

class Shuffleboard(PyGameFramework): 
    def init(self): 
        self.colors = ['red', 'blue', 'yellow', 'black']
        self.settings = {
            'player1': self.colors[0], 
            'player2': self.colors[1], 
            'audio': True, 
            'pve': None
        }
        self.initScreenController()
        self.splashScreen = SplashScreen(self)
        self.recordScreen = Record(self)
        self.mainGame = MainGame(self)
        self.helpScreen = HelpScreen(self)
        self.settingsScreen = SettingsScreen(self)

    def initScreenController(self): 
        self.isSplashScreen = True
        self.isRecordScreen = False
        self.isMainGame = False
        self.isHelpScreen = False
        self.isSettingsScreen = False

    def mouseMoved(self, x, y): 
        if (self.isSplashScreen): 
            self.splashScreen.mouseMoved(x, y)
        elif (self.isRecordScreen): 
            self.recordScreen.mouseMoved(x, y)
        elif (self.isMainGame): 
            self.mainGame.mouseMoved(x, y)
        elif (self.isHelpScreen): 
            self.helpScreen.mouseMoved(x, y)
        elif (self.isSettingsScreen): 
            self.settingsScreen.mouseMoved(x, y)

    def mousePressed(self, x, y): 
        if (self.isSplashScreen): 
            self.splashScreen.mousePressed(x, y)
        elif (self.isRecordScreen): 
            self.recordScreen.mousePressed(x, y)
        elif (self.isMainGame): 
            self.mainGame.mousePressed(x, y)
        elif (self.isHelpScreen): 
            self.helpScreen.mousePressed(x, y)
        elif (self.isSettingsScreen): 
            self.settingsScreen.mousePressed(x, y)

    def mouseDragged(self, x, y): 
        if (self.isSplashScreen): 
            pass
        elif (self.isRecordScreen): 
            pass
        elif (self.isMainGame): 
            self.mainGame.mouseDragged(x, y)
        elif (self.isHelpScreen): 
            pass
        elif (self.isSettingsScreen): 
            self.settingsScreen.mouseDragged(x, y)

    def mouseReleased(self, x, y): 
        if (self.isSplashScreen): 
            pass
        elif (self.isRecordScreen): 
            pass
        elif (self.isMainGame): 
            self.mainGame.mouseReleased(x, y)
        elif (self.isHelpScreen): 
            pass
        elif (self.isSettingsScreen): 
            self.settingsScreen.mouseReleased(x, y)

    def keyPressed(self, keyCode, modifier): 
        if (self.isSplashScreen): 
            pass
        elif (self.isRecordScreen): 
            pass
        elif (self.isMainGame): 
            self.mainGame.keyPressed(keyCode, modifier)
        elif (self.isHelpScreen): 
            pass
        elif (self.isSettingsScreen): 
            pass

    def timerFired(self, dt): 
        if (self.isSplashScreen): 
            pass
        elif (self.isRecordScreen): 
            pass
        elif (self.isMainGame): 
            self.mainGame.timerFired(dt)
        elif (self.isHelpScreen): 
            pass
        elif (self.isSettingsScreen): 
            pass

    def redrawAll(self, screen): 
        if (self.isSplashScreen): 
            self.splashScreen.redrawAll(screen)
        elif (self.isRecordScreen): 
            self.recordScreen.redrawAll(screen)
        elif (self.isMainGame): 
            self.mainGame.redrawAll(screen)
        elif (self.isHelpScreen): 
            self.helpScreen.redrawAll(screen)
        elif (self.isSettingsScreen): 
            self.settingsScreen.redrawAll(screen)

def main(): 
    Shuffleboard(width=1080, height=680).run()

if __name__ == '__main__': 
    main()