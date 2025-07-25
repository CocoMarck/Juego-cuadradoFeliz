'''
Funciones especificamente para el juego Cuadrado Feliz
'''
from core.text_util import * # No lo necesita
from core.file_util import list_files

from controllers.cf_info import *
from controllers.cf_controller import *
from core.pygame.pygame_util import *

import math
import pygame, os, random




# Sonidos
sound_type = '.ogg'
all_sounds = {
    'steps':
    [
        pygame.mixer.Sound( dir_audio.joinpath('effects/steps/step-1.ogg') ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/steps/step-2.ogg') ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/steps/step-3.ogg') )
    ],
    
    'hits': [
        pygame.mixer.Sound( dir_audio.joinpath('effects/hits/hit-1.ogg') ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/hits/hit-2.ogg') ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/hits/hit-3.ogg') )
    ],
    
    'jump': pygame.mixer.Sound(dir_audio.joinpath('effects/jump.ogg') ),
    
    'dead': [
        pygame.mixer.Sound( dir_audio.joinpath('effects/dead/dead-1.ogg' ) ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/dead/dead-2.ogg' ) ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/dead/dead-3.ogg' ) )
    ],
    
    'score': [
        pygame.mixer.Sound( dir_audio.joinpath('effects/items/score-1.ogg' ) ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/items/score-2.ogg' ) ),
        pygame.mixer.Sound( dir_audio.joinpath('effects/items/score-3.ogg' ) )
    ]
}
# Sonido | Establecer Volumen
for key in all_sounds.keys():
    sound_or_sounds = all_sounds[key]
    if isinstance( sound_or_sounds, list):
        for sound in sound_or_sounds:
            sound.set_volume( data_CF.volume )
    else:
        sound_or_sounds.set_volume( data_CF.volume )
        
        
# Sonido | Musica
all_music = {}
dir_music = os.path.join(dir_audio, 'music/') # Sin os no jala el este for
for music in list_files( files=f'*{sound_type}', path=dir_music ):
    name = music.replace(dir_music, '').replace(sound_type, '')
    all_music.update( {name: music} )
#for key in all_music.keys():
#    print(key)
#    print(all_music[key])




# Sonido | Función para devolver un sonido
def get_sound( sound=None, number=None ) -> pygame.mixer.Sound:
    '''
    Devuelve un objeto pygame.mixer.Sound.
    sound=str, es un key para diccionario all_sprites
    number=int, es el indice para poner en una lista de sonidos que este en all_sprites
    '''
    # Detectar que los parametros esten correctos
    error = False
    if sound == None:
        error = True
    else:
        sound_good = False
        for key in all_sounds.keys():
            if sound == key:
                if sound_good == False:
                    sound_good = True
        if sound_good == False:
            error = True
    
    # Detectar que parametro number este correcto
    if not number == None and error == False:
        if (type(all_sounds[sound]) == list):
            if (
                ( not number <= ( len( all_sounds[sound] )-1 ) ) or
                ( number < 0 )
            ):
                error = True
    
    # El error es verdadero, establecer un sonido default
    if error == True:
        sound = 'steps'
        number = 0
    
    # Devolver sonido | Establecer sonido final
    if type( all_sounds[sound] ) == list:
        if number == None:
            sound_final = random.choice( all_sounds[sound] )
        else:
            sound_final = all_sounds[sound][number]
    else:
        sound_final = all_sounds[sound]
    
    return sound_final




