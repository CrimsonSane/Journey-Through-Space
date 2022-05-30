import GLOBAL
import generalized_functions as gen_func
from objects.moving_text import Moving_text
from objects.explosion import Explosion

import pygame

# LAZER CLASS
class Lazer(pygame.sprite.Sprite):
    def __init__(self, pos, group, lazer_type="PLAYER_NORM_LAZER", spd=-1, angle=0, destry_scrap=False):
        super().__init__()
        group.add(self)
        
        self.lazer_type = lazer_type
        self.can_destroy_scrap = destry_scrap
        
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
    
    def update(self, key_butns):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0] + self.spd * (self.angle/30), self.pos[1] + self.spd]
            self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        # Scrap collision
        scrap_collision_value = self.check_collision(GLOBAL.scraps_group)
        if scrap_collision_value != -1:
            CURRENT_SPD = [self.spd * (self.angle/30), self.spd]
            
            if self.can_destroy_scrap:
                if self.lazer_type == "PLAYER_CANNON_LAZER":
                    EXPLOSION_SIZE = 3
                    
                    # If is not on screen
                    if self.pos[1] < 0:
                        GLOBAL.scraps_group.sprites()[scrap_collision_value].regen()
                        if self.explosion == 0:
                            self.explosion = 1
                            gen_func.play_sound(GLOBAL.lazer_cannon_hit, GLOBAL.EXPLOSION_CHANNEL)
                            Explosion(CURRENT_SPD, GLOBAL.explosion_group, [2,2, EXPLOSION_SIZE,EXPLOSION_SIZE], self.pos, True)
                        self.kill()
                    else:
                        # Add and display points
                        GLOBAL.score += GLOBAL.SCRAP_SCORE_AMTS[GLOBAL.scraps_group.sprites()[scrap_collision_value].pts]
                        Moving_text(str(GLOBAL.SCRAP_SCORE_AMTS[GLOBAL.scraps_group.sprites()[scrap_collision_value].pts]),
                                    self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                        
                        GLOBAL.scraps_group.sprites()[scrap_collision_value].regen()
                        if self.explosion == 0:
                            self.explosion = 1
                            gen_func.play_sound(GLOBAL.lazer_cannon_hit, GLOBAL.EXPLOSION_CHANNEL)
                            Explosion(CURRENT_SPD, GLOBAL.explosion_group, [2,2, EXPLOSION_SIZE,EXPLOSION_SIZE], self.pos, True)
                        self.kill()
                elif self.lazer_type == "PLAYER_PIERCE_LAZER":
                    PIERCE_MAX = 2
                    # If is not on screen
                    if self.pos[1] < 0:
                        GLOBAL.scraps_group.sprites()[scrap_collision_value].regen()
                        gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                        self.kill()
                    elif self.hits >= PIERCE_MAX:
                        self.kill()
                    else:
                        # Add and display points
                        GLOBAL.score += GLOBAL.SCRAP_SCORE_AMTS[GLOBAL.scraps_group.sprites()[scrap_collision_value].pts]
                        Moving_text(str(GLOBAL.SCRAP_SCORE_AMTS[GLOBAL.scraps_group.sprites()[scrap_collision_value].pts]),
                                    self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                        
                        GLOBAL.scraps_group.sprites()[scrap_collision_value].regen()
                        gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                        self.hits += 1
                else:
                    # If is not on screen
                    if self.pos[1] < 0:
                        GLOBAL.scraps_group.sprites()[scrap_collision_value].regen()
                        gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                        self.kill()
                    else:
                        # Add and display points
                        GLOBAL.score += GLOBAL.SCRAP_SCORE_AMTS[GLOBAL.scraps_group.sprites()[scrap_collision_value].pts]
                        Moving_text(str(GLOBAL.SCRAP_SCORE_AMTS[GLOBAL.scraps_group.sprites()[scrap_collision_value].pts]),
                                    self.pos, [0,-self.spd], GLOBAL.mving_txt_group)
                        
                        GLOBAL.scraps_group.sprites()[scrap_collision_value].regen()
                        gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                        self.kill()
            else:
                REDUCTION = 20
                
                scrap_spd = GLOBAL.scraps_group.sprites()[scrap_collision_value].spd
                #gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                Explosion(scrap_spd, GLOBAL.explosion_group, [0.1,0.1, 0.1,0.1], self.pos)
                GLOBAL.scraps_group.sprites()[scrap_collision_value].health -= 1
                
                GLOBAL.scraps_group.sprites()[scrap_collision_value].spd = [scrap_spd[0] + (self.spd * (self.angle/30) / REDUCTION),
                                                                            scrap_spd[1] + (self.spd / REDUCTION)]
                self.kill()
        
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
            if len(group) == 0:
                return -1
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)