import pygame
import Colors
import Fonts
from PulseAnimation import PulseAnimation

class TextField:


    def __init__(self, label, screen):
        self.label = label
        self.screen = screen  # this will hold the object that holds the textfield

        self.width = int(self.screen[0] * 0.8)
        self.height = int(self.screen[1] * 0.2)
        self.center()

        self.bg_color = Colors.black  # background color of the text field
        self.txtfield_color = Colors.white  # color of the textfield input area
        self.txtincolor = Colors.black  # color of text the player will be typing
        self.lbltxtcolor = Colors.white  # color of text of the label of the text field
        self.borderColor = Colors.white
        self.borderWidth = 20
        #def __init__(self, shape, xRange, yRange, heightRange, widthRange, fillRange, borderColorRange, borderWidthRange, duration = 1, numFullCycles = 0, connectedObjectBounds = None):
        self.pulser = PulseAnimation('rectangle',
                                     [i for i in range(self.x, self.x + 1)],
                                     [i for i in range(self.y, self.y + 1)],
                                     [i for i in range(self.height, self.height + 1)],
                                     [i for i in range(self.width, self.width + 1)],
                                     [i for i in range(0, 1)],
                                     [i for i in range(0, 255)],
                                     [i for i in range(0, self.borderWidth)],
                                     120, 1,
                                     {
                                         'left': self.x,
                                         'right': self.x + self.width,
                                         'top': self.y,
                                         'bottom': self.y + self.height
                                     })
        self.nameIn = "(3 characters maximum)"



    def center(self):
        self.x = int(self.screen[0] * 0.5 - self.width * 0.5)
        self.y = int(self.screen[1] * 0.5 - self.height * 0.5)


    def update(self, gameWindow):
        self.inputBox = pygame.Rect((self.x + self.width * 0.05, self.y + self.height * 0.4),  # the box that will "hold" the user input
                                    (self.width * 0.9, self.height * 0.4))
        self.center()
        pygame.draw.rect(gameWindow, self.borderColor, pygame.Rect((self.x - self.borderWidth, self.y - self.borderWidth), (self.width + 2* self.borderWidth, self.height + 2 * self.borderWidth)))
        pygame.draw.rect(gameWindow, self.borderColor, pygame.Rect((self.x, self.y), (self.width, self.height)))
        #pygame.draw.rect(gameWindow, self.bg_color, pygame.Rect((self.x, self.y), (self.width, self.height)))
        self.pulser.iterate()
        self.pulser.update(gameWindow, 'center')
        pygame.draw.rect(gameWindow, self.txtfield_color, self.inputBox)
        self.lblDraw = Fonts.standard.render(self.label, False, self.lbltxtcolor)
        self.nameShow = Fonts.standard.render(self.nameIn, False, self.txtincolor)
        gameWindow.blit(self.lblDraw, [self.x  + self.width * 0.5 - self.lblDraw.get_width() * 0.5, self.y + self.height * 0.175 - self.lblDraw.get_height() * 0.5])
        gameWindow.blit(self.nameShow, [self.x + self.width * 0.5 - self.nameShow.get_width() * 0.5, self.y + self.height * 0.6 - self.nameShow.get_height() * 0.5])