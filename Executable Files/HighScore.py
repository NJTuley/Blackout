# object to hold high scores

class HighScore:

    def __init__(self, name, time):
        if(not self.isEmpty(name)):
            self.name = name
        else:
            raise Exception("Invalid high score name: Cannot have empty name")
        self.time = time


    def isEmpty(self, val):
        for char in val:
            if char == ' ':
                return True

        return False