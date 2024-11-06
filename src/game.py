import pygame
import os
import csv
import math
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()


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
            self.x < player.x + player.width
            and self.x + self.width > player.x
            and self.y < player.y + player.height
            and self.y + self.height > player.y
        )
