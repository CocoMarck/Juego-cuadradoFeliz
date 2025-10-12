from .general_use.sprite_pasted_rect import SpritePastedRect, StandardSprite

import pygame, random
from core.pygame.cf_util import get_image

from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)


class Gun( StandardSprite ):
    def __init__(
     self, size=pixel_space_to_scale,
     position=[pixel_space_to_scale,pixel_space_to_scale], transparency_collide=255,
     transparency_sprite=255, layer_all_sprites=None, update_objects=None, gun_objects=None
    ):
        # Iniciar
        surf=pygame.Surface( [size,size], pygame.SRCALPHA )
        super().__init__(
         surf, transparency_collide, position=position
        )

        # Sprite arma
        self.sprite = SpritePastedRect(
         get_image("gun", size=[size,size] ),
         self.rect, difference_xy=[0,0]
        )

        # Rotación y lado de sprite
        if random.choice( [False, True] ):
            self.rotation_increment = 1
        else:
            self.rotation_increment = -1

        self.sprite.flip_x = random.choice( [False, True] )


        # Grupos
        self.__layer_all_sprites = layer_all_sprites
        self.__update_objects = update_objects
        self.__gun_objects = gun_objects

        # Agragar a Grupos
        self.__layer_all_sprites.add( self, layer=3 )
        self.__layer_all_sprites.add( self.sprite, layer=2 )

        self.__update_objects.add(self)
        self.__gun_objects.add(self)

    def update(self):
        self.sprite.angle += self.rotation_increment
        self.sprite.rotate()
        self.sprite.update()