# Sprites
all_images = {
    'icon':
    ( dir_data.joinpath('icons', 'cuadradoFeliz.png') ),

    'background':
    ( dir_sprites.joinpath('background.png') ),
    
    'stone':
    ( dir_sprites.joinpath('floor/stone.png') ),
    
    'ladder':
    ( dir_sprites.joinpath('floor/ladder.png') ),
    
    'trampoline':
    ( dir_sprites.joinpath('floor/trampoline.png') ),
    
    'elevator':
    ( dir_sprites.joinpath('floor/elevator.png') ),
    
    'level_change':
    ( dir_sprites.joinpath('floor/level_change.png') ),
    
    'spike':
    ( dir_sprites.joinpath('spikes/spike.png')),
    
    'star-pointed':
    ( dir_sprites.joinpath('spikes/star-pointed.png') ),
    
    'rain':
    ( dir_sprites.joinpath('climate/rain.png' ) ),
    
    'coin':
    ( dir_sprites.joinpath('items/coin.png') ),
    

    'cloud-1':
    ( dir_sprites.joinpath(f'climate/clouds/cloud-1.png') ),
    
    'cloud-2':
    ( dir_sprites.joinpath(f'climate/clouds/cloud-2.png') ),
    
    'cloud-3':
    ( dir_sprites.joinpath(f'climate/clouds/cloud-3.png') ),
    

    'player_not-move':
    ( dir_sprites.joinpath('player/player_not-move.png') ) ,
    
    'player_move':
    ( dir_sprites.joinpath('player/player_move.png') ) ,
}




def get_image( 
    image=str, number=int, size=[int, int], color=[int,int,int], transparency=int, 
    return_method='auto', flip_x=False, flip_y=False, colored_method='normal', 
    ):
    go = False
    for key in all_images.keys():
        if key == image:
            go = True

    if go == True:
        try:
            image = pygame.image.load( all_images[image] ).convert_alpha()
        except:
            image = pygame.image.load( all_images[image] )
        if flip_x == True or flip_y == True:
            image = pygame.transform.flip(image, flip_x, flip_y)
        
        list_mode = False
        if return_method == 'auto':
            rect = image.get_rect()
            if rect.width != rect.height:
                list_mode = True
        elif return_method == 'anim':
            list_mode = True
        
        # Cambiar color o no
        if isinstance(color, list) or isinstance(color, tuple):
            good_values = False
            if len(color) == 3:
                good_values = True
                for value in color:
                    if isinstance(value, int):
                        if not value >= 0 and value <= 255:
                            good_values = False
                    else:
                        good_values = False
            if good_values == True:
                if colored_method == 'surface':
                    colorImage = pygame.Surface( image.get_size()).convert_alpha()
                    colorImage.fill( color )
                    image.blit(colorImage, (0,0), special_flags = pygame.BLEND_MULT)
                else:
                    image.fill( color, special_flags=pygame.BLEND_ADD)
        
        # Cambiar transparencia o no
        if isinstance(transparency, int):
            if transparency <= 255 or transparency >= 0:
                image.set_alpha( transparency )
        
        # Reescalar o no
        resize = False
        if type(size) == list or type(size) == tuple:
            if len(size) == 2:
                if type(size[0]) == int and type(size[1]) == int:
                    resize = True
        
        # Si la imagen es una animacion o no
        if list_mode == True:
            # Cargar imagenes
            image = Anim_sprite_set( sprite_sheet=image )

        
        # Redimensionar imagenes, dependiendo si es animacion o imagen
        if resize == True:
            if list_mode == True:
                for frame in range(0, len(image) ):
                    image[frame] = pygame.transform.scale(
                        image[frame], size
                    )
    
            else:
                image = pygame.transform.scale( image, size )
                
        # Etablecer frame o no
        if list_mode == True:
            if isinstance( number, int):
                if number <= len(image)-1 and number >= 0:
                    image = image[number]
                else:
                    image = random.choice( image )
        
        
        # Devolver imagen o lista de imagenes/animacion
        return image





def get_number(number=int):
    limit_max = max(data_CF.disp)
    limit_min = 2
    
    if number > limit_max:
        number = limit_max
    elif nunber < limit_min:
        number = limit_min
    
    return number





player_key = {
    'jump': pygame.K_SPACE,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'walk': pygame.K_LSHIFT,
    'action': pygame.K_a
}




