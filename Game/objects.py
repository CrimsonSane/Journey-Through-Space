# objects script
# The goal for this script is to hold all the game objects

import math, random, pygame

# Outside py scripts that handle other things
import GLOBAL
import generalized_functions as gen_func

# SETTINGS CLASS
class Setting():
    def __init__(self):
        self.VOL_MIN = 0
        self.VOL_MAX = 100
        
        self.fullscreen = False
        self.latest_fulscrn = self.fullscreen
        self.resolution = [1200, 900]
        self.sound_volume = 100
        self.music_volume = 100
        
        # Key binds!
        self.move_left = [pygame.K_a, pygame.K_LEFT]
        self.move_right = [pygame.K_d,pygame.K_RIGHT]
        self.move_up = [pygame.K_w,pygame.K_UP]
        self.move_down = [pygame.K_s,pygame.K_DOWN]
        self.shoot = [pygame.K_j,pygame.K_RETURN]
        self.pause = [pygame.K_p,pygame.K_ESCAPE]
    
    def inc_dec_volume(self, value, vol_type):
        if vol_type == "SOUND":
            # If future sound volume is over maximum volume
            if (value + self.sound_volume) >= self.VOL_MAX:
                self.sound_volume = self.VOL_MAX
            # If future sound volume is under minimum volume
            elif (value + self.sound_volume) <= self.VOL_MIN:
                self.sound_volume = self.VOL_MIN
            else:
                # Change volume as normal
                self.sound_volume += value
            
        elif vol_type == "MUSIC":
            # If future sound volume is over maximum volume
            if (value + self.music_volume) >= self.VOL_MAX:
                self.music_volume = self.VOL_MAX
            # If future sound volume is under minimum volume
            elif (value + self.music_volume) <= self.VOL_MIN:
                self.music_volume = self.VOL_MIN
            else:
                # Change volume as normal
                self.music_volume += value
            
        else:
            print("Unknown volume type: "+str(vol_type))
    
    def write_changes(self):
        with open("Settings.txt","w") as d:
            lines_to_write = ["fullscreen: "+str(self.fullscreen)+"\n",
                              "resolution: "+str(self.resolution)+"\n",
                              "sound_vol: "+str(self.sound_volume)+"\n",
                              "music_vol: "+str(self.music_volume)+"\n",
                              "left: "+str(self.move_left)+"\n",
                              "right: "+str(self.move_right)+"\n",
                              "up: "+str(self.move_up)+"\n",
                              "down: "+str(self.move_down)+"\n",
                              "shoot: "+str(self.shoot)+"\n"]
            d.writelines(lines_to_write)
            d.close()
    
    def setup_settings(self):
        exists = gen_func.get_txt("Settings")
        
        if exists:
            with open("Settings.txt","r") as d:
                lines = d.readlines()
                
                for line in lines:
                    # Fullscreen setting
                    if "fullscreen: " in line:
                        value = line[len("fullscreen: "):-1]
                        if value.upper() == "TRUE":
                            self.fullscreen = True
                        else:
                            self.fullscreen = False
                    # Resolution
                    if "resolution: " in line:
                        value = line[len("fullscreen: "):-1]
                        
                        self.resolution = eval(value)
                    # Sound volume control
                    if "sound_vol: " in line:
                        value = int(line[len("sound_vol: "):-1])
                        if value >= 100:
                            self.sound_volume = 100
                        elif value <= 0:
                            self.sound_volume = 0
                        else:
                            self.sound_volume = value
                    # Music volume control
                    if "music_vol: " in line:
                        value = int(line[len("music_vol: "):-1])
                        if value >= 100:
                            self.music_volume = 100
                        elif value <= 0:
                            self.music_volume = 0
                        else:
                            self.music_volume = value
                    # Left keybindings
                    if "left: " in line:
                        value = line[len("left: "):-1]
                        
                        self.move_left = eval(value)
                    # Right keybindings
                    if "right: " in line:
                        value = line[len("right: "):-1]
                        
                        self.move_right = eval(value)
                    # Up keybindings
                    if "up: " in line:
                        value = line[len("up: "):-1]
                        
                        self.move_up = eval(value)
                    # Down keybindings
                    if "down: " in line:
                        value = line[len("down: "):-1]
                        
                        self.move_down = eval(value)
                    # Shoot keybindings
                    if "shoot: " in line:
                        value = line[len("shoot: "):-1]
                        
                        self.shoot = eval(value)
                d.close()
        else:
            print("Settings.txt doesn't exist. We'll create one for you. :)")
            self.write_changes()

