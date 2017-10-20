from Button import Button
import Colors
import Fonts
import pygame
from GameOverSpinnerAnimation import GameOverSpinnerAnimation
from HighScoreDisplay import HighScoreDisplay

class GameOverScreen():
    options = []
    options_txt = [
        'Play Again',
        'Main Menu'
    ]
    animationDone = False

    def __init__(self, screen, difficulty_index):
        self.counter = 0
        self.max_color_num = int(255 * 0.3)  # maximum color value for background
        self.text_color_min = int(255 * 0.3)  # minimum color value for text
        self.text_color = self.text_color_min
        for i in range(len(self.options_txt)):  # create the buttons for this screen
            self.options.append(Button(50, screen[1] * 0.25, (screen[0] * 0.6), (screen[1] * 0.6 + i * 80), self.options_txt[i], Colors.white, Fonts.standard, Colors.black))
        self.spinner = GameOverSpinnerAnimation(screen, 255)
        self.gameOverTxt = Fonts.title.render("You Blacked Out...", False, (self.text_color, self.text_color, self.text_color))
        self.highScores = HighScoreDisplay((screen[0] * 0.5 - self.gameOverTxt.get_width() / 2), (screen[1] * 0.1 + self.gameOverTxt.get_height() + 20), (screen[0] * 0.4), (screen[1] * 0.6), difficulty_index)


    def update(self, window, screen, time, difficulty_index):
        self.bg_color = Colors.black[0]
        self.text_color = Colors.white[0]


        window.fill(Colors.black)
        self.gameOverTxt = Fonts.title.render("You Blacked Out...", False, (self.text_color, self.text_color, self.text_color))
        window.blit(self.gameOverTxt, [(screen[0] - self.gameOverTxt.get_width()) * 0.5, (screen[1] - self.gameOverTxt.get_height()) * 0.075])


        # show the buttons on this screen
        for i in range(len(self.options)):
            self.options[i].update(window)

        # show the high scores on this screen
        self.highScores.update(window, difficulty_index)

        self.spinner.update(window)
        self.displayTime(time, window, screen)

    # show the player their time on the last game they played (must have been played since the game was opened)
    def displayTime(self, gameplay_time, gameWindow, screen):
        minutes = ""
        seconds = ""
        milliseconds = ""
        if (gameplay_time['minutes'] < 10):
            minutes = '0' + str('%.0f' % gameplay_time['minutes'])
        else:
            minutes = str('%.0f' % gameplay_time['minutes'])
        if (gameplay_time['seconds'] < 10):
            seconds = '0' + str('%.0f' % gameplay_time['seconds'])
        else:
            seconds = str('%.0f' % gameplay_time['seconds'])
        if (gameplay_time['milliseconds'] / 10 < 10):
            milliseconds = '0' + str('%.0f' % (gameplay_time['milliseconds'] / 10))
        else:
            milliseconds = str('%.0f' % (gameplay_time['milliseconds'] / 10))

        self.stopWatchDisplay = Fonts.standard.render(("Your Time - " + minutes + ":" + seconds + ":" + milliseconds), False, Colors.white)
        gameWindow.blit(self.stopWatchDisplay, (
        (screen[0] * 0.8 + self.stopWatchDisplay.get_width()) * 0.5, (screen[1] * 0.7 - self.stopWatchDisplay.get_height()) * 0.5))