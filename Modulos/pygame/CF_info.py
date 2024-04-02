from Modulos.pygame.CF_data import (
    get_disp,
    get_fps,
    get_volume,
    get_level,
    get_show_collide,
    get_show_clouds,

    dir_game,
    dir_maps,
    dir_data
)
import os, pygame
#import sys

# Inicalizar pygame
pygame.init()

# Resolución de pantalla de juego
# Obligatorio resoluciones tipo 16:9, de lo contrario no funciona, o funcionara raro.
# Los blockes/cuadricula tienen esta dimencion = (disp_width//60). Recuerda que los "//" son para que el resultado de la divición sea un entero (redondea). Lo mas adecuado hubiera sido (disp_height//60)
# 480x270
# 960x540
# 1440x810
# 1920x1080
disp = get_disp()
disp_width = disp[0]
disp_height = disp[1]

# Fotogramas del juego
fps = get_fps()

# Titulo del juego
game_title = 'El cuadrado Feliz'

# Mostrar collider
show_collide=get_show_collide()
if show_collide == True:
    show_sprite = False
else:
    show_sprite = True

# Mostrar nubes
show_clouds=get_show_clouds()

# Volumen
volume = get_volume()




# Directorio del juego "dir_data". Y...
# Sub directorios Data
dir_sprites = os.path.join(dir_data, 'sprites')
dir_audio = os.path.join(dir_data, 'audio')



# Nivel actual
current_level = get_level()