# MENU CLASS
class Menu():
    def __init__(self, menu_name, settings_object):
        super().__init__()
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        self.menu_name = menu_name
        
        self.but_index = 0
        self.latest_index = 0
        self.but_press_time = 0
        self.config = False
        self.config_type = ""
        self.config_index = 0
        
        self.menu_funcs = []
        self.scroll_type = "UP_DOWN"
        
        self.settings_object = settings_object
        
        # PLAYER DEATH menu
        self.plyer_death_mnu = [["PLAY AGAIN",
                                 "QUIT TO MENU"],
                                [(self.WIDTH/2,(self.HEIGHT/2)-35),
                                 (self.WIDTH/2,(self.HEIGHT/2)+35)],
                                [46,
                                 46,
                                 46],
                                ["RELOAD_GAME",
                                 "MAIN_SCENE"]]
        # PAUSE menu
        self.pause_mnu = [["CONTINUE",
                           "SETTINGS",
                           "RESTART",
                           "QUIT TO MENU"],
                          [(self.WIDTH/2,(self.HEIGHT/2)-100),
                           (self.WIDTH/2,(self.HEIGHT/2)-35),
                           (self.WIDTH/2,(self.HEIGHT/2)+35),
                           (self.WIDTH/2,(self.HEIGHT/2)+100)],
                          [46,
                           46,
                           46,
                           46,
                           46],
                          ["GAME_SCENE",
                           "GAME_SETTING_SCENE",
                           "RELOAD_GAME",
                           "MAIN_SCENE"]]
        # MAIN menu
        self.main_mnu = [["PLAY",
                          "SETTINGS",
                          "QUIT"],
                         [(self.WIDTH/2,(self.HEIGHT/2)-35),
                          (self.WIDTH/2,(self.HEIGHT/2)+35),
                          (self.WIDTH/2,(self.HEIGHT/2)+100)],
                         [46,
                          46,
                          46],
                         ["RELOAD_GAME",
                          "SETTING_SCENE",
                          "QUIT"]]
        # SETTING menu
        self.setting_mnu = [["SOUND: "+str(self.settings_object.sound_volume),
                             "MUSIC: "+str(self.settings_object.music_volume),
                             "FULLSCREEN: "+str(self.settings_object.fullscreen),
                             "RESOLUTION: "+str(self.settings_object.resolution),
                             "BACK"],
                            [(self.WIDTH/2,150),
                             (self.WIDTH/2,220),
                             (self.WIDTH/2,290),
                             (self.WIDTH/2,360),
                             (self.WIDTH/2, self.HEIGHT - 50)],
                            [46,
                             46,
                             46,
                             46,
                             46],
                            ["CONFIGURE_SOUND",
                             "CONFIGURE_MUSIC",
                             "CONFIGURE_FULLSCREEN",
                             "CONFIGURE_RESOLUTION",
                             "MAIN_SCENE"]]
        # ERROR menu
        self.error_mnu = [["ERROR INVALID MENU NAME"],
                         [(self.WIDTH/2,(self.HEIGHT/2))],
                         [69],
                         ["QUIT"]]
        
        self.error2_mnu = [["ERROR INVALID SCENE NAME"],
                           [(self.WIDTH/2,(self.HEIGHT/2))],
                           [69],
                           ["QUIT"]]
        
        if menu_name == "MAIN":
            self.menu_funcs = self.main_mnu
        elif menu_name == "SETTINGS":
            self.menu_funcs = self.setting_mnu
        elif menu_name == "PAUSE":
            self.menu_funcs = self.pause_mnu
        elif menu_name == "GAME_SETTINGS":
            self.menu_funcs = self.setting_mnu
            self.menu_funcs[3][len(self.menu_funcs[2]) - 1] = "PAUSE_SCENE"
        elif menu_name == "PLAYER_DEATH":
            self.menu_funcs = self.plyer_death_mnu
        elif menu_name == "ERROR":
            self.menu_funcs = self.error2_mnu
        else:
            print("!!! ERROR MENU NAME IS INVALID !!!")
            self.menu_funcs = self.error_mnu
        
        self.menu_timer = Timer()
        self.config_options = []
    
    def update(self, key_butns):
        if self.menu_name == "SETTINGS" or self.menu_name == "GAME_SETTINGS":
            self.menu_funcs[0][0] = "SOUND: "+str(self.settings_object.sound_volume)
            self.menu_funcs[0][1] = "MUSIC: "+str(self.settings_object.music_volume)
            self.menu_funcs[0][2] = "FULLSCREEN: "+str(self.settings_object.fullscreen)
            self.menu_funcs[0][3] = "RESOLUTION: "+str(self.settings_object.resolution)
        
        BUTTON_TIME_COOLDOWN = 150
        
        if self.scroll_type == "UP_DOWN":
            if self.config:
                
                BUTTON_TIME_COOLDOWN = 150
                currnt_tme, targt_tme = self.menu_timer.unpauseable_start(self.but_press_time, BUTTON_TIME_COOLDOWN)
                
                if self.config_type == "RESOLUTION":
                    self.config_options = GLOBAL.RESOLUTIONS[0]
                    self.settings_object.resolution = [GLOBAL.RESOLUTIONS[0][self.config_index],GLOBAL.RESOLUTIONS[1][self.config_index]]
                
                # Move left and right to configure sound volume
                if currnt_tme > targt_tme:
                    if "LEFT" in key_butns:
                        self.but_press_time = pygame.time.get_ticks()
                        GLOBAL.menu_selection.play()
                        self.configurate_option(-1)
                        
                        if self.config_index > 0:
                            self.config_index -= 1
                        else:
                            self.config_index = len(self.config_options) - 1
                        
                    if "RIGHT" in key_butns:
                        self.but_press_time = pygame.time.get_ticks()
                        GLOBAL.menu_selection.play()
                        self.configurate_option(1)
                        
                        if self.config_index < len(self.config_options) - 1:
                            self.config_index += 1
                        else:
                            self.config_index = 0
            else:
                currnt_tme, targt_tme = self.menu_timer.unpauseable_start(self.but_press_time, BUTTON_TIME_COOLDOWN)
                
                # Can hold the down key to cycle through options
                if currnt_tme > targt_tme:
                    if "DOWN" in key_butns:
                        self.but_press_time = pygame.time.get_ticks()
                        GLOBAL.menu_selection.play()
                        if self.but_index < len(self.menu_funcs[0]) - 1:
                            self.but_index += 1
                        else:
                            self.but_index = 0
                    if "UP" in key_butns:
                        self.but_press_time = pygame.time.get_ticks()
                        GLOBAL.menu_selection.play()
                        if self.but_index > 0:
                            self.but_index -= 1
                        else:
                            self.but_index = len(self.menu_funcs[0]) - 1
                    #print(self.but_index)
            
            # If the enter button was pressed
            if "ENTER" in key_butns:
                GLOBAL.menu_select.play()
                
                # If the button pressed has configure in the event string
                if "CONFIGURE_" in self.menu_funcs[3][self.but_index]:
                    # Sound configuration
                    if self.menu_funcs[3][self.but_index] == "CONFIGURE_SOUND":
                        self.config = not self.config
                        if not self.config:
                            self.settings_object.write_changes()
                            self.config_type = ""
                        else:
                            self.config_type = "SOUND"
                    # Music configuration
                    elif self.menu_funcs[3][self.but_index] == "CONFIGURE_MUSIC":
                        self.config = not self.config
                        if not self.config:
                            self.settings_object.write_changes()
                            self.config_type = ""
                        else:
                            self.config_type = "MUSIC"
                    # Fullscreen configuration
                    elif self.menu_funcs[3][self.but_index] == "CONFIGURE_FULLSCREEN":
                        self.config = not self.config
                        if not self.config:
                            self.settings_object.write_changes()
                            self.config_type = ""
                        else:
                            self.config_type = "FULLSCREEN"
                    # Resolution configuration
                    elif self.menu_funcs[3][self.but_index] == "CONFIGURE_RESOLUTION":
                        self.config = not self.config
                        if not self.config:
                            self.settings_object.write_changes()
                            self.config_type = ""
                        else:
                            self.config_type = "RESOLUTION"
                            
                            self.config_index = gen_func.get_index_frm_2d_list(GLOBAL.RESOLUTIONS, self.settings_object.resolution)
                else:
                    if self.menu_funcs[3][self.but_index] == "GAME_SCENE" or self.menu_funcs[3][self.but_index] == "MAIN_SCENE":
                        GLOBAL.paused = False
                    GLOBAL.scene_strng = self.menu_funcs[3][self.but_index]
                    self.but_index = 0
    
    def configurate_option(self, movement):
        if self.config_type == "SOUND" or self.config_type == "MUSIC":
            if movement < 0:
                self.settings_object.inc_dec_volume(-10, self.config_type)
            elif movement > 0:
                self.settings_object.inc_dec_volume(10, self.config_type)
            
        elif self.config_type == "FULLSCREEN":
            self.settings_object.fullscreen = not self.settings_object.fullscreen
    
    def draw(self, disply):
        for butn_index in range(len(self.menu_funcs[0])):
            # Display selected button
            if butn_index == self.but_index:
                # Simulate a blink when selected
                if butn_index == self.latest_index:
                    # When config is true make button look like:
                    #  <BUTTON>
                    if self.config:
                        font_size = self.menu_funcs[2][butn_index]
                        text = "<"+self.menu_funcs[0][butn_index]+">"
                        rendered_text = gen_func.get_font(font_size).render(text, 1, (255,255,255))
                        
                        disply.blit(rendered_text, rendered_text.get_rect(center = self.menu_funcs[1][butn_index]))
                    else:
                    # When config is false make button look like:
                    #  >BUTTON<
                        font_size = self.menu_funcs[2][butn_index]
                        text = ">"+self.menu_funcs[0][butn_index]+"<"
                        rendered_text = gen_func.get_font(font_size).render(text, 1, (255,255,255))
                        
                        disply.blit(rendered_text, rendered_text.get_rect(center = self.menu_funcs[1][butn_index]))
                else:
                    # Set latest index
                    self.latest_index = self.but_index
            else:
                # The button has not been selected
                font_size = self.menu_funcs[2][butn_index]
                text = self.menu_funcs[0][butn_index]
                rendered_text = gen_func.get_font(font_size).render(text, 1, (255,255,255))
                
                disply.blit(rendered_text, rendered_text.get_rect(center = self.menu_funcs[1][butn_index]))

