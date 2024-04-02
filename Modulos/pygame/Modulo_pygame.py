import os, sys
from pathlib import Path as pathlib


import pygame, random
from pygame.locals import *




def obj_collision_sides_solid(obj_main, obj_collide):
    '''
    El objeto main, tiene que tener atributos adicionales llamados
    self.jumping = bool
    self.not_move = bool
    self.speed = entero/int
    '''
    # Si el obj_main, esta colisionando con el obj_collide, seguira el codigo
    if obj_main.rect.colliderect(obj_collide.rect):
        # Para detectar que la altura el solido y la del jugador sean correctas.
        more_height = obj_more_height(obj_main=obj_main, obj_collide=obj_collide)


        # Deteccion de colision arriba/abajo
        # Recuerda que no se puede colisionar dos veces, se eliguira una colision, y en este caso siempre tiene mas pioridad la colision arriba, debido a que esta arriba de la linea de colision de a abajo.
        direction = None
        if obj_main.rect.y < obj_collide.rect.y:
            # El obj_main, se movera "el valor de coordenadas y del obj_collide, menos el valor de la altura del obj_collide, mas un pixel", mueve al obj_main hacia arriba ( tendencia a ser valor negativo ).
            # Unicamente en esta posición, el jugador podra moverse y saltar.
            direction = 'collide_up'
            obj_main.rect.y = obj_collide.rect.y - obj_main.rect.height+1

        elif obj_main.rect.y > obj_collide.rect.y + (more_height):
            # El obj_main, se movera "el valor de coorenadas y de obj_collide, mas el valor de la altura del obj_collide", mueva al obj_main hacia abajo ( tendencia a ser valor positivo ).
            # El obj_main, ya no tendra permitido saltar.
            direction = 'collide_down'
            obj_main.jumping = False
            obj_main.not_move = True
            obj_main.rect.y = obj_collide.rect.y + obj_collide.rect.height
            
            # Si el obj_collide tiene menos altura que el obj_main, el obj_main no podra moverse de izq/der
            # Se forzara aleatoriamente el movimiento hacia la izquierda o derecha.
            if more_height == 0:
                #obj_main.not_move = True
                x_positive = random.randint(0, 1)
                if x_positive == 0:
                    obj_main.rect.x -= obj_main.speed
                elif x_positive == 1:
                    obj_main.rect.x += obj_main.speed

        # Deteccion de colision izquierda/derecha
        # Collisionar de izquierda/derecha solo cuando el obj_main no es mas pequeño en hight que del obj_collide
        # Si more_height esta en 0, el jugador no colisionara en lados izquierda/derecha.
        elif not more_height == 0:
            # El "obj_main.not_move", ayuda a que no se pueda mover de ninguna manera al obj_main
            # Los "obj_main.rect.x +- = self.speed" vistos aqui, redirecciónan al lado contrario al obj_main dependiendo si colisiono del lado derecho o del lado izquierdo
            # Recuerda que no se puede colisionar dos veces, se eliguira una colision, y en este caso siempre tiene mas pioridad la colision izquirda, debido a que esta arriba de la linea de colision de la derecha.
            if obj_main.rect.x < obj_collide.rect.x + (obj_main.speed/8):
                direction = 'collide_left'
                obj_main.not_move = True
                obj_main.jumping = False
                obj_main.rect.x = obj_collide.rect.x -obj_main.rect.width -obj_main.speed

            elif obj_main.rect.x > obj_collide.rect.x - (obj_main.speed/8):
                direction = 'collide_right'
                obj_main.not_move = True
                obj_main.jumping = False
                obj_main.rect.x = obj_collide.rect.x + obj_collide.rect.width + obj_main.speed
        
        # Retornar valores
        if not direction == None:
            return direction




