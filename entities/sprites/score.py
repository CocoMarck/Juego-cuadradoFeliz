import pygame
from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import get_image
from controllers.cf_info import pixel_space_to_scale

from .general_use.multi_layer_sprite import MultiLayerSprite




class Score(MultiLayerSprite):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0], transparency_collide=255, transparency_sprite=255,
        score_objects:object=None, layer_all_sprites:object=None
    ):
        # Inicializar todo
        super().__init__(
         surf=pygame.Surface( ( size//2, size//2 ), pygame.SRCALPHA ), 
         transparency=transparency_collide, position=position, 
         layer=[ get_image('coin', size=[size, size]) ], 
         layer_transparency=transparency_sprite, layer_difference_xy=[0,0]
        )
        
        # Collider
        self.surf.fill( generic_colors('yellow', transparency=transparency_collide) )
        self.rect.x += ( size -self.rect.width)//2
        self.rect.y += ( size -self.rect.height)//2
        
        # Agregar collider
        layer_all_sprites.add(self, layer=3)
        score_objects.add(self)
        
        # Sprite
        self.sprite = self.sprite_layer.layer[0]
        self.sprite.update()
        layer_all_sprites.add(self.sprite, layer=2)
        
        
        # Variables principales
        self.point = False
    
    def remove_point(self):
        if not self.sprite == None:
            self.sprite.kill()
        self.kill()
