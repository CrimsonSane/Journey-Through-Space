import random

import GLOBAL
import generalized_functions as gen_func

import pygame

# LINE CLASS
class Line(pygame.sprite.Sprite):
    def __init__(self, imgs, spd, group, spd_rng):
        super().__init__()
        group.add(self)
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = [GLOBAL.scroll_spd * spd[0],GLOBAL.scroll_spd * spd[1]]
        self.spd_rng = spd_rng
        self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
        self.images = imgs
        self.image = random.choice(self.images)
        self.orignial_img = self.image # Save image for later
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        self.allow_regen = True
    
    def update(self, key_butns):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
        # This will make the line disappear once it regens
        if GLOBAL.scroll_spd < 5:
            self.allow_regen = False
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def regen(self):
        if self.allow_regen:
            self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
            self.image = random.choice(self.images)
            self.orignial_img = self.image
            
            self.spd[0] = GLOBAL.scroll_spd * random.randint(self.spd_rng[0],self.spd_rng[1])
            self.spd[1] = GLOBAL.scroll_spd * random.randint(self.spd_rng[2],self.spd_rng[3])
        else:
            self.kill()
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > 0:
            disply.blit(self.image, self.rect)