import pygame
import csv


class Map:
    def __init__(self, csv_file, tileset_image, tile_size):
        self.tile_size = tile_size
        self.tileset = pygame.image.load(tileset_image).convert_alpha()
        self.map_data = self.load_csv(csv_file)
        self.tiles = self.load_tiles()

    def load_csv(self, filename):
        """Loads the CSV file and returns a 2D list of integers"""
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
        """Draws the map based on the CSV data"""
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile_id in enumerate(row):
                if tile_id >= 0:  # -1 or any invalid ID can be ignored
                    tile = self.tiles[tile_id]
                    screen.blit(tile, (col_idx * self.tile_size, row_idx * self.tile_size))