def obj_collision_sides_rebound(obj_main, obj_collide):
    '''
    El objeto main, tiene que tener atributos adicionales llamados
    self.jumping = bool
    self.move_positive_x = bool
    '''
    # Si el obj_main, esta colisionando con el obj_collide, seguira el codigo
    if obj_main.rect.colliderect(obj_collide.rect):
        # Para detectar que la altura el solido y la del jugador sean correctas.
        more_height = obj_more_height(obj_main=obj_main, obj_collide=obj_collide)

        # Deteccion de colision arriba/abajo
        # Recuerda que no se puede colisionar dos veces, se eliguira una colision, y en este caso siempre tiene mas pioridad la colision arriba, debido a que esta arriba de la linea de colision de a abajo.
        direction = None
        if obj_main.rect.y < obj_collide.rect.y:
            # El obj_main, se movera "el valor de coordenadas y del obj_collide, menos el valor de la altura del obj_collide, mas un pixel", mueve al obj_main hacia arriba ( tendencia a ser valor negativo ).
            # Unicamente en esta posición, el jugador podra moverse y saltar.
            direction = 'collide_up'
            #obj_main.rect.y = obj_collide.rect.y - obj_main.rect.height
            obj_main.jumping = True

        elif obj_main.rect.y > obj_collide.rect.y + (more_height):
            # El obj_main, se movera "el valor de coorenadas y de obj_collide, mas el valor de la altura del obj_collide", mueva al obj_main hacia abajo ( tendencia a ser valor positivo ).
            # El obj_main, ya no tendra permitido saltar.
            direction = 'collide_down'
            obj_main.rect.y = obj_collide.rect.y + obj_collide.rect.height
            obj_main.jumping = False
            
            # Si el obj_collide tiene menos altura que el obj_main, el obj_main no podra moverse de izq/der
            # Se forzara aleatoriamente el movimiento hacia la izquierda o derecha.
            if more_height == 0:
                pass

        # Deteccion de colision izquierda/derecha
        # Collisionar de izquierda/derecha solo cuando el obj_main no es mas pequeño en hight que del obj_collide
        # Si more_height esta en 0, el jugador no colisionara en lados izquierda/derecha.
        elif not more_height == 0:
            # El "obj_main.not_move", ayuda a que no se pueda mover de ninguna manera al obj_main
            # Los "obj_main.rect.x +- = self.speed" vistos aqui, redirecciónan al lado contrario al obj_main dependiendo si colisiono del lado derecho o del lado izquierdo
            # Recuerda que no se puede colisionar dos veces, se eliguira una colision, y en este caso siempre tiene mas pioridad la colision izquirda, debido a que esta arriba de la linea de colision de la derecha.
            if obj_main.rect.x < obj_collide.rect.x + (obj_main.speedxy/8):
                direction = 'collide_left'
                obj_main.rect.x = obj_collide.rect.x -obj_main.rect.width*2
                obj_main.move_positive_x = False

            elif obj_main.rect.x > obj_collide.rect.x - (obj_main.speedxy/8):
                direction = 'collide_right'
                obj_main.rect.x = obj_collide.rect.x +obj_collide.rect.width*2
                obj_main.move_positive_x = True
        
        # Retornar valores
        if not direction == None:
            return direction




def obj_more_height(obj_main, obj_collide):
    # Si el obj_main, esta colisionando con el obj_collide, seguira el codigo
    # Para detectar que la altura el solido y la del jugador sean correctas.
    if obj_main.rect.height > obj_collide.rect.height:
        # Advertencia Altura de obj_collide mas pequeña comparada con la del obj_main
        if obj_collide.rect.height == obj_main.rect.height/2:
            # obj_main = 16, obj_collide = 8, 
            # more_height = obj_main -( obj_main + (obj_collide/2) ) = -4
            more_height = (
                obj_main.rect.height -( obj_main.rect.height + (obj_collide.rect.height/2) )
            )
        else:
            more_height = 0

    elif obj_main.rect.height < obj_collide.rect.height:
        # Advertencia Altura de obj_collide mas alta comparada con la del obj_main
        # Para acomodar colision del lado de abajo de forma adecuada.
        # Ejemplo:
        # obj_collide.altura = 32
        # obj_main.altura = 16
        # 16 cabe dos veces en 32, entonces: count = 2
        # more_height = obj_collide.altura - ( obj_main.altura / ( count/(count/2) ) ) = 24
        # para evitar bugs:
        # more_height = more_height -(obj_main.altura/4)
        count = 1
        difference = obj_collide.rect.height
        reduction = True
        while reduction:
            count += 1
            difference -= obj_main.rect.height
            if difference <= obj_main.rect.height:
                reduction = False
        more_height = (
            obj_collide.rect.height -( obj_main.rect.height / ( count/(count/2) ) )
            -(obj_main.rect.height/4)
        )

    else:
        # Excelente, la altura de obj_main es la misma que la de obj_collide
        # El "+(obj_collide.rect.height//4)", es para evitar dos colisiones seguidas:
        # Puede ser colisionar del lado izquierdo o derecho y seguido el lado inferior.
        # Funciona, porque la colision del lado inferior, esta un poco mas abajo de lo normal.
        more_height = obj_collide.rect.height//4
    
    return more_height




