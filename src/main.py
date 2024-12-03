import pygame
from game import Player, Enemy, Wave, Item
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, FPS
from map import Map
import time
import random


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alchemists Quest")
    clock = pygame.time.Clock()

    player = Player(640, 640, 2)
    game_map = Map(
        "assets/levels/test_map2_Background layer.csv",
        tile_spritesheet="assets/img/spritesheet.png",
    )

    wave_number = 1
    wave = Wave(wave_number)
    next_wave_time = time.time() + 5

    font = pygame.font.Font(None, 96)
    wave_display_time = 2
    wave_start_display = True
    wave_text_start_time = time.time()

    game_over = False
    healing_items = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            player.movement(keys)

            if pygame.mouse.get_pressed()[0]:
                player.shoot()

            screen.fill((0, 0, 0))

            game_map.draw(screen)

            player.draw(screen)
            player.update_bullets(screen, wave.enemies)
            # Draw the crosshair
            mouse_x, mouse_y = pygame.mouse.get_pos()
            crosshair_size = 10
            pygame.draw.line(screen, (10, 10, 10), (mouse_x - crosshair_size, mouse_y), (mouse_x + crosshair_size, mouse_y), 2)
            pygame.draw.line(screen, (10, 10, 10), (mouse_x, mouse_y - crosshair_size), (mouse_x, mouse_y + crosshair_size), 2)

            for healing_item in healing_items[:]:
                healing_item.draw(screen)

                if healing_item.check_collision(player):
                    player.health = 100
                    healing_items.remove(healing_item)
                    break

            if wave_start_display:
                wave_text = font.render(f"Wave {wave_number}", True, (0, 0, 0))
                screen.blit(
                    wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 20)
                )
                if time.time() - wave_text_start_time > wave_display_time:
                    wave_start_display = False

            current_time = time.time()
            if wave.is_wave_complete and current_time >= next_wave_time:
                wave_number += 1
                wave = Wave(wave_number)
                healing_items = [
                    Item(
                        random.randint(50, SCREEN_WIDTH - 50),
                        random.randint(50, SCREEN_HEIGHT - 50),
                        (200, 238, 200),
                    )
                ]
                next_wave_time = current_time + 5

                wave_start_display = True
                wave_text_start_time = current_time

            wave.update(player, screen)
            wave.draw(screen)

            if player.health <= 0:
                game_over = True

            player.draw_health_bar(screen)
            player.draw_dash_cooldown(screen)

        if game_over:
            screen.fill((0, 0, 0))

            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(
                game_over_text,
                (
                    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                    SCREEN_HEIGHT // 3,
                ),
            )

            restart_text = font.render(
                "Press R to Restart or Q to Quit", True, (255, 255, 255)
            )
            screen.blit(
                restart_text,
                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2),
            )

            pygame.display.flip()

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                        if event.key == pygame.K_r:
                            game_loop()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    game_loop()
