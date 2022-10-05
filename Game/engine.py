import os, json, pygame, random

class Game_engine():
    def __init__(self, game_res, scenes={}, current_scene="", fps=30, background_color=(0,0,0)):
        pygame.init()
        print("* Pygame has been initialized in engine")
        
        # Scenes
        self.scenes        = scenes
        self.current_scene = current_scene
        
        # Global
        self.globl_evnts   = {}
        self.globl_vars    = {}
        
        # Display
        self.display_info  = pygame.display.Info()
        self.fps           = fps
        self.fill_color    = background_color
        self.machine_res   = [self.display_info.current_w, self.display_info.current_h]
        
        if len(game_res) == 2:
            self.game_res  = game_res
        else:
            print(game_res)
            raise Exception("X! Resolution value must contain 2 values")
        self.win_res      = self.game_res
        
        self.game_surf    = pygame.Surface((self.game_res[0], self.game_res[1]))
        self.win_surf     = pygame.display.set_mode((self.win_res[0], self.win_res[1]), pygame.RESIZABLE)
        
        # Additional modules
        self.time_mod     = Time_mod(self)
        self.audio_mod    = Audio_mod(self)
        self.event_mod    = Event_mod(self)
        self.opt_mgr      = Options_mgr(self)
        
        self.opt_mgr.get_opt_file()
        self.opt_mgr.load_file_to_opts()
        print("* Engine initialization finished!")
    
    def set_window(self, new_res):
        if self.win_res != new_res:
            self.win_res  = new_res
            self.win_surf = pygame.display.set_mode((self.win_res[0], self.win_res[1]), pygame.RESIZABLE)
    
    def draw_gme_to_window(self):
        scaled_display, new_pos = self.get_scaled_gme_surf()
        
        self.win_surf.blit(scaled_display, new_pos)
    
    def get_scaled_gme_surf(self):
        """
        HD display resolution: 1920, 1080
        Game resolution: 1200, 900
        
        1920 / 1200 = 1.6
        1080 / 900 = 1.2
         
        """
        self.win_res = [self.win_surf.get_width(), self.win_surf.get_height()]
        gme_scale = (self.win_res[0] / self.game_res[0], self.win_res[1] / self.game_res[1])
        #print(gme_scale)
        
        if gme_scale[0] > gme_scale[1]:
            working_scale = gme_scale[1]
        else:
            working_scale = gme_scale[0]
        
        scaled_game_surf = pygame.transform.scale(self.game_surf, (int(self.game_res[0] * working_scale),
                                                                   int(self.game_res[1] * working_scale)))
        #(1920 - (1200 * working_scale))/2 = to the halfway point of the screen
        
        win_pos = (self.win_res[0] - int(self.game_res[0] * working_scale))/2
        return scaled_game_surf, (win_pos, 0)
    
    def get_user_input(self):
        usr_in = {
            "key press":   [],
            "key lift":    [],
            "mouse press": [],
            "mouse lift":  [],
            "mouse pos":   ()
            }
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                usr_in["key press"].append(event.key)
            
            if event.type == pygame.KEYUP:
                usr_in["key lift"].append(event.key)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                usr_in["mouse press"].append(event.button)
            
            if event.type == pygame.MOUSEBUTTONUP:
                usr_in["mouse lift"].append(event.button)
            
            if event.type == pygame.MOUSEMOTION:
                usr_in["mouse pos"] = event.pos
            
            if event.type == pygame.QUIT:
                self.globl_vars["quit"] = True
        return usr_in
    
    def update_current(self):
        self.draw_gme_to_window()
        
        # Update modules
        self.time_mod.update()
        self.audio_mod.update(self.opt_mgr)
        self.event_mod.update()
        
        self.time_mod.clock.tick(self.fps)
        
        # Update global variables
        self.globl_vars["user_input"] = self.get_user_input()
        
        if self.scenes.get(self.current_scene) == None:
            raise Exception("X! Scene name: '" + self.current_scene + "' does not exist.")
        
        self.scenes[self.current_scene].update(self)
    
    def add_global_event(self, name, args):
        if self.globl_evnts.get(name) != None:
            print("X cannot write global event '" + name + "' it already exists!")
        else:
            self.globl_evnts[name] = args
    
    def add_global_var(self, name, value):
        if self.globl_vars.get(name) != None:
            print("X cannot write global variable '" + name + "' it already exists!")
        else:
            self.globl_vars[name] = value

    def add_scene(self, name, scene):
        if self.scenes.get(name) != None:
            print("X cannot write scene '" + name + "' it already exists!")
        else:
            self.scenes[name] = scene 

    def draw_current(self):
        self.game_surf.fill(self.fill_color)
        
        if self.scenes.get(self.current_scene) == None:
            raise Exception("X! Scene name: '" + self.current_scene + "' does not exist.")
        
        self.scenes[self.current_scene].draw(self)
        
        if self.opt_mgr.options.get("debug mode"):
            self.draw_debug_overlay()
    
    def draw_debug_overlay(self):
        debug_txt_dict = {"FPS": self.time_mod.clock.get_fps(),
                          "Current scene": self.current_scene,
                          "Current scene layers": self.scenes[self.current_scene].object_layers,
                          "Scenes": self.scenes,
                          "Global vars": self.globl_vars,
                          "Global events": self.globl_evnts,
                          "Current tck": self.time_mod.current_tick,
                          "Game tck": self.time_mod.game_tick,
                          "Start tcks": self.time_mod.start_ticks,
                          "Paused": self.time_mod.paused}
        
        debug_text = []
        for key, value in debug_txt_dict.items():
            debug_text.append(str(key) + ": " + str(value))
        
        for dti in range(len(debug_text)):
            debug_render = self.get_font_obj("Assets/Font/Computer Speak v0.3.ttf", size=12).render(debug_text[dti], 1, (255,0,0))
            debug_rect = debug_render.get_rect(topleft = (5,5 + (dti * 16)))
            self.game_surf.blit(debug_render, debug_rect)
    
    def get_image_surf(self, image_file, scale=(-1, -1)):
        img = pygame.image.load(image_file).convert_alpha()
        
        if scale == (-1,-1):
            return img
        else:
            return pygame.transform.scale(img, scale)
    
    def get_font_obj(self, font_file, size=12):
        return pygame.font.Font(font_file, size)
    
    def get_running(self):
        if self.globl_vars.get("quit") == None:
            self.globl_vars["quit"] = False
        return not self.globl_vars["quit"]


