# std lib
from random import randint

# reqs
import pygame as pg
import noise

# local
from .settings import TS, PLACEMENT_ALPHA, VALID_BLD_COLOR, INVALID_BLD_COLOR, EXAM_OBJ_COLOR, SELECTED_BORDER
from .utils import draw_text

class World:
    def __init__(self, hud, grid_length_x, grid_length_y, width, height):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width, self.height = width, height

        # Perlin-scale randomness
        self.perlin_scale = self.grid_length_x / 2

        #  size of grass surface derived from Cart-to-Iso conversion
        w = self.grid_length_x * TS * 2  # because x-range is [-lengthx * TS, lengthx * TS]
        h = self.grid_length_y * TS  # because y-range is [0, lengthy * TS]
        self.grass_tiles = pg.Surface((w, h + 2 * TS)).convert_alpha()  # 2 * TS padding
        self.tile_images = self.load_images()
        self.world = self.create_world()  # contains tile info for world grid

        self.temp_tile = None
        self.tile_to_examine = None


    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:  # right click
            self.tile_to_examine = None
            self.hud.examined_tile = None
            
        grid_x, grid_y = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

        self.temp_tile = None        

        if self.hud.selected_tile:

            if self.can_place_tile(grid_x, grid_y):
                img = self.hud.selected_tile['image'].copy()
                img.set_alpha(PLACEMENT_ALPHA)

                render_pos = self.world[grid_x][grid_y]['render_pos']
                iso_poly = self.world[grid_x][grid_y]['iso_poly']
                collision = self.world[grid_x][grid_y]['collision']

                self.temp_tile = {
                    'image': img,
                    'render_pos': render_pos,
                    'iso_poly': iso_poly,
                    'collision': collision
                }
                if mouse_action[0] and not collision:
                    # update world with our new tile
                    self.world[grid_x][grid_y]['tile'] = self.hud.selected_tile['name']
                    self.world[grid_x][grid_y]['collision'] = True
                    # de-select the item
                    self.hud.selected_tile = None
        else:
            # similar to above
            if self.can_place_tile(grid_x, grid_y):
                # if collision True, there is an obj in that spot                
                collision = self.world[grid_x][grid_y]['collision']
                if mouse_action[0] and collision:
                    self.tile_to_examine = (grid_x, grid_y)
                    self.hud.examined_tile = self.world[grid_x][grid_y]


    def draw(self, win, camera):
        # can blit a surface that already has blits on it! This helps performance b/c only rendering once!
        win.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        '''
        # DEBUG DRAW GRID
        grass_tiles_rect = self.grass_tiles.get_rect(topleft = (camera.scroll.x, camera.scroll.y))        
        world_rect = [
            (0, 0),
            (0, self.grid_length_x * TS),
            (self.grid_length_x * TS, self.grid_length_y * TS),
            (self.grid_length_x * TS, 0)
        ]
        xoff = camera.scroll.x + self.grass_tiles.get_width() / 2
        yoff = camera.scroll.y

        iso_poly = [self.cart_to_iso(x, y) for x, y in world_rect]
        world_rect = [(x + xoff, y + yoff) for x, y in world_rect]
        iso_poly = [(x + xoff, y + yoff) for x, y in iso_poly]

        # draw grass_tiles surface
        pg.draw.rect(win, 'green', grass_tiles_rect, 3)

        # draw Cartesian grid
        for x in range(1, self.grid_length_x):
            for y in range(1, self.grid_length_y + 1):                
                pg.draw.line(win, 'blue', (x * TS + xoff, yoff), (x * TS + xoff, y * TS + yoff), 1)
                pg.draw.line(win, 'blue', (xoff, y * TS + yoff), (self.grid_length_x * TS + xoff, y * TS + yoff), 1)

        
        # draw Cartesian (world) grid outline
        pg.draw.lines(win, 'blue', True, world_rect, 3)

        # draw Iso grid
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                p = self.world[x][y]["iso_poly"]
                p = [(x + xoff, y + yoff) for x, y in p]
                # Cart
                # draw_text(win, (x * TS + xoff, y * TS + yoff), f'({x}, {y})', 15, 'red')
                # Iso
                # draw_text(win, self.cart_to_iso(x * TS + xoff, y* TS + yoff), f'({x}, {y})', 15, 'blue')
                pg.draw.polygon(win, 'red', p, 1)      

        # # draw screen outline
        # win_rect = win.get_rect(topleft = (0, 0))
        # pg.draw.rect(win, 'white', win_rect, 2)


        ## END DEBUG
        '''        

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                tile_dict = self.world[x][y]

                # images
                render_pos = tile_dict['render_pos']
                tile_key = tile_dict['tile']                

                if tile_key:
                    img = self.tile_images[tile_key]
                    off_x = render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x
                    off_y = render_pos[1] - (img.get_height() - TS) + camera.scroll.y
                    win.blit(img, (off_x, off_y))

                    if self.tile_to_examine:
                        if (x == self.tile_to_examine[0]) and (y == self.tile_to_examine[1]):
                            # create a mask and convert to a list of points of its outline
                            mask = pg.mask.from_surface(self.tile_images[tile_key]).outline()
                            # apply offset to align mask with the image
                            mask = [(x + off_x, y + off_y) for x, y in mask]
                            pg.draw.polygon(win, EXAM_OBJ_COLOR, mask, SELECTED_BORDER)                            

        if self.temp_tile:
            # extract data
            img = self.temp_tile['image']
            render_pos = self.temp_tile['render_pos']
            iso_poly = self.temp_tile['iso_poly']
            # add offset to poly - no image_height adjustment for iso poly tile
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]

            # color depending on validity of placement
            if self.temp_tile['collision']:
                pg.draw.polygon(win, INVALID_BLD_COLOR, iso_poly, 3)
            else:
                pg.draw.polygon(win, VALID_BLD_COLOR, iso_poly, 3)

            # add offset and scroll from tile_key blit above
            pos_x = render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x
            pos_y = render_pos[1] - (img.get_height() - TS) + camera.scroll.y
            win.blit(img, (pos_x, pos_y))


    def create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):  # 0 -> grid_length_x - 1
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                render_pos = world_tile['render_pos']
                # apply x-offset so all x-vals >= 0
                self.grass_tiles.blit(self.tile_images['block'], (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        return world


    def grid_to_world(self, grid_x, grid_y):
        # turn grid coords into screen coords
        # Cartesian tile
        cart_rect = [
            (grid_x * TS, grid_y * TS),
            (grid_x * TS + TS, grid_y * TS),
            (grid_x * TS + TS, grid_y * TS + TS),
            (grid_x * TS, grid_y * TS + TS)
        ]
        # isometric polygon tile
        iso_poly = [self.cart_to_iso(x, y) for x, y in cart_rect]

        # get x closest to left and y closest to top for our blit pos
        # thus objs are drawn left to right, top to bottom (y-sorting)
        minx, miny = min([x for x, _ in iso_poly]), min([y for _, y in iso_poly])

        # random scene generation
        r = randint(1, 100)
        # perlin, in short, gives us a more natural randomness for forest
        perlin = noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale) * 100

        if (perlin >= 15) or (perlin <= -35):
            tile = 'tree'
        else:
            if r == 1: tile = 'tree'
            elif r == 2: tile = 'rock'
            else: tile = ''
        
        return {
            'grid': [grid_x, grid_y],
            'cart_rect': cart_rect,
            'iso_poly': iso_poly,
            'render_pos': [minx, miny],
            'tile': tile,
            'collision': (False if not tile else True)
        }

    
    def mouse_to_grid(self, x, y, scroll):
        # convert Cart (x, y) to Iso coords
        # first we remove camera scroll and above x-offset
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y

        # convert Iso to Cart - reverse of cart_to_iso()
        cart_x = (world_x + 2 * world_y) / 2  
        cart_y = (2 * world_y - world_x) / 2
        # cart_x = cart_y + world_x # this also works
        
        # convert Cart to grid and return
        grid_x = int(cart_x // TS)
        grid_y = int(cart_y // TS)
        return grid_x, grid_y


    def cart_to_iso(self, x, y):
        # std Cart to Iso conversion fmla
        iso_x = x - y
        iso_y = (x + y) / 2        
        return iso_x, iso_y


    def can_place_tile(self, grid_x, grid_y):

        # Cannot place over HUDs
        mouse_on_panel = False
        for rect in [self.hud.rsrc_rect, self.hud.bldg_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True

        # Cannot place out of bounds (also restricts index out of range error for grid_x, grid_y)
        world_bounds = (0 <= grid_x < self.grid_length_x) and (0 <= grid_y < self.grid_length_y)

        return True if world_bounds and not mouse_on_panel else False


    def load_images(self):
        return {
            'block': pg.image.load('assets/graphics/block.png').convert_alpha(),
            'building1': pg.image.load('assets/graphics/building01.png').convert_alpha(), 
            'building2': pg.image.load('assets/graphics/building02.png').convert_alpha(), 
            'tree': pg.image.load('assets/graphics/tree.png').convert_alpha(), 
            'rock': pg.image.load('assets/graphics/rock.png').convert_alpha()
        }