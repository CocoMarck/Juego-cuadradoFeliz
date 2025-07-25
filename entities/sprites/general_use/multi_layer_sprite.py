import pygame, sys, os, random
from pygame.locals import *

from .standard_sprite import StandardSprite
from .sprite_layer_pasted_rect import SpriteLayerPastedRect




class MultiLayerSprite( StandardSprite ):
    '''
    Un sprite, que tiene otros muchos sprites que estan pegados a este sprite
    Su función es tener entre una capa/layer a muchos capas/layers de sprites.
    '''
    def __init__(
        self, surf, transparency=255, position=[0,0], 
        layer=[], layer_transparency=255, layer_difference_xy=[0,0]
    ):
        super().__init__(
            surf=surf, transparency=transparency, position=position
        )
        
        # Agregar layers            
        self.sprite_layer = SpriteLayerPastedRect(
            rect_pasted=self.rect, transparency=layer_transparency, difference_xy=layer_difference_xy, 
            layer=layer
        )
