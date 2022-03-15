import random

import GLOBAL
import generalized_functions as gen_func
from objects.timer import Timer
from objects.moving_text import Moving_text

import pygame

# EXPLOSION CLASS
class Explosion(pygame.sprite.Sprite):
    def __init__(self, spd, group, size, pos, destroy_objs=False):
        super().__init__()
        group.add(self)
        
        self.destroy_objs = destroy_objs
        
        self.WIDTH = GLOBAL.WIN_WIDTH
        self.HEIGHT = GLOBAL.WIN_HEIGHT
        
        self.spd = spd
        self.angle = random.randint(-360, 360)
        self.size = size
        self.pos = pos
        self.images = [gen_func.get_image("Assets","Explosion-frame-0.png",(size[0]*0,size[1]*0)),
                        gen_func.get_image("Assets","Explosion-frame-1.png",(size[0]*32,size[1]*32)),
                        gen_func.get_image("Assets","Explosion-frame-2.png",(size[0]*32,size[1]*32)),
                        gen_func.get_image("Assets","Explosion-frame-2.png",(size[0]*32,size[1]*32)),
                        gen_func.get_image("Assets","Explosion-frame-3.png",(size[0]*44,size[1]*44)),
                        gen_func.get_image("Assets","Explosion-frame-3.png",(size[0]*44,size[1]*44)),
                        gen_func.get_image("Assets","Explosion-frame-4.png",(size[0]*54,size[1]*54)),
                        gen_func.get_image("Assets","Explosion-final-frame.png",(size[0]*64,size[1]*64)),
                        gen_func.get_image("Assets","Explosion-final-frame.png",(size[0],size[1])),
                        gen_func.get_image("Assets","Explosion-frame-6.png",(size[2]*66,size[3]*66)),
                        gen_func.get_image("Assets","Explosion-frame-7.png",(size[2]*76,size[3]*76)),
                        gen_func.get_image("Assets","Explosion-frame-8.png",(size[2]*86,size[3]*86)),
                        gen_func.get_image("Assets","Explosion-frame-9.png",(size[2]*96,size[3]*96)),
                        gen_func.get_image("Assets","Explosion-frame-10.png",(size[2]*106,size[3]*106)),
                        gen_func.get_image("Assets","Explosion-frame-11.png",(size[2]*116,size[3]*116)),
                        gen_func.get_image("Assets","Explosion-frame-12.png",(size[2]*126,size[3]*126)),
                        gen_func.get_image("Assets","Explosion-frame-12.png",(size[2]*136,size[3]*136))]
        self.image = self.images[0]
        self.orignial_imgs = self.images # Save images for later
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
        
        self.start_time = pygame.time.get_ticks()
        self.image_index = 0
        
        self.timer = Timer()
    
    def update(self):
        # Move with given speed
        if not GLOBAL.paused:
            self.pos = [self.pos[0]+self.spd[0], self.pos[1]+self.spd[1]]
        
        timeSinceEnter = pygame.time.get_ticks() - self.start_time
       
        time = (self.image_index + 1) * 50
        current_time, target_time = self.timer.start(self.start_time, time)

        if self.image_index < len(self.images) - 1:
            # Rotate
            self.image = pygame.transform.rotate(self.orignial_imgs[self.image_index], self.angle)
            
            if target_time <= current_time:
                # Move to the next image
                self.image_index += 1
        # Destroy the object the animation has finished
        elif self.image_index >= len(self.images) - 1:
            self.kill()
        
        # If object moves out of screen
        if self.pos[1] > self.HEIGHT or self.pos[0] > self.WIDTH or self.pos[0] < 0:
            self.kill()
        else:
            self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))
            
        if self.destroy_objs:
            # Collision
            astroid_collision_value = self.check_collision(GLOBAL.astroids_group)
            if astroid_collision_value != -1:
                # Trys to split objects if in screen
                
                if self.pos[1] < 0:
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].regen()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
                else:
                    # Add and display points
                    GLOBAL.score += GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]
                    Moving_text(str(GLOBAL.ASTROID_SCORE_AMTS[GLOBAL.astroids_group.sprites()[astroid_collision_value].pts]),
                                self.pos, [0,-self.spd[1]], GLOBAL.mving_txt_group)
                    
                    GLOBAL.astroids_group.sprites()[astroid_collision_value].split()
                    gen_func.play_sound(GLOBAL.lazer_hit, GLOBAL.LAZER_HIT_CHANNEL)
    
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