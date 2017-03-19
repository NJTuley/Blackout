
from HighScore import HighScore

scores = []  # list to hold all the high scores of the player
newHighScore = False

# sort the score numeric values that were given
def sortScores():
    for i in range(len(scores)):
        for j in range(len(scores)):
            if (scores[i].time > scores[j].time):
                temp = scores[i]
                scores[i] = scores[j]
                scores[j] = temp


def importScores(filename):
    file = open(filename, 'r')
    num_high_scores = 10

    scores.clear()

    for i in range(num_high_scores):
        line = file.readline()
        line = line.split()
        if (line):
            score = []
            name = ""
            for i in range(len(line)):
                if(i == 0):
                    name = line[i]
                else:
                    score.append(int(line[i]))

            scores.append(HighScore(name, score))  # append the new High Score the the list of high scores

    file.close()


# check if the time from the last game was a new record
def isHighScore(time):
    max_score = len(scores) - 1

    if(time['minutes'] > scores[max_score].time[0]
       or (time['minutes'] == scores[max_score].time[0] and time['seconds'] > scores[max_score].time[1])
       or time['minutes'] == scores[max_score].time[0] and time['seconds'] == scores[max_score].time[1] and time['milliseconds'] > scores[max_score].time[2]):

        return True
    return False


def isBestScore(time):
    max_score = 0

    if (time['minutes'] > scores[max_score].time[0]
        or (time['minutes'] == scores[max_score].time[0] and time['seconds'] > scores[max_score].time[1])
        or time['minutes'] == scores[max_score].time[0] and time['seconds'] == scores[max_score].time[1] and time[
            'milliseconds'] > scores[max_score].time[2]):
        return True
    return False


def newHighScoreInsert(time, name):
    max_score = len(scores) - 1
    if (time['minutes'] > scores[max_score].time[0]
        or (time['minutes'] == scores[max_score].time[0] and time['seconds'] > scores[max_score].time[1])
        or time['minutes'] == scores[max_score].time[0] and time['seconds'] == scores[max_score].time[1] and time[
            'milliseconds'] > scores[max_score].time[2]):
        insertNewHighScore(time, max_score, name)
        exportScoresToFile()


# exports the high score data to a file in order to save data between gameplay sessions
def exportScoresToFile():
    outFile = open("Assets/highscores.txt", 'w')

    for i in range(len(scores)):
        outFile.write(scores[i].name + " " + str(scores[i].time[0]) + " " + str(scores[i].time[1]) + " " + str(scores[i].time[2]))
        if(i != len(scores) - 1):
            outFile.write('\n')

    outFile.close()

# insert a new high schore into the last at the specified index, pushing everything below the index down one space in the list (i.e. if index was 5, the item at index 3 would be pushed to index 4), shifting everything below the index down in the list
def insertNewHighScore(time, index, name):
    if(not len(scores) < 10):
        min_score = []
        min_val = None
        for i in range(len(scores)):
            if(i == 0):
                # initial values set
                min_score.append(scores[i].time[0])
                min_score.append(scores[i].time[1])
                min_score.append(scores[i].time[2])
            else:
                if(min_score[0] > scores[i].time[0]
                    or (min_score[0] == scores[i].time[0] and min_score[1] > scores[i].time[1])
                    or (min_score[0] == scores[i].time[0] and min_score[1] == scores[i].time[1] and min_score[2] > scores[i].time[2])):
                    min_score = scores[i].time
                    min_val = scores[i]

        if(min_val != None):
            scores.remove(min_val)

    scores.append(HighScore(name, [time['minutes'], time['seconds'], int(time['milliseconds'] / 10)]))
    sortScores()