import pygame
import math
from game import Player
from settings import *


def game_loop():
    # Initializing pygame, setting up window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest Game")
    clock = pygame.time.Clock()
    player = Player(50, 50, 5)

    running = True
    while running:

        # Quitting game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.movement(keys)

        screen.fill((0, 0, 0))

        player.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
