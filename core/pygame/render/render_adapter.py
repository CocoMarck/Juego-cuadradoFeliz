from .window import Window
from core.pygame.math_helpers import get_resolution_porcentage_difference

class RenderAdapter():
    '''
    Para establecer imagenes en window layers.

    sticky_sprites = {
        "name": [sprite, size_multiplier_xy, layer]
    }
    Multiplo con respecto a size_xy
    '''
    def __init__(self, layers, size_xy, scaled_size_xy, sprites: dict = None ):
        self.layers = layers
        self.size_xy = size_xy
        self.scaled_size_xy = scaled_size_xy
        self._sprites = sprites

    def insert_sprites(self):
        for sprite, size_multiplier_xy, layer in self._sprites:
            self.layers.add( sprite, layer=layer )

    def resize_sprites(self):
        for sprite, size_multiplier_xy, layer in self._sprites:
            sprite.resize_with_multiplier( size_multiplier_xy )

    def get_multiplier(self):
        return get_resolution_porcentage_difference( self.size_xy, self.scaled_size_xy )
