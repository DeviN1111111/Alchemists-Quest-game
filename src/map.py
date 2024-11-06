import pygame
import csv


class Map:
<<<<<<< Updated upstream
    def __init__(self, csv_file, tileset_image, tile_size):
        self.tile_size = tile_size
        self.tileset = pygame.image.load(tileset_image).convert_alpha()
        self.map_data = self.load_csv(csv_file)
        self.tiles = self.load_tiles()

    def load_csv(self, filename):
        """Loads the CSV file and returns a 2D list of integers"""
=======
    def __init__(
        self, map_file, tile_spritesheet
    ):  # Changed from tile_folder to tile_spritesheet
        self.tile_spritesheet = tile_spritesheet  # Store the path to the spritesheet
        self.tiles = self.load_tiles()  # Load tiles using the new method
        self.map_data = self.load_map(map_file)

    def load_tiles(self):
        """Load tile images from a spritesheet."""
        tiles = {}
        spritesheet = pygame.image.load(
            self.tile_spritesheet
        ).convert()  # Use the class attribute for the spritesheet

        # Get the width and height of the spritesheet
        sheet_width, sheet_height = spritesheet.get_size()

        # Calculate the number of tiles based on the spritesheet width and TILE_SIZE
        num_tiles = sheet_width // TILE_SIZE

        # Loop through the number of tiles
        for i in range(num_tiles):
            # Calculate the position of the tile in the spritesheet
            x = (
                i * TILE_SIZE
            )  # Calculate x position based on index (since it's a single row)
            y = 0  # The y position is always 0 since it's a single row

            # Extract tile from spritesheet
            tile_image = spritesheet.subsurface(
                (x, y, TILE_SIZE, TILE_SIZE)
            )  # Extract tile from spritesheet
            tiles[i] = tile_image

        return tiles

    def load_map(self, map_file):
        """Load map data from a CSV file."""
>>>>>>> Stashed changes
        map_data = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                map_data.append([int(tile) for tile in row])
        return map_data

    def load_tiles(self):
        """Divides the tileset image into individual tile surfaces"""
        tiles = []
        tileset_width, tileset_height = self.tileset.get_size()
        for y in range(0, tileset_height, self.tile_size):
            for x in range(0, tileset_width, self.tile_size):
                tile = self.tileset.subsurface((x, y, self.tile_size, self.tile_size))
                tiles.append(tile)
        return tiles

    def draw(self, screen):
<<<<<<< Updated upstream
        """Draws the map based on the CSV data"""
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile_id in enumerate(row):
                if tile_id >= 0:  # -1 or any invalid ID can be ignored
                    tile = self.tiles[tile_id]
                    screen.blit(tile, (col_idx * self.tile_size, row_idx * self.tile_size))
=======
        """Draw the map to the screen based on the loaded data."""
        for y, row in enumerate(self.map_data):
            for x, tile_num in enumerate(row):
                if tile_num in self.tiles and tile_num != -1:  # Added check for -1
                    screen.blit(self.tiles[tile_num], (x * TILE_SIZE, y * TILE_SIZE))


class Room:
    def __init__(self, x, y, width, height, screen):
        self.x = x  # Top-left x position
        self.y = y  # Top-left y position
        self.width = width  # Room width
        self.height = height  # Room height
        self.screen = screen  # Pygame screen to draw on

        # Colors for room borders
        self.border_color = (255, 255, 255)  # White for the borders
        self.wall_thickness = 5  # Thickness of the walls

    def draw(self):
        # Draw top border
        pygame.draw.rect(
            self.screen,
            self.border_color,
            (self.x, self.y, self.width, self.wall_thickness),
        )

        # Draw bottom border
        pygame.draw.rect(
            self.screen,
            self.border_color,
            (
                self.x,
                self.y + self.height - self.wall_thickness,
                self.width,
                self.wall_thickness,
            ),
        )

        # Draw left border
        pygame.draw.rect(
            self.screen,
            self.border_color,
            (self.x, self.y, self.wall_thickness, self.height),
        )

        # Draw right border
        pygame.draw.rect(
            self.screen,
            self.border_color,
            (
                self.x + self.width - self.wall_thickness,
                self.y,
                self.wall_thickness,
                self.height,
            ),
        )
>>>>>>> Stashed changes
