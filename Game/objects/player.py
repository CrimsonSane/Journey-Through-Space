import math

import GLOBAL
from objects.lazer import Lazer
import generalized_functions as gen_func
from objects.timer import Timer
from objects.explosion import Explosion

import pygame

# PLAYER CLASS 
class Player_space_ship(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        GLOBAL.player_group.add(self)
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.MAX_HEALTH = [4,5,6,7,8]
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
        
        self.shield_time = [5000, 6000, 7000, 8000, 10_000]
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
        
        self.spd_thruster_imgs = [gen_func.get_image("Assets","speed-thrusterFire-frame0.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame1.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame2.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame3.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame4.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame5.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame6.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame7.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame8.png", (0,0)),
                              gen_func.get_image("Assets","speed-thrusterFire-frame9.png", (0,0))]
        self.fire_image = self.thruster_imgs[0]
        self.spd_fire_image = self.spd_thruster_imgs[0]
        self.fire_rect = self.fire_image.get_rect(midtop = (self.pos[0],self.pos[1]+50))
        self.spd_fire_rect = self.fire_image.get_rect(midtop = (self.pos[0],self.pos[1]+50))
        self.fire_index = 0
        
        self.lazer_type = "PLAYER_NORM_LAZER"
        self.LAZER_COOLDOWNS = [8, 5, 20, 9, 10, 7]
        self.LAZER_REDUCTION = [[0,2,2,3,3],
                                [0,1,1,2,2],
                                [0,5,5,6,6],
                                [0,2,2,3,3],
                                [0,3,3,4,4],
                                [0,1,1,2,2]]
        self.lazer_cooldown = self.LAZER_COOLDOWNS[0]
        self.shoot_start_time = -1
        self.lazer_timer = Timer()
        
        self.upgrade = 0
        self.MAX_UPGRADE = 4
        
        self.speed_hoop_timer = Timer()
        self.speed_hoop_strt_time = -1
        self.speed_hoop_amt = 0
        self.speed_hop = False
    
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
            self.spd_fire_image = pygame.transform.rotate(self.spd_thruster_imgs[self.fire_index], self.angle)
            self.spd_fire_rect = self.spd_fire_image.get_rect(midtop = (15*math.sin(math.radians(self.angle)) + self.pos[0], self.pos[1] + 5 + math.cos(math.radians(self.angle))))
            self.fire_rect = self.fire_image.get_rect(midtop = (15*math.sin(math.radians(self.angle)) + self.pos[0], self.pos[1] + 5 + math.cos(math.radians(self.angle))))
            
            # if player isn't dead
            if self.health > 0:
                # Speed hop if allowed
                if self.speed_hop:
                    self.do_speed_hop()
                
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
            self.latest_health = self.health
            self.shield_bool = True
        # Activate shield
        if self.shield_bool:
            self.shield(self.shield_time[self.upgrade])
        # Health reaches zero
        if self.health <= 0 and self.display_player == True:
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
        
        # Scrap collision
        scrap_collision_value = self.check_collision(GLOBAL.scraps_group)
        if scrap_collision_value != -1:
            if len(GLOBAL.scraps_group) != 0:
                GLOBAL.scraps_group.sprites()[scrap_collision_value].regen()
            # If the latest health is equal to current health
            if self.latest_health == self.health:
                
                # If the player is not protected
                if not self.shield_bool:
                    self.health -= 1
                    gen_func.play_sound(GLOBAL.player_hit, GLOBAL.PLAYER_CHANNEL)
                else:
                    # It plays a lazer sound if the astroid hits while the player has a shield
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_CHANNEL)
        
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
            self.shoot_start_time = self.lazer_timer.get_start_time(self.shoot_start_time)
            
            current_time, target_time = self.lazer_timer.start(self.shoot_start_time, COOLDOWN_TIME, True)
            
            if current_time >= target_time:
                self.lazer_cooldown -= 1
                self.shoot_start_time = -1
    
    def set_speed_hop(self, time):
        SPEED_AMT = 5
        
        self.speed_hoop_strt_time = -1
        self.shield_start_time = -1
        self.speed_hoop_amt = time
        self.speed_hop = True
        self.shield_bool = True
        if GLOBAL.zone_id < len(GLOBAL.ZONE_VALUES[0]) - 1:
            GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][GLOBAL.zone_id] + SPEED_AMT
        else:
            GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][len(GLOBAL.ZONE_VALUES[0]) - 1] + SPEED_AMT
        GLOBAL.speed_skip += time
    
    def do_speed_hop(self):
        EXTRA_TIME = 5000
        self.speed_hoop_strt_time = self.speed_hoop_timer.get_start_time(self.speed_hoop_strt_time)
        current_time, target_time = self.speed_hoop_timer.start(self.speed_hoop_strt_time, self.speed_hoop_amt, True)
        
        self.shield(self.speed_hoop_amt + EXTRA_TIME)
        
        if current_time >= target_time:
            if GLOBAL.zone_id < len(GLOBAL.ZONE_VALUES[0]) - 1:
                GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][GLOBAL.zone_id]
            else:
                GLOBAL.scroll_spd = GLOBAL.ZONE_VALUES[0][len(GLOBAL.ZONE_VALUES[0]) - 1]
            self.speed_hop = False
    
    def shield(self, on_time):
        self.shield_start_time = self.shield_timer.get_start_time(self.shield_start_time)
        current_time, target_time = self.shield_timer.start(self.shield_start_time, on_time, True)
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
                if self.upgrade > 3:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-5, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0], self.pos[1]-1], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-5, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                
                if self.upgrade >= 2:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-5, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0], self.pos[1]-1], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-5, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    
                else:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                
                self.lazer_cooldown = self.LAZER_COOLDOWNS[0] - self.LAZER_REDUCTION[0][self.upgrade]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # Rapid fire player lazer
        elif self.lazer_type == "PLAYER_RAPID_LAZER":
            
            if self.lazer_cooldown <= 0:
                if self.upgrade > 3:
                    Lazer(pos=[self.pos[0]-7, self.pos[1]-2], spd=-10, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+7, self.pos[1]-2], spd=-9, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    
                    Lazer(pos=[self.pos[0]-9, self.pos[1]-2], spd=-9, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+9, self.pos[1]-2], spd=-10, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    
                if self.upgrade >= 2:
                    Lazer(pos=[self.pos[0]-7, self.pos[1]-2], spd=-8, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+7, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    
                    Lazer(pos=[self.pos[0]-9, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+9, self.pos[1]-2], spd=-8, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    
                else:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                
                self.lazer_cooldown = self.LAZER_COOLDOWNS[1] - self.LAZER_REDUCTION[1][self.upgrade]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # player lazer cannon
        elif self.lazer_type == "PLAYER_CANNON_LAZER":
            
            if self.lazer_cooldown <= 0:
                if self.upgrade > 3:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                
                elif self.upgrade >= 2:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                
                else:
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                
                self.lazer_cooldown = self.LAZER_COOLDOWNS[2] - self.LAZER_REDUCTION[2][self.upgrade]
                gen_func.play_sound(GLOBAL.lazer_cannon_shooting, GLOBAL.LAZER_CHANNEL)
        # Split fire player lazer
        elif self.lazer_type == "PLAYER_SPLIT_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-7, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[3] - self.LAZER_REDUCTION[3][self.upgrade]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # Pierce fire player lazer
        elif self.lazer_type == "PLAYER_PIERCE_LAZER":
            
            if self.lazer_cooldown <= 0:
                Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-8, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-8, angle=self.angle,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type, destry_scrap=True)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[4] - self.LAZER_REDUCTION[4][self.upgrade]
                gen_func.play_sound(GLOBAL.lazer_shooting, GLOBAL.LAZER_CHANNEL)
        # Spread fire player lazer
        elif self.lazer_type == "PLAYER_SPREAD_LAZER":
            
            if self.lazer_cooldown <= 0:
                OFFSET_ANGLE0 = 30
                OFFSET_ANGLE1 = 15
                
                UPGRADED_OFFSET_ANGLE0 = 45
                UPGRADED_OFFSET_ANGLE1 = 20
                
                if self.upgrade > 3:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type="PLAYER_SPLIT_LAZER", destry_scrap=True)
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type="PLAYER_SPLIT_LAZER", destry_scrap=True)
                
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type="PLAYER_SPLIT_LAZER", destry_scrap=True)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type="PLAYER_SPLIT_LAZER", destry_scrap=True)
                    
                elif self.upgrade >= 2:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + UPGRADED_OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + UPGRADED_OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - UPGRADED_OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - UPGRADED_OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    
                else:
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]-8, self.pos[1]-2], spd=-6, angle=self.angle + OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - OFFSET_ANGLE1,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                    Lazer(pos=[self.pos[0]+8, self.pos[1]-2], spd=-6, angle=self.angle - OFFSET_ANGLE0,
                      group=GLOBAL.lazer_group, lazer_type=self.lazer_type)
                self.lazer_cooldown = self.LAZER_COOLDOWNS[5] - self.LAZER_REDUCTION[5][self.upgrade]
                
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
            if len(group) == 0:
                return -1
    
    def draw(self, disply):
        if self.display_player:
            # Display normal thruster flame when bellow a certain speed
            if GLOBAL.scroll_spd < 5:
                disply.blit(self.fire_image, self.fire_rect)
            else:
                disply.blit(self.spd_fire_image, self.spd_fire_rect)
            
            disply.blit(self.image, self.rect)
        if self.display_shield:
            disply.blit(self.bubble_img, self.shield_rect)