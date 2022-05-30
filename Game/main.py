# Created by Crimson Sane
# Journey Through Space Game
# This is a complete redo of the old and unorganized codebase

import os, pygame, random

# Initialize mixer before everything else
pygame.mixer.pre_init(44100, 32, 1, 512)
pygame.mixer.init()

# Outside py scripts that handle other things
import objects
import GLOBAL
import generalized_functions as gen_func

FPS = 60

pygame.font.init()
pygame.init()

# Setup the settings from Settings.txt
settings_obj = objects.Setting()
settings_obj.setup_settings()

# Menus
MENUS = {"main": objects.Menu("MAIN", settings_obj),
         "settings": objects.Menu("SETTINGS", settings_obj),
         "pause": objects.Menu("PAUSE", settings_obj),
         "game settings": objects.Menu("GAME_SETTINGS", settings_obj),
         "death": objects.Menu("PLAYER_DEATH", settings_obj),
         "error": objects.Menu("ERROR", settings_obj)}

# Timer for zone updater
zone_timer = objects.Timer()

# Game display
game_display = pygame.Surface((GLOBAL.WIN_WIDTH,GLOBAL.WIN_HEIGHT))
# Actual display
window_display = pygame.display.set_mode((settings_obj.resolution[0], settings_obj.resolution[1]),
                                         pygame.RESIZABLE | pygame.DOUBLEBUF, 16)

# Set window icon and caption name
pygame.display.set_caption("Journey Through Space")
pygame.display.set_icon(gen_func.get_image("Assets","Icon.png", (0,0)))

def main():
    
    # Activate debug mode if file exists
    debug = gen_func.get_txt("DEBUG_MODE")
    
    # Create the stars
    gen_func.create_stars(GLOBAL.STAR_AMT, GLOBAL.stars_group)
    
    # Create planets
    gen_func.create_planets(4, GLOBAL.planet_group)
    
    # Create the player ship
    player = objects.Player_space_ship([int(GLOBAL.WIN_WIDTH/2),GLOBAL.WIN_HEIGHT -100],
                                       gen_func.get_image("Assets","SpaceShip.png", (0,0)))
    
    # Dictionary containing the objects to update and draw
    objs_dict = {"STARS": GLOBAL.stars_group, "PLANETS": GLOBAL.planet_group, "PLAYER": player, "LAZERS": GLOBAL.lazer_group,
                 "ASTROIDS": GLOBAL.astroids_group, "SCRAPS": GLOBAL.scraps_group, "EXPLOSIONS": GLOBAL.explosion_group,
                 "ITEMS": GLOBAL.item_group, "MOVING_TXT": GLOBAL.mving_txt_group, "LINES": GLOBAL.fast_lines_group}
    menu_obj_order = ["STARS", "PLANETS", "LINES"]
    game_obj_order = ["STARS", "PLANETS", "PLAYER", "LAZERS", "ASTROIDS", "SCRAPS", "EXPLOSIONS", "ITEMS", "MOVING_TXT", "LINES"]
    
    running = True
    
    while running:
        
        GLOBAL.current_tick = pygame.time.get_ticks()
        
        # Get user input:
        player_keys = get_user_keys(settings_obj)
        
        # Process user input:
        if player_keys == "QUIT" or GLOBAL.scene_strng == "QUIT":
            running = False
        
        window_display.blit(get_scaled_window_display(window_display)[0], get_scaled_window_display(window_display)[1])
        update_sound_vols()

        if GLOBAL.scene_strng == "MAIN_SCENE":
            # Run main_scene
            GLOBAL.current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[0])
            # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
            main_scene(player_keys, objs_dict, menu_obj_order, debug)
            
        elif GLOBAL.scene_strng == "SETTING_SCENE":
            # Run settings_scene
            GLOBAL.current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[0])
            # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
            settings_scene(player_keys, objs_dict, menu_obj_order, debug)
            
        # If configuring a setting
        elif "CONFIGURE_" in GLOBAL.scene_strng:
            # Run configuration_scene
            GLOBAL.current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[0])
            # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
            configuration_scene(player_keys, objs_dict, menu_obj_order, debug)
            
        elif GLOBAL.scene_strng == "RELOAD_GAME":
            # Reload and reopen game_scene
            reload_scene(player)
            
        elif GLOBAL.scene_strng == "GAME_SCENE":
            # Run game_scene
            # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
            game_scene(player_keys, objs_dict, game_obj_order, debug)
            
        elif GLOBAL.scene_strng == "PAUSE_SCENE" or GLOBAL.scene_strng == "GAME_SETTING_SCENE":
            # Run pause_scene
            # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
            pause_scene(player_keys, objs_dict, game_obj_order, debug)
            
        elif GLOBAL.scene_strng == "GAME_OVER_SCENE":
            # Run game_over_scene
            
            # 5 second delay before playing
            
            # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
            game_over_scene(player_keys, objs_dict, game_obj_order, debug)
            
        else:
            # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
            unknown_scene(player_keys)
    
    # After leaving the loop lets close the window down
    pygame.quit()


