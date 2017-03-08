from Application import Application
import pygame

pygame.init()

def main():
    game = Application()
    try:
        game.run()
    except Exception as err:
        print(err)


main()
pygame.quit()
quit()