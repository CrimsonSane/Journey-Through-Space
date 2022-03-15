import random

import GLOBAL
import generalized_functions as gen_func
from objects.explosion import Explosion
from objects.item import Item

import pygame

# ASTROID CLASS
class Astroid(pygame.sprite.Sprite):
    def __init__(self, pos, imgs, spd_rng, group, spd=[0,random.randint(1,5)], pts=random.randint(1,6), is_astroid=True):
        super().__init__()
        group.add(self)
        
        self.is_astroid = is_astroid
        
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = [GLOBAL.scroll_spd * spd[0],GLOBAL.scroll_spd * spd[1]]
        self.spd_rng = spd_rng
        self.angleSpd = random.randint(-1,1)
        self.angle = random.randint(-360, 360)
        self.pos = pos
        
        self.pts = pts # Astroid points
        
        self.images = imgs # Contains lists inside
        
        self.image = random.choice(self.images[self.pts - 1])
        self.orignial_img = self.image # Save image for later
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        
        self.explosion = 0
        self.item = "NONE"
        self.item_chance = (1,2)
    
    def update(self):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
            self.image = pygame.transform.rotate(self.orignial_img, self.angle)
        
            # Rotate
            self.angle += self.angleSpd
        
        # Collision
        astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
        if astroid_collision_value != -1:
            # Trys to split both objects if in screen
            if self.pos[1] < -100:
                self.regen()
                GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
            else:
                self.split()
                GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                gen_func.play_sound(GLOBAL.astroid_explosion, GLOBAL.EXPLOSION_CHANNEL)
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT + 100 or self.pos[0] > self.WIDTH or self.pos[0] < 0:
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
        if self.item != "NONE":
                
            chance = random.randint(1,self.item_chance[1])
            if chance == self.item_chance[0]:
                Item(self.item, [self.pos[0],self.pos[1] - 5], [0,6], GLOBAL.item_group)
                self.item = "NONE"
            else:
                self.item = "NONE"
        
        if self.is_astroid:
            
            # Has to be an astroid to properly regen
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
        else:
            # Make an explosion if it is on the window
            if self.pos[1] > -10 and self.pos[1] < self.HEIGHT + 100:
                # Only display one explosion
                if self.explosion == 0:
                    self.explosion = 1
                    Explosion(self.spd, GLOBAL.explosion_group, [1,1, 1,1], self.pos)
            self.kill()
    
    def split(self):
        """
        4
        | <- -1
        V
        3
        | <- /2
        V
        1.5 -> round down to 1
        
        I call it The Twinstroid Algorithm since it always ends up with twins that split the same way.
        Meaning 2 point astroids are essentialy 1 point astroids and they don't split.
        """
        splitted_pts = int((self.pts - 1)/2) # The point was to round down but int can do the job.
        
        old_pos = self.pos
        if self.pos[1] > -10 and self.pos[1] < self.HEIGHT + 100:
            # Only display one explosion
            if self.explosion == 0:
                self.explosion = 1
                Explosion(self.spd, GLOBAL.explosion_group, [1,1, 1,1], self.pos)
        self.regen()
        
        if splitted_pts > 0:
            Astroid(pos=[old_pos[0]+(10*self.pts), old_pos[1]], imgs=self.images, spd=[1,3],
                    group=GLOBAL.astroids_group, pts=splitted_pts, is_astroid=False, spd_rng=[0,0, 0,0])
            Astroid(pos=[old_pos[0]+(-10*self.pts), old_pos[1]], imgs=self.images, spd=[-1,3],
                    group=GLOBAL.astroids_group, pts=splitted_pts, is_astroid=False, spd_rng=[0,0, 0,0])
        else:
            self.regen()
    
    def draw(self, disply):
        # Only display if on screen
        if self.pos[1] > -10:
            disply.blit(self.image, self.rect)