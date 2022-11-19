# std lib
import sys

# reqs
import pygame as pg

class Game:
    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.width, self.height = self.win.get_size()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
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
        pg.display.flip()