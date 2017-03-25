
from HighScore import HighScore
from Difficulty import difficulties

easy_filename = "Assets/easy_scores.txt"
moderate_filename = "Assets/moderate_scores.txt"
hard_filename = "Assets/hard_scores.txt"
filenames = [easy_filename, moderate_filename, hard_filename]

easy_scores = []  # list to hold all the high scores of the player
moderate_scores = []
hard_scores = []
all_scores = [easy_scores, moderate_scores, hard_scores]
newHighScore = False

# sort the score numeric values that were given
def sortScores():
    for i in range(len(all_scores)):
        for k in range(len(all_scores[i])):
            for j in range(len(all_scores[i])):
                if (all_scores[i][k].time > all_scores[i][j].time):
                    temp = all_scores[i][k]
                    all_scores[i][k] = all_scores[i][j]
                    all_scores[i][j] = temp


def importScores(filename):
    num_high_scores = 10

    for k in range(len(all_scores)):
        all_scores[k].clear()
        file = open(filenames[k], 'r')

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

                all_scores[k].append(HighScore(name, score))  # append the new High Score the the list of high scores

        file.close()


# check if the time from the last game was a new record
def isBestScore(time, difficulty):
    for i in range(len(difficulties)):
        if(difficulty == difficulties[i]):
            max_score = len(all_scores[i]) - 1
            if (len(all_scores[i]) == 0 or len(all_scores[i]) < 10):
                return True
            if(time['minutes'] > all_scores[i][max_score].time[0]
               or (time['minutes'] == all_scores[i][max_score].time[0] and time['seconds'] > all_scores[i][max_score].time[1])
               or time['minutes'] == all_scores[i][max_score].time[0] and time['seconds'] == all_scores[i][max_score].time[1] and time['milliseconds'] > all_scores[i][max_score].time[2]):

                return True
            return False
    raise Exception("Invalid difficulty: " + str(difficulty))


def isHighScore(time, difficulty):
    max_score = 0
    for i in range(len(difficulties)):
        if(difficulty == difficulties[i]):
            if(len(all_scores[i]) == 0):
                return True
            if (time['minutes'] > all_scores[i][max_score].time[0]
                or (time['minutes'] == all_scores[i][max_score].time[0] and time['seconds'] > all_scores[i][max_score].time[1])
                or time['minutes'] == all_scores[i][max_score].time[0] and time['seconds'] == all_scores[i][max_score].time[1] and time[
                    'milliseconds'] > all_scores[i][max_score].time[2]):
                return True
            return False
    raise Exception("Invalid difficulty: " + str(difficulty.name))


def newHighScoreInsert(time, name, difficulty):
    for i in range(len(difficulties)):
        if(difficulty == difficulties[i]):
            max_score = len(all_scores[i]) - 1
            if (len(all_scores[i]) == 0 or time['minutes'] > all_scores[i][max_score].time[0]
                or (time['minutes'] == all_scores[i][max_score].time[0] and time['seconds'] > all_scores[i][max_score].time[1])
                or time['minutes'] == all_scores[i][max_score].time[0] and time['seconds'] == all_scores[i][max_score].time[1] and time[
                    'milliseconds'] > all_scores[i][max_score].time[2]):
                insertNewHighScore(time, max_score, name, difficulty)
                exportScoresToFile(difficulty)


# exports the high score data to a file in order to save data between gameplay sessions
def exportScoresToFile(difficulty):
    for j in range(len(difficulties)):
        if(difficulty == difficulties[j]):
            outFile = open(filenames[j], 'w')
            for i in range(len(all_scores[j])):
                outFile.write(all_scores[j][i].name + " " + str(all_scores[j][i].time[0]) + " " + str(all_scores[j][i].time[1]) + " " + str(all_scores[j][i].time[2]))
                if(i != len(all_scores[j]) - 1):
                    outFile.write('\n')

            outFile.close()

# insert a new high schore into the last at the specified index, pushing everything below the index down one space in the list (i.e. if index was 5, the item at index 3 would be pushed to index 4), shifting everything below the index down in the list
def insertNewHighScore(time, index, name, difficulty):
    for k in range(len(difficulties)):
        if difficulty == difficulties[k]:
            if(not len(all_scores[k]) < 10):
                min_score = []
                min_val = None
                for i in range(len(all_scores[k])):
                    if(i == 0):
                        # initial values set
                        min_score.append(all_scores[k][i].time[0])
                        min_score.append(all_scores[k][i].time[1])
                        min_score.append(all_scores[k][i].time[2])
                    else:
                        if(min_score[0] > all_scores[k][i].time[0]
                            or (min_score[0] == all_scores[k][i].time[0] and min_score[1] > all_scores[k][i].time[1])
                            or (min_score[0] == all_scores[k][i].time[0] and min_score[1] == all_scores[k][i].time[1] and min_score[2] > all_scores[k][i].time[2])):
                            min_score = all_scores[k][i].time
                            min_val = all_scores[k][i]

                if(min_val != None):
                    all_scores[k].remove(min_val)

            all_scores[k].append(HighScore(name, [time['minutes'], time['seconds'], int(time['milliseconds'] / 10)]))
            sortScores()