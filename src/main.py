import pygame
from game import *
from settings import *

def running(run):
    return run


def game_loop():
    # initializing pygame, setting up window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest Game")

    player = pygame.Rect((300, 250, 50, 50))

    while running(True):
        pygame.draw.rect(screen, (255, 0, 0), player)

        check_events()

        pygame.display.update()


if __name__ == "__main__":
    game_loop()
