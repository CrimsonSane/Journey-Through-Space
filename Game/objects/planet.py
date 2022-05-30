import random

import GLOBAL
import generalized_functions as gen_func

import pygame

# PLANET CLASS
class Planet(pygame.sprite.Sprite):
    def __init__(self, spd, group, spd_rng):
        super().__init__()
        group.add(self)
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.ref_spd = [spd[0],spd[1]]
        self.spd = [GLOBAL.scroll_spd * self.ref_spd[0],GLOBAL.scroll_spd * self.ref_spd[1]]
        self.spd_rng = spd_rng
        self.angle = random.randint(-360, 360)
        self.size = random.randint(25, 100)
        self.pos = [random.randint(0,self.WIDTH),random.randint(0,self.HEIGHT)] # Randomize position
        
        self.angle_spd = random.randint(-1,1)
        self.angle_spd /= random.randint(5,25)
        
        self.images = [gen_func.get_image("Assets", "Planet1.png",(0,0)),
                       gen_func.get_image("Assets", "Planet2.png",(0,0)),
                       gen_func.get_image("Assets", "Planet3.png",(0,0)),
                       gen_func.get_image("Assets", "Planet4.png",(0,0)),
                       gen_func.get_image("Assets", "Planet5.png",(0,0))]
        self.image = pygame.transform.scale(random.choice(self.images),(self.size, self.size))
        self.orignial_img = self.image # Save image for later
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def update(self, key_butns):
        # Move with given speed
        if not GLOBAL.paused:
            self.spd = [GLOBAL.scroll_spd * self.ref_spd[0],GLOBAL.scroll_spd * self.ref_spd[1]]
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
            self.angle += self.angle_spd
        
        # rotate
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT + 25 or self.pos[0] > self.WIDTH + 25 or self.pos[0] < 0 - 25:
            self.regen()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
    
    def regen(self):
        self.pos = [random.randint(0,self.WIDTH),random.randint(-self.HEIGHT,0)] # Randomize position
        
        self.angle = random.randint(-360, 360)
        self.size = random.randint(25, 150)
        
        self.angle_spd = random.randint(-1,1)
        self.angle_spd /= random.randint(5,25)
        
        self.image = pygame.transform.scale(random.choice(self.images),(self.size, self.size))
        self.orignial_img = self.image
        self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
        self.ref_spd[0] = random.randint(self.spd_rng[0],self.spd_rng[1])
        self.ref_spd[1] = random.randint(self.spd_rng[2],self.spd_rng[3])
        
        self.spd = [GLOBAL.scroll_spd * self.ref_spd[0],GLOBAL.scroll_spd * self.ref_spd[1]]
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > 0:
            disply.blit(self.image, self.rect)