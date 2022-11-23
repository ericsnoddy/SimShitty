# reqs
import pygame as pg

# local
from .settings import COOLDOWN_STONE, COOLDOWN_WOOD


class LumberMill:
    def __init__(self, pos, resource_manager, game_images):
        self.name = 'lumbermill'
        self.image = game_images[self.name].convert_alpha()        
        self.rect = self.image.get_rect(topleft = pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.cooldown_start = pg.time.get_ticks()


    def update(self):
        now = pg.time.get_ticks()
        if now - self.cooldown_start > COOLDOWN_WOOD:
            self.resource_manager.resources['wood'] += 1
            self.cooldown_start = now



class Masonry:
    def __init__(self, pos, resource_manager, game_images):
        self.name = 'masonry'
        self.image = game_images[self.name].convert_alpha()        
        self.rect = self.image.get_rect(topleft = pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.cooldown_start = pg.time.get_ticks()


    def update(self):
        now = pg.time.get_ticks()
        if now - self.cooldown_start > COOLDOWN_STONE:
            self.resource_manager.resources['stone'] += 1
            self.cooldown_start = now