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

# Sprites
from entities.pygame.game_object import GameObject
from entities.cuadrado_feliz.object_with_happy_physics import ObjectWithHappyPhysics
from entities.cuadrado_feliz.player import Player

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

        # Scroll
        self.scroll_float = [0.0,0.0]

    def init_objects(self):
        '''
        Usando groups y layers.
        '''
        sprite = ObjectWithHappyPhysics(
            surf=pygame.Surface( (self.tile_size, self.tile_size) ),
            position=(
                self.render_resolution[0]*0.5,self.render_resolution[1]*0.5
            ), name="music_box", group="music_boxes"
        )
        #sprite.vertical_force = 0
        self.x_positive = True
        self.count = 0
        self.layers.add( sprite, layer=0 )
        self.groups["music_boxes"].add( sprite )

        for tile in range(0, 64):
            solid = GameObject(
                surf=pygame.Surface( (self.tile_size, self.tile_size) ),
                position=( tile*self.tile_size, self.render_resolution[1]-self.tile_size  )
            )
            self.groups["solids"].add(solid)
            self.layers.add( solid, layer=0 )
        for tile in range(0, 8):
            solid = GameObject(
                surf=pygame.Surface( (self.tile_size, self.tile_size) ),
                position=( 0, tile*self.tile_size )
            )
            self.groups["solids"].add(solid)
            self.layers.add( solid, layer=0 )

        for tile in range(0, 8):
            solid = GameObject(
                surf=pygame.Surface( (self.tile_size, self.tile_size) ),
                position=( self.render_resolution[0]*3-self.tile_size, tile*self.tile_size )
            )
            self.groups["solids"].add(solid)
            self.layers.add( solid, layer=0 )

        fx_sound = SoundEffect(
            MUSICS[5], volume=0.05, rect=sprite.rect#pygame.Rect(0, 1, 2, 3)
        )
        fx_sound.play(loops=-1)
        self.sound_effects.add( fx_sound )

        # Player
        self.player = Player(
            surf=pygame.Surface( (self.tile_size, self.tile_size) ),
            position=( self.render_resolution[0]*0.2, self.render_resolution[1]*0.2 )
        )
        self.groups["characters"].add(self.player)
        self.layers.add( self.player, layer=0 )


    def update(self, dt=1, fps=1, key_get_pressed=None):
        '''
        Actualizar eventos, normalmente solo usando groups.
        Normalmente es, los `"update"`, reciben `sprite.update()`.
        '''
        self.count += dt

        # Scroll
        self.scroll_float = self.calculate_scroll(
            xy=self.player.rect, view_xy=self.render_resolution, difference_xy=[0,0]
        )

        # Movement para music boxes.
        for sprite in self.groups["music_boxes"]:
            if self.x_positive:
                sprite.moving_xy[0] = self.tile_size*5
            else:
                sprite.moving_xy[0] = -self.tile_size*5
            if self.count >= 4:
                #sound.rect.x = self.render_resolution[0]*0.5
                self.count = 0
                self.x_positive = not self.x_positive
            sprite.update(dt, self.groups["solids"])

        # Evento efectos de sonido.
        for sound in self.sound_effects.sounds():
            multiplier_x = axis_coord_porcentage(
                size=self.render_resolution[0],
                positive_start_counted=self.render_resolution[0],
                negative_start_counted=0,
                coord=sound.rect.x-self.scroll_float[0]
            )
            multiplier_y = axis_coord_porcentage(
                size=self.render_resolution[1],
                positive_start_counted=self.render_resolution[1],
                negative_start_counted=0,
                coord=sound.rect.y-self.scroll_float[1]
            )
            multiplier = min( multiplier_x, multiplier_y )
            if multiplier > 1:
                multiplier = 1
            elif multiplier < 0:
                multiplier = 0

            sound.set_multiply_init_volume( multiplier )

        # Characters
        self.player.handle_input( key_get_pressed )
        for character in self.groups['characters']:
            character.move()
            character.update( dt, self.groups['solids'] )

    def calculate_scroll(
        self, xy=[0,0], view_xy=[0,0], limit_xy=[0,0], difference_xy=[0,0]
    ) ->[float, float]:

        return [ (xy[0] -view_xy[0]/2), (xy[1] -view_xy[1]/2) ]

    def render(self):
        '''
        Renderizado, utilizando layers.
        '''

        scroll_int = [ int(self.scroll_float[0]), int(self.scroll_float[1]) ]
        self.render_surface.fill( 'green' )
        for sprite in self.layers.sprites():
            self.render_surface.blit(
                sprite.surf, (
                    sprite.rect.x -scroll_int[0], sprite.rect.y -scroll_int[1]
                )
            )
