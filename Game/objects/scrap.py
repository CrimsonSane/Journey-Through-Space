import random

import GLOBAL
import generalized_functions as gen_func
from objects.explosion import Explosion

import pygame

# SCRAP CLASS
class Scrap(pygame.sprite.Sprite):
    def __init__(self, pos, imgs, spd_rng, group, spd=[random.randint(-2,2),random.randint(1,5)], pts=random.randint(1,2)):
        super().__init__()
        group.add(self)
        
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = [GLOBAL.scroll_spd * spd[0],GLOBAL.scroll_spd * spd[1]]
        self.spd_rng = spd_rng
        self.angleSpd = random.randint(-1,1)
        self.angle = random.randint(-360, 360)
        self.pos = pos
        
        self.pts = pts # Scrap points
        
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
        
        # Astroid collision
        astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
        if astroid_collision_value != -1:
            # Trys to split astroid objects if in screen
            if self.pos[1] < -100:
                GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
            else:
                GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                gen_func.play_sound(GLOBAL.astroid_explosion, GLOBAL.EXPLOSION_CHANNEL)
        
        # Scrap collision
        scrap_collision_value = self.check_collision(GLOBAL.scraps_group)
        if scrap_collision_value != -1:
            
            REDUCTION = 8
            
            other_scrap = GLOBAL.scraps_group.sprites()[scrap_collision_value]
            
            if self.pts > other_scrap.pts:
                self.spd = [self.spd[0] + (self.pts / REDUCTION), self.spd[1] + (self.pts / REDUCTION)]
                other_scrap.spd = [other_scrap.spd[0] - (self.pts / REDUCTION), other_scrap.spd[1] - (self.pts / REDUCTION)]
            else:
                other_scrap.spd = [other_scrap.spd[0] + (other_scrap.pts / REDUCTION), other_scrap.spd[1] + (other_scrap.pts / REDUCTION)]
                self.spd = [self.spd[0] - (other_scrap.pts / REDUCTION), self.spd[1] - (other_scrap.pts / REDUCTION)]
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT + 100 or self.pos[0] > self.WIDTH or self.pos[0] < 0 or self.pos[1] < -self.HEIGHT - 100:
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
            if len(group) == 0:
                return -1
    
    def regen(self):
        # Make an explosion if it is on the window
        if self.pos[1] > -10 and self.pos[1] < self.HEIGHT + 100:
            # Only display one explosion
            if self.explosion == 0:
                self.explosion = 1
                Explosion(self.spd, GLOBAL.explosion_group, [1,1, 2,2], self.pos)
        
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
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > -10:
            disply.blit(self.image, self.rect)