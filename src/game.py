import pygame
import math
import time
import random
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Player:
    def __init__(self, x, y, speed, bullet_damage=10, fire_rate=5):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.speed = speed
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.last_hit_time = 0
        self.hit_cooldown = 1.0
        self.bullets = []
        self.bullet_damage = bullet_damage
        self.fire_rate = fire_rate
        self.last_shot_time = 0
        self.speed_boost_end_time = 0
        #  Dashing logic
        self.is_dashing = False
        self.dash_speed = speed * 3
        self.dash_time = 0.2
        self.dash_cooldown = 2
        self.last_dash = 0
        self.dash_direction = (0, 0)
        # Speed boost logic
        self.speed_boost = 0
        self.is_speed_boosting = False
        self.speed_boost_end_time = 0
        # Damage boost logic
        self.damage_boost = 0
        self.is_damage_boosting = False
        self.damage_boost_end_time = 0



    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            direction = (
                mouse_x - (self.x + self.width // 2),
                mouse_y - (self.y + self.height // 2),
            )
            distance = math.hypot(direction[0], direction[1])
            if distance != 0:
                direction = (direction[0] / distance, direction[1] / distance)

            if self.is_damage_boosting:
                bullet_damage = self.bullet_damage * self.damage_boost
                bullet_color = (255, 0, 0)
            else:
                bullet_damage = self.bullet_damage
                bullet_color = (255, 255, 0)

            bullet = Bullet(
                self.x + self.width // 2,
                self.y + self.height // 2,
                direction,
                5,
                bullet_damage,
                bullet_color,
            )
            self.bullets.append(bullet)
            self.last_shot_time = current_time    

    def update(self, screen, enemies):
        current_time = time.time()

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw(screen)

            for enemy in enemies[:]:
                if bullet.check_collision(enemy):
                    enemy.take_damage(bullet.damage)
                    self.bullets.remove(bullet)
                    break

            # Remove bullet if it has exceeded its duration
            if current_time - bullet.creation_time > bullet.duration:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

        # Reset damage boost if duration has ended
        if self.is_damage_boosting and time.time() > self.damage_boost_end_time:
            self.is_damage_boosting = False
            self.damage_boost = 0
            print("Damage boost ended")

        # Reset speed boost if duration has ended
        if self.is_speed_boosting and time.time() > self.speed_boost_end_time:
            self.is_speed_boosting = False
            self.speed_boost = 0
            print("Speed boost ended")

    def apply_damage_boost(self, damage_boost, duration):
        self.damage_boost = damage_boost
        self.is_damage_boosting = True
        self.damage_boost_end_time = time.time() + duration
        print(f"Damage boost applied: {damage_boost} for {duration} seconds")

    def apply_speed_boost(self, speed_boost, duration):
        self.speed_boost = speed_boost
        self.is_speed_boosting = True
        self.speed_boost_end_time = time.time() + duration
        print(f"Speed boost applied: {speed_boost} for {duration} seconds")

    def movement(self, keys):
        dx = 0
        dy = 0

        if not self.is_dashing:
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
                if self.is_speed_boosting:
                    self.x += dx * (self.speed + self.speed_boost)
                    self.y += dy * (self.speed + self.speed_boost)
                else:
                    self.x += dx * self.speed
                    self.y += dy * self.speed
                self.dash_direction = (dx, dy)

            if (
                keys[pygame.K_SPACE]
                and time.time() - self.last_dash > self.dash_cooldown
            ):
                self.is_dashing = True
                self.dash_start_time = time.time()
                self.last_dash = time.time()
        else:
            if time.time() - self.dash_start_time < self.dash_time:
                if self.is_speed_boosting:
                    self.x += self.dash_direction[0] * (
                        self.dash_speed + self.speed_boost
                    )
                    self.y += self.dash_direction[1] * (
                        self.dash_speed + self.speed_boost
                    )
                else:
                    self.x += self.dash_direction[0] * self.dash_speed
                    self.y += self.dash_direction[1] * self.dash_speed
            else:
                self.is_dashing = False

        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        self.rect.topleft = (self.x, self.y)

    def take_damage(self, amount):
        self.health -= amount
        self.health = max(self.health, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.draw_line(screen)

    def draw_line(self, screen):
        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle between the player and the mouse
        angle = math.atan2(
            mouse_y - (self.y + self.height // 2), mouse_x - (self.x + self.width // 2)
        )

        # Calculate the end point of the line
        line_length = 32  # Length of the line (gun)
        end_x = self.x + self.width // 2 + math.cos(angle) * line_length
        end_y = self.y + self.height // 2 + math.sin(angle) * line_length

        pygame.draw.line(
            screen,
            (255, 0, 0),
            (self.x + self.width // 2, self.y + self.height // 2),
            (end_x, end_y),
            4,
        )

    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (10, 10, bar_width * health_percentage, bar_height),
        )

    def draw_dash_cooldown(self, screen):
        bar_width = 200
        bar_height = 10
        elapsed_time = time.time() - self.last_dash
        cooldown_percentage = min(elapsed_time / self.dash_cooldown, 1.0)
        pygame.draw.rect(screen, (100, 100, 100), (10, 40, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (10, 40, bar_width * cooldown_percentage, bar_height),
        )


class Bullet:
    def __init__(
        self,
        x,
        y,
        direction,
        speed,
        damage,
        color: tuple[int : 0 - 255, int : 0 - 255, int : 0 - 255],
    ):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.width = 5
        self.height = 5
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.creation_time = time.time()
        self.duration = 1.5  # Duration in seconds

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, enemy):
        return self.rect.colliderect(enemy.rect)


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

    def movement(self, players, enemies):
        pass

    def take_damage(self, amount):
        self.health -= amount
        self.health = max(self.health, 0)

    def is_defeated(self):
        return self.health <= 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 30
        bar_height = 3
        health_percentage = self.health / self.max_health
        pygame.draw.rect(
            screen, (255, 0, 0), (self.x, self.y - 8, bar_width, bar_height)
        )
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (self.x, self.y - 8, bar_width * health_percentage, bar_height),
        )

    def check_collision(self, other):
        return self.rect.colliderect(other.rect)


# Subclasses for Enemy
class ChasingEnemy(Enemy):
    def __init__(self, x, y, speed, health):
        super().__init__(x, y, speed, health)
        self.color = (0, 0, 0)

    def movement(self, players, enemies):
        self.move_towards_player(players, enemies)

    def move_towards_player(self, player, enemies):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx, dy = dx / distance, dy / distance

        # Checks for collision with other enemies
        for other_enemy in enemies:
            if other_enemy != self:
                dist_to_other = math.hypot(
                    other_enemy.x - self.x, other_enemy.y - self.y
                )
                if dist_to_other < 20:
                    avoid_dx = self.x - other_enemy.x
                    avoid_dy = self.y - other_enemy.y
                    avoid_length = math.hypot(avoid_dx, avoid_dy)
                    if avoid_length != 0:
                        avoid_dx, avoid_dy = (
                            avoid_dx / avoid_length,
                            avoid_dy / avoid_length,
                        )
                        dx += avoid_dx * 0.5
                        dy += avoid_dy * 0.5

        length = math.hypot(dx, dy)
        if length != 0:
            dx, dy = dx / length, dy / length

        self.x += dx * self.speed
        self.y += dy * self.speed

        self.rect.x = self.x
        self.rect.y = self.y


class RandMovingEnemy(Enemy):
    def __init__(self, x, y, speed, health):
        super().__init__(x, y, speed, health)
        self.color = (255, 122, 0)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_counter = 0
        self.border_buffer = 16  # Buffer zone near the edges

    def movement(self, player, enemies):
        self.move_randomly(enemies)

    def move_randomly(self, enemies):
        # Increase move counter
        self.move_counter += 1

        # Change direction after moving for a certain number of frames
        if self.move_counter > random.randint(6, 12) * 30:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.move_counter = 0

        dx, dy = self.direction

        # Normalize direction
        length = math.hypot(dx, dy)
        if length != 0:
            dx /= length
            dy /= length

        # Move the enemy
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Boundary check to prevent getting stuck in walls and corners
        if self.x < self.border_buffer:
            self.x = self.border_buffer
            self.direction = random.choice([(1, 0), (0, 1), (0, -1)])
            self.x += random.randint(1, 3)  # Add random offset
            self.move_counter = 0  # Reset random direction coutner
        elif self.x > SCREEN_WIDTH - self.border_buffer:
            self.x = SCREEN_WIDTH - self.border_buffer
            self.direction = random.choice([(-1, 0), (0, 1), (0, -1)])
            self.x -= random.randint(1, 3)
            self.move_counter = 0
        elif self.y < self.border_buffer:
            self.y = self.border_buffer
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1)])
            self.y += random.randint(1, 3)
            self.move_counter = 0
        elif self.y > SCREEN_HEIGHT - self.border_buffer:
            self.y = SCREEN_HEIGHT - self.border_buffer
            self.direction = random.choice([(1, 0), (-1, 0), (0, -1)])
            self.y -= random.randint(1, 3)
            self.move_counter = 0

        # Update the enemy's rectangle position
        self.rect.topleft = (self.x, self.y)


