from Application import Application
import pygame

pygame.init()

def main():
    game = Application()
    try:
        game.run()
    except Exception as err:
        print(str(err) + "Caused by " + str(err.__cause__) + " and \n" + str(err.__traceback__))


main()
pygame.quit()
quit()