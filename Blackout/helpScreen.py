# class to show the help screen

import pygame
import Fonts
import Colors
from Button import Button
from PulseAnimation import PulseAnimation

class helpScreen():
    text = ["OBJECTIVE:",
            "Do not be \"standing\" on a black tile",
            "as the tiles move around the board.",
            "",
           "-Use the mouse to move",
           "-Press P to pause the game",
           "-Press R to restart the game",
           "-Press Esc to return to main menu"]
    #def __init__(self, height = 0, width = 0, x = 0, y = 0, text = "", fill = (0,0,0), font = pygame.font.Font(None, 32), fontColor = (255,255,255)):
    renderedTxt = []
    for i in range(len(text)):
        renderedTxt.append(Fonts.medLarge.render(text[i], False, Colors.white))
    title = Fonts.title.render("How To Play", False, Colors.white)

    # @param screen The screen that this help screen is being displayed on
    def __init__(self, screen):
        self.x = int(screen[0] * 0.05)
        self.y = int(screen[1] * 0.1)
        self.width = int(screen[0] * 0.9)
        self.height = int(screen[1] * 0.8)
        self.borderWidth = 10
        self.returnBtn = Button(50, self.width * 0.5, self.x + self.width * 0.25,  self.y + self.height - 25, "Return to Menu")
        #, shape, xRange, yRange, heightRange, widthRange, fillRange, borderColorRange, borderWidthRange, duration = 1, numFullCycles = 0, connectedObjectBounds = None):
        self.borderPulse = PulseAnimation('rectangle',
                                          [i for i in range(self.x, self.x + 1)],
                                          [i for i in range(self.y, self.y + 1)],
                                          [i for i in range(self.height, self.height + 1)],
                                          [i for i in range(self.width, self.width + 1)],
                                          [i for i in range(0, 1)],
                                          [i for i in range(0, 255)],
                                          [i for i in range(0, int(screen[0] * 0.05))],
                                          15, 1,
                                          {
                                              'left': self.x,
                                              'right': self.x + self.width,
                                              'top': self.y,
                                              'bottom': self.y + self.height
                                          })

    def update(self, gameWindow):
        pygame.draw.rect(gameWindow, Colors.white, pygame.Rect((self.x - self.borderWidth, self.y - self.borderWidth), (self.width + self.borderWidth * 2, self.height + self.borderWidth * 2)))
        self.borderPulse.iterate()
        self.borderPulse.update(gameWindow, 'center')
        pygame.draw.rect(gameWindow, Colors.black, pygame.Rect((self.x, self.y), (self.width, self.height)))
        gameWindow.blit(self.title, ((self.x + self.width * 0.5 - self.title.get_width() * 0.5, self.y + self.height * 0.2 - self.title.get_height() * 0.5), (self.title.get_width(), self.title.get_height())))
        for i in range(len(self.text)):
            gameWindow.blit(self.renderedTxt[i], ((self.x + self.width * 0.5 - self.renderedTxt[i].get_width() * 0.5, self.y + self.height * 0.35 + self.renderedTxt[i].get_height() * i), (self.renderedTxt[i].get_width(), self.renderedTxt[i].get_height())))
        self.returnBtn.update(gameWindow)


