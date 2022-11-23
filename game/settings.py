FPS = 60
TS = TILESIZE = 64
TILES = 50
SCROLL_SPEED = 25

# HUD
HUD_COLOR = (198, 155, 93, 175)  # includes alpha value for slight transparency
RSRC_SCALE = (1, 0.03)  # HUD as percent of screen width/height
BLDG_SCALE = (0.15, 0.25)  # HUD as percent of screen width/height
SELECT_SCALE = (0.3, 0.20) # HUD as percent of screen width/height
EXAM_PAD_L = 40  # px border padding left
EXAM_PAD_T = 25  # px border padding top
EXAM_IMG_SCALE = 0.70  # scaling of obj inside examination HUD
EXAM_FONT_SIZE = 40
HUD_PAD = 0.01  # as percent of screen width/height
BLDG_ITEM_PAD = 10  # px between elements
RSRC_PAD_RIGHT = 225  # px from right
RSRC_PAD_ITEM = 125  # px between elements
RSRC_FONT_SIZE = 30
RSRC_FONT_COLOR = 'white'  # resource inventory top of screen
VALID_BLD_COLOR = 'white'  # can place building 
INVALID_BLD_COLOR = 'red'  # cannot place building
EXAM_OBJ_COLOR = 'yellow' # examining object
EXAM_FONT_COLOR = 'white'  # HUD text
SELECTED_BORDER = 2  # outline thickness
PLACEMENT_ALPHA = 100  # placement item transparency

# resource management
RESOURCES = {
    'wood': 10,
    'stone': 10
    }

COSTS = {
    'lumbermill': {'wood': 7, 'stone': 3},
    'masonry': {'wood': 3, 'stone': 5}
}
COOLDOWN_WOOD = 2000  # timer for wood collection
COOLDOWN_STONE = 4000  # timer for stone collection
WORKER_PATH_RATE = 1000  # timer for new position pathfinding
