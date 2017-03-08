# menu shown when player pauses the game

import pygame
import Colors
import Fonts
from Menu import Menu
from Button import Button

class PauseMenu(Menu):
    options = []
    options_txt = [
        'Resume',
        'Return To Main Menu'
    ]

    title = Fonts.title.render("PAUSED", False, Colors.white)

    def __init__(self, height = 0, width = 0):
        super(Menu, self).__init__()
        self.height = height
        self.width = width

        for i in range(len(self.options_txt)):
            #self, height = 0, width = 0, x = 0, y = 0, text = "", fill = (0,0,0), font = pygame.font.Font(None, 32), fontColor = (255,255,255)
            self.options.append(Button(50, 300, (self.width * 0.5) - 150, (self.height * 0.5) + i * 70, self.options_txt[i], Colors.white, Fonts.standard, Colors.black))