# TIMER CLASS
class Timer():
    def __init__(self):
        self.paused_ticks = 0
        self.target_time = 0
    
    # Returns current time and the target time with the pausing
    def start(self, start_time, time):
        self.target_time = start_time + time + self.paused_ticks
        
        if GLOBAL.paused:
            self.paused_ticks = GLOBAL.current_tick - GLOBAL.pause_tick
        elif self.target_time <= GLOBAL.current_tick:
            self.paused_ticks = 0
        
        return GLOBAL.current_tick, self.target_time
    
    # Returns a start time that doesn't update during a loop
    def get_start_time(self, start_time):
        if start_time < 0:
            start_time = GLOBAL.current_tick
        return start_time

    # Returns current time and the target time without the pausing
    def unpauseable_start(self, start_time, time):
        current_time = GLOBAL.current_tick
        target_time = start_time + time
        
        return current_time, target_time

# PLAYER CLASS 
class Player_space_ship(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        GLOBAL.player_group.add(self)
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.MAX_HEALTH = 4
        self.health = 3
        self.latest_health = self.health
        self.display_player = True
        
        self.MV_SPD = 12
        self.AGLE_SPD = 5
        self.velocity = 0.0
        self.pos = pos
        self.angle = 0
        self.orignial_img = img
        self.image = self.orignial_img
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        
        self.shield_time = 5000
        self.shield_start_time = -1
        self.shield_bool = False
        self.display_shield = False
        self.bubble_img = gen_func.get_image("Assets","Bubble.png", (0,0))
        self.shield_rect = self.bubble_img.get_rect(center = (self.pos[0],self.pos[1]))
        self.shield_timer = Timer()
        
        self.thruster_imgs = [gen_func.get_image("Assets","thrusterFire-frame0.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame1.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame2.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame3.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame4.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame5.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame6.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame7.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame8.png", (0,0)),
                              gen_func.get_image("Assets","thrusterFire-frame9.png", (0,0))]
        self.fire_image = self.thruster_imgs[0]
        self.fire_rect = self.fire_image.get_rect(midtop = (self.pos[0],self.pos[1]+50))
        self.fire_index = 0
        
        self.lazer_type = "PLAYER_NORM_LAZER"
        self.LAZER_COOLDOWNS = [8, 4, 20, 9, 10, 5]
        self.lazer_cooldown = self.LAZER_COOLDOWNS[0]
        self.shoot_start_time = -1
        self.lazer_timer = Timer()
    
    def update(self, key_butns):
        # Move the ship as long as it has velocity
        if not GLOBAL.paused:
            self.pos[0] += ((GLOBAL.scroll_spd + self.MV_SPD) * self.velocity)
            self.image = pygame.transform.rotate(self.orignial_img, self.angle)
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
            self.shield_rect = self.bubble_img.get_rect(center = (self.pos[0],self.pos[1]))
        
            # Loop through the thruster images
            if self.fire_index < len(self.thruster_imgs) - 1:
                self.fire_index += 1
            else:
                self.fire_index = 0
            self.fire_image = pygame.transform.rotate(self.thruster_imgs[self.fire_index], self.angle)
            self.fire_rect = self.fire_image.get_rect(midtop = (15*math.sin(math.radians(self.angle)) + self.pos[0], self.pos[1] + 5 + math.cos(math.radians(self.angle))))
            
            # if player isn't dead
            if self.health > 0:
                # Shoot weapon
                if "SHOOT" in key_butns:
                    self.shoot()
                
                # Change velocity and angle based off of key_buttons
                if "LEFT" in key_butns:
                    if self.velocity > -1 and self.pos[0] > 0:
                        self.velocity = round(self.velocity,1) - 0.1
                    
                    elif self.pos[0] <= 0:
                        self.velocity = 0
                        
                    if self.angle < 45:
                        self.angle += self.AGLE_SPD
                    
                if "RIGHT" in key_butns:
                    if self.velocity < 1 and self.pos[0] < self.WIDTH:
                        self.velocity = round(self.velocity,1) + 0.1
                    
                    elif self.pos[0] >= self.WIDTH:
                        self.velocity = 0
                    
                    if self.angle > -45:
                        self.angle -= self.AGLE_SPD
        
        # When a change in health happens
        if self.latest_health != self.health and self.health > 0:
            self.shield_bool = True
            self.latest_health = self.health
        # Activate shield
        elif self.shield_bool:
            self.shield(self.shield_time)
        # Health reaches zero
        elif self.health <= 0 and self.display_player == True:
            Explosion([0,0], GLOBAL.explosion_group, [3,3, 5,5], self.pos)
            self.display_player = False
        # Reset player position after death
        if self.health == 0:
            self.pos = [int(GLOBAL.WIN_WIDTH/2),GLOBAL.WIN_HEIGHT -100]
        
        self.lazer_cooldown_setup()
        
        # If not moving change velocity back to ZERO
        if not "LEFT" in key_butns and not "RIGHT" in key_butns:
            if self.velocity > 0:
                self.velocity = round(self.velocity,1) - 0.1
                
            elif self.velocity < 0:
                self.velocity = round(self.velocity,1) + 0.1
            
            if self.angle > 0:
                self.angle -= self.AGLE_SPD
            
            elif self.angle < 0:
                self.angle += self.AGLE_SPD
        
        # Astroid collision
        astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
        if astroid_collision_value != -1:
            # Trys to split both objects and damages the player
            GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
            # If the latest health is equal to current health
            if self.latest_health == self.health:
                
                # If the player is not protected
                if not self.shield_bool:
                    self.health -= 1
                    gen_func.play_sound(GLOBAL.player_hit, GLOBAL.PLAYER_CHANNEL)
                else:
                    # It plays a lazer sound if the astroid hits while the player has a shield
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_CHANNEL)
    
    def lazer_cooldown_setup(self):
        # Lazer cooldown setup
        COOLDOWN_TIME = 10
        
        if self.lazer_cooldown > 0:
            self.shoot_start_time = gen_func.get_start_time(self.shoot_start_time)
            
            current_time, target_time = self.lazer_timer.start(self.shoot_start_time, COOLDOWN_TIME)
            
            if current_time >= target_time:
                self.lazer_cooldown -= 1
                self.shoot_start_time = -1
    
    def shield(self, on_time):
        self.shield_start_time = gen_func.get_start_time(self.shield_start_time)
        current_time, target_time = self.shield_timer.start(self.shield_start_time, on_time)
        BLINK_TIME = target_time - 1000
        
        # The shield is done 
        if current_time >= target_time:
            self.shield_bool = False
            self.display_shield = False
            self.shield_start_time = -1
        
        # The shield is being displayed
        elif current_time < BLINK_TIME:
            self.display_shield = True
            
        # The shield is about to go out
        elif current_time >= BLINK_TIME and current_time < target_time:
            for i in range(10):
                if current_time >= BLINK_TIME + 100*i:
                    self.display_shield = not self.display_shield
    
    def shoot(self):
        # Normal player lazer
        if self.lazer_type == "PLAYER_NORM_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[0]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # Rapid fire player lazer
        elif self.lazer_type == "PLAYER_RAPID_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[1]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # player lazer cannon
        elif self.lazer_type == "PLAYER_CANNON_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[2]
                gen_func.play_sound(GLOBAL.lazer_cannon_shooting, GLOBAL.LAZER_CHANNEL)
        # Split fire player lazer
        elif self.lazer_type == "PLAYER_SPLIT_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[3]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # Pierce fire player lazer
        elif self.lazer_type == "PLAYER_PIERCE_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-11, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-11, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[4]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # Spread fire player lazer
        elif self.lazer_type == "PLAYER_SPREAD_LAZER":
            
            if self.lazer_cooldown <= 0:
                OFFSET_ANGLE0 = 30
                OFFSET_ANGLE1 = 15
                
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[5]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        # The try method is to help prevent crashes
        try:
            # Makes sure not to return itself
            if self.rect != group.sprites()[collide_lst_index].rect:
                return collide_lst_index
            else:
                return -1
        except:
            print("There are no objects to collide with")
    
    def draw(self, disply):
        if self.display_player:
            disply.blit(self.fire_image, self.fire_rect)
            disply.blit(self.image, self.rect)
        if self.display_shield:
            disply.blit(self.bubble_img, self.shield_rect)

