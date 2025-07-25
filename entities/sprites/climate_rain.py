import pygame
from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import *
from .cf_sounds import *

# CF
from controllers.cf_info import (
    pixel_space_to_scale
)




class ClimateRain(pygame.sprite.Sprite):
    def __init__(
     self, size=pixel_space_to_scale, position=(scale_surface_size[0]//2, scale_surface_size[1]//2),
     transparency_collide=255, transparency_sprite=255, damage=False, climate_objects=None, 
     damage_objects=None, player_objects=None, solid_objects=None, 
     layer_all_sprites=None
    ):
        super().__init__()
        
        # grupos
        self.__layer_all_sprites=layer_all_sprites
        self.__player_objects = player_objects
        self.__solid_objects = solid_objects
        
        # Mostrar Collider o no
        self.transparency_sprite = transparency_sprite
        self.transparency_collide = transparency_collide
        
        # Sección de collider
        self.surf = pygame.Surface( (size//4, size//4), pygame.SRCALPHA )
        self.rect = self.surf.get_rect( topleft=position )
        self.speed_y = random.choice(
            [  
                size//2, 
                ( (size//2) -(size//16) ),
                ( (size//2) -(size//8) )
            ]
        )
        self.speed_x = self.speed_y//2
        self.move = True
        self.not_move = False
        self.spawn_xy = [self.rect.x, self.rect.y]
        
        layer_all_sprites.add(self, layer=1)
        climate_objects.add(self)
        # Establecer que es objeto dañino, con color y grupo de objetos
        if damage == True: 
            self.surf.fill( generic_colors('red', self.transparency_collide) )
            color_sprite = [0,255,0]
            self.damage = 1
            damage_objects.add(self)
        else: 
            self.surf.fill( generic_colors('sky_blue', self.transparency_collide) )
            self.damage = damage
            color_sprite = [0,0,127]
        
        # Sección de sprite
        self.fps = data_CF.fps//4
        self.fps_count = 0
        self.sprite_collide = None
        self.sprite = None
        self.size = size
        self.size_difference = (size//4)*3

        self.__image = get_image( 
            'rain', size=[size,size], color=color_sprite, transparency=self.transparency_sprite
        )
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = self.__image[0]
        self.sprite.rect = self.surf.get_rect( topleft=(self.rect.x,self.rect.y-self.size_difference) )
        layer_all_sprites.add(self.sprite, layer=3)
        
        # Tiempo
        self.time_respawn = 0 # Esta variable se usa en el loop del juego
        
    def update(self):            
        # Mover al jugador si el collider esta en false
        self.collide = False
        if (
            self.collide == False and 
            self.move == True and
            self.not_move == False
        ):
            self.rect.y += self.speed_y
            self.rect.x -= self.speed_x
        
        # Esta variable permite establecer si se quiere parar el movimiento de la lluvia o no.
        #self.not_move = False

        # Eventos | Si traspasa la pantalla
        '''
        transfer_disp = obj_not_see(
            disp_width=scale_surface_size[0], disp_height=scale_surface_size[1], obj=self, difference=(self.size*32)
        )
        if transfer_disp == 'height_positive':
            self.collide = True
        elif (
            transfer_disp == 'width_positive' or
            transfer_disp == 'width_negative'
        ):
            self.not_move = True
        '''

        # Eventos | Si toca objetos solidos
        for solid_object in self.__solid_objects:
            if self.rect.colliderect(solid_object.rect):
                self.collide = True
                self.time_respawn = 1

        # Eventos | Si colisiona con el player        
        for player in self.__player_objects:
            if self.rect.colliderect(player.rect):
                self.collide = True
                if self.damage == False: self.time_respawn = 1
        
        # Sección para mover sprite correctamente
        if not self.sprite == None:
            self.sprite.rect.topleft = (
                self.rect.x, self.rect.y-(self.size_difference)
            )
        
        # Sección para dibujar un sprite al colisionar con piso
        if self.collide == True:
            if self.sprite_collide == None and (not self.sprite == None):
                self.sprite_collide = pygame.sprite.Sprite()
                self.sprite_collide.surf = self.__image[1]
                self.sprite_collide.rect = self.sprite_collide.surf.get_rect()
                self.sprite_collide.rect.topleft = (
                    self.rect.x, self.rect.y-(self.size_difference)
                )
                self.__layer_all_sprites.add(self.sprite_collide, layer=3)
        else:
            if not self.sprite_collide == None:
                self.fps_count += 1
                if self.fps_count == self.fps:
                    self.sprite_collide.kill()
                    self.sprite_collide = None
                    self.fps_count = 0