class Time_mod():
    def __init__(self, game_engine):
        self.gme_engine = game_engine
        
        self.clock        = pygame.time.Clock()
        self.current_tick = pygame.time.get_ticks()
        self.last_tick    = 0
        self.game_tick    = 0
        self.paused       = False
        self.start_ticks  = {}
        
        # Add global var
        self.gme_engine.globl_vars["reset_game_tick"] = False
        print("* Time module loaded")
    
    def update(self):
        self.last_tick    = self.current_tick
        self.current_tick = pygame.time.get_ticks()
        self.game_tick    = self.get_game_tick()
        #print("DEBUG: ", "curnt tck: " + str(self.current_tick), "gme tck: " + str(self.game_tick))
    
    def get_game_tick(self):
        if self.paused:
            return self.game_tick
        elif self.gme_engine.globl_vars.get("reset_game_tick"):
            self.gme_engine.globl_vars["reset_game_tick"] = False # Reset back to default
            
            return self.current_tick
        else:
            return self.game_tick + (self.current_tick - self.last_tick)
    
    def global_timer(self, time=1000, timer_tag="default"):
        start_time = 0
        
        # Creates new start time when none is taken
        if self.start_ticks.get(timer_tag) == None:
            self.start_ticks[timer_tag] = self.current_tick
            print("- Starting global timer with tag:", timer_tag)
        
        start_time  = self.start_ticks[timer_tag]
        target_time = start_time + time
        
        if self.current_tick > target_time:
            self.start_ticks.pop(timer_tag)
            print("- Ended global timer with tag:", timer_tag)
            return True
        return False
    
    def game_timer(self, time=1000, timer_tag="default"):
        start_time = 0
        
        # Creates new start time when none is taken
        if self.start_ticks.get(timer_tag) == None:
            self.start_ticks[timer_tag] = self.game_tick
            print("- Starting game timer with tag:", timer_tag)
        
        start_time  = self.start_ticks[timer_tag]
        target_time = start_time + time
        
        if self.game_tick > target_time:
            self.start_ticks.pop(timer_tag)
            print("- Ended game timer with tag:", timer_tag)
            return True
        return False