# LAZER CLASS
class Lazer(pygame.sprite.Sprite):
    def __init__(self, pos, group, lazer_type="PLAYER_NORM_LAZER", spd=-1, angle=0):
        super().__init__()
        group.add(self)
        
        self.lazer_type = lazer_type
        
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = spd
        self.angle = angle
        self.pos = pos
        
        self.images = [gen_func.get_image("Assets", "Lazer.png", (0,0)),
                       gen_func.get_image("Assets", "Cannon.png", (0,0)),
                       gen_func.get_image("Assets", "SplitLazer.png", (0,0)),
                       gen_func.get_image("Assets", "PierceLazer.png", (0,0))]
        
        if self.lazer_type == "PLAYER_CANNON_LAZER":
            self.image = self.images[1]
        elif self.lazer_type == "PLAYER_SPLIT_LAZER":
            self.image = self.images[2]
        elif self.lazer_type == "PLAYER_PIERCE_LAZER":
            self.image = self.images[3]
            self.hits = 0
        else:
            self.image = self.images[0]
        self.orignial_img = self.image # Save image for later
        self.rect = self.image.get_rect(midbottom = (self.pos[0] + (self.angle/5),self.pos[1] + (-abs(self.angle/10))))
        
        self.explosion = 0
    
    def update(self):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0] + self.spd * (self.angle/30), self.pos[1] + self.spd]
            self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        # Collision
        astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
        if astroid_collision_value != -1:
            # Trys to split objects if in screen
            
            if self.lazer_type == "PLAYER_CANNON_LAZER":
                EXPLOSION_SIZE = 3
                CURRENT_SPD = [self.spd * (self.angle/30), self.spd]
                
                # If is not on screen
                if self.pos[1] < 0:
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                    if self.explosion == 0:
                        self.explosion = 1
                        gen_func.play_sound(GLOBAL.lazer_cannon_hit, GLOBAL.EXPLOSION_CHANNEL)
                        Explosion(CURRENT_SPD, GLOBAL.explosion_group, [2,2, EXPLOSION_SIZE,EXPLOSION_SIZE], self.pos, True)
                    self.kill()
                else:
                    # Add and display points
                    GLOBAL.score += GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]
                    Moving_text(str(GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]),
                                self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                    
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                    if self.explosion == 0:
                        self.explosion = 1
                        gen_func.play_sound(GLOBAL.lazer_cannon_hit, GLOBAL.EXPLOSION_CHANNEL)
                        Explosion(CURRENT_SPD, GLOBAL.explosion_group, [2,2, EXPLOSION_SIZE,EXPLOSION_SIZE], self.pos, True)
                    self.kill()
            elif self.lazer_type == "PLAYER_SPLIT_LAZER":
                # If is not on screen
                if self.pos[1] < 0:
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                    self.kill()
                else:
                    # Add and display points
                    GLOBAL.score += GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]
                    Moving_text(str(GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]),
                                self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                    
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-9, angle=-30,
                          group=GLOBAL.lazer_group)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-9, angle=30,
                          group=GLOBAL.lazer_group)
                    
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                    
                    self.kill()
            elif self.lazer_type == "PLAYER_PIERCE_LAZER":
                PIERCE_MAX = 2
                # If is not on screen
                if self.pos[1] < 0:
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                    self.kill()
                elif self.hits >= PIERCE_MAX:
                    self.kill()
                else:
                    # Add and display points
                    GLOBAL.score += GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]
                    Moving_text(str(GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]),
                                self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                    
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                    self.hits += 1
            else:
                # If is not on screen
                if self.pos[1] < 0:
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                    self.kill()
                else:
                    # Add and display points
                    GLOBAL.score += GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]
                    Moving_text(str(GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]),
                                self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                    
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                    self.kill()
        
        # If object moves out of screen
        if self.pos[1] < -10 or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.kill()
        else:
            self.rect = self.image.get_rect(midbottom = (self.pos[0],self.pos[1]))
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        # The try method is to help prevent crashes
        try:
            # Makes sure not to return itself
            if self.rect != group.sprites()[collide_lst_index].rect:
                return collide_lst_index
            else:
                return -1
        except:
            print("There are no objects to collide with")
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)

