# reqs
import pygame as pg

# local
from .data import IMAGES


class LumberMill:
    def __init__(self, pos):
        self.name = 'lumbermill'
        self.image = IMAGES[self.name].convert_alpha()        
        self.rect = self.image.get_rect(topleft = pos)
        self.counter = 0  # debug


    def update(self):
        self.counter += 1



class Masonry:
    def __init__(self, pos):
        self.name = 'masonry'
        self.image = IMAGES[self.name].convert_alpha()        
        self.rect = self.image.get_rect(topleft = pos)
        self.counter = 0  # debug


    def update(self):
        self.counter += 1