import math, random, pygame

import engine

class Transform_sprite(engine.Game_sprite):
    def __init__(self, image, final_trans, spd=10, pos=[0,0], layer="default", angle=0):
        super().__init__(image, pos, layer, angle)
        
        self.final_transform = final_trans
        self.speed           = spd
    
    def update_img(self):
        rottated_img = pygame.transform.rotate(self.og_image, self.rotation)
        
        self.image   = rottated_img
    
    def update_rect(self, move=[0,0]):
        new_rect = self.image.get_rect(center = (self.rect.centerx + move[0], self.rect.centery + move[1]))
        
        self.rect = new_rect
    
    def update(self, gme_engine):
        self.update_img()
        self.update_rect()
        
        if self.final_transform.get("pos") != None:
            # Get direction
            x_distance = self.final_transform["pos"][0] - self.rect.centerx
            y_distance = self.final_transform["pos"][1] - self.rect.centery
            
            # 1 to self.speed
            x_spd_mod = 1
            if abs(x_distance) < self.speed:
                x_spd_mod = self.speed
            y_spd_mod = 1
            if abs(y_distance) < self.speed:
                y_spd_mod = self.speed
            
            if int(x_distance) > 0:
                self.rect.centerx += self.speed // x_spd_mod
            elif int(x_distance) < 0:
                self.rect.centerx -= self.speed // x_spd_mod
            
            if int(y_distance) > 0:
                self.rect.centery += self.speed // y_spd_mod
            elif int(y_distance) < 0:
                self.rect.centery -= self.speed // y_spd_mod
            
            #print(x_spd_mod, y_spd_mod)
            #print(x_distance, y_distance)
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Space_decor_sprite(engine.Game_sprite):
    def __init__(self, images, act_spd=[0,0], pos=[0,0], layer="default", angle=0):
        chosen_img = random.choice(images)
        super().__init__(chosen_img, pos, layer, angle)
        
        self.images       = images
        self.actual_speed = act_spd
    
    def update_img(self):
        rottated_img = pygame.transform.rotate(self.og_image, self.rotation)
        
        self.image   = rottated_img
    
    def update_rect(self, move=[0,0]):
        new_rect = self.image.get_rect(center = (self.rect.centerx + move[0], self.rect.centery + move[1]))
        
        self.rect = new_rect
    
    def update(self, gme_engine):
        self.update_img()
        self.update_rect()
        
        if not gme_engine.time_mod.paused:
            self.rect.centery += gme_engine.globl_vars["player_speed"]
            #print("DEBUG: ", "center y:", self.rect.centery)
        
        if self.rect.centery > gme_engine.game_res[1] + self.rect.height:
            self.regen(gme_engine)
    
    def regen(self, gme_engine):
        chosen_img = random.choice(self.images)
        self.image = chosen_img
        self.og_image = self.image
        
        self.rect.centerx = random.randint(0, gme_engine.game_res[0])
        self.rect.centery = random.randint(-gme_engine.game_res[1], 0)
        
        self.rotation = random.randint(-360, 360)
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Weapon_sys():
    def __init__(self, ship, bullet_poses=[], facing=1):
        self.ship = ship
        self.bullet_poses = bullet_poses
        self.current_weapon = "basic"
        self.allow_fire = True
        
        if abs(facing) == 1:
            self.facing = facing
        elif facing != 0:
            self.facing = abs(facing) // facing
        else:
            self.facing = 1
        
        # Weapon key:
        # [ Name
        #   Description
        #   Cooldown
        #   Bullet Speed
        #   Cooldown Time
        #   Strength
        #   auto fire
        #   Shoot Sound
        #   Hit Sound
        #   Bullet Asset ]
        self.weapons = {"basic":{"name": "Basic Lazer Gun",
                                 "description": "The default lazer gun equiped in all T1 FSC Star Fighters. One of the cheapest and weakest lazer guns in the galaxy.",
                                 "cooldown": 250,
                                 "bullet speed": 10,
                                 "autofire": False,
                                 "strength": 1,
                                 "shoot sound": "Lazer Shoot",
                                 "hit sound": "Lazer Hit",
                                 "bullet asset": "Assets/Lazers/Lazer.png"}}
    
    def update(self, gme_engine):
        if not self.allow_fire:
            self.allow_fire = gme_engine.time_mod.game_timer(time=self.weapons[self.current_weapon]["cooldown"], timer_tag=self.current_weapon + str(self.ship))
    
    def shoot(self, gme_engine):
        if self.allow_fire:
            print("DEBUG: ", "pew")
            gme_engine.audio_mod.play_audio(self.weapons[self.current_weapon]["shoot sound"], channel_num=1)
            self.place_bullets(gme_engine)
            self.allow_fire = False
    
    def place_bullets(self, gme_engine):
        for p in self.bullet_poses:
            image = gme_engine.get_image_surf(self.weapons[self.current_weapon]["bullet asset"])
            position = [p[0] + self.ship.rect.centerx, p[1] + self.ship.rect.centery]
            speed = self.weapons[self.current_weapon]["bullet speed"] * self.facing
            
            gme_engine.globl_vars["bullet_sprite_group"].add(Bullet(image, position, self.ship.rotation, speed))


