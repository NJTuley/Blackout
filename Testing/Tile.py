import Error
import pygame

TILE_HEIGHT = 100
TILE_WIDTH = 100

class Tile(object):
    value = ''
    fill_color = (0,0,0)
    border_color = (0,0,0)
    border_width = 0
    height = TILE_HEIGHT
    width = TILE_WIDTH
    x = 0
    y = 0

    def __init__(self, value = 'x', x = 0, y = 0, height = 0, width = 0, fill = (255, 255, 255), border_color = (0,0,0), border_width = 10):
        print("ADD INPUT VALIDATION FOR CONSTRUCTOR VALUES")
        self.value = value
        self.height = height
        self.width = width
        self.fill_color = fill
        self.border_color = border_color
        self.border_width = border_width
        self.x = x
        self.y = y

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setHeight(self, height):
        if(height >= 0):
            self.height = height
        else:
            raise Error("Invalid Height", "Height must be greater than or equal to 0")

    def getHeight(self):
        return self.height

    def setWidth(self, width):
        if(width >= 0):
            self.width = width
        else:
            raise Error("Invalid Width", "Width must be greater than or equal to 0")

    def setFillColor(self, color):
        self.fill_color = color

    def getFillColor(self):
        return self.fill_color

    def setBorderColor(self, color):
        self.border_color = color

    def getBorderColor(self):
        return self.border_color

    def setBorderWidth(self, width):
        if(width >= 0):
            self.border_width = width
        else:
            raise Error("Invalid Border Width", "Border width must be >= 0")

    def update(self):
        if (self.value == 2):
            self.fill_color = (255, 255, 255)
        elif (self.value == 1):
            self.fill_color = (170, 170, 170)
        elif (self.value == 0):
            self.fill_color = (85, 85, 85)
        else:
            self.fill_color = (0, 0, 0)