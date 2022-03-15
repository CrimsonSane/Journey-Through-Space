import GLOBAL
import generalized_functions as gen_func

import pygame

# MOVING TEXT CLASS
class Moving_text(pygame.sprite.Sprite):
    def __init__(self, text, pos, spd, group):
        super().__init__()
        group.add(self)
        
        self.text = text
        self.spd = spd
        self.pos = pos
        
        self.image = gen_func.get_font(36).render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
    
    def update(self):
        if not GLOBAL.paused:
            # Move the text
            self.pos[0] += self.spd[0]
            self.pos[1] += self.spd[1]
        
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        
        if self.pos[1] < -10 or self.pos[1] > GLOBAL.WIN_HEIGHT:
            self.kill()
    
    def draw(self, disply):
        disply.blit(self.image, self.rect)