class TurretEnemy(Enemy):
    def __init__(self, x, y, speed, health):
        super().__init__(x, y, speed, health)
        self.speed = 0
        self.bullets = []
        self.fire_rate = 1  # Bullets per second
        self.last_shot_time = 0
        self.color = (160, 32, 240)

    def movement(self, players, enemies):
        pass

    def shoot(self, player):
        current_time = time.time()
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            direction = (player.x - self.x, player.y - self.y)
            distance = math.hypot(direction[0], direction[1])
            if distance != 0:
                direction = (direction[0] / distance, direction[1] / distance)

            bullet = Bullet(
                self.x + self.width // 2,
                self.y + self.height // 2,
                direction,
                speed=3,
                damage=15,
                color=self.color,
            )
            self.bullets.append(bullet)
            self.last_shot_time = current_time

    def update_bullets(self, screen, player):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw(screen)

            if bullet.check_collision(player):
                player.take_damage(bullet.damage)
                self.bullets.remove(bullet)


class FastChasingEnemy(Enemy):
    def __init__(self, x, y, speed, health):
        super().__init__(x, y, speed, health)
        self.color = (128, 128, 128)
        self.is_dashing = False
        self.is_paused = False
        self.dash_cooldown = 2  # Cooldown time in seconds
        self.last_dash_time = 0
        self.dash_duration = 0.5  # Dash duration in seconds
        self.pause_duration = 0.5  # Pause duration before dashing
        self.dash_speed = speed * 3  # Dash speed
        self.dash_direction = (0, 0)  # Initialize dash direction

    def movement(self, player, enemies):
        current_time = time.time()
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx, dy = dx / distance, dy / distance

        # Normal movement towards the player
        if not self.is_dashing and not self.is_paused:
            self.x += dx * self.speed
            self.y += dy * self.speed

        # Check if close to the player and cooldown has passed
        if distance < 50 and current_time - self.last_dash_time > self.dash_cooldown:
            self.dash_direction = (dx, dy)  # Store the direction for dashing
            self.dash_start_time = (
                current_time  # Record the time when starting the dash
            )
            self.is_paused = True
            self.last_dash_time = current_time  # Update last dash time

        # Pause before dashing
        if (
            self.is_paused
            and current_time - self.dash_start_time >= self.pause_duration
        ):
            self.is_paused = False
            self.is_dashing = True

        # Perform the dash
        if self.is_dashing:
            if (
                current_time - self.dash_start_time - self.pause_duration
                <= self.dash_duration
            ):
                self.x += self.dash_direction[0] * self.dash_speed
                self.y += self.dash_direction[1] * self.dash_speed
            else:
                self.is_dashing = False  # End the dash after the duration

        # Boundary check to prevent walking off the map
        self.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.y))

        # Collision avoidance with other enemies
        for enemy in enemies:
            if enemy != self:
                dist_to_other = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if dist_to_other < 20:
                    avoid_dx = self.x - enemy.x
                    avoid_dy = self.y - enemy.y
                    avoid_length = math.hypot(avoid_dx, avoid_dy)
                    if avoid_length != 0:
                        avoid_dx /= avoid_length
                        avoid_dy /= avoid_length
                        self.x += avoid_dx * 0.5
                        self.y += avoid_dy * 0.5

        self.rect.x = self.x
        self.rect.y = self.y