class Audio_mod():
    def __init__(self, game_engine):
        #
        # Channels:
        # 0 = menus/default/general purpose
        # 1 = player ship/enemy ships
        # 2 = lazer object sounds
        # 3 = obstacle object sounds
        # 4 = other
        
        self.gme_engine = game_engine
        
        pygame.mixer.pre_init(44100, 32, 1, 512)
        pygame.mixer.init()
        print("* Pygame mixer has been initialized in audio module")
        
        self.current_song = ""
        self.sounds = {"Menu Selection": "Assets/Audio/Menu Selection.wav",
                       "Menu Select": "Assets/Audio/Menu Select.wav",
                       "Lazer Shoot": "Assets/Audio/Lazer Shoot.wav"}
        self.sound_vol = 100
        self.music  = {"Gaze Upon the Stars": "Assets/Audio/Gaze Upon the Stars.wav",
                       "In The Beginning": "Assets/Audio/In The Beginning.wav",
                       "Nebulus": "Assets/Audio/Nebulus.wav"}
        self.music_vol = 100
        print("* Audio module loaded")
    
    def update(self, opt_mgr):
        self.set_vols(opt_mgr)
        
    def set_vols(self, opt_mgr):
        if opt_mgr.options.get("music volume") != None:
            self.music_vol = opt_mgr.options.get("music volume")
        
        if opt_mgr.options.get("sound volume") != None:
            self.sound_vol = opt_mgr.options.get("sound volume")
        
        pygame.mixer.music.set_volume(self.music_vol / 100)
    
    def play_audio(self, audio_name, channel_num=0, loop=0):
        if self.sounds.get(audio_name) != None:
            sound_obj = pygame.mixer.Sound(self.sounds.get(audio_name))
            sound_obj.set_volume(self.sound_vol / 100)
            
            pygame.mixer.Channel(channel_num).play(sound_obj, loops=loop)
        else:
            print("X Uh oh looks like audio file:", audio_name, "doesn't exist!")
    
    def play_music(self, song_nme):
        if not pygame.mixer.music.get_busy() or self.current_song != song_nme:
            if self.music.get(song_nme) != None:
                pygame.mixer.music.load(self.music.get(song_nme))
                pygame.mixer.music.play(-1)
                self.current_song = song_nme
            else:
                print("X Uh oh looks like music track:", song_nme, "doesn't exist!")


class Event_mod():
    def __init__(self, gme_engine):
        self.game_engine     = gme_engine
        self.discared_events = []
        print("* Event module loaded")
    
    def update(self):
        self.clean_up()
        
        for evnt, args in self.game_engine.globl_evnts.items():
            self.execute_event(evnt, args)
    
    def execute_event(self, evnt, args):
        if evnt == "quit game":
            self.game_engine.globl_vars["quit"] = True
        
        if evnt == "switch scene":
            print("DEBUG: ", "Switch scene:", str(args))
            
            if args in self.game_engine.scenes:
                self.game_engine.current_scene = args
            else:
                print("! Cannot switch to scene: '" + str(args) + "' it does not exist")
        
        if evnt == "play music":
            print("DEBUG: ", "Play song:", args)
            if args in self.game_engine.audio_mod.music.keys():
                self.game_engine.audio_mod.play_music(args)
            else:
                print("! Song '" + str(args) + "' does not exist")
        
        self.add_to_discard(evnt)
    
    def add_to_discard(self, event):
        if event not in self.discared_events:
            self.discared_events.append(event)
    
    def clean_up(self):
        for d_event in self.discared_events:
            self.game_engine.globl_evnts.pop(d_event)
            self.discared_events.remove(d_event)


