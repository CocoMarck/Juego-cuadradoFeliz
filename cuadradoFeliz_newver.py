from logic.Modulo_Text import (Text_Read, Ignore_Comment, Only_Comment)
from data import Modulo_Language as Lang
from logic.pygame.Modulo_pygame import *
from data.CF_info import *
from data.CF_data import *
from entities import Map, CF
from logic.pygame.CF_object_newver import *

import time
import pygame, sys, os, random
from pygame.locals import *

# Resolución de pantalla de juego
disp_resolution = ( data_CF.disp[0], data_CF.disp[1] )
display = pygame.display.set_mode( disp_resolution )

# Fotogramas del juego
clock = pygame.time.Clock()

# Titulo del juego
pygame.display.set_caption(game_title)

# Audio | Musica de fondo
#...

# Fuentes de texto
size_font_big = int(data_CF.pixel_space*4)
size_font_normal = data_CF.pixel_space
font_str = 'monospace'
font_normal = pygame.font.SysFont(font_str, size_font_normal)
font_big = pygame.font.SysFont(font_str, size_font_big)

# Fondo
if data_CF.show_sprite == True:
    image_background = get_image('background', size=data_CF.disp, return_method='normal')
else:
    image_background = pygame.Surface( (data_CF.disp[0], data_CF.disp[1]) )
    image_background.fill( (63, 63, 63) )
color_background = pygame.Surface( (data_CF.disp[0], data_CF.disp[1]), pygame.SRCALPHA )




