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
        self.tile_size = self.window.window_resolution[0]//12
        size_porcentage_difference = resolution_scale_ratio(
            (128,128), (self.tile_size, self.tile_size)
        )
        music_box = self.scene.groups['music_boxes'].sprites()[0]

        # Agragar imagenes pegajosas, con diferencia de tamano, y actualizar posición inicial.
        sticky_sprite = StickySprite(
            surf=surface_with_background( (128,128), color="purple"), game_object=music_box, center=True, alpha=127
        )
        self.insert_sprite(
            sticky_sprite, size_porcentage_difference, 0
        )
        for solid in self.scene.groups['solids']:
            sprite = StickySprite(
                surf=surface_with_background( (128,128), color="white"),
                game_object=solid, center=True, alpha=127
            )
            self.insert_sprite( sprite, size_porcentage_difference, 0 )

        self.update_sprites()

        # Establecer actualizador de capas.
        self.window.update_layers = self.update_sticky

    def update_sticky(self):
        self.size_xy = self.window.window_resolution
        self.scaled_size_xy = self.scene.render_resolution
        self.update_all_size_multiplier_xy()
        self.resize_sprites()
        for sprite, _, _ in self._sprites.values():
            sprite.stick(
                multiplier=self.get_resolution_scale_ratio( "max" )
            )
