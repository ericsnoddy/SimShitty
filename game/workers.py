# std lib
from random import randint

# reqs
import pygame as pg
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# local
from .settings import WORKER_PATH_RATE


class Worker:
    def __init__(self, world, tile, game_images):
        self.world = world
        self.world.entities.append(self)  # place self into entities group
        self.name = 'worker'
        image = game_images[self.name].convert_alpha()
        self.image = pg.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.tile = tile

        # pathfinding
        grid_x, grid_y = self.tile['grid'][0], self.tile['grid'][1]
        self.world.workers[grid_x][grid_y] = self  # place self into workers matrix
        self.move_timer = pg.time.get_ticks()
        self.create_path()


    def update(self):
        now = pg.time.get_ticks()
        if now - self.move_timer > 1000:
            # update pos in the world
            new_pos = self.path[self.node_index]           
            self.change_tile(new_pos)
            self.node_index += 1
            self.move_timer = now
            if self.node_index == len(self.path) - 1:
                self.create_path()


    def change_tile(self, new_tile):
        # update worker's position in the matrix
        grid_x, grid_y = self.tile['grid'][0], self.tile['grid'][1]
        new_grid_x, new_grid_y = new_tile[0], new_tile[1]

        self.world.workers[grid_x][grid_y] = None
        self.world.workers[new_grid_x][new_grid_y] = self
        self.tile = self.world.world[new_grid_x][new_grid_y]


    def create_path(self):
        searching_for_path = True
        while searching_for_path:
            x = randint(0, self.world.grid_length_x - 1)
            y = randint(0, self.world.grid_length_y - 1)

            dest_tile = self.world.world[x][y]
            if not dest_tile['collision']:
                self.grid = Grid(matrix = self.world.collision_matrix) 

                grid_x, grid_y = self.tile['grid'][0], self.tile['grid'][1]
                print(grid_x, grid_y)                          
                self.start = self.grid.node(grid_x, grid_y)
                self.end = self.grid.node(x, y)

                finder = AStarFinder(diagonal_movement = DiagonalMovement.never)
                self.node_index = 0  # how many nodes along the path
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False


    