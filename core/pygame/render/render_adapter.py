from .window import Window
from core.pygame.math_helpers import resolution_scale_ratio, axis_coord_porcentage

class RenderAdapter():
    '''
    Para establecer imagenes en window layers.

    ```python
    sticky_sprites = [
        [sprite: GameObject, size_multiplier_xy: list, layer: int]
    ]
    ```
    > Multiplo con respecto a size_xy. El sprite tiene que ser un `GameObject`
    '''
    def __init__(self, layers, size_xy, scaled_size_xy ):
        self.layers = layers
        self.size_xy = size_xy
        self.scaled_size_xy = scaled_size_xy
        self._sprites = {}

    def insert_sprite(self, sprite, size_multiplier_xy, layer):
        key = len(self._sprites.keys())
        self._sprites[key] = [sprite, size_multiplier_xy, layer]
        return True

    def remove_sprite(self, key):
        if key in self._sprites.keys():
            del self._sprites[key]
            return True
        return False

    def update_sprite_size_multiplier_xy(self, key, size_multiplier_xy):
        self._sprites[key][1] = size_multiplier_xy

    def clear_sprites(self):
        self._sprites.clear()

    def add_sprites_to_layers(self):
        for sprite, size_multiplier_xy, layer in self._sprites.values():
            self.layers.add( sprite, layer=layer )

    def resize_sprites(self):
        for sprite, size_multiplier_xy, layer in self._sprites.values():
            sprite.resize_with_multiplier( size_multiplier_xy )

    def update_sprites(self):
        self.layers.empty()
        self.add_sprites_to_layers()
        self.resize_sprites()

    def get_resolution_sacle_ratio(self):
        return resolution_scale_ratio( self.size_xy, self.scaled_size_xy )
