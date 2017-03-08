import Fonts
import Colors

# parent class for all menus

class Menu():
    options = []
    title = Fonts.title.render("", False, Colors.white)

    def __init__(self, height = 0, width = 0):
        self.height = height
        self.width = width

    def show(self, window, fillWindow):
        if(fillWindow):  # check whether or not you need to fill the window this time or not
            window.fill(Colors.black)
        window.blit(self.title, ((self.width * 0.5) - (self.title.get_width() * 0.5), (self.height * 0.3) - (self.title.get_height() * 0.5)))
        for i in range(len(self.options)):
            self.options[i].update(window)