# General
from core.pygame.pygame_util import generic_colors

import pygame
from pygame.locals import *

# CF
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import get_image
from .cf_sounds import *




class Trampoline(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0],
        transparency_collide=255, transparency_sprite=255,
        jumping_objects=None, layer_all_sprites=None
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collide
        self.surf = pygame.Surface( (size, size//8), pygame.SRCALPHA )
        self.surf.fill( generic_colors('sky_blue', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.y += self.rect.height//2
        
        layer_all_sprites.add(self, layer=2)
        jumping_objects.add(self)
        
        # Sprite
        sprite = pygame.sprite.Sprite()
        sprite.surf = get_image( 'trampoline', size=(size, size), transparency=self.transparency_sprite )
        sprite.rect = sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add( sprite, layer=1 )