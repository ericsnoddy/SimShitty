# std lib
import sys

# reqs
import pygame as pg

# local
from game.game import Game


def main():
    running, playing = True, True
    win, clock = pg_init()
    
    # init menus

    # implement game
    game = Game(win, clock)

    while running:

        # start menu
        pass

        while playing:

            # game loop
            game.run()
    

def pg_init():
    pg.init()
    # pg.mixer.init()
    return pg.display.set_mode((0, 0), pg.FULLSCREEN), pg.time.Clock()


if __name__ == '__main__':
    main()