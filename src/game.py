import pygame
import os
import csv
import math
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            image_path
        ).convert_alpha()  # Load image directly
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:
    def __init__(self, filename):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)

        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == "0":
                    tiles.append(
                        Tile(
                            "assets/img/tile000.png",
                            x * self.tile_size,
                            y * self.tile_size,
                        )
                    )
                elif tile == "1":
                    tiles.append(
                        Tile(
                            "assets/img/tile001.png",
                            x * self.tile_size,
                            y * self.tile_size,
                        )
                    )
                elif tile == "2":
                    tiles.append(
                        Tile(
                            "assets/img/tile002.png",
                            x * self.tile_size,
                            y * self.tile_size,
                        )
                    )
                elif tile == "3":
                    tiles.append(
                        Tile(
                            "assets/img/tile003.png",
                            x * self.tile_size,
                            y * self.tile_size,
                        )
                    )
                elif tile == "4":
                    tiles.append(
                        Tile(
                            "assets/img/tile004.png",
                            x * self.tile_size,
                            y * self.tile_size,
                        )
                    )
                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles


class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        # self.image = self.load.image()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def movement(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1

        # Normalize movement vector for consistent speed
        if dx != 0 or dy != 0:
            length = math.sqrt(dx**2 + dy**2)
            dx /= length  # Normalize the x component
            dy /= length  # Normalize the y component
            self.x += dx * self.speed
            self.y += dy * self.speed

        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
<<<<<<< Updated upstream
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
=======
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.color = (0, 0, 0)
        self.speed = 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.x += dx * self.speed
            self.y += dy * self.speed

    def check_collision(self, player):
        return (
            self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y < player.y + player.height and
            self.y + self.height > player.y
        )
>>>>>>> Stashed changes
