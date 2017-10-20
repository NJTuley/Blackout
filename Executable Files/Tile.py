
import pygame
from Error import Error

#the amount to decrement each tile status by each frame
tileStatusDecrement = 255/ (60 * 3)

white = (255, 255, 255)
black = (0, 0, 0)

fullTileColor = black
emptyTileColor = white



# function that will generate the list to pass into Tile contstructor for new tiles
# @param x The x coordinate of the new tile
# @param y The y coordinate of the new tile
# @param height The height of the new tile
# @param width The width of the new tile
# @param row The row in the board grid the tile will be placed in
# @param column The column in the board grid the tile will be placed in
def newTileParamGenerator(tiles_wide, value, x, y, height, width, row, column, borderWidth = 1):
    # parameter list to send to constructor for new Tile object
    param_list = {
        'value': value,
        'x': x,
        'y': y,
        'height': height,
        'width': width,
        'row': row,
        'col': column,
        'borderWidth': borderWidth,
        'tiles_wide' : tiles_wide
    }

    # send the populated parameter list to create a new tile with the specified parameters and return this Tile
    return Tile(False, param_list)


# function that will generate the list to pass into Tile constructor for a tile that is a copy of an existing tile
def copyTileParameterGenerator(tiles_wide, tile):
    # parameter list to send to constructor for copied Tile objects
    param_list = {
        'tile': tile,
        'tiles_wide' : tiles_wide
    }

    return Tile(True, param_list)

#class to hold
class Tile():
    """
    Member Variables:
        positionX
        positionY
        height
        width
        fillColor
        borderColor
        borderWidth
        status (a value from 0 to # that indicates how many rounds until this tile is blacked out as a float) (this is used to determine the color)
        value
        row The row in the board grid that the tile is in
        column The column in the board grid that the tile is in
        surface The actual shape that will represent the tile on the game display
    Constants
        Black
        White
    """

    def __init__(self, copied, args):
        self.tileSafeColors = []
        if(not copied):  # make a new Tile
            self.value = args['value']
            self.positionX = args['x']
            self.positionY = args['y']
            self.row = args['row']
            self.column = args['col']
            if(args['height'] >= 0):
                self.height = args['height']
            else:
                raise Error("InvalidInput", "Cannot create Tile with negative height")

            if (args['width'] >= 0):
                self.width = args['width']
            else:
                raise Error("InvalidInput", "Cannot create Tile with negative width")

            self.borderWidth = args['borderWidth']

        else:  # Make a copy of an existing tile
            self.value = 'x'  # default value is a black, 'full' tile
            self.positionX = args['tile'].positionX
            self.positionY = args['tile'].positionY
            self.row = args['tile'].row
            self.column = args['tile'].column
            if (args['tile'].height >= 0):
                self.height = args['tile'].height
            else:
                raise Error("InvalidInput", "(Attempted to copy tile) Cannot create Tile with negative height")

            if (args['tile'].width >= 0):
                self.width = args['tile'].width
            else:
                raise Error("InvalidInput", "(Attempted to copy tile) Cannot create Tile with negative width")
        self.numTilesAhead = args['tiles_wide']
        for i in range(self.numTilesAhead):
            colorNum = ((255 / (self.numTilesAhead + 1)) * (i + 1))
            self.tileSafeColors.append((255 - colorNum, 255 - colorNum, 255 - colorNum))
        self.setColor()  # update tile color based on status
        self.status = 255.0  # set the status of this tile
        super().__init__()


    # reset the game board to its initial state
    #def reset(self):
       # self.__init__(self, newTileParamGenerator(self.numTilesAhead, self.value, self.positionX, self.positionY, self.height, self.width, self.row, self.column))


    #set tile color based on tile value
    def setColor(self):
        if(self.value == 'x'):  # full tile
            self.fillColor = black
        elif(self.value == '0'):  # empty tile
            self.fillColor = white
        else:  # transitioning to empty or empty itself
            self.fillColor = self.tileSafeColors[int(self.value) - 1]

        self.borderColor = self.fillColor


    def setValue(self, value):
        self.value = value

    def update(self, window):
        self.setColor()
        #draw the tile
        # the filled background of the tile
        pygame.draw.rect(window, self.fillColor, pygame.Rect(self.positionX, self.positionY, self.height, self.width), 0)
        #the border of the tile
        pygame.draw.rect(window, self.borderColor, pygame.Rect(self.positionX - 1, self.positionY - 1, self.height + 2, self.width + 2), self.borderWidth)


    def __str__(self):
            return "\nValue: \"" + self.value + "\"\tStatus: " + str(self.status) + \
                   "\nPosition (X, Y): (" + str(self.positionX) + ", " + str(self.positionY) + ")\n" \
                    "Height: " + str(self.height) + "\tWidth: " + str(self.width) + "\n" \
                   "Fill Color: " + str(self.fillColor) + "\tBorder Color: " + str(self.borderColor) + \
                    "\nBoard Row: " + str(self.row) + "\tBoard Column: " + str(self.column)


    def adjacent(self, tile):
        if(self.column + 1 == tile.column
           or self.column - 1 == tile.column
           or self.row + 1 == tile.row
           or self.row - 1 == tile.row):
            return True
        else:
            return False