# MOVING TEXT CLASS
class Moving_text(pygame.sprite.Sprite):
    def __init__(self, text, pos, spd, group):
        super().__init__()
        group.add(self)
        
        self.text = text
        self.spd = spd
        self.pos = pos
        
        self.image = gen_func.get_font(36).render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
    
    def update(self):
        if not GLOBAL.paused:
            # Move the text
            self.pos[0] += self.spd[0]
            self.pos[1] += self.spd[1]
        
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        
        if self.pos[1] < -10 or self.pos[1] > GLOBAL.WIN_HEIGHT:
            self.kill()
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)

# STAR CLASS
class Star(pygame.sprite.Sprite):
    def __init__(self, imgs, spd, group, spd_rng):
        super().__init__()
        group.add(self)
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = [GLOBAL.scroll_spd * spd[0],GLOBAL.scroll_spd * spd[1]]
        self.spd_rng = spd_rng
        self.angle = random.randint(-360, 360)
        self.pos = [random.randint(0,self.WIDTH),random.randint(0,self.HEIGHT)] # Randomize position
        self.images = imgs
        self.image = random.choice(self.images)
        self.orignial_img = self.image # Save image for later
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def update(self):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def regen(self):
        self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
        self.image = random.choice(self.images)
        self.orignial_img = self.image
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        self.spd[0] = GLOBAL.scroll_spd * random.randint(self.spd_rng[0],self.spd_rng[1])
        self.spd[1] = GLOBAL.scroll_spd * random.randint(self.spd_rng[2],self.spd_rng[3])
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > 0:
            disply.blit(self.image, self.rect)

