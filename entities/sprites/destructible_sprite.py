import pygame
from .general_use.multi_layer_sprite import MultiLayerSprite


class DestructibleSprite( MultiLayerSprite ):
    def __init__(
        self, size=[int,int], sprite=pygame.Surface, position=[int,int], time=int,
        sprite_transparency=int, collider_transparency=int, collider_color=[int,int,int],
        update_objects=pygame.sprite.Group, layer_all_sprites=pygame.sprite.LayeredUpdates
    ):


        # Solo si sprite es un surface
        layer = [sprite]

        # Collider
        surf = pygame.Surface( size, pygame.SRCALPHA )
        surf.fill( (255,255,255) )

        # Inicializar
        super().__init__(
            surf=surf, transparency=collider_transparency, position=position,
            layer=layer, layer_transparency=sprite_transparency, layer_difference_xy=[0,0]
        )
        self.sprite_layer.update_layer()
        self.sprite_layer.transparency = 255
        self.sprite_layer.set_transparency_layer()

        self.time = time

        self.update_objects = update_objects
        self.layer_all_sprites = layer_all_sprites

        self.update_objects.add( self )
        self.layer_all_sprites.add(self, layer=2)
        self.sprite_layer.add_to_layer_group( layer_all_sprites, layer=1 )

    def count(self):
        if self.time_count == self.time:
            self.sprite_layer.rm_layer()
            self.kill()
        self.time_count += 1

    def update(self):

        self.count()
