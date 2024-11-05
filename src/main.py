# main.py
import pygame
from game import Player
from settings import *
from map import Map


def game_loop():
    # Initializing pygame, setting up window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest Game")
    clock = pygame.time.Clock()

    # Load the player and map
    player = Player(50, 50, player_speed)
    game_map = Map(map_file="assets/levels/test_map.csv", tile_folder="assets/img")

    running = True
    while running:
        # Quitting game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        player.movement(keys)

        # Render everything
        screen.fill((0, 0, 0))  # Clear the screen
        game_map.draw(screen)  # Draw the map
        player.draw(screen)  # Draw the player

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
