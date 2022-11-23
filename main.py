# reqs
import pygame as pg

# local
from game.game import Game
from game.menu import StartMenu, GameMenu


def main():
    running, playing = True, True
    pg.init()
    # pg.mixer.init()
    win = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    
    # implement menus
    start_menu = StartMenu(win, clock)
    game_menu = GameMenu(win, clock)

    # implement game
    game = Game(win, clock)

    while running:

        # start menu
        playing = start_menu.run()

        while playing:

            # game loop
            game.run()

            # pause loop
            playing = game_menu.run()
    

if __name__ == '__main__':
    main()