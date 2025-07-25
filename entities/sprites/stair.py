import pygame
from core.pygame.cf_util import get_image
from controllers.cf_info import pixel_space_to_scale
from .floor import Floor



class Stair(pygame.sprite.Sprite):
    def __init__( 
        self, size=pixel_space_to_scale, position=[0, 0], 
        transparency_collide=255, transparency_sprite=255, invert=False, climate=None, 
        solid_objects:object=None, update_objects:object=None, layer_all_sprites:object=None
    ):
        super().__init__()
        
        self.__update_objects = update_objects
        self.__solid_objects = solid_objects
        self.__layer_all_sprites = layer_all_sprites
        
        # transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite


        # Tamaños y parametros de floor/partes de escalera
        size_part = size//2
        self.climate = climate
        
        # Para posicionar correctamente
        if invert == True:
            more_pixels1 = 0
            more_pixels2 = size_part
            more_pixels3 = -(size)
        else:
            more_pixels1 = size_part
            more_pixels2 = size_part
            more_pixels3 = size        

        # Colliders | Partes de escalera | objetos
        self.stair_part( 
            size=size_part, 
            position=[position[0]+more_pixels1, position[1]]
        )
        self.stair_part( 
            size=size_part, 
            position=[position[0], position[1]+more_pixels2]
        )
        self.stair_part( 
            size=size_part, 
            position=[position[0]+more_pixels2, position[1]+more_pixels2]
        )
        
        self.stair_part( # Parte necesaria para evitar bugs
            size=size, 
            position=(position[0]+more_pixels3, position[1])
        )
        
    def stair_part(self, size=4, position=(0,0) ):
        stair_part = Floor( 
            size=[size, size], position=position, 
            transparency_collide=self.transparency_collide, transparency_sprite=self.transparency_sprite, 
            limit=False, climate=self.climate, solid_objects=self.__solid_objects, 
            update_objects=self.__update_objects, layer_all_sprites=self.__layer_all_sprites
        )