# PLANET CLASS
class Planet(pygame.sprite.Sprite):
    def __init__(self, spd, group, spd_rng):
        super().__init__()
        group.add(self)
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = [spd[0],spd[1]]
        self.spd_rng = spd_rng
        self.angle = random.randint(-360, 360)
        self.size = random.randint(25, 100)
        self.pos = [random.randint(0,self.WIDTH),random.randint(0,self.HEIGHT)] # Randomize position
        
        self.angle_spd = random.randint(-1,1)
        self.angle_spd /= random.randint(5,25)
        
        self.images = [gen_func.get_image("Assets", "Planet1.png",(0,0)),
                       gen_func.get_image("Assets", "Planet2.png",(0,0)),
                       gen_func.get_image("Assets", "Planet3.png",(0,0)),
                       gen_func.get_image("Assets", "Planet4.png",(0,0)),
                       gen_func.get_image("Assets", "Planet5.png",(0,0))]
        self.image = pygame.transform.scale(random.choice(self.images),(self.size, self.size))
        self.orignial_img = self.image # Save image for later
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def update(self):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
            self.angle += self.angle_spd
        
        # rotate
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT + 25 or self.pos[0] > self.WIDTH + 25 or self.pos[0] < 0 - 25:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def regen(self):
        self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
        
        self.angle = random.randint(-360, 360)
        self.size = random.randint(25, 100)
        
        self.angle_spd = random.randint(-1,1)
        self.angle_spd /= random.randint(5,25)
        
        self.image = pygame.transform.scale(random.choice(self.images),(self.size, self.size))
        self.orignial_img = self.image
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        self.spd[0] = random.randint(self.spd_rng[0],self.spd_rng[1])
        self.spd[1] = random.randint(self.spd_rng[2],self.spd_rng[3])
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > 0:
            disply.blit(self.image, self.rect)

