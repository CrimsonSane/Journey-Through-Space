import os, pygame

VERSION = "0.0.1"

# Declare game window width and height
WIN_WIDTH = 1200
WIN_HEIGHT = 900

# Declare common resolutions
# Top is width bottom is height
RESOLUTIONS = [[720,720,1280,1200,1600,1920,1920,3840],
               [480,576, 720, 900, 900,1080,1200,2160]]

# Declare sprite groups
player_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()
astroids_group = pygame.sprite.Group()
lazer_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
mving_txt_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

# Declare time values
clock = pygame.time.Clock()
current_tick = 0 # Initial value

# Declare other values

# First list is scroll speed
# Second list is astroid amount
ZONE_VALUES = [[1,2,3,4,4,4],
               [0,5,7,10,12,15]]
ASTROID_SCORE_AMTS = [0,5,10,15,25,50,100]
MUSIC_TRACKS = []
score = 0
zone_id = 1
scroll_spd = 2
start_game_ticks = 0
pause_ticks = 0

# Declare scene values
scene_strng = "MAIN_SCENE"