# std lib
import sys

# reqs
import pygame as pg

# local
from settings import RES

class main:
    def __init__(self):
        pg.init()
        self.win = pg.display.set_mode((RES))
        self.clock = pg.time.Clock()