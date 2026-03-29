# Librerias estándar
import random

# Librerias externas
import pygame

# Paths
from config.paths import MUSICS, SPRITES

# Window, render, loop
from core.pygame.render.window import Window

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
