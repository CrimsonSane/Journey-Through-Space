import GLOBAL
from objects.timer import Timer
import generalized_functions as gen_func

import pygame

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
                            [(self.WIDTH/2,250),
                             (self.WIDTH/2,320),
                             (self.WIDTH/2,390),
                             (self.WIDTH/2,460),
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