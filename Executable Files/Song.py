import pygame

# class to hold a song and all of its behaviors and meta data

# set initial settings for music playback
pygame.mixer.set_num_channels(2)
bg_songs = pygame.mixer.Channel(0)  # sound playback channel for all background music for the game
sound_fx = pygame.mixer.Channel(1)  # sound playback channel for all game sound effects

class Song():

    def __init__(self, filepath, title, artist, length):
        self.filepath = filepath
        self.title = title
        self.artist = artist
        self.length = length  # the length of the song, stored in a tuple that is of the format (minutes, seconds), and the values are numeric
        self.delay = 0


    # play this song on the background songs playback channel
    def play(self, delay):
        if(self.delay != delay):
            bg_songs.play(pygame.mixer.Sound(self.filepath), -1)
        else:
            self.delay += 1

        pass


    def pause(self):
        bg_songs.pause()


    def unpause(self):
        bg_songs.unpause()


    def fadeout(self, time):
        bg_songs.fadeout(time)


    # formats and returns the information about this song so it can be displayed to the screen
    # format is as follows
    #   Title
    #   Artist
    def getSongInfo(self):
        return str(self.title + '\n' + self.artist)