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
        self.resolution = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.sound_volume = 100
        self.music_volume = 100
        
        # Key binds!
        self.move_left = [pygame.K_a, pygame.K_LEFT]
        self.move_right = [pygame.K_d,pygame.K_RIGHT]
        self.move_up = [pygame.K_w,pygame.K_UP]
        self.move_down = [pygame.K_s,pygame.K_DOWN]
        self.shoot = [pygame.K_j,pygame.K_RETURN]
    
    def inc_dec_volume(self, value, vol_type):
        if vol_type == "SOUND":
            if (value + self.sound_volume) >= self.VOL_MAX:
                self.sound_volume = self.VOL_MAX
            elif (value + self.sound_volume) <= self.VOL_MIN:
                self.sound_volume = self.VOL_MIN
            else:
                self.sound_volume += value
            
        elif vol_type == "MUSIC":
            if (value + self.music_volume) >= self.VOL_MAX:
                self.music_volume = self.VOL_MAX
            elif (value + self.music_volume) <= self.VOL_MIN:
                self.music_volume = self.VOL_MIN
            else:
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
            print("Settings.txt doesn't exist. Game will run on default values.")

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
                             "BACK"],
                            [(self.WIDTH/2,50),
                             (self.WIDTH/2,120),
                             (self.WIDTH/2, self.HEIGHT - 50)],
                            [46,
                             46,
                             46],
                            ["CONFIGURE_SOUND",
                             "CONFIGURE_MUSIC",
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
        elif menu_name == "PLAYER_DEATH":
            self.menu_funcs = self.plyer_death_mnu
        elif menu_name == "ERROR":
            self.menu_funcs = self.error2_mnu
        else:
            print("!!! ERROR MENU NAME IS INVALID !!!")
            self.menu_funcs = self.error_mnu
    
    def update(self, key_butns):
        self.setting_mnu[0][0] = "SOUND: "+str(self.settings_object.sound_volume)
        self.setting_mnu[0][1] = "MUSIC: "+str(self.settings_object.music_volume)
        
        BUTTON_TIME_COOLDOWN = 150
        
        if self.scroll_type == "UP_DOWN":
            if self.config:
                if self.config_type == "SOUND" or self.config_type == "MUSIC":
                    self.configure_vol(key_butns, self.config_type)
            else:
                currnt_tme, targt_tme = gen_func.timer(self.but_press_time, BUTTON_TIME_COOLDOWN)
                
                # Can hold the down key to cycle through options
                if currnt_tme > targt_tme:
                    if "DOWN" in key_butns:
                        self.but_press_time = pygame.time.get_ticks()
                        if self.but_index < len(self.menu_funcs[0]) - 1:
                            self.but_index += 1
                        else:
                            self.but_index = 0
                    if "UP" in key_butns:
                        self.but_press_time = pygame.time.get_ticks()
                        if self.but_index > 0:
                            self.but_index -= 1
                        else:
                            self.but_index = len(self.menu_funcs[0]) - 1
                    #print(self.but_index)
            
            if "ENTER" in key_butns:
                if "CONFIGURE_" in self.menu_funcs[3][self.but_index]:
                    # Sound configuration
                    if self.menu_funcs[3][self.but_index] == "CONFIGURE_SOUND":
                        self.config = not self.config
                        if not self.config:
                            self.settings_object.write_changes()
                            self.config_type = ""
                        else:
                            self.config_type = "SOUND"
                    elif self.menu_funcs[3][self.but_index] == "CONFIGURE_MUSIC":
                        self.config = not self.config
                        if not self.config:
                            self.settings_object.write_changes()
                            self.config_type = ""
                        else:
                            self.config_type = "MUSIC"
                else:
                    GLOBAL.scene_strng = self.menu_funcs[3][self.but_index]
    
    def configure_vol(self, key_butns, vol_type):
        BUTTON_TIME_COOLDOWN = 150
        currnt_tme, targt_tme = gen_func.timer(self.but_press_time, BUTTON_TIME_COOLDOWN)
        
        # Move left and right to configure sound volume
        if currnt_tme > targt_tme:
            if "LEFT" in key_butns:
                self.but_press_time = pygame.time.get_ticks()
                self.settings_object.inc_dec_volume(-10, vol_type)
                
            if "RIGHT" in key_butns:
                self.but_press_time = pygame.time.get_ticks()
                self.settings_object.inc_dec_volume(10, vol_type)
            #print(self.settings_object.sound_volume)
    
    def draw(self, disply):
        for butn_index in range(len(self.menu_funcs[0])):
            # Display selected button
            if butn_index == self.but_index:
                # Simulate a blink when selected
                if butn_index == self.latest_index:
                    if self.config:
                        font_size = self.menu_funcs[2][butn_index]
                        text = "<"+self.menu_funcs[0][butn_index]+">"
                        rendered_text = gen_func.get_font(font_size).render(text, 1, (255,255,255))
                        
                        disply.blit(rendered_text, rendered_text.get_rect(center = self.menu_funcs[1][butn_index]))
                    else:
                        font_size = self.menu_funcs[2][butn_index]
                        text = ">"+self.menu_funcs[0][butn_index]+"<"
                        rendered_text = gen_func.get_font(font_size).render(text, 1, (255,255,255))
                        
                        disply.blit(rendered_text, rendered_text.get_rect(center = self.menu_funcs[1][butn_index]))
                else:
                    self.latest_index = self.but_index
            else:
                font_size = self.menu_funcs[2][butn_index]
                text = self.menu_funcs[0][butn_index]
                rendered_text = gen_func.get_font(font_size).render(text, 1, (255,255,255))
                
                disply.blit(rendered_text, rendered_text.get_rect(center = self.menu_funcs[1][butn_index]))

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
        self.shield_start_time = 0
        self.shield_bool = False
        self.display_shield = False
        self.bubble_img = gen_func.get_image("Assets","Bubble.png", (0,0))
        self.shield_rect = self.bubble_img.get_rect(center = (self.pos[0],self.pos[1]))
        
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
        self.LAZER_COOLDOWNS = [13]
        self.lazer_cooldown = self.LAZER_COOLDOWNS[0]
        self.shoot_start_time = 0
    
    def update(self, key_butns):
        # Move the ship as long as it has velocity
        self.pos[0] += ((GLOBAL.scroll_spd + self.MV_SPD) * self.velocity)
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        self.shield_rect = self.bubble_img.get_rect(center = (self.pos[0],self.pos[1]))
        
        
        if self.fire_index < len(self.thruster_imgs) - 1:
            self.fire_index += 1
        else:
            self.fire_index = 0
        self.fire_image = pygame.transform.rotate(self.thruster_imgs[self.fire_index], self.angle)
        self.fire_rect = self.fire_image.get_rect(midtop = (15*math.sin(math.radians(self.angle)) + self.pos[0],
                                                            self.pos[1] + 5 + math.cos(math.radians(self.angle))))
        
        # When a change in health happens
        if self.latest_health != self.health and self.health > 0:
            self.shield_start_time = pygame.time.get_ticks()
            self.shield_bool = True
            self.latest_health = self.health
        # Activate shield
        elif self.shield_bool:
            self.shield(self.shield_start_time, self.shield_time)
        # Health reaches zero
        elif self.health <= 0 and self.display_player == True:
            Explosion([0,0], GLOBAL.explosion_group, [3,3, 5,5], self.pos)
            self.display_player = False
        if self.health == 0:
            self.pos = [int(GLOBAL.WIN_WIDTH/2),GLOBAL.WIN_HEIGHT -100]
        
        # Lazer cooldown setup
        if self.lazer_cooldown != 0:
            time = pygame.time.get_ticks()
            if time >= 1000:
                time = 0
                self.lazer_cooldown -= 1
        
        # if player isn't dead
        if self.health > 0:
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
        if astroid_collision_value != -1 and self.health > 0:
            # Trys to split both objects and damages the player
            GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
            if self.latest_health == self.health and not self.shield_bool:
                self.health -= 1
                #print(self.health)
    
    def shield(self, start_time, on_time):
        current_time, target_time = gen_func.timer(start_time, on_time)
        BLINK_TIME = target_time - 1000
        
        if current_time >= target_time:
            self.shield_bool = False
            self.display_shield = False
        elif current_time < BLINK_TIME:
            self.display_shield = True
        elif current_time >= BLINK_TIME and current_time < target_time:
            for i in range(10):
                if current_time >= BLINK_TIME + 100*i:
                    self.display_shield = not self.display_shield
    
    def shoot(self):
        if self.lazer_type == "PLAYER_NORM_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[0]
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        if collide_lst_index > 0:
            # Makes sure not to return itself
            if self.rect != group.sprites()[collide_lst_index].rect:
                return collide_lst_index
            else:
                return -1
        return -1
    
    def draw(self, disply):
        if self.display_player:
            disply.blit(self.fire_image, self.fire_rect)
            disply.blit(self.image, self.rect)
        if self.display_shield:
            disply.blit(self.bubble_img, self.shield_rect)

# LAZER CLASS
class Lazer(pygame.sprite.Sprite):
    def __init__(self, pos, group, lazer_type, spd=-1, angle=0):
        super().__init__()
        group.add(self)
        
        self.lazer_type = lazer_type
        
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = spd
        self.angle = angle
        self.pos = pos
        
        self.images = [gen_func.get_image("Assets", "Lazer.png", (0,0))]
        
        self.image = self.images[0]
        self.orignial_img = self.image # Save image for later
        self.rect = self.image.get_rect(midbottom = (self.pos[0] + (self.angle/5),self.pos[1] + (-abs(self.angle/10))))
    
    def update(self):
        # Move with given speed
        self.pos = [self.pos[0] + self.spd * (self.angle/30), self.pos[1] + self.spd]
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        # Collision
        astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
        if astroid_collision_value != -1:
            # Trys to split objects if in screen
            if self.pos[1] < 0:
                GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                self.kill()
            else:
                GLOBAL.score += GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]
                Moving_text(str(GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]),
                            self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                self.kill()
        
        # If object moves out of screen
        if self.pos[1] < -10 or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.kill()
        else:
            self.rect = self.image.get_rect(midbottom = (self.pos[0],self.pos[1]))
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        # Makes sure not to return itself
        if self.rect != group.sprites()[collide_lst_index].rect:
            return collide_lst_index
        else:
            return -1
    
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
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def update(self):
        # Move with given speed
        self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
        # Rotate
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        self.angle += 2
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def regen(self):
        self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
        self.image = random.choice(self.images)
        self.orignial_img = self.image
        
        self.spd[0] = GLOBAL.scroll_spd * random.randint(self.spd_rng[0],self.spd_rng[1])
        self.spd[1] = GLOBAL.scroll_spd * random.randint(self.spd_rng[2],self.spd_rng[3])
    
    def draw(self, disply):
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
    
    def update(self):
        # Move with given speed
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
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT + 100 or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def check_collision(self, group):
        collide_lst_index = self.rect.collidelist(group.sprites())
        
        # Makes sure not to return itself
        if self.rect != group.sprites()[collide_lst_index].rect:
            return collide_lst_index
        else:
            return -1
    
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
        else:
            if self.pos[1] > -10 and self.pos[1] < self.HEIGHT + 100:
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
                Explosion(self.spd, GLOBAL.explosion_group, [1,1, 1,1], old_pos)
        self.regen()
        
        if splitted_pts > 0:
            Astroid(pos=[old_pos[0]+(10*self.pts), old_pos[1]], imgs=self.images, spd=[1,3],
                    group=GLOBAL.astroids_group, pts=splitted_pts, is_astroid=False, spd_rng=[0,0, 0,0])
            Astroid(pos=[old_pos[0]+(-10*self.pts), old_pos[1]], imgs=self.images, spd=[-1,3],
                    group=GLOBAL.astroids_group, pts=splitted_pts, is_astroid=False, spd_rng=[0,0, 0,0])
        else:
            self.regen()
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)