# Map
'''
Nota:
Los objetos en vez de posicionar el rect con "lefttop", se hace con "center", lo cual no es lo adecuado, seria bueno cambiarlo (probablemente se tararia un poco menos el renderizado y seria mas facil el manejo de este).
'''
class Start_Map( ):
    def __init__(self, Map):
        super().__init__()
        
        # Atributos necesarios
        self.player_spawn = [0,0]

        # Renderizar mapa
        xy = [0,0]
        for line in Map.list_map:
            xy[0] = 0
            position = [ xy[0], xy[1]*data_CF.pixel_space ]
            xy[1] += 1
            
            for character in line:
                position[0] = xy[0]*data_CF.pixel_space
                
                xy[0] += 1

                # Jugador
                if character == 'j':
                    self.player_spawn = [ position[0], position[1] ]
                
                
                
                
                # Objetos solidos/saltarines/monedas/checkpoint, no dañinos
                elif character == 'p':
                    # Objeto plataforma Piso Floor
                    Floor(
                        size=(data_CF.pixel_space, data_CF.pixel_space),
                        position=position, climate=Map.climate,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                elif character == 'P':
                    # Posicionar de forma adecuada
                    new_size_pos = get_coordinate_multipler( 
                        multipler=2, pixel_space=data_CF.pixel_space, position=position 
                    )
                    new_size_pos[1] = position
                
                    # Objeto plataforma Piso Floor
                    Floor(
                        size=new_size_pos[0], position=new_size_pos[1], climate=Map.climate,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                
                elif character == 's':
                    Score( 
                        size=data_CF.pixel_space, position=position, 
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == '+':
                    Stair(
                        size=data_CF.pixel_space, position=position, invert=False,
                        climate=Map.climate, show_collide=data_CF.show_collide
                    )
                    
                elif character == '-':
                    Stair(
                        size=data_CF.pixel_space, position=position, invert=True,
                        climate=Map.climate, show_collide=data_CF.show_collide
                    )

                elif character == 'H':
                    Ladder(
                        size=data_CF.pixel_space, position=position,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == '_':
                    Trampoline(
                        size=data_CF.pixel_space, position=position,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == 'x':
                    Elevator(
                        size=data_CF.pixel_space, position=position, move_dimension=1,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == 'y':
                    Elevator(
                        size=data_CF.pixel_space, position=position, move_dimension=2,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == '~':
                    Climate_rain(
                        position=position,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )

                elif character == '0':
                    level = Level_change(
                        dir_level=Map.path, level=Map.next_level, position=position, 
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == 'F':
                    Level_change(
                        dir_level=Map.path, level=Map.next_level, position=position, gamecomplete=True,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                
                
                
                
                # Limite del mapa
                elif character == '|':
                    Limit_indicator(
                        position=position, show_collide=data_CF.show_collide
                    )
                
                
                
                # Objetos dañinos
                elif character == '^':
                    spike = Spike( 
                        position=position,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == 'A':
                    # Objeto pico
                    Spike(
                        size=data_CF.pixel_space*2, position=position,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == '\\':
                    Spike( 
                        position=position, moving=True, instakill=True,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )

                elif character == '!':
                    Spike( 
                        position=position, instakill=True,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
                    
                elif character == 'Y':
                    Star_pointed(
                        position=position,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )

                elif character == '*':
                    Star_pointed(
                        position=position, moving=True, instakill=True,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )

                elif character == 'X':
                    Star_pointed(
                        position=position, instakill=True,
                        show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                    )
        



        # Sección generación de clima
        if Map.climate == 'rain':
            print(xy)
            rain_multipler = 2
            for generate_number in range(0, rain_multipler):
                if xy[0] > 0:
                    more_distance_xy = [4, 0]
                    for x in range( more_distance_xy[0], xy[0]+(xy[1]//2)+more_distance_xy[0] ):
                        Climate_rain(
                            position=(
                                random.randint( x*data_CF.pixel_space, x*(data_CF.pixel_space*4) ),
                                -( random.randint( data_CF.pixel_space, data_CF.pixel_space*16) )
                            ),
                            show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite
                        )
 
current_map = Map
read_Map( Map=current_map, level=data_CF.current_level )
render_map = Start_Map(current_map)
player = Player(
    position=render_map.player_spawn,
    show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite 
)
player_spawn_hp = player.hp
player_anim_dead = None




# Loop dia y noche | Fondo de color de clima
def get_climate( Map ):
    if Map.climate in dict_climate.keys():
        return Map.climate
    else:
        return 'default'

def Loop_allday( Map ):
    climate = get_climate( Map )
    gradiant_color = GradiantColor( 
        color=dict_climate[climate], transparency=127, divider=16, start_with_max_power=True, time=data_CF.fps*120
    )
    gradiant_color.climate=climate
    return gradiant_color

loop_allday = Loop_allday( current_map )

background_surf = pygame.Surface( data_CF.disp, pygame.SRCALPHA )
background_surf.fill( loop_allday.current_color )



# Funcion Musica
# Crear un evento personalizado para el final de la pista
end_of_track_event = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(end_of_track_event)


# Nota: Tienen que ser directorios de archivo, no objetos Sound
class Play_background_music():
    def __init__(self, music=data_CF.music, climate=f'climate_{Map.climate}' ):
        self.climate = climate
        self.music = music
        self.list_music = []
        self.update_list_music()


    def update_list_music(self):
        if self.list_music == []:
            for key in all_music.keys():
                if not key.startswith('climate_'):
                    self.list_music.append( all_music[key])

    def play(self):
        current_music = None
        if self.music == True:
            # Reproducir musica y clima
            self.update_list_music()
            if isinstance(self.list_music, list):
                current_music = random.choice( self.list_music )
                self.list_music.remove(current_music)
            else:
                self.list_music = all_music['music']
        else:
            # Solo reproducir el clima
            for key in all_music.keys():
                if self.climate == key:
                    current_music = all_music[self.climate]
        
        # Cagar y reproducir cancion
        if isinstance(current_music, str):
            pygame.mixer.music.load( current_music )
            pygame.mixer.music.set_volume( data_CF.volume )
            pygame.mixer.music.play()
play_background_music = Play_background_music( music=data_CF.music, climate=f'climate_{Map.climate}' )
play_background_music.play()


class Play_Music():
    def __init__(self, music=data_CF.music, climate=None, climate_sound=data_CF.climate_sound ):
        # Para reproducir musica en el juegito
        self.list_music = [
            [os.path.join(dir_audio, 'music/default-music.ogg'), 4],
            [os.path.join(dir_audio, 'music/music-party.ogg'), 8],
            #[os.path.join(dir_audio, 'music/music-cover.ogg'), 1],

            [os.path.join(dir_audio, 'music/music-test1.ogg'), 1],
            [os.path.join(dir_audio, 'music/music-test2.ogg'), 2],
            [os.path.join(dir_audio, 'music/music-test3.ogg'), 2],
            [os.path.join(dir_audio, 'music/music-test4.ogg'), 2],
            [os.path.join(dir_audio, 'music/music-test5.ogg'), 1]
        ]

        self.climate_sound = climate_sound
        self.__go = False
        self.music = music
        self.climate = climate
        self.limit_music = 0
        self.__limit_music_climate = 8
        self.play()
        
    def set_climate(self):
        if self.climate == 'rain':
            return os.path.join(dir_audio, 'music/climate_rain.ogg')
        if self.climate == 'alien':
            return os.path.join(dir_audio, 'music/climate_alien.ogg')
        if self.climate == 'sunny':
            return os.path.join(dir_audio, 'music/climate_sunny.ogg')
        if self.climate == 'black':
            return os.path.join(dir_audio, 'music/climate_black.ogg')
        else:
            return os.path.join(dir_audio, 'music/climate_default.ogg')
    
    def play(self):
        # Reproducir musica o sonido del silencio/ambiente.
        if self.climate_sound == True:
            self.__go = random.choice( [True, 2, 3] )
        else:
            if self.music == True:
                self.__go = True
            else:
                self.__go = False
        
        # Reproducir musica o no
        if self.__go == True and self.music == True:
            # Cuando se puede reproducir musica.
            music_ready = random.choice(self.list_music)
            music = music_ready[0]
            self.limit_music = music_ready[1]
        else:
            # Sonido del silencio/ambiente
            music = self.set_climate()
            self.limit_music = self.__limit_music_climate
        pygame.mixer.music.load( music )
        pygame.mixer.music.set_volume( data_CF.volume )
        pygame.mixer.music.play()
        
        return self.limit_music
        
    def change_climate(self, climate=None):
        self.climate = climate
        if not self.__go == True:
            music = self.set_climate()
            pygame.mixer.music.load( music )
            pygame.mixer.music.set_volume( data_CF.volume )
            pygame.mixer.music.play()
            self.limit_music = self.__limit_music_climate


# Función nubes de fondo
def create_clouds(c_number = 15):
    '''
    Imagenes de fondo | Nubes de fondo
    # Si hay demasiadas nubes se dejaran de crear.
    # Se creara una nube de forma random, con posibilidades 1-6
    '''
    c_sizex = data_CF.disp[0]//c_number
    c_sizey = data_CF.disp[1]//c_number
    c_size = (c_sizex, c_sizey)

    clouds = 0
    for y in range(0, c_number):
        posy = c_sizey*(y)
        for x in range(0, c_number):
            posx = c_sizex*(x)

            create = random.choice( [True, 2, 3, 4, 5, 6] )
            if create == True:
                clouds += 1
                Cloud(
                    size=c_size, position=(posx, posy),
                    show_collide=data_CF.show_collide
                )




# Iniciar Funciones y contantes necesarias
# Funcion nubes
if data_CF.show_clouds == True:
    create_clouds()

# Funcion | Dia y noche
'''
loop_allday = Loop_allday(climate=start_map.climate)
count_fps_day = loop_allday.count_fps_day
color_day = loop_allday.color_day
color_day_red = loop_allday.color_day_red
color_day_green = loop_allday.color_day_green
color_day_blue = loop_allday.color_day_blue
color_change = loop_allday.color_change
changes_day = loop_allday.changes_day
is_night = loop_allday.is_night
'''

# Funcion musica
'''
play_music = Play_Music( climate=start_map.climate )
count_playmusic = 0
limit_playmusic = play_music.limit_music
'''


# Funcion del mapa
score = 0

for plat in solid_objects:
    plat.limit_collision()

# Funcion juego completado
gamecomplete = False

# Función cretidos
credits = False
credits_fps = data_CF.fps*4
credits_count = 0




# Función camara / Scroll
def get_limit_xy():
    '''
    Limite del mapa
    '''
    pos_x = []
    pos_y = []
    #for sprite in layer_all_sprites.sprites():
    for sprite in limit_objects:
        pos_x.append(sprite.rect.x)
        pos_y.append(sprite.rect.y)
    return [ max(pos_x), max(pos_y)]
limit_xy = get_limit_xy()


def start_scroll( pos_xy=[0,0], display_xy=[0,0], limit_xy=[0,0], difference_xy=[0,0] ) ->[int, int]:
    xy = [0,0]
    
    # Posicionar camara, con el jugador a la der o izq, arriba o abajo
    if (pos_xy[0] + difference_xy[0] + (display_xy[0]/2)) > limit_xy[0]:
        # Jugador en la izq
        xy[0] = pos_xy[0] -(display_xy[0]/2) +difference_xy[0]
    else:
        # Jugador en la der
        xy[0] = pos_xy[0] +(display_xy[0]/2) -difference_xy[0]
    
    if (pos_xy[1] +difference_xy[1] + (display_xy[1]/2)) > limit_xy[1]:
        # Jugador abajo
        xy[1] = pos_xy[1] -(display_xy[1]/2) +difference_xy[1]
    else:
        # Jugador arriba
        xy[1] = pos_xy[1] +(display_xy[1]/2) -difference_xy[1]

    # Posicionar camara
    scroll_float = [ (xy[0] -display_xy[0]/2), (xy[1] -display_xy[1]/2) ]
    
    return [int(scroll_float[0]), int(scroll_float[1])]
scroll_float = [0,0]
scroll_float = start_scroll(
    pos_xy=[player.rect.x, player.rect.y], display_xy=data_CF.disp, limit_xy=limit_xy,
    difference_xy=[data_CF.pixel_space*2, data_CF.pixel_space*3]
)





# Bucle del juego
exec_game = True
while exec_game:
    for event in pygame.event.get():
        if event.type == end_of_track_event:
            play_background_music.play()
        if event.type == pygame.KEYDOWN:
            if event.key == player.pressed_jump:
                # Si se preciona la tecla para saltar.
                # El jugador salta si no hay mensajes
                player.jump()
            elif event.key == pygame.K_r:
                # Por si se bugea el juego, poder matar al jugador y por consecuensia reiniciar el nivel
                if not player.hp <= 0:
                    player.hp = -1
        if event.type == pygame.QUIT:
            exec_game = False
    
    
    
    
    # Fondo
    background_surf.fill( loop_allday.current_color )
    display.fill( generic_colors('green') )
    display.blit( image_background, (0,0) )
    display.blit( background_surf, (0,0) )
    loop_allday.update()




    # Jugador
    player.move()
    player.update()
    



    # Función camara / Scroll
    player_pos = [player.rect.x, player.rect.y]
    '''
    # Forzar que la camara este en buena posición
    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]  
    if player_pos[0]-scroll_int[0] > ( (data_CF.disp[0]/2)-data_CF.pixel_space ):
        scroll_float[0] += 8
    if player_pos[0]-scroll_int[0] < ( (data_CF.disp[0]/2)-data_CF.pixel_space ):
        scroll_float[0] -= 8
    '''
    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]
    diference = data_CF.pixel_space
    for index in range(0, 2):
        # en los "((data_CF.disp[index]/2) )" antes tenia "((data_CF.disp[index]/2) -data_CF.pixel_space)
        if not (
            ( player_pos[index] + ((data_CF.disp[index]/2) ) > limit_xy[index] ) or
            ( player_pos[index] - ((data_CF.disp[index]/2) ) < 0)
        ):
            # Mover scroll
            scroll_float[index] += (player_pos[index] -scroll_float[index] -data_CF.disp[index]/2)/4
        else:
            # Detectados limites de mapa/scroll | Evitar movimiento de scroll/camera
            # Nota: El limite positivo debe estar un bloque/grid/cuadricula de mas
            # more_pixels, sirve para añadir mas pixeles en el lado pistivo "x" o "y".
            #print( 'posicion jugador: ', player_pos[index])
            #print( 'posicion jugador en patalla: ', player_pos[index]-scroll_int[index])
            #print( 'scroll: ', scroll_int[index])
            #print( 'limite: ', limit_xy[index])
            #print( 'pantalla', data_CF.disp[index])
            more_pixels = data_CF.pixel_space
            if player_pos[index]-scroll_float[index] > data_CF.disp[index]/2 + more_pixels:
                aditional = limit_xy[index] -(scroll_float[index] + data_CF.disp[index])
                #if scroll_float[index] < limit_xy[index]-scroll_float[index]:
                scroll_float[index] += aditional + more_pixels
                # limite - (scroll + pantalla)
            elif player_pos[index]-scroll_float[index] < data_CF.disp[index]/2 -more_pixels:
                scroll_float[index] -= scroll_float[index]
                
    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]  
    


    # Funciones / Objetos / Puntos
    for obj in score_objects:
        if obj.point == True:
            obj.remove_point()
            score += 1

            
    # Función actualizar animacion de sprites.
    for sprite in anim_sprites:
        sprite.anim()
    
    
    # Función clima
    for climate in climate_objects:
        climate.update()
        if climate.rect.y > limit_xy[1] or climate.collide == True:
            # Regrasar la gota de lluvia al spawn
            climate.rect.x = climate.spawn_xy[0]
            climate.rect.y = climate.spawn_xy[1]
    
    
    # Función | Player | Limite del mapa
    if player.rect.x > limit_xy[0]:
        player.hp = -1
    elif player.rect.y > limit_xy[1]:
        player.hp = -1
    
    
    # Función | Level | Cambiar de nivel
    for sprite in level_objects:
        sprite.update()
        level = sprite.level
        if not sprite.level == None:
            print(level)
            # Establecer nivel actual
            data_CF.current_level = level
            save_CF( data_CF )

            # Eliminar sprites
            for other_sprite in layer_all_sprites.sprites():
                other_sprite.kill()

            # Renderizar mapa                
            read_Map( Map=current_map, level=data_CF.current_level )
            render_map = Start_Map(current_map)
            player = Player(
                position=render_map.player_spawn,
                show_collide=data_CF.show_collide, show_sprite=data_CF.show_sprite 
            )
            player_spawn_hp = player.hp
            player_anim_dead = None
            
            # Clima | Color de fondo
            if not loop_allday.climate == get_climate( current_map ):
                loop_allday = Loop_allday( current_map )
            
            # Posicionar camara y establecer limites de camara.
            limit_xy = get_limit_xy()
            scroll_float = [0,0]
            scroll_float = start_scroll(
                pos_xy=[player.rect.x, player.rect.y], display_xy=data_CF.disp, limit_xy=limit_xy,
                difference_xy=[data_CF.pixel_space*2, data_CF.pixel_space*3]
            )




    # Función renderizado de sprites / Mostrar / Todos los sprites / Layer Capas
    for sprite in layer_all_sprites.sprites():
        # Detectar que el sprite no sebrepase la pantalla
        display_collision = scroll_display_collision(
            [sprite.rect.x, sprite.rect.y], scroll_int, data_CF.disp, [data_CF.pixel_space, 0]
        )

        # Si el esprite esta en pantalla, mostrarlo.
        if display_collision == None:
            display.blit(
                sprite.surf, 
                ( sprite.rect.x -scroll_int[0], sprite.rect.y -scroll_int[1] )
            )
    
    
    
    
    # Funcion | Player Muerto/Dead
    if player.hp <= 0:
        if player_anim_dead == None:
            # Iniciar animacion
            player_anim_dead = Anim_player_dead(
                position=(
                    player.rect.x -player.rect.width//2, player.rect.y
                ),
                show_collide=data_CF.show_collide
            )
            player.show_sprite = False
            ( random.choice(sounds_dead) ).play()
        else:
            if player_anim_dead.anim_fin == True:
                # Finalizar animacion y spawnear al jugador
                player.hp = player_spawn_hp
                player.show_sprite = data_CF.show_sprite
                player.rect.topleft = render_map.player_spawn
                player.rect.x += (data_CF.pixel_space -player.rect.width)//2

                scroll_float = start_scroll(
                    pos_xy=[player.rect.x, player.rect.y], display_xy=data_CF.disp, limit_xy=limit_xy,
                    difference_xy=[data_CF.pixel_space*2, data_CF.pixel_space*3]
                )
                
                player_anim_dead = None
    
    
    
    
    # Sección de HUD y texto del juego
    # Mostrar Vida de jugador
    text_hp = font_normal.render( str(player.hp), True, generic_colors('green') )
    display.blit(
        text_hp, ( (data_CF.disp[0])-(size_font_normal*3), size_font_normal )
    )
    
    # Mostrar Puntaje
    text_score = font_normal.render( str(score), True, generic_colors('yellow') )
    display.blit(
        text_score, ( (data_CF.disp[0])-(size_font_normal*3), size_font_normal*2 )
    )    
    
    
    
    
    # Fin
    clock.tick(data_CF.fps)
    pygame.display.update()

pygame.quit()