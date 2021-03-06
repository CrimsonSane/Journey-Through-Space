import os, pygame, random
import objects
import GLOBAL

# Returns a surface object which is the image
def get_image(folder, img_nme, scle):
    img = pygame.image.load(os.path.join(folder, img_nme)).convert_alpha()
    # Determine if scale needs to be changed
    if scle == (0,0):
        return img
    else:
        return pygame.transform.scale(img, scle)

# Returns the font object
def get_font(size):
    return pygame.font.Font(os.path.join('Assets','Computer Speak v0.3.ttf'),size)

# Creates moving text that displays the zone number
def create_zone_text():
    objects.Moving_text("ZONE:"+str(GLOBAL.zone_id), [GLOBAL.WIN_WIDTH/2,-10],
                        [0,GLOBAL.scroll_spd], GLOBAL.mving_txt_group)

# Creates amount of stars from passed argument
def create_stars(amount, group):
    for i in range(amount):
        objects.Star([get_image("Assets","Star0.png",(0,0)),
                      get_image("Assets","Star1.png",(0,0))],
                     [0,random.randint(1,2)], group, [0,0, 1,2])

# Creates amount of lines from passed argument
def create_lines(amount, group):
    while len(group) < amount:
        objects.Line([get_image("Assets","Line0.png",(0,0)),
                      get_image("Assets","Line1.png",(0,0)),
                      get_image("Assets","Line2.png",(0,0)),
                      get_image("Assets","Line3.png",(0,0)),
                      get_image("Assets","Line4.png",(0,0))],
                     [0,random.randint(2,4)], group, [0,0, 2,4])

# Creates amount of planets from passed argument
def create_planets(amount, group):
    for i in range(amount):
        objects.Planet([0,random.randint(1,2)], group, [0,0, 1,2])

# Creates amount of astroids from passed argument
def create_astroids(amount, group):
    for i in range(amount):
        objects.Astroid(pos=[random.randint(0,GLOBAL.WIN_WIDTH),random.randint(-GLOBAL.WIN_HEIGHT,0)],
                        imgs=[[get_image("Assets","P1-Astroid1.png",(0,0)),
                          get_image("Assets","P1-Astroid2.png",(0,0)),
                          get_image("Assets","P1-Astroid3.png",(0,0)),
                          get_image("Assets","P1-Astroid4.png",(0,0)),
                          get_image("Assets","P1-Astroid5.png",(0,0))],
                         [get_image("Assets","P2-Astroid1.png",(0,0)),
                          get_image("Assets","P2-Astroid2.png",(0,0)),
                          get_image("Assets","P2-Astroid3.png",(0,0)),
                          get_image("Assets","P2-Astroid4.png",(0,0)),
                          get_image("Assets","P2-Astroid5.png",(0,0))],
                         [get_image("Assets","P3-Astroid1.png",(0,0)),
                          get_image("Assets","P3-Astroid2.png",(0,0)),
                          get_image("Assets","P3-Astroid3.png",(0,0)),
                          get_image("Assets","P3-Astroid4.png",(0,0)),
                          get_image("Assets","P3-Astroid5.png",(0,0))],
                         [get_image("Assets","P4-Astroid1.png",(0,0)),
                          get_image("Assets","P4-Astroid2.png",(0,0)),
                          get_image("Assets","P4-Astroid3.png",(0,0)),
                          get_image("Assets","P4-Astroid4.png",(0,0)),
                          get_image("Assets","P4-Astroid5.png",(0,0))],
                         [get_image("Assets","P5-Astroid1.png",(0,0)),
                          get_image("Assets","P5-Astroid2.png",(0,0)),
                          get_image("Assets","P5-Astroid3.png",(0,0)),
                          get_image("Assets","P5-Astroid4.png",(0,0)),
                          get_image("Assets","P5-Astroid5.png",(0,0)),
                          get_image("Assets","P5-Astroid6.png",(0,0))],
                         [get_image("Assets","P6-Astroid1.png",(0,0)),
                          get_image("Assets","P6-Astroid2.png",(0,0)),
                          get_image("Assets","P6-Astroid3.png",(0,0)),
                          get_image("Assets","P6-Astroid4.png",(0,0))]],
                        group=group, spd_rng=[0,0, 1,4])

# Creates amount of scrap from passed argument
def create_scrap(amount, group):
    for i in range(amount):
        objects.Scrap(pos=[random.randint(0,GLOBAL.WIN_WIDTH),random.randint(-GLOBAL.WIN_HEIGHT,0)],
                        imgs=[[get_image("Assets","P1-Scrap1.png",(0,0)),
                               get_image("Assets","P1-Scrap2.png",(0,0)),
                               get_image("Assets","P1-Scrap3.png",(0,0)),
                               get_image("Assets","P1-Scrap4.png",(0,0)),
                               get_image("Assets","P1-Scrap5.png",(0,0))],
                              [get_image("Assets","P2-Scrap1.png",(0,0)),
                               get_image("Assets","P2-Scrap2.png",(0,0)),
                               get_image("Assets","P2-Scrap3.png",(0,0)),
                               get_image("Assets","P2-Scrap4.png",(0,0)),
                               get_image("Assets","P2-Scrap5.png",(0,0))]],
                      group=group, spd_rng=[-2,2, 1,4])

