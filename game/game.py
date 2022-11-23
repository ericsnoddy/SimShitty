# std lib
import sys

# reqs
import pygame as pg

# local
from .settings import FPS, TS, TILES
from .data import game_images
from .utils import draw_text
from .world import World
from .camera import Camera
from .hud import HUD
from .resource_manager import ResourceManager
from .workers import Worker

class Game:
    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.width, self.height = self.win.get_size()

        # entities
        self.entities = []

        # resource manager
        self.resource_manager = ResourceManager()

        # HUD
        self.hud = HUD(self.resource_manager, self.width, self.height, game_images)
        
        # world
        self.world = World(self.entities, self.resource_manager, self.hud, TILES, TILES, self.width, self.height, game_images)
        for _ in range(10): Worker(self.world, self.world.world[int(TILES // 2)][int(TILES // 2)], game_images)

        # camera
        scroll_start_x = (self.width - self.world.grass_tiles.get_width()) / 2  # map center
        scroll_start_y = (self.height - self.world.grass_tiles.get_height()) / 4  # map center
        scroll_start_x, scroll_start_y = 0, 0
        self.camera = Camera(self.width, self.height, (scroll_start_x, scroll_start_y))

        
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
                    self.playing = False


    def update(self):
        self.camera.update()
        for e in self.entities: e.update()
        self.hud.update()
        self.world.update(self.camera)


    def draw(self):
        self.win.fill('black')
        self.world.draw(self.win, self.camera)        
        self.hud.draw(self.win)        
        draw_text(self.win, (10, 10), f'fps={self.clock.get_fps() :.1f}', 25, 'white')
        mpos = pg.mouse.get_pos()
        x, y = self.world.mouse_to_grid(mpos[0], mpos[1], self.camera.scroll)
        draw_text(self.win, (10, 40), 
            f'(pgx,pgy)={mpos}, cam.off=({self.camera.scroll.x}, {self.camera.scroll.y}), mtg=({x}, {y}) ',
            25, 'white')
        pg.display.flip()
        