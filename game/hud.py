# reqs
import pygame as pg

# local
from .settings import (
    HUD_COLOR, 
    RSRC_HUD_SCALE, 
    BLDG_HUD_SCALE, 
    SELECT_HUD_SCALE, 
    HUD_BUFF, 
    BLDG_ITEM_BUFF, 
    RSRC_BUFF_ITEM, 
    RSRC_BUFF_RIGHT,
    PLACEMENT_ALPHA
)
from .utils import draw_text



class HUD:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.hud_color = HUD_COLOR

        # resources HUD
        self.rsrc_surf = pg.Surface((self.width * RSRC_HUD_SCALE[0], self.height * RSRC_HUD_SCALE[1]), pg.SRCALPHA)
        self.rsrc_rect = self.rsrc_surf.get_rect(topleft = (0, 0))
        self.rsrc_surf.fill(self.hud_color)

        # building HUD
        self.bldg_surf = pg.Surface((self.width * BLDG_HUD_SCALE[0], self.height * BLDG_HUD_SCALE[1]), pg.SRCALPHA)
        self.bldg_rect = self.bldg_surf.get_rect(topleft = (self.width * (1 - BLDG_HUD_SCALE[0] - HUD_BUFF), 
                                                            self.height * (1 - BLDG_HUD_SCALE[1] - HUD_BUFF)))
        self.bldg_surf.fill(self.hud_color)

        # selection HUD
        self.select_surf = pg.Surface((self.width * SELECT_HUD_SCALE[0], self.height * SELECT_HUD_SCALE[1]), pg.SRCALPHA)
        self.select_rect = self.select_surf.get_rect(topleft = (self.width * (1 - SELECT_HUD_SCALE[0]) / 2, 
                                                                self.height * (1 - SELECT_HUD_SCALE[1] - HUD_BUFF)))
        self.select_surf.fill(self.hud_color)

        # images/interaction
        self.images = self.load_images()
        self.tiles = self.create_build_hud()
        self.selected_tile = None


    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:  # right click
            self.selected_tile = None

        for tile in self.tiles:
            if tile['rect'].collidepoint(mouse_pos):
                if mouse_action[0]:  # left click
                    self.selected_tile = tile    


    def draw(self, win):

        # if self.selected_tile:
        #     img = self.selected_tile['image'].copy()
        #     img.set_alpha(PLACEMENT_ALPHA)
        #     win.blit(img, pg.mouse.get_pos())

        # resource HUD
        win.blit(self.rsrc_surf, (0,0))

        # building HUD
        win.blit(self.bldg_surf, 
                (self.width * (1 - BLDG_HUD_SCALE[0] - HUD_BUFF), 
                self.height * (1 - BLDG_HUD_SCALE[1] - HUD_BUFF)))

        # selection HUD
        win.blit(self.select_surf, 
                (self.width * (1 - SELECT_HUD_SCALE[0]) / 2, 
                self.height * (1 - SELECT_HUD_SCALE[1] - HUD_BUFF)))

        # building
        for tile in self.tiles:
            win.blit(tile['icon'], tile['rect'].topleft)

        # resources
        pos = self.width - RSRC_BUFF_RIGHT
        for resource in ['wood:', 'stone:', 'gold:']:
            draw_text(win, (pos, 0), resource, 30, 'white')
            pos += RSRC_BUFF_ITEM



    def load_images(self):
        building1 = pg.image.load('assets/graphics/building01.png').convert_alpha()
        building2 = pg.image.load('assets/graphics/building02.png').convert_alpha()
        tree = pg.image.load('assets/graphics/tree.png').convert_alpha()
        rock = pg.image.load('assets/graphics/rock.png').convert_alpha()
        return {
            'building1': building1, 
            'building2': building2, 
            'tree': tree, 
            'rock': rock
        }


    def scale_image(self, image, w=None, h=None):
        if not w and not h:
            pass
        elif not h:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif not w:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))        
        return image


    def create_build_hud(self):

        render_pos = [self.width * (1 - BLDG_HUD_SCALE[0] - HUD_BUFF) + BLDG_ITEM_BUFF,  
                      self.height * (1 - BLDG_HUD_SCALE[1] - HUD_BUFF) + BLDG_ITEM_BUFF]
        obj_width = self.bldg_surf.get_width() // 5  # 5 equal parts

        tiles = []  # all the objs

        for image_name, image in self.images.items():
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scaled = self.scale_image(image_tmp, w=obj_width)
            rect = image_scaled.get_rect(topleft = pos)
            tiles.append(
                {
                    'name': image_name,
                    'icon': image_scaled,
                    'image': self.images[image_name],
                    'rect': rect
                }
            )

            render_pos[0] += image_scaled.get_width() + BLDG_ITEM_BUFF

        return tiles