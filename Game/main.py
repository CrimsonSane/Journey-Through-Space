# Created by Crimson Sane
# Journey Through Space Game
# This is a complete redo of the old and unorganized codebase

import os, pygame

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

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

# Setup the settings from Settings.txt
settings_obj = objects.Setting()
settings_obj.setup_settings()

# Menus
MENUS = [objects.Menu("MAIN", settings_obj),
         objects.Menu("SETTINGS", settings_obj),
         objects.Menu("PLAYER_DEATH", settings_obj),
         objects.Menu("ERROR", settings_obj)]

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
    gen_func.create_stars(84, GLOBAL.stars_group)
    
    # Create the player ship
    player = objects.Player_space_ship([int(GLOBAL.WIN_WIDTH/2),GLOBAL.WIN_HEIGHT -100],
                                       gen_func.get_image("Assets","SpaceShip.png", (0,0)))
    
    # Lists containing objects to update and draw
    menu_objs_list = [GLOBAL.stars_group]
    
    game_objs_list = [GLOBAL.stars_group, player, GLOBAL.lazer_group, GLOBAL.astroids_group, GLOBAL.explosion_group,
                      GLOBAL.item_group, GLOBAL.mving_txt_group]
    
    # Initalize current music as the title song
    current_music = GLOBAL.MUSIC_TRACKS[0]
    
    running = True
    
    while running:
        
        GLOBAL.current_tick = pygame.time.get_ticks()
        
        # Get user input:
        player_keys = get_user_keys(settings_obj)
        
        # Process user input:
        if player_keys == "QUIT" or GLOBAL.scene_strng == "QUIT":
            running = False
        
        set_window_display()
        update_sound_vols()
        
        if GLOBAL.scene_strng == "MAIN_SCENE":
            # Run main_scene
            current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[0], current_music)
            main_scene(player_keys, menu_objs_list, debug)
        elif GLOBAL.scene_strng == "SETTING_SCENE":
            # Run settings_scene
            current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[0], current_music)
            settings_scene(player_keys, menu_objs_list)
        elif "CONFIGURE_" in GLOBAL.scene_strng:
            # Run configuration_scene
            current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[0], current_music)
            configuration_scene(player_keys, menu_objs_list)
        elif GLOBAL.scene_strng == "RELOAD_GAME":
            # Reload and reopen game_scene
            reload_scene(player)
        elif GLOBAL.scene_strng == "GAME_SCENE":
            # Run game_scene
            current_music = gen_func.play_music(GLOBAL.MUSIC_TRACKS[1], current_music)
            game_scene(player_keys, game_objs_list, debug)
        elif GLOBAL.scene_strng == "GAME_OVER_SCENE":
            # Run game_over_scene
            game_over_scene(player_keys, game_objs_list, debug)
        else:
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

def set_window_display():
    
    global window_display
    if settings_obj.fullscreen != settings_obj.latest_fulscrn:
        if settings_obj.fullscreen:
            window_display = pygame.display.set_mode((settings_obj.resolution[0], settings_obj.resolution[1]),
                                                     pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)
            settings_obj.latest_fulscrn = settings_obj.fullscreen
        else:
            window_display = pygame.display.set_mode((window_display.get_width(), window_display.get_height()),
                                                     pygame.RESIZABLE | pygame.DOUBLEBUF, 16)
            settings_obj.latest_fulscrn = settings_obj.fullscreen
    
    scaled_display = get_scaled_display(window_display)
    window_display.blit(scaled_display[0],scaled_display[1])

def unknown_scene(user_inpt):
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    MENUS[3].update(user_inpt)
    
    game_display.fill((0,0,0)) # Fills background to black
    error_img = gen_func.get_image("Assets","ERROR.png", (420,345))
    
    MENUS[3].draw(game_display)
    game_display.blit(error_img, error_img.get_rect(center = (int(GLOBAL.WIN_WIDTH/2), int(GLOBAL.WIN_HEIGHT/2) - 235)))
    display_version()

