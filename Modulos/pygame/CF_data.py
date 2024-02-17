import os
from Modulos.Modulo_System import(
    get_system
)
from Modulos.Modulo_Files import(
    Path,
    Files_List
)
from Modulos.Modulo_Text import(
    Text_Read,
    Ignore_Comment,
    Text_Separe
)
from pathlib import Path as pathlib

# Directorio del juego
dir_game = os.path.dirname(__file__)
dir_game = os.path.dirname( os.path.abspath(dir_game) )
dir_game = os.path.dirname( os.path.abspath(dir_game) )
dir_game = os.path.join(dir_game)

dir_data = os.path.join(dir_game, 'data')

# Archivo de data
dir_game_data = os.path.join(dir_data, 'CF.dat')


def get_data(mode_dict=True):
    '''Obtener los datos de ejecución del juego'''
    # Leer texto y ignorar comentarios tipo '#'
    archive_cf = Text_Read(
        dir_game_data,
        'ModeText'
    )
    data_cf = Ignore_Comment(
        text=archive_cf,
        comment='#'
    )
    
    # Agregar valores en el texto a un diccionario
    data_cf = Text_Separe(
        text=data_cf,
        text_separe='='
    )
    
    # Retornor solo el diccionario o el archivo
    if mode_dict == True:
        return data_cf
    else:
        return archive_cf


def set_data():
    '''Establecer el archivo de configuración'''
    if not pathlib(dir_game_data).exists():
        with open(dir_game_data, 'w') as data_text:
            data_text.write(
                'disp=960x540\n'
                'volume=0.02\n'
                'fps=30\n'
                f'current_level={os.path.join(dir_data, "maps/part1/cf_map_part1-level1.txt")}'
            )
        return True
    else:
        return False

set_data()


    

def get_level():
    '''Devuelve el ultimo nivel jugado'''
    data = get_data()
    last_level = data['current_level']
    
    if pathlib(last_level).exists():
        return last_level
    else:
        return None

def set_level(level=None):
    '''
    Establecer el nivel
    Retorna True o False, si es que se creo o no.
    '''
    
    # Verificar el level si existe o no
    level = str(level)
    go = False
    if not pathlib(level).exists():
        level = level.replace(':', '/')
        level = level.split('/')
        level = f'{level[0]}/{level[1]}'
        level = os.path.join(dir_data, 'maps', level)
        
        if pathlib(level).exists():
            go = True
    else:
        go = True

    # Continuar o no
    if go == True:
        # Establecer el level en el archivo de data CF.dat
        data = get_data(mode_dict=False)
        text_ready = ''
        for line in data.split('\n'):
            if line.startswith('current_level='):
                line = f'current_level={level}'
            else:
                pass
            text_ready += line + '\n'
        
        with open(dir_game_data, 'w') as data_text:
            data_text.write(text_ready[:-1])

        return go
    else:
        return go




def get_disp():
    '''Obtener resolución de juego'''
    data = get_data()
    disp = data['disp'].split('x')

    return [ int(disp[0]), int(disp[1]) ]

def set_disp(width=960, height=540):
    '''Establecer resolución de juego'''
    # Establecer resolución en el archivo de data CF.dat
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('disp='):
            line = f'disp={width}x{height}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write(text_ready[:-1])



    
def get_fps():
    '''Obtener FPS de juego'''
    data = get_data()
    return int(data['fps'])

def set_fps(fps=30):
    '''Establecer FPS de juego'''
    if fps > 30:
        fps = 30
    elif fps <= 0:
        fps = 1

    # Establecer los fps en el archivo de data CF.dat
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('fps='):
            line = f'fps={fps}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write(text_ready[:-1])




def get_volume():
    '''Obtener volumen de juego'''
    data = get_data()
    return float(data['volume'])

def set_volume(volume=1):
    '''Establecer volumen de juego'''
    if volume > 1:
        volume = 1
    elif volume <= -1:
        volume = 0.01
    
    # Establecer el volumen en el archivo de data CF.dat
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('volume='):
            line = f'volume={volume}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write(text_ready[:-1])