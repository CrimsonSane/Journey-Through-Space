import os, pygame

VERSION = "0.0.3dev"

# Declare game window width and height
WIN_WIDTH = 1200
WIN_HEIGHT = 900

# Declare common resolutions
# Top is width bottom is height
RESOLUTIONS = [[720,720,1280,1200,1600,1920,1920,3840],
               [480,576, 720, 900, 900,1080,1200,2160]]

# Audio channels
PLAYER_CHANNEL = 0
LAZER_CHANNEL = 1
LAZER_HIT_CHANNEL = 2
EXPLOSION_CHANNEL = 3

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
score = 0
zone_id = 1
scroll_spd = 2
start_game_ticks = 0
pause_ticks = 0

# Sounds
MUSIC_TRACKS = [os.path.join("Assets", "Gaze Upon the Stars.wav"),
                os.path.join("Assets", "Nebulus.wav")]

lazer_shooting = pygame.mixer.Sound(os.path.join("Assets", "lazer.wav"))
lazer_hit = pygame.mixer.Sound(os.path.join("Assets", "lazerHit.wav"))
astroid_explosion = pygame.mixer.Sound(os.path.join("Assets", "astroidHit.wav"))
menu_selection = pygame.mixer.Sound(os.path.join("Assets", "menuSelection.wav"))
menu_select = pygame.mixer.Sound(os.path.join("Assets", "menuSelect.wav"))
item_collect = pygame.mixer.Sound(os.path.join("Assets", "collectItem.wav"))
player_hit = pygame.mixer.Sound(os.path.join("Assets", "playerHit.wav"))

# Declare scene values
scene_strng = "MAIN_SCENE"