# Librerias estándar
import random

# Librerias externas
import pygame

# Sound
from core.pygame.audio.sound_effect import SoundEffect
from core.pygame.audio.sound_effect_group import SoundEffectGroup

# Paths
from config.paths import MUSICS, SPRITES

# Window, render, loop
from core.pygame.render.scene import Scene

# Resolución, escala, correcciones.
from core.pygame.math_helpers import (
    resolution_scale_ratio, axis_coord_porcentage, calculate_aspect_ratio
)

# SoundEffects Window
class CuadradoFelizScene(Scene):
    '''
    La escena de juego. Todo se guardara en el `RenderSurface`.
    '''
    def __init__( self, *args, **kwargs ):
        super().__init__(
            *args,
            groups={
                "characters": pygame.sprite.Group(),
                "music_boxes": pygame.sprite.Group(),
                "solids": pygame.sprite.Group()
            },
            **kwargs
        )

        self.tile_size = self.render_resolution[0]//16
        self.sound_effects = SoundEffectGroup()

    def init_objects(self):
        '''
        Usando groups y layers.
        '''
        sprite = pygame.sprite.Sprite()
        sprite.surf = pygame.Surface( (self.tile_size, self.tile_size) )
        sprite.rect = sprite.surf.get_rect(
            topleft=(
                self.render_resolution[0]*0.5,self.render_resolution[1]*0.5
            )
        )
        self.x_positive = False
        self.count = 0
        self.layers.add( sprite, layer=0 )
        self.groups["music_boxes"].add( sprite )

        fx_sound = SoundEffect(
            MUSICS[5], volume=0.05, rect=sprite.rect#pygame.Rect(0, 1, 2, 3)
        )
        fx_sound.play(loops=-1)
        self.sound_effects.add( fx_sound )


    def update(self, dt=1, key_get_pressed=None):
        '''
        Actualizar eventos, normalmente solo usando groups.
        Normalmente es, los `"update"`, reciben `sprite.update()`.
        '''
        self.count += dt
        # Movement para music boxes.
        for sprite in self.groups["music_boxes"]:
            if self.x_positive:
                sprite.rect.x += self.tile_size*5 * dt
            else:
                sprite.rect.x -= self.tile_size*5 * dt
            if self.count >= 4:
                #sound.rect.x = self.render_resolution[0]*0.5
                self.count = 0
                self.x_positive = not self.x_positive

        # Evento efectos de sonido.
        for sound in self.sound_effects.sounds():
            multiplier_x = axis_coord_porcentage(
                size=self.render_resolution[0],
                positive_start_counted=self.render_resolution[0],
                negative_start_counted=0,
                coord=sound.rect.x
            )
            multiplier_y = axis_coord_porcentage(
                size=self.render_resolution[1],
                positive_start_counted=self.render_resolution[1],
                negative_start_counted=0,
                coord=sound.rect.y
            )
            multiplier = min( multiplier_x, multiplier_y )
            if multiplier > 1:
                multiplier = 1
            elif multiplier < 0:
                multiplier = 0

            sound.set_multiply_init_volume( multiplier )
