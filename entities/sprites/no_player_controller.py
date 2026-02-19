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
import random



class NoPlayerController(Character):
    def __init__(
     self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255,
     dict_sprite={
        'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
        'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
     }, position=[0,0], limit_xy=[0,0], color_sprite=[200,200,200],
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
         sprite_difference_xy=sprite_difference_xy, solid_objects=solid_objects, damage_objects=damage_objects,
         level_objects=level_objects, score_objects=score_objects, jumping_objects=jumping_objects,
         moving_objects=moving_objects, ladder_objects=ladder_objects, particle_objects=particle_objects,
         anim_sprites=anim_sprites, update_objects=update_objects, gun_objects=gun_objects, player_objects=player_objects, layer_all_sprites=layer_all_sprites
        )
        #self.transparency=0

        self.init_wait = 10
        self.init_count = 0
        self.variation_xy = [None,None]
        self.variation_count = 0
        self.variation_time = air_count_based_on_resolution*2.5 #10

        self.time_to_jump = air_count_based_on_resolution*0.75 # 3

        # Dirección a moverse, no moverse
        self.direction_xy = [ False, False ]
        self.not_move = False

        # Tiempo esparar y cambiar de dirección
        self.time_change_direction = 10
        self.count_change_direction = 0
        self.bool_direction = False

        # Tiempos para no movimierse
        self.times_not_move = [data_CF.fps*2, data_CF.fps*1, data_CF.fps*0.5, data_CF.fps*0.25]
        self.count_not_move = 0

        # Tiempos para caminar aleatoriamente
        self.times_for_walk = [data_CF.fps*20, data_CF.fps*10, data_CF.fps*5]
        self.count_for_walk = 0

        self.times_walking = [data_CF.fps*10, data_CF.fps*5, data_CF.fps*2]
        self.count_walking = 0

        # Activar inteligencia artificial
        self.ai = True

        #self.sprite_layer.layer[0].center_difference_xy = [0, -(self.rect.height//2)]
        respawn_objects.add(self)

        # Daño
        self.identifer = "npc"

        # Timer | Pararse a mirar a la nada
        self.random_stop_times = [data_CF.fps*2, data_CF.fps*4, data_CF.fps*8]
        self.random_stop_time = self.random_stop_times[0]
        self.random_stop_count = 0

        # Iniciar variables
        self.init_ai()

    def init_ai(self):
        self.direction_xy = [ random.choice( [False, True] ), False ]
        self.not_move = random.choice( [False, True] )
        self.random_stop_time = random.choice( self.random_stop_times )

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
        # Al morir inicializar todo
        if self.dead:
            self.init_ai()

        # No mover al resivir daño
        if self.damage_effect:
            self.not_move = True
        if self.not_move:
            self.count_not_move += 1
            if self.count_not_move >= random.choice( self.times_not_move ):
                self.not_move = False
        else:
            self.count_not_move = 0

        # Caminar
        self.count_for_walk += 1
        if self.count_for_walk >= random.choice( self.times_for_walk ):
            self.count_walking += 1
            if self.count_walking >= random.choice( self.times_walking ):
                self.walk = False
                self.count_for_walk = 0
                self.count_walking = 0
            else:
                self.walk = True

        # Movimiento de ai
        if self.ai:
            # Paradas random automaticas
            if self.fall == False:
                self.random_stop_count += 1
            if self.random_stop_count == self.random_stop_time:
                self.random_stop_time = random.choice( self.random_stop_times )
                self.random_stop_count = 0
                self.not_move = True

            # Lo demas
            if self.init_count < self.init_wait:
                self.init_count += 1
            if self.init_count >= self.init_wait:
                self.set_direction( )

                # Nomas detectar caida.
                if self.air_count > self.time_to_jump:
                    # Nomas detectar caida, forzar correr y salto.
                    self.set_and_jump(1)

                    #self.right = False
                    #self.left = True
                    self.walk = False
                else:
                    self.jump = False
                    #self.right = True
                    #self.left = False
                    #self.walk = False

                if self.bool_direction == True:
                    if self.count_change_direction == 0:
                        #print('Cambiando')
                        self.change_direction()

                    self.count_change_direction += 1
                    if self.count_change_direction >= self.time_change_direction:
                        #print('listo')
                        self.bool_direction = False
                        self.count_change_direction = 0


                if self.rect.x == self.variation_xy[0]:
                    self.bool_direction = True
                    #self.jump = True

            self.variation_count += 1
            if self.variation_count >= self.variation_time:
                self.variation_xy = [self.rect.x,self.rect.y]
                self.variation_count = 0