def get_scaled_display(current_disply):
    """
    HD display resolution: 1920, 1080
    Game resolution: 1200, 900
    
    1920 / 1200 = 1.6
    1080 / 900 = 1.2
     
    """
    # Scale of the current display to game display
    win_scale = (current_disply.get_width() / GLOBAL.WIN_WIDTH,
                 current_disply.get_height() / GLOBAL.WIN_HEIGHT)
    
    # If width scale is greater than height scale
    if win_scale[0] > win_scale[1]:
        working_scale = win_scale[1]
        scaled_game_display = pygame.transform.scale(game_display, (int(GLOBAL.WIN_WIDTH * working_scale),
                                                                    int(GLOBAL.WIN_HEIGHT * working_scale)))
        #(1920 - (1200 * working_scale))/2 = to the halfway point of the screen
        
        win_pos = (window_display.get_width() - int(GLOBAL.WIN_WIDTH * working_scale))/2
        return scaled_game_display, (win_pos,0)
        #window_display.blit(scaled_game_display, (win_pos,0))
    else:
        working_scale = win_scale[0]
        scaled_game_display = pygame.transform.scale(game_display, (int(GLOBAL.WIN_WIDTH * working_scale),
                                                                    int(GLOBAL.WIN_HEIGHT * working_scale)))
        #(1920 - (1200 * working_scale))/2 = to the halfway point of the screen
        
        win_pos = (window_display.get_width() - int(GLOBAL.WIN_WIDTH * working_scale))/2
        return scaled_game_display, (win_pos,0)


def get_scaled_window_display(win_disply):
    
    if settings_obj.fullscreen != settings_obj.latest_fulscrn:
        if settings_obj.fullscreen:
            window_display = pygame.display.set_mode((settings_obj.resolution[0], settings_obj.resolution[1]),
                                                     pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)
            settings_obj.latest_fulscrn = settings_obj.fullscreen
        else:
            win_disply = pygame.display.set_mode((win_disply.get_width(), win_disply.get_height()),
                                                     pygame.RESIZABLE | pygame.DOUBLEBUF, 16)
            settings_obj.latest_fulscrn = settings_obj.fullscreen
    
    scaled_display = get_scaled_display(win_disply)
    return scaled_display[0], scaled_display[1]


def pause_scene(user_inpt, obj_lst, obj_order, debug):
    # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    if GLOBAL.scene_strng == "PAUSE_SCENE":
        MENUS["pause"].update(user_inpt)
    else:
        MENUS["game settings"].update(user_inpt)
    
    # Process user input:
    update_objects(obj_lst, obj_order, user_inpt)
    
    zone_updater()

    if "PAUSE" in user_inpt:
        GLOBAL.paused = False
        GLOBAL.menu_selection.play()
        GLOBAL.scene_strng = "GAME_SCENE"
    
    # Output objects:
    draw_objects(obj_lst, obj_order, game_display)
    
    if GLOBAL.scene_strng == "PAUSE_SCENE":
        pygame.draw.rect(game_display, (0,0,0), pygame.Rect(GLOBAL.WIN_WIDTH/3,(GLOBAL.WIN_HEIGHT/3) -100,400,400))
        MENUS["pause"].draw(game_display)
        scene_title = gen_func.get_font(69).render("PAUSED",1,(255,255,255))
        game_display.blit(scene_title, scene_title.get_rect(center = (int(GLOBAL.WIN_WIDTH / 2),255)))
    elif GLOBAL.scene_strng == "GAME_SETTING_SCENE":
        pygame.draw.rect(game_display, (0,0,0), pygame.Rect(GLOBAL.WIN_WIDTH/4,0,600,700))
        MENUS["game settings"].draw(game_display)
        scene_title = gen_func.get_font(69).render("SETTINGS",1,(255,255,255))
        game_display.blit(scene_title, scene_title.get_rect(center = (int(GLOBAL.WIN_WIDTH / 2),105)))

    display_health(obj_lst["PLAYER"].health, game_display)
    score_txt = gen_func.get_font(36).render("Score: {:,}".format(GLOBAL.score),1,(255,255,255))
    game_display.blit(score_txt, score_txt.get_rect(center = (int(GLOBAL.WIN_WIDTH/2),36)))
    display_gun(obj_lst["PLAYER"], game_display)
    draw_debug_screen(debug, obj_lst["PLAYER"], game_display)


