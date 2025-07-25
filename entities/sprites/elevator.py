# General
import pygame, math
from core.pygame.pygame_util import generic_colors

import pygame, random
from pygame.locals import *

# CF
from controllers.cf_info import (
    pixel_space_to_scale
)
from core.pygame.cf_util import *
from .cf_sounds import *




class Elevator(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=(0,0),
        transparency_collide=255, transparency_sprite=255, move_dimension=1, 
        moving_objects=None, anim_sprites=None, solid_objects=None, layer_all_sprites=None
    ):
        super().__init__()
        
        self.__solid_objects = solid_objects
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        size_ready = (size*2, size)
        self.surf = pygame.Surface( size_ready, pygame.SRCALPHA)
        self.surf.fill( generic_colors('grey', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=2)
        moving_objects.add(self)
        anim_sprites.add(self)
        
        # Sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = get_image('elevator', size=size_ready, transparency=self.transparency_sprite)
        self.sprite.rect = self.sprite.surf.get_rect( topleft=(self.rect.x, self.rect.y) )
        layer_all_sprites.add(self.sprite, layer=1)
        
        # Velocidades
        self.move_dimension = move_dimension
        self.move_positive = True#bool(random.getrandbits(1))
        #self.speed = int( (size)*0.25 ) # Entero, funcional, pero demasiado rapido | 4
        #self.speed = int( (size)*0.125 ) # Entero, funcional, pero demasiado lento | 2

        # Decimal, funcinal pero en resoluciones inferiores a 960 irregular | 3
        # Por default; 4.5, no se redondea a 5, se rodondea a 4. 1.5 a 2.
        # Esto se debe a la Regla del redondeo. Se redondeara siempre al numero par mas cercano.
        self.speed = int( (size)*0.1875 )
        #if self.speed == 2:
        #    self.speed = 1

        #print(self.speed)
    
    def anim(self):
        # Si colisiona con algun objeto solido.
        #if pygame.sprite.spritecollide(self, solid_objects, False):
        for obj in self.__solid_objects:
            #collision = obj_collision_sides_solid(obj_main=self, obj_collide=obj)
            #if not collision == None:
            #    self.move_positive = bool(random.getrandbits(1))
            if self.rect.colliderect(obj.rect):
                if self.rect.x > obj.rect.x: #- (self.speed/8):
                    self.move_positive = True
                elif self.rect.x < obj.rect.x: #+ (self.speed/8):
                    self.move_positive = False
                    
                if self.rect.y > obj.rect.y: #- (self.speed/8):
                    self.move_positive = True
                elif self.rect.y < obj.rect.y: #+ (self.speed/8):
                    self.move_positive = False
    
        # Moverse positivo o negativamente
        if self.move_dimension == 1:
            if self.move_positive == True:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
        elif self.move_dimension == 2:
            if self.move_positive == True:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
                
        # Sprite
        self.sprite.rect.x = self.rect.x
        self.sprite.rect.y = self.rect.y