class Wave:
    def __init__(self, wave_number):
        self.wave_number = wave_number
        self.enemies = self.spawn_enemies()
        self.items = self.spawn_items()
        self.is_wave_complete = False

    def spawn_enemies(self):
        enemies = []
        base_health = 10
        base_speed = 1
        num_enemies = self.wave_number * 3

        enemy_classes = [ChasingEnemy, RandMovingEnemy, TurretEnemy, FastChasingEnemy]
        for _ in range(num_enemies):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)

            enemy_class = random.choice(enemy_classes)
            if enemy_class == FastChasingEnemy:
                health = 4 + self.wave_number * 2
                speed = 1.25 + 0.05 * self.wave_number
            else:
                health = base_health + self.wave_number * 5
                speed = base_speed + 0.05 * self.wave_number

            enemies.append(enemy_class(x, y, speed, health))

        return enemies

    def spawn_items(self):
        items = []
        num_items = self.wave_number // 2

        item_types = [HealingItem, DamageBoostItem, SpeedBoostItem]
        for _ in range(num_items):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)

            item_type = random.choice(item_types)

            if item_type == HealingItem:
                items.append(HealingItem(x, y))

            elif item_type == SpeedBoostItem:
                items.append(SpeedBoostItem(x, y, speed_boost=1.5, duration=3))

            elif item_type == DamageBoostItem:
                items.append(DamageBoostItem(x, y, damage_boost=2, duration=3))

        return items

    def update(self, player, screen):
        # Check collision for items
        for item in self.items[:]:
            if item.check_collision(player):
                item.apply_effect(player)
                self.items.remove(item)

        for enemy in self.enemies[:]:
            enemy.movement(player, self.enemies)
            if isinstance(enemy, TurretEnemy):
                enemy.shoot(player)
                enemy.update_bullets(screen, player)

            if enemy.check_collision(player):
                player.take_damage(2)
                enemy.take_damage(1)

            if enemy.is_defeated():
                self.enemies.remove(enemy)

        self.is_wave_complete = len(self.enemies) == 0

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

        for item in self.items:
            item.draw(screen)


