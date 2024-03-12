from Modulos.Modulo_Text import (
    Text_Read, Ignore_Comment, Only_Comment
)
from Modulos import Modulo_Language as Lang
from Modulos.pygame.Modulo_pygame import (
    generic_colors, obj_collision_sides_solid, obj_coordinate_multiplier,
    player_camera_prepare, player_camera_move,
    obj_collision_sides_rebound, obj_not_see,
    Anim_sprite, Anim_sprite_set, Split_sprite
)
from Modulos.pygame.CF_info import (
    disp_width,
    disp_height,
    
    fps,
    game_title,
    volume,

    dir_game,
    dir_data,
    dir_sprites,
    dir_maps,
    dir_audio,
    
    current_level
)
from Modulos.pygame.CF_data import (
    set_level,
    get_music,
    get_climate_sound,
    save_gamecomplete
)
from Modulos.pygame.CF_object import(
    Player,

    Floor,
    Ladder,

    Spike,
    Star_pointed,
    Climate_rain,
    Anim_player_dead,
    Player_part,
    Limit_indicator,
    Level_change,
    Stair,
    Score,
    Cloud,
    Trampoline,
    Elevator,
    
    layer_all_sprites,
    nocamera_back_sprites,

    solid_objects,
    ladder_objects,
    jumping_objects,
    moving_objects,

    damage_objects,
    limit_objects,
    level_objects,
    anim_sprites,
    climate_objects,
    player_objects,
    score_objects,
    
    sounds_hit,
    sounds_step,
    sounds_dead,
    sound_jump
)

import time
import pygame, sys, os, random
from pygame.locals import *

# Resolución de pantalla de juego
disp_resolution = ( disp_width, disp_height )
display = pygame.display.set_mode( disp_resolution )

# Fotogramas del juego
clock = pygame.time.Clock()

# Titulo del juego
pygame.display.set_caption(game_title)

# Audio | Musica de fondo
#...

# Fuentes de texto
size_font_big = disp_width//15
size_font_normal = disp_width//60
font_str = 'monospace'
font_normal = pygame.font.SysFont(font_str, size_font_normal)
font_big = pygame.font.SysFont(font_str, size_font_big)

# Fondo
image_background = pygame.transform.scale(
    pygame.image.load( os.path.join( dir_sprites, 'background.png' ) ),
    (disp_width, disp_height)
).convert()
color_background = pygame.Surface( (disp_width, disp_height), pygame.SRCALPHA )


'''
for x in range(0, 10):
    floor = Floor(
        size=(disp_width//30, disp_width//60),
        position=(
            random.randint(disp_width//60, disp_width-disp_width//60),
            random.randint(disp_width//60, disp_height-disp_width//60)            
        ),
        limit=False,
        show_collide=False
    )
'''



