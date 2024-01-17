import os, sys
from pathlib import Path as pathlib


current_dir = os.path.dirname( os.path.abspath(sys.argv[0]) )


import pygame, random
from pygame.locals import *




def collision_sides_solid(obj_main, obj_collide):
    '''
    El objeto main, tiene que tener atributos adicionales llamados
    self.jumping = bool
    self.not_move = bool
    '''
    # Si el obj_main, esta colisionando con el obj_collide, seguira el codigo
    if obj_main.rect.colliderect(obj_collide.rect):
        # Para detectar que la altura el solido y la del jugador sean correctas.
        if obj_main.rect.height > obj_collide.rect.height:
            # Advertencia Altura de obj_collide mas pequeña comparada con la del obj_main
            #height_difference = obj_main.rect.height - obj_collide.rect.height
            more_height = 0
        elif obj_main.rect.height < obj_collide.rect.height:
            # Advertencia Altura de obj_collide mas alta comparada con la del obj_main
            #height_difference = obj_collide.rect.height - obj_main.rect.height
            # Obtener cuantas veces cabe la altura del obj_main en el obj_collide. (Solo enteros).
            # count = "cuantas veces cabe el obj_main en obj_collide""
            # obj_collide.altura - ( obj_main.altura / ( count/ (count/2) ) )
            count = 1
            difference = obj_collide.rect.height
            reduction = True
            while reduction:
                count += 1
                difference -= obj_main.rect.height
                if difference <= obj_main.rect.height:
                    reduction = False
            '''
            if count == 2:
                count = count
            elif count == 4: 
                count = count/2
            elif count == 8:
                count = count/4
            '''
            more_height = obj_collide.rect.height -( obj_main.rect.height / ( count/(count/2) ) )
        else:
            # Excelente, la altura de obj_main es la misma que la de obj_collide
            # El "+(obj_collide.rect.height//4)", es para evitar dos colisiones seguidas:
            # Puede ser colisionar del lado izquierdo o derecho y seguido el lado inferior.
            # Funciona, porque la colision del lado inferior, esta un poco mas abajo de lo normal.
            more_height = obj_collide.rect.height//4

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
            # El obj_main, ya no tendra permitido saltar,
            direction = 'collide_down'
            obj_main.jumping = False
            obj_main.rect.y = obj_collide.rect.y + obj_collide.rect.height
            
            # Si el obj_collide tiene menos altura que el obj_main, el obj_main no podra moverse de izq/der
            # Se forzara aleatoriamente el movimiento hacia la izquierda o derecha.
            if more_height == 0:
                obj_main.not_move = True
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




def generic_colors(color='green'):
    # Principales
    if color == 'red':
        return(255, 0, 0)
    if color == 'green':
        return (0, 255, 0)
    elif color == 'blue':
        return (0, 0, 255)

    # Escala de grises
    elif color == 'white':
        return (255, 255, 255)
    elif color == 'black':
        return (0, 0, 0)
    elif color == 'grey':
        return (128, 128, 128)
    
    # Otros
    elif color == 'sky_blue':
        return (0, 255, 255)
    
    elif color == 'yellow':
        return (255, 255, 0)