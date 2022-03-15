import GLOBAL
import generalized_functions as gen_func
from objects.timer import Timer
from objects.moving_text import Moving_text

import pygame

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
            self.og_image = self.image
            self.desc = "HEALTH"
        
        elif self.item_name == "SCREW_DRIVER":
            self.image = gen_func.get_image("Assets","ScrewDriver.png",ITEM_SIZE)
            self.og_image = self.image
            self.desc = "UPGRADE"
        
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
        
        elif self.item_name == "SPEED_HOOP":
            self.image = gen_func.get_image("Assets","SpeedHoop.png",GUN_ITEM_SIZE)
            self.og_image = self.image
            self.desc = "SPEED HOOP"
        
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        
        self.text = gen_func.get_font(20).render(self.desc,1,(255,255,255))
        self.text_rect = self.text.get_rect(center = (self.pos[0], self.pos[1]+32))
    
    def update(self):
        # Move the text
        if not GLOBAL.paused:
            self.pos[0] += self.spd[0]
            self.pos[1] += self.spd[1]
            self.angle += self.angle_spd
        
        if self.item_name != "SPEED_HOOP":
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
                if plyer.health < plyer.MAX_HEALTH[plyer.upgrade]:
                    plyer.health += 1
                    self.kill()
                else:
                    GLOBAL.score += BONUS_SCORE
                    Moving_text(str(BONUS_SCORE), self.pos, [self.spd[0],-self.spd[1]], GLOBAL.mving_txt_group)
                    
                    self.kill()
            # Screw drivers increases upgrade attribute which improve weapons, max health and shield durability
            if self.item_name == "SCREW_DRIVER":
                gen_func.play_sound(GLOBAL.item_collect, GLOBAL.PLAYER_CHANNEL)
                if plyer.upgrade < plyer.MAX_UPGRADE:
                    plyer.upgrade += 1
                    self.kill()
                else:
                    GLOBAL.score += BONUS_SCORE + 500
                    Moving_text(str(BONUS_SCORE + 500), self.pos, [self.spd[0],-self.spd[1]], GLOBAL.mving_txt_group)
                    
                    self.kill()
            # Speed hoops speed the player through the zone
            if self.item_name == "SPEED_HOOP":
                gen_func.play_sound(GLOBAL.item_collect, GLOBAL.PLAYER_CHANNEL)
                
                # Speed up screen and decrease zone target time
                plyer.set_speed_hop(GLOBAL.SPEED_SKIP_TIME)
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
        
        if astroid_collision_value != -1:
            GLOBAL.astroids_group.sprites()[astroid_collision_value].item = self.item_name
            GLOBAL.astroids_group.sprites()[astroid_collision_value].item_chance = (1,2)
            self.kill()
    
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
        if self.desc != "":
            disply.blit(self.text, self.text_rect)