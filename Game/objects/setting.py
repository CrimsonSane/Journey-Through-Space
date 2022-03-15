import generalized_functions as gen_func

import pygame

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
        
        self.enable_tooltip = True
    
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