def unknown_scene(user_inpt):
    # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    MENUS["error"].update(user_inpt)
    
    game_display.fill((0,0,0)) # Fills background to black
    error_img = gen_func.get_image("Assets","ERROR.png", (420,345))
    
    MENUS["error"].draw(game_display)
    game_display.blit(error_img, error_img.get_rect(center = (int(GLOBAL.WIN_WIDTH/2), int(GLOBAL.WIN_HEIGHT/2) - 235)))
    display_version()


def reload_scene(plyer):
    # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
    
    GLOBAL.paused = False
    GLOBAL.zone_id = 1
    GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][1]
    
    plyer.health = 3
    plyer.upgrade = 0
    plyer.latest_health = plyer.health
    plyer.display_player = True
    plyer.lazer_type = "PLAYER_NORM_LAZER"
    plyer.lazer_cooldown = plyer.LAZER_COOLDOWNS[0]
    plyer.pos[0] = int(GLOBAL.WIN_WIDTH/2)

    GLOBAL.astroids_group.empty()
    GLOBAL.scraps_group.empty()
    GLOBAL.mving_txt_group.empty()
    GLOBAL.lazer_group.empty()
    GLOBAL.item_group.empty()
    gen_func.create_astroids(GLOBAL.ZONE_VALUES[1][1], GLOBAL.astroids_group)
    GLOBAL.start_game_ticks = GLOBAL.current_tick
    GLOBAL.score = 0
    gen_func.create_zone_text()
    
    #GLOBAL.current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[1])
    GLOBAL.current_playlist.clear()
    set_music()
    GLOBAL.scene_strng = "GAME_SCENE"


def set_music():
    # Set playlist if empty
    if len(GLOBAL.current_playlist) == 0 or GLOBAL.track_num >= len(GLOBAL.current_playlist) - 1:
        GLOBAL.current_playlist = gen_func.get_song_playlist(GLOBAL.ZONE_TRACKS)
        GLOBAL.track_num = 0
    else:
        GLOBAL.track_num += 1
        #print(GLOBAL.track_num)
    GLOBAL.current_music = gen_func.play_music(GLOBAL.current_playlist[GLOBAL.track_num])


def zone_updater():
    ZONE_CHANGE_TIME = 120000
    cur_time, tar_time = zone_timer.start(GLOBAL.start_game_ticks, (ZONE_CHANGE_TIME * GLOBAL.zone_id) - GLOBAL.speed_skip)
    
    #print(cur_time, tar_time, "Paused Tick:", zone_timer.paused_tick)
    
    if cur_time >= tar_time:
        # Determines if the zone will do additional actions
        if GLOBAL.zone_id < len(GLOBAL.ZONE_VALUES[0]) - 1:
            #GLOBAL.current_music = gen_func.play_random_music()
            set_music()
            GLOBAL.zone_id += 1
            
            GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][GLOBAL.zone_id]
            astroid_amt = GLOBAL.ZONE_VALUES[1][GLOBAL.zone_id] - GLOBAL.ZONE_VALUES[1][GLOBAL.zone_id - 1]
            scrap_amt = GLOBAL.ZONE_VALUES[2][GLOBAL.zone_id] - GLOBAL.ZONE_VALUES[2][GLOBAL.zone_id - 1]
            
            gen_func.add_or_remove_astroids(astroid_amt, GLOBAL.astroids_group)
            gen_func.add_or_remove_scrap(scrap_amt, GLOBAL.scraps_group)
            
            gen_func.create_zone_text()
            GLOBAL.speed_skip = 0
            #print(GLOBAL.zone_id)
        else:
            # Increase the zone there is no more values to add
            #GLOBAL.current_music = gen_func.play_random_music()
            set_music()
            GLOBAL.zone_id += 1
            GLOBAL.speed_skip = 0


