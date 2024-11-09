<<<<<<< Updated upstream
=======
import pygame
import math
import time
import random
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Bullet:
    def __init__(self, x, y, direction, speed, damage):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.width = 5
        self.height = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.damage = damage

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)

    def check_collision(self, enemy):
        return self.rect.colliderect(enemy.rect)


class Player:
    def __init__(self, x, y, speed, bullet_damage=10, fire_rate=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 16
        self.height = 16
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.last_hit_time = 0
        self.hit_cooldown = 1.0
        self.bullets = []
        self.bullet_damage = bullet_damage
        self.fire_rate = fire_rate  # Bullets per second
        self.last_shot_time = 0  # To track the last time the player shot

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= 1 / self.fire_rate:  # Only shoot if enough time has passed
            mouse_x, mouse_y = pygame.mouse.get_pos()
            direction = (mouse_x - self.x, mouse_y - self.y)
            distance = math.hypot(direction[0], direction[1])
            if distance != 0:
                direction = (direction[0] / distance, direction[1] / distance)

                bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, direction, 5, self.bullet_damage)
                self.bullets.append(bullet)
                self.last_shot_time = current_time  # Update the last shot time

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

        if dx != 0 or dy != 0:
            length = math.sqrt(dx**2 + dy**2)
            dx /= length
            dy /= length
            self.x += dx * self.speed
            self.y += dy * self.speed

        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))

    def take_damage(self, amount):
        self.health -= amount
        self.health = max(self.health, 0)


    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 5
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 5, self.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x + 5, self.y - 10, bar_width * health_percentage, bar_height))

    def update_bullets(self, screen, enemies):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw(screen)

            for enemy in enemies[:]:
                if bullet.check_collision(enemy):
                    enemy.take_damage(bullet.damage)
                    self.bullets.remove(bullet)  # Remove the bullet after collision
                    break


class Enemy:
    def __init__(self, x, y, speed, health):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.color = (0, 0, 0)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.draw_health_bar(screen)

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.x += dx * self.speed
            self.y += dy * self.speed

        self.rect.x = self.x
        self.rect.y = self.y

    def take_damage(self, amount):
        self.health -= amount
        self.health = max(self.health, 0)

    def is_defeated(self):
        return self.health <= 0

    def draw_health_bar(self, screen):
        bar_width = 30
        bar_height = 3
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 8, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 8, bar_width * health_percentage, bar_height))

    def check_collision(self, player):
        return (
            self.x < player.x + player.width
            and self.x + self.width > player.x
            and self.y < player.y + player.height
            and self.y + self.height > player.y
        )


class Wave:
    def __init__(self, wave_number):
        self.wave_number = wave_number
        self.enemies = self.spawn_enemies()
        self.is_wave_complete = False

    def spawn_enemies(self):
        enemies = []
        base_health = 10
        base_speed = 1
        num_enemies = self.wave_number * 3

        for i in range(num_enemies):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            health = base_health + self.wave_number * 5
            speed = base_speed + 0.05 * self.wave_number
            enemies.append(Enemy(x, y, speed, health))

        return enemies

    def update(self, player):
        for enemy in self.enemies[:]:
            enemy.move_towards_player(player)
            if enemy.check_collision(player):
                player.take_damage(2)
                enemy.take_damage(1)

            if enemy.is_defeated():
                self.enemies.remove(enemy)

        self.is_wave_complete = len(self.enemies) == 0

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)


import pygame

class Item:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 26
        self.height = 26
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen): #Hier draw je een rec die lijkt op een healing kit als je andere items wilt in spawnen moet je een nieuwe draw functie maken
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        pygame.draw.rect(screen, (144, 238, 144), pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height - 6))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x + self.width // 4, self.y + self.height // 2 - 2, self.width // 2, 4))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x + self.width // 2 - 2, self.y + self.height // 4, 4, self.height // 2))

    def check_collision(self, player):
        return (
            self.x < player.x + player.width
            and self.x + self.width > player.x
            and self.y < player.y + player.height
            and self.y + self.height > player.y
        )



>>>>>>> Stashed changes
