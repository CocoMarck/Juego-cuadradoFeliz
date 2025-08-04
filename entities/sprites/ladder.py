# General
from core.pygame.pygame_util import generic_colors

import pygame, sys, os, random
from pygame.locals import *

# CF
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import *
from .general_use.multi_layer_sprite import MultiLayerSprite
from .cf_sounds import *



class Ladder( MultiLayerSprite ):
    def __init__(self, size=pixel_space_to_scale, position=[0,0],
        transparency_collide=255, transparency_sprite=255, 
        ladder_objects:object=None, layer_all_sprites:object=None
    ):
        size_collide = round(size*0.75)
        size_difference = size -size_collide 
        super().__init__(
         surf=pygame.Surface( (size_collide, size_collide), pygame.SRCALPHA ), 
         transparency=transparency_collide, position=position, 
         layer=[get_image('ladder', size=[size, size], transparency=transparency_sprite)], 
         layer_transparency=transparency_sprite, layer_difference_xy=[0,0]
        )
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider y surface
        self.surf.fill( (113,77,41, self.transparency_collide) )
        self.rect.x += (size_difference/2)
        self.rect.y += (size_difference/2)
        layer_all_sprites.add(self, layer=2)
        ladder_objects.add(self)
        
        # Sprite
        sprite = self.sprite_layer.layer[0]
        self.sprite_layer.update_layer()
        layer_all_sprites.add(sprite, layer=1)