def scroll_display_collision( 
        pos_xy=[int,int], scroll_xy=[int, int], display_xy=[int, int], 
        more_pixels_positive_negative=[0,0], 
    ) -> str:
    '''
    Detectar que el sprite no sebrepase la pantalla, se necesita de una camara funcionando con el metodo "scroll".
    Donde scroll es una lista de xy de enteros.
    '''
    side = None
    if pos_xy[0]-scroll_xy[0] < 0 -more_pixels_positive_negative[0]:
        side = 'left'
    elif pos_xy[0]-scroll_xy[0] > display_xy[0] +more_pixels_positive_negative[1]:
        side = 'right'
        
    if pos_xy[1]-scroll_xy[1] < 0 -more_pixels_positive_negative[0]:
        side = 'top'
    elif pos_xy[1]-scroll_xy[1] > display_xy[1] +more_pixels_positive_negative[1]:
        side = 'bottom'
    
    return side





def detect_camera_limit(
    limit_xy=[int,int], moving_xy=[int,int], camera_xy=[int,int], camera_spawn_xy=[int,int], 
    scroll_float=[float,float], not_scroll_xy=[bool,bool], grid_square=int, disp_xy=[int,int]
    ) -> bool:
    '''
    Función objetos que limitan la camara/scroll, para detectar la posición del limite y detectar si el scroll esta sobrepasando el limite y entonces parar el scroll.
    
    limit_xy = coordenadas xy de objeto tipo limite de camara.
    camera_xy = coordenadas xy de camara/player
    moving_xy = coordenadas xy de movimiento del objeto camara/player
    '''
    # Limite positivo x
    if limit_xy[0] >= disp_xy[0]:
        if scroll_float[0] >= limit_xy[0]-(disp_xy[0]):
            if moving_xy[0] < 0:
                # Cuando quiere salir del limite positivo
                if not camera_xy[0] <= limit_xy[0]-(disp_xy[0]/2):
                    not_scroll_xy[0] = True
            else:
                # Cuando llega al limite positivo
                not_scroll_xy[0] = True
                
    # Limite negativo x
    if limit_xy[0] <= 0:
        if scroll_float[0] <= limit_xy[0]:
            if moving_xy[0] > 0:
                # Cuando quiere salir del limite negativo
                if not camera_xy[0] >= limit_xy[0]+(disp_xy[0]/2):
                    not_scroll_xy[0] = True
            else:
                # Cuando llega al limite negativo
                not_scroll_xy[0] = True
    
    
    # Limite positivo y
    if limit_xy[1] >= disp_xy[1]-grid_square:
        if scroll_float[1] >= limit_xy[1]-(disp_xy[1]):
            if moving_xy[1] < 0:
                # Cuando quiere salir del limite positivo
                if not camera_xy[1] <= limit_xy[1]-(disp_xy[1]/2):
                    not_scroll_xy[1] = True
            else:
                # Cuando llega al limite positivo
                not_scroll_xy[1] = True
                
    # Limite negativo y
    if limit_xy[1] <= 0:
        if scroll_float[1] <= limit_xy[1]:
            if moving_xy[1] > 0:
                # Cuando quiere salir del limite negativo
                if not camera_xy[1] >= limit_xy[1]+(disp_xy[1]/2):
                    not_scroll_xy[1] = True
            else:
                # Cuando llega al limite negativo
                not_scroll_xy[1] = True

    # Restablecer camara al spawn
    # volver a anlizar los limites, para que se acomode al 100% bien
    if camera_xy[1] == camera_spawn_xy[0] and camera_xy[1] == camera_spawn_xy[1]:
        not_scroll_xy = [False, False]
    
    # Devolver el mover el scroll en x o en y.
    return not_scroll_xy





def get_coordinate_multipler( multipler=int, pixel_space=int, position=[int,int] ):
    new_size = (pixel_space*multipler, pixel_space*multipler )
    aditional_pos = ( (pixel_space*multipler)-( (pixel_space*multipler) /2) )-pixel_space//2
    new_position=[ 
        position[0] +aditional_pos,  position[1] +aditional_pos
    ]
    return [new_size, new_position]




