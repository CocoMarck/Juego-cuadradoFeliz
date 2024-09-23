'''
Este modulo tiene la función de obtener los datos/recursos necesarios para que el programa tenga imagenes/iconos/sonidos. Etc...
'''
from logic.Modulo_System import *
import os, sys

# Obtén la ruta al directorio actual del script
current_dir = os.path.dirname( os.path.abspath(sys.argv[0]) )

# Data
dir_data = os.path.join(current_dir, 'resources')

# Subcarpeta
dir_icon = os.path.join( dir_data, 'icons' )
dir_images = os.path.join( dir_data, 'images' )

# Archivos...

# Archivos | Fuente de texto
if get_system() == 'win':
    file_font = 'Cascadia Code'
else:
    file_font = 'Liberation Mono'
