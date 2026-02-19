# General
from core.pygame.pygame_util import generic_colors

import pygame
from pygame.locals import *

# CF
from controllers.cf_controller import dict_climate
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import *
from .cf_sounds import *
from .general_use.multi_layer_sprite import MultiLayerSprite



class Floor( MultiLayerSprite ):
    '''
    El piso del videojuego Cuadrado Feliz
    '''
    def __init__(
        self, size = [pixel_space_to_scale, pixel_space_to_scale], position = [0,0], 
        transparency_collide=255, transparency_sprite=255, color=None, limit=True, climate=None, 
        solid_objects=None, update_objects=None, layer_all_sprites=None
    ):
        
        # Establecer color
        '''
        random_more_color = random.choice( [8, 16, 32] )

        if climate == 'alien':
            color = [0,random_more_color,random_more_color]#'sky_blue'

        elif climate == 'sunny':
            color = [random_more_color,0,0]#'red'

        elif climate == 'rain':
            color = [0,0,random_more_color]#'blue'

        elif climate == 'black':
            color = [
                (random_more_color//2),
                random_more_color,
                0
            ]#'Verde amarillento'
        else:
        '''
        if climate in dict_climate.keys():
            invert_color = invert_rgb_color( dict_climate[climate] )
            multipler = random.choice( [0, 0.05, 0.2, 0.4] )
            color = []
            for x in invert_color:
                color.append( int(x*multipler) )
        else:
            color = None
        #color = None
        
        # Iniziar uso de SpriteMultiLayer
        super().__init__( 
            surf=pygame.Surface(size, pygame.SRCALPHA), transparency=transparency_collide, position=position,
            layer=[get_image( 'stone', size=size, color=color )], 
            layer_transparency=transparency_sprite, layer_difference_xy=[0,0]
        )
        
        # Cambiar color de collider
        #self.surf.fill( color )
        self.surf.fill( generic_colors('grey') )
        self.set_transparency()
        layer_all_sprites.add( self, layer=2 )
        solid_objects.add(self)
        
        # Agregar a grupos al Sprite
        self.sprite_layer.add_to_sprite_group( update_objects )
        self.sprite_layer.add_to_layer_group( layer_all_sprites, layer=1 )
        
        # Agregar o no limite
        self.limit_collision( limit )
    
    def limit_collision(self, limit=False):
        # Para agergar un objeto en medio del floor que mate por si traspasa el collider.
        pass
