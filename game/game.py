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

        # HUD
        self.hud = HUD(self.width, self.height)
        
        # world
        self.world = World(self.hud, TILES, TILES, self.width, self.height)

        # camera
        self.camera = Camera(self.width, self.height)

        
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
        self.world.draw(self.win, self.camera)

        # Cart
        # tile = tile_dict['cart_tile']        
        # rect = pg.Rect(tile[0][0], tile[0][1], TS, TS)
        # pg.draw.rect(self.win, 'blue', rect, 1)

        # Iso
        # poly = tile_dict['iso_poly']
        # poly = [(x + self.width / 2, y + self.height / 4) for x, y in poly]
        # pg.draw.polygon(self.win, 'red', poly, 1)
        
        self.hud.draw(self.win)        
        draw_text(self.win, (10, 10), f'fps={self.clock.get_fps() :.1f}', 25, 'white')


        pg.display.flip()
        