def obj_coordinate_multiplier(
    multipler=2,
    pixel=16,
    x=0, y=0
):
    '''
    (Solo funciona con cuadrados)
    Para acomodar los objetos de forma adecuada. Ejemplo:
    multipler = 2
    pixel = 16
    more_pixels = pixel*multipler = 32
    (more_pixels + pixel)/2 = 24
    (more_pixels + pixel)/2 -(pixel*2) = -8
    more_pixels -(more_pixels + pixel)/2 = 8
    Tamaño final de objeto = 32
    x posicion final = -8
    y posicion final = 8
    '''
    if multipler >= 2:
        more_pixel = pixel*multipler
    else:
        more_pixel = pixel*2

    difference = (more_pixel + pixel)/2
    difference = [
        difference -(pixel*2),
        more_pixel -(difference)
    ]
    return [ (more_pixel, more_pixel), ( (x*pixel)+difference[0], (y*pixel)+difference[1] ) ]




def player_camera_prepare(
    disp_width=None, disp_height=None, more_pixels=0,
    all_sprites=None, player=None,
    show_coordenades=True
):
    '''
    Posicionar la camara en donde estan las coordenadas del jugador.
    Inicia desde coordenadas 0, 0 de la resolución de la pantalla, y se mueve derecha o arriba, segun sea necesario. No se mueve de izquierda abajo, pero no deberia es necesario hacer esto.

    - disp_width y disp_height, son valores enteros que son las dimenciones de la pantalla de juego.
    
    - more_pixels, es un entero que tiene la función de posicionar un la camara un poco mas de pixeles a la derecha o izquierda, para que se vea mas facilmente el jugador.

    - all_sprites, player, son objeto tipo: "pygame.sprite.Group()" y "pygame.sprite.Sprite()" resectivamente.

    - Donde all_sprites son todos los sprites vistos en la pantalla, (incluyendo al jugador)

    - El parametro player, es el jugador. Este parametro es opcional
    
    - El parametro show_coordenades es un booleano opcional, unicamente para mostrar los cambios que hizo la función a la posición del jugador, en la terminal. Aunque mueva todos los sprites, unicamente mostrara los cambios de coordenadas que hizo al player.
    '''
    move_camera = True
    while move_camera:
        for sprite in all_sprites:
            if disp_height-more_pixels < player.rect.y:
                sprite.rect.y -= disp_width//60
                # arriba
            elif disp_width-more_pixels < player.rect.x:
                sprite.rect.x -= disp_width//60
                # izquierda
            else:
                move_camera = False

        if show_coordenades == True:
            print(
                f"Display:              {disp_width} X {disp_height} \n"
                f"Player coordenades:   {player.rect.x} X {player.rect.y}\n"
            )
    return [player.rect.x, player.rect.y]