# Funcion del clima
def divider_color_rgb( 
        color=[255,255,255], divider=2, alpha=255, min_value_multipler=0, 
        most_to_least=True, from_zero=False, int_value=True
    ):
    '''
    Dividir un color rgb, en varios colores rgb.
    
    Argumentos
        color = [int, int, int] (min 0, max 255)
        divider = int
        alpha = int ; Valor de transparencia. Por defecto 255
        min_value_multipler ; Multiplicador del valor minimo. Por defecto 0.
        most_to_least = bool ; Para hacer la lista de mayor a menor o de menor a mayor.
        from_zero = bool ; Para determinar si el valor se saltara el primer o el ultimo valor.
        int_value = bool ; Para devolver un numero entero si o si.
    
    Devulve:
        Una lista con listas de tres items.
        Ejemplo: [ [0,0,0] ]
    '''
    # Dividir cada valor del rgb
    r = stepped_number_sequence(
        [color[0], color[0]*min_value_multipler], divider=divider,
        most_to_least=most_to_least, from_zero=from_zero, int_value=int_value 
    )
    g = stepped_number_sequence(
        [color[1], color[1]*min_value_multipler], divider=divider,
        most_to_least=most_to_least, from_zero=from_zero, int_value=int_value 
    )
    b = stepped_number_sequence( 
        [color[2], color[2]*min_value_multipler], divider=divider,
        most_to_least=most_to_least, from_zero=from_zero, int_value=int_value 
    )
    
    # Asignar cada valor del rgb
    list_color = []
    for x in range(divider):
        #list_color.append( [ r[x], g[x], b[x] ] )
        list_color.append( [ r[x], g[x], b[x], alpha ] )
    return list_color



class GradiantColor():
    def __init__ (
        self, color=[255,255,255], transparency=255, divider=2, start_with_max_power=False, time=0
    ):
        super().__init__()
        
        # Lista de colores
        self.__divider = divider # Divisor de colores/cantidad de indices.
        self.__transparency = transparency
        self.__start_with_max_power = start_with_max_power
        self.color = color
        self.__color_list = divider_color_rgb( 
            color=self.color, divider=self.__divider, 
            alpha=self.__transparency, most_to_least=self.__start_with_max_power
        )
        

        self.time = time # Tiempo para que se realice cada cambio.
        
        # Contador de tiempo, indice de lista de color.
        self.count = 0
        self.index = 0

        # Color actual, color de inicio, color final
        self.current_color = self.__color_list[ self.index ]
        self.start_color = self.__color_list[ 0 ]
        self.end_color = self.__color_list[ self.__divider-1 ]
        
        # Invert es para poner los indices de menos a mas o de mas a menos.
        self.invert = False

    def update(self):
        '''
        Cambia de color, 
        invert False, hace que el index de la lista sea de menor a mayor
        invert True, hace que el index de la lista sea de mayor a menor
        '''
        self.count += 1
        if self.count >= self.time:
            self.count = 0
            self.current_color = self.__color_list[self.index]

            if self.invert == False:
                self.index += 1
                if self.index >= self.__divider:
                    self.index = self.__divider-1
                    self.invert = True
            elif self.invert == True:
                self.index -= 1
                if self.index <= 0:
                    self.index = 0
                    self.invert = False

    def restart(self):
        '''
        Restablecer valores de inicio. Se empezara de 0
        '''
        # Colores
        self.__color_list = divider_color_rgb( 
            color=self.color, divider=self.__divider, 
            alpha=self.__transparency, most_to_least=self.__start_with_max_power
        )
        
        # Contador de tiempo, indice de lista de color.
        self.count = 0
        self.index = 0

        # Color actual, color de inicio, color final
        self.current_color = self.__color_list[ self.index ]
        self.start_color = self.__color_list[ 0 ]
        self.end_color = self.__color_list[ self.__divider-1 ]
        
        # Invert es para poner los indices de menos a mas o de mas a menos.
        self.invert = False




