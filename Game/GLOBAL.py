import os, pygame

VERSION = "0.0.5dev"

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

# Event names
SPD_HP_EVENT = pygame.USEREVENT + 1
SPD_HP_END_EVENT = pygame.USEREVENT + 2

# Define our player

# Declare sprite groups
stars_group = pygame.sprite.Group()
astroids_group = pygame.sprite.Group()
scraps_group = pygame.sprite.Group()
lazer_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
planet_group = pygame.sprite.Group()
mving_txt_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fast_lines_group = pygame.sprite.Group()

# Declare time values
clock = pygame.time.Clock()
current_tick = 0 # Initial value
speed_skip = 0

# Declare other values

# First list is scroll speed
# Second list is astroid amount
# Third list is scrap amount
ZONE_VALUES = [[1,2,2,3,3,4,4,5,5],
               [0,5,3,5,6,8,12,5,0,0],
               [0,0,5,5,10,12,15,20,20]]
ASTROID_SCORE_AMTS = [0,5,10,15,25,50,100]
SCRAP_SCORE_AMTS = [0,10,20,30,50,100,200]
SPEED_SKIP_TIME = 10_000
STAR_AMT = 90
FAST_LINE_AMT = 25
score = 0
zone_id = 1
scroll_spd = 2
start_game_ticks = 0
paused = False

# Sounds
MUSIC_TRACKS = [os.path.join("Assets", "Gaze Upon the Stars.wav"),
                os.path.join("Assets", "Nebulus.wav"),
                os.path.join("Assets", "Cosmic Glory.wav"),
                os.path.join("Assets", "Dead Space.wav"),
                os.path.join("Assets", "Travel The Galaxy.wav"),
                os.path.join("Assets", "Scrap Central.wav"),
                os.path.join("Assets", "No Hope Out Here.wav")]
# Songs that will play in each zone
ZONE_TRACKS = [MUSIC_TRACKS[1],
               MUSIC_TRACKS[2],
               MUSIC_TRACKS[3],
               MUSIC_TRACKS[4],
               MUSIC_TRACKS[5],
               MUSIC_TRACKS[6]]

# Initalize current music as the title song
current_music = MUSIC_TRACKS[0]

track_num = 0
current_playlist = []

lazer_shooting = pygame.mixer.Sound(os.path.join("Assets", "lazer.wav"))
lazer_cannon_shooting = pygame.mixer.Sound(os.path.join("Assets", "Cannon.ogg"))
lazer_hit = pygame.mixer.Sound(os.path.join("Assets", "lazerHit.wav"))
lazer_cannon_hit = pygame.mixer.Sound(os.path.join("Assets", "CannonExplode.ogg"))
astroid_explosion = pygame.mixer.Sound(os.path.join("Assets", "astroidHit.wav"))
menu_selection = pygame.mixer.Sound(os.path.join("Assets", "menuSelection.wav"))
menu_select = pygame.mixer.Sound(os.path.join("Assets", "menuSelect.wav"))
item_collect = pygame.mixer.Sound(os.path.join("Assets", "collectItem.wav"))
player_hit = pygame.mixer.Sound(os.path.join("Assets", "playerHit.wav"))

# Declare scene values
scene_strng = "MAIN_SCENE"

