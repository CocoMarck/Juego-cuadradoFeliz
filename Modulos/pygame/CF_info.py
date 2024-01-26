import sys, os

# Resolución de pantalla de juego
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
current_level = os.path.join(dir_maps, 'part1', 'cf_map_part1-level3.txt')