# class that formats high score output (this object formats a single high score, and this object will be placed in a table-like format in the HighScoreDisplay class

import Colors
import Fonts
import pygame

class ScoreItem():


    def __init__(self, index, score, x, y, width, height):
        self.score = score
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = index


    # @param rightBorder the right edge of the rectangle object that contains this ScoreItem
    def update(self, window, rightBorder):
        # draw the rectangles that will "hold" all the data about the score
        pygame.draw.rect(window, Colors.white, pygame.Rect((self.x, self.y), (self.width, self.height)), 0)  # the filled rectangle
        pygame.draw.rect(window, Colors.black, pygame.Rect((self.x, self.y), (self.width, self.height)), 1)  # a border around the rectange/row holding the score info

        self.scoreText = Fonts.standard.render(str(self.score), False, Colors.black)
        window.blit(self.scoreText, ((rightBorder) - (self.scoreText.get_width() + 40), self.y + (self.height / 2) - (self.scoreText.get_height() / 2)))
        window.blit(Fonts.standard.render(self.name, False, Colors.black), (self.x + 40, self.y + self.height / 2 - self.scoreText.get_height() / 2))
