# reqs
import pygame as pg

# local
from .settings import SCROLL_SPEED

class Camera:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.dx, self.dy = 0, 0
        self.scroll = pg.math.Vector2()        
        self.speed = SCROLL_SPEED


    def update(self):
        mouse_pos = pg.mouse.get_pos()

        # horizontal
        if mouse_pos[0] > self.width * 0.97:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.03:
            self.dx = self.speed
        else:
            self.dx = 0

        # vertical
        if mouse_pos[1] > self.height * 0.97:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.03:
            self.dy = self.speed
        else:
            self.dy = 0

        # udpate camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy

        
    