import random
import pygame
from Tile import numTilesAhead
from Error import Error
from Tile import white
from Tile import black
from Tile import newTileParamGenerator
from Tile import copyTileParameterGenerator

#the game board the player will be playing the game on (holds all tiles for the game)
class Board():
    #variables
    # tiles - all game tiles on the board
    # height - The height of the board
    # width - The width of the baord
    # tileHeight - The height of the individual tiles on the board
    # tileWidth - The width of the individual tiles on the board
    # backgroundColor - The background color of the board

    # constructor for board object
    # height The height of the board
    # width The width of the board
    # tilesWide The number of tiles wide that the board is
    # tilesHigh The number of tiles high that the board is
    # activeTiles The tiles currently being shown on the board as not full

    def __init__(self, height, width, tilesWide, tilesHigh, screen):
        try:
            self.tiles = []
            self.numActiveTiles = numTilesAhead + 1
            self.activeTiles = []
            self.setHeight(height)
            self.setWidth(width)
            self.backgroundColor = black

            #position the board on the screen
            self.x = int((screen[0] - self.width) / 2)
            self.y = int((screen[1] - self.height)) - screen[0] * 0.05

            self.initTiles(tilesWide, tilesHigh)

        except Error as err:
            if(err.name == "invalidHeight"):
                print("Invalid height - " + err.description)
            elif(err.name == "invalidWidth"):
                print("Invalid width - " + err.description)
            else:
                print(err.description)

    #set the height of the board
    def setHeight(self, height):
        if(height > 0):
            self.height = height
        elif(height == 0):
            raise Error("invalidHeight", "Cannot create board with height of 0")
        else:
            raise Error("invalidHeight", "Cannot create board with negative height")

    #set the width of the board
    def setWidth(self, width):
        if(width > 0):
            self.width = width
        elif(width == 0):
            raise Error("invalidWidth", "Cannot create a board with width of 0")
        else:
            raise Error("invalidWidth", "Cannot create a board with negative width")


    #initialize all tiles for the board and set default tile (center tile) to open status
    def initTiles(self, tilesWide, tilesHigh):

        self.tileHeight = self.height / tilesHigh
        self.tileWidth = self.width / tilesWide

        try:
            for row in range(tilesHigh):
                self.tiles.append([])
                for tile in range(tilesWide):
                    if(tile == int(tilesWide / 2) and row == int(tilesHigh / 2)): #initialize center tile to empty
                        self.tiles[row].append(newTileParamGenerator('0', tile * self.tileWidth + self.x, row * self.tileHeight + self.y, self.tileHeight, self.tileWidth, row, tile))
                    else: #initialize all other tiles to full
                        self.tiles[row].append(newTileParamGenerator('x', tile * self.tileWidth + self.x, row * self.tileHeight + self.y, self.tileHeight, self.tileWidth, row, tile))

            self.iterateTiles()

        except Error as err:
            if(err.name == "invalidTile"):
                print("Invalid tile created on board initialization - " + err.description)
            else:
                print(err.description)

    def resetTiles(self):
        for row in range(len(self.tiles)):
            for cell in range(len(self.tiles[0])):
                self.tiles[row][cell].value = 'x'

    def iterateTiles(self):
        self.resetTiles()
        #check if there are tiles already active
        if(len(self.activeTiles) == numTilesAhead + 1):
            for i in range(numTilesAhead + 1):
                if(not i == numTilesAhead):
                    self.activeTiles[i] = self.activeTiles[i + 1]
                    self.activeTiles[i].value = str(numTilesAhead - i)
            # generate what the new tile will be for this iteration, and put it at the end of the active tiles list
            self.activeTiles[len(self.activeTiles) - 1] = self.setNextTile(self.activeTiles[len(self.activeTiles) - 2])
            self.activeTiles[len(self.activeTiles) - 1].value = str(0)
            self.activeTiles[len(self.activeTiles) - 1].setColor()

            for i in range(len(self.activeTiles)):
                if (i != 0 and not self.activeTiles[i].adjacent(self.activeTiles[i - 1])):
                    raise Exception("Sequential Active Tiles NOT Adjacent")
        else:

            tempTile = self.tiles[int(len(self.tiles) / 2)][int(len(self.tiles[0]) / 2)]
            for i in range(numTilesAhead + 1):
                # set the 4 tiles to be open after the current one (the center tile at initialization)
                tempTile.value = str(numTilesAhead - i)
                self.activeTiles.append(tempTile)
                tempTile = self.setNextTile(tempTile)

        # loop through the list of active tiles and make sure they all have the correct value
        for i in range(len(self.activeTiles)):
            self.activeTiles[i].values = str(len(self.activeTiles) - (i + 1))
            self.activeTiles[i].setColor()
            if(self.activeTiles[i].fillColor == black):
                raise Exception("Error: Black Active Tile")

        if self.numActiveTiles == len(self.activeTiles):
            self.numActiveTiles = len(self.activeTiles)
        else:
            raise Exception("Error: Active Tile Count Mismatch")



    def update(self, window):
        pygame.draw.rect(window, white, [self.x, self.y, self.width, self.height])
        for row in range(len(self.tiles)):
            for tile in range(len(self.tiles[row])):
                self.tiles[row][tile].update(window)

    #returns the tile that is being set as the next tile active, relative to the currTile passed in as parameter
    def setNextTile(self, currTile):
        valid_tiles = self.getValidSurroundingTiles(currTile)  # get a list of all tiles directly neighbor the current tile that are valid as the next tile
        if(len(valid_tiles) > 0):
            rand = random.randint(0, len(valid_tiles) - 1)
            #return the randomly selected tile that was selected from the list of valid neighbor tiles
            return self.tiles[valid_tiles[rand][0]][valid_tiles[rand][1]]
        else:
            #the program has cornered itself, time to just push through one of the other active tiles that is a direct (4-directional) neighbor of the current tile
            for i in range(len(self.activeTiles)):
                if(currTile.row == self.activeTiles[i].row and (currTile.column == self.activeTiles[i].column - 1 or currTile.column == self.activeTiles[i].column + 1)):
                    return copyTileParameterGenerator(self.activeTiles[i])
                elif(currTile.column == self.activeTiles[i].column and (currTile.row == self.activeTiles[i].row - 1 or currTile.row == self.activeTiles[i].row + 1)):
                    return copyTileParameterGenerator(self.activeTiles[i])

            raise Exception("Did not find a active tile that directly neighbored the current tile that is cornered.")



    def getValidSurroundingTiles(self, curr_tile):
        valid_tiles = []
        # check if the current tile is a valid tile on the game board
        if(curr_tile.column < len(self.tiles) and curr_tile.column >= 0 and curr_tile.row < len(self.tiles[0]) and curr_tile.row >= 0):
            if(curr_tile.column > 0 and self.tiles[curr_tile.row][curr_tile.column - 1].value == 'x'):
                #the tile to the left of the current tile is valid, so store the grid coordinates in the valid tiles list
                valid_tiles.append((curr_tile.row, curr_tile.column - 1))
            if(curr_tile.row < len(self.tiles[0]) - 1 and self.tiles[curr_tile.row + 1][curr_tile.column].value == 'x'):
                #the tile below the current tile is valid, so store the grid coordinates in the valid tiles list
                valid_tiles.append((curr_tile.row + 1, curr_tile.column))
            if(curr_tile.column < len(self.tiles) - 1 and self.tiles[curr_tile.row][curr_tile.column + 1].value == 'x'):
                #the tile to the right of the current tile is valid, so store the grid coordinates in the valid tiles list
                valid_tiles.append((curr_tile.row, curr_tile.column + 1))
            if(curr_tile.row > 0 and self.tiles[curr_tile.row - 1][curr_tile.column].value == 'x'):
                #the tile above the current tile is valid, so store the grid coordinates in the valid tiles list
                valid_tiles.append((curr_tile.row - 1, curr_tile.column))

            return valid_tiles
        else:
            raise Exception("The provided current tile is not a tile within the boundaries of the board.")