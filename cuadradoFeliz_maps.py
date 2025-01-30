from entities import CF, Map
from data.CF_info import *
from data.CF_data import (save_Map, dict_object, prefix_object, return_map, dict_climate)
from logic.pygame.Modulo_pygame import *
from logic.pygame.CF_function import *
import pygame, os, random
from pygame.locals import *


# Inicio
pygame.display.set_caption(game_title)
display = pygame.display.set_mode( data_CF.disp )
clock = pygame.time.Clock()



# Surface | Para mostrar los objetos en solo en una perte de la pantalla
# Se utilizara size_display_edit, para el funcionamiento del scroll
# Se usara difference_display_edit, para el posicionamiento del displa edit en el display. Y tambien para la pos del mouse al aplicar un evento.
size_display_edit = [ int(data_CF.disp[0]*0.8), int(data_CF.disp[1]*0.8) ]
difference_display_edit = [ 
    (data_CF.disp[0]-size_display_edit[0])//2,
    (data_CF.disp[1]-size_display_edit[1])//2
]
display_edit = pygame.Surface( size_display_edit )




# Objetos de interfaz agregar boton.
buttons = pygame.sprite.Group()
interface_background = pygame.sprite.Group()
class Button(pygame.sprite.Sprite):
    def __init__(
        self, font=pygame.font.SysFont, text=str, use_lang=False,
        color_text=[int,int,int], color_background=(int,int,int,int),
        position_xy=[int,int], size_xy=[int, int] 
    ):
        super().__init__()
        
        # Parametros
        self.text = text
        self.color_text = color_text
        self.spawn_xy = position_xy
        
        # Cambiar tamaño de todo o no
        change_size = True
        if isinstance(size_xy, list):
            for item in size_xy:
                if not isinstance(item, int):
                    change_size = False
        else:
            change_size = False
        
        # Fondo para el boton o no
        set_background = True
        if isinstance(color_background, tuple):
            for item in color_background:
                if isinstance(item, int):
                    if item > 255:
                        set_background = False
                else:
                    set_background = False
        else:
            set_background = False
        
        # Superficie y rectangulo
        # Utilizar la función Language
        # Cambiar tamaño del texto escrito
        if use_lang == True:
            text_ready = get_text(self.text)
        else:
            text_ready = self.text
        self.surf = font.render(text_ready, True, self.color_text)
        if change_size == True:
            self.surf = pygame.transform.scale( self.surf, size_xy )
        self.rect = self.surf.get_rect( topleft=self.spawn_xy )
        
        # Fondo para el texto
        if set_background == True:
            self.background = pygame.sprite.Sprite()
            self.background.surf = pygame.Surface( (self.rect.width, self.rect.height) )
            self.background.surf.fill( color_background )
            self.background.rect = self.background.surf.get_rect( topleft=self.spawn_xy )
            interface_background.add( self.background )
        else:
            self.background = None

        # Rectangulo y agregar a los sprites
        buttons.add( self )


font_str='monospace'
font_size = int(data_CF.pixel_space*0.75)
font=pygame.font.SysFont(font_str, font_size)
color_background=generic_colors('white')
color_text=generic_colors('black')
use_lang=False

list_option = ['message', 'save', 'play']
posx = data_CF.disp[0]//(len(list_option)+1)
for index in range(0, len(list_option)) :
    Button(
        font=font, text=list_option[index], use_lang=use_lang,
        color_text=color_text, color_background=color_background,
        position_xy=[ posx*(index+1), data_CF.pixel_space ]
    )
    print( posx*(index+1) )


posx = data_CF.disp[0]//(len(dict_climate.keys())+1)
posy = data_CF.disp[1] -data_CF.pixel_space*2
for index in range(0, len(dict_climate.keys()) ):
    Button(
        font=font, text=list(dict_climate.keys())[index], use_lang=use_lang,
        color_text=color_text, color_background=color_background,
        position_xy=[ posx*(index+1), posy ]
    )
    


# Tipos de objetos
print( f'prefix objects: "{prefix_object}"')



# Objetos
layer_all_sprites = pygame.sprite.LayeredUpdates()
grid_objects = pygame.sprite.Group()




