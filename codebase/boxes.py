# boxes.py
# view citations in __shuffleboard__.py

import pygame

class TextBox(pygame.sprite.Sprite): 
    COLOR = (44, 44, 44)
    FILL = (255, 255, 255)
    HOVERFILL = (200, 200, 200)

    def __init__(self, x, y, text, fontSize, bold=False, padding=10, url=None): 
        super().__init__()
        self.x, self.y = x, y
        self.url = url
        self.padding = padding
        self.font = pygame.font.SysFont('Courier New', int(fontSize), bold=bold)
        self.loadContent(text)
        if (self.url != None): 
            self.icon = pygame.transform.scale(pygame.image.load(self.url), 
            (self.height, self.height)).convert_alpha()
        self.drawContent(TextBox.FILL)   

    def loadContent(self, text): 
        self.textSurface = self.font.render(text, True, TextBox.COLOR)
        w, h = self.font.size(text)
        self.width = w+2*self.padding
        self.height = h+2*self.padding
        if (self.url != None): # contains icon
            self.width += self.height
            self.textRect = self.textSurface.get_rect(
            left=self.height+self.padding, centery=self.height/2)
        else: 
            self.textRect = self.textSurface.get_rect(center=(self.width/2, 
            self.height/2))
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.updateRect()

    def updateRect(self): # x, y refer to the center of the box
        self.rect = pygame.Rect(self.x-self.width/2, self.y-self.height/2, 
        self.width, self.height)

    def drawContent(self, fill): 
        self.image.fill(fill)
        if (self.url != None): 
            self.image.blit(self.icon, (self.padding, 0, self.height, 
            self.height))
        self.image.blit(self.textSurface, self.textRect)

    def isSelected(self, x, y): 
        if (self.rect.collidepoint(x, y)): 
            self.drawContent(TextBox.FILL) # reset to default
            return True
        else: 
            return False

    def updateText(self, text): 
        self.loadContent(text)
        self.drawContent(TextBox.FILL)






class Button(TextBox): 
    def __init__(self, x, y, text, fontSize, bold=False, padding=10, url=None): 
        super().__init__(x, y, text, fontSize, bold, padding, url)
        if (len(text) != 0): # contains text
            self.width = max(self.width, self.height*4.5) # standardizing size
            self.image = pygame.Surface((self.width, 
            self.height)).convert_alpha()
        self.drawContent(TextBox.FILL)
        self.updateRect()
        
    def update(self, x, y): 
        if (self.isSelected(x, y)): 
            self.drawContent(TextBox.HOVERFILL)
        else: 
            self.drawContent(TextBox.FILL)





class Option(pygame.sprite.Sprite): 
    def __init__(self, x, y, size, color): 
        super().__init__()
        self.size = size
        self.color = color
        self.image = pygame.transform.scale(
        pygame.image.load(f'image/puck_{color}.png'), (self.size, self.size)
        ).convert_alpha()
        self.updateRect(x, y)
        self.selected = False

    def updateRect(self, x, y): 
        self.rect = pygame.Rect(x-self.size/2, y-self.size/2, 
        self.size, self.size)

    def isSelected(self, x, y): 
        return self.rect.collidepoint(x, y)

    def changePosition(self, x, y): 
        self.updateRect(x, y)