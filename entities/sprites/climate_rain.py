import pygame
from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import *
from .cf_sounds import *

# CF
from controllers.cf_info import (
    pixel_space_to_scale
)
from .general_use.multi_layer_sprite import MultiLayerSprite
from .destructible_sprite import DestructibleSprite




class ClimateRain( MultiLayerSprite ):
    def __init__(
     self, size=pixel_space_to_scale, position=(scale_surface_size[0]//2, scale_surface_size[1]//2),
     transparency_collide=255, transparency_sprite=255, damage=False, climate_objects=None, 
     damage_objects=None, player_objects=None, solid_objects=None, 
     layer_all_sprites=None
    ):    
        # Variables necesarias
        color_sprite = [0,0,127]
        surf_color = generic_colors('sky_blue')
        self.acid_rain = damage
        if damage == True: 
            surf_color = generic_colors('red')
            color_sprite = [0,255,0]
        self.size = [size, size]
            
        self.__image = get_image( 'rain', size=[size,size], color=color_sprite )
        self.size_difference = size*0.375

        # Inicializar todo
        super().__init__(
         surf=pygame.Surface( (size//4, size//4), pygame.SRCALPHA ),
         transparency=transparency_collide, position=position, 
         layer=[ self.__image[0] ], 
         layer_transparency=transparency_sprite, 
         layer_difference_xy=[self.size_difference,-self.size_difference]
        )

        self.damage = 2
        
        # grupos
        self.__climate_objects = climate_objects
        self.__layer_all_sprites=layer_all_sprites
        self.__player_objects = player_objects
        self.__solid_objects = solid_objects
        
        # Valores de movimiento Velocidad
        self.speed_y = random.choice(
         [  size//2, ( (size//2) -(size//16) ), ( (size//2) -(size//8) ) ]
        )
        self.speed_x = self.speed_y//2
        self.move = True
        self.not_move = False
        self.spawn_xy = [self.rect.x, self.rect.y]

        # Color collider
        self.surf.fill( surf_color )
        self.set_transparency()

        # Establecer sprite y posicion actual
        self.sprite = self.sprite_layer.layer[0]
        
        # Tiempo de sprite de gota que colisiona
        self.fps = data_CF.fps//4
        self.fps_count = 0
        self.sprite_collide = None
        self.time_respawn = 0 # Esta variable se usa en el loop del juego
        
        # Agregar a grupo de sprites
        layer_all_sprites.add(self, layer=1)
        climate_objects.add(self)
        if damage == True:
            damage_objects.add(self)
        layer_all_sprites.add(self.sprite, layer=3)

        #
        self.identifer = "rain"


    def respawn(self):
        current_position = self.rect.topleft
        better_position = [ current_position[0], current_position[1]-self.size[1] ]
        particle = DestructibleSprite(
         size=self.size, sprite=self.__image[1],
         time=self.fps, position=better_position, collider_color=(0,255,0),
         collider_transparency=self.transparency,
         sprite_transparency=self.sprite_layer.transparency_layer,
         update_objects=self.__climate_objects, layer_all_sprites=self.__layer_all_sprites
        )
        self.rect.topleft = self.position
        
    def update(self):
        # Mover al jugador si el collider esta en false
        if (
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
         disp_width=scale_surface_size[0], disp_height=scale_surface_size[1], obj=self, 
         difference=(self.size*32)
        )
        if transfer_disp == 'height_positive':
            self.collide = True
        elif transfer_disp == 'width_positive' or transfer_disp == 'width_negative':
            self.not_move = True
        '''

        # Eventos | Si toca objetos solidos
        for solid_object in self.__solid_objects:
            if self.rect.colliderect(solid_object.rect):
                self.respawn()

        if self.acid_rain == False:
            # Eventos | Si colisiona con el player
            for player in self.__player_objects:
                if self.rect.colliderect(player.rect):
                    self.respawn()
        
        # Sección para mover sprite correctamente
        self.sprite.update()
