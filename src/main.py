import pygame
<<<<<<< Updated upstream
import os
from game import * # Ensure TileMap is imported
from settings import * 
=======
from game import Player, Enemy
from settings import *
from map import Map

>>>>>>> Stashed changes

def game_loop():
    # Initializing pygame, setting up window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest Game")
    clock = pygame.time.Clock()

<<<<<<< Updated upstream
    # Create player instance
    player = Player(50, 50, 5)

    # Load the tile map
    level_path = os.path.join("assets", "levels", "test_map.csv")
    print("Loading level from:", level_path)  # Debugging line
    tile_map = TileMap(level_path)
=======
    # Load the player and map
    player = Player(16, 16, 2)
    enemy = Enemy(100, 100)
    enemy2 = Enemy(150, 100)
    enemy3 = Enemy(100, 150)
    enemy4 = Enemy(100, 200)
    game_map = Map(
        map_file="assets/levels/test_map.csv",
        tile_spritesheet="assets/img/spritesheet.png",
    )
>>>>>>> Stashed changes

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
        tile_map.load_map()

        # Draw the player
        player.draw(screen)

        # enemy movement
        enemy.move_towards_player(player)
        enemy.draw(screen)

        enemy2.move_towards_player(player)
        enemy2.draw(screen)

        enemy3.move_towards_player(player)
        enemy3.draw(screen)

        enemy4.move_towards_player(player)
        enemy4.draw(screen)

        # enemy collision detection
        if enemy.check_collision(player):
            enemy.color = (255, 255, 0)
        if enemy2.check_collision(player):
            enemy2.color = (255, 255, 0)
        if enemy3.check_collision(player):
            enemy3.color = (255, 255, 0)
        if enemy4.check_collision(player):
            enemy4.color = (255, 255, 0)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    game_loop()