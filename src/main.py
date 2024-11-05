import pygame
import os
from game import Player, TileMap  # Ensure TileMap is imported
from settings import *

def game_loop():
    # Initializing pygame, setting up window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest Game")
    clock = pygame.time.Clock()

    # Create player instance
    player = Player(50, 50, 5)

    # Load the tile map
    level_path = os.path.join("assets", "levels", "test_map.csv")
    print("Loading level from:", level_path)  # Debugging line
    tile_map = TileMap(level_path)

    running = True
    while running:
        # Quitting game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.movement(keys)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the map
        tile_map.draw_map(screen)

        # Draw the player
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
