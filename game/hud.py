# reqs
import pygame as pg

# local
from .settings import (
    HUD_COLOR, 
    RSRC_SCALE, 
    BLDG_SCALE, 
    SELECT_SCALE,
    PLACEMENT_ALPHA,
    EXAM_IMG_SCALE,
    EXAM_FONT_SIZE,
    EXAM_FONT_COLOR,
    EXAM_PAD_L,
    EXAM_PAD_T,
    RSRC_FONT_SIZE,
    RSRC_FONT_COLOR,
    HUD_PAD,
    BLDG_ITEM_PAD, 
    RSRC_PAD_ITEM, 
    RSRC_PAD_RIGHT,
)
from .utils import draw_text


class HUD:
    def __init__(self, resource_manager, width, height, game_images):
        self.resource_manager = resource_manager
        self.width, self.height = width, height
        self.hud_color = HUD_COLOR
        self.images = {}
        for key in game_images.keys():
            self.images[key] = game_images[key].convert_alpha()

        # resources HUD
        self.rsrc_surf = pg.Surface((self.width * RSRC_SCALE[0], self.height * RSRC_SCALE[1]), pg.SRCALPHA)
        self.rsrc_rect = self.rsrc_surf.get_rect(topleft = (0, 0))
        self.rsrc_surf.fill(self.hud_color)

        # building HUD
        self.bldg_surf = pg.Surface((self.width * BLDG_SCALE[0], self.height * BLDG_SCALE[1]), pg.SRCALPHA)
        self.bldg_rect = self.bldg_surf.get_rect(topleft = (self.width * (1 - BLDG_SCALE[0] - HUD_PAD), 
                                                            self.height * (1 - BLDG_SCALE[1] - HUD_PAD)))
        self.bldg_surf.fill(self.hud_color)

        # selection HUD
        self.select_surf = pg.Surface((self.width * SELECT_SCALE[0], self.height * SELECT_SCALE[1]), pg.SRCALPHA)
        self.select_rect = self.select_surf.get_rect(topleft = (self.width * (1 - SELECT_SCALE[0]) / 2, 
                                                                self.height * (1 - SELECT_SCALE[1] - HUD_PAD)))
        self.select_surf.fill(self.hud_color)

        # interaction
        
        self.tiles = self.create_build_hud()
        self.selected_tile = None
        self.examined_tile = None


    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:  # right click
            self.selected_tile = None

        for tile in self.tiles:
            # flag affordability
            if self.resource_manager.is_affordable(tile['name']):
                tile['affordable'] = True
            else:
                tile['affordable'] = False
            
            # check for mouse click selection
            if tile['rect'].collidepoint(mouse_pos) and tile['affordable']:
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
                (self.width * (1 - BLDG_SCALE[0] - HUD_PAD), 
                self.height * (1 - BLDG_SCALE[1] - HUD_PAD)))

        # selection HUD - don't draw if we're examining an obj
        if self.examined_tile:
            # display the HUD window
            win.blit(self.select_surf, (self.width * (1 - SELECT_SCALE[0]) / 2, 
                                        self.height * (1 - SELECT_SCALE[1] - HUD_PAD)))

            # display the building image
            img = self.examined_tile.image.copy()
            img_scaled = self.scale_image(img, h = self.select_rect.height * EXAM_IMG_SCALE)            
            win.blit(img_scaled, ((self.width * (1 - SELECT_SCALE[0]) / 2) + EXAM_PAD_L, 
                                (self.height * (1 - SELECT_SCALE[1] - HUD_PAD)) + EXAM_PAD_T))
            
            # display the examination text
            draw_text(win, self.select_rect.topleft, self.examined_tile.name, EXAM_FONT_SIZE, EXAM_FONT_COLOR)

        # building
        for tile in self.tiles:
            icon = tile['icon'].copy()
            if not tile['affordable']:
                icon.set_alpha(PLACEMENT_ALPHA)

            win.blit(icon, tile['rect'].topleft)

        # resources
        posx = self.width - RSRC_PAD_RIGHT
        for resource, value in self.resource_manager.resources.items():
            draw_text(win, (posx, 0), f'{resource}: {str(value)}', RSRC_FONT_SIZE, RSRC_FONT_COLOR)
            posx += RSRC_PAD_ITEM


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

        render_pos = [self.width * (1 - BLDG_SCALE[0] - HUD_PAD) + BLDG_ITEM_PAD,  
                      self.height * (1 - BLDG_SCALE[1] - HUD_PAD) + BLDG_ITEM_PAD]
        obj_width = self.bldg_surf.get_width() // 5  # 5 equal parts

        tiles = []  # all the objs
        for image_name, image in self.images.items():
            if image_name in ['lumbermill', 'masonry']:
                pos = render_pos.copy()
                image_tmp = image.copy()
                image_scaled = self.scale_image(image_tmp, w=obj_width)
                rect = image_scaled.get_rect(topleft = pos)
                tiles.append(
                    {
                        'name': image_name,
                        'icon': image_scaled,
                        'image': self.images[image_name],
                        'rect': rect,
                        'affordable': True
                    }
                )

                render_pos[0] += image_scaled.get_width() + BLDG_ITEM_PAD

        return tiles