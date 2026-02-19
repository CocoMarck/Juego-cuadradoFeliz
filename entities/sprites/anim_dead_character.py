# General
from core.pygame.pygame_util import (
    Split_sprite
)
import pygame
from pygame.locals import *

# CF
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import get_image

# Objetos
from .particle import Particle



class AnimDeadCharacter(pygame.sprite.Sprite):
    def __init__(
        self, position=[0,0], fps=data_CF.fps*3,
        transparency_collide=255, transparency_sprite=255, color_sprite=(153,252,152),
        particle_objects:object=None, solid_objects=None, damage_objects=None, jumping_objects=None, 
        anim_sprites:object=None, layer_all_sprites:object=None
    ):
        super().__init__()

        # Transparencia        
        self.transparency_collide=transparency_collide
        self.transparency_sprite=transparency_sprite

        # Principal
        self.size = pixel_space_to_scale
        self.surf = pygame.Surface( (self.size, self.size), pygame.SRCALPHA )
        self.rect = self.surf.get_rect( topleft=position )
    
        self.fps = fps
        self.__count = 0
        self.anim_fin = False
        anim_sprites.add( self )
        layer_all_sprites.add(self, layer=2)
        
        # Partes
        size_parts = self.size//2
        img = get_image( 
            'player_not-move', number=0, size=[pixel_space_to_scale*2, pixel_space_to_scale*2],
            colored_method='surface', color=color_sprite
        )
        img = Split_sprite(sprite_sheet=img, parts=8)
        self.part1 = Particle( 
         size=[size_parts, size_parts], position=[ self.rect.x, self.rect.y+size_parts ],
         image=img[13], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
         time_kill=self.fps, sound='player',
         particle_objects=particle_objects, solid_objects=solid_objects, damage_objects=damage_objects, 
         jumping_objects=jumping_objects, anim_sprites=anim_sprites, layer_all_sprites=layer_all_sprites
        )
        
        self.part2 = Particle( 
         size=[size_parts, size_parts], position=[self.rect.x+size_parts, self.rect.y+size_parts ],
         image=img[14], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
         time_kill=self.fps, sound='player',
         particle_objects=particle_objects, solid_objects=solid_objects, damage_objects=damage_objects, 
         jumping_objects=jumping_objects, anim_sprites=anim_sprites, layer_all_sprites=layer_all_sprites
        )
        
        self.part3 = Particle( 
         size=[size_parts, size_parts], position=[self.rect.x, self.rect.y],
         image=img[9], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
         time_kill=self.fps, sound='player',
         particle_objects=particle_objects, solid_objects=solid_objects, damage_objects=damage_objects, 
         jumping_objects=jumping_objects, anim_sprites=anim_sprites, layer_all_sprites=layer_all_sprites
        )

        self.part4 = Particle( 
         size=[size_parts, size_parts], position=[self.rect.x+size_parts, self.rect.y],
         image=img[10], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
         time_kill=self.fps, sound='player',
         particle_objects=particle_objects, solid_objects=solid_objects, damage_objects=damage_objects, 
         jumping_objects=jumping_objects, anim_sprites=anim_sprites, layer_all_sprites=layer_all_sprites
        )
    
    def anim(self):
        # Contador 
        self.__count += 1
        if self.__count*5 <= 128:
            self.surf.fill( ( 255-(self.__count*5), 0, 0, self.transparency_collide)  )

        if self.__count == self.fps:
            # Animacion terminada, todos los objetos se eliminaran
            self.anim_fin = True
            self.kill()
