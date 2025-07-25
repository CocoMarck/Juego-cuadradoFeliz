import pygame
from core.pygame.pygame_util import generic_colors
from controllers.cf_info import pixel_space_to_scale

class LimitIndicator(pygame.sprite.Sprite):
    def __init__(self, 
        size=[pixel_space_to_scale, pixel_space_to_scale], transparency_collide=255, position = [0, 0],
        layer_all_sprites:object=None, limit_objects:object=None
    ):
        super().__init__()
        
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.transparency_collide = transparency_collide
        self.surf.fill( generic_colors(color='red', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )

        layer_all_sprites.add(self, layer=1)
        limit_objects.add(self)