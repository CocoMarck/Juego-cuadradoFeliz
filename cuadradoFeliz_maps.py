from entities import CF, Map
from data.CF_info import *
from logic.pygame.Modulo_pygame import *
from logic.pygame.CF_function import *
import pygame, os, random
from pygame.locals import *


# Inicio
pygame.display.set_caption(game_title)
display = pygame.display.set_mode( data_CF.disp )
clock = pygame.time.Clock()




# Objetos
layer_all_sprites = pygame.sprite.LayeredUpdates()
grid_objects = pygame.sprite.Group()




class object_grid( pygame.sprite.Sprite ):
    def __init__(self, size=[data_CF.pixel_space, data_CF.pixel_space], position=[0,0], image=None ):
        super().__init__()

        if image is None:
            transparency = 47
            color = 'black'
            layer = 1
            
            self.surf = pygame.Surface( size, pygame.SRCALPHA )
            self.surf.fill( generic_colors(color, 0) )

            square = pygame.sprite.Sprite()
            square.surf = pygame.Surface( [size[0], size[1]*0.125], pygame.SRCALPHA )
            square.surf.fill( generic_colors(color, transparency) )
            square.rect = square.surf.get_rect( topleft=position )
            layer_all_sprites.add(square, layer=layer)
            
            square = pygame.sprite.Sprite()
            square.surf = pygame.Surface( [size[0], size[1]*0.125], pygame.SRCALPHA )
            square.surf.fill( generic_colors(color, transparency) )
            square.rect = square.surf.get_rect( topleft=[ position[0], position[1]+(size[1]-size[1]*0.125) ] )
            layer_all_sprites.add(square, layer=layer)
            
            square = pygame.sprite.Sprite()
            square.surf = pygame.Surface( [size[0]*0.125, size[1]], pygame.SRCALPHA )
            square.surf.fill( generic_colors(color, transparency) )
            square.rect = square.surf.get_rect( topleft=position )
            layer_all_sprites.add(square, layer=layer)
            
            square = pygame.sprite.Sprite()
            square.surf = pygame.Surface( [size[0]*0.125, size[1]], pygame.SRCALPHA )
            square.surf.fill( generic_colors(color, transparency) )
            square.rect = square.surf.get_rect( topleft=[ position[0]+(size[0]-size[0]*0.125), position[1] ] )
            layer_all_sprites.add(square, layer=layer)
        else:
            if image == 'limit':
                self.surf = pygame.Surface( size )
                self.surf.fill( generic_colors('red') )
            else:
                self.surf = get_image( image=image, number=0, size=size )

        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=0)
        grid_objects.add(self)




# Generador de cuadritos para hacer el mapa
current_map = Map
read_Map( current_map, level=data_CF.current_level )
#read_Map( current_map, level='./resources/maps/cf_map_default.txt' )
#read_Map( current_map, level='./resources/maps/cf_map.txt' )

#object_grid()

player_spawn_xy = [0,0]
xy = [0, 0]
for line in current_map.list_map:
    xy[0] = 0
    position = [ xy[0], xy[1]*data_CF.pixel_space]
    xy[1] += 1
    
    for character in line:
        position[0] = xy[0]*data_CF.pixel_space

        '''
        Tipos de objeto
        "." "#" = Espacios
        "p" = Floor
        ""
        '''
        dict_preset = {
            '.': [None, None], 
            '#': [None, None],
            '|': ['limit', None],

            'j': ['player_not-move', 2],

            'p': ['stone', None],
            'P': ['stone', 2 ],
            '+': ['stone', None ],
            '-': ['stone', None ],
            '-': ['stone', None ],

            'H': ['ladder', None ],
            '_': ['trampoline', None ],

            '^': ['spike', None],
            'A': ['spike', 2 ],
            '!': ['spike', None],
            '\\': ['spike', None ],

            '*': ['star-pointed', None],
            'Y': ['star-pointed', None],
            'X': ['star-pointed', None ],

            'x': ['elevator', None],
            'y': ['elevator', None],

            's': ['coin', None],

            '0': ['level_change', None],
            'F': ['level_change', None],
        }
        for preset in dict_preset.keys():
            if character == preset:
                # Agregar espacio y cuadrito
                xy[0] += 1
                object_grid( position=position )
                
                # Agregar imagen si es que tiene
                if type(dict_preset[preset][0]) == str:
                    if dict_preset[preset][1] is None:
                        # Establecer objeto tipo imagen
                        size = [data_CF.pixel_space, data_CF.pixel_space]
                        object_grid(
                            position=position, size=size, image=dict_preset[preset][0] 
                        )
                    else:
                        # Establecer nuevo tamaño
                        size = [
                            data_CF.pixel_space*dict_preset[preset][1], 
                            data_CF.pixel_space*dict_preset[preset][1]
                        ]
                        
                        # Detectar si es el sprite del jugador o no
                        if dict_preset[preset][0] == 'player_not-move':
                            new_pos = [
                                position[0]-size[0]/4,
                                position[1]-size[1]/2
                            ]
                            player_spawn_xy = new_pos
                        else:
                            new_pos = position
                            
                        # Establecer objeto
                        object_grid(
                            position=new_pos, size=size, image=dict_preset[preset][0]
                        )




