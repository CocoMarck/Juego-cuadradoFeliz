# general funcs
from core.text_util import (read_text, ignore_comment, only_the_comment) # No se necesita.
from controllers import language_controller as Lang

# CF pygame funcs
from core.pygame.pygame_util import *
from core.pygame.cf_util import (
    get_image, player_key, all_music, GradiantColor, surface_bloom, get_coordinate_multipler, 
    scroll_display_collision, create_mask_gradient, surf_limit_width, invert_rgb_color,
    get_mask_for_surface
)
from controllers.cf_info import *
from controllers.cf_controller import *

# CF sprites
from entities import Map, CF
from entities.sprites import *
from entities.sprites.sprite_groups import *

# pygame
import time
import pygame, sys, os, random
from pygame.locals import *

# Resolución de pantalla de juego
window = pygame.display.set_mode( data_CF.disp )
display = pygame.Surface( scale_surface_size )

# Fotogramas del juego
clock = pygame.time.Clock()

# Titulo del juego
pygame.display.set_caption(game_title)

# Audio | Musica de fondo
# Estan en el modulo CF_function

# Fuentes de texto
size_font_big = int(pixel_space_to_scale*4)
size_font_normal = pixel_space_to_scale
font_str = 'monospace'
font_normal = pygame.font.SysFont(font_str, size_font_normal)
font_big = pygame.font.SysFont(font_str, size_font_big)

# Fondo
if data_CF.show_sprite == True:
    image_background = get_image('background', size=scale_surface_size, return_method='normal')
else:
    image_background = pygame.Surface( (scale_surface_size[0], scale_surface_size[1]) )
    image_background.fill( (63, 63, 63) )
color_background = pygame.Surface( (scale_surface_size[0], scale_surface_size[1]), pygame.SRCALPHA )

# Transparencia
if data_CF.show_collide == True: transparency_collide = 255
else: transparency_collide = 0

if data_CF.show_sprite == True:
    transparency_sprite = 255
    transparency_sprite_rain = 127
else:
    transparency_sprite = 0
    transparency_sprite_rain = 0
if data_CF.show_collide == False and data_CF.show_sprite == False:
    transparency_collide, transparency_sprite, transparency_sprite_rain, = 127, 127, 127
    




# Map
'''
Nota:
Los objetos en vez de posicionar el rect con "lefttop", se hace con "center", lo cual no es lo adecuado, seria bueno cambiarlo (probablemente se tararia un poco menos el renderizado y seria mas facil el manejo de este).
'''
class Start_Map( ):
    def __init__(self, Map):
        super().__init__()
        
        print(f'pixel space: {pixel_space_to_scale}px' )# Mostrar pixel space
        
        # Mensaje de inicio
        self.message_start = current_map.message_start
        if isinstance(self.message_start,str):
            if self.message_start.startswith('stock_'):
                self.message_start = Lang.get_text(self.message_start)
        
        # Atributos necesarios
        self.player_spawn = [0,0]

        # Renderizar mapa
        xy = [0,0]
        for line in Map.list_map:
            print_line = '' # Mostrar mapa en caracteres
        
            xy[0] = 0
            position = [ xy[0], xy[1]*pixel_space_to_scale ]
            xy[1] += 1
            
            for character in line:
                position[0] = xy[0]*pixel_space_to_scale
                
                xy[0] += 1

                # Jugador
                if character == dict_object['player']:
                    self.player_spawn = [ position[0], position[1] ]
                
                
                
                
                # Objetos solidos/saltarines/monedas/checkpoint, no dañinos
                elif character == dict_object['stone']:
                    # Objeto plataforma Piso Floor
                    Floor(
                        size=(pixel_space_to_scale, pixel_space_to_scale),
                        position=position, climate=Map.climate,
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        solid_objects=solid_objects, 
                        update_objects=update_objects, layer_all_sprites=layer_all_sprites
                    )
                elif character == dict_object['stone-big']:
                    # Posicionar de forma adecuada
                    new_size_pos = get_coordinate_multipler( 
                        multipler=2, pixel_space=pixel_space_to_scale, position=position 
                    )
                    new_size_pos[1] = position
                
                    # Objeto plataforma Piso Floor
                    Floor(
                        size=new_size_pos[0], position=new_size_pos[1], climate=Map.climate,
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        solid_objects=solid_objects, 
                        update_objects=update_objects, layer_all_sprites=layer_all_sprites
                    )
                
                elif character == dict_object['coin']:
                    Score( 
                        size=pixel_space_to_scale, position=position, 
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        score_objects=score_objects, layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['stair-right']:
                    Stair(
                        size=pixel_space_to_scale, position=position, invert=False, climate=Map.climate, 
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        solid_objects=solid_objects, update_objects=update_objects, 
                        layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['stair-left']:
                    Stair(
                     size=pixel_space_to_scale, position=position, invert=True, climate=Map.climate,      
                     transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                     solid_objects=solid_objects, update_objects=update_objects, 
                     layer_all_sprites=layer_all_sprites
                    )

                elif character == dict_object['ladder-y']:
                    Ladder(
                     size=pixel_space_to_scale, position=position,
                     transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                     ladder_objects=ladder_objects, layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['trampoline']:
                    Trampoline(
                        size=pixel_space_to_scale, position=position,
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        jumping_objects=jumping_objects, layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['elevator-x']:
                    Elevator(
                     size=pixel_space_to_scale, position=position, move_dimension=1,
                     transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                     moving_objects=moving_objects, anim_sprites=anim_sprites, solid_objects=solid_objects,
                     layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['elevator-y']:
                    Elevator(
                     size=pixel_space_to_scale, position=position, move_dimension=2,
                     transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                     moving_objects=moving_objects, anim_sprites=anim_sprites, solid_objects=solid_objects,
                     layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['climate-rain']:
                    ClimateRain(
                     position=position, transparency_collide=transparency_collide, 
                     transparency_sprite=transparency_sprite_rain, climate_objects=climate_objects, 
                     damage_objects=damage_objects, player_objects=player_objects, 
                     solid_objects=solid_objects, layer_all_sprites=layer_all_sprites
                    )

                # NPC
                elif character == dict_object['enemy']:
                    Enemy(
                     transparency_collide=transparency_collide,
                     transparency_sprite=transparency_sprite,
                     dict_sprite={
                      'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
                      'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
                     },
                     position=[ (xy[0]-1)*pixel_space_to_scale, (xy[1]-1)*pixel_space_to_scale ],
                     solid_objects=solid_objects, damage_objects=damage_objects,
                     level_objects=level_objects, score_objects=score_objects,
                     jumping_objects=jumping_objects, moving_objects=moving_objects,
                     ladder_objects=ladder_objects, particle_objects=particle_objects,
                     anim_sprites=anim_sprites, update_objects=update_objects,
                     gun_objects=gun_objects, respawn_objects=respawn_objects,
                     player_objects=player_objects, layer_all_sprites=layer_all_sprites
                    )


                # Niveles
                elif character == dict_object['level-change']:
                    level = ChangeLevel(
                        dir_level=Map.path, level=Map.next_level, position=position, 
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        layer_all_sprites=layer_all_sprites, level_objects=level_objects
                    )
                    
                elif character == dict_object['end-game']:
                    ChangeLevel(
                        dir_level=Map.path, level=Map.next_level, position=position, gamecomplete=True,
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        layer_all_sprites=layer_all_sprites, level_objects=level_objects
                    )
                
                
                
                
                # Limite del mapa
                elif character == dict_object['limit']:
                    LimitIndicator(
                        position=position, transparency_collide=transparency_collide,
                        layer_all_sprites=layer_all_sprites, limit_objects=limit_objects
                    )
                
                
                
                # Objetos dañinos
                elif character == dict_object['spike']:
                    spike = Spike(
                     position=position, transparency_collide=transparency_collide, 
                     transparency_sprite=transparency_sprite, damage_objects=damage_objects, 
                     anim_sprites=anim_sprites, solid_objects=solid_objects, update_objects=update_objects, 
                     layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['spike-big']:
                    # Objeto pico
                    Spike(
                     size=pixel_space_to_scale*2, position=position, transparency_collide=transparency_collide,
                     transparency_sprite=transparency_sprite, damage_objects=damage_objects, 
                     anim_sprites=anim_sprites, solid_objects=solid_objects, update_objects=update_objects, 
                     layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['spike-anim']:
                    Spike( 
                     position=position, moving=True, instakill=True, transparency_collide=transparency_collide, 
                     transparency_sprite=transparency_sprite, damage_objects=damage_objects, 
                     anim_sprites=anim_sprites, solid_objects=solid_objects, update_objects=update_objects, 
                     layer_all_sprites=layer_all_sprites
                    )

                elif character == dict_object['spike-instakill']:
                    Spike( 
                     position=position, instakill=True, transparency_collide=transparency_collide,
                     transparency_sprite=transparency_sprite, damage_objects=damage_objects, 
                     anim_sprites=anim_sprites, solid_objects=solid_objects, update_objects=update_objects, 
                     layer_all_sprites=layer_all_sprites
                    )
                    
                elif character == dict_object['star-pointed']:
                    PointedStar(
                        position=position,
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        damage_objects=damage_objects, anim_sprites=anim_sprites, 
                        layer_all_sprites=layer_all_sprites
                    )

                elif character == dict_object['star-pointed-anim']:
                    PointedStar(
                        position=position, moving=True, instakill=True,
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        damage_objects=damage_objects, anim_sprites=anim_sprites, 
                        layer_all_sprites=layer_all_sprites
                    )

                elif character == dict_object['star-pointed-instakill']:
                    PointedStar(
                        position=position, instakill=True,
                        transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
                        damage_objects=damage_objects, anim_sprites=anim_sprites, 
                        layer_all_sprites=layer_all_sprites
                    )

                elif character == dict_object['gun']:
                    Gun(
                     size=pixel_space_to_scale,
                     position=position,
                     transparency_collide=transparency_collide,
                     transparency_sprite=transparency_sprite,
                     layer_all_sprites=layer_all_sprites, update_objects=update_objects,
                     gun_objects=gun_objects
                    )
        
                print_line += character
        
            print(print_line) # Mostrar mapa en caracteres

        # Establecer Limite del mapa
        if xy[0] > 0 and xy[1] > 0:
            reduce = 1
        else:
            reduce = 0
        self.limit_xy = [ (xy[0]-reduce) *pixel_space_to_scale, (xy[1]-reduce) *pixel_space_to_scale ]



        '''
        Limite para objetos que hacen respawn
        '''
        for obj in respawn_objects:
            obj.limit_xy=self.limit_xy


        # Sección generación de clima
        '''
        Si la cantidad de objetos en el eje "x" es mayor que cero, entonces se procedera a generar la lluvia.

        rain_multipler; Es para multiplicar la cantidad de lluvia.
        
        El primer ciclo for; con un rango del 0 al rain_multipler, es para generar la lluvia.
        
        more_distance_xy; es para adicionar en la posicion de generación de lluvia mas espacio, ya sea en el eje x o en el y.
        
        Ciclo for con un:
        Rango de more_distance_x a ultimo objeto en eje "x", mas la mitad del ultimo objeto en eje y mas la more_distance_x.
        
        Cada valor obtenido de este ciclo, generara una lluvia, en la posición x. Que sera el valor actual obtenido del ciclo. Y en el eje "y" en un rango -pixel_space a -pixel_space*16
        '''
        if (Map.climate == 'rain' or Map.climate == 'acid') and xy[0] > 0:
            if Map.climate == 'rain': damage = False
            if Map.climate == 'acid': damage = True

            rain_multipler = 2
            for generate_number in range(0, rain_multipler):
                more_distance_xy = [8, 0]
                for x in range( more_distance_xy[0], xy[0]+(xy[1]//2)+more_distance_xy[0] ):
                    #print(x)
                    ClimateRain(
                     position=(
                        #random.randint(
                        #    x*pixel_space_to_scale, (x*pixel_space_to_scale) + pixel_space_to_scale*1
                        #),
                        x*pixel_space_to_scale,
                        -( random.randint( pixel_space_to_scale, pixel_space_to_scale*16) )
                     ),
                     transparency_collide=transparency_collide, transparency_sprite=transparency_sprite_rain,
                     damage=damage, climate_objects=climate_objects, damage_objects=damage_objects,
                     player_objects=player_objects, solid_objects=solid_objects,
                     layer_all_sprites=layer_all_sprites
                    )
            print( 
                f'rain multipler: {rain_multipler}\n' 
                f'raindrops: {x}'
            )
 
current_map = Map
read_Map( Map=current_map, level=data_CF.current_level )
render_map = Start_Map(current_map)
player = Player(
 dict_sprite={
  'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
  'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
 },
 position=render_map.player_spawn, transparency_collide=transparency_collide, 
 transparency_sprite=transparency_sprite, player_objects=player_objects,
 solid_objects=solid_objects, damage_objects=damage_objects, level_objects=level_objects, 
 score_objects=score_objects, jumping_objects=jumping_objects, moving_objects=moving_objects,
 ladder_objects=ladder_objects, particle_objects=particle_objects, anim_sprites=anim_sprites,
 update_objects=update_objects, gun_objects=gun_objects, layer_all_sprites=layer_all_sprites
)
player_spawn_hp = player.hp
player_anim_dead = None
message_skip = False




# Loop dia y noche | Fondo de color de clima
def get_climate( Map ):
    if Map.climate in dict_climate.keys():
        return Map.climate
    else:
        return 'default'

#time_dayloop=data_CF.fps*0 # Tienpo de duración del dia y de la noche.
#time_dayloop=data_CF.fps*0.5 # Tienpo de duración del dia y de la noche.
time_dayloop=data_CF.fps*10 # Tienpo de duración del dia y de la noche.
def Loop_allday( Map ):
    climate = get_climate( Map )
    gradiant_color = GradiantColor( 
        color=dict_climate[climate], transparency=127, divider=16, start_with_max_power=True, 
        #time=data_CF.fps*120
        time=time_dayloop
        #time=data_CF.fps*0
    )
    gradiant_color.climate=climate
    
    print( 
        f'climate start color: {gradiant_color.start_color}\n'
        f'climate end color: {gradiant_color.end_color}'
    )
    return gradiant_color

loop_allday = Loop_allday( current_map )

background_surf = pygame.Surface( scale_surface_size, pygame.SRCALPHA )
background_surf.fill( loop_allday.current_color )



# Funcion Musica
# Crear un evento personalizado para el final de la pista
end_of_track_event = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(end_of_track_event)


# Nota: Tienen que ser directorios de archivo, no objetos Sound
class Play_background_music():
    def __init__(self, climate_sound=data_CF.climate_sound, music=data_CF.music,  climate='default' ):
        self.climate = climate
        self.music = music
        self.climate_sound = climate_sound
        self.play_music = False
        self.list_music = []
        self.update_list_music()
        self.count_played = 0
        self.current_music = None
        self.limit = 0


    def update_list_music(self):
        if self.list_music == []:
            for key in all_music.keys():
                if not key.startswith('climate_'):
                    self.list_music.append( all_music[key] )

    def play(self):
        # Detectar si existe musica de fondo
        for key in all_music.keys():
            if self.climate != key:
                self.climate_sound = False

        #print(self.count_played)
        if self.music == True:
            if self.climate_sound == True:
                self.play_music = random.choice( [True, True, False, False, False] )
            else:
                self.play_music = True

        if self.count_played == 0:
            # Seleccionar una musica aleatoria | Seleccionar modo clima o modo musica
            if self.music == True and self.play_music == True:
                # Reproducir musica y clima
                self.update_list_music()
                if isinstance(self.list_music, list):
                    self.current_music = random.choice( self.list_music )
                    self.list_music.remove(self.current_music)
                #else:
                #    self.list_music = all_music['music']
                self.limit = 0
                    
            if self.climate_sound:
                # Solo reproducir el clima
                self.current_music = all_music[self.climate]
                self.limit = 4

        elif self.count_played == self.limit:
            # Llego al limite, reproducir otra musica aletoria.
            self.count_played = -1
        
        # Cargar y reproducir cancion
        if isinstance(self.current_music, str):
            pygame.mixer.music.load( self.current_music )
            pygame.mixer.music.set_volume( data_CF.volume )
            pygame.mixer.music.play()

            # Contador de veces reporducidas (Solo contara cuando el limite de contado sea mayor que cero)
            if self.limit > 0:
                self.count_played += 1

play_background_music = Play_background_music( 
    music=data_CF.music, climate=f'climate_{get_climate( current_map )}' 
)
play_background_music.play()


# Función nubes de fondo
# rehacer
def create_clouds(c_number = int( (scale_surface_size[0]//3.75)//pixel_space_to_scale) ): #16 nubes por defecto
    '''
    Imagenes de fondo | Nubes de fondo
    # Si hay demasiadas nubes se dejaran de crear.
    # Se creara una nube de forma random, con posibilidades 1-6
    '''
    c_size = [scale_surface_size[0]//c_number, scale_surface_size[1]//c_number]

    pos = [0, 0]
    clouds = 0
    for y in range(0, c_number):
        pos[1] = c_size[1]*(y)
        for x in range(0, c_number):
            pos[0] = c_size[0]*(x)

            create = random.choice( [True, 2, 3, 4, 5, 6] )
            if data_CF.show_collide == False: transparency_sprite_collide=random.choice([8,16,32])
            else: transparency_sprite_collide=0
            if create == True:
                clouds += 1
                Cloud(
                    size=c_size, position=pos,
                    transparency_collide=transparency_collide, transparency_sprite=transparency_sprite_collide,
                    anim_sprites=anim_sprites, nocamera_back_sprites=nocamera_back_sprites
                )
    print( f'cloud_number: {x}' )




# Iniciar Funciones y contantes necesarias
# Funcion nubes
if data_CF.show_clouds == True:
    create_clouds()


# Funcion del mapa
score = 0

#for plat in solid_objects:
#    plat.limit_collision()

# Funcion juego completado
gamecomplete = False

# Función cretidos
credits_fps = data_CF.fps*4
credits_count = 0

go_credits = False




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
    
    xy_return = [ max(pos_x), max(pos_y)]
    print(f'limit_xy: {xy_return}')
    return xy_return
limit_xy = render_map.limit_xy#get_limit_xy()




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
    
    xy_return = [int(scroll_float[0]), int(scroll_float[1])]
    print(f'start scroll: {xy_return}')
    return xy_return
scroll_float = [0,0]
scroll_float = start_scroll(
    pos_xy=[player.rect.x, player.rect.y], display_xy=scale_surface_size, limit_xy=limit_xy,
    difference_xy=[pixel_space_to_scale*2, pixel_space_to_scale*3]
)




# Sol solecito
# Total en tardar el loop del sun: data_CF.fps*240
HappySun = Sun( 
 size=[pixel_space_to_scale,pixel_space_to_scale], time=time_dayloop*2,
 display=[ scale_surface_size[0]+pixel_space_to_scale, scale_surface_size[1] ], divider=24,
 anim_sprites=anim_sprites, lighting_objects=lighting_objects, nocamera_back_sprites=nocamera_back_sprites
)
#HappySun = Sun( time=data_CF.fps*0, display=[ scale_surface_size[0]+pixel_space_to_scale, scale_surface_size[1] ], divider=24)

light_dict = {}

def create_light():
    '''
    Función para crear iluminación en objetos luminosos
    '''
    for key in light_dict.keys():
        light_dict[key].kill()
    light_dict.clear()

    for object in lighting_objects:
        sprite = pygame.sprite.Sprite()
        sprite.surf = surface_bloom(
            size=object.surf.get_size(), alpha_range=[127, 0], 
            color=generic_colors('yellow'), middle_color=False
        )
        sprite.surf.get_rect()
        sprite.rect = sprite.surf.get_rect( 
            topleft=[object.rect.x-sprite.surf.get_width(), object.rect.y-sprite.surf.get_height()] 
        )
        sprite.color = object.color
        nocamera_back_sprites.add(sprite)
        light_dict.update( {object : sprite} )

create_light()




# Prueba de enemigo
'''
enemy = Enemy( 
 position=render_map.player_spawn, 
 solid_objects=solid_objects, damage_objects=damage_objects, level_objects=level_objects, 
 score_objects=score_objects, jumping_objects=jumping_objects, moving_objects=moving_objects,
 ladder_objects=ladder_objects, particle_objects=particle_objects, anim_sprites=anim_sprites,
 update_objects=update_objects, layer_all_sprites=layer_all_sprites, respawn_objects=respawn_objects
)
enemy.limit_xy = limit_xy
#enemy.left = True
#enemy.jump = True
#enemy.walk = True
'''




# Bucle del juego
exec_game = True
while exec_game:
    for event in pygame.event.get():
        if event.type == end_of_track_event:
            play_background_music.play()
        if event.type == pygame.KEYDOWN:
            if event.key == player.pressed_jump:
                # Si se preciona la tecla para saltar.
                if isinstance(render_map.message_start, str):
                    # Evitar mensaje
                    render_map.message_start = None
                    
                if credits_count == credits_fps*2:
                    # Cerrar juegito si estamos en el mensaje para saltar los credito
                    exec_game = False

            elif event.key == pygame.K_r and go_credits == False:
                # Por si se bugea el juego, poder matar al jugador y por consecuensia reiniciar el nivel
                if player.hp > 0 and not isinstance(render_map.message_start, str):
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
    #player.move()
    #player.update(False)
    



    # Función camara / Scroll
    player_pos = [player.rect.x, player.rect.y]

    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]
    diference = pixel_space_to_scale
    for index in range(0, 2):
    #if True == False: # Para evitar scroll
        '''
        Para que funcione la camara solo se necesita de esto:
        scroll_float[index] += (player_pos[index] -scroll_float[index] -scale_surface_size[index]/2)/4
        
        Lo demas esta relacionado con evitar que se mueva la camara, cuando se llega a un cierto limite.
        '''
        # en los "((scale_surface_size[index]/2) )" antes tenia "((scale_surface_size[index]/2) -pixel_space_to_scale)
        if not (
            ( player_pos[index] + ((scale_surface_size[index]/2) ) > limit_xy[index] ) or
            ( player_pos[index] - ((scale_surface_size[index]/2) ) < 0)
        ):
            # Mover scroll
            scroll_float[index] += (player_pos[index] -scroll_float[index] -scale_surface_size[index]/2)/4
        else:
            # Detectados limites de mapa/scroll | Evitar movimiento de scroll/camera
            # Nota: El limite positivo debe estar un bloque/grid/cuadricula de mas
            # more_pixels, sirve para añadir mas pixeles en el lado pistivo "x" o "y".
            #print( 'posicion jugador: ', player_pos[index])
            #print( 'posicion jugador en patalla: ', player_pos[index]-scroll_int[index])
            #print( 'scroll: ', scroll_int[index])
            #print( 'limite: ', limit_xy[index])
            #print( 'pantalla', scale_surface_size[index])
            more_pixels = pixel_space_to_scale
            if player_pos[index]-scroll_float[index] > scale_surface_size[index]/2 + more_pixels:
                aditional = limit_xy[index] -(scroll_float[index] + scale_surface_size[index])
                #if scroll_float[index] < limit_xy[index]-scroll_float[index]:
                scroll_float[index] += aditional + more_pixels
                # limite - (scroll + pantalla)
            elif player_pos[index]-scroll_float[index] < scale_surface_size[index]/2 -more_pixels:
                scroll_float[index] -= scroll_float[index]
                
    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]  
    


    # Funciones / Objetos / Puntos
    score = player.score
    #for obj in score_objects:
    #    if obj.point == True:
    #        obj.remove_point()
    #        score += 1

            
    # Función actualizar animacion de sprites.
    for sprite in anim_sprites:
        sprite.anim()
        
    # Función Objetos actualizables
    for obj in update_objects:
        obj.update()
    
    # Función respawn
    for obj in respawn_objects:
        if obj.dead and obj.anim_fin:
            obj.hp = obj.initial_hp
            obj.rect.topleft = obj.position
            obj.change_direction()
    
    
    # Función clima
    for climate in climate_objects:
        '''
        Actualizar el objeto tipo clima
        Respawn cuendo el objeto colisione y cuando el tiempo para respawn pase. Reinciar tiempo de respawn al spawnear.
        '''
        climate.update()

        # Respawn si sale da pantalla.
        if (climate.rect.y > limit_xy[1]):
            climate.rect.topleft = climate.position
    
    
    # Función | Player | Limite del mapa
    if player.rect.x > limit_xy[0] +pixel_space_to_scale or player.rect.x < 0:
        player.hp = -1
    elif player.rect.y > limit_xy[1] +pixel_space_to_scale or player.rect.y < 0:
        player.hp = -1
    
    
    # Función | Level | Cambiar de nivel | Acabar juego
    for sprite in level_objects:
        sprite.update()
        level = sprite.level
        if not sprite.level == None:
            # El juego ha sido completado porque el jugador a llegado el checkpoint.
            if sprite.gamecomplete == True:
                print('Gamecomplete Saved')
                gamecomplete = True
                sprite.kill()
                save_gamecomplete(level=data_CF.current_level.replace(dir_maps, '') , score=score)
                
                print('Change the level')
                data_CF.current_level = level
                save_CF( data_CF )

            if gamecomplete == False:
                print('Game saved and change the level')
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
                 dict_sprite={
                  'side-x' : get_image(
                   'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2]
                  ),
                  'side-y' : get_image(
                   'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2]
                  )
                 },
                 position=render_map.player_spawn, transparency_collide=transparency_collide, 
                 transparency_sprite=transparency_sprite, player_objects=player_objects,
                 solid_objects=solid_objects, damage_objects=damage_objects, level_objects=level_objects,
                 score_objects=score_objects, jumping_objects=jumping_objects, moving_objects=moving_objects,
                 ladder_objects=ladder_objects, update_objects=update_objects, 
                 particle_objects=particle_objects, anim_sprites=anim_sprites,
                 gun_objects=gun_objects,layer_all_sprites=layer_all_sprites
                )
                player.score = score
                player_spawn_hp = player.hp
                
                # Clima | Color de fondo
                if not loop_allday.climate == get_climate( current_map ):
                    #loop_allday = Loop_allday( current_map )
                    loop_allday.climate = get_climate( current_map )
                    loop_allday.color = dict_climate[ get_climate( current_map ) ]
                    loop_allday.restart()
                    HappySun.restart()
                    
                # Clima | Sonido de fondo
                play_background_music.climate=f'climate_{get_climate( current_map )}'
                if play_background_music.play_music == False:
                    # Forzar el cambiado de music si no se esta reproduciondo el sonido del clima como musica.
                    play_background_music.play()
                
                # Posicionar camara y establecer limites de camara.
                limit_xy = render_map.limit_xy #get_limit_xy()
                scroll_float = [0,0]
                scroll_float = start_scroll(
                    pos_xy=[player.rect.x, player.rect.y], display_xy=scale_surface_size, limit_xy=limit_xy,
                    difference_xy=[pixel_space_to_scale*2, pixel_space_to_scale*3]
                )
    
    
    
    
    # Ilumination
    for key in light_dict.keys():
        if light_dict[key].color != key.color:
            light_dict[key].surf = surface_bloom(
                size=key.surf.get_size(), alpha_range=[127, 0], 
                color=key.color, middle_color=False
            )
        light_dict[key].rect.topleft = (
            key.rect.x - key.rect.width, 
            key.rect.y - key.rect.height
        )

    # Objetos / Mostrar / Los sprites de atras, que no puede mover la camara.
    for sprite in nocamera_back_sprites:
        display.blit(sprite.surf, sprite.rect)
    
    '''
    # Objetos con iluminacion
    for sprite in lighting_objects:
        # Generar lusesillas
        size = [sprite.rect.width, sprite.rect.height]
        surf = surface_bloom(
            size=size, alpha_range=[127, 0], color=sprite.color, middle_color=False
        )
        position = ( sprite.rect.x-size[0], sprite.rect.y-size[1] )
        display.blit(surf, position)
    '''


    # Función renderizado de sprites / Mostrar / Todos los sprites / Layer Capas
    for sprite in layer_all_sprites.sprites():
        # Detectar que el sprite no sebrepase la pantalla
        display_collision = scroll_display_collision(
         [sprite.rect.x, sprite.rect.y], scroll_int, scale_surface_size, [pixel_space_to_scale*2, pixel_space_to_scale*1]
        )

        # Si el esprite esta en pantalla, mostrarlo.
        if display_collision == None:
            display.blit(
                sprite.surf,
                ( sprite.rect.x -scroll_int[0], sprite.rect.y -scroll_int[1] )
            )

            # Sprite visible o no
            sprite_alpha = sprite.surf.get_alpha()
            visible = sprite_alpha > 0

            # Estos boleanos deberan de estar en la config. En el DB.
            if data_CF.contrast or data_CF.shadows:
                # Color del dia invertido
                invert_day_color = invert_rgb_color( loop_allday.current_color )
                invert_min_color = []
                normal_max_color = []
                max_color = int( max(loop_allday.current_color)*0.5 )
                min_color = int( min(invert_day_color) )
                for x in range(0, 3):
                    normal_max_color.append( max_color )
                    invert_min_color.append( min_color )

            if visible:
                # Color de contraste para sprite
                if data_CF.contrast:
                    contrast_mask = pygame.Surface( sprite.surf.get_size(), pygame.SRCALPHA)
                    contrast_mask.fill( normal_max_color )
                    contrast_mask.set_alpha( int(sprite_alpha*0.125) )
                    contrast_mask = get_mask_for_surface( sprite.surf, mask=contrast_mask )
                    display.blit(
                    contrast_mask, ( sprite.rect.x -scroll_int[0], sprite.rect.y -scroll_int[1] )
                    )

                # Sombra
                if data_CF.shadows:
                    # [255, 169]
                    # Invertir color
                    shadow = create_mask_gradient(
                    sprite.surf, alpha_range=[ int(sprite_alpha*0.25), 0],
                    color=invert_min_color, dimension=0, positive=False
                    )
                    display.blit(
                        shadow,
                        ( sprite.rect.x -scroll_int[0], sprite.rect.y -scroll_int[1] )
                    )

            # Volumen
            sprite.volume=float(data_CF.volume)
        else:
            sprite.volume=float(0)
    
    
    # Funcion | Player Muerto/Dead
    if player.hp <= 0:
        if player.anim_fin == True:
            # Finalizar animacion y spawnear al jugador
            player.not_move=False
            player.transparency_sprite = transparency_sprite
            player.hp = player_spawn_hp
            #if data_CF.show_sprite == True: player.transparency_sprite = 255
            #player.show_sprite = data_CF.show_sprite
            player.rect.topleft = render_map.player_spawn
            player.rect.x += (pixel_space_to_scale -player.rect.width)//2

            scroll_float = start_scroll(
                pos_xy=[player.rect.x, player.rect.y], display_xy=scale_surface_size, limit_xy=limit_xy,
                difference_xy=[pixel_space_to_scale*2, pixel_space_to_scale*3]
            )
                
                



    # Mostrar mensaje de fin de juego y creaditos, y Cerrar el juego.        
    if gamecomplete == True:
        print('Fin')
        if go_credits == False:
            #render_map.message_start = Lang.get_text('gamecomplete')
            go_credits = True
    
    
    
    
    # Sección de HUD y texto del juego
    # Mostrar Vida de jugador
    text_hp = font_normal.render( str(player.hp), True, generic_colors('green') )
    display.blit(
        text_hp, ( (scale_surface_size[0])-(size_font_normal*3), size_font_normal )
    )
    
    # Fondo negro | Ocultar todo
    if credits_count >= credits_fps:
        pygame.draw.rect(
            display, generic_colors('black'),
            (
                0, 0, scale_surface_size[0], scale_surface_size[1]
            )
        )
    
    # Mostrar Puntaje
    text_score = font_normal.render( str(score), True, generic_colors('yellow') )
    display.blit(
        text_score, ( (scale_surface_size[0])-(size_font_normal*3), size_font_normal*2 )
    )
    
    
    
    
    # Función | Mensaje de inicio
    if isinstance(render_map.message_start, str) or credits_count == credits_fps*2:
        # No moverse player mientras se ve el mensaje
        player.not_move = True

        # Para cerrar el juego
        if credits_count == credits_fps*2:
            message = ''
        else:
            message = render_map.message_start
            #message = "Desde los años noventa se dice que el texto es texto. Y tambien ahora es texto esta es una prueba de mucho texto, escribir mucho texto en pantalla, es bueno para la salud mental. Perros locos, loquitas. Bueno eso es todo amigos hasta la proxima."

        # Mensaje tiene surf rect y anchura de mansaje
        text_message = font_normal.render(
            message, True, generic_colors('white')
        )
        rect_text = text_message.get_rect()
        width_message = rect_text.width

        # Determinar diviciones de texto si sobrepasa la pantalla. En base al limit_of_text
        limit_of_text = scale_surface_size[0]

        text_parts = surf_limit_width( text_message, limit_of_text )


        if len(text_parts) > 0:
            for x in range( len(text_parts) ):
                # Parte
                message_part = text_parts[x]
            
                # Mostrar parte de mensaje
                rect_text = message_part.get_rect()
                position = [
                    (scale_surface_size[0]//2)-(rect_text.width//2),
                    size_font_normal * (x+1)
                ]

                pygame.draw.rect(
                    display, generic_colors('black'), (
                        position[0], position[1],
                        rect_text.width, rect_text.height
                    )
                )

                display.blit(
                    message_part, position
                )
            
            
        else:
            # Mostrar todo el mensaje sin dividirlo.
            position = [
                (scale_surface_size[0]//2)-(rect_text.width//2),
                size_font_normal
            ]

            pygame.draw.rect(
                display, generic_colors('black'), (
                    position[0], position[1],
                    rect_text.width, rect_text.height
                )
            )

            display.blit(
                text_message, position
            )
        
        # Iformación acerca de como cuntinuar tras el mensaje
        text_continue = font_normal.render(
            f"{Lang.get_text('continue_jump')}...", True, generic_colors('white')
        )
        position = [size_font_normal, scale_surface_size[1]-(size_font_normal*2)]
        
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
    else:
        # Poder moverse
        player.not_move = False
           
    
    
    # Juego completado:
    if go_credits == True:
        player.not_move = True
        if credits_count >= credits_fps:
            if credits_count < credits_fps*2:
                credits_count += 1
        
            # Texto creditos
            text_credits = font_normal.render(
                Lang.get_text('credits'), True, generic_colors('yellow')
            )
            position = [(scale_surface_size[0]//2)-(text_credits.get_rect().width//2), (size_font_normal//2)]
        
            display.blit(
                text_credits, (
                    position[0],
                    position[1]
                )
            )
        
            # Texto nombre del creador 
            text_by = font_normal.render(
                credits(), True, generic_colors('green')
            )
            position = [
                (scale_surface_size[0]//2)-(text_by.get_rect().width//2), (scale_surface_size[1]//2)-(size_font_normal//2)
            ]
        
            display.blit(
                text_by, (
                    position[0],
                    position[1]
                )
            )

        else:
            credits_count += 1

            # Mensaje tiene surf rect y anchura de mansaje
            text_message = font_normal.render(
                Lang.get_text("gamecomplete"), True, generic_colors('white')
            )
            rect_text = text_message.get_rect()
            width_message = rect_text.width

            # Determinar diviciones de texto si sobrepasa la pantalla. En base al limit_of_text
            text_parts = surf_limit_width( text_message, scale_surface_size[0] )
            
            if len(text_parts) == 0:
                text_parts.append( text_message )

            for x in range( len(text_parts) ):
                # Parte
                message_part = text_parts[x]
            
                # Mostrar parte de mensaje
                rect_text = message_part.get_rect()
                position = [
                    (scale_surface_size[0]//2)-(rect_text.width//2),
                    (scale_surface_size[1]//2)-(rect_text.height//2) + ( size_font_normal * (x) )
                ]

                pygame.draw.rect(
                    display, generic_colors('black'), (
                        position[0], position[1],
                        rect_text.width, rect_text.height
                    )
                )

                display.blit(
                    message_part, position
                )
    

    # Sección adicionar todos los sprites a una superficie y agregarlo a la pantalla
    surf = pygame.transform.scale(display, [data_CF.disp[0]*1, data_CF.disp[1]*1] )
    window.blit(surf, (0,0) )
    
    # Fin
    clock.tick(data_CF.fps)
    pygame.display.update()

pygame.quit()
