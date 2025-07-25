# General
from core.pygame.pygame_util import generic_colors

import pygame, sys, os, random
from pygame.locals import *

# CF
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import *
from .cf_sounds import *



class Ladder(pygame.sprite.Sprite):
    def __init__(self, size=pixel_space_to_scale, position=[0,0],
        transparency_collide=255, transparency_sprite=255, 
        ladder_objects:object=None, layer_all_sprites:object=None
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider y surface
        size_collide = round(size*0.75)
        self.surf = pygame.Surface( (size_collide, size_collide), pygame.SRCALPHA )
        self.surf.fill( (113,77,41, self.transparency_collide) )
        self.rect = self.surf.get_rect( 
            topleft=( position[0]+size_collide*0.25, position[1]+size_collide*0.25 ) 
        )
        layer_all_sprites.add(self, layer=2)
        ladder_objects.add(self)
        
        # Sprite
        sprite = pygame.sprite.Sprite()
        sprite.surf = get_image('ladder', size=[size, size], transparency=self.transparency_sprite)
        sprite.rect = sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add(sprite, layer=1)