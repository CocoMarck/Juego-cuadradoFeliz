# General
from core.pygame.pygame_util import generic_colors

import pygame
from pygame.locals import *

# CF
from controllers.cf_info import (
    pixel_space_to_scale, data_CF
)
from core.pygame.cf_util import get_image
from .character import Character, air_count_based_on_resolution



class Enemy(Character):
    def __init__(
     self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255, 
     dict_sprite={
        'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
        'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
     }, position=[0,0], limit_xy=[0,0], color_sprite=[255,127,127], 
     sprite_difference_xy=[0,-(pixel_space_to_scale//2)],
     solid_objects=None, damage_objects=None, level_objects=None, score_objects=None, jumping_objects=None,
     moving_objects=None, ladder_objects=None, particle_objects=None, anim_sprites=None,
     update_objects=None, layer_all_sprites=None, respawn_objects=None
    ):
        
        super().__init__( 
         size=size, 
         transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
         dict_sprite=dict_sprite, position=position, limit_xy=limit_xy, color_sprite=color_sprite,
         sprite_difference_xy=sprite_difference_xy, solid_objects=solid_objects, damage_objects=damage_objects, 
         level_objects=level_objects, score_objects=score_objects, jumping_objects=jumping_objects,
         moving_objects=moving_objects, ladder_objects=ladder_objects, particle_objects=particle_objects,
         anim_sprites=anim_sprites, update_objects=update_objects, layer_all_sprites=layer_all_sprites
        )
        self.transparency=0

        self.init_wait = 10
        self.init_count = 0
        self.variation_xy = [None,None]
        self.variation_count = 0
        self.variation_time = air_count_based_on_resolution*2.5 #10
        
        self.time_change_direction = 8
        self.count_change_direction = 0
        self.direction_xy = [True, False]
        self.bool_direction = False
        self.ai = True
        self.time_not_move = data_CF.fps*0.5
        self.count_not_move = 0
        
        #self.sprite_layer.layer[0].center_difference_xy = [0, -(self.rect.height//2)]
        respawn_objects.add(self)
    
    def change_direction(self):
        if self.direction_xy[0] == True:
            self.direction_xy[0] = False
        else:
            self.direction_xy[0] = True
            
        if self.direction_xy[1] == True:
            self.direction_xy[1] = False
        else:
            self.direction_xy[1] = True
    
    def set_direction( self ):
        self.right = self.direction_xy[0] == True
        self.left = self.direction_xy[0] == False
        
        self.down = self.direction_xy[1] == True
        self.up = self.direction_xy[1] == False
    
    def move(self):
        # No mover al resivir daño
        if self.damage_effect:
            self.not_move = True
            self.count_not_move = 0
        if self.not_move:
            if self.count_not_move >= self.time_not_move:
                self.not_move = False
            self.count_not_move += 1

        # Movimiento de ai
        if self.ai:
            if self.init_count < self.init_wait:
                self.init_count += 1
            if self.init_count >= self.init_wait:
                self.set_direction( )
                self.walk = False
                
                # Nomas detectar caida.
                if self.air_count > air_count_based_on_resolution*0.625:
                    self.set_and_jump(1)
                    
                    #self.right = False
                    #self.left = True
                    #self.walk = True
                else:
                    self.jump = False
                    #self.right = True
                    #self.left = False
                    #self.walk = False
                
                if self.bool_direction == True:
                    if self.count_change_direction == 0:
                        self.change_direction()
                        print('Cambiando')
                    self.count_change_direction += 1
                    if self.count_change_direction >= self.time_change_direction:
                        self.bool_direction = False
                        self.count_change_direction = 0
                        print('listo')
                
                if self.rect.x == self.variation_xy[0]:
                    self.bool_direction = True
                    #self.jump = True
            
            self.variation_count += 1
            if self.variation_count >= self.variation_time:
                self.variation_xy = [self.rect.x,self.rect.y]
                self.variation_count = 0