class Options_mgr():
    def __init__(self, game_engine):
        self.game_engine     = game_engine
        self.options_file    = "options.json"
        self.default_options = {"resolution": [1200, 900],
                                "sound volume": 100,
                                "music volume": 100,
                                "debug mode": True,
                                "keybinds": {"up": pygame.K_w,
                                             "down": pygame.K_s,
                                             "left": pygame.K_a,
                                             "right": pygame.K_d,
                                             "shoot": pygame.K_j,
                                             "pause": pygame.K_p}}
        self.options         = {}
        print("* Option manager loaded")
        
    def get_opt_file(self):
        print("- Getting option file...")
        try:
            with open(self.options_file) as file:
                contents = json.load(file)
                print("* got file with no errors!")
            
        except FileNotFoundError:
            print("X file not found!")
            print("- Creating file...")
            self.create_file()
            
        except IsADirectoryError:
            print("X That is not a file!")
            print("- Creating file...")
            self.create_file()
        
        except Exception as e:
            print("X Json parse error:", e)
            print("- Overriding file...")
            self.create_file()
    
    def create_file(self):
        with open(self.options_file, "w") as file:
            file.write(json.dumps(self.default_options, indent=4))
    
    def load_file_to_opts(self):
        if self.options == self.default_options:
            print("! Options are loaded from default. Fix your errors or remove the file.")
        else:
            print("- Now loading options..")
            with open(self.options_file) as file:
                self.options = json.load(file)
                #print("DEBUG: ", self.options)
    
    def save_opts_to_file(self):
        pass


class Scene():
    def __init__(self, layers=["background", "default", "foreground"], workspace=[]):
        self.workspace = workspace
        
        self.object_layers = layers
        print("* Scene loaded")
    
    def update(self, gme_engine):
        
        for spr_obj in self.workspace:
            if type(spr_obj) == pygame.sprite.Group:
                
                for sprt in spr_obj:
                    sprt.update(gme_engine)
            else:
                spr_obj.update(gme_engine)
    
    def draw(self, gme_engine):
        for layer in self.object_layers:
            
            for spr_obj in self.workspace:
                if type(spr_obj) == pygame.sprite.Group:
                    
                    for sprt in spr_obj:
                        if sprt.layer == layer:
                            sprt.draw(gme_engine.game_surf)
                else:
                    if spr_obj.layer == layer:
                        spr_obj.draw(gme_engine.game_surf)


class Game_sprite(pygame.sprite.Sprite):
    def __init__(self, image, pos=[0,0], layer="default", angle=0):
        super().__init__()
        
        # Surface
        self.og_image = image
        self.image    = self.og_image
        
        # Transform values
        self.rotation = angle
        self.rect     = self.image.get_rect(center = (pos[0], pos[1]))
        
        # Other
        self.layer = layer
    
    def update_img(self):
        rottated_img = pygame.transform.rotate(self.og_image, self.rotation)
        
        self.image   = rottated_img
    
    def update_rect(self, move=[0,0]):
        new_rect = self.image.get_rect(center = (self.rect.centerx + move[0], self.rect.centery + move[1]))
        
        self.rect = new_rect
    
    def update(self, gme_engine):
        self.update_img()
        self.update_rect()
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)
        #pygame.draw.rect(surf, rect=self.rect, color=(255, 0, 0), width=1)

