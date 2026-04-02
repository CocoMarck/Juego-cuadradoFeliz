# Resolución, escala, correcciones.
from core.pygame.math_helpers import (
    resolution_scale_ratio, axis_coord_porcentage, calculate_aspect_ratio
)

# Paths
from config.paths import MUSICS, SPRITES

# Sprites
from entities.pygame.game_object import GameObject
from entities.pygame.sticky_sprite import StickySprite
from entities.pygame.animated_sticky_sprite import AnimatedStickySprite
from core.pygame.graphics_utils import surface_with_background

# Controllers
from controllers.pygame.entities.animation_controller import AnimationController

# Sprites
from core.pygame.render.render_adapter import RenderAdapter

# Pygame
import pygame


GRID_SIZE = 128
player_surf = pygame.Surface( (GRID_SIZE*0.8, GRID_SIZE*0.5), pygame.SRCALPHA )
player_surf.blit(
    surface_with_background( (GRID_SIZE*0.5, GRID_SIZE*0.5), "white"),
    (0,0)
)
player_surf.blit(
    surface_with_background( (GRID_SIZE*0.3, GRID_SIZE*0.1), "white"),
    (GRID_SIZE*0.5,0)
)

def get_surf( color, angle=0 ):
    surf = player_surf.copy()

    mask = pygame.Surface( surf.get_size() ).convert_alpha()
    mask.fill(color)

    surf.blit( mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT )
    if angle != 0:
        return pygame.transform.rotate( surf, angle )

    return surf


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


        # Animation
        player_animations = {
            'idle': (
                [
                    get_surf("blue"),
                    get_surf("red"),
                    get_surf("purple"),
                ], 1
            ),
            'move': (
                [
                    get_surf("white"),
                    get_surf("grey", 10),
                    get_surf("black", -10),
                ], 0.1
            ),
            'move-walk': (
                [
                    get_surf("white"),
                    get_surf("grey", 5),
                    get_surf("black", -5),
                ], 0.2
            ),
            'jumping-idle': (
                [
                    get_surf("skyblue", 10),
                ], 1
            ),
            'falling-idle': (
                [
                    get_surf("pink", -10),
                ], 1
            ),
            'jumping-move': (
                [
                    get_surf("red", 20),
                ], 1
            ),
            'falling-move': (
                [
                    get_surf("yellow", -20),
                ], 1
            )
        }
        animation = AnimatedStickySprite(
            surf=player_animations['idle'][0][0],
            game_object=self.scene.player, center=True,
            animation_controller=AnimationController( player_animations, state='idle' )
        )
        self.insert_sprite(
            animation, size_porcentage_difference, 0
        )
        self.update_sprites()
        self.scene.groups["anims"].add( animation )

    def update_sticky(self):
        self.size_xy = self.window.window_resolution
        self.scaled_size_xy = self.scene.render_resolution
        self.update_all_size_multiplier_xy()
        self.resize_sprites()
        scale_max_ratio = self.get_resolution_scale_ratio( "max" )
        for sprite, _, _ in self._sprites.values():
            sprite.stick(
                multiplier=scale_max_ratio
            )
        self.window.scroll_int = [
            int(self.scene.scroll_float[0]*scale_max_ratio[0]),
            int(self.scene.scroll_float[1]*scale_max_ratio[1])
        ]
