# General
from core.pygame.pygame_util import generic_colors

import pygame
from pygame.locals import *

# CF
from controllers.cf_info import (
    pixel_space_to_scale, data_CF
)
from core.pygame.cf_util import get_image
from .no_player_controller import NoPlayerController
from .character import air_count_based_on_resolution
import random



class Enemy(NoPlayerController):
    def __init__(
     self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255, 
     dict_sprite={
        'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
        'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
     }, position=[0,0], limit_xy=[0,0], color_sprite=[255,127,127],
     sprite_difference_xy=[0,-(pixel_space_to_scale//2)],
     solid_objects=None, damage_objects=None, level_objects=None, score_objects=None, jumping_objects=None,
     moving_objects=None, ladder_objects=None, particle_objects=None, anim_sprites=None,
     update_objects=None, gun_objects=None, player_objects=None, layer_all_sprites=None,
     respawn_objects=None
    ):
        
        super().__init__( 
         size=size, 
         transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
         dict_sprite=dict_sprite, position=position, limit_xy=limit_xy, color_sprite=color_sprite,
         sprite_difference_xy=sprite_difference_xy, solid_objects=solid_objects,
         damage_objects=damage_objects, level_objects=level_objects, score_objects=score_objects,
         jumping_objects=jumping_objects, moving_objects=moving_objects,
         ladder_objects=ladder_objects, particle_objects=particle_objects, anim_sprites=anim_sprites,
         update_objects=update_objects, gun_objects=gun_objects, respawn_objects=respawn_objects,
         player_objects=player_objects, layer_all_sprites=layer_all_sprites

        )
        #self.transparency=0

        # Daño
        self.identifer = "enemy"
        self.damage = int(25)
        self.damage_activated = True
        damage_objects.add(self)