def game_scene(user_inpt, obj_lst, obj_order, debug):
    # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, obj_order, user_inpt)
    
    gen_func.create_items()
    zone_updater()
    
    # Add the lines
    if GLOBAL.scroll_spd >= 5:
        gen_func.create_lines(GLOBAL.FAST_LINE_AMT, GLOBAL.fast_lines_group)
    
    # display game over if dead
    if obj_lst["PLAYER"].health <= 0:
        GLOBAL.scene_strng = "GAME_OVER_SCENE"
    
    if "PAUSE" in user_inpt:
        GLOBAL.paused = True
        GLOBAL.menu_selection.play()
        GLOBAL.scene_strng = "PAUSE_SCENE"
    
    # Output objects:
    draw_objects(obj_lst, obj_order, game_display)
    display_health(obj_lst["PLAYER"].health, game_display)
    display_upgrade_bar(obj_lst["PLAYER"].upgrade, game_display)
    
    #tool_txt = gen_func.get_font(22).render("Press A, D or arrow keys to move. Press J or enter to shoot",1,(255,255,255))
    #game_display.blit(tool_txt, tool_txt.get_rect(center = (int(GLOBAL.WIN_WIDTH/2),GLOBAL.WIN_HEIGHT - 22)))
    score_txt = gen_func.get_font(36).render("Score: {:,}".format(GLOBAL.score),1,(255,255,255))
    game_display.blit(score_txt, score_txt.get_rect(center = (int(GLOBAL.WIN_WIDTH/2),36)))
    display_gun(obj_lst["PLAYER"], game_display)
    draw_debug_screen(debug, obj_lst["PLAYER"], game_display)


def display_gun(plyr, display):
    OFFSET = 84
    MED_OFFSET = 64
    LOW_OFFSET = 20
    gun_imgs = [gen_func.get_image('Assets','BasicLazerGun.png', (OFFSET,OFFSET)),
                gen_func.get_image('Assets','RapidFireLazerGun.png', (OFFSET,OFFSET)),
                gen_func.get_image('Assets','CannonLazerGun.png', (OFFSET,OFFSET)),
                gen_func.get_image('Assets','SplitLazerGun.png', (OFFSET,OFFSET)),
                gen_func.get_image('Assets','PiercingLazerGun.png', (OFFSET,OFFSET)),
                gen_func.get_image('Assets','SpreadLazerGun.png', (OFFSET,OFFSET))]
    WEAPONS = ["PLAYER_NORM_LAZER",
               "PLAYER_RAPID_LAZER",
               "PLAYER_CANNON_LAZER",
               "PLAYER_SPLIT_LAZER",
               "PLAYER_PIERCE_LAZER",
               "PLAYER_SPREAD_LAZER"]
    
    ui_pos = (GLOBAL.WIN_WIDTH - OFFSET, GLOBAL.WIN_HEIGHT - OFFSET)
    
    for i in range(len(WEAPONS)):
        if plyr.lazer_type == WEAPONS[i]:
            display.blit(gun_imgs[i], ui_pos)
            y_pos_offset = (MED_OFFSET + LOW_OFFSET) - MED_OFFSET * (plyr.lazer_cooldown / plyr.LAZER_COOLDOWNS[i])
    
            cooldwn_bar_pos = [[GLOBAL.WIN_WIDTH - OFFSET, GLOBAL.WIN_HEIGHT - LOW_OFFSET],
                       [GLOBAL.WIN_WIDTH - OFFSET, GLOBAL.WIN_HEIGHT - y_pos_offset]]
            pygame.draw.line(display, (255,255,255), cooldwn_bar_pos[0], cooldwn_bar_pos[1], 6)


def game_over_scene(user_inpt, obj_lst, obj_order, debug):
    # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, obj_order, user_inpt)
    MENUS["death"].update(user_inpt)
    
    # Output objects:
    draw_objects(obj_lst, obj_order, game_display)
    
    MENUS["death"].draw(game_display)
    score_txt = gen_func.get_font(36).render("Your score: {:,}".format(GLOBAL.score),1,(255,255,255))
    game_display.blit(score_txt, score_txt.get_rect(center = (int(GLOBAL.WIN_WIDTH/2),(GLOBAL.WIN_HEIGHT/2)-110)))
    scene_title = gen_func.get_font(96).render("YOU DIED",1,(255,255,255))
    game_display.blit(scene_title, scene_title.get_rect(center = (int(GLOBAL.WIN_WIDTH / 2),(GLOBAL.WIN_HEIGHT/2)-215)))
    draw_debug_screen(debug, obj_lst["PLAYER"], game_display)


