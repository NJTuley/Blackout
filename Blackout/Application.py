# application class to handle the actual running of the Blackout game application

import pygame

pygame.init()

from Player import Player
from Song import Song
import Colors
import Fonts
from Board import Board
from Board import numTilesAhead
import random
from MainMenu import MainMenu
from PauseMenu import PauseMenu
from GameOverScreen import GameOverScreen
from HighScoreDisplay import scores
from PulseAnimation import PulseAnimation
from HighScoreDisplay import importScores

class Application():
    pygame.mixer.set_num_channels(2)  # set the maximum number of channels of playback that are allowed for audio
    songPlayback = pygame.mixer.Channel(0)  # the channel that will play the background music for the game during play

    # list of songs that will be played as background music during active gameplay (not during menus)
    songs = [
        Song("Assets/Music/Tobu - Seven.wav", "Seven", "Tobu", (3, 54)),
        Song("Assets/Music/Tobu - Hope.wav", "Hope", "Tobu", (4, 46)),
        Song("Assets/Music/Itro & Tobu - Cloud 9.wav", "Cloud 9", "Itro & Tobu", (4, 36)),
        Song("Assets/Music/Tobu & Itro - Sunburst.wav", "Sunburst", "Tobu & Itro", (3, 11)),
        Song("Assets/Music/Tobu - Infectious.wav", "Infectious", "Tobu", (4, 17)),
        Song("Assets/Music/Tobu - Candyland [NCS Release].wav", "Candyland", "Tobu", (3, 19)),
        Song("Assets/Music/Alan Walker - Spectre [NCS Release].wav", "Spectre", "Alan Walker", (3, 47)),
        Song("Assets/Music/Disfigure - Blank.wav", 'Blank', 'Disfigure', (3, 30)),
        Song("Assets/Music/Jim Yosef - Firefly.wav", "Firefly", "Jim Yosef", (4, 17))
    ]

    # the different states that the game can be in
    game_states = {
        'Main Menu': 0,
        'Game Active': 1,
        'Game Paused': 2,
        'Game Over': 3,
    }

    def_fps = 60  # the default value for frames per second that the game will run at
    def_frames_per_round = 15  # the default value for the number of frames per "round" (a round is the period of time between each tile iteration on the game board)
    def_frames_per_round_iter = 1  # the default value for how much to decrement the tiles_per_round value each time the game speeds up
    def_player_speed_iter = 2  # the default value for the player's speed

    secondsPerIdealGame = 120  # the number of seconds that a player should be able to survive for (if this game had a win condition, it would be upon reaching this point)
    numTimesSpeedUp = 11  # the number of times that the game will speed up before it reachs the maximum speed

    def __init__(self):
        self.frames_per_round_iter = self.def_frames_per_round_iter  # how often to speed up the game
        self.player_speed_iter = self.def_player_speed_iter  # how much to increase the speed of the player when the game speeds up

        # initialize game clock
        self.gameClock = pygame.time.Clock()

        print("Tiles Wide default still used")
        self.tiles_wide = 3
        print("Screen resolution default still used")
        self.screen = (800, 800)  # screen width, height
        # create the pygame window
        self.gameWindow = pygame.display.set_mode(self.screen)
        pygame.display.set_caption("BLACKOUT")

        self.restart = True  # whether or not this game session has ended (if it does it returns you to main menu or game over screen)
        self.terminate = False  # whether or not to restart a new game
        # initialize starter values
        self.game_state = self.game_states['Main Menu']
        # variables to determine where the player is moving towards this frame
        self.playerYMove = 0
        self.playerXMove = 0
        # initialize frames per second(fps)
        self.fps = self.def_fps
        # set up the game board
        self.gameBoard = Board(self.screen[0] * 0.8, self.screen[0] * 0.8, self.tiles_wide, self.tiles_wide, self.screen)
        # set up the player object
        self.player = Player(self.gameBoard.activeTiles[numTilesAhead].positionX + (self.gameBoard.activeTiles[numTilesAhead].width / 2), self.gameBoard.activeTiles[numTilesAhead].positionY + (self.gameBoard.activeTiles[numTilesAhead].height / 2))
        # center the player's mouse over the player object (a circle on the screen)
        pygame.mouse.set_pos(self.player.posX, self.player.posY)

        self.gameplay_time = {
            # the time that the player lasted in the game this time (measured in minutes:seconds:milliseconds)
            'minutes': 0,
            'seconds': 0,
            'milliseconds': 0
        }

        self.curr_song = self.songs[0]  # the song that is currently being used for background music

        # initialize all screens and menus
        self.mainMenu = MainMenu(self.screen[0], self.screen[1])
        self.gameOverScreen = GameOverScreen(self.screen)
        self.pauseMenu = PauseMenu(self.screen[0], self.screen[1])

        self.song_num = random.randint(0, len(self.songs) - 1)


    def run(self):
        while(self.restart):
            self.terminate = False
            while(not self.terminate):
                self.counter = 0
                self.framesPerRound = self.def_frames_per_round

                # User is in the main menu
                if(self.game_state == self.game_states['Main Menu']):
                    self.curr_song = self.songs[7]
                    self.curr_song.play()

                while(self.game_state == self.game_states['Main Menu'] and not self.terminate):
                    self.fps = 30
                    # stop playing the current song

                    # make the mouse visible to the player
                    pygame.mouse.set_visible(True)

                    if(self.mainMenu.titleAnimationCreated):
                        self.mainMenu.runTitleAnimation(self.gameWindow)
                    else:
                        self.mainMenu.startTitleAnimation(self.gameWindow)
                        self.mainMenu.show(self.gameWindow, True)

                    # event handling within the main menu
                    for event in pygame.event.get():
                        if(event.type == pygame.QUIT):  # user quits game
                            self.endGame()
                        if(event.type == pygame.MOUSEBUTTONDOWN):
                            if(self.mainMenu.options[0].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user has clicked on the start game button
                                self.prepNewGame()
                                continue
                            elif(self.mainMenu.options[1].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user has clicked the exit game button
                                self.endGame()
                                continue
                        if(event.type == pygame.KEYDOWN):
                            if(event.key == pygame.K_ESCAPE):
                                # user wants to exit game
                                self.endGame()
                                continue
                    self.gameClock.tick(self.fps)
                    pygame.display.update()
                if(self.game_state == self.game_states['Game Over'] and not self.terminate):
                    self.curr_song.fadeout(100)
                    importScores("Assets/highscores.txt")

                while(self.game_state == self.game_states['Game Over'] and not self.terminate):
                    # player is seeing the game over screen
                    pygame.mouse.set_visible(True)
                    self.gameOverScreen.update(self.gameWindow, self.screen, self.gameplay_time)

                    # event handling in the game over screen
                    for event in pygame.event.get():
                        if(event.type == pygame.QUIT):
                            self.endGame()
                            continue
                        if(event.type == pygame.KEYDOWN):
                            if(event.key == pygame.K_ESCAPE):
                                # user wants to exit game
                                self.restartGame()
                                self.game_state = self.game_states['Main Menu']
                                continue
                            if(event.key == pygame.K_SPACE):
                                # user wants to play again
                                self.newGameSession()
                                self.prepNewGame()
                                continue
                        if(event.type == pygame.MOUSEBUTTONDOWN):
                            if(self.gameOverScreen.options[0].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user selected the play again button
                                self.newGameSession()
                                self.prepNewGame()
                                self.game_state = self.game_states['Game Active']
                                continue
                            if(self.gameOverScreen.options[1].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user selected to return to the main menu
                                self.newGameSession()
                                self.game_state = self.game_states['Main Menu']
                                continue

                    self.fps = 120
                    self.gameClock.tick(self.fps)
                    pygame.display.update()

                while(self.game_state == self.game_states['Game Paused'] and not self.terminate):
                    self.curr_song.pause()
                    pygame.mouse.set_visible(True)
                    self.fps = 60
                    self.pauseMenu.show(self.gameWindow, True)

                    # event handling for pause menu actions
                    for event in pygame.event.get():
                        if(event.type == pygame.QUIT):
                            self.endGame()
                            continue
                        if(event.type == pygame.MOUSEBUTTONDOWN):
                            if(self.pauseMenu.options[0].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user selected the resume game button
                                self.unpauseGame()
                            if(self.pauseMenu.options[1].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user selected the main menu button
                                self.newGameSession()
                                self.game_state = self.game_states['Main Menu']
                                continue
                        if(event.type == pygame.KEYDOWN):
                            if(event.key == pygame.K_SPACE):
                                # user wants to resume the game
                                self.unpauseGame()
                            if(event.key == pygame.K_ESCAPE):
                                # user wants to return to the main menu
                                self.game_state = self.game_states['Main Menu']
                                self.newGameSession()
                                continue
                            if(event.key == pygame.K_r):
                                self.newGameSession()
                                self.prepNewGame()
                                self.game_state = self.game_states['Game Active']
                                continue

                    self.gameClock.tick(self.fps)
                    pygame.display.update()

                while(self.game_state == self.game_states['Game Active'] and not self.terminate):
                    # active gameplay for the user
                    pygame.mouse.set_visible(False)

                    self.fps = 30

                    self.iterateTime()

                    # event handling for active gameplay
                    for event in pygame.event.get():
                        if(event.type == pygame.QUIT):
                            self.endGame()
                            continue
                        if(event.type == pygame.MOUSEMOTION):
                            if (not (pygame.mouse.get_pos()[0] < self.gameBoard.x or pygame.mouse.get_pos()[0] > self.gameBoard.x + self.gameBoard.width) and pygame.mouse.get_focused() != 0):
                                self.playerXMove = pygame.mouse.get_pos()[0]
                            if (not (pygame.mouse.get_pos()[1] < self.gameBoard.y or pygame.mouse.get_pos()[1] > self.gameBoard.y + self.gameBoard.height) and pygame.mouse.get_focused() != 0):
                                self.playerYMove = pygame.mouse.get_pos()[1]
                        if(event.type == pygame.KEYDOWN):
                            if(event.key == pygame.K_SPACE):
                                # user wants to pause the game
                                self.pauseGame()
                                self.terminate = False
                                self.player.status = 1
                                continue
                            if(event.key == pygame.K_r):
                                self.newGameSession()
                                self.prepNewGame()
                                self.game_state = self.game_states['Game Active']
                                continue
                            if(event.key == pygame.K_ESCAPE):
                                # user wants to return to the main menu
                                self.newGameSession()
                                self.game_state = self.game_states['Main Menu']
                                continue

                    #check if the mouse is outside of the game board, and if it is, move them back inside the game board
                    if(self.playerXMove < self.gameBoard.x + self.player.radius):
                        self.playerXMove = self.gameBoard.x + self.player.radius
                    elif(self.playerXMove > self.gameBoard.x + self.gameBoard.width - self.player.radius):
                        self.playerXMove = self.gameBoard.x + self.gameBoard.width - self.player.radius
                    if(self.playerYMove < self.gameBoard.y + self.player.radius):
                        self.playerYMove = self.gameBoard.y + self.player.radius
                    elif(self.playerYMove > self.gameBoard.y + self.gameBoard.height - self.player.radius):
                        self.playerYMove = self.gameBoard.y + self.gameBoard.height - self.player.radius


                    # move the player to their new position as specified by either mouse movement or "not-movement"
                    self.player.move(self.playerXMove, self.playerYMove)

                    # move the mouse to the center of the new player position
                    pygame.mouse.set_pos(self.player.posX, self.player.posY)

                    self. collisions = self.player.getTileCollisions(self.gameBoard.tiles)

                    for tile in self.collisions:
                        if(tile.value == 'x'):
                            self.player.status = 0
                            terminate = True
                            restart = True

                    self.gameWindow.fill((10, 10, 10))
                    self.gameWindow.fill(Colors.black, pygame.Rect((0,0), (self.screen[0], self.screen[1] * 0.1)))

                    # update all non-board and non-player elements on the screen during active game state
                    self.activeGameDisplay()

                    # iterate tiles, increase speeds, etc. when the time is correct (as specified by the counter variable)
                    if(self.counter % (int(self.fps * (self.secondsPerIdealGame / self.numTimesSpeedUp))) == 0 and self.counter != 0):
                        # time to speed up the game
                        if(self.framesPerRound > 5):
                            self.framesPerRound -= self.frames_per_round_iter
                            self.player.speed += self.player_speed_iter
                    if(self.counter % self.framesPerRound == 0 and self.counter != 0):
                        # game board needs to iterate its tiles to the next set
                        self.gameBoard.iterateTiles()

                    self.gameClock.tick(self.fps)
                    self.boardPulseAnimation.iterate()
                    self.boardPulseAnimation.update(self.gameWindow, 'center')
                    self.gameBoard.update(self.gameWindow)
                    self.player.update(self.gameWindow)
                    pygame.display.update()

                    self.counter += 1

                    # check if the player has "blacked out" and if they have, send them to the game over screen and let them choose what to do from there
                    if(self.player.status == 0):
                        self.game_state = self.game_states['Game Over']
                        # check if this player got a high score, and record it accordingly
                        if(self.isHighScore(self.gameplay_time)):
                            print("VICTORY")







    # function to handle reseting all required values and any other actions required when a new game session starts (the user just lost during their last game session)
    def newGameSession(self):
        self.terminate = False
        self.restart = True

        self.curr_song.fadeout(10)
        self.song_num = random.randint(0, len(self.songs) - 1)
        self.curr_song = self.songs[self.song_num]

        # reset the game counter (keeps track of what to do when by modulus operation)
        self.counter = 0

        # reset the gameboard to a new board as the game starts
        self.gameBoard = Board(self.screen[0] * 0.8, self.screen[0] * 0.8, self.tiles_wide, self.tiles_wide, self.screen)


    def prepNewGame(self):
        self.game_state = self.game_states['Game Active']
        self.player.status = 1
        self.terminate = False
        self.restart = True
        self.resetStopWatch()
        self.counter = 0
        self.curr_song = self.songs[self.song_num]
        self.curr_song.play()

        # reset the player position to the center of the first active tile on the board (the pure white tile)
        self.player.posX = self.gameBoard.activeTiles[numTilesAhead].positionX + (self.gameBoard.activeTiles[numTilesAhead].width / 2)
        self.player.posY = self.gameBoard.activeTiles[numTilesAhead].positionY + (self.gameBoard.activeTiles[numTilesAhead].height / 2)

        # move the player mouse to the center of the player object for ease of play at start of game
        pygame.mouse.set_pos(self.player.posX, self.player.posY)
        # set up the animation that will be played around the game board during play
        self.boardPulseAnimation = PulseAnimation('rectangle',
                                                  [i for i in range(int(self.gameBoard.x), int(self.gameBoard.x + 1))],
                                                  [i for i in range(int(self.gameBoard.y), int(self.gameBoard.y + 1))],
                                                  [i for i in range(int(self.gameBoard.height), int(self.gameBoard.height + 1))],
                                                  [i for i in range(int(self.gameBoard.width), int(self.gameBoard.width + 1))],
                                                  [i for i in range(254, 255)],
                                                  [i for i in range(0, 255)],
                                                  [i for i in range(0, int(self.screen[0] * 0.05))],
                                                  15, 1,
                                                  {
                                                      'left': int(self.gameBoard.x),
                                                      'right': int(self.gameBoard.x + self.gameBoard.width),
                                                      'top': int(self.gameBoard.y),
                                                      'bottom': int(self.gameBoard.y + self.gameBoard.height)
                                                  })


    # resets the stopwatch that tracks the time a player lasts during play
    def resetStopWatch(self):
        self.gameplay_time['minutes'] = 0
        self.gameplay_time['seconds'] = 0
        self.gameplay_time['milliseconds'] = 0


    # ends the game and terminates the program
    def endGame(self):
        self.terminate = True
        self.restart = False


    # carry out necessary operations to start a new game
    def restartGame(self):
        self.terminate = True
        self.restart = True


    def unpauseGame(self):
        self.game_state = self.game_states['Game Active']
        pygame.mouse.set_pos(self.player.posX, self.player.posY)
        self.curr_song.unpause()


    def pauseGame(self):
        self.game_state = self.game_states['Game Paused']
        self.curr_song.pause()


    def iterateTime(self):
        self.gameplay_time['milliseconds'] += self.gameClock.get_time()
        if (self.gameplay_time['milliseconds'] >= 1000):
            self.gameplay_time['milliseconds'] -= 1000
            self.gameplay_time['seconds'] += 1

        if (self.gameplay_time['seconds'] >= 60):
            self.gameplay_time['minutes'] += 1
            self.gameplay_time['seconds'] -= 60


    def activeGameDisplay(self):
        #show the gameplay time on screen
        self.displayTimeActiveGame()

        # show some help statements for how to pause and restart the game while playing
        pauseTxt = Fonts.medSmall.render("(P)ause", False, Colors.white)
        restartTxt = Fonts.medSmall.render("(R)estart", False, Colors.white)
        self.gameWindow.blit(pauseTxt, (self.screen[0] * 0.95 - pauseTxt.get_width(),
                                        self.screen[1] * 0.1 * 0.5 - ((pauseTxt.get_height() + restartTxt.get_height()) / 2)))
        self.gameWindow.blit(restartTxt, (self.screen[0] * 0.95 - restartTxt.get_width(), self.screen[1] * 0.1 * 0.5 - (
        (pauseTxt.get_height() + restartTxt.get_height()) / 2) + pauseTxt.get_height()))


    def displayTimeActiveGame(self):
        minutes = ""
        seconds = ""
        milliseconds = ""
        if (self.gameplay_time['minutes'] < 10):
            minutes = '0' + str('%.0f' % self.gameplay_time['minutes'])
        else:
            minutes = str('%.0f' % self.gameplay_time['minutes'])
        if (self.gameplay_time['seconds'] < 10):
            seconds = '0' + str('%.0f' % self.gameplay_time['seconds'])
        else:
            seconds = str('%.0f' % self.gameplay_time['seconds'])
        if (self.gameplay_time['milliseconds'] / 10 < 10):
            milliseconds = '0' + str('%.0f' % (self.gameplay_time['milliseconds'] / 10))
        else:
            milliseconds = str('%.0f' % int(self.gameplay_time['milliseconds'] / 10))

        gameStopWatchDisplay = Fonts.large.render(str(minutes + ":" + seconds + ":" + milliseconds), False, Colors.white)
        self.gameWindow.blit(gameStopWatchDisplay,
                        (self.screen[0] * 0.075, self.screen[1] * 0.1 * 0.5 - (gameStopWatchDisplay.get_height() / 2)))

    # check if the time from the last game was a new record
    def isHighScore(self, time):
        for i in range(len(scores)):
            if(time['minutes'] > scores[i][0]
               or (time['minutes'] == scores[i][0] and time['seconds'] > scores[i][1])
               or time['minutes'] == scores[i][0] and time['seconds'] == scores[i][1] and time['milliseconds'] > scores[i][2]):
                self.insertNewHighScore(time, i)
                self.exportScoresToFile()
                return True

        return False

    # exports the high score data to a file in order to save data between gameplay sessions
    def exportScoresToFile(self):
        outFile = open("Assets/highscores.txt", 'w')

        for i in range(len(scores)):
            outFile.write(str(scores[i][0]) + " " + str(scores[i][1]) + " " + str(scores[i][2]))
            if(i != len(scores) - 1):
                outFile.write('\n')

        outFile.close()

    # insert a new high schore into the last at the specified index, pushing everything below the index down one space in the list (i.e. if index was 5, the item at index 3 would be pushed to index 4), shifting everything below the index down in the list
    def insertNewHighScore(self, time, index):
        for i in range(len(scores) - index):
            scores[len(scores) - i - 1][0] = scores[len(scores) - i - 2][0]
            scores[len(scores) - i - 1][1] = scores[len(scores) - i - 2][1]
            scores[len(scores) - i - 1][2] = scores[len(scores) - i - 2][2]
        scores[index][0] = time['minutes']
        scores[index][1] = time['seconds']
        scores[index][2] = int(time['milliseconds'] / 10)