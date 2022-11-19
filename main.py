# std lib
import sys

# reqs
import pygame as pg

# local
from game.game import Game


def main():
    running, playing = True, True
    pg.init()
    # pg.mixer.init()
    win = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    
    # init menus

    # implement game
    game = Game(win, clock)

    while running:

        # start menu
        pass

        while playing:

            # game loop
            game.run()
    

if __name__ == '__main__':
    main()