def update_sound_vols():
    GLOBAL.lazer_shooting.set_volume(settings_obj.sound_volume/100)
    GLOBAL.lazer_hit.set_volume(settings_obj.sound_volume/100)
    GLOBAL.astroid_explosion.set_volume(settings_obj.sound_volume/100)
    GLOBAL.menu_selection.set_volume(settings_obj.sound_volume/100)
    GLOBAL.menu_select.set_volume(settings_obj.sound_volume/100)
    GLOBAL.item_collect.set_volume(settings_obj.sound_volume/100)
    GLOBAL.player_hit.set_volume(settings_obj.sound_volume/100)
    
    pygame.mixer.music.set_volume(settings_obj.music_volume/100)


def settings_scene(user_inpt, obj_lst, obj_order, debug):
    # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, obj_order, user_inpt)
    MENUS["settings"].update(user_inpt)
    
    # Output objects:
    draw_objects(obj_lst, obj_order, game_display)
    MENUS["settings"].draw(game_display)
    
    scene_title = gen_func.get_font(69).render("SETTINGS",1,(255,255,255))
    game_display.blit(scene_title, scene_title.get_rect(center = (int(GLOBAL.WIN_WIDTH / 2),105)))
    
    display_version()


def main_scene(user_inpt, obj_lst, obj_order, debug):
    # SCENE_NAME_scene(player_input, object_list, obj_order, debug)
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, obj_order, user_inpt)
    MENUS["main"].update(user_inpt)
    
    # Output objects:
    draw_objects(obj_lst, obj_order, game_display)
    MENUS["main"].draw(game_display)
    
    ship_img = gen_func.get_image("Assets","Sterlton-17.png", (290,220))
    title_img = gen_func.get_image("Assets","Journey Through Space.png", (850,100))
    game_display.blit(title_img, title_img.get_rect(center = (int(GLOBAL.WIN_WIDTH/2), int(GLOBAL.WIN_HEIGHT/2) - 135)))
    game_display.blit(ship_img, ship_img.get_rect(center = (int(GLOBAL.WIN_WIDTH/2), int(GLOBAL.WIN_HEIGHT/2) - 305)))
    display_version()


def display_version():
    ver_txt = gen_func.get_font(16).render(GLOBAL.VERSION, 1, (255,255,255))
    game_display.blit(ver_txt, ver_txt.get_rect(topleft = (5,5)))


def display_health(health_amt, surface):
    SIZE = (24,28)
    HEALTH_DISPLY_Y = GLOBAL.WIN_HEIGHT - 40
    HEALTH_DISPLY_XS = [5,25,45,65,95,115,135,155]
    
    IMAGE = gen_func.get_image("Assets","I.png", SIZE)
    
    # Display health text
    health_txt = gen_func.get_font(24).render("HEALTH: ",1,(255,255,255))
    surface.blit(health_txt, health_txt.get_rect(midleft = (5,HEALTH_DISPLY_Y - 20)))
    
    # Display tallies
    for d in range(health_amt):
        surface.blit(IMAGE,(HEALTH_DISPLY_XS[d],HEALTH_DISPLY_Y))


def display_upgrade_bar(upgrade_amt, surface):
    SIZE = (192, 28)
    POS = (int(GLOBAL.WIN_WIDTH/2),GLOBAL.WIN_HEIGHT - 16)
    
    if upgrade_amt == 1:
        upgrade_img = gen_func.get_image("Assets","Upgrade_bar0.png", SIZE)
        surface.blit(upgrade_img, upgrade_img.get_rect(center = POS))
        
    elif upgrade_amt == 2:
        upgrade_img = gen_func.get_image("Assets","Upgrade_bar1.png", SIZE)
        surface.blit(upgrade_img, upgrade_img.get_rect(center = POS))
        
    elif upgrade_amt == 3:
        upgrade_img = gen_func.get_image("Assets","Upgrade_bar2.png", SIZE)
        surface.blit(upgrade_img, upgrade_img.get_rect(center = POS))
        
    elif upgrade_amt == 4:
        upgrade_img = gen_func.get_image("Assets","Upgrade_bar3.png", SIZE)
        surface.blit(upgrade_img, upgrade_img.get_rect(center = POS))


