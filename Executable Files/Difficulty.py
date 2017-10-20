# holds all setting associated with difficulties

from Song import Song

class Difficulty():


    def __init__(self, name, tiles_wide, max_fpr, min_fpr, player_speed, songs):
        self.name = name
        self.tiles_wide = tiles_wide
        self.max_fpr = max_fpr
        self.min_fpr = min_fpr
        self.player_speed = player_speed
        self.songs = songs




easy_songs = [
    Song("Assets/Music/Itro & Tobu - Cloud 9.wav", "Cloud 9", "Itro & Tobu", (4, 36)),
    Song("Assets/Music/Tobu & Itro - Sunburst.wav", "Sunburst", "Tobu & Itro", (3, 11)),
    Song("Assets/Music/Tobu - Candyland [NCS Release].wav", "Candyland", "Tobu", (3, 19))
]

moderate_songs = [
    Song("Assets/Music/Tobu - Infectious.wav", "Infectious", "Tobu", (4, 17)),
    Song("Assets/Music/Alan Walker - Spectre [NCS Release].wav", "Spectre", "Alan Walker", (3, 47)),
    Song("Assets/Music/Tobu - Hope.wav", "Hope", "Tobu", (4, 46))
]

hard_songs = [
    Song("Assets/Music/Tobu - Seven.wav", "Seven", "Tobu", (3, 54)),
    Song("Assets/Music/Jim Yosef - Firefly.wav", "Firefly", "Jim Yosef", (4, 17)),
    Song("Assets/Music/Different Heaven - Nekozilla.wav", "Nekozilla", "Different Heaven", (2,45))
]

difficulties = [
    Difficulty("Easy", 3, 20, 5, 15, easy_songs),
    Difficulty("Moderate", 4, 17, 4, 17, moderate_songs),
    Difficulty("Hard", 5, 15, 3, 20, hard_songs)
]