def reload_scene(plyer):
    GLOBAL.zone_id = 1
    GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][1]
    
    plyer.health = 3
    plyer.latest_health = plyer.health
    plyer.display_player = True
    plyer.lazer_type = "PLAYER_NORM_LAZER"
    
    GLOBAL.astroids_group.empty()
    GLOBAL.mving_txt_group.empty()
    GLOBAL.lazer_group.empty()
    gen_func.create_astroids(GLOBAL.ZONE_VALUES[1][1], GLOBAL.astroids_group)
    GLOBAL.start_game_ticks = GLOBAL.current_tick
    GLOBAL.score = 0
    gen_func.create_zone_text()
    
    GLOBAL.scene_strng = "GAME_SCENE"

def zone_updater():
    ZONE_CHANGE_TIME = 120000
    cur_time, tar_time = gen_func.timer(GLOBAL.start_game_ticks, ZONE_CHANGE_TIME * GLOBAL.zone_id)
    
    if cur_time >= tar_time:
        if GLOBAL.zone_id < 5:
            GLOBAL.zone_id += 1
            GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][GLOBAL.zone_id]
            astroid_amt = GLOBAL.ZONE_VALUES[1][GLOBAL.zone_id] - GLOBAL.ZONE_VALUES[1][GLOBAL.zone_id - 1]
            
            gen_func.add_or_remove_astroids(astroid_amt, GLOBAL.astroids_group)
            
            gen_func.create_zone_text()
            #print(GLOBAL.zone_id)
        else:
            GLOBAL.zone_id += 1

def game_scene(user_inpt, obj_lst, debug):
    plyer = obj_lst[1] # Player is second on the list
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, user_inpt)
    
    gen_func.create_items()
    zone_updater()
    
    if plyer.health == 0:
        GLOBAL.scene_strng = "GAME_OVER_SCENE"
    
    # Output objects:
    draw_objects(obj_lst, game_display)
    display_health(plyer.health, game_display)
    score_txt = gen_func.get_font(36).render("Score: {:,}".format(GLOBAL.score),1,(255,255,255))
    game_display.blit(score_txt, score_txt.get_rect(center = (int(GLOBAL.WIN_WIDTH/2),36)))
    draw_debug_screen(debug, plyer, game_display)

def game_over_scene(user_inpt, obj_lst, debug):
    plyer = obj_lst[1] # Player is second on the list
    
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, user_inpt)
    MENUS[2].update(user_inpt)
    
    # Output objects:
    draw_objects(obj_lst, game_display)
    MENUS[2].draw(game_display)
    score_txt = gen_func.get_font(36).render("Score: {:,}".format(GLOBAL.score),1,(255,255,255))
    game_display.blit(score_txt, score_txt.get_rect(center = (int(GLOBAL.WIN_WIDTH/2),36)))
    draw_debug_screen(debug, plyer, game_display)

def update_sound_vols():
    GLOBAL.lazer_shooting.set_volume(settings_obj.sound_volume/100)
    GLOBAL.lazer_hit.set_volume(settings_obj.sound_volume/100)
    GLOBAL.astroid_explosion.set_volume(settings_obj.sound_volume/100)
    GLOBAL.menu_selection.set_volume(settings_obj.sound_volume/100)
    GLOBAL.menu_select.set_volume(settings_obj.sound_volume/100)
    GLOBAL.item_collect.set_volume(settings_obj.sound_volume/100)
    GLOBAL.player_hit.set_volume(settings_obj.sound_volume/100)
    
    pygame.mixer.music.set_volume(settings_obj.music_volume/100)

def settings_scene(user_inpt, obj_lst):
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, user_inpt)
    MENUS[1].update(user_inpt)
    
    update_sound_vols()
    
    # Output objects:
    draw_objects(obj_lst, game_display)
    MENUS[1].draw(game_display)
    display_version()

def main_scene(user_inpt, obj_lst, debug):
    pygame.display.update()
    GLOBAL.clock.tick(FPS)
    
    # Process user input:
    update_objects(obj_lst, user_inpt)
    MENUS[0].update(user_inpt)
    
    # Output objects:
    draw_objects(obj_lst, game_display)
    MENUS[0].draw(game_display)
    ship_img = gen_func.get_image("Assets","Sterlton-17.png", (290,220))
    title_img = gen_func.get_image("Assets","Journey Through Space.png", (850,100))
    game_display.blit(title_img, title_img.get_rect(center = (int(GLOBAL.WIN_WIDTH/2), int(GLOBAL.WIN_HEIGHT/2) - 135)))
    game_display.blit(ship_img, ship_img.get_rect(center = (int(GLOBAL.WIN_WIDTH/2), int(GLOBAL.WIN_HEIGHT/2) - 305)))
    display_version()

