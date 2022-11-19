# std lib
from random import randint

# reqs
import pygame as pg

# local
from .settings import TS

class World:
    def __init__(self, grid_length_x, grid_length_y, width, height):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width, self.height = width, height
        # world is a grid
        self.grass_tiles = pg.Surface((self.width, self.height))
        self.tile_images = self.load_images()
        self.world = self.create_world()


    def create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.tile_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                render_pos = world_tile['render_pos']
                self.grass_tiles.blit(self.tile_images['block'], (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1]))

        return world


    def tile_to_world(self, grid_x, grid_y):
        # turn grid coords into screen coords
        # Cartesian tile
        cart_rect = [
            (grid_x * TS, grid_y * TS),
            (grid_x * TS + TS, grid_y * TS),
            (grid_x * TS + TS, grid_y * TS + TS),
            (grid_x * TS, grid_y * TS + TS)
        ]
        # isometric polygon tile
        iso_poly = [self.cart_to_iso(x, y) for x, y in cart_rect]

        r = randint(1, 100)
        tile = ''
        if r <= 5: tile = 'tree'
        elif r <= 10: tile = 'rock'

        # get x closest to left and y closest to top for our blit pos
        # so objects are drawn left to right, top to bottom (y-sorting)
        minx = min([x for x, _ in iso_poly])
        miny = min([y for _, y in iso_poly])

        return {
            'grid': [grid_x, grid_y],
            'cart_rect': cart_rect,
            'iso_poly': iso_poly,
            'render_pos': [minx, miny],
            'tile': tile
        }

    
    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y


    def load_images(self):
        block = pg.image.load('assets/graphics/block.png').convert_alpha()
        tree = pg.image.load('assets/graphics/tree.png').convert_alpha()
        rock = pg.image.load('assets/graphics/rock.png').convert_alpha()
        return {'block': block, 'tree': tree, 'rock': rock}