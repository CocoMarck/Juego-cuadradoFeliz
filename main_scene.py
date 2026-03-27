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
from core.pygame.render.render_adapter import RenderAdapter
from core.pygame.render.scene import Scene
from core.pygame.render.window import Window

# Resolución, escala, correcciones.
from core.pygame.math_helpers import (
    resolution_scale_ratio, axis_coord_porcentage, calculate_aspect_ratio
)

# Sprites
from entities.pygame.game_object import GameObject
from entities.pygame.sticky_sprite import StickySprite
from core.pygame.graphics_utils import surface_with_background

# Game
from core.game.cuadrado_feliz_scene import CuadradoFelizScene
from core.game.cuadrado_feliz_render_adapter import CuadradoFelizRenderAdapter


# Init
scene = CuadradoFelizScene(
    render_resolution=[16*32, 9*32], name="game"
)
window = Window(
    window_resolution=[960, 540], fps=100, scene=scene, resize=True, title="Efectos de sonido"
)
window.init_pygame()
scene.init_objects()

render_adapter = CuadradoFelizRenderAdapter( window=window, scene=scene )



if __name__ == "__main__":
    window.run(datetime=True, show_fps=False)
