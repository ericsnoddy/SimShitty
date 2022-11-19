# std lib
import sys

# reqs
import pygame as pg

# local
from .settings import FPS, TS, TILES
from .world import World

class Game:
    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.width, self.height = self.win.get_size()
        self.world = World(TILES, TILES, self.width, self.height)


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pg.event.get():            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()


    def update(self):
        pass


    def draw(self):
        self.win.fill('black')

        # can blit a surface that already has blits on it! This helps performance b/c only rendered once!
        self.win.blit(self.world.grass_tiles, (0, 0))

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                tile_dict = self.world.world[x][y]

                # tile info is a square [(topleft), (topright), (bottomleft), (bottomright)]
                # tile = tile_dict['cart_tile']
                
                # # use topleft to make a rect
                # rect = pg.Rect(tile[0][0], tile[0][1], TS, TS)
                # pg.draw.rect(self.win, 'blue', rect, 1)

                # images
                render_pos = tile_dict['render_pos']
                tile_key = tile_dict['tile']

                if tile_key:
                    img = self.world.tile_images[tile_key]
                    self.win.blit(img, (render_pos[0] + self.width /2, 
                                render_pos[1] + self.height / 4 - (img.get_height() - TS)))

                # poly = tile_dict['iso_poly']
                # # offset polygon so shows more than half
                # poly = [(x + self.width / 2, y + self.height / 4) for x, y in poly]
                # pg.draw.polygon(self.win, 'red', poly, 1)

        pg.display.flip()
        