# ASTROID CLASS
class Astroid(pygame.sprite.Sprite):
    def __init__(self, pos, imgs, spd_rng, group, spd=[0,random.randint(1,5)], pts=random.randint(1,6), is_astroid=True):
        super().__init__()
        group.add(self)
        
        self.is_astroid = is_astroid
        
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = [GLOBAL.scroll_spd * spd[0],GLOBAL.scroll_spd * spd[1]]
        self.spd_rng = spd_rng
        self.angleSpd = random.randint(-1,1)
        self.angle = random.randint(-360, 360)
        self.pos = pos
        
        self.pts = pts # Astroid points
        
        self.images = imgs # Contains lists inside
        
        self.image = random.choice(self.images[self.pts - 1])
        self.orignial_img = self.image # Save image for later
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        
        self.explosion = 0
    
    def update(self):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
            self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
            # Rotate
            self.angle += self.angleSpd
        
        # Collision
        astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
        if astroid_collision_value != -1:
            # Trys to split both objects if in screen
            if self.pos[1] < 0:
                self.regen()
                GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
            else:
                self.split()
                GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                gen_func.play_sound(GLOBAL.astroid_explosion, GLOBAL.EXPLOSION_CHANNEL)
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT + 100 or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        # The try method is to help prevent crashes
        try:
            # Makes sure not to return itself
            if self.rect != group.sprites()[collide_lst_index].rect:
                return collide_lst_index
            else:
                return -1
        except:
            print("There are no objects to collide with")
    
    def regen(self):
        if self.is_astroid:
            # Has to be an astroid to properly regen
            self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
            self.pts = random.randint(1,len(self.images))
            
            self.angleSpd = random.randint(-1,1)
            self.angle = random.randint(-360, 360)
            
            self.spd[0] = GLOBAL.scroll_spd * random.randint(self.spd_rng[0],self.spd_rng[1])
            self.spd[1] = GLOBAL.scroll_spd * random.randint(self.spd_rng[2],self.spd_rng[3])
            
            self.image = random.choice(self.images[self.pts - 1])
            self.orignial_img = self.image
            
            self.explosion = 0
        else:
            # Make an explosion if it is on the window
            if self.pos[1] > -10 and self.pos[1] < self.HEIGHT + 100:
                # Only display one explosion
                if self.explosion == 0:
                    self.explosion = 1
                    Explosion(self.spd, GLOBAL.explosion_group, [1,1, 1,1], self.pos)
            self.kill()
    
    def split(self):
        """
        4
        | <- -1
        V
        3
        | <- /2
        V
        1.5 -> round down to 1
        
        I call it The Twinstroid Algorithm since it always ends up with twins that split the same way.
        Meaning 2 point astroids are essentialy 1 point astroids and they don't split.
        """
        splitted_pts = int((self.pts - 1)/2) # The point was to round down but int can do the job.
        
        old_pos = self.pos
        if self.pos[1] > -10 and self.pos[1] < self.HEIGHT + 100:
            # Only display one explosion
            if self.explosion == 0:
                self.explosion = 1
                Explosion(self.spd, GLOBAL.explosion_group, [1,1, 1,1], self.pos)
        self.regen()
        
        if splitted_pts > 0:
            Astroid(pos=[old_pos[0]+(10*self.pts), old_pos[1]], imgs=self.images, spd=[1,3],
                    group=GLOBAL.astroids_group, pts=splitted_pts, is_astroid=False, spd_rng=[0,0, 0,0])
            Astroid(pos=[old_pos[0]+(-10*self.pts), old_pos[1]], imgs=self.images, spd=[-1,3],
                    group=GLOBAL.astroids_group, pts=splitted_pts, is_astroid=False, spd_rng=[0,0, 0,0])
        else:
            self.regen()
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > -10:
            disply.blit(self.image, self.rect)

# EXPLOSION CLASS
class Explosion(pygame.sprite.Sprite):
    def __init__(self, spd, group, size, pos, destroy_objs=False):
        super().__init__()
        group.add(self)
        
        self.destroy_objs = destroy_objs
        
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = spd
        self.angle = random.randint(-360, 360)
        self.size = size
        self.pos = pos
        self.images = [gen_func.get_image("Assets","Explosion-frame-0.png",(size[0]*0,size[1]*0)),
                        gen_func.get_image("Assets","Explosion-frame-1.png",(size[0]*32,size[1]*32)),
                        gen_func.get_image("Assets","Explosion-frame-2.png",(size[0]*32,size[1]*32)),
                        gen_func.get_image("Assets","Explosion-frame-2.png",(size[0]*32,size[1]*32)),
                        gen_func.get_image("Assets","Explosion-frame-3.png",(size[0]*44,size[1]*44)),
                        gen_func.get_image("Assets","Explosion-frame-3.png",(size[0]*44,size[1]*44)),
                        gen_func.get_image("Assets","Explosion-frame-4.png",(size[0]*54,size[1]*54)),
                        gen_func.get_image("Assets","Explosion-final-frame.png",(size[0]*64,size[1]*64)),
                        gen_func.get_image("Assets","Explosion-final-frame.png",(size[0]*0,size[1]*0)),
                        gen_func.get_image("Assets","Explosion-frame-6.png",(size[2]*66,size[3]*66)),
                        gen_func.get_image("Assets","Explosion-frame-7.png",(size[2]*76,size[3]*76)),
                        gen_func.get_image("Assets","Explosion-frame-8.png",(size[2]*86,size[3]*86)),
                        gen_func.get_image("Assets","Explosion-frame-9.png",(size[2]*96,size[3]*96)),
                        gen_func.get_image("Assets","Explosion-frame-10.png",(size[2]*106,size[3]*106)),
                        gen_func.get_image("Assets","Explosion-frame-11.png",(size[2]*116,size[3]*116)),
                        gen_func.get_image("Assets","Explosion-frame-12.png",(size[2]*126,size[3]*126)),
                        gen_func.get_image("Assets","Explosion-frame-12.png",(size[2]*136,size[3]*136))]
        self.image = self.images[0]
        self.orignial_imgs = self.images # Save images for later
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        
        self.start_time = pygame.time.get_ticks()
        self.image_index = 0
        
        self.timer = Timer()
    
    def update(self):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
        timeSinceEnter = pygame.time.get_ticks() - self.start_time
       
        time = (self.image_index + 1) * 50
        current_time, target_time = self.timer.start(self.start_time, time)

        if self.image_index < len(self.images) - 1:
            # Rotate
            self.image = pygame.transform.rotate(self.orignial_imgs[self.image_index], self.angle)
            
            if target_time <= current_time:
                # Move to the next image
                self.image_index += 1
        # Destroy the object the animation has finished
        elif self.image_index >= len(self.images) - 1:
            self.kill()
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.kill()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
            
        if self.destroy_objs:
            # Collision
            astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
            if astroid_collision_value != -1:
                # Trys to split objects if in screen
                
                if self.pos[1] < 0:
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                else:
                    # Add and display points
                    GLOBAL.score += GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]
                    Moving_text(str(GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]),
                                self.pos, [0,-self.spd[1]], GLOBAL.mving_txt_group)
                    
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        # The try method is to help prevent crashes
        try:
            # Makes sure not to return itself
            if self.rect != group.sprites()[collide_lst_index].rect:
                return collide_lst_index
            else:
                return -1
        except:
            print("There are no objects to collide with")
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)

