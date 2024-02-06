from Modulos.Modulo_Text import (
    Text_Read, Ignore_Comment, Only_Comment
)
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
from Modulos.pygame.CF_object import(
    Player,
    Floor,
    Spike,
    Star_pointed,
    Climate_rain,
    Anim_player_dead,
    Player_part,
    Limit_indicator,
    Level_change,
    Stair,
    
    all_sprites,
    forward_sprites,

    solid_objects,
    instakill_objects,
    damage_objects,
    limit_objects,
    level_objects,
    anim_sprites,
    climate_objects,
    player_objects,
    player_sprites,
    
    sounds_hit,
    sounds_step,
    sounds_dead,
    sound_jump
)

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
        map_level = Text_Read(current_level, 'ModeText')
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
        self.player_spawn = None
        plat_number = 0
        pixel_space = disp_width//60
        
        # Establecer la información del mapa
        next_level = None
        self.climate = None
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
            next_level = info[0].split(':')
        if number_info == 2:
            self.climate = info[1]

        # Establecer objetos en su posición inidaca
        map_level = Ignore_Comment(text=map_level, comment='//')
        map_level = Ignore_Comment(text=map_level, comment='$$')
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
                        show_collide=False
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
                        show_collide=False
                    )

                elif space == '|':
                    x_space += 1
                    limit = Limit_indicator(
                        position=position,
                        see=False
                    )

                elif space == 'j':
                    x_space += 1
                    self.player_spawn = position

                elif space == '^':
                    x_space += 1
                    spike = Spike( position=position, show_collide=False )
                    
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
                        position=position,
                        show_collide=False
                    )
                
                elif space == 'Y':
                    x_space += 1
                    Star_pointed(position=position)

                elif space == '+':
                    x_space += 1
                    Stair(
                        size=pixel_space,
                        position=position,
                        invert=False
                    )
                    
                elif space == '-':
                    x_space += 1
                    Stair(
                        size=pixel_space,
                        position=position,
                        invert=True
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
    def __init__ (self, climate=None, minutes=1, fps=fps):
        self.count_fps_day = 0

        if climate == None:
            self.color_day_red = 108
            self.color_day_green = 150
            self.color_day_blue = 255
        elif climate == 'rain':
            self.color_day_red = 155
            self.color_day_green = 168
            self.color_day_blue = 187
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

def play_music():
    list_music = [
        #os.path.join(dir_audio, 'music/silence.ogg'),
        [os.path.join(dir_audio, 'music/default-music.ogg'), 4],
        [os.path.join(dir_audio, 'music/music-test1.ogg'), 2],
        [os.path.join(dir_audio, 'music/music-test2.ogg'), 3]
    ]

    go = random.choice( [True, 2, 3, 4] )
    #go = True
    if go == True:
        music_ready = random.choice(list_music)
        music = music_ready[0]
        limit_music = music_ready[1]
    else:
        music = os.path.join(dir_audio, 'music/silence.ogg')
        limit_music = 10
    pygame.mixer.music.load( music )
    pygame.mixer.music.set_volume( volume )
    pygame.mixer.music.play()
    
    return limit_music

count_playmusic = 0
limit_playmusic = play_music()




# Iniciar Funciones y contantes necesarias
# Funcion del mapa
start_map = Start_Map(0, 0)

for plat in solid_objects:
    plat.limit_collision()

player = Player( position=start_map.player_spawn )

player_spawn_hp = player.hp
player_spawn_xy = player_camera_prepare(
    disp_width=disp_width, disp_height=disp_height, more_pixels=disp_width//30,
    all_sprites=all_sprites, player=player, show_coordenades=True
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
    


# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == player.pressed_jump:
                player.jump()
        if event.type == end_of_track_event:
            # Cuando se acaba la musica
            count_playmusic += 1
            print(count_playmusic)
            if count_playmusic == limit_playmusic:
                count_playmusic = 0
                limit_playmusic = play_music()
                print(limit_playmusic)
            else:
                pygame.mixer.music.play()

    
    # Fondo | Ciclo dia y noche
    display.fill(
        ( color_day[0],color_day[1],color_day[2] )
    )

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
        if not sprite.level == None:
            level = sprite.level

            for other_sprite in all_sprites:
                other_sprite.kill()

            start_map = Start_Map(
                 0, 0,
                 map_level = Text_Read(level, 'ModeText')
            )

            for plat in solid_objects:
                plat.limit_collision()

            player = Player( position=start_map.player_spawn )
            player.hp = player_spawn_hp

            #player_spawn_hp = player_spawn_hp
            player_spawn_xy = player_camera_prepare(
                disp_width=disp_width, disp_height=disp_height, more_pixels=disp_width//30,
                all_sprites=all_sprites, player=player, show_coordenades=True
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

    # Objetos / Mostrar / Todos los sprites, solo si se ven en la pantalla
    for sprite in all_sprites:
        if obj_not_see(
            disp_width=disp_width, disp_height=disp_height, obj=sprite, difference=disp_width//60
        ) == None:
            if (
                (not sprite in forward_sprites) and
                (not sprite in player_sprites)
            ):
                display.blit(sprite.surf, sprite.rect)
        
    # Objetos / Mostrar / Jugador, el se vera encima de los demas sprites (Las lineas de arriba)
    for sprite in player_sprites:
        display.blit(sprite.surf, sprite.rect)

    display.blit(player.surf, player.rect)
    
    # Objetos / Mostrar / Adelante, maxima pioridad
    for sprite in forward_sprites:
        if obj_not_see(
            disp_width=disp_width, disp_height=disp_height, obj=sprite, difference=disp_width//60
        ) == None:
            display.blit(sprite.surf, sprite.rect)


    # Camara
    camera = player_camera_move(
        disp_width=disp_width, disp_height=disp_height,
        camera_x=camera_x, camera_y=camera_y, 
        all_sprites=all_sprites,
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
                for sprite in all_sprites:
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
        

    
    # Fin
    clock.tick(fps)
    pygame.display.update()