def draw_debug_screen(is_debug, plyer, surface):
    if is_debug:
        # Draw rectangles 
        pygame.draw.rect(surface, (255,0,0), plyer.rect, 2)
        pygame.draw.rect(surface, (0,0,255), plyer.shield_rect, 2)
        draw_objects_rects(surface, (255,0,0), GLOBAL.astroids_group, 2)
        draw_objects_rects(surface, (255,255,0), GLOBAL.explosion_group, 2)
        
        # Get text of game values
        tick_txt = gen_func.get_font(16).render("current game ticks: "+str(GLOBAL.current_tick),1,(255,255,255))
        fps_txt = gen_func.get_font(16).render("current game FPS: "+str(GLOBAL.clock.get_fps()),1,(255,255,255))
        player_pos_txt = gen_func.get_font(16).render("player position: "+str(plyer.pos),1,(255,255,255))
        astroid_num_txt = gen_func.get_font(16).render("astroid amount: "+str(len(GLOBAL.astroids_group)),1,(255,255,255))
        scroll_spd_txt = gen_func.get_font(16).render("current scroll speed: "+str(GLOBAL.scroll_spd),1,(255,255,255))
        zone_id_txt = gen_func.get_font(16).render("zone id: "+str(GLOBAL.zone_id),1,(255,255,255))
        
        # Display those in game values
        surface.blit(tick_txt, tick_txt.get_rect(midleft = (20,20)))
        surface.blit(fps_txt, fps_txt.get_rect(midleft = (20,45)))
        surface.blit(player_pos_txt, player_pos_txt.get_rect(midleft = (20,70)))
        surface.blit(astroid_num_txt, astroid_num_txt.get_rect(midleft = (20,95)))
        surface.blit(scroll_spd_txt, scroll_spd_txt.get_rect(midleft = (20,120)))
        surface.blit(zone_id_txt, zone_id_txt.get_rect(midleft = (20,145)))


def draw_objects_rects(surface, color, group, rect_val):
    for r in group:
        pygame.draw.rect(surface, color, r, rect_val)


def update_objects(objs, obj_order, plyr_keys):
    for key in obj_order:
        try:
            if objs.get(key) != None:
                objs[key].update(plyr_keys)
                
            else:
                print(objs.get(key))
                print(key, "Key does not exist in objects dictionary")
            
        except Exception as error:
            print("An error has occured: ", error)


def draw_objects(objs, obj_order, disply):
    disply.fill((0,0,0)) # Fills background to black
    
    for key in obj_order:
        try:
            if objs.get(key) != None:
                
                # If it is a sprite group
                if type(objs[key]) == pygame.sprite.Group:
                    
                    # Draw sprites in group
                    for sprite in objs[key].sprites():
                        sprite.draw(disply)
                else:
                    objs[key].draw(disply)
                
            else:
                print(objs.get(key))
                print(key, "Key does not exist in objects dictionary")
            
        except Exception as error:
            print("An error has occured: ", error)


def get_user_keys(setng_obj):
    key_button = ""
    
    # Get pygame events
    for event in pygame.event.get():
        
        # Allows the user to close the game
        if event.type == pygame.QUIT:
            print("User quit the game.")
            return "QUIT"
        
        if event.type == pygame.KEYDOWN:
            for i in range(len(setng_obj.shoot)):
                if event.key == setng_obj.shoot[i]:
                    key_button += "ENTER"
                
            for i in range(len(setng_obj.pause)):
                if event.key == setng_obj.pause[i]:
                    key_button += "PAUSE"
    
    # Assign key_button a string of the pressed key
    for i in range(len(setng_obj.move_left)):
        if pygame.key.get_pressed()[setng_obj.move_left[i]]:
            key_button += "LEFT"
    
    for i in range(len(setng_obj.move_right)):
        if pygame.key.get_pressed()[setng_obj.move_right[i]]:
            key_button += "RIGHT"
        
    for i in range(len(setng_obj.move_up)):
        if pygame.key.get_pressed()[setng_obj.move_up[i]]:
            key_button += "UP"
        
    for i in range(len(setng_obj.move_down)):
        if pygame.key.get_pressed()[setng_obj.move_down[i]]:
            key_button += "DOWN"
        
    for i in range(len(setng_obj.shoot)):
        if pygame.key.get_pressed()[setng_obj.shoot[i]]:
            key_button += "SHOOT"
        
    return key_button


if __name__ == "__main__":
    main()
