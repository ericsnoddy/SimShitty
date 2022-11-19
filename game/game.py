# std lib
import sys

# reqs
import pygame as pg

# local
from .settings import FPS, TS, TILES
from .utils import draw_text
from .world import World
from .camera import Camera
from .hud import HUD

class Game:
    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.width, self.height = self.win.get_size()
        
        # world
        self.world = World(TILES, TILES, self.width, self.height)

        # camera
        self.camera = Camera(self.width, self.height)

        # HUD
        self.hud = HUD(self.width, self.height)


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
        self.camera.update()
        self.hud.update()


    def draw(self):
        self.win.fill('black')

        # can blit a surface that already has blits on it! This helps performance b/c only rendered once!
        self.win.blit(self.world.grass_tiles, (self.camera.scroll.x, self.camera.scroll.y))

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
                    grass_tiles = self.world.grass_tiles
                    img = self.world.tile_images[tile_key]
                    self.win.blit(img, (render_pos[0] + grass_tiles.get_width() / 2 + self.camera.scroll.x, 
                                render_pos[1] - (img.get_height() - TS) + self.camera.scroll.y))

                # poly = tile_dict['iso_poly']
                # # offset polygon so shows more than half
                # poly = [(x + self.width / 2, y + self.height / 4) for x, y in poly]
                # pg.draw.polygon(self.win, 'red', poly, 1)
        
        self.hud.draw(self.win)
        
        draw_text(self.win, (10, 10), f'fps={self.clock.get_fps() :.1f}', 25, 'white')


        pg.display.flip()
        