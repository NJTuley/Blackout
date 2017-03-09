
from ScoreItem import ScoreItem
import Colors
import Fonts

scores = []


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

        importScores(fileName)

        self.sortScores()

        for i in range(len(scores)):
            self.scoreDisplays.append(ScoreItem(i, self.getTimeFormatted(scores[i]), self.x + self.scoreBorderWidth, self.y + self.scoreTitle.get_height() + ((self.scoreBorderWidth + (i * int(self.height / 10))) + self.scoreBorderWidth), self.width - 2 * self.scoreBorderWidth, self.height / len(scores) - 2 * self.scoreBorderWidth))


    def update(self, window):
        self.scoreDisplays.clear()
        for i in range(len(scores)):
            self.scoreDisplays.append(ScoreItem(i, self.getTimeFormatted(scores[i]), self.x + self.scoreBorderWidth, self.y + self.scoreTitle.get_height() + ((self.scoreBorderWidth + (i * int(self.height / 10))) + self.scoreBorderWidth), self.width - 2 * self.scoreBorderWidth, self.height / len(scores) - 2 * self.scoreBorderWidth))

        window.blit(self.scoreTitle, [self.x + (self.width / 2) - (self.scoreTitle.get_width() / 2), self.y])
        for i in range(len(self.scoreDisplays)):
            self.scoreDisplays[i].update(window, self.x + self.width)


    # sort the score numeric values that were given
    def sortScores(self):
        for i in range(len(scores)):
            for j in range(len(scores)):
                if(scores[i] > scores[j]):
                    temp = scores[i]
                    scores[i] = scores[j]
                    scores[j] = temp


    def getTimeFormatted(self, time):
        return (str(time[0]) + ":" + str(time[1]) + ":" + str(time[2]))


def resetScores():
    scores =[]


def importScores(filename):
    file = open(filename, 'r')
    num_high_scores = 10

    scores.clear()

    for i in range(num_high_scores):
        line = file.readline()
        line = line.split()
        if(line):
            scores.append([int(i) for i in line])

    file.close()
