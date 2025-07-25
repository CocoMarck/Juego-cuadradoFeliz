import pygame
from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import get_image
from controllers.cf_info import pixel_space_to_scale




class Score(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0], transparency_collide=255, transparency_sprite=255,
        score_objects:object=None, layer_all_sprites:object=None
    ):
        super().__init__()
        
        # Transaparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        self.surf = pygame.Surface( ( size//2, size//2 ), pygame.SRCALPHA )
        self.surf.fill( generic_colors('yellow', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.x += ( size -self.rect.width)//2
        self.rect.y += ( size -self.rect.height)//2
        
        # Agregar collider
        layer_all_sprites.add(self, layer=3)
        score_objects.add(self)
        
        # Sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = get_image( 'coin', size=[size, size], transparency=self.transparency_sprite )
        self.sprite.rect = self.sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add(self.sprite, layer=3)
        
        
        # Variables principales
        self.point = False
    
    def remove_point(self):
        if not self.sprite == None:
            self.sprite.kill()
        self.kill()
