import pygame
from game import Player, Enemy
from settings import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from map import Map


def game_loop():
    # Initializing pygame, setting up window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest")
    clock = pygame.time.Clock()

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

if __name__ == "__main__":
    game_loop()
