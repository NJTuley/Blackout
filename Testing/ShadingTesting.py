import pygame
import Tilesets_Dict
import Tileset
import random

pygame.init()

#START CODE
def main():
    tileset = Tileset.Tileset(Tilesets_Dict.tilesets['single'][15])
    tiles = [] #list to hold all tiles on the board

    black = (0,0,0)
    white = (255,255,255)
    red = (255, 0, 0)

    num_rows = 3 #number of rows in board grid
    num_cols = 3 #number of columns in board grid

    board_size = {"height": 660, "width": 660} #size of the screen
    tile_size = {"height": board_size['height'] / num_cols, "width": board_size['width'] / num_rows} #size of tiles on board
    #set offsets for each tile to space them evenly on board
    tile_offset_x = tile_size['width'] / 2
    tile_offset_y = tile_size['height'] / 2

    window = pygame.display.set_mode((board_size['height'], board_size['width']))

    terminate = False

    clock = pygame.time.Clock()

    for i in range(num_rows):
        tiles.append([])
        for j in range(num_cols):
            tiles[i].append(pygame.Rect(j*tile_offset_x * 2, i*tile_offset_y * 2, tile_size['height'], tile_size['width']))

    counter = 0
    lib_num = 0
    status = 2
    while(not terminate):
        if(counter % 20 == 0):
            old_tileset = tileset
            while (old_tileset == tileset):
                tileset = Tileset.Tileset(Tilesets_Dict.tilesets['single'][random.randint(0, len(Tilesets_Dict.tilesets['single']) - 1)])


        clock.tick(10)



        decrement = int(counter / 20) #amount to change color by
        main_color = (255 - decrement, 255 - decrement, 255 - decrement)

        #check for if the user wants to terminate program
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user hits red x button
                terminate = True
            if event.type == pygame.KEYDOWN: #user presses escape
                if(event.key == pygame.K_ESCAPE):
                    terminate = True
                #if(event.key == pygame.K_SPACE):
                    """if(lib_num >= len(Tilesets_Dict.tilesets['single'])):
                        lib_num = 0
                    else:"""


        key = pygame.key.get_pressed()

        if(key[pygame.K_SPACE]):
            lib_num = random.randint(0, len(Tilesets_Dict.tilesets['single']) - 1)

        #reset window view
        window.fill(red)
        #draw shapes
        """for i in range(num_cols):
            for j in range(num_rows):
                #decide if rectangle is red or white
                if(Tilesets_Dict.tilesets['single'][lib_num][i][j] == ''):
                    this_color = white
                else:
                    this_color = main_color
                #draw the rectangles for each tile on the board with updated shading and colors
                pygame.draw.rect(window, this_color, tiles[i][j], 0)"""

        if(counter % 20 == 0):
            status = 2
        elif(counter % 5 == 0):
            if(status >= 0):
                status -= 1
        tileset.update(window, status)
        pygame.display.update()
        counter += 1


    pygame.quit()
    quit()

main()