class Items:
    def __init__(self, x, y, width=16, height=16):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pass  # To be overridden by subclasses

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)

    def apply_effect(self, player):
        pass  # To be overridden by subclasses


class HealingItem(Items):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 0, 0)

    def draw(self, screen):
        # Draw the black outline
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        # Draw the inner light green square
        pygame.draw.rect(
            screen,
            (144, 238, 144),
            pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height - 6),
        )
        # Draw the horizontal red bar
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.x + self.width // 4,
                self.y + self.height // 2 - 2,
                self.width // 2,
                4,
            ),
        )
        # Draw the vertical red bar
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.x + self.width // 2 - 2,
                self.y + self.height // 4,
                4,
                self.height // 2,
            ),
        )

    def apply_effect(self, player):
        player.health = 100


class SpeedBoostItem(Items):
    def __init__(self, x, y, speed_boost, duration):
        super().__init__(x, y)
        self.speed_boost = speed_boost
        self.duration = duration
        self.color = (255, 255, 0)

    def draw(self, screen):
        # Draw the black outline
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        # Draw the inner light green square
        pygame.draw.rect(
            screen,
            (144, 238, 144),
            pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height - 6),
        )
        # Draw two arrows pointing to the right
        arrow_width = 2
        arrow_height = 6
        arrow_spacing = 2
        for i in range(2):
            pygame.draw.polygon(
                screen,
                self.color,
                [
                    (
                        self.x + 5 + i * (arrow_width + arrow_spacing),
                        self.y + self.height // 2 - arrow_height // 2,
                    ),
                    (
                        self.x + 5 + i * (arrow_width + arrow_spacing) + arrow_width,
                        self.y + self.height // 2,
                    ),
                    (
                        self.x + 5 + i * (arrow_width + arrow_spacing),
                        self.y + self.height // 2 + arrow_height // 2,
                    ),
                ],
            )

    def apply_effect(self, player):
        player.apply_speed_boost(self.speed_boost, self.duration)


class DamageBoostItem(Items):
    def __init__(self, x, y, damage_boost, duration):
        super().__init__(x, y, 16, 16, )
        self.damage_boost = damage_boost
        self.duration = duration
        self.color = (255, 165, 0)

    def draw(self, screen):
        # Draw the black outline
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        # Draw the inner light green square
        pygame.draw.rect(
            screen,
            (144, 238, 144),
            pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height - 6),
        )
        # Draw a single red arrow pointing upwards
        arrow_width = 6
        arrow_height = 6
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width // 2 - arrow_width // 2, self.y + self.height // 2 + arrow_height // 2),
            (self.x + self.width // 2 + arrow_width // 2, self.y + self.height // 2 + arrow_height // 2),
            (self.x + self.width // 2, self.y + self.height // 2 - arrow_height // 2 - 1),
        ])

    def apply_effect(self, player):
        player.apply_damage_boost(self.damage_boost, self.duration)
