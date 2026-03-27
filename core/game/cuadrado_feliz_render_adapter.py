# Resolución, escala, correcciones.
from core.pygame.math_helpers import (
    resolution_scale_ratio, axis_coord_porcentage, calculate_aspect_ratio
)

# Paths
from config.paths import MUSICS, SPRITES

# Sprites
from entities.pygame.game_object import GameObject
from entities.pygame.sticky_sprite import StickySprite
from core.pygame.graphics_utils import surface_with_background

# Sprites
from core.pygame.render.render_adapter import RenderAdapter

class CuadradoFelizRenderAdapter(RenderAdapter):
    def __init__(self, window, scene):
        self.window = window
        self.scene = scene

        super().__init__(
            layers = self.window.layers, size_xy = self.window.window_resolution, scaled_size_xy = self.scene.render_resolution
        )

        # Tamaño de cuadritos y escala de images
        self.tile_size = self.window.window_resolution[0]//8
        self.size_porcentage_difference = resolution_scale_ratio(
            (128,128), (self.tile_size, self.tile_size)
        )
        self.music_box = self.scene.groups['music_boxes'].sprites()[0]

        # Agragar imagenes pegajosas, con diferencia de tamano, y actualizar posición inicial.
        self.sticky_sprite = StickySprite(
            surf=surface_with_background( (128,128), color="purple"), game_object=self.music_box, center=True, alpha=127
        )
        self.insert_sprite(
            self.sticky_sprite, self.size_porcentage_difference, 0
        )
        self.update_sprites()

        # Establecer actualizador de capas.
        self.window.update_layers = self.update_sticky

    def update_sticky(self):
        self.size_xy = self.window.window_resolution
        self.scaled_size_xy = self.scene.render_resolution
        self.update_all_size_multiplier_xy()
        self.resize_sprites()
        self.sticky_sprite.stick(
            multiplier=self.get_resolution_scale_ratio( "max" )
        )