# Funciones
class Start_Map():
    def __init__(self,
        x_column = 0,
        y_column = 0,
        level = current_level
    ):
        #cf_map_default.txt
        #cf_map.txt
        #cf_map_level-test.txt
        #cf_map_level-test1.txt
        '''
        Funcion que permite crear niveles de una forma visual y sencilla.
        "." para un espacio de el "ancho sobre 60" del juego
        "p" para una plataforma con un espacio del "ancho sobre 60" del juego
        "|" para establecer el limite de la camara, con un espacio del ancho sobre el juego"
        
        "x, y" column son para establecer el pixel de inicio basado en la resolucion del juego. Por defecto inician en 0, 0.
        '''
        # Establecer archivo y información del level
        next_level = None
        self.level = level.replace(dir_maps, '')

        self.climate = None
        self.message_start = None
        map_level = Text_Read(level, 'ModeText')
        map_info = Only_Comment(
            text=map_level,
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
                next_level = info[0].split(':')
            else:
                next_level = [None, None]
        if number_info >= 2:
            self.climate = info[1]

        if number_info >= 3:
            if info[2].startswith('stock_'):
                self.message_start = Lang.get_text(info[2])
            else:
                self.message_start = info[2]
        map_level = Ignore_Comment(text=map_level, comment='//')
        map_level = Ignore_Comment(text=map_level, comment='$$')
                
        # Establecer variables de inicio de juego, de posición y tamaño de objetos.
        self.player_spawn = None
        plat_number = 0
        pixel_space = disp_width//60

        # Establecer objetos en su posición indicada
        test = ''
        for column in map_level.split('\n'):
            if column == '':
                pass
            else:
                y_column += 1
    
            x_space = x_column
            for space in column:
                position=( (x_space*pixel_space), (y_column*pixel_space) )
                if space == '.' or space == '#':
                    x_space += 1

                elif space == 'p':
                    x_space += 1
                    plat = Floor(
                        size=(pixel_space, pixel_space),
                        position=position,
                        climate=self.climate
                    )
                
                elif space == 'P':
                    x_space += 1

                    # Para acomodar los objetos de forma adecuada.
                    multipler = obj_coordinate_multiplier(
                        multipler=2,
                        pixel=pixel_space,
                        x=x_space,
                        y=y_column
                    )
                    size=multipler[0]
                    position=multipler[1]

                    plat = Floor(
                        size=size,
                        position=position,
                        climate=self.climate
                    )
                    
                elif space == 'H':
                    x_space += 1
                    Ladder(
                        size=pixel_space,
                        position=position,
                    )
                    
                elif space == '_':
                    x_space += 1
                    Trampoline(
                        size=pixel_space,
                        position=position,
                    )

                elif space == 'x':
                    x_space += 1
                    Elevator(
                        size=pixel_space,
                        position=position, move_dimension=1
                    )
                    
                elif space == 'y':
                    x_space += 1
                    Elevator(
                        size=pixel_space,
                        position=position, move_dimension=2
                    )

                elif space == '|':
                    x_space += 1
                    limit = Limit_indicator(
                        position=position,
                        show_collide=False
                    )

                elif space == 'j':
                    x_space += 1
                    self.player_spawn = position

                elif space == '^':
                    x_space += 1
                    spike = Spike( position=position )

                elif space == '!':
                    x_space += 1
                    spike = Spike( position=position, instakill=True )
                    
                elif space == 'A':
                    x_space += 1

                    # Para acomodar los objetos de forma adecuada.
                    multipler = obj_coordinate_multiplier(
                        multipler=2,
                        pixel=pixel_space,
                        x=x_space,
                        y=y_column
                    )
                    for x in multipler[0]:
                        size = x
                    position=multipler[1]

                    spike = Spike(
                        size=size,
                        position=position
                    )
                    
                elif space == '\\':
                    x_space += 1
                    spike = Spike( position=position, moving=True, instakill=True )
                
                elif space == 'Y':
                    x_space += 1
                    Star_pointed(position=position)

                elif space == 'X':
                    x_space += 1
                    Star_pointed(position=position, instakill=True)
                    
                elif space == '*':
                    x_space += 1
                    Star_pointed(position=position, moving=True, instakill=True)

                elif space == '+':
                    x_space += 1
                    Stair(
                        size=pixel_space,
                        position=position,
                        invert=False,
                        climate=self.climate
                    )
                    
                elif space == '-':
                    x_space += 1
                    Stair(
                        size=pixel_space,
                        position=position,
                        invert=True,
                        climate=self.climate
                    )

                elif space == 's':
                    x_space += 1
                    Score(
                        size=pixel_space,
                        position=position,
                    )

                elif space == '~':
                    x_space += 1

                    Climate_rain(
                        position=position
                    )

                elif space == '0':
                    x_space += 1

                    level = Level_change(
                        dir_level=next_level[0],
                        level=next_level[1],
                        position=position
                    )
                    
                elif space == 'F':
                    x_space += 1

                    Level_change(
                        dir_level=next_level[0],
                        level=next_level[1],
                        position=position,
                        gamecomplete=True
                    )
        
        # Sección de genración de clima:
        if self.climate == 'rain':
            rain_space_x = 0
            for space in map_level.split('\n')[0]:
                if (
                    space == '.' or
                    space == '|' or
                    space == '~'
                ):
                    rain_space_x += 1
            rain_pixels_x = rain_space_x*pixel_space
            rain_pixels_y = y_column*pixel_space
            # Esto funciona bien, los bugs que sucedan, deberian ser por otras funciones
            # pixel_space = 16
            # pixel_space*16 = 256
            # pixel_space*4 = 64
            difference_x = pixel_space*16
            difference_y = rain_pixels_y//(pixel_space*4)
            if rain_space_x > 0:
                for x in range(0, rain_space_x):
                    Climate_rain( 
                        position=( 
                            random.randint( difference_x, rain_pixels_x+(difference_x) ),
                            random.randint( (difference_y)-(difference_x//2),  difference_y )
                        )
                    )


# Loop dia y noche
class Loop_allday():
    def __init__ (self, climate=None, minutes=5, fps=fps):
        self.count_fps_day = 0
        if climate == 'rain':
            self.color_day_red = 155
            self.color_day_green = 168
            self.color_day_blue = 187
        elif climate == 'sunny':
            self.color_day_red = 240
            self.color_day_green = 202
            self.color_day_blue = 134
        elif climate == 'alien':
            self.color_day_red = 68
            self.color_day_green = 38
            self.color_day_blue = 136
        elif climate == 'black':
            self.color_day_red = 47
            self.color_day_green = 47
            self.color_day_blue = 47
        else:
            # climate == None
            self.color_day_red = 108
            self.color_day_green = 150
            self.color_day_blue = 255
        self.color_day = [self.color_day_red, self.color_day_green, self.color_day_blue]
        self.is_night = False

        # Cambio de dia a noche, y de noche a dia, entre mas bajo, mas cambios. Y mas oscura la noche
        # Como minimo, reductor tiene que ser dos, o si no falla el programa
        # Minutos de duración
        #minutes = minutes

        reducer = 4
        self.changes_day = []
        for value in self.color_day:
            if value > (reducer-1):
                self.changes_day.append( value//reducer )
            else:
                self.changes_day.append( 0 )

        reducer = (reducer-1)

        # fps = 30
        # Si son 30 cambios maximos, entonces cada segundo secedera un cambio. (fps/1)
        # Si son 60 cambios maximos, entonces cada medio segundo secedera un cambio. (fps/2)
        # Si son 90 cambios maximos, entonces cada 1/3 segundo secedera un cambio. (fps/3)
        # Esto con el fin de que cada dia/noche, duren aproximadamente medio minuto, de esa manera cada dia completo dura 1 minuto
        self.color_change = (
            ( fps//( ( max(self.changes_day) )/fps ) )//(reducer)
        )*minutes
        if self.color_change < 1:
            self.color_change = 1



# Funcion Musica
# Crear un evento personalizado para el final de la pista
end_of_track_event = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(end_of_track_event)

class Play_Music():
    def __init__(self, music=get_music(), climate=None, climate_sound=get_climate_sound()):
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
        pygame.mixer.music.set_volume( volume )
        pygame.mixer.music.play()
        
        return self.limit_music
        
    def change_climate(self, climate=None):
        self.climate = climate
        if not self.__go == True:
            music = self.set_climate()
            pygame.mixer.music.load( music )
            pygame.mixer.music.set_volume( volume )
            pygame.mixer.music.play()
            self.limit_music = self.__limit_music_climate


# Función nubes de fondo
def create_clouds(c_number = 15):
    '''
    Imagenes de fondo | Nubes de fondo
    # Si hay demasiadas nubes se dejaran de crear.
    # Se creara una nube de forma random, con posibilidades 1-6
    '''
    c_sizex = disp_width//c_number
    c_sizey = disp_height//c_number
    c_size = (c_sizex, c_sizey)

    clouds = 0
    for y in range(0, c_number):
        posy = c_sizey*(y)
        for x in range(0, c_number):
            posx = c_sizex*(x)

            create = random.choice( [True, 2, 3, 4, 5, 6] )
            if create == True:
                clouds += 1
                Cloud( size=c_size, position=(posx, posy) )




# Iniciar Funciones y contantes necesarias
# Funcion nubes
create_clouds()


# Funcion del mapa
score = 0
start_map = Start_Map(0, 0)

for plat in solid_objects:
    plat.limit_collision()

player = Player( position=start_map.player_spawn )

player_spawn_hp = player.hp
player_spawn_xy = player_camera_prepare(
    disp_width=disp_width, disp_height=disp_height, more_pixels=disp_width//30,
    all_sprites=layer_all_sprites.sprites(), player=player, show_coordenades=True
)
player_show_sprite = player.show_sprite
player_anim_dead = None

camera_x = 0
camera_y = 0

climate_number = 0
dict_climate = {}
for climate in climate_objects:
    climate_number += 1
    dict_climate.update( {climate_number : [climate.rect.x, climate.rect.y]} )
    

message_start = start_map.message_start


# Funcion | Dia y noche
loop_allday = Loop_allday(
    climate=start_map.climate
)
count_fps_day = loop_allday.count_fps_day
color_day = loop_allday.color_day
color_day_red = loop_allday.color_day_red
color_day_green = loop_allday.color_day_green
color_day_blue = loop_allday.color_day_blue
color_change = loop_allday.color_change
changes_day = loop_allday.changes_day
is_night = loop_allday.is_night

# Funcion musica
play_music = Play_Music( climate=start_map.climate )
count_playmusic = 0
limit_playmusic = play_music.limit_music


# Funcion juego completado
gamecomplete = False

# Función cretidos
credits = False
credits_fps = fps*4
credits_count = 0
    


# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == player.pressed_jump:
                # Si se preciona la tecla para saltar.
                # Mensajes
                if type(message_start) is str:
                    # El mensaje se cierra
                    message_start = None
                else:
                    # El jugador salta si no hay mensajes
                    player.jump()
                    
                # Creditos
                if credits == True:
                    if credits_count >= credits_fps:
                        pygame.quit()
                        sys.exit()
                    
                # Juego completado
                elif gamecomplete == True:
                    # Si el juego esta completado
                    save_gamecomplete(level=start_map.level, score=score)
                    if credits == False:
                        for sprite in layer_all_sprites.sprites():
                            if not sprite == player:
                                sprite.kill()
                        credits = True

            elif event.key == pygame.K_r:
                # Por si se bugea el juego, poder matar al jugador y por consecuensia reiniciar el nivel
                if not player.hp <= 0:
                    if gamecomplete == False:
                        player.hp = -1
        if event.type == end_of_track_event:
            # Cuando se acaba la musica
            count_playmusic += 1
            #print(count_playmusic)
            if count_playmusic == limit_playmusic:
                count_playmusic = 0
                limit_playmusic = play_music.play()
            else:
                pygame.mixer.music.play()

    
    # Fondo | Ciclo dia y noche
    display.blit( image_background, (0,0) )

    color_background.fill( ( color_day[0],color_day[1],color_day[2], 143 ) )
    display.blit( color_background, (0,0) )


    if count_fps_day == color_change:
        count_fps_day = 0
        if is_night == False:
            values = [False, False, False]
            if not color_day[0] == changes_day[0]:
                color_day[0] -= 1
            else:
                values[0] = True

            if not color_day[1] == changes_day[1]:
                color_day[1] -= 1
            else:
                values[1] = True
            
            if not color_day[2] == changes_day[2]:
                color_day[2] -= 1
            else:
                values[2] = True
            
            if (
                values[0] == True and
                values[1] == True and
                values[2] == True
            ):
                is_night = True

        elif is_night == True:
            values = [False, False, False]
            if not color_day[0] == color_day_red:
                color_day[0] += 1
            else:
                values[0] = True

            if not color_day[1] == color_day_green:
                color_day[1] += 1
            else:
                values[1] = True

            if not color_day[2] == color_day_blue:
                color_day[2] += 1
            else:
                values[2] = True
                
            if (
                values[0] == True and
                values[1] == True and
                values[2] == True
            ):
                is_night = False
                
    count_fps_day += 1
    
    # Objetos / Funciones / Para cambiar de nivel
    for sprite in level_objects:
        sprite.update()
        if sprite.gamecomplete == True:
            sprite.level = None
            gamecomplete = True

        if not sprite.level == None:
            level = sprite.level

            for other_sprite in layer_all_sprites.sprites():
                other_sprite.kill()

            start_map = Start_Map(
                 0, 0,
                 level = level
            )

            for plat in solid_objects:
                plat.limit_collision()

            player = Player( position=start_map.player_spawn )
            player.hp = player_spawn_hp

            #player_spawn_hp = player_spawn_hp
            player_spawn_xy = player_camera_prepare(
                disp_width=disp_width, disp_height=disp_height, more_pixels=disp_width//30,
                all_sprites=layer_all_sprites.sprites(), player=player, show_coordenades=True
            )
            #player_show_sprite = player_show_sprite
            player_anim_dead = None

            camera_x = 0
            camera_y = 0

            climate_number = 0
            dict_climate = {}
            for climate in climate_objects:
                climate_number += 1
                dict_climate.update( {climate_number : [climate.rect.x, climate.rect.y]} )
            
            message_start = start_map.message_start
                
            # Funcion de dia y noche
            loop_allday = Loop_allday(
                climate=start_map.climate
            )
            if not (
                color_day_red == loop_allday.color_day_red or
                color_day_green == loop_allday.color_day_green or
                color_day_blue == loop_allday.color_day_blue
            ):
                count_fps_day = loop_allday.count_fps_day
                color_day = loop_allday.color_day
                color_day_red = loop_allday.color_day_red
                color_day_green = loop_allday.color_day_green
                color_day_blue = loop_allday.color_day_blue
                color_change = loop_allday.color_change
                changes_day = loop_allday.changes_day
                is_night = loop_allday.is_night
            
            # Función musica
            play_music.change_climate(climate=start_map.climate)
            
            # Establecer nivel actual
            set_level(level=level)


    # Objetos / Funciones / Puntos
    for obj in score_objects:
        if obj.point == True:
            obj.remove_point()
            score += 1
    
    # Objetos / Funciones / Player
    player.move()
    player.update()
    
    # Objetos / Funciones / Animaciones
    for sprite in anim_sprites:
        sprite.anim()
        
    # Objetos / Funciones / Clima Colision
    number = 0
    for climate in climate_objects:
        number += 1
        climate.update()
        if climate.collide == True:
            climate.rect.center = (
                camera_x + dict_climate.get(number)[0], camera_y + dict_climate.get(number)[1]
            )
    # Objetos / Mostrar / Los sprites de atras, que no puede mover la camara.
    for sprite in nocamera_back_sprites:
        display.blit(sprite.surf, sprite.rect)
            
    # Objetos / Mostrar / Todos los sprites, solo si se ven en la pantalla
    for sprite in layer_all_sprites.sprites():
        if obj_not_see(
            disp_width=disp_width, disp_height=disp_height, obj=sprite, difference=disp_width//60
        ) == None:
            display.blit(sprite.surf, sprite.rect)


    # Camara
    camera = player_camera_move(
        disp_width=disp_width, disp_height=disp_height,
        camera_x=camera_x, camera_y=camera_y, 
        all_sprites=layer_all_sprites.sprites(),
        limit_objects=limit_objects,
        player=player,
    )
    camera_x=camera[0]
    camera_y=camera[1]
    dead = camera[2]
    if dead == True:
        if player_anim_dead == None:
            player_anim_dead = Anim_player_dead(
                position=(
                    (player.rect.x +(player.rect.width/2)),
                    player.rect.y+(player.rect.height//2)
                )
            )
            player.show_sprite = False
            ( random.choice(sounds_dead) ).play()
        else:
            if player_anim_dead.anim_fin == True:
                player_anim_dead = None
                # Establecer todos los objetos como al inicio del juego
                # Con base al valor xy actual de la camara, sus valores xy se invierten y se suman a las coordenadas actuales de los sprites.
                # Recuerda que esto es posible: "x+ -x = 0"
                for sprite in layer_all_sprites.sprites():
                    sprite.rect.x += (camera_x*-1)
                    sprite.rect.y += (camera_y*-1)
            
                # Establecer camara en la posición inicial
                camera_x = 0
                camera_y = 0
            
                # Establecer player como al inicio del juego
                player.rect.x = player_spawn_xy[0]
                player.rect.y = player_spawn_xy[1]
                player.hp = player_spawn_hp
                player.show_sprite = player_show_sprite
    
    
    # Sección del texto del juego (Interfaz/HUD)
    if credits == False:
        # Mostrar Vida de jugador
        text_hp = font_normal.render(
            str(player.hp), True, generic_colors('green')
        )
        display.blit(
            text_hp, (
                (disp_width)-(size_font_normal*3),
                size_font_normal
            )
        )
        
        # Mostrar Puntaje
        text_score = font_normal.render(
            str(score), True, generic_colors('yellow')
        )
        display.blit(
            text_score, (
                (disp_width)-(size_font_normal*3),
                size_font_normal*2
            )
        )
        
        
        # Función juego completado
        # Funciones | Mensajes
        message_continue = False

        # Función | Mensaje de inicio
        if type(message_start) is str:
            text_message = font_normal.render(
                message_start, True, generic_colors('white')
            )
            position = [
                (disp_width//2)-(text_message.get_rect().width//2),
                size_font_normal
            ]

            rect_text = text_message.get_rect()
            pygame.draw.rect(
                display, generic_colors('black'), 
                (
                    position[0], position[1],
                    rect_text.width, rect_text.height
                )
            )

            display.blit(
                text_message, (
                    position[0],
                    position[1]
                )
            )
            message_continue = True
        
        # Función mensaje fin de juego
        if gamecomplete == True and credits == False:
            # Lo que pasa cuando el juego es completado
            text_gamecomplete = font_big.render(
                Lang.get_text('gamecomplete'), True, generic_colors('yellow')
            )
            position = [
                (disp_width//2)-(text_gamecomplete.get_rect().width//2),
                (disp_height//2)-(size_font_big//2)
            ]
            
            rect_text = text_gamecomplete.get_rect()
            pygame.draw.rect(
                display, generic_colors('black'), 
                (
                    position[0], position[1],
                    rect_text.width, rect_text.height
                )
            )

            display.blit(
                text_gamecomplete, (
                    position[0],
                    position[1]
                )
            )
            message_continue = True
        
        # Función mensaje continuar
        if message_continue == True:
            # El mensaje continuar, mantiene al personaje inmovil
            player.not_move = True
            player.gravity = False
            player.rect.y -= player.gravity_power

            text_continue = font_normal.render(
                f"{Lang.get_text('continue_jump')}...", True, generic_colors('white')
            )
            position = [size_font_normal, disp_height-(size_font_normal*2)]
            
            rect_text = text_continue.get_rect()
            pygame.draw.rect(
                display, generic_colors('black'), 
                (
                    position[0], position[1],
                    rect_text.width, rect_text.height
                )
            )

            display.blit(
                text_continue, (
                    position[0],
                    position[1]
                )
            )
    
    # Mostrar Creditos
    else:
        # Fondo negro
        display.fill( generic_colors('black') )
        
        # Para que no se mueva el jugador
        # Si, el jugador sige creado en los creditos... XD
        player.not_move = True
        player.gravity = False
        player.rect.y -= player.gravity_power
        
        # Texto creditos
        text_credits = font_normal.render(
            Lang.get_text('credits'), True, generic_colors('yellow')
        )
        position = [(disp_width//2)-(text_credits.get_rect().width//2), (size_font_normal//2)]
        
        display.blit(
            text_credits, (
                position[0],
                position[1]
            )
        )
        
        # Texto nombre del creador 
        text_by = font_normal.render(
            'Jean Abraham Chacón Candanosa @CocoMarck', True, generic_colors('green')
        )
        position = [(disp_width//2)-(text_by.get_rect().width//2), (disp_height//2)-(size_font_normal//2)]
        
        display.blit(
            text_by, (
                position[0],
                position[1]
            )
        )
        
        # Mostrar Puntaje
        text_score = font_normal.render(
            f'{Lang.get_text("score")}: {score}', True, generic_colors('white')
        )
        display.blit(
            text_score, (
                size_font_normal,
                size_font_normal*2
            )
        )

        # Habilitar "Cerrar el juego"
        if credits_count < credits_fps:
            credits_count += 1
        else:
            # Texto continuar
            text_continue = font_normal.render(
                f"{Lang.get_text('continue_jump')}...", True, generic_colors('white')
            )
            position = [size_font_normal, disp_height-(size_font_normal*2)]

            display.blit(
                text_continue, (
                    position[0],
                    position[1]
                )
            )

    
    # Fin
    clock.tick(fps)
    pygame.display.update()