def display_version():
    ver_txt = gen_func.get_font(16).render(GLOBAL.VERSION, 1, (255,255,255))
    game_display.blit(ver_txt, ver_txt.get_rect(topleft = (5,5)))

def display_health(health_amt, surface):
    HEALTH_DISPLY_Y = GLOBAL.WIN_HEIGHT - 40
    HEALTH_DISPLY_XS = [5,25,45,65]
    
    IMAGE = gen_func.get_image("Assets","I.png", (24,28))
    
    for d in range(health_amt):
        surface.blit(IMAGE,(HEALTH_DISPLY_XS[d],HEALTH_DISPLY_Y))

def draw_debug_screen(is_debug, plyer, surface):
    if is_debug:
            pygame.draw.rect(surface, (255,0,0), plyer.rect, 2)
            pygame.draw.rect(surface, (0,0,255), plyer.shield_rect, 2)
            draw_objects_rects(surface, (255,0,0), GLOBAL.astroids_group, 2)
            draw_objects_rects(surface, (255,255,0), GLOBAL.explosion_group, 2)
            tick_txt = gen_func.get_font(16).render("current game ticks: "+str(GLOBAL.current_tick),1,(255,255,255))
            fps_txt = gen_func.get_font(16).render("current game FPS: "+str(GLOBAL.clock.get_fps()),1,(255,255,255))
            player_pos_txt = gen_func.get_font(16).render("player position: "+str(plyer.pos),1,(255,255,255))
            astroid_num_txt = gen_func.get_font(16).render("astroid amount: "+str(len(GLOBAL.astroids_group)),1,(255,255,255))
            scroll_spd_txt = gen_func.get_font(16).render("current scroll speed: "+str(GLOBAL.scroll_spd),1,(255,255,255))
            zone_id_txt = gen_func.get_font(16).render("zone id: "+str(GLOBAL.zone_id),1,(255,255,255))
            
            surface.blit(tick_txt, tick_txt.get_rect(midleft = (20,20)))
            surface.blit(fps_txt, fps_txt.get_rect(midleft = (20,45)))
            surface.blit(player_pos_txt, player_pos_txt.get_rect(midleft = (20,70)))
            surface.blit(astroid_num_txt, astroid_num_txt.get_rect(midleft = (20,95)))
            surface.blit(scroll_spd_txt, scroll_spd_txt.get_rect(midleft = (20,120)))
            surface.blit(zone_id_txt, zone_id_txt.get_rect(midleft = (20,145)))

def draw_objects_rects(surface, color, group, rect_val):
    for r in group:
        pygame.draw.rect(surface, color, r, rect_val)

def update_objects(objs, plyr_keys):
    for index in range(len(objs)):
        try:
            objs[index].update(plyr_keys)
        except:
            objs[index].update()

def draw_objects(objs, disply):
    disply.fill((0,0,0)) # Fills background to black
    for index in range(len(objs)):
        objs[index].draw(disply)

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
                if event.key == setng_obj.shoot[i]: key_button += "ENTER"
    
    # Assign key_button a string of the pressed key
    for i in range(len(setng_obj.move_left)):
        if pygame.key.get_pressed()[setng_obj.move_left[i]]: key_button += "LEFT"
    for i in range(len(setng_obj.move_right)):
        if pygame.key.get_pressed()[setng_obj.move_right[i]]: key_button += "RIGHT"
    for i in range(len(setng_obj.move_up)):
        if pygame.key.get_pressed()[setng_obj.move_up[i]]: key_button += "UP"
    for i in range(len(setng_obj.move_down)):
        if pygame.key.get_pressed()[setng_obj.move_down[i]]: key_button += "DOWN"
    for i in range(len(setng_obj.shoot)):
        if pygame.key.get_pressed()[setng_obj.shoot[i]]: key_button += "SHOOT"
    return key_button

if __name__ == "__main__":
    main()