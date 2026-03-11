# Librerias estándar
import random

# Librerias externas
import pygame

# Mopdulos internos
from core.pygame.render.scene import Scene
from core.pygame.render.window import Window
from core.pygame.audio.sound_effect import SoundEffect
from core.pygame.math_helpers import (
    resolution_scale_ratio, axis_coord_porcentage, calculate_aspect_ratio
)
from config.paths import MUSICS, SPRITES
from core.pygame.render.render_adapter import RenderAdapter
from entities.pygame.game_object import GameObject
from entities.pygame.sticky_sprite import StickySprite
from core.pygame.graphics_utils import surface_with_background


# SoundEffects Window
class SoundEffectsScene(Scene):
    '''
    La escena de juego. Todo se guardara en el `RenderSurface`.
    '''
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )

        self.tile_size = self.render_resolution[0]//16

    def init_objects(self):
        '''
        Usando groups y layers.
        '''
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = pygame.Surface( (self.tile_size, self.tile_size) )
        self.sprite.rect = self.sprite.surf.get_rect(
            topleft=(
                self.render_resolution[0]*0.5,self.render_resolution[1]*0.5
            )
        )
        self.layers.add( self.sprite, layer=0 )
        self.sound_effect = SoundEffect(
            MUSICS[5], volume=1, rect=self.sprite.rect#pygame.Rect(0, 1, 2, 3)
        )
        self.sound_effect.play(loops=-1)
        self.x_positive = False
        self.count = 0

    def update(self, dt=1, key_get_pressed=None):
        '''
        Actualizar eventos, normalmente solo usando groups.
        Normalmente es, los `"update"`, reciben `sprite.update()`.
        '''
        multiplier_x = axis_coord_porcentage(
            size=self.render_resolution[0],
            positive_start_counted=self.render_resolution[0],
            negative_start_counted=0,
            coord=self.sound_effect.rect.x
        )
        multiplier_y = axis_coord_porcentage(
            size=self.render_resolution[1],
            positive_start_counted=self.render_resolution[1],
            negative_start_counted=0,
            coord=self.sound_effect.rect.y
        )
        multiplier = min( multiplier_x, multiplier_y )
        if multiplier > 1:
            multiplier = 1
        elif multiplier < 0:
            multiplier = 0
        if self.x_positive:
            self.sound_effect.rect.x += self.tile_size*5 * dt
        else:
            self.sound_effect.rect.x -= self.tile_size*5 * dt
        if self.count >= 4:
            #self.sound_effect.rect.x = self.render_resolution[0]*0.5
            self.count = 0
            self.x_positive = not self.x_positive
        self.count += dt

        self.sound_effect.set_multiply_init_volume( multiplier )

# Init
scene = SoundEffectsScene(
    render_resolution=[16*32, 9*32], groups={}, name="game"
)
window = Window(
    window_resolution=[960, 540], fps=100, scene=scene, resize=True, title="Efectos de sonido"
)
window.init_pygame()
scene.init_objects()


grid_size = window.window_resolution[0]//16
size_porcentage_difference = resolution_scale_ratio(
    (128,128), (grid_size, grid_size)
)
sticky_sprite = StickySprite(
    surf=surface_with_background( (128,128), color="purple"), game_object=scene.sprite, center=True, alpha=127
)
render_adapter = RenderAdapter(
    layers=window.layers,
    size_xy=window.window_resolution, scaled_size_xy=scene.render_resolution,
)
render_adapter.insert_sprite(
    sticky_sprite, size_porcentage_difference, 0
)
coord_porcentage_difference = resolution_scale_ratio(
    window.window_resolution, scene.render_resolution, dividend="max"
)
print( coord_porcentage_difference )
print( calculate_aspect_ratio( window.window_resolution ) )
render_adapter.update_sprites()
def update_sticky():
    dividend_coord = "min"
    if window.window_resolution[0] > scene.render_resolution[0]:
        dividend_coord = "max"
    grid_size = window.window_resolution[0]//8
    dividend_size = "min"
    if sticky_sprite.get_spawn_size()[0] < grid_size:
        dividend_size = "max"
    render_adapter.update_sprite_size_multiplier_xy(
        0, resolution_scale_ratio(
            sticky_sprite.get_spawn_size(), (grid_size, grid_size), dividend=dividend_size
        )
    )
    render_adapter.resize_sprites()
    sticky_sprite.stick(
        multiplier=resolution_scale_ratio(
            window.window_resolution, scene.render_resolution, dividend=dividend_coord
        )
    )
window.update_layers = update_sticky



if __name__ == "__main__":
    window.run(datetime=True, show_fps=False)
