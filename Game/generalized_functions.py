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

# Returns a start time that doesn't update during a loop
def get_start_time(start_time):
    if start_time < 0:
        start_time = GLOBAL.current_tick
    return start_time

# Returns current time and the target time
def timer(start_time, time):
    current_time = GLOBAL.current_tick - GLOBAL.pause_ticks
    target_time = start_time + time
    
    return current_time, target_time

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

# Creates amount of astroids from passed argument
def create_astroids(amount, group):
    for i in range(amount):
        objects.Astroid(pos=[random.randint(0,GLOBAL.WIN_WIDTH),random.randint(-GLOBAL.WIN_HEIGHT,0)],
                        imgs=[[get_image("Assets","P1-Astroid1.png",(0,0)),
                          get_image("Assets","P1-Astroid2.png",(0,0)),
                          get_image("Assets","P1-Astroid3.png",(0,0))],
                         [get_image("Assets","P2-Astroid1.png",(0,0)),
                          get_image("Assets","P2-Astroid2.png",(0,0)),
                          get_image("Assets","P2-Astroid3.png",(0,0))],
                         [get_image("Assets","P3-Astroid1.png",(0,0)),
                          get_image("Assets","P3-Astroid2.png",(0,0)),
                          get_image("Assets","P3-Astroid3.png",(0,0))],
                         [get_image("Assets","P4-Astroid1.png",(0,0)),
                          get_image("Assets","P4-Astroid2.png",(0,0)),
                          get_image("Assets","P4-Astroid3.png",(0,0))],
                         [get_image("Assets","P5-Astroid1.png",(0,0)),
                          get_image("Assets","P5-Astroid2.png",(0,0)),
                          get_image("Assets","P5-Astroid3.png",(0,0)),
                          get_image("Assets","P5-Astroid4.png",(0,0))],
                         [get_image("Assets","P6-Astroid1.png",(0,0)),
                          get_image("Assets","P6-Astroid2.png",(0,0)),
                          get_image("Assets","P6-Astroid3.png",(0,0)),
                          get_image("Assets","P6-Astroid4.png",(0,0))]],
                        group=group, spd_rng=[0,0, 1,4])

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
                    print("Astroid killed")
        
        create_astroids(amount, group)
    except:
        print("There are:", len(group), "Astroids")

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

# Plays music and returns currently playing song
def play_music(music, current_music):
    if not pygame.mixer.music.get_busy() or current_music != music:
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()
    
    return music

# Returns a bool on whether the text file exists
def get_txt(name):
    try:
        with open(name + ".txt") as d:
            d.close()
            return True
    except:
        return False

# Creates items when certain conditions are met
def create_items():
    ran_nums = [random.randint(1,4), random.randint(1,8)]
    ITEM_NAMES = ["HAMMER"]
    SPAWN_INTERVAL = 1500
    
    #print(round(GLOBAL.current_tick/SPAWN_INTERVAL,2), round(GLOBAL.current_tick/SPAWN_INTERVAL,2).is_integer())
    if round(GLOBAL.current_tick/SPAWN_INTERVAL,2).is_integer():
        if ran_nums[0] == ran_nums[1]:
            objects.Item(ITEM_NAMES[0], [random.randint(0,GLOBAL.WIN_WIDTH),random.randint(-GLOBAL.WIN_HEIGHT,0)],
                         [0,6], GLOBAL.item_group)
