# General
import math
from core.pygame.pygame_util import generic_colors, Anim_sprite

import pygame
from pygame.locals import *

# CF
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import get_image
from .cf_sounds import *




class PointedStar(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0], transparency_collide=255, transparency_sprite=255,
        moving=False, instakill=False, damage_objects=None, anim_sprites=None, layer_all_sprites=None
    ):
        super().__init__()
        
        # Sprites
        self.__damage_objects=damage_objects
        self.__anim_sprites=anim_sprites
        self.__layer_all_sprites=layer_all_sprites
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Movimiento variables
        self.moving = moving
        self.instakill = instakill
        self.count_moving = 0
        self.moving_pixels = size*4
        self.moving_speed = size//4
        
        # Collider principal
        self.surf = pygame.Surface( ( size/2, size/2 ), pygame.SRCALPHA )
        self.surf.fill( generic_colors('green', self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.x += (size -self.rect.width)//2
        self.rect.y += (size -self.rect.height)//2
        
        layer_all_sprites.add(self, layer=2)
        anim_sprites.add(self)
        
        # Sprite
        self.__size = size
        if self.instakill == True:
            color = [95, 0, 0]
        else:
            color = [0, 0, 127]

        self.sprite = Anim_sprite(
            sprite_sheet=get_image(
                'star-pointed', size=[self.__size*7, self.__size], return_method='image', color=color,
                transparency=self.transparency_sprite
            )
        )
        self.sprite.rect.topleft = (
            self.rect.x-(self.__size//4),
            self.rect.y-(self.__size//4)
        )
        layer_all_sprites.add(self.sprite, layer=1)
        
        # Cuadrados dañinos
        size_square = self.rect.width/2
        
        self.square_x1 = self.square_damage(
            size=size_square, position=(self.rect.x, self.rect.y +(size_square//2) ),
            color=generic_colors('black', self.transparency_collide)
        )
        self.square_x2 = self.square_damage(
            size=size_square, position=(
                self.rect.x-size_square, self.rect.y +(size_square//2) 
            ),
            color=generic_colors('red', self.transparency_collide)
        )
        self.square_x3 = self.square_damage(
            size=size_square, position=(self.rect.x+size_square, self.rect.y +(size_square//2) ),
            color=generic_colors('grey', self.transparency_collide)
        )
        self.square_x4 = self.square_damage(
            size=size_square, position=(self.rect.x+(size_square*2), self.rect.y +(size_square//2) ),
            color=generic_colors('blue', self.transparency_collide)
        )
        
        # Animacion Variables
        self.__size_square = size_square
        self.__move = 0
        self.__size_square_percentage_50 = self.__size_square//2
        self.__size_square_percentage_150 = self.__size_square*1.5
        self.__size_square_percentage_300 = self.__size_square*3

    def square_damage(self, size=4, position=(0,0), color=generic_colors('green')):
        # Cuadrado de daño
        # Daño
        square = pygame.sprite.Sprite()
        square.surf = pygame.Surface( (size, size), pygame.SRCALPHA )
        square.surf.fill( color )
        square.rect = square.surf.get_rect( topleft=position)
        self.__layer_all_sprites.add(square, layer=2)
        if self.instakill == True:
            square.damage = 0
        else:
            square.damage = 10
        self.__damage_objects.add(square)
        return square
    
    def anim(self):
        # Animación del sprite
        self.sprite.anim()
        
        # Movimiento estandar del collider
        if self.__move == 0:
            self.__move = 0.1

        elif self.__move == 0.1:
            self.square_x2.rect.y -= self.__size_square_percentage_150
            self.square_x1.rect.y -= self.__size_square_percentage_50
            
            self.square_x4.rect.y += self.__size_square_percentage_150
            self.square_x3.rect.y += self.__size_square_percentage_50
            self.__move = 0.2

        elif self.__move == 0.2:
            self.square_x2.rect.x += self.__size_square_percentage_150
            self.square_x1.rect.x += self.__size_square_percentage_50
        
            self.square_x4.rect.x -= self.__size_square_percentage_150
            self.square_x3.rect.x -= self.__size_square_percentage_50
            self.__move = 0.3

        elif self.__move == 0.3:
            self.square_x2.rect.x += self.__size_square_percentage_150
            self.square_x1.rect.x += self.__size_square_percentage_50
        
            self.square_x4.rect.x -= self.__size_square_percentage_150
            self.square_x3.rect.x -= self.__size_square_percentage_50
            self.__move = 0.4

        elif self.__move == 0.4:
            self.square_x2.rect.y += self.__size_square_percentage_150
            self.square_x1.rect.y += self.__size_square_percentage_50
            self.square_x2.rect.x -= self.__size_square_percentage_300
            self.square_x1.rect.x -= self.__size_square
            
            self.square_x4.rect.y -= self.__size_square_percentage_150
            self.square_x3.rect.y -= self.__size_square_percentage_50
            self.square_x4.rect.x += self.__size_square_percentage_300
            self.square_x3.rect.x += self.__size_square
            self.__move = 0.1

        
        # Si la estrella se va a mover
        if self.moving == True:
            if self.count_moving < self.moving_pixels:
                self.count_moving += self.moving_speed
                self.rect.x += self.moving_speed

                self.square_x1.rect.x += self.moving_speed
                self.square_x2.rect.x += self.moving_speed
                self.square_x3.rect.x += self.moving_speed
                self.square_x4.rect.x += self.moving_speed

                self.sprite.rect.x += self.moving_speed
            elif self.count_moving >= self.moving_pixels:
                if self.count_moving < self.moving_pixels*1.5:
                    self.count_moving += self.moving_speed
                    self.rect.y -= self.moving_speed

                    self.square_x1.rect.y -= self.moving_speed
                    self.square_x2.rect.y -= self.moving_speed
                    self.square_x3.rect.y -= self.moving_speed
                    self.square_x4.rect.y -= self.moving_speed

                    self.sprite.rect.y -= self.moving_speed
                elif self.count_moving >= self.moving_pixels*1.5:
                    if self.count_moving < self.moving_pixels*2.5:
                        self.count_moving += self.moving_speed
                        self.rect.x -= self.moving_speed

                        self.square_x1.rect.x -= self.moving_speed
                        self.square_x2.rect.x -= self.moving_speed
                        self.square_x3.rect.x -= self.moving_speed
                        self.square_x4.rect.x -= self.moving_speed

                        self.sprite.rect.x -= self.moving_speed

                    elif self.count_moving >= self.moving_pixels*2.5:
                        if self.count_moving < self.moving_pixels*3:
                            self.count_moving += self.moving_speed
                            self.rect.y += self.moving_speed

                            self.square_x1.rect.y += self.moving_speed
                            self.square_x2.rect.y += self.moving_speed
                            self.square_x3.rect.y += self.moving_speed
                            self.square_x4.rect.y += self.moving_speed

                            self.sprite.rect.y += self.moving_speed
                        elif self.count_moving == self.moving_pixels*3:
                            self.count_moving = 0
