import pygame
import Tile

tile_size = 660 / 3
tile_offset = tile_size / 2

white = (255, 255, 255)
black = (0, 0, 0)

class Tileset:
    tiles = []
    status = -1


    def __init__(self, tiles_):
        for row in range(len(tiles_)):
            self.tiles.append([])
            for cell in range(len(tiles_[row])):
                if(tiles_[row][cell] == 'x'):
                    color = black
                else:
                    color = white
                self.tiles[row].append(Tile.Tile(tiles_[row][cell], cell * tile_offset * 2, row * tile_offset * 2, tile_size, tile_size, color, color))


    def update(self, window, status):
        self.status = status
        for row in range(len(self.tiles)):
            for cell in range(len(self.tiles[row])):
                if(self.tiles[row][cell].getValue() != 'x'):
                    print("found!")
                    self.tiles[row][cell].setValue(self.status)
                self.tiles[row][cell].update()

                #update all tiles
                self.showTile(self.tiles[row][cell], window)

    def showTile(self, tile, window):
        pygame.draw.rect(window, tile.fill_color, pygame.Rect(tile.x, tile.y, tile.height, tile.width), 0)
        pygame.draw.rect(window, tile.border_color, pygame.Rect(tile.x, tile.y, tile.height, tile.width), tile.border_width)
