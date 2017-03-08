import pygame

pygame.init()
pygame.display.set_caption("Dodge You Fools!!!")

#color declarations
white = (255, 255, 255)

#initializations
screen = {
    "width": 650,
    "height": 650
}
gameWindow = pygame.display.set_mode((screen['width'], screen['height']))
background_image = pygame.image.load("Assets\Images\Board_Background.png")
board_position = {
    "x": (screen['width'] / 2) - (background_image.get_rect().size[0] / 2),
    "y": (screen['height'] / 2) - (background_image.get_rect().size[1] / 2)
}

def drawBoard():
    gameWindow.blit(background_image, (board_position['x'], board_position['y']))

clock = pygame.time.Clock()

terminate = False

pImage = pygame.image.load("Assets\Images\Player.png")
pPosition = {
    "x": (screen['width'] / 2) - (pImage.get_rect().size[0] / 2),
    "y": (screen['height'] / 2) - (pImage.get_rect().size[1] / 2)
}
speed = 20

def playerTranslate(x, y):
    gameWindow.blit(pImage, (x, y))


while(not terminate):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            terminate = True

    player_x_change = 0
    player_y_change = 0

    keys = pygame.key.get_pressed()
    #check for player exiting game by hitting escape key
    if(keys[pygame.K_ESCAPE]):
        terminate = True
    #player movement checking
    if(keys[pygame.K_LEFT]):
        player_x_change -= speed
    elif(keys[pygame.K_RIGHT]):
        player_x_change += speed
    elif(keys[pygame.K_UP]):
        player_y_change -= speed
    elif(keys[pygame.K_DOWN]):
        player_y_change += speed

    pPosition['x'] += player_x_change
    pPosition['y'] += player_y_change

    gameWindow.fill(white)
    drawBoard()
    playerTranslate(pPosition['x'], pPosition['y'])
    pygame.display.update()

pygame.quit()
quit()
