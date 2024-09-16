'''
Funciones especificamente para el juego Cuadrado Feliz
'''
from data.CF_info import *
from data.CF_data import *
from logic.Modulo_Text import *
from logic.pygame.Modulo_pygame import *
import pygame, os, random




# Sonidos
all_sounds = {
    'steps':
    [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-1.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-2.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-3.ogg') )
    ],
    
    'hits': [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-1.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-2.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-3.ogg') )
    ],
    
    'jump': pygame.mixer.Sound(os.path.join(dir_audio, 'effects/jump.ogg') ),
    
    'dead': [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-1.ogg' ) ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-2.ogg' ) ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-3.ogg' ) )
    ],
    
    'score': [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/items/score-1.ogg' ) ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/items/score-2.ogg' ) ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/items/score-3.ogg' ) )
    ]
}
for key in all_sounds.keys():
    sound_or_sounds = all_sounds[key]
    if type( sound_or_sounds ) == list:
        for sound in sound_or_sounds:
            sound.set_volume( data_CF.volume )
    else:
        sound_or_sounds.set_volume( data_CF.volume )




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
    'background':
    ( os.path.join(dir_sprites, 'background.png') ),
    
    'stone':
    ( os.path.join(dir_sprites, 'floor/stone.png') ),
    
    'ladder':
    ( os.path.join(dir_sprites, 'floor/ladder.png') ),
    
    'trampoline':
    ( os.path.join(dir_sprites, 'floor/trampoline.png') ),
    
    'elevator':
    ( os.path.join(dir_sprites, 'floor/elevator.png') ),
    
    'level_change':
    ( os.path.join(dir_sprites, 'floor/level_change.png') ),
    
    'spike':
    ( os.path.join(dir_sprites, 'spikes/spike.png')),
    
    'star-pointed':
    ['anim', ( os.path.join(dir_sprites, 'spikes/star-pointed.png') ) ],
    
    'rain':
    ( os.path.join(dir_sprites, 'climate/rain.png' ) ),
    
    'coin':
    ( os.path.join(dir_sprites, 'items/coin.png') ),
    
    'clouds':
    [
        ( os.path.join(dir_sprites, f'climate/clouds/cloud-1.png') ),
        ( os.path.join(dir_sprites, f'climate/clouds/cloud-2.png') ),
        ( os.path.join(dir_sprites, f'climate/clouds/cloud-3.png') )
    ],
    
    'player_not-move':
    ['anim', ( os.path.join(dir_sprites, 'player/player_not-move.png') ) ],
    
    'player_move':
    ['anim', ( os.path.join(dir_sprites, 'player/player_move.png') ) ],
}




def get_image( image=str, number=int, size=[int, int] ):
    go = False
    for key in all_images.keys():
        if key == image:
            go = True

    if go == True:
        image = all_images[image]
        
        # Reescalar o no
        resize = False
        if type(size) == list:
            if len(size) == 2:
                if type(size[0]) == int and type(size[1]) == int:
                    resize = True
        
        # Si la imagen es una animacion o no
        list_mode = False
        if type(image) == list:
            list_mode = True
            # Cargar imagenes
            if image[0] == 'anim':
                image = Anim_sprite_set( sprite_sheet=pygame.image.load( image[1] ).convert_alpha() )
            else:
                list_images = []
                for frame in range(0, len(image) ):
                    list_images.append( pygame.image.load( image[frame] ).convert_alpha() )
                image = list_images

        else:
            # Cargar imagen
            image = pygame.image.load( image )

        
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
            if number <= len(image)-1 and number >= 0:
                image = image[number]
            else:
                image = rendom.choice( image )
        
        
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
    'right': pygame.K_RIGHT
}