def collide_and_move( obj=None, obj_movement=[0,0], solid_objects=None):
    '''
    Esta función collisiona y mueve un objeto tipo "pygame.sprite.Sprite()"
    
    Para esta función se necesita del siguiente objeto, con estos atributos:
    Objeto tipo "pygame.sprite.Sprite"
    self.rect
    Este objeto lo utilizaremos para el parametro:
    obj=objeto

    Tambien se necesita una lista de dos valores, que haran la función de movimiento del jugador.
    obj_movement = [0, 0]
    El primer valor de la lista seria el movimiento "x" y el segundo valor de la lista el movimiento "y"
    
    solid_objects, es una lista de objetos que teinen los siguientes atributos:
    Objetos tipo pygame.sprite.Sprite()
    self.rect
    solid_objects = lista_de_objetos
    


    Cuando "obj" colisione con algun "solid_objects", dependiendo de la dirección de su colision, el "obj" se posicionara de forma inversa a la dirección de colisión.
    Primero obj se mueve en dirección "x" si obj_movement[0] es menor o meyor a cero.
    Y se determina lo siguiente:
    - Si obj colisiona del lado derecho del solid_object, este se movera a su lado izquierdo.
    - Si obj colisiona del lado izquiedo del solid_object, este se movera a su lado derecho.
    
    Despues obj se mueve en dirección "y" si obj_movement[1] es menor o meyor a cero, y se determina lo siguiente:
    Y se determina lo siguiente:
    - Si obj colisiona del lado inferior del solid_object, este se movera a su lado superior.
    - Si obj colisiona del lado superior del solid_object, este se movera a su lado inferior.
    '''
    collided_side = None
    solid_collide_x = None # Esto es para Forzar posicion arriba

    # Colisiones en eje x
    obj.rect.x += obj_movement[0]
    for solid in solid_objects:
        if (
            obj.rect.height <= solid.rect.height and # Para solidos mas pequños que el obj
            obj.rect.colliderect( solid.rect )
        ):
            if obj_movement[0] > 0:
                obj.rect.right = solid.rect.left
                collided_side = 'right'
            elif obj_movement[0] < 0:
                obj.rect.left = solid.rect.right
                collided_side = 'left'
            
            # Esto es para Forzar posicion arriba
            if isinstance(collided_side, str):
                solid_collide_x = solid
    
    # Colisiones en eje y
    obj.rect.y += obj_movement[1]
    for solid in solid_objects:
        if obj.rect.colliderect( solid.rect ):
            if obj_movement[1] > 0:
                obj.rect.bottom = solid.rect.top
                collided_side = 'bottom'
            elif (
                obj.rect.height <= solid.rect.height and # Para solidos mas pequeños que el obj, esto hace que no se colisione abajo
                obj_movement[1] < 0
            ):
                obj.rect.top = solid.rect.bottom
                collided_side = 'top'
    
    # Forzar posicion arriba | Sirve para establecer en el piso al obj, si el obj esta lo suficientemente arriba como para forzar estarlo arriba.
    if not solid_collide_x == None:
        if obj.rect.y < solid_collide_x.rect.y -(obj.rect.height*0.5):
            obj.rect.bottom = solid_collide_x.rect.top
            collided_side = 'bottom'
                    
    
    return collided_side





def segment_value( full_value, max_value  ) -> list:
    '''
    Partir un numero "full_value" que es mayor que "max_value"
    
    full_value = int, float
    max_value = int, float
    '''
    # Determinar diviciones si full_value es mayor que max_value
    if full_value > max_value:
        parts_value = [max_value]

        while full_value > 0:
            full_value -= max_value

            # Agregar valores partes
            if full_value > 0:
                if full_value >= max_value:
                    parts_value.append( max_value )
                else:
                    parts_value.append( full_value )

        return parts_value
    else:
        return []
        #raise ValueError("full_value tiene que ser mayor que max_value.")




