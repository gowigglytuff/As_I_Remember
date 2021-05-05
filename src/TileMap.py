import pygame, csv, os
from spritesheet import Spritesheet

class Tilling(object):
    def __init__ (self, image, x, y):
        # self.image = Spritesheet(image).image_at((0, 0, 32, 40)),
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


    def draw_tile(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, tile1, tile2):
        self.tile_size = 32
        self.tile_style_list = {"grass": "assets/csv_maps/csv_tiles/grass_tile.png", "water": "assets/csv_maps/csv_tiles/water2_tile.png"}
        self.start_x, self.start_y = 0, 0
        self.tiles = self.load_tiles(filename, tile1, tile2)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()


    def return_map(self):
        # surface.blit(self.map_surface, (0, 0))
        return self.map_surface

    def load_map(self):
        for tile in self.tiles:
            tile.draw_tile(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename, tile1, tile2):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == "0":
                    tiles.append(Tilling(self.tile_style_list[tile1], x * self.tile_size, y * self.tile_size))
                elif tile == "1":
                    tiles.append(Tilling(self.tile_style_list[tile2], x * self.tile_size, y * self.tile_size))
                x +=1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

class TileSet(object):
    def __init__(self, filename, number_of_tiles, tile_width, tile_height):
        pass