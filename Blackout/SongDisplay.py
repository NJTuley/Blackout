import Colors
import Fonts
import pygame

class SongDisplay():


    def __init__(self, pauseMenu, song):
        self.x = 0
        self.width = int(pauseMenu.width * 0.4)
        self.height = int(pauseMenu.height * 0.15)
        self.y = int(pauseMenu.height - self.height)
        self.song = song


    def update(self, gameWindow):
       # window.blit(self.title, ((self.width * 0.5) - (self.title.get_width() * 0.5), (self.height * 0.3) - (self.title.get_height() * 0.5)))
       song_title = Fonts.songText.render("Song - " + self.song.title, False, Colors.white)
       song_artist = Fonts.songText.render("Artist - " + self.song.artist, False, Colors.white)
       pygame.draw.rect(gameWindow, Colors.black, pygame.Rect(self.x, self.y, self.width, self.height))
       gameWindow.blit(song_title, (int(self.x + 40), int(self.y + self.height * 0.3 - song_title.get_height() * 0.5)))
       gameWindow.blit(song_artist, (int(self.x + 40), int(self.y + self.height * 0.6 - song_artist.get_height() * 0.5)))