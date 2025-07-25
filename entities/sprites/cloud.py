import pygame, random
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import get_image

class Cloud(pygame.sprite.Sprite):
    def __init__(
        self, size = (pixel_space_to_scale*4, pixel_space_to_scale*2),  position=(0,0),
        transparency_collide=255, transparency_sprite=255, 
        anim_sprites=None, nocamera_back_sprites=None
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide=transparency_collide
        self.transparency_sprite=transparency_sprite
        
        # Seccion de imagen
        image_set = random.choice( [1, 2, 3] )
        
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.surf.fill( (191,191,191, self.transparency_collide) )
        self.rect = self.surf.get_rect(topleft=position)
        
        nocamera_back_sprites.add(self)
        anim_sprites.add(self)
        
        # Sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = get_image(
            f'cloud-{image_set}', size=size, transparency=self.transparency_sprite, return_method='image'
        )
        self.sprite.rect = self.sprite.surf.get_rect( topleft=position )
        nocamera_back_sprites.add(self.sprite)
        
        # Sección de velocidad
        self.speed = random.choice( 
            [-pixel_space_to_scale//4, pixel_space_to_scale//4] 
        )
        self.fps = (data_CF.fps*1.5)//( random.choice( [2, 3, 4] ) )
        self.count_fps = 0
        
    def anim(self):
        self.count_fps += 1
        if self.count_fps == self.fps:
            self.rect.x += self.speed
            self.count_fps = 0

        # Eventos | Si traspasa la pantalla
        if self.rect.x > scale_surface_size[0]+self.rect.width:
            # Si coordenada x es mayor a pantalla mas ancho de nube.
            self.rect.x = -self.rect.width
        elif self.rect.x < -self.rect.width:
            # Si coordenada x es menor a menos ancho de nube.
            self.rect.x = scale_surface_size[0]
        
        self.sprite.rect.x = self.rect.x
        self.sprite.rect.y = self.rect.y
