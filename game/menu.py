# std lib
import sys

# reqs
import pygame as pg

# local
from .utils import draw_text


class StartMenu:

    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.win_size = self.win.get_size()


    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw()
        return True


    def update(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.menu_running = False
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def draw(self):

        self.win.fill((0, 0, 0))

        draw_text(self.win,
                (0, self.win_size[1]*0.3),
                'City building tutorial',
                100,
                (255, 255, 255))

        draw_text(self.win,
                (0, self.win_size[1]*0.5),
                'ENTER to play',
                60,
                (255, 255, 255))

        pg.display.flip()



class GameMenu:
    def __init__(self, screen, clock):
        self.win = screen
        self.clock = clock
        self.win_size = self.win.get_size()
        self.playing = True

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw()
        return self.playing

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.menu_running = False
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.menu_running = False

    def draw(self):

        self.win.fill((0, 0, 0))

        draw_text(self.win,
                (0, self.win_size[1]*0.3),
                'PAUSE',
                100,
                (255, 255, 255))

        draw_text(self.win,
                (0, self.win_size[1]*0.5),
                'ESC to quit, ENTER to play',
                60,
                (255, 255, 255))

        pg.display.flip()

