
from ScoreItem import ScoreItem
import Colors
import Fonts
import HighScores


NUM_SCORES = 10

class HighScoreDisplay():

    scoreDisplays = []

    def __init__(self, x, y, width, height):
        fileName = "Assets/highscores.txt"
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.scoreBorderWidth = 4

        self.scoreTitle = Fonts.large.render("High Scores", False, Colors.white)

        HighScores.importScores(fileName)

        HighScores.sortScores()
        scores_len = len(HighScores.scores)

        for i in range(NUM_SCORES):

            if (scores_len <= NUM_SCORES and i >= scores_len):
                # populate any empty high score places
                timeVal = " - "
                nameVal = " - "
            elif (scores_len <=  NUM_SCORES and i < scores_len):
                timeVal = self.getTimeFormatted(HighScores.scores[i].time)
                nameVal = HighScores.scores[i].name
            else:
                raise Exception("Too many high scores imported")

            self.scoreDisplays.append(ScoreItem(nameVal, timeVal, self.x + self.scoreBorderWidth,
                                                self.y + self.scoreTitle.get_height() + ((self.scoreBorderWidth + (
                                                i * int(self.height / 10))) + self.scoreBorderWidth),
                                                self.width - 2 * self.scoreBorderWidth,
                                                self.height / 10 - 2 * self.scoreBorderWidth))


    def update(self, window):
        self.scoreDisplays.clear()
        scores_len = len(HighScores.scores)

        for i in range(NUM_SCORES):

            if (scores_len <= NUM_SCORES and i >= scores_len):
                # populate any empty high score places
                timeVal = " - "
                nameVal = " - "
            elif (scores_len <=  NUM_SCORES and i < scores_len):
                timeVal = self.getTimeFormatted(HighScores.scores[i].time)
                nameVal = HighScores.scores[i].name
            else:
                raise Exception("Too many high scores imported")

            self.scoreDisplays.append(ScoreItem(nameVal, timeVal, self.x + self.scoreBorderWidth,
                                                self.y + self.scoreTitle.get_height() + ((self.scoreBorderWidth + (
                                                i * int(self.height / 10))) + self.scoreBorderWidth),
                                                self.width - 2 * self.scoreBorderWidth,
                                                self.height / 10 - 2 * self.scoreBorderWidth))

        window.blit(self.scoreTitle, [self.x + (self.width / 2) - (self.scoreTitle.get_width() / 2), self.y])
        for i in range(len(self.scoreDisplays)):
            self.scoreDisplays[i].update(window, self.x + self.width)

    def getTimeFormatted(self, time):
        return (str(time[0]) + ":" + str(time[1]) + ":" + str(time[2]))



