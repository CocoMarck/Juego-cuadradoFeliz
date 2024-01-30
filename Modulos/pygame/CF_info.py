import sys, os

# Resolución de pantalla de juego
# Obligatorio resoluciones tipo 16:9, de lo contrario no funciona, o funcionara raro.
# Los blockes/cuadricula tienen esta dimencion = (disp_width//60). Recuerda que los "//" son para que el resultado de la divición sea un entero (redondea). Lo mas adecuado hubiera sido (disp_height//60)
# 480x270
# 960x540
# 1440x810
# 1920x1080
disp_width = 960
disp_height = 540

# Fotogramas del juego
fps = 30

# Titulo del juego
game_title = 'El cuadrado Feliz'




# Directorio del juego
dir_game = os.path.dirname(__file__)
dir_game = os.path.dirname( os.path.abspath(dir_game) )
dir_game = os.path.dirname( os.path.abspath(dir_game) )
dir_game = os.path.join(dir_game, '.')

dir_data = os.path.join(dir_game, 'data')

# Sub directorios Data
dir_sprites = os.path.join(dir_data, 'sprites')
dir_maps = os.path.join(dir_data, 'maps')



# Nivel actual
current_level = os.path.join(dir_maps, 'part1', 'cf_map_part1-level4.txt')