class object_grid( pygame.sprite.Sprite ):
    def __init__(self, size=[data_CF.pixel_space, data_CF.pixel_space], position=[0,0], image=None ):
        super().__init__()
        
        # Para mostrar cuadricula, ayuda visual.
        transparency = 47
        color = 'black'
        layer = 1
        
        square = pygame.sprite.Sprite()
        square.surf = pygame.Surface( [data_CF.pixel_space, data_CF.pixel_space*0.125], pygame.SRCALPHA )
        square.surf.fill( generic_colors(color, transparency) )
        square.rect = square.surf.get_rect( topleft=position )
        layer_all_sprites.add(square, layer=layer)
        
        square = pygame.sprite.Sprite()
        square.surf = pygame.Surface( [data_CF.pixel_space, data_CF.pixel_space*0.125], pygame.SRCALPHA )
        square.surf.fill( generic_colors(color, transparency) )
        square.rect = square.surf.get_rect(
            topleft=[ position[0], position[1]+(data_CF.pixel_space-data_CF.pixel_space*0.125) ] 
        )
        layer_all_sprites.add(square, layer=layer)
        
        square = pygame.sprite.Sprite()
        square.surf = pygame.Surface( [data_CF.pixel_space*0.125, data_CF.pixel_space], pygame.SRCALPHA )
        square.surf.fill( generic_colors(color, transparency) )
        square.rect = square.surf.get_rect( topleft=position )
        layer_all_sprites.add(square, layer=layer)
        
        square = pygame.sprite.Sprite()
        square.surf = pygame.Surface( [data_CF.pixel_space*0.125, data_CF.pixel_space], pygame.SRCALPHA )
        square.surf.fill( generic_colors(color, transparency) )
        square.rect = square.surf.get_rect( 
            topleft=[ position[0]+(data_CF.pixel_space-data_CF.pixel_space*0.125), position[1] ] 
        )
        layer_all_sprites.add(square, layer=layer)

        # Establecer imagen con size personalizado
        self.image = pygame.sprite.Sprite()
        '''
        if image is None:
            self.image = None

        else:
            self.image = pygame.sprite.Sprite()
            if image == 'limit':
                self.image.surf = pygame.Surface( size )
                self.image.surf.fill( generic_colors('red') )
            else:
                self.image.surf = get_image( image=image, number=0, size=size )
            
            self.image.rect = self.image.surf.get_rect( topleft=position )
            layer_all_sprites.add(self.image, layer=0)
        '''

        # Superficie/collider que sera para los clicks
        self.surf = pygame.Surface( (data_CF.pixel_space, data_CF.pixel_space), pygame.SRCALPHA )
        self.surf.fill( generic_colors(color, 0) )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=0)
        grid_objects.add(self)
        
        # Tipo de objeto
        self.type_object = (
            current_map.list_map
            [ (self.rect.y) //data_CF.pixel_space ]
            [ (self.rect.x) //data_CF.pixel_space ]
        )
        self.xy_spawn = [ (self.rect.y) //data_CF.pixel_space,  (self.rect.x) //data_CF.pixel_space ]
        
        self.update_type_object()
        
    def update_type_object(self):
        # Establecer superficie de colision
        self.surf = pygame.Surface( (self.rect.width, self.rect.height), pygame.SRCALPHA )
        self.surf.fill( (0, 0, 0, 0) )

        # Borrar imagen actual
        if not self.image == None:
            self.image.kill()
        
        # Establecer imagen basado en el tipo de objeto
        if not (self.type_object == '.' or self.type_object == '#'):
            # Parametros necesarios
            image = 'stone'
            color = None
            multipler_size_xy = [1,1]
            position_reduction_xy = [0,0]
            frame_number = 0
            
            # Establecer imagen dependiendo el tipo de caracter.
            if self.type_object == 'j':
                image = 'icon'
            elif self.type_object == '|':
                image = 'limit'
            elif self.type_object == 'p' or self.type_object == 'P':
                image = 'stone'

            elif (
                self.type_object == '^' or self.type_object == 'A' or
                self.type_object == '\\' or self.type_object == '!'
            ):
                image = 'spike'
            elif self.type_object == 'Y' or self.type_object == 'X' or self.type_object == '*':
                image = 'star-pointed'

            elif self.type_object == 's':
                image = 'coin'
                
            elif self.type_object == '_':
                image = 'trampoline'

            elif self.type_object == 'H':
                image = 'ladder'
            elif self.type_object == 'x' or self.type_object == 'y':
                image = 'elevator'

            elif self.type_object == '0' or self.type_object == 'F':
                image = 'level_change'            
            
            # Establecer color
            if (
                self.type_object == '!' or self.type_object == '\\' or 
                self.type_object == '*' or self.type_object == 'X'
            ):
                color = [71, 0, 0]
            elif (
                self.type_object == '^' or self.type_object == 'A' or 
                self.type_object == 'Y'
            ):
                color = [0, 0, 71]
            elif self.type_object == 'F':
                color = [0, 47, 0]

            # Cambiar tamaño y pos
            if self.type_object == 'P' or self.type_object == 'A':
                multipler_size_xy = [2,2]
                
            elif self.type_object == '\\':
                multipler_size_xy[1] = 4
                position_reduction_xy[1] = self.rect.width*(multipler_size_xy[1]-1)

            elif self.type_object == '*':
                multipler_size_xy = [5,3]
                position_reduction_xy[1] = self.rect.height *(multipler_size_xy[1]-1)
            elif (
                self.type_object == '+' or self.type_object == '-' or
                self.type_object == 'x' or self.type_object == 'y'
            ):
                multipler_size_xy[0] = 2
                if self.type_object == '-':
                    position_reduction_xy[0] = self.rect.width
                

            # Establecer objeto tipo sprite para la previsualización
            self.image = pygame.sprite.Sprite()
            if image == 'limit':
                self.image.surf = pygame.Surface( 
                    [self.rect.width*multipler_size_xy[0], self.rect.height*multipler_size_xy[1]] 
                )
                self.image.surf.fill( generic_colors('red') )
            else:
                self.image.surf = get_image( 
                    image=image, number=frame_number,
                    size=[self.rect.width*multipler_size_xy[0], self.rect.height*multipler_size_xy[1]]
                )
                # Establecer color
                if not color == None:
                    self.image.surf.fill( color, special_flags=pygame.BLEND_ADD )
            self.image.rect = self.image.surf.get_rect( 
                topleft=(self.rect.x -position_reduction_xy[0], self.rect.y -position_reduction_xy[1]) 
            )
            layer_all_sprites.add(self.image, layer=0)
            
        # Establecer nuevo tipo de texto en el texto a guardar/cambiar
        current_map.list_map [self.xy_spawn[0]] [self.xy_spawn[1]] = self.type_object



# Funcion para crear un mapa default
def generate_map( size_xy=[int,int], with_limit=True, path='custom', name='custumTumTum' ):
    '''
    Te genera un archivo de texto, que sirve como un mapa para el juego.
    '''
    preset_type = 'cf_map_'
    preset_file = '.txt'
    text = ''
    if isinstance( size_xy[0], int) and isinstance( size_xy[1], int):
        if size_xy[1] >= 4 and size_xy[0] >= 4:
            for line in range(0, size_xy[1]):
                for number in range(0, size_xy[0]):
                    obj = 'space'
                    if with_limit == True:
                        if line == 0 or line == size_xy[1]-1:
                            if number == 0 or number == size_xy[0]-1:
                                obj = 'limit'
                    if line == 1:
                        if number == 1:
                            obj = 'player'

                    text += dict_object[obj]
                text += '\n'
            text += (
                f'$${path}:{name}\n'+
                f'$$default\n'+
                f'$$'
            )

            text_to_save = os.path.join(dir_maps, path, f'{preset_type}{name}{preset_file}')
            if not os.path.isfile(text_to_save):
            #if True == True:
                with open(
                    text_to_save, 
                    'w', encoding="utf-8"
                ) as text_file:
                    text_file.write(text)
            #data_CF.current_level=text_to_save
            #save_CF( data_CF )
            print(text)

            return text_to_save
        else:
            print( 'ERROR: The game min-size is 4x4')
            return data_CF.current_level
    else:
        print( 'ERROR: Only int values' )
        return data_CF.current_level
file_current_map = generate_map( [60, 34] )
print( f'map file: {file_current_map}' )
    



# Generador de cuadritos para hacer el mapa / Renderizado del mapa
current_map = Map
read_Map( current_map, level=file_current_map )
print( 
    f'map path: {current_map.path}\n'
    f'map next level: {current_map.next_level}\n'
    f'map climate: {current_map.climate}\n'
    f'map message start: {current_map.message_start}'
)
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
        for key in dict_object.keys():
            preset = dict_object[key]
            if character == preset:
                # Agregar espacio y cuadrito
                xy[0] += 1
                
                object_grid( position=position )
                if preset == 'j':
                    player_spawn_xy[0] = position[0]
                    player_spawn_xy[1] = position[1]
        '''
        if character == '#':
            # Agregar espacio y cuadrito
            xy[0] += 1
            
            object_grid( position=position )
        '''



# Clima
def get_climate( Map ):
    climate = None
    if Map.climate in dict_climate.keys():
        climate = Map.climate
    else:
        climate = 'default'
    
    if climate != None:
        print(f'climate {climate}: {dict_climate[climate]}')
        return dict_climate[climate]
    #return generic_colors('green')
climate_color = get_climate( current_map )




# Camara | Scroll
scroll_float = [0,0]




# Función | Limite del mapa y de camara | Camara
def get_limit_xy():
    '''
    Limite del mapa
    '''
    '''
    limit_xy = [ [], [] ]
    for sprite in grid_objects:
        if sprite.type_object == '|':
            limit_xy[0].append( sprite.rect.x )
            limit_xy[1].append( sprite.rect.y )
    return [ max(limit_xy[0]),  max(limit_xy[1]) ]
    '''
    pos_x = []
    pos_y = []
    for sprite in grid_objects:
        pos_x.append(sprite.rect.x)
        pos_y.append(sprite.rect.y)
        
    xy = [ max(pos_x), max(pos_y) ]
    print(f'limit xy: {xy}')
    return xy
limit_xy = get_limit_xy()
#input(get_limit_xy())




# Posición de camara en donde esta el jugador
print(f'display edit: {size_display_edit}')
print(f'player spawn: {player_spawn_xy}' )
print( player_spawn_xy[0] - (size_display_edit[0]/2) )
#input()
def start_camera( pos_xy=[0,0], display_xy=[0,0], limit_xy=[0,0], difference_xy=[0,0] ) ->[int, int]:
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
    
    print(f'start camera: {xy}')
    return xy
camera_xy = start_camera(
    pos_xy=player_spawn_xy, display_xy=size_display_edit, limit_xy=limit_xy,
    #pos_xy=player_spawn_xy, display_xy=size_display_edit,
    difference_xy=[data_CF.pixel_space*2, data_CF.pixel_space*3]
)
#camera_xy = [size_display_edit[0]/2,size_display_edit[1]/2]
click_left = False
click_right = False
move_up = False
move_down = False
move_left = False
move_right = False




# Función Scroll/Camara | Posicionar camara en donde esta la posición de camara
def start_scroll( pos_xy=[0,0] ):
    scroll_float[0] += (pos_xy[0] -size_display_edit[0]/2)
    scroll_float[1] += (pos_xy[1] -size_display_edit[1]/2)
    
    xy = [int(scroll_float[0]), int(scroll_float[1])]
    print(f'start scroll: {xy}')
    return xy
                        
scroll_float = start_scroll( camera_xy )
scroll_int = [0,0]


# Seleccion de objeto en el grid
current_object_selected = None


# Loop del juego
run_game = False
exec_game = True
while exec_game:
    click_left = False
    click_right = False
    set_object_prefix = None
    # Eventos de juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exec_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Detección de mouse
            left, middle, right = pygame.mouse.get_pressed()
            if left or right:
                # Click izquierdo
                mouse_pos = pygame.mouse.get_pos()
                click_left = True
                click_right = False
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
            # Detectar letra actual precionada
            letter = event.unicode
            if letter in prefix_object:
                #print( letter )
                set_object_prefix = letter
        
            # Mover camara/scroll
            if event.key == player_key['up']:
                move_up = True
            if event.key == player_key['down']:
                move_down = True

            if event.key == player_key['left']:
                move_left = True
            if event.key == player_key['right']:
                move_right = True    

        if event.type == pygame.KEYUP:
            # Detectar letra actual precionada
            set_object_prefix = None
        
            # Mover camara/scroll
            if event.key == player_key['up']:
                move_up = False
            if event.key == player_key['down']:
                move_down = False

            if event.key == player_key['left']:
                move_left = False
            if event.key == player_key['right']:
                move_right = False
    
    # Ejecutar juego
    if run_game == True:
        exec_game = False
    
    
    
    
    # Limpiar pantalla (agregar esta línea)
    display.fill( generic_colors('black') )
    display_edit.fill( climate_color )
    
    
    
    
    # Movimiento camara | Establecer si direccion de movimietno
    moving_xy = [0,0]
    if move_up == True:
        moving_xy[1] -= data_CF.pixel_space
    if move_down == True:
        moving_xy[1] += data_CF.pixel_space
        
    if move_left == True:
        moving_xy[0] -= data_CF.pixel_space
    if move_right == True:
        moving_xy[0] += data_CF.pixel_space
    
    # Movimienteo camara 
    # Detactar limites | Función para bloquear el movimiento de camara
    '''
    print(limit_xy, 'limit of map')
    print(player_spawn_xy, 'camera spawn')
    print(camera_xy, 'camera')
    print(scroll_float, 'scroll')
    '''

    for index in range(0, 2):
        if camera_xy[index] + ((size_display_edit[index]/2)-data_CF.pixel_space) > limit_xy[index]:
            if moving_xy[index] > 0:
                moving_xy[index] = 0
        elif camera_xy[index] < (size_display_edit[index]/2):
            if moving_xy[index] < 0:
                moving_xy[index] = 0
    camera_xy[0] += moving_xy[0]
    camera_xy[1] += moving_xy[1]
    
    '''
    # Función objetos que limitan la camara
    not_scroll_xy = [False, False]
    for obj in grid_objects:
        if obj.type_object == '|':
            not_scroll_xy = detect_camera_limit(
                limit_xy=[obj.rect.x, obj.rect.y], moving_xy=moving_xy, 
                camera_xy=camera_xy, camera_spawn_xy=player_spawn_xy,
                scroll_float=scroll_float, not_scroll_xy=not_scroll_xy,
                grid_square=data_CF.pixel_space, disp_xy=size_display_edit
            )
                
    
    # Función Scroll/Camara
    if not_scroll_xy[0] == False:
        scroll_float[0] += (camera_xy[0] -scroll_float[0] -size_display_edit[0]/2)/4
    if not_scroll_xy[1] == False:
        scroll_float[1] += (camera_xy[1] -scroll_float[1] -size_display_edit[1]/2)/4
    '''
    # Función scroll | Camara
    scroll_float[0] += (camera_xy[0] -scroll_float[0] -size_display_edit[0]/2)/4
    scroll_float[1] += (camera_xy[1] -scroll_float[1] -size_display_edit[1]/2)/4
    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]
    
    
    
    # Función | Mouse | Cuando se hace click a un objeto
    if click_left == True or click_right == True:
        click_left = False
        
        # Detectar si se clickea una opcion
        button_change_object = False
        button_change_map = False
        button_text = None
        for button in buttons:
            if button.rect.collidepoint( 
                mouse_pos[0],
                mouse_pos[1]
            ):
                for text in dict_object.keys():
                    if button.text == text:
                        button_change_object = True
                        button_text = button.text
                        print( button.text )
                if button_text == None:
                    button_change_map = True
                    button_text = button.text
                    print( button.text )
                    if button.text == 'save':
                        data_CF.current_level = file_current_map
                        save_CF( data_CF )
                        save_Map( current_map, data_CF.current_level )
                    elif button.text == 'play':
                        run_game = True
                    else:
                        if button.text in dict_climate.keys():
                            current_map.climate = button.text
                            climate_color = get_climate( current_map )
                                
        if button_change_object == True:
            # Establecer tipo de objeto
            if not current_object_selected == None:
                if isinstance(button_text, str):
                    current_object_selected.type_object = dict_object[button_text]
                    current_object_selected.update_type_object()
            # Borrar                                
            for button in buttons:
                for text in dict_object.keys():
                    if button.text == text:
                        button.kill()
                        if not button.background == None:
                            button.background.kill()
            

        # Detectar que se clickea un objeto_grid
        if button_change_object == False:
            for obj in grid_objects:
                # Calcular la posición relativa del objeto dentro de la vista previa
                rel_pos_x = obj.rect.x - scroll_int[0]
                rel_pos_y = obj.rect.y - scroll_int[1]

                # Comprobar si el objeto está dentro de la vista previa (display_edit)
                if (0 <= rel_pos_x < size_display_edit[0]) and (0 <= rel_pos_y < size_display_edit[1]):
                    if obj.rect.collidepoint(
                        mouse_pos[0] - difference_display_edit[0] + scroll_int[0],
                        mouse_pos[1] - difference_display_edit[1] + scroll_int[1]
                    ):
                        # Si el objeto está en la vista y se hace clic, realizar la acción
                        #print(obj.rect.x, obj.rect.y)  # Posición en píxeles
                        #print(obj.type_object)
                        #obj.type_object = '.'
                        #obj.update_type_object()
                        current_object_selected = obj
                        
                        number = 0
                        for option in dict_object.keys():
                            Button(
                                font=font, text=option, use_lang=use_lang,
                                color_text=color_text, color_background=color_background,
                                position_xy=[mouse_pos[0], mouse_pos[1] +(font_size*number)]
                            )
                            number+=1
                            
    
    # Funcion cambiar objeto con teclado
    if not current_object_selected == None:
        if not set_object_prefix == None:
            if not set_object_prefix.replace(' ', '') == '':
                #print(set_object_prefix)
                for button in buttons:
                    if button.text in dict_object.keys():
                        button.kill()
                        button.background.kill()
                current_object_selected.type_object = set_object_prefix
                current_object_selected.update_type_object()
                current_object_selected = None


    '''
    if click_left == True or click_right == True:
        for obj in grid_objects:
            if obj.rect.collidepoint( 
                mouse_pos[0]-difference_display_edit[0] +scroll_int[0],
                mouse_pos[1]-difference_display_edit[1] +scroll_int[1]
            ):
                # Click en grid
                # Obtener menu de objetos y seleccionar uno
                print( obj.rect.x, obj.rect.y ) # Posicion en pixeles
                print( obj.type_object )
                obj.type_object = '.'
                obj.update_type_object()
    '''

    
    
    
    # Objetos / Mostrar / Todos los sprites
    for sprite in layer_all_sprites.sprites():
        # Detectar que el sprite no sebrepase la pantalla
        display_collision = scroll_display_collision(
            [sprite.rect.x, sprite.rect.y], scroll_int, size_display_edit, [data_CF.pixel_space, 0]
        )

        # Si el esprite esta en pantalla, mostrarlo.
        if display_collision == None:
            display_edit.blit(
                sprite.surf, (
                    sprite.rect.x -scroll_int[0], sprite.rect.y -scroll_int[1]
                )
            )
    
    
    # Mostrar display edit
    display.blit( display_edit, (difference_display_edit[0], difference_display_edit[1]) )


    
    # Detectar dimencion x.
    size_buttons_xy = [0,0]
    pos_x = []
    pos_y = []
    aditional = 0
    for button in buttons:
        if button.text in dict_object.keys():
            size_buttons_xy[0] = button.rect.width
            size_buttons_xy[1] += button.rect.height
            aditional = button.rect.height
            pos_x.append(button.rect.x)
            pos_y.append(button.rect.y)

    #print(size_buttons_xy)
    if not (pos_x == [] or pos_y == []):
        #print( max(pos_x), max(pos_y)+aditional )
        #print( min(pos_x), min(pos_y) )
        if max(pos_y)+aditional >= data_CF.disp[1]:
            #print( max(pos_y)+aditional )
            #print( ( max(pos_y)+aditional ) -data_CF.disp[1] )
            for button in buttons:
                if button.text in dict_object.keys():
                    button.rect.y -= ( max(pos_y)+aditional ) -data_CF.disp[1]
                    button.background.rect.y -= ( max(pos_y)+aditional ) -data_CF.disp[1]

    # Sección de interfaz/hud
    if click_left == False:
        # Borrar botones repetidos
        for sprite in buttons:
            for x in buttons:
                if not sprite == x:
                    if sprite.rect.x == x.rect.x and sprite.rect.y == x.rect.y:
                        print('borrar')
                        x.kill()
                        if not x.background == None:
                            x.background.kill()
                    elif sprite.text == x.text:
                        print('borrar')
                        x.kill()
                        if not x.background == None:
                            x.background.kill()
    
    for sprite in interface_background:
        display.blit( sprite.surf, sprite.rect )
    
    for sprite in buttons:
        display.blit( sprite.surf, sprite.rect )


    
    # Fin
    pygame.display.update()
    clock.tick( data_CF.fps )
if run_game == True:
    data_CF.current_level = file_current_map
    save_CF( data_CF )
    import cuadradoFeliz
pygame.quit()

print( return_map( current_map ) )