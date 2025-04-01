import os, sys
from logic.Modulo_System import(
    get_system
)
from logic.Modulo_Files import(
    Path,
    Files_List
)
from logic.Modulo_Text import(
    Text_Read,
    Ignore_Comment, Text_Separe, Only_Comment, ignore_text_filter
)
from data.Modulo_Language import get_text
from entities import CF, Map
from pathlib import Path as pathlib

# Directorio del juego
#dir_game = os.path.dirname(__file__)
#dir_game = os.path.join(dir_game, '../..')
#dir_game = os.path.join('')
dir_game = pathlib().absolute()

dir_data = os.path.join(dir_game, 'resources')

# Subcarpetas
dir_maps = os.path.join(dir_data, 'maps')

# Archivo de data
dir_game_data = os.path.join(dir_data, 'CF.dat')

# Archivo de juego completado
file_gamecomplete = os.path.join(dir_data, 'gamecomplete.dat')


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
                'music=True\n'
                'climate_sound=True\n'
                'show_clouds=False\n'
                'show_collide=False\n'
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
        return os.path.join(dir_maps, 'cf_map_default.txt')

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





def get_level_list():
    '''
    Obtener una lista de todos los niveles disponibles
    Una lista con los niveles disponibles en la ruta del juego ".data/maps/*"
    Tienen que empezar con "cf_map_"  y terminar en ".txt' (incluir subcarpetas)
    
    Solo detecta las carpetas: part1, part2, part3 y custom.
    '''
    # Subdirectorios de mapas.
    sub_dir_maps = [
        os.path.join(dir_maps, 'part1'),
        os.path.join(dir_maps, 'part2')
    ]

    dir_custom = os.path.join(dir_maps, 'custom')
    sub_dir_maps.append( dir_custom )
    custom_dir_list = os.listdir( dir_custom )

    for x in custom_dir_list:
        sub_dir_maps.append( os.path.join(dir_custom, x) )

    # Obtener mapas
    list_level = []
    for sub_dir in sub_dir_maps:
        for level_map in Files_List(
            files='cf_map_*.txt',
            path=sub_dir,
            remove_path=False
        ):
            list_level.append(level_map)
    
    # Asi se imprimirian
    #for level in list_level:
    #   print( f'{level}\n\n' )
    
    return list_level




def get_music():
    '''
    Para saber si se desea o no escuchar musica en el juego
    Devuelve un boleano, True or False
    '''
    data = get_data()
    music = data['music']
    if music == "True":
        return True
    else:
        return False

def set_music(music=True):
    '''
    Para establecer si reproducir musica o no
    '''
    # Establecer si reproducir musica o no en el archivo de data CF.dat
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('music='):
            line = f'music={music}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write(text_ready[:-1])




def get_climate_sound():
    '''
    Saber si sonara el sonido del clima
    '''
    data = get_data()
    climate_sound = data['climate_sound']
    if climate_sound == "True":
        return True
    else:
        return False


def set_climate_sound(climate_sound=True):
    '''
    Para establecer si reproducir el sonido de ambiente o no.
    '''
    # Establecer si reproducir musica o no en el archivo de data CF.dat
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('climate_sound='):
            line = f'climate_sound={climate_sound}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write(text_ready[:-1])





def save_gamecomplete(level=None, score=None):
    '''
    Guardar juego completado
    '''
    if not type(score) is int:
        score = 0
    line_save = f'{level}, {score}'
    
    if pathlib(file_gamecomplete).exists():
        line_save = f'\n{line_save}'
        with open(file_gamecomplete, 'a') as text:
            text.write(line_save)
    else:
        with open(file_gamecomplete, 'w') as text:
            text.write(line_save)


def get_gamecomplete():
    '''
    Obtener juegos completados
    '''
    if pathlib(file_gamecomplete).exists():
        text = Text_Read(
            file_gamecomplete,
            'ModeList'
        )
        list_gamecomplete = []
        for i in text:
            info = i.split(',')
            info = [ info[0], int(info[1]) ]
            list_gamecomplete.append(info)
        return list_gamecomplete
    else:
        return None
        
        


def get_show_collide():
    '''
    Para saber si se desea o ver colliders o no
    Devuelve un boleano, True or False
    '''
    data = get_data()
    show_collide = data['show_collide']
    if show_collide == "True":
        return True
    else:
        return False

def set_show_collide(show_collide=True):
    '''
    Para establecer si se desea ver colliders o no
    '''
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('show_collide='):
            line = f'show_collide={show_collide}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write(text_ready[:-1])




def get_show_sprite():
    '''
    Para saber si se desea o ver colliders o no
    Devuelve un boleano, True or False
    '''
    data = get_data()
    if data['show_sprite'] == "True":
        return True
    else:
        return False

def set_show_sprite(show_sprite=True):
    '''
    Para establecer si se desea ver colliders o no
    '''
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('show_sprite='):
            line = f'show_sprite={show_sprite}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write(text_ready[:-1])




def get_show_clouds():
    '''
    Para saber si se mostraran las nubes o no.
    Devuelve un boleano, True o False
    '''
    data = get_data()
    show_clouds = data['show_clouds']
    if show_clouds == 'True':
        return True
    else:
        return False