def player_camera_move(
    disp_width=0, disp_height=0,
    camera_x=0, camera_y=0, 
    all_sprites=None,
    limit_objects=None,
    player=None,
): 
    '''
    Función para mover la camara, segun donde se mueva el jugador. Ya sea verticalmente o horizontalmente
    
    - disp_width y disp_height, son valores enteros que son las dimenciones de la pantalla de juego.

    - camera_x, camera_y, son los valores de posición de la camara, estos varian segun la posición establecida.

    - all_sprites, limit_objects, son objeto tipo: "pygame.sprite.Group()"
    all_sprites, son todos los sprites disponibles, y limit_objects esta incuildo en el.
    
    - limit_objects, son para establecer a la camara un limite de movimiento xy
    
    - player, es el objeto player, y tiene que tener los siguietes atributos adicionales:
    Enteros: hp, speed, jump_power, gravity_power
    Booleanos: gravity, jumping
    
    - player constantes:
    Entero: player_spawn_hp, es el valor entero de vida inicial del jugador.
    Lista:  player_spawn_xy, es la posición de inicio "x y"  del jugador.
    '''
    dead = False
    # Camara lado x
    # Si la camara detecta que hay un limite de camara del lado derecho/izquierdo y que el jugador no esta en medio de la pantalla, lo detectara, y no permitira mover la camara.
    camera_move_x = True
    for limit in limit_objects:
        for x in range(0, disp_width//60):
            if (
                limit.rect.x == x and player.rect.x < disp_width//2
            ):
                #print('limite detectado izquierda')
                camera_move_x = False
            elif (
                limit.rect.x == disp_width-x and player.rect.x > disp_width//2
            ):
                #print('limite detectado derecha')
                camera_move_x = False
                
    # Si el player desea y puede moverse al lado derecho/izquierdo. Todos los objetos que no sean el jugador se moveran al lado contrario de la dirección de el, con su misma velocidad horizontal, pero invertida.
    if player.moving == True and camera_move_x == True:
        positive = None
        if player.rect.x > disp_width//2:
            # mover camara derecha
            camera_x -= player.speed
            positive = False

        elif player.rect.x < disp_width//2:
            # mover camara izquierda
            camera_x += player.speed
            positive = True

        for sprite in all_sprites:
            if positive == False:
                # mover camara derecha
                sprite.rect.x -= player.speed

            elif positive == True:
                # mover camara izquierda
                sprite.rect.x += player.speed


    # Camara lado y
    # Si la camara detecta que hay un limite de camara arriba/abajo y que el jugador no esta en medio de la pantalla, lo detectara, y no permitira mover la camara.
    camera_move_y = True
    for limit in limit_objects:
        for y in range(0, disp_height//60):
            if (
                limit.rect.y == y and player.rect.y < disp_height//2
            ):
                # Limite arriba
                camera_move_y = False
            elif (
                limit.rect.y == disp_height-y and player.rect.y > disp_height//2
            ):
                # Limite abajo
                camera_move_y = False
                
    # Si el player desea y puede moverse arriba/abajo. Todos los objetos que no sean el jugador se moveran al lado contrario de la dirección de el, con su misma velocidad vertical, pero invertida.
    if camera_move_y == True:
        positive = None
        if player.rect.y < disp_height//2:
            # mover camara arriba
            camera_y += player.jump_power
            positive = True

        elif player.rect.y > disp_height//2 and player.gravity == True:
            # mover camara abajo
            camera_y -= player.gravity_power
            positive = False
    
        for sprite in all_sprites:
            if positive == True:
                # mover camara arriba
                sprite.rect.y += player.jump_power

            elif positive == False:
                # mover camara abajo
                sprite.rect.y -= player.gravity_power
    
    # Cuando el player muere
    if player.hp <= 0:
        dead = True
    
    return [camera_x, camera_y, dead]




def obj_not_see(disp_width=None, disp_height=None, obj=None, difference=0, reduce_positive=False):
    '''
    Para detectar si esta en la pantalla el sprite, si esta fuera de la pantalla, devolvera un string indicador de la posición en la que no se ve. Y si esta adentro de la pantalla, devolvera un None.
    disp_width  =int, Ancho de pantalla
    disp_height =int, Altura de pantalla
    obj         =pygame.sprite.Sprite(), Objeto tipo sprite, con atributo rect

    difference  =int, Añade/Dismunille, la altura y anchura de pantalla establecida. 
    difference, es un parametro opcional. Los demas son necesarios
    
    '''
    # Diferencia para numero positivo (Ancho positivo, o Alto positivo de pantalla)
    if difference >= 0:
        if reduce_positive == True:
            difference_for_positive = -(round(difference*0.75))
        else:
            difference_for_positive = difference

    else:
        difference_for_positive = difference*2
    
    # Devolver un string si se detecta que se sobrepaso la pantalla
    direction = None
    if obj.rect.x > disp_width +(difference_for_positive):
        direction = 'width_positive'
    elif obj.rect.x < 0 -(difference):
        direction = 'width_negative'
    
    elif obj.rect.y > disp_height +(difference_for_positive):
        direction = 'height_positive'
    elif obj.rect.y < 0 -(difference):
        direction = 'height_negative'
    return direction




def generic_colors(color='green', transparency=255):
    '''
    Colores que considero genericos, estan bueno tenerlos en una función y obtenerlos de una forma rapida y consistente.
    
    color, Un string, escribe el nombre del color en ingles y minuscilas y te debolvera su valor rgb.
    colores: red, green, blue, white, black, grey, sky_blue, yellow.
    
    transparency, sirve para cambiar su transparencia; de 0 a 255, entre mas alto mas opaco. (Opcional)
    '''
    # Principales
    if color == 'red':
        return(255, 0, 0, transparency)
    if color == 'green':
        return (0, 255, 0, transparency)
    elif color == 'blue':
        return (0, 0, 255, transparency)

    # Escala de grises
    elif color == 'white':
        return (255, 255, 255, transparency)
    elif color == 'black':
        return (0, 0, 0, transparency)
    elif color == 'grey':
        return (128, 128, 128, transparency)
    
    # Otros
    elif color == 'sky_blue':
        return (0, 255, 255, transparency)
    
    elif color == 'yellow':
        return (255, 255, 0, transparency)




class Anim_sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, position=(0,0) ):
        super().__init__()
        '''
        Para utilizar la animación de los sprites.
        '''
        
        # Cargar la hoja de sprites
        # Sprite sheet tiene que ser un pygame.image.load()
        rect_sheet = sprite_sheet.get_rect()
        
        # Dimenciones de cada cuadro de animación
        self.frame_square = rect_sheet.height
        self.frame_number = rect_sheet.width//rect_sheet.height
        
        # Lista para almacenar los cuardos de animación
        self.frames = []
        
        # Recortar la hoja de sprites en cuadros individuales
        for i in range(self.frame_number):
            frame = sprite_sheet.subsurface( 
                (i*self.frame_square, 0, self.frame_square, self.frame_square) 
            )
            self.frames.append(frame)
        
        # Índice para rastrear el cuadro de animación actual
        self.current_frame = 0
        
        # Configurar la imagen inicial
        self.surf = self.frames[self.current_frame]
        
        # Mostrar
        surf = pygame.Surface( (self.frame_square, self.frame_square) )
        self.rect = surf.get_rect( topleft=position )
    
    def anim(self):
        # Actualizar la animación
        self.current_frame = (self.current_frame +1) % len(self.frames)
        self.surf = self.frames[self.current_frame]
        



def Anim_sprite_set(sprite_sheet=None, current_frame=None):
    '''
    Establecer un frame de un srpite tipo animación
    '''
    # Cargar la hoja de sprites
    # Sprite sheet tiene que ser un pygame.image.load()
    rect_sheet = sprite_sheet.get_rect()
    
    # Dimenciones de cada cuadro de animación
    frame_square = rect_sheet.height
    frame_number = rect_sheet.width//rect_sheet.height
    
    # Lista para almacenar los cuardos de animación
    frames = []
    
    # Recortar la hoja de sprites en cuadros individuales
    for i in range(frame_number):
        frame = sprite_sheet.subsurface( 
            (i*frame_square, 0, frame_square, frame_square) 
        )
        frames.append(frame)
    
    # Índice para rastrear el cuadro de animación actual "current_frame"
    # Configurar la imagen inicial
    if not frames == []:
        if current_frame == None:
            return frames
        else:
            return( frames[current_frame] )




def Split_sprite(sprite_sheet, parts=4):
    """
    Divide un sprite en partes iguales.
    """
    parts = parts//2
    # Sprite sheet tiene que ser un pygame.image.load()
    rect_sheet = sprite_sheet.get_rect()

    # Dimensiones de cada cuadro de animación
    frame_width = rect_sheet.width // parts
    frame_height = rect_sheet.height // parts

    # Lista para almacenar los cuadros divididos
    frames = []

    # Recortar la hoja de sprites en cuadros individuales
    number = -1
    for _ in range(parts):
        number += 1
        for x in range(parts):
            frame = sprite_sheet.subsurface( 
                (x*frame_width, (frame_height*number), frame_width, frame_height) 
            )
            frames.append(frame)

    return frames



def obj_detect_collision(obj_main, obj_collide):
    collision_direction = None
    if obj_main.rect.y == obj_collide.rect.y-(obj_main.rect.height):
        # Colision arriba
        collision_direction = 'collide_up'
    elif obj_main.rect.y == obj_collide.rect.y+(obj_collide.rect.height):
        # Colision abajo
        collision_direction = 'collide_down'
    elif obj_main.rect.x == obj_collide.rect.x-(obj_main.rect.width):
        # Colision izquierda
        collision_direction = 'collide_left'
    elif obj_main.rect.x == obj_collide.rect.x+(obj_collide.rect.width):
        # Collide derecha
        collision_direction = 'collide_right'
    
    return collision_direction