# application class to handle the actual running of the Blackout game application

import pygame

pygame.init()

from Player import Player
from Player import defSpeed
from Song import Song
import Colors
import Fonts
from Board import Board
import random
from MainMenu import MainMenu
from PauseMenu import PauseMenu
from GameOverScreen import GameOverScreen
import HighScores
from PulseAnimation import PulseAnimation
from TextField import TextField
from helpScreen import helpScreen
from Difficulty import difficulties
from EpilepsyWarning import EpilepsyWarning


class Application():

    pygame.mixer.set_num_channels(2)  # set the maximum number of channels of playback that are allowed for audio
    songPlayback = pygame.mixer.Channel(0)  # the channel that will play the background music for the game during play

    # song that will play during the main menu
    title_song = Song("Assets/Music/Elektronomia - Limitless.wav", "Limitless", "Elektronomia", (4, 4))

    # the different states that the game can be in
    game_states = {
        'Main Menu': 0,
        'Game Active': 1,
        'Game Paused': 2,
        'Game Over': 3,
    }

    def_fps = 60  # the default value for frames per second that the game will run at
    def_frames_per_round = 20  # the default value for the number of frames per "round" (a round is the period of time between each tile iteration on the game board)
    def_frames_per_round_iter = 1  # the default value for how much to decrement the tiles_per_round value each time the game speeds up
    def_player_speed_iter = 2  # the default value for the player's speed

    secondsPerIdealGame = 120  # the number of seconds that a player should be able to survive for (if this game had a win condition, it would be upon reaching this point)


    num_active_tiles = 4

    def __init__(self):

        self.difficulty_level = difficulties[0]
        self.numTimesSpeedUp = self.difficulty_level.max_fpr - self.difficulty_level.min_fpr  # the number of times that the game will speed up before it reaches the maximum speed
        self.framesPerRound = self.difficulty_level.max_fpr
        self.frames_per_round_iter = 1 # how often to speed up the game
        self.player_speed_iter = self.def_player_speed_iter  # how much to increase the speed of the player when the game speeds up

        # initialize game clock
        self.gameClock = pygame.time.Clock()

        # how many tiles are shown on the screen as a grid (this number is the number of tiles per side of the grid, aka 3 means the grid is 3x3)
        self.tiles_wide = self.difficulty_level.tiles_wide
        self.screen = (800, 800)  # screen width, height
        # create the pygame window and set the window caption
        self.gameWindow = pygame.display.set_mode(self.screen)
        pygame.display.set_caption("BLACKOUT")

        self.restart = True  # whether or not this game session has ended (if True it returns you to main menu or game over screen)
        self.terminate = False  # whether or not to restart a new game
        # initialize starter values
        self.game_state = self.game_states['Main Menu']  # displays the epilepsy warning
        # variables to determine where the player is moving towards this frame
        self.playerYMove = 0
        self.playerXMove = 0
        # initialize frames per second(fps)
        self.fps = self.def_fps
        # set up the game board
        self.gameBoard = Board(self.screen[0] * 0.8, self.screen[0] * 0.8, self.tiles_wide, self.tiles_wide, self.screen)
        # set up the player object
        self.player = Player(self.gameBoard.activeTiles[self.difficulty_level.tiles_wide - 1 - 1].positionX + (self.gameBoard.activeTiles[self.difficulty_level.tiles_wide - 1 - 1].width / 2), self.gameBoard.activeTiles[self.difficulty_level.tiles_wide - 1 - 1].positionY + (self.gameBoard.activeTiles[self.difficulty_level.tiles_wide - 1 - 1].height / 2), int(self.gameBoard.tileHeight * 0.2))
        # center the player's mouse over the player object (a circle on the screen)
        pygame.mouse.set_pos(self.player.posX, self.player.posY)

        self.gameplay_time = {
            # the time that the player lasted in the game this time (measured in minutes:seconds:milliseconds)
            'minutes': 0,
            'seconds': 0,
            'milliseconds': 0
        }


        # initialize all screens and menus
        self.mainMenu = MainMenu(self.screen[0], self.screen[1])
        diff_index = -1
        for i in range(len(difficulties)):
            if self.difficulty_level == difficulties[i]:
                diff_index = i
        if(diff_index != -1):
            self.gameOverScreen = GameOverScreen(self.screen, diff_index)
        else:
            raise Exception("Invalid difficulty index")


        self.curr_song = self.title_song
        self.pauseMenu = PauseMenu(self.curr_song, self.screen[0], self.screen[1])
        # text field to gather new text input from the user that will be the 3 character long name associated with a new high score
        self.newHighScoreInput = TextField("New High Score, type your name and press enter!:", self.screen)


    def run(self):
        self.fps = 30
        self.gameClock.tick(self.fps)
        self.epilepsy_warning = EpilepsyWarning(self.screen)
        self.epilepsy_warning.run(self.gameWindow, self.fps, self.gameClock)
        while(self.restart):
            self.terminate = False
            while(not self.terminate):
                # counter variable to track the number of frames passed during game execution
                self.counter = 0
                # the number of frames that pass between each tile iteration
                self.framesPerRound = self.difficulty_level.max_fpr
                # User is in the main menuif(self.game_state == self.game_states['Main Menu']):
                self.curr_song = self.title_song
                self.curr_song.play(self.fps / 2)

                while(self.game_state == self.game_states['Main Menu'] and not self.terminate):
                    self.fps = 30
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
                                self.difficulty_level = difficulties[0]
                                self.prepNewGame()
                                continue
                            if (self.mainMenu.options[1].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user has clicked on the start game button
                                self.difficulty_level = difficulties[1]
                                self.prepNewGame()
                                continue
                            if (self.mainMenu.options[2].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user has clicked on the start game button
                                self.difficulty_level = difficulties[2]
                                self.prepNewGame()
                                continue
                            elif(self.mainMenu.options[3].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                # user has clicked the How to play button
                                self.fps = 30
                                help = helpScreen(self.screen)
                                helping = True
                                while(helping):
                                    for event in pygame.event.get():
                                        if(event.type == pygame.QUIT):
                                            self.terminate = True
                                            helping = False
                                            self.restart = False
                                        if(event.type == pygame.MOUSEBUTTONDOWN):
                                            if(help.returnBtn.inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                                                helping = False
                                    help.update(self.gameWindow)
                                    pygame.display.update()
                                    self.gameClock.tick(self.fps)
                            elif(self.mainMenu.options[4].inBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
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
                    HighScores.importScores("Assets/highscores.txt")

                while(self.game_state == self.game_states['Game Over'] and not self.terminate):
                    # player is seeing the game over screen
                    pygame.mouse.set_visible(True)
                    diff_index = -1
                    for i in range(len(difficulties)):
                        if self.difficulty_level == difficulties[i]:
                            diff_index = i
                    if (diff_index != -1):
                        self.gameOverScreen.update(self.gameWindow, self.screen, self.gameplay_time, diff_index)
                    else:
                        raise Exception("Invalid difficulty index")

                    while(HighScores.newHighScore):
                        for event in pygame.event.get():
                            if(event.type == pygame.QUIT):
                                terminate = True
                                restart = False
                                HighScores.newHighScore = False
                                continue
                            if(event.type == pygame.KEYDOWN):
                                if(event.key == pygame.K_RETURN):
                                    HighScores.newHighScore = False
                                    if(self.newHighScoreInput.nameIn == "(3 characters maximum)"):
                                        HighScores.newHighScoreInsert(self.gameplay_time, "-", self.difficulty_level)
                                    else:
                                        HighScores.newHighScoreInsert(self.gameplay_time, self.newHighScoreInput.nameIn[0:3], self.difficulty_level)
                                if(event.key == pygame.K_ESCAPE):
                                    HighScores.newHighScore = False
                                if(event.key == pygame.K_BACKSPACE):
                                    self.newHighScoreInput.nameIn = self.newHighScoreInput.nameIn[0:len(self.newHighScoreInput.nameIn) - 1]
                                if(self.isAlphanumericKey(event)):
                                    if(self.newHighScoreInput.nameIn == "(3 characters maximum)"):
                                        self.newHighScoreInput.nameIn = self.getKeyVal(event).upper()
                                    else:
                                        if(len(self.newHighScoreInput.nameIn) < 3):
                                            self.newHighScoreInput.nameIn += self.getKeyVal(event).upper()
                        self.newHighScoreInput.update(self.gameWindow)
                        pygame.display.update()

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

                    if(self.gameClock.get_fps() < 20):
                        print(self.gameClock.get_fps())

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
                            if(event.key == pygame.K_p):
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
                            self.terminate = True
                            self.restart = True

                    self.gameWindow.fill((10, 10, 10))
                    self.gameWindow.fill(Colors.black, pygame.Rect((0,0), (self.screen[0], self.screen[1] * 0.1)))

                    # update all non-board and non-player elements on the screen during active game state
                    self.activeGameDisplay()

                    if(self.counter % self.framesPerRound == 0 and self.counter != 0):
                        # game board needs to iterate its tiles to the next set
                        self.gameBoard.iterateTiles()

                    # iterate tiles, increase speeds, etc. when the time is correct (as specified by the counter variable)
                    if (self.counter % (int(self.fps * (self.secondsPerIdealGame / self.numTimesSpeedUp))) == 0 and self.counter != 0):
                        # time to speed up the game
                        if (self.framesPerRound > self.difficulty_level.min_fpr):
                            self.framesPerRound -= self.frames_per_round_iter
                            self.player.speed += self.player_speed_iter

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
                        if(HighScores.isBestScore(self.gameplay_time, self.difficulty_level)):
                            HighScores.newHighScore = True


    # function to handle resetting all required values and any other actions required when a new game session starts (the user just lost during their last game session)
    def newGameSession(self):
        self.terminate = False
        self.restart = True

        self.curr_song.fadeout(10)
        self.song_num = random.randint(0, len(self.difficulty_level.songs) - 1)
        self.curr_song = self.difficulty_level.songs[self.song_num]

        # reset the game counter (keeps track of what to do when by modulus operation)
        self.counter = 0



        self.newHighScoreInput = TextField("New High Score, type your name and press enter!:", self.screen)


    def prepNewGame(self):
        self.game_state = self.game_states['Game Active']
        self.player.status = 1
        self.terminate = False
        self.restart = True
        self.resetStopWatch()
        self.counter = 0
        self.song_num = random.randint(0, len(self.difficulty_level.songs) - 1)
        self.curr_song = self.difficulty_level.songs[self.song_num]
        self.curr_song.play(self.fps / 2)
        diff_index = -1
        for i in range(len(difficulties)):
            if self.difficulty_level == difficulties[i]:
                diff_index = i
        if(diff_index != -1):
            self.gameOverScreen = GameOverScreen(self.screen, diff_index)
        else:
            raise Exception("Invalid difficulty index")

        self.numTimesSpeedUp = self.difficulty_level.max_fpr - self.difficulty_level.min_fpr  # the number of times that the game will speed up before it reaches the maximum speed

        # reset the gameboard to a new board as the game starts
        self.gameBoard = Board(self.screen[0] * 0.8, self.screen[0] * 0.8, self.difficulty_level.tiles_wide, self.difficulty_level.tiles_wide, self.screen)

        self.framesPerRound = self.difficulty_level.max_fpr

        #reset the player object
        self.player = Player(
            self.gameBoard.activeTiles[self.num_active_tiles - 1].positionX + (self.gameBoard.activeTiles[self.num_active_tiles - 1].width / 2),
            self.gameBoard.activeTiles[self.num_active_tiles - 1].positionY + (
            self.gameBoard.activeTiles[self.num_active_tiles - 1].height / 2), int(self.gameBoard.tileHeight * 0.2))



        # reset the player position to the center of the first active tile on the board (the pure white tile)
        self.player.posX = self.gameBoard.activeTiles[self.num_active_tiles - 1].positionX + (self.gameBoard.activeTiles[self.num_active_tiles - 1].width / 2)
        self.player.posY = self.gameBoard.activeTiles[self.num_active_tiles - 1].positionY + (self.gameBoard.activeTiles[self.num_active_tiles - 1].height / 2)
        self.player.speed = defSpeed


        # move the player mouse to the center of the player object for ease of play at start of game
        pygame.mouse.set_pos(self.player.posX, self.player.posY)

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
        self.pauseMenu = PauseMenu(self.curr_song, self.screen[0], self.screen[1])
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

        if(HighScores.isHighScore(self.gameplay_time, self.difficulty_level)):
            newScoretxt = Fonts.standard.render("YOU GOT A NEW BEST SCORE!!", False, Colors.white)
            self.gameWindow.blit(newScoretxt, (self.screen[0] * 0.52 - newScoretxt.get_width() * 0.5, self.screen[1] * 0.1 * 0.5 - newScoretxt.get_height() * 0.5))


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
                        (self.screen[0] * 0.05, self.screen[1] * 0.1 * 0.5 - (gameStopWatchDisplay.get_height() / 2)))


    #check if the given key pressed is a letter or number
    def isAlphanumericKey(self, event):
        for key in pygame_keycodes_alpha:
            if(event.key == pygame_keycodes_alpha[key]):
                return True
        return False

    #get the character value of a key pressed
    def getKeyVal(self, event):
        for key in pygame_keycodes_alpha:
            if(event.key == pygame_keycodes_alpha[key]):
                return key
        return ' '


# all alphanumeric keycodes in pygame
pygame_keycodes_alpha = {
    '0': pygame.K_0, '1': pygame.K_1, '2': pygame.K_2, '3': pygame.K_3, '4': pygame.K_4, '5': pygame.K_5, '6': pygame.K_6, '7': pygame.K_7, '8': pygame.K_8,
    '9': pygame.K_9, 'a': pygame.K_a, 'b': pygame.K_b, 'c': pygame.K_c, 'd': pygame.K_d, 'e': pygame.K_e, 'f': pygame.K_f, 'g': pygame.K_g, 'h': pygame.K_h,
    'i': pygame.K_i, 'j': pygame.K_j, 'k': pygame.K_k, 'l': pygame.K_l, 'm': pygame.K_m, 'n': pygame.K_n, 'o': pygame.K_o, 'p': pygame.K_p, 'q': pygame.K_q,
    'r': pygame.K_r, 's': pygame.K_s, 't': pygame.K_t, 'u': pygame.K_u, 'v': pygame.K_v, 'w': pygame.K_w, 'x': pygame.K_x, 'y': pygame.K_y, 'z': pygame.K_z
}