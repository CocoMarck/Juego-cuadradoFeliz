# General
from core.pygame.pygame_util import generic_colors

import pygame
from pygame.locals import *

# CF
from controllers.cf_info import pixel_space_to_scale
from core.pygame.cf_util import get_image
from .general_use.multi_layer_sprite import MultiLayerSprite
from .floor import Floor




class Spike( MultiLayerSprite ):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0], transparency_collide=255, transparency_sprite=255,
        moving=False, instakill=False, damage_objects:object=None, anim_sprites=None, solid_objects=None, 
        update_objects=None, layer_all_sprites:object=None
    ):  
        # Establecer color y daño
        color = (0, 0, 71)
        damage = 20
        if instakill == True:
            color = (71, 0, 0)
            damage = 0
        
        # Inicializar SpriteMultiLayer
        super().__init__( 
            surf=pygame.Surface( (size/4, size/2), pygame.SRCALPHA ), transparency=transparency_collide,
            position=position, layer=[ 
                get_image(
                    'spike', colored_method='normal',  color=color, size=[size,size]
                )
            ],
            layer_transparency=transparency_sprite, layer_difference_xy=[0,size*0.25]
        )

        self.__color = color
        self.damage = damage

        
        # Añadir a los grupos de sprites
        # Daño
        if moving == True:
            anim_sprites.add(self)

        
        # Collider
        self.surf.fill( generic_colors(color='red') )
        self.set_transparency()
        self.rect.x += (size-self.rect.width)//2
        damage_objects.add(self)
        layer_all_sprites.add(self, layer=3)
        
        # Sprite
        self.sprite_layer.set_transparency_layer()
        self.sprite_layer.update_layer() # Establecer posición
        self.sprite_layer.add_to_layer_group( layer_all_sprites, layer=1 )
        
        # Cuadrados solidos
        square_size = self.rect.height
        floor_x = Floor(
         size = ( square_size, square_size ), position = [position[0], position[1]+square_size],
         transparency_collide=transparency_collide, transparency_sprite=0, limit = False, 
         solid_objects=solid_objects, update_objects=update_objects, layer_all_sprites=layer_all_sprites
        )
        
        floor_y = Floor(
         size = ( square_size, square_size ), position = [position[0]+square_size, position[1]+square_size],
         transparency_collide=transparency_collide, transparency_sprite=0, limit = False,
         solid_objects=solid_objects, update_objects=update_objects, layer_all_sprites=layer_all_sprites
        )
        
        # Mover o no sprite
        self.size = size
        self.size_y = size
        self.moving = moving
        self.__move_count = 0
        self.__move_pixels = size*4
        self.__move_speed = size//2
        self.__move_type = 'UP'
    
    def anim(self):
        # Solo se activa esta función si se mueve el picote
        if self.moving == True:
            if self.__move_type == 'UP':
                self.__move_count += self.__move_speed                
                self.size_y += self.__move_speed

                self.surf = pygame.Surface( (self.rect.width, self.size_y), pygame.SRCALPHA )
                self.surf.fill( generic_colors(color='red', transparency=self.transparency) )
                position = (self.rect.x, self.rect.y)
                self.rect = self.surf.get_rect( topleft=position )
                self.rect.y -= self.__move_speed
                
                if not self.sprite_layer.layer[0] == None:
                    self.sprite_layer.layer[0].surf = pygame.transform.scale(
                        self.sprite_layer.layer[0].surf_base, (self.size, (self.size_y))
                    )
                    self.sprite_layer.layer[0].rect.y -= self.__move_speed
                
                if self.__move_count >= self.__move_pixels:
                    self.__move_type = 'DOWN'

            elif self.__move_type == 'DOWN':
                self.__move_count -= self.__move_speed//2
                self.size_y -= self.__move_speed//2

                self.surf = pygame.Surface( (self.rect.width, self.size_y), pygame.SRCALPHA )
                self.surf.fill( generic_colors(color='red', transparency=self.transparency) )
                position = (self.rect.x, self.rect.y)
                self.rect = self.surf.get_rect( topleft=position )
                self.rect.y += self.__move_speed//2
                
                if not self.sprite_layer.layer[0] == None:
                    self.sprite_layer.layer[0].surf = pygame.transform.scale(
                        self.sprite_layer.layer[0].surf_base, (self.size, (self.size_y))
                    )
                    self.sprite_layer.layer[0].rect.y += self.__move_speed//2
                
                if self.__move_count <= 0:
                    self.__move_type = 'UP'