def set_show_clouds(show_clouds=True):
    '''
    Para mostrar o no las nubes
    '''
    data = get_data(mode_dict=False)
    text_ready = ''
    for line in data.split('\n'):
        if line.startswith('show_clouds='):
            line = f'show_clouds={show_clouds}'
        else:
            pass
        text_ready += line + '\n'
    
    with open(dir_game_data, 'w') as data_text:
        data_text.write( text_ready[:-1] )




def credits(share=True, jump_lines=False):
    # Creditos al creador
    # Establecer si se quiere compartir el arroba del creador
    # y si se quiere separar mediente un salto de linea
    credits = 'Jean Abraham Chacón Candanosa'

    if jump_lines == True:
        jln = '\n'
    else:
        jln = ' '
    
    if share == True:
        credits += f'{jln}@CocoMarck'
    else:
        pass

    return credits



display_width_divisor = 60
def read_CF( CF ) -> bool:
    CF.disp = get_disp()
    CF.pixel_space = CF.disp[0]//display_width_divisor

    CF.volume = get_volume()
    CF.fps = get_fps()

    CF.music = get_music()
    CF.climate_sound = get_climate_sound()
    CF.show_clouds = get_show_clouds()

    CF.show_collide = get_show_collide()
    CF.show_sprite = get_show_sprite()
    
    CF.current_level = get_level()




def save_CF( CF ) -> bool:
    try:
        set_disp( CF.disp[0], CF.disp[1] )
        CF.pixel_space = CF.disp[0]//display_width_divisor

        set_volume( CF.volume )
        set_fps( CF.fps )

        set_music( CF.music )
        set_show_clouds( CF.show_clouds )
        set_climate_sound( CF.climate_sound )

        set_show_collide( CF.show_collide )
        set_show_sprite( CF.show_sprite )
    
        set_level( CF.current_level )
        
        return True
    except:
        return False




# Tipos de objetos
dict_object = {
    'space': '.',
    'space-alternative': '#',
    'limit': '|',

    'player': 'j',

    'stone': 'p',
    'stone-big': 'P',
    'coin': 's',

    'spike': '^',
    'spike-big': 'A',
    'spike-anim': '\\',
    'spike-instakill': '!',

    'star-pointed': 'Y',
    'star-pointed-anim': '*',
    'star-pointed-instakill': 'X',

    'ladder-y': 'H',
    'trampoline': '_',

    'ladder-x-right': '+',
    'ladder-x-left': '-',

    'elevator-y': 'x',
    'elevator-x': 'y',
    
    'climate-rain': '~',

    'level-change': '0',
    'end-game': 'F'
}
prefix_object = ''
for key in dict_object.keys():
    prefix_object += dict_object[key]
dict_climate = {
    'default': [108,150,255],
    'rain': [155,168,187],
    'sunny': [240,202,134],
    'alien': [68,38,136],
    'black': [47,47,47]
}
def read_Map( Map, level=str ) -> bool:
    '''Leer el archivo map y establecer sus parametros'''
    # Leer archivo
    text_level = Text_Read(level, 'ModeText')
    
    # Obtener información de parametros
    #Map.path = None
    #Map.next_level = None
    #Map.climate = None
    #Map.message_start = None
    
    map_info = Only_Comment(
        text=text_level,
        comment='$$'
    )
    number_info = 0
    info = None
    if not map_info == None:
        info = []
        for line in map_info.split('\n'):
            info.append(line)
            number_info += 1
        if not info[0] == '':
            path_and_level = info[0].split(':')
            Map.path = path_and_level[0]
            Map.next_level = path_and_level[1]
            
    if number_info >= 2:
        Map.climate = info[1]
    else:
        Map.climate = None
    
    Map.message_start = None
    if number_info >= 3:
        if not info[2].replace( ' ', '') == '':
            Map.message_start = info[2]

    
    
    # Obtener información del mapa
    map_level = Ignore_Comment(text=text_level, comment='//')
    map_level = Ignore_Comment(text=map_level, comment='$$')
    
    Map.list_map = []
    for line in map_level.split('\n'):
        text = ignore_text_filter( line, prefix_object )
        if not text == None:
            Map.list_map.append( list(text) )


def return_map( Map ):
    save_this_text = ''
    for line in Map.list_map:
        for char in line:
            save_this_text += char
        save_this_text += '\n'
    return save_this_text[:-1]
    
def save_Map( Map, file=None ):
    with open( file, 'w', encoding='utf-8') as file_text:
        text = return_map( Map )

        text += '\n'
        preset = '$$'

        # Path y level
        if isinstance(Map.path, str):
            text += f'{preset}{Map.path}:'
            if isinstance(Map.next_level, str):
                text += f'{Map.next_level}'
            text += '\n'
        else:
            text +=  f'{preset}\n'
        
        # Clima
        if isinstance(Map.climate, str):
            text += f'{preset}{Map.climate}\n'
        else:
            text += f'{preset}\n'
            
        # Mensaje
        if isinstance(Map.message_start, str):
            text += f'$${Map.message_start}'
        else:
            text += f'{preset}'
        
        # Escribir datos / guardar mapa
        file_text.write( text )