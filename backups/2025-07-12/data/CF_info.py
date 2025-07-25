from entities import CF
from data.CF_data import (
    get_disp,
    get_fps,
    get_volume,
    get_level,
    get_show_collide,
    get_show_clouds,

    dir_game,
    dir_maps,
    dir_data,
    read_CF
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
data_CF = CF
read_CF( data_CF )

# Titulo del juego
game_title = 'El cuadrado Feliz'


# Directorio del juego "dir_data". Y...
# Sub directorios Data
dir_sprites = os.path.join(dir_data, 'sprites')
dir_audio = os.path.join(dir_data, 'audio')

scale_surface_size = [960, 540]
pixel_space_to_scale = 16