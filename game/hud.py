# reqs
import pygame as pg

# local
from .settings import HUD_COLOR, RSRC_HUD_SCALE, BLDG_HUD_SCALE, SELECT_HUD_SCALE, HUD_BUFFER

class HUD:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.hud_color = HUD_COLOR

        # resources HUD
        self.rsrc_surf = pg.Surface((self.width * RSRC_HUD_SCALE[0], self.height * RSRC_HUD_SCALE[1]), pg.SRCALPHA)
        self.rsrc_surf.fill(self.hud_color)

        # building HUD
        self.bldg_surf = pg.Surface((self.width * BLDG_HUD_SCALE[0], self.height * BLDG_HUD_SCALE[1]), pg.SRCALPHA)
        self.bldg_surf.fill(self.hud_color)

        # selection HUD
        self.select_surf = pg.Surface((self.width * SELECT_HUD_SCALE[0], self.height * SELECT_HUD_SCALE[1]), pg.SRCALPHA)
        self.select_surf.fill(self.hud_color)


    def draw(self, win):

        # resource HUD
        win.blit(self.rsrc_surf, (0,0))

        # building HUD
        win.blit(self.bldg_surf, 
                (self.width * (1 - BLDG_HUD_SCALE[0] - HUD_BUFFER), 
                self.height * (1 - BLDG_HUD_SCALE[1] - HUD_BUFFER))
        )

        # selection HUD
        win.blit(self.select_surf, 
                (self.width * (1 - SELECT_HUD_SCALE[0]) / 2, 
                self.height * (1 - SELECT_HUD_SCALE[1] - HUD_BUFFER))
        )