def surf_limit_width( surf, limit_widht ) -> list:
    '''
    Limitar el ancho de un surf, y dividirlo en partes no mas grandes que el limite del ancho.
    Depende de la funcion "segment_value"
    
    surf = pygame.Surface(), pygame.image.load(), pygame.font()
    limit_widht = int
    '''
    # Mensaje tiene surf rect y anchura de mansaje
    rect = surf.get_rect()
    full_widht = rect.width

    # Determinar diviciones de surf si sobrepasa la pantalla. En base al limit_width
    parts_size = []

    list_size = segment_value( full_widht, limit_widht )    
    for x in range( len(list_size) ):
        parts_size.append( 
            surf.subsurface(
                ( x*limit_widht, 0, list_size[x], rect.height ) 
            )
        )
    
    return parts_size




def stepped_number_sequence(
        number_range=[256,0], divider=8, most_to_least=True, from_zero=True, int_value=True 
    ):
    '''
    Listar un numero de mas a menos o de menos a mas. 
    En esta función siempre queda un valor suelto, ya sea el rango max o el min.
    
    Donde en el number_range el indice 0 es mayor que el indice 1.
    Divisior indica la cantidad de numeros en la lista.
    
    El operación necesaria es: (number_range[0]/divisor) -number_range[1]/divisor
    Donde el indice 0 es mayor que el indice 1.
    Esta operación sirve para saber cuanto restar, o cuanto agregar
    
    Argumentos:
        number_range = [int, int]   # Max, Min default(256,0)
        divider = int               # Para hacer la lista, cantidad de indices con valores determinados por el rango.
        most_to_least = bool        # Determinar si ir de mas a menos, o de menos a mas.
        from_zero = bool            # Terminar en el fin execto o no.
        int_value = bool            # Determinar si los valores de la lista seran enteros o no.

    Return:
        list[] # Con divider cantidad de indices.
    '''
    return_list = [] # Lista a devolver

    # Los ejempos que se veran serian; si divider = 8, range = [256,128]
    # Valor necesario. Se usa para restar | Operar en el bucle
    necessary_value = (number_range[0]/divider)
    if number_range[1] > 0:
        necessary_value -= (number_range[1]/divider)
    
    # Determinar si inicia en cero o no.
    if from_zero == True:   initial_value = 0
    else:                   initial_value = 1
    
    # Bucle
    for i in range(0, divider):
        if most_to_least == True:
            # Restar, si ya esta o ya paso el para valor inicial
            # De mas a menos
            if i >= initial_value:
                # 256 -(32-16)
                number_range[0] -= necessary_value
                value_to_add = number_range[0]
            else:
                value_to_add = number_range[0]
        else:
            # De menos a mas
            # 256 - (32-16)*8
            value_to_add = number_range[0] -( necessary_value*(divider-i-initial_value) )
        
        # Agregar a la lista
        if int_value == True:   return_list.append( int(value_to_add) )
        else:                   return_list.append( value_to_add )
    
    
    return return_list # Devolver lista

cocos = stepped_number_sequence([512, 0], 8, most_to_least=True, from_zero=True)
print( cocos )
print( len( cocos ) )

espuma = stepped_number_sequence([1920, 0], 8, most_to_least=False, from_zero=True)
print( espuma )
print( len( espuma ) )




def surface_gradient( size=[32,32], alpha_range=[255,0], color=[0,0,0], dimension=0, positive=True ):
    '''
    Crear un gradiante, que sera una superficie chida, con degradado excitante.

    size = [0,0] # Tamaño xy del gradiante
    alpha_range = [255, 0] # Valor inicial y final del gradiante
    color = [0,0,0] # Color del gradiante
    dimension=int, # Dimención donde se hara el gradiante.
    positive=bool, # Gradiante de mas a menos, o de menos a mas.
    
    return pygame.Surface()
    '''
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Determinar multiplicador y adición por la dimensión establecida.
    if positive == True:
        multipler = -1
        addition = 1
    else:
        multipler = 1
        addition = 0
    
    
    # Degradado
    #alpha_values = stepped_number_sequence(
    #    alpha_range, divider=size[dimension], most_to_least=positive, from_zero=True, int_value=True
    #)
    #print(alpha_values)
    for d in range(size[dimension]):
        #alpha = alpha_values[d]

        alpha = int(
            ( alpha_range[0] -alpha_range[1] ) * ( addition + ( multipler*(d / (size[dimension]-1) ) ) )
        )  
        if dimension == 0:
            pygame.draw.line(
                surface, (color[0], color[1], color[2], alpha), (d, 0), (d, size[1])
            )
        elif dimension == 1:
            pygame.draw.line(
                surface, (color[0], color[1], color[2], alpha), (0,d), (size[0], d)
            )
    

    # Devolver superficie
    return surface




