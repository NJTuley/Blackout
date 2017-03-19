# The Main Menu object for the Blackout game

from PulseAnimation import PulseAnimation
from Button import Button
from Menu import Menu
import Colors
import Fonts
import pygame


class MainMenu(Menu):
    options = []  # list holding all menu options (buttons)
    options_txt = [
        "Start Game",
        "How To Play",
        "Exit"
    ]
    title = Fonts.largeTitle.render("BLACKOUT", False, Colors.white)

    def __init__(self, windowWidth, windowHeight):
        super(Menu, self).__init__()
        self.width = windowWidth
        self.height = windowHeight
        self.numButtons = len(self.options_txt)
        buttonHeight = 50
        buttonWidth = windowWidth * 0.3
        buttonX = (windowWidth * 0.5) - (buttonWidth * 0.5)
        buttonStartY = windowWidth * 0.3 + self.title.get_height() + 100  # starting point for the buttons
        buttonYOffset = buttonHeight + 20

        self.titleAnimationCreated = False

        for i in range(len(self.options_txt)):
            self.options.append(Button(buttonHeight, buttonWidth, buttonX, buttonStartY + buttonYOffset * i, self.options_txt[i], (255, 255, 255), Fonts.standard, (0, 0, 0)))


    # starts the animation for the main menu title
    def startTitleAnimation(self, window):
        self.titleAnimationCreated = True
        # testing animation animation = MinMaxLoopAnimation('square', [i for i in range(int(screen['width'] / 2), int(screen['width'] / 2 + 1))], [i for i in range(int(screen['height'] / 2), int(screen['height'] / 2 + 1))], [i for i in range(50, 251)], [i for i in range(50, 251)], [i for i in range(0, 120)], [i for i in range(0, 256)], [i for i in range(0, 20)], 1000, 3)
        animation_border_width = 35
        animation_max_width = int(self.title.get_width() + 2 * animation_border_width)
        animation_max_height = int(self.title.get_height() + 2 * animation_border_width)
        self.titleAnimation = PulseAnimation('rectangle',
                                             [i for i in range(int((self.width * 0.5) - (self.title.get_width() * 0.5)),
                                                               int((self.width * 0.5) - (self.title.get_width() * 0.5) + 1) + 1)],
                                             [i for i in range(int((self.height * 0.3) - (self.title.get_height() * 0.5)),
                                                               int((self.height * 0.3) - (self.title.get_height() * 0.5)) + 1)],
                                             [i for i in range(int(animation_max_width - 2 * animation_border_width), int(animation_max_width - 2 * animation_border_width) + 1)],
                                             [i for i in range(int(animation_max_height - 2 * animation_border_width), int(animation_max_height - 2 * animation_border_width) + 1)],
                                             [i for i in range(0, 1)],
                                             [i for i in range(0, 256)],
                                             [i for i in range(1, animation_border_width + 1)], 15, 1)

        # set the bounds for the animation so that it can align properly around the title text
        self.titleAnimation.setParentBounds(
            int((self.width * 0.5) - (self.title.get_width() * 0.5)),  # left bound
            int((self.width * 0.5) - (self.title.get_width() * 0.5) + self.title.get_width() + 15),  # right bound
            int((self.height * 0.3) - (self.title.get_height() * 0.5)),  # top bound
            int((self.height * 0.3) - (self.title.get_height() * 0.5) + self.title.get_height())  # bottom bound
            )


    # runs the animation for the main menu title (shows a pulsing rectangle around the title text
    def runTitleAnimation(self, window):
        window.fill(Colors.black)
        self.titleAnimation.iterate()
        self.titleAnimation.update(window, 'center')
        self.show(window, False)


    def show(self, window, fillWindow):
        if (fillWindow):  # check whether or not you need to fill the window this time or not
            window.fill(Colors.black)
        window.blit(self.title, ((self.width * 0.5) - (self.title.get_width() * 0.5), (self.height * 0.3) - (self.title.get_height() * 0.5)))
        for i in range(len(self.options)):
            self.options[i].update(window)