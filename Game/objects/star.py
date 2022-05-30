import random

import GLOBAL
import generalized_functions as gen_func

import pygame

# STAR CLASS
class Star(pygame.sprite.Sprite):
    def __init__(self, imgs, spd, group, spd_rng):
        super().__init__()
        group.add(self)
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.ref_spd = [spd[0],spd[1]]
        self.spd = [GLOBAL.scroll_spd * self.ref_spd[0],GLOBAL.scroll_spd * self.ref_spd[1]]
        self.spd_rng = spd_rng
        self.angle = random.randint(-360, 360)
        self.pos = [random.randint(0,self.WIDTH),random.randint(0,self.HEIGHT)] # Randomize position
        self.images = imgs
        self.image = random.choice(self.images)
        self.orignial_img = self.image # Save image for later
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def update(self, key_butns):
        # Move with given speed
        if not GLOBAL.paused:
            self.spd = [GLOBAL.scroll_spd * self.ref_spd[0],GLOBAL.scroll_spd * self.ref_spd[1]]
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def regen(self):
        self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
        self.image = random.choice(self.images)
        self.orignial_img = self.image
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        self.ref_spd[0] = random.randint(self.spd_rng[0],self.spd_rng[1])
        self.ref_spd[1] = random.randint(self.spd_rng[2],self.spd_rng[3])
        
        self.spd = [GLOBAL.scroll_spd * self.ref_spd[0],GLOBAL.scroll_spd * self.ref_spd[1]]
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > 0:
            disply.blit(self.image, self.rect)