def create_mask_gradient(sprite, alpha_range=[255, 0], color=[0,0,0], dimension=0, positive=True ):
    """
    Crear un gradiante, que sera una maskara chida, con degradado excitante. Es una superficie individual
    Depende de surface_gradient

    sprite = pygame.Surface() # Superficie de pygame
    color = [0,0,0] # RGB color
    dimension=int # Dimencion donde se hara el gradiante.
    positive=bool # Gradiante de mas a menos, o de menos a mas.
    
    return pygame.Surface()
    """
    # Obtener datos necesarios, inciar objetos necesarios
    mask = pygame.mask.from_surface(sprite)  
    width, height = sprite.get_size()
    size = [width, height]
    
    # Degradado
    surf_grad = surface_gradient( size, alpha_range, color, dimension, positive )


    # Para que siga la forma del sprite.
    # Aplicar la máscara para que la sombra siga la forma del sprite
    shadow_mask = mask.to_surface(setcolor=(color[0], color[1], color[2], 255), unsetcolor=(0, 0, 0, 0))  
    shadow_mask.set_colorkey((0, 0, 0))  
    surf_grad.blit(shadow_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  



    return surf_grad  # Retorna solo la sombra, sin tocar el sprite
    



def surface_bloom( size=[32,32], alpha_range=[255, 0], color=[0,0,0], middle_color=True ):
    '''
    Pone alrededor de un cuadrado, gradiantes en dirección de los lados. Gradiantes de mas a menos.
    Depende de surface_gradient
    
    size = [0,0] # Tamaño xy
    alpha_range = [255, 0] # Valor inicial y valor final del gradiante.
    color = bool # Color del bloom
    middle_color = bool # Color en el medio del bloom.
    
    return pygame.Surface()
    '''
    # Establecer el surface a devolver
    final_size = [size[0]*3, size[1]*3]
    surface_final = pygame.Surface( final_size, pygame.SRCALPHA)
    if middle_color == True:  
        surf_middle = pygame.Surface( size, pygame.SRCALPHA)
        surf_middle.fill( color )
        surf_middle.set_alpha( alpha_range[0] )
        surface_final.blit( surf_middle, [size[0],size[1]] )

    # Generar cuatro gradianes alrederdor de los lados del size
    for part in range(4):
        # Mover de positivo a negativo o de negativo a positivo
        if part == 0 or part == 2:  positive = True
        else:                       positive = False
        
        # Dimension del gradiante
        if part == 0 or part == 1:  dimension = 0
        if part == 2 or part == 3:  dimension = 1
        
        # Posición
        if part == 0:       position = [size[0]*2, size[1]]
        elif part == 1:     position = [0, size[1]]
        elif part == 2:     position = [size[0], size[1]*2]
        elif part == 3:     position = [size[0], 0]
        
        surf_grad = surface_gradient(
            size, [ alpha_range[0], alpha_range[1] ], color, dimension, positive
        )
        
        surface_final.blit( surf_grad, position )
    
    # Devolver surface.
    return surface_final




def speed2d_with_angle( speed, angle ):
    speed_xy = [ speed *math.cos(math.radians(angle)),  -speed *math.sin(math.radians(angle)) ]
    # math.radians(), Convierte angulos a radianes
    # math.cos, funcion coseno.
    # math.sin, función seno.
    # x = speed * cos(angle)
    # y = speed * sin(angle)
    # Coseno de cero es uno y seno de cero es cero. Por eso en el angulo cero; xy=[4,0]
    
    return speed_xy