# Camara | Scroll
scroll_float = [0,0]




# Posición de camara
camera_xy = player_spawn_xy
move_up = False
move_down = False
move_left = False
move_right = False




# Función Scroll/Camara | Posicionar camara en donde esta el jugador
def start_camera():
    scroll_float = [0,0]
    scroll_float[0] += (camera_xy[0] -scroll_float[0] -data_CF.disp[0]/2)
    scroll_float[1] += (camera_xy[1] -scroll_float[1] -data_CF.disp[1]/2)
    
    return [int(scroll_float[0]), int(scroll_float[1])]
                        
scroll_float = start_camera()
scroll_int = [0,0]



# Loop del juego
exec_game = True
while exec_game:
    # Eventos de juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exec_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Detección de mouse
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                # Click izquierdo
                mouse_pos = pygame.mouse.get_pos()
                for obj in grid_objects:
                    if obj.rect.collidepoint( mouse_pos[0]+scroll_int[0], mouse_pos[1]+scroll_int[1] ):
                        # Click en grid
                        print( obj.rect.x, obj.rect.y ) # Posicion en pixeles
                        print( 
                            (obj.rect.x) //data_CF.pixel_space, 
                            (obj.rect.y) //data_CF.pixel_space 
                        ) # Posición en cuadros/rejillas/cuadriculas/mallas/
            if middle:
                # Click Rueda de mouse
                mouse_movement = pygame.mouse.get_rel()

                if mouse_movement[1] < 0:
                    move_up = True
                if mouse_movement[1] > 0:
                    move_down = True
                
                if mouse_movement[0] < 0:
                    move_left = True
                if mouse_movement[0] > 0:
                    move_right = True
        if event.type == pygame.MOUSEBUTTONUP:
            move_up = False
            move_down = False
            move_left = False
            move_right = False
                    

        if event.type == pygame.KEYDOWN:
            if event.key == player_key['up']:
                move_up = True
            if event.key == player_key['down']:
                move_down = True

            if event.key == player_key['left']:
                move_left = True
            if event.key == player_key['right']:
                move_right = True    
        if event.type == pygame.KEYUP:
            if event.key == player_key['up']:
                move_up = False
            if event.key == player_key['down']:
                move_down = False

            if event.key == player_key['left']:
                move_left = False
            if event.key == player_key['right']:
                move_right = False
    
    
    
    
    # Limpiar pantalla (agregar esta línea)
    display.fill( generic_colors('green') )
    
    
    
    
    # Movimiento camara:
    if move_up == True:
        camera_xy[1] -= data_CF.pixel_space
    if move_down == True:
        camera_xy[1] += data_CF.pixel_space
        
    if move_left == True:
        camera_xy[0] -= data_CF.pixel_space
    if move_right == True:
        camera_xy[0] += data_CF.pixel_space

    
    
    
    # Función scroll | Camara
    scroll_float[0] += (camera_xy[0] -scroll_float[0] -data_CF.disp[0]/2)/4
    scroll_float[1] += (camera_xy[1] -scroll_float[1] -data_CF.disp[1]/2)/4
    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]
    
    
    # Objetos / Mostrar / Todos los sprites
    for sprite in layer_all_sprites.sprites():
        display.blit(
            sprite.surf, 
            (
                sprite.rect.x -scroll_int[0],
                sprite.rect.y -scroll_int[1]
            )
        )
    
    
    
    
    # Fin
    pygame.display.update()
    clock.tick( data_CF.fps )
pygame.quit()