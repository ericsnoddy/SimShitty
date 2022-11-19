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
        self.world = self.create_world()
        self.tile_images = self.load_images()


    def create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.tile_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
        return world


    def tile_to_world(self, grid_x, grid_y):
        # turn grid coords into screen coords
        # Cartesian tile
        cart_tile = [
            (grid_x * TS, grid_y * TS),
            (grid_x * TS + TS, grid_y * TS),
            (grid_x * TS + TS, grid_y * TS + TS),
            (grid_x * TS, grid_y * TS + TS)
        ]
        # isometric polygon tile
        iso_poly = [self.cart_to_iso(x, y) for x, y in cart_tile]

        tile_data = {
            'grid': [grid_x, grid_y],
            'cart_tile': cart_tile,
            'iso_poly': iso_poly
        }
        return tile_data

    
    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y


    def load_images(self):
        block = pg.image.load('../assets/grpahics/block.png')
        tree = pg.image.load('../assets/grpahics/tree.png')
        rock = pg.image.load('../assets/grpahics/rock.png')
        return {'block': block, 'tree': tree, 'rock': rock}