# ITEM CLASS
class Item(pygame.sprite.Sprite):
    def __init__(self, item_name, pos, spd, group):
        super().__init__()
        group.add(self)
        
        self.item_name = item_name
        self.spd = spd
        self.pos = pos
        self.angle = 0
        self.angle_spd = 5
        self.desc = ""
        
        ITEM_SIZE = (32, 32)
        GUN_ITEM_SIZE = (64, 64)
        
        if self.item_name == "HAMMER":
            self.image = gen_func.get_image("Assets","Hammer.png",ITEM_SIZE)
            self.desc = "HEALTH"
            self.og_image = self.image
        
        elif self.item_name == "NORMAL_GUN":
            self.image = gen_func.get_image("Assets","BasicLazerGun.png",GUN_ITEM_SIZE)
            self.og_image = self.image
            self.desc = "NORMAL"
            self.lazer_type = "PLAYER_NORM_LAZER"
        
        elif self.item_name == "RAPID_GUN":
            self.image = gen_func.get_image("Assets","RapidFireLazerGun.png",GUN_ITEM_SIZE)
            self.og_image = self.image
            self.desc = "RAPID"
            self.lazer_type = "PLAYER_RAPID_LAZER"
        
        elif self.item_name == "CANNON_GUN":
            self.image = gen_func.get_image("Assets","CannonLazerGun.png",GUN_ITEM_SIZE)
            self.og_image = self.image
            self.desc = "CANNON"
            self.lazer_type = "PLAYER_CANNON_LAZER"
        
        elif self.item_name == "SPLIT_GUN":
            self.image = gen_func.get_image("Assets","SplitLazerGun.png",GUN_ITEM_SIZE)
            self.og_image = self.image
            self.desc = "SPLIT"
            self.lazer_type = "PLAYER_SPLIT_LAZER"
        
        elif self.item_name == "PIERCE_GUN":
            self.image = gen_func.get_image("Assets","PiercingLazerGun.png",GUN_ITEM_SIZE)
            self.og_image = self.image
            self.desc = "PIERCE"
            self.lazer_type = "PLAYER_PIERCE_LAZER"
        
        elif self.item_name == "SPREAD_GUN":
            self.image = gen_func.get_image("Assets","SpreadLazerGun.png",GUN_ITEM_SIZE)
            self.og_image = self.image
            self.desc = "SPREAD"
            self.lazer_type = "PLAYER_SPREAD_LAZER"
        
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        
        self.text = gen_func.get_font(20).render(self.desc,1,(255,255,255))
        self.text_rect = self.text.get_rect(center = (self.pos[0], self.pos[1]+32))
        
    
    def update(self):
        # Move the text
        if not GLOBAL.paused:
            self.pos[0] += self.spd[0]
            self.pos[1] += self.spd[1]
            self.angle += self.angle_spd
        
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        
        self.text_rect = self.text.get_rect(center = (self.pos[0], self.pos[1]+32))
        
        # If it is outside of the screen
        if self.pos[1] < -GLOBAL.WIN_HEIGHT or self.pos[1] > GLOBAL.WIN_HEIGHT:
            self.kill()
        
        # Player collision
        player_collide_lst_index = self.rect.collidelist(GLOBAL.player_group.sprites())
        if player_collide_lst_index != -1:
            BONUS_SCORE = 1000
            plyer = GLOBAL.player_group.sprites()[player_collide_lst_index]
            
            # Hammer increases health to one and gives bonus points if max health is reached
            if self.item_name == "HAMMER":
                gen_func.play_sound(GLOBAL.item_collect, GLOBAL.PLAYER_CHANNEL)
                if plyer.health < plyer.MAX_HEALTH:
                    plyer.health += 1
                    self.kill()
                else:
                    GLOBAL.score += BONUS_SCORE
                    Moving_text(str(BONUS_SCORE), self.pos, [self.spd[0],-self.spd[1]], GLOBAL.mving_txt_group)
                    
                    self.kill()
            # Gun changes the player's lazer type to the collected item and give bonus points if you collect the same gun
            if "GUN" in self.item_name:
                gen_func.play_sound(GLOBAL.item_collect, GLOBAL.PLAYER_CHANNEL)
                if plyer.lazer_type != self.lazer_type:
                    plyer.lazer_type = self.lazer_type
                    self.kill()
                else:
                    GLOBAL.score += BONUS_SCORE
                    Moving_text(str(BONUS_SCORE), self.pos, [self.spd[0],-self.spd[1]], GLOBAL.mving_txt_group)
                    
                    self.kill()
        
        # Astroid collision
        astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
        try:
            if astroid_collision_value != -1:
                # Trys to split objects if in screen
                if self.pos[1] < 0:
                    self.kill()
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                else:
                    self.kill()
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
        except:
            print("Cannot collide with any more astroids")
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        # The try method is to help prevent crashes
        try:
            # Makes sure not to return itself
            if self.rect != group.sprites()[collide_lst_index].rect:
                return collide_lst_index
            else:
                return -1
        except:
            print("There are no objects to collide with")
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)
        if self.desc != "":
            disply.blit(self.text, self.text_rect)