class Bullet(engine.Game_sprite):
    def __init__(self, img, pos=[0,0], angle=0, speed=0):
        super().__init__(img, pos, angle=angle)
        self.id = id(self)
        self.speed = speed
        
        self.movement_vector = pygame.Vector2(0, speed)
        self.movement_vector.rotate_ip(-self.rotation)
    
    def update(self, gme_engine):
        super().update(gme_engine)
        
        if not gme_engine.time_mod.paused:
            self.rect.centerx += self.movement_vector.x
            self.rect.centery += self.movement_vector.y
            
            if gme_engine.time_mod.game_timer(time=5000, timer_tag=self.id):
                self.kill()


class Thrust_sys(engine.Game_engine):
    def __init__(self, ship, imgs, thruster_pos=[0,0]):
        pos = [thruster_pos[0] + ship.rect.centerx, thruster_pos[1] + ship.rect.centery]
        super().__init__(imgs, pos)
        
        self.imgs = imgs
        self.ship = ship

    
class Player_ship(engine.Game_sprite):
    def __init__(self, img, thruster_imgs, pos=[1200 / 2, 800]):
        super().__init__(img, pos)
        
        self.speed = 20
        self.controls = {"left": False,
                         "right": False,
                         "shoot": False}
        self.velocity = 0.0
        self.max_angle = 45
        
        self.weapon_system = Weapon_sys(self, facing=-1, bullet_poses=[[-10, -5],
                                                                       [10, -5]])
        self.thruster_system = Thrust_sys(self, thruster_imgs, thruster_pos=[0, 12])
    
    def update(self, gme_engine):
        super().update(gme_engine)
        
        self.update_controls(gme_engine)
        self.weapon_system.update(gme_engine)
        self.thruster_system.update(gme_engine)
        
        if not gme_engine.time_mod.paused:
            self.execute_controls(gme_engine)
        
    def inc_vel(self):
        if self.velocity < 1.0:
            self.velocity += 0.1
    
    def dec_vel(self):
        if self.velocity > -1.0:
            self.velocity -= 0.1
        
    def stab_vel(self):
        if abs(self.velocity) < 0.1:
            self.velocity = 0
        
        elif self.velocity > 0.0:
            self.velocity -= 0.1
        
        elif self.velocity < 0.0:
            self.velocity += 0.1
        
    def update_angle(self):
        self.rotation = -self.max_angle * self.velocity
        
    def execute_controls(self, gme_engine):
        # Left and right movement
        #print("DEBUG: ", "Velocity:" + str(self.velocity))
        if self.controls["left"]:
            self.dec_vel()
        
        elif self.controls["right"]:
            self.inc_vel()
        
        else:
            self.stab_vel()
        self.rect.centerx += self.speed * self.velocity
        self.update_angle()
        
        if self.controls["shoot"]:
            self.weapon_system.shoot(gme_engine)
    
    def update_controls(self, gme_engine):
        if gme_engine.opt_mgr.options["keybinds"]["left"] in gme_engine.globl_vars["user_input"]["key press"]:
            #print("DEBUG: ", "left")
            self.controls["left"] = True
        elif gme_engine.opt_mgr.options["keybinds"]["left"] in gme_engine.globl_vars["user_input"]["key lift"]:
            self.controls["left"] = False
        
        if gme_engine.opt_mgr.options["keybinds"]["right"] in gme_engine.globl_vars["user_input"]["key press"]:
            #print("DEBUG: ", "right")
            self.controls["right"] = True
        elif gme_engine.opt_mgr.options["keybinds"]["right"] in gme_engine.globl_vars["user_input"]["key lift"]:
            self.controls["right"] = False
        
        if self.weapon_system.weapons[self.weapon_system.current_weapon]["autofire"]:
            if gme_engine.opt_mgr.options["keybinds"]["shoot"] in gme_engine.globl_vars["user_input"]["key press"]:
                #print("DEBUG: ", "shoot auto fire")
                self.controls["shoot"] = True
            elif gme_engine.opt_mgr.options["keybinds"]["shoot"] in gme_engine.globl_vars["user_input"]["key lift"]:
                self.controls["shoot"] = False
        else:
            if self.controls["shoot"]:
                self.controls["shoot"] = False
            
            elif gme_engine.opt_mgr.options["keybinds"]["shoot"] in gme_engine.globl_vars["user_input"]["key press"]:
                #print("DEBUG: ", "shoot not auto fire")
                self.controls["shoot"] = True