# EXPLOSION CLASS
class Explosion(pygame.sprite.Sprite):
    def __init__(self, spd, group, size, pos):
        super().__init__()
        group.add(self)
        
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
        self.orignial_imgs = self.images # Save image for later
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        
        self.start_time = pygame.time.get_ticks()
        self.image_index = 0
    
    def update(self):
        # Move with given speed
        self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
        # Rotate
        self.image = pygame.transform.rotate(self.orignial_imgs[self.image_index], self.angle)
        
        timeSinceEnter = pygame.time.get_ticks() - self.start_time
        #print(timeSinceEnter)
        if (self.image_index + 1) * 5 <= timeSinceEnter and self.image_index < len(self.images):
            self.image_index += 1
            self.start_time = pygame.time.get_ticks()
        elif self.image_index == len(self.images) - 1:
            self.kill()
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.kill()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
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
        
        if self.item_name == "HAMMER":
            self.image = gen_func.get_image("Assets","Hammer.png",(32,32))
            self.og_image = self.image
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
    
    def update(self):
        # Move the text
        self.pos[0] += self.spd[0]
        self.pos[1] += self.spd[1]
        self.angle += self.angle_spd
        
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        
        if self.pos[1] < -GLOBAL.WIN_HEIGHT or self.pos[1] > GLOBAL.WIN_HEIGHT:
            self.kill()
        
        # Player collision
        player_collide_lst_index = self.rect.collidelist(GLOBAL.player_group.sprites())
        if player_collide_lst_index != -1:
            BONUS_SCORE = 1000
            plyer = GLOBAL.player_group.sprites()[player_collide_lst_index]
            
            if self.item_name == "HAMMER":
                if plyer.health < plyer.MAX_HEALTH:
                    plyer.health += 1
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
        
        # Makes sure not to return itself
        try:
            if self.rect != group.sprites()[collide_lst_index].rect:
                return collide_lst_index
            else:
                return -1
        except:
            print("There are no more objects to collide with")
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)