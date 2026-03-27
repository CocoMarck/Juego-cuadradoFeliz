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
        self._sprites_first_multiplier_xy = {}
        self._init_resolution_scale_ratio = self.get_resolution_scale_ratio()

    def insert_sprite(self, sprite, size_multiplier_xy, layer):
        key = len(self._sprites.keys())
        self._sprites[key] = [sprite, size_multiplier_xy, layer]
        self._sprites_first_multiplier_xy[key] = size_multiplier_xy
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

    def _get_dividend(self, option="max"):
        strings = ["min", "max"]
        if option == "max":
            strings = ["max", "min"]
        if (
            (self.size_xy[0] > self.scaled_size_xy[0]) or
            (self.size_xy[1] > self.scaled_size_xy[1])
        ):
            return strings[0]
        return strings[1]

    def get_resolution_scale_ratio(self, option="min" ):
        return resolution_scale_ratio(
            self.size_xy, self.scaled_size_xy, dividend=self._get_dividend(option)
        )

    def get_updated_resolution_scale_ratio(self, option):
        current_resolution_scale_ratio = self.get_resolution_scale_ratio( option )
        dividend = "min"
        if self._init_resolution_scale_ratio > current_resolution_scale_ratio:
            dividend = "max"
        return resolution_scale_ratio(
            self._init_resolution_scale_ratio, current_resolution_scale_ratio, dividend=dividend
        )

    def update_all_size_multiplier_xy(self):
        for key in self._sprites.keys():
            if (
                self._sprites_first_multiplier_xy[key][0] > 1 or
                self._sprites_first_multiplier_xy[key][1] > 1
            ):
                option = "max"
            else:
                option = "min"
            multiplier_xy = self.get_updated_resolution_scale_ratio( option )

            new_size_multiplier = (
                self._sprites_first_multiplier_xy[key][0]*multiplier_xy[0],
                self._sprites_first_multiplier_xy[key][1]*multiplier_xy[1]
            )
            self._sprites[key][1] = new_size_multiplier