# Adds or removes astroids based off of given amount whether it is negative or positive
def add_or_remove_astroids(amount, group):
    try:
        for astroid in group:
            if amount < 0:
                for i in range(abs(amount)):
                    if astroid.pos[1] < 0:
                        astroid.kill()
            elif amount == 0:
                if astroid.pos[1] < 0:
                    astroid.kill()
                    #print("Astroid killed")
        
        create_astroids(amount, group)
    except:
        print("There are:", len(group), "Astroids")

# Adds or removes scrap based off of given amount whether it is negative or positive
def add_or_remove_scrap(amount, group):
    try:
        for scrap in group:
            if amount < 0:
                for i in range(abs(amount)):
                    if scrap.pos[1] < 0:
                        scrap.kill()
            elif amount == 0:
                if scrap.pos[1] < 0:
                    scrap.kill()
                    #print("Scrap killed")
        
        create_scrap(amount, group)
    except:
        print("There are:", len(group), "Scrap")

# Returns an integer after searching a list for a value
def get_index_frm_2d_list(lst, elems):
    # elems has to be a list of two values
    possible_indexes = []
    possible_indexes_wthout_repeat = []
    index_counts = []
    
    # Create list of possible indexes
    for r in range(len(lst)):
        for c in range(len(lst[r])):
            if lst[r][c] == elems[r]:
                possible_indexes.append(c)
    # Make a list without the repeated values
    possible_indexes_wthout_repeat = list(set(possible_indexes))
    
    # get each values count
    for index in possible_indexes_wthout_repeat:
        index_counts.append(possible_indexes.count(index))
    
    # Return the value that has the highest count
    for i in range(len(possible_indexes_wthout_repeat)):
        if max(index_counts) == index_counts[i]:     
            return possible_indexes_wthout_repeat[i]
    # Value has not been found
    return -1

# Plays sound on specified mixer
def play_sound(sound, mixer):
    pygame.mixer.Channel(mixer).play(sound)

# Returns a list of randomized songs to play that don't repeat and always has the first song play
def get_song_playlist(song_list):
    new_playlist = []
    new_playlist.append(song_list[0])
    
    while len(new_playlist) != len(song_list):
        random_song = song_list[random.randint(1,len(song_list) - 1)]
        if random_song not in new_playlist:
            new_playlist.append(random_song)
    
    return new_playlist

# Plays music and returns currently playing song
def play_music(music):
    if not pygame.mixer.music.get_busy() or GLOBAL.current_music != music:
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(loops= -1)
    
    return music

# Returns a bool on whether the text file exists
def get_txt(name):
    try:
        with open(name + ".txt") as f:
            f.close()
            return True
    except:
        return False

# Plays random music and returns currently playing song
def play_random_music():
    while 1:
        rand_song = random.randint(1,len(GLOBAL.MUSIC_TRACKS) - 1)
        if GLOBAL.current_music != GLOBAL.MUSIC_TRACKS[rand_song]:
            return play_music(GLOBAL.MUSIC_TRACKS[rand_song])

# Creates items when certain conditions are met
def create_items():
    ITEM_NAMES = ["HAMMER", "NORMAL_GUN", "RAPID_GUN", "CANNON_GUN", "SPLIT_GUN", "PIERCE_GUN", "SPREAD_GUN", "SCREW_DRIVER", "SPEED_HOOP"]
    ITEM_CHANCES = [(1,35), (1,50), (1,25), (1,30), (1,30), (1,30), (1,35), (1,35), (1,20)]
    ran_item_index = random.randint(0, len(ITEM_NAMES) - 1)
    SPAWN_INTERVAL = 15
    
    #print(round(GLOBAL.current_tick/SPAWN_INTERVAL,2), round(GLOBAL.current_tick/SPAWN_INTERVAL,2).is_integer())
    if round(GLOBAL.current_tick/SPAWN_INTERVAL,2).is_integer():
        # Grab the item's chances and determine if it can spawn
        chance_target = ITEM_CHANCES[ran_item_index][0]
        chance_amount = ITEM_CHANCES[ran_item_index][1]
        
        chance = random.randint(1,chance_amount)
        
        if chance == chance_target:
            objects.Item(ITEM_NAMES[ran_item_index], [random.randint(0,GLOBAL.WIN_WIDTH),random.randint(-GLOBAL.WIN_HEIGHT,0)],
                         [0,6], GLOBAL.item_group)
