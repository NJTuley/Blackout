# Button object for all menus in the Blackout game

import pygame
import Colors

pygame.init()

class Button():


    def __init__(self, height = 0, width = 0, x = 0, y = 0, text = "", fill = (0,0,0), font = pygame.font.Font(None, 32), fontColor = (255,255,255)):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.text = text
        self.fill = fill
        self.font = font
        self.textColor = fontColor
        self.borderColor = Colors.white
        self.borderWidth = 0


    # check if the given x, y coordinate is within this button
    # @param x The x coordinate of the point being checked
    # @param y The y coordinate of the point being checked
    def inBounds(self, x, y):
        if((x > self.x and x < self.x + self.width) and (y > self.y and y < self.y + self.height)):
            return True
        else:
            return False
    def update(self, window):
        if(self.inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
            self.fill = Colors.white
            self.textColor = Colors.black
            self.borderColor = Colors.black
            self.borderWidth = 0
        else:
            self.fill = Colors.black
            self.textColor = Colors.white
            self.borderColor = Colors.white
            self.borderWidth = 5

        pygame.draw.rect(window, self.borderColor, pygame.Rect(self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(window, self.fill, pygame.Rect(self.x + self.borderWidth, self.y + self.borderWidth, self.width - 2 * self.borderWidth, self.height - 2 * self.borderWidth), 0)
        self.textRendered = self.font.render(self.text, False, self.textColor)
        window.blit(self.textRendered, [(self.width - self.textRendered.get_width()) * 0.5 + self.x, (self.height - self.textRendered.get_height()) * 0.5 + self.y])


    def setBorderColor(self, color):
        self.borderColor = color