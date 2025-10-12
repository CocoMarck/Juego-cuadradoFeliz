# General
from core.pygame.pygame_util import generic_colors

import pygame, random
from pygame.locals import *

# CF
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import get_sound, collide_and_move
from .cf_sounds import *

air_count_based_on_resolution = 5


class Particle(pygame.sprite.Sprite):
    def __init__(
        self, size=[pixel_space_to_scale//2, pixel_space_to_scale//2], position=[0,0],
        color_collide=generic_colors('green'), color_sprite=None,
        transparency_sprite=255, transparency_collide=255,
        time_kill=0, image=None, sound=None, 
        particle_objects:object=None, solid_objects=None, damage_objects=None, jumping_objects=None, 
        anim_sprites:object=None, layer_all_sprites:object=None
    ):
        super().__init__()
        
        self.__particle_objects = particle_objects
        self.__solid_objects = solid_objects
        self.__jumping_objects = jumping_objects
        self.__damage_objects = damage_objects
        
        # 
        self.sounds_str = None
        if sound == 'player':
            self.sounds_str = ['steps', 'hits']
            
        
        # Transparencia de collider y imagen
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.surf.fill( color_collide )
        self.surf.set_alpha( self.transparency_collide )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=2)
        anim_sprites.add(self)
        particle_objects.add(self)
        
        # Imagen
        if type(image) == pygame.Surface:
            rect = image.get_rect()
            if rect.x != self.rect.x or rect.y != self.rect.y:
                image = pygame.transform.scale(image, size)
                
            self.image = pygame.sprite.Sprite()
            self.image.surf = image
            self.image.surf.set_alpha( self.transparency_sprite )
            self.image.rect = self.image.surf.get_rect( topleft=position )
            layer_all_sprites.add(self.image, leyer=1)
        else: self.image = None
        
        # Movimiento
        self.moving_xy = [0,0]
        
        self.gravity_power = random.choice( [size[0]*0.025, size[0]*0.05] )
        self.gravity_limit = size[0]*0.75
        self.gravity_current = -self.gravity_power # Para que inicie callendo
        self.air_count = 8 # 8 Para que inicie en caida
        self.gravity = True
        
        self.move_positive_x = random.choice( [False,True] )
        self.speed = random.randint( size[0]//4, size[0]//2 )

        self.jumping = random.choice( [False, True] )
        self.jump_power = random.choice( [size[0]*0.125, size[0]*0.25, size[0]*0.4] )
        
        # Tiempo para eliminar la particula
        self.time_kill = time_kill
        self.time_kill_count = 0
    
    def anim(self):
        # Movimiento en x
        if self.move_positive_x == True:    self.moving_xy[0] = self.speed
        else:                               self.moving_xy[0] = -self.speed
    
        # Detectar si esta callendo o no
        if self.air_count <= air_count_based_on_resolution: fall = False
        else:                                               fall = True
        
        # Salto
        if fall == False:
            self.gravity_current = -self.jump_power
        if self.jumping == True:
            self.jumping = False
            self.gravity_current = -self.jump_power
        
        # Gravedad
        if self.gravity == True:
            self.moving_xy[1] = self.gravity_current
            if self.gravity_current < self.gravity_limit:   self.gravity_current += self.gravity_power
            else:                                           self.gravity_current = self.gravity_limit
        
        
        # Colision objetos dañinos
        damage_effect=False
        for obj in self.__damage_objects:
            if self.rect.colliderect(obj.rect):
                damage_effect=True

            if hasattr(obj, "dead"):
                if obj.dead:
                    damage_effect = False

        if damage_effect == True:
            self.moving_xy[0] += self.rect.width * random.choice([1,-1])
            self.moving_xy[1] += self.rect.height * random.choice([1,-1])
        
        # Mover y colisionar Solidos
        collide_objects = []
        for obj in self.__solid_objects: collide_objects.append(obj)
        for obj in self.__particle_objects: 
            if not obj == self: 
                collide_objects.append(obj)
        for obj in self.__jumping_objects: collide_objects.append(obj)
        collided_side = collide_and_move( 
            obj=self, obj_movement=self.moving_xy, solid_objects=collide_objects
        )
        self.air_count += 1
        if collided_side == 'bottom':
            self.gravity_current = 0
            self.air_count = 0
        elif collided_side == 'top': self.gravity_current = 0
        elif collided_side == 'right': self.move_positive_x = False
        elif collided_side == 'left': self.move_positive_x = True
        
        
        
        # Posicionear imagen
        if not self.image == None:
            self.image.rect.x = self.rect.x
            self.image.rect.y = self.rect.y
        
        
        # Sonido
        if isinstance(self.sounds_str, list):
            if damage_effect == True:
                get_sound(sound=self.sounds_str[1], volume=self.volume).play()
            if isinstance(collided_side, str):
                get_sound(sound=self.sounds_str[0], volume=self.volume).play()


        # Tiempo de vida
        if self.time_kill > 0:
            self.time_kill_count += 1
            if self.time_kill_count == self.time_kill:
                if not self.image == None: self.image.kill()
                self.kill()
