import pygame
import csv
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Map:
    def __init__(self, map_file, tile_folder):
        self.tile_folder = tile_folder
        self.tiles = self.load_tiles()
        self.map_data = self.load_map(map_file)

    def load_tiles(self):
        """Load tile images and map them to tile numbers."""
        tiles = {}
        for i in range(5):  # Assuming you have 5 tiles (tile000 to tile004)
            tile_path = os.path.join(self.tile_folder, f"tile00{i}.png")
            tile_image = pygame.image.load(tile_path).convert()
            tiles[i] = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
        return tiles

    def load_map(self, map_file):
        """Load map data from a CSV file."""
        map_data = []
        with open(map_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                map_data.append([int(tile) for tile in row])
        return map_data

    def draw(self, screen):
        """Draw the map to the screen based on the loaded data."""
        for y, row in enumerate(self.map_data):
            for x, tile_num in enumerate(row):
                if tile_num in self.tiles:
                    screen.blit(self.tiles[tile_num], (x * TILE_SIZE, y * TILE_SIZE))


class Room:
    def __init__(self, x, y, width, height, screen):
        self.x = x            # Top-left x position
        self.y = y            # Top-left y position
        self.width = width    # Room width
        self.height = height  # Room height
        self.screen = screen  # Pygame screen to draw on

        # Colors for room borders
        self.border_color = (255, 255, 255)  # White for the borders
        self.wall_thickness = 5              # Thickness of the walls

    def draw(self):
        # Draw top border
        pygame.draw.rect(self.screen, self.border_color, 
                         (self.x, self.y, self.width, self.wall_thickness))

        # Draw bottom border
        pygame.draw.rect(self.screen, self.border_color, 
                         (self.x, self.y + self.height - self.wall_thickness, self.width, self.wall_thickness))

        # Draw left border
        pygame.draw.rect(self.screen, self.border_color, 
                         (self.x, self.y, self.wall_thickness, self.height))

        # Draw right border
        pygame.draw.rect(self.screen, self.border_color, 
                         (self.x + self.width - self.wall_thickness, self.y, self.wall_thickness, self.height))
