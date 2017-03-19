# class to show the help screen

import pygame
import Fonts
import Colors
from Button import Button

class helpScreen():
    text = ["OBJECTIVE: Do not be \"standing\" on a black tile",
            "as the tiles move around the board.",
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
        self.x = screen[0] * 0.04
        self.y = screen[1] * 0.2
        self.width = screen[0] * 0.92
        self.height = screen[1] * 0.6
        self.borderWidth = 10
        self.returnBtn = Button(50, self.width * 0.5, self.x + self.width * 0.25,  self.y + self.height * 0.9 + 25, "Return to Menu")

    def update(self, gameWindow):
        pygame.draw.rect(gameWindow, Colors.white, pygame.Rect((self.x - self.borderWidth, self.y - self.borderWidth), (self.width + self.borderWidth * 2, self.height + self.borderWidth * 2)))
        pygame.draw.rect(gameWindow, Colors.black, pygame.Rect((self.x, self.y), (self.width, self.height)))
        gameWindow.blit(self.title, ((self.x + self.width * 0.5 - self.title.get_width() * 0.5, self.y + self.height * 0.2 - self.title.get_height() * 0.5), (self.title.get_width(), self.title.get_height())))
        for i in range(len(self.text)):
            gameWindow.blit(self.renderedTxt[i], ((self.x + self.width * 0.5 - self.renderedTxt[i].get_width() * 0.5, self.y + self.height * 0.4 + self.renderedTxt[i].get_height() * i), (self.renderedTxt[i].get_width(), self.renderedTxt[i].get_height())))
        self.returnBtn.update(gameWindow)


