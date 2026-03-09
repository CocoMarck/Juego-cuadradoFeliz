# Librerias estándar
import random

# Librerias externas
import pygame

# Mopdulos internos
from core.pygame.render.scene import Scene
from core.pygame.render.window import Window
from core.pygame.audio.sound_effect import SoundEffect
from core.pygame.math_helpers import (
    get_resolution_porcentage_difference, porcentage_of_coord_on_axis
)
from config.paths import MUSICS, SPRITES



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
        Usando grops y layers.
        '''
        sprite = pygame.sprite.Sprite()
        sprite.surf = pygame.Surface( (self.tile_size, self.tile_size) )
        sprite.rect = sprite.surf.get_rect(
            topleft=(
                self.render_resolution[0]*0.5,self.render_resolution[1]*0.5
            )
        )
        self.layers.add( sprite, layer=0 )
        self.sound_effect = SoundEffect(
            MUSICS[4], volume=1, rect=sprite.rect#pygame.Rect(0, 1, 2, 3)
        )
        self.sound_effect.play(loops=-1)
        self.x_positive = False
        self.count = 0

    def update(self, dt=1, key_get_pressed=None):
        '''
        Actualizar eventos, normalmente solo usando groups.
        Normalmente es, los `"update"`, reciben `sprite.update()`.
        '''
        multiplier_x = porcentage_of_coord_on_axis(
            size=self.render_resolution[0],
            positive_start_counted=self.render_resolution[0],
            negative_start_counted=0,
            coord=self.sound_effect.rect.x
        )
        multiplier_y = porcentage_of_coord_on_axis(
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
        if self.count >= 6:
            self.sound_effect.rect.x = self.render_resolution[0]*0.5
            self.count = 0
            self.x_positive = not self.x_positive
        self.count += dt

        self.sound_effect.set_multiply_init_volume( multiplier )

# Init
scene = SoundEffectsScene(
    render_resolution=[16*32, 9*32], groups={}, name="game"
)
window = Window(
    window_size=[960,540], fps=100, scene=scene, title="Efectos de sonido"
)
window.init_pygame()
scene.init_objects()

if __name__ == "__main__":
    window.run(datetime=True, show_fps=False)
