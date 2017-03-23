# holds all setting associated with difficulties

class Difficulty():


    def __init__(self, name, tiles_wide, max_fpr, min_fpr, player_speed):
        self.name = name
        self.tiles_wide = tiles_wide
        self.max_fpr = max_fpr
        self.min_fpr = min_fpr
        self.player_speed = player_speed


difficulties = [
    Difficulty("Easy", 3, 20, 5, 15),
    Difficulty("Moderate", 4, 17, 4, 17),
    Difficulty("Hard", 5, 15, 3, 20)
]
