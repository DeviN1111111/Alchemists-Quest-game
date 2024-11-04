import pygame
from game import *
from settings import *


def game_loop():
    # initializing pygame, setting up window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest Game")

    player = pygame.Rect((300, 250, 50, 50))

    running = True
    while running:

        screen.fill((0, 0, 0))  # reset the screen black

        pygame.draw.rect(screen, (255, 0, 0), player)  # draw the player

        # WASD movement
        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            player.move_ip(-1, 0)

        elif key[pygame.K_d]:
            player.move_ip(1, 0)

        elif key[pygame.K_w]:
            player.move_ip(0, -1)

        elif key[pygame.K_s]:
            player.move_ip(0, 1)

        # Quitting game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
