import math
from logic.pygame.Modulo_pygame import (
    generic_colors, obj_collision_sides_solid, obj_coordinate_multiplier,
    player_camera_prepare, player_camera_move,
    obj_collision_sides_rebound, obj_not_see,
    Anim_sprite, Anim_sprite_set, Split_sprite
)
from data.CF_info import (
    game_title,

    dir_game,
    dir_data,
    dir_sprites,
    dir_maps,
    dir_audio,
    
    data_CF,
    scale_surface_size, pixel_space_to_scale
)
from logic.pygame.CF_function import *

import pygame, sys, os, random
from pygame.locals import *


# Objetos para uso general
class SpriteStandar(pygame.sprite.Sprite):
    '''
    Sprite estandar para el juego CuadradoFeliz
    
    Objeto heredado de pygame.sprite.Sprite
    Con respecto a pygame.sprite.Srprite
        - Este objeto tiene varios atributos adicioneles.     
        - Este objeto tiene varias funciones adicionales. 

    Parametros:
        surf; pygame.Surface
        transparency; int
        position; [int,int]
    
    Atributos:
        surf_base = pygame.Surface
        surf = pygame.Surface
        rect = pygame.Rect
        transparency = int (de 0 a 255)
        position = [int,int]
        not_see = False
        
        angle = int. Para rotar surf
        moving_xy = [int,int]. Para mover rect
        
        time = int, Tiempo para hacer algo
        time_count = int, Contador para llegar al tiempo
    

    Como se establecen lo atributos:
    Esta objeto con el surf, establece el rect.
    Con el position, establece la posición del rect.
    El transparency establece el alpha de surf.
    Los demas atributos, tienen valores default y es posible que no se usen.
    '''
    def __init__(
        self, surf, transparency=255, position=[0,0]
    ):
        super().__init__()

        self.surf_base = surf
        self.surf = surf
        self.transparency = transparency
        self.surf.set_alpha( self.transparency )
        self.rect = self.surf.get_rect( topleft=position )
        self.position = position
        self.not_see = False

        # Relacionado con el movimiento.
        self.angle = 0 
        self.moving_xy = [0,0]
        
        # Relacionado con el tiempo/timer/time
        self.time = 0
        self.time_count = 0
    
    def sync_size(self):
        '''
        Sincronisar tamaño del surf y el tamaño del rect. Mismo size xy.
        Si cambia de tamaño surf, volver a obtener rect.
        '''
        if self.surf.get_size() != self.rect.size:
            self.rect = self.surf.get_rect()
    
    def set_transparency(self):
        '''
        Establecer alpha del surf
        Si esta en "not_see" es true, si o si; no se vera el surf.
        '''
        if self.not_see == False:
            self.surf.set_alpha( self.transparency )
        else:
            self.surf.set_alpha( 0 )
    
    def set_color(self, color=[0,0,0], method='surface'):
        '''
        Establecemos el color
        '''
        if method == 'surface':
            colorSurf = pygame.Surface( self.surf.get_size() ).convert_alpha()
            colorSurf.fill( color )
            self.surf.blit(colorSurf, (0,0), special_flags = pygame.BLEND_MULT)
        else:
            self.surf.fill( color, special_flags=pygame.BLEND_ADD)
    
    def movement(self):
        '''
        Mover rectangulo. Mover sprite
        '''
        self.rect.x += self.moving_xy[0]
        self.rect.y += self.moving_xy[1]
    
    def rotate(self):
        '''
        Rotar el surf base. Y establecer lo rotado en el surf. Rotar sprite
        '''
        if self.angle != 0:
            self.surf = pygame.transform.rotate( self.surf_base, self.angle )
        else:
            self.surf = self.surf_base
        self.sync_size()
        
    def sync_all(self):
        '''
        Sincronisar todo lo que se pueda
        '''
        self.sync_size()
        self.set_transparency()
        self.rotate()
        self.movement()
        
    def time_over(self):
        '''
        Verifica si ha pasado el tiempo especificado.
        
        Devolver:
            True El time_count es mayor o igual a time.
            False Si no pasa lo anterior mencionado.
        '''
        return self.time_count >= self.time




class SpritePasteRect(SpriteStandar):
    '''
    Este objeto es heredado de SpriteStandar

    Este objeto tiene un metodo update, este metodo hace que se quede centralizado en el rect indicado en los parametros.
    
    Parametros:
    rect_pasted=collider, coordenadas de objeto a pegarse
    update_group=grupo en donde se añadira (opcional)
    
    Tiene el un metodo update, el cual permite que el sprite se pege al rect, a la posición.
    '''
    def __init__( 
        self, surf, rect_pasted, difference_xy=[0,0]
    ):  
        # Establecer parametros para SpriteStandar
        super().__init__( surf, surf.get_alpha(), rect_pasted.center )

        # Superficie
        self.rect_pasted = rect_pasted
        
        # Diferencia de centrado.
        self.center_difference_xy = difference_xy
    
    def update(self):
        # Si cambia de tamaño surf, volver a obtener rect.
        self.sync_size()
        
        # Centrar rect en el rect_pasted
        self.rect.center = self.rect_pasted.center
        
        # Agregar diferencia.
        self.rect.x += self.center_difference_xy[0]
        self.rect.y += self.center_difference_xy[1]
            
            

class LayerSpriteRectPasted( ):
    '''
    Un objeto que contiene varios objetos SpritePasteRect
    Su función es tener entre una capa/layer a muchos capas/layers de sprites.
    
    rect_pasted, es un pygame.Rect, obtiene sus coordenadas xy
    layer, es una lista de SpritePasteRect
    '''
    def __init__(
        self, rect_pasted, transparency=255, layer=[], difference_xy=[0,0]
    ):  
        # Agregar layers
        self.transparency_layer = transparency
        self.rect_pasted = rect_pasted
        self.layer = []
        for surf in layer:
            sprite = SpritePasteRect( surf=surf, rect_pasted=self.rect_pasted, difference_xy=difference_xy ) 
            sprite.transparency = self.transparency_layer
            sprite.set_transparency()
            self.layer.append( sprite )
    
    def add_to_sprite_group(self, group):
        '''
        Agregar a grupo de sprites
        '''
        for sprite in self.layer:
            group.add(sprite)
    
    def add_to_layer_group(self, group, layer=0):
        '''
        Agregar a grupo de layer
        '''
        for sprite in self.layer:
            group.add(sprite, layer=layer)
    
    def rm_layer(self):
        '''
        Eliminar todos los layer
        '''
        for sprite in self.layer:
            sprite.kill()
        

    def set_transparency_layer(self):
        '''
        Establecer transparencia a todos los layers. Todas las capas
        '''
        for sprite in self.layer:
            sprite.transparency = self.transparency_layer
    
    def update_layer(self):
        '''
        Acomodar todos los layer
        '''
        for layer in self.layer:
            layer.update()
            
            

            
class SpriteMultiLayer( SpriteStandar ):
    '''
    Un sprite, que tiene otros muchos sprites que estan pegados a este sprite
    Su función es tener entre una capa/layer a muchos capas/layers de sprites.
    '''
    def __init__(
        self, surf, transparency=255, position=[0,0], 
        layer=[], layer_transparency=255, layer_difference_xy=[0,0]
    ):
        super().__init__(
            surf=surf, transparency=transparency, position=position
        )
        
        # Agregar layers            
        self.sprite_layer = LayerSpriteRectPasted(
            rect_pasted=self.rect, transparency=layer_transparency, difference_xy=layer_difference_xy, 
            layer=layer
        )




# Audio | Pasos | Golpes | Salto | Muertes
sounds_step = [
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-1.ogg') ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-2.ogg') ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-3.ogg') )
]
for step in sounds_step:
    step.set_volume(data_CF.volume)


sounds_hit = [
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-1.ogg') ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-2.ogg') ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-3.ogg') )
]
for hit in sounds_hit:
    hit.set_volume(data_CF.volume)


sound_jump = pygame.mixer.Sound(
    os.path.join(dir_audio, 'effects/jump.ogg')
)
sound_jump.set_volume(data_CF.volume)

sounds_dead = [
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-1.ogg' ) ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-2.ogg' ) ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-3.ogg' ) )
]
for dead in sounds_dead:
    dead.set_volume(data_CF.volume)


sounds_score = [
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/items/score-1.ogg' ) ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/items/score-2.ogg' ) ),
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/items/score-3.ogg' ) )
]
for score in sounds_score:
    score.set_volume(data_CF.volume)




# Objetos / Clases
# Contador jugador en el aire, basado en la resolucion del juego. Se usa "data_CF". Esta basado en la resolución maxima 1920x1080
# Valores usados: 0.1875, 0.3125
air_count_based_on_resolution = round( 1920 / ( scale_surface_size[0] * 0.4) ) #round(pixel_space_to_scale*0.3125) 
if air_count_based_on_resolution < 0:
    air_count_based_on_resolution = 0
elif air_count_based_on_resolution > 5:
    air_count_based_on_resolution = 5
print( round( 1920 / (pixel_space_to_scale*20) ) )

# Basado en las dimenciones del ancho de la resolución maxima, entre el 26% de la resolución de ancho seelccionada.
# Resolución base 1920, resolucion seleccionada llamemosla res_current (res_current*/)
air_count_based_on_resolution = round( 1920 / (scale_surface_size[0]*0.5) )#4#round( 1920 / (scale_surface_size[0]*0.26) )




class Character( SpriteStandar ):
    '''
    Objeto Personaje, para Player, y para NPC.
    '''
    def __init__(
        self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255, 
        dict_sprite={
            'side-x' : pygame.Surface( [pixel_space_to_scale,pixel_space_to_scale] ),
            'side-y' : pygame.Surface( [pixel_space_to_scale,pixel_space_to_scale] )
        }, 
        position=[0,0], limit_xy=[0,0], color_sprite=[153,252,152], sprite_difference_xy=[0,0]
    ):
        # Parametros para Sprite Standar
        surf = pygame.Surface( [size*0.5,size] )
        surf.fill( [0,0,0] )
        
        # Establecer parametros
        super().__init__( 
            surf, transparency=transparency_collide, position=position
        )
        
        # Transparencia
        #self.transparency
        
        # Imagen que se vera.
        self.anim_xy = [False, False]
        self.dict_sprite = dict_sprite
        self.frames_xy = [0,0]
        first_sprite = None
        if isinstance( dict_sprite['side-x'], list ):
            first_sprite = dict_sprite['side-x'][0]
            self.frames_xy[0] = len(dict_sprite['side-x'])
            self.anim_xy[0] = True
        else:
            first_sprite = dict_sprite['side-x']
            self.frames_xy[0] = 8
        if isinstance( dict_sprite['side-y'], list ):
            self.frames_xy[1] = len(dict_sprite['side-y'])
            self.anim_xy[1] = True
            
        # Sprite GUN
        self.gun_surf = pygame.Surface( [size, size], pygame.SRCALPHA)
        palote = pygame.Surface( [size, size//2 ], pygame.SRCALPHA )
        palote.fill( (127, 127, 127) )
        self.gun_surf.blit( palote, [0, size//2 - size//4 ] )

        puntito = pygame.Surface( [size//4, size//4], pygame.SRCALPHA )
        puntito.fill( [255,0,0] )
        self.gun_surf.blit( puntito, [ size -size//4, size//2 - size//8 ] )
        
        # Capas | Sprites | Apariencia de player
        self.sprite_layer = LayerSpriteRectPasted(
            rect_pasted=self.rect, transparency=transparency_sprite, difference_xy=[0,0], 
            layer=[ self.dict_sprite['side-x'][0], self.gun_surf ]
        )
        self.sprite_layer.layer[0].center_difference_xy = sprite_difference_xy
        self.sprite_layer.layer[1].center_difference_xy = [0,0]
        self.sprite_layer.layer[1].transparency = 255 # Sprite gun
        self.sprite_layer.layer[1].set_transparency()
        
        # Color de sprite
        if self.anim_xy[0] == True:
            for image in self.dict_sprite['side-x']:
                colorImage = pygame.Surface( image.get_size() ).convert_alpha()
                colorImage.fill( color_sprite )
                image.blit(colorImage, (0,0), special_flags = pygame.BLEND_MULT)
        else:
            colorImage = pygame.Surface( self.dict_sprite['side-x'].get_size() ).convert_alpha()
            colorImage.fill( color_sprite )
            self.dict_sprite['side-x'].blit(colorImage, (0,0), special_flags = pygame.BLEND_MULT)

        if self.anim_xy[1] == True:
            for image in self.dict_sprite['side-y']:
                colorImage = pygame.Surface( image.get_size() ).convert_alpha()
                colorImage.fill( color_sprite )
                image.blit(colorImage, (0,0), special_flags = pygame.BLEND_MULT)
        else:
            colorImage = pygame.Surface( self.dict_sprite['side-y'].get_size() ).convert_alpha()
            colorImage.fill( color_sprite )
            self.dict_sprite['side-y'].blit(colorImage, (0,0), special_flags = pygame.BLEND_MULT)
        
        # Movimiento
        #self.moving_xy = [0,0]
        #self.angle = 0
        self.not_move = False
        self.speed = self.rect.height*0.5
        self.collision_solid = None
        self.side_positive = True

        # Vida
        self.damage_effect = False
        self.hp = 100
        self.dead = False
        
        # Movimiento | Gravedad
        # Valores de porcentaje de porder de gravedad usados
        # 0.0625 0.05 0.025 0.028125 0.03125 0.015625
        # Valores de porcentaje para limite gravedad usados 00.375 0.35 0.3125 0.03 0.306 0.25 
        self.gravity_power = self.rect.height*0.03125  #0.03125#0.0625
        self.gravity_limit = self.rect.height-1#*0.75#0.25
        self.gravity_current = -self.gravity_power # Para que empieze en 0 poder de gravedad
        self.air_count = 8 # Para que inicie en caida
        
        # Movimiento salto
        self.jumping = False
        self.jump_power = self.rect.height*0.5
        self.jump_max_height = (self.rect.height*4)
        self.jump_count = 0
        
        # Movimiento | Sonido contador de pasos
        self.step_count = 0
        self.state_collide_in_floor = 'wait'
        
        # Movimiento | Variables de movimiento.
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walk = False
        self.jump = False
        self.fall = True
        self.action = False
        self.change_level = False
        
        # Movimiento | Limit
        self.limit_xy = limit_xy
        
        # Puntos
        self.score = 0
        self.collision_score = False
        
        # Agregar a grupos de sprites
        update_objects.add(self)
        layer_all_sprites.add(self, layer=3)
        
        self.sprite_layer.add_to_sprite_group( update_objects )
        self.sprite_layer.add_to_layer_group( layer_all_sprites, layer=2 )
    
    def get_speed(self, multipler=1):
        '''
        Obtener velocidad. Un valor numerico int o float
        '''
        return self.speed*multipler
    
    def get_max_hp(self, multipler=1):
        '''
        Un valor entero.
        '''
        return int(100*multipler)
    
    def set_and_jump(self, multipler=1):
        '''
        Saltar. Multipler indica la altura maxima.
        '''
        self.jump = True
        self.jump_max_height = (self.rect.height*4)*multipler
    
    def collision_no_solid(self):
        '''
        Eventos de colisión con objetos no solidos.
        
        Objetos dañinos.
        Cambio de nivel.
        Monedas.
        Objetos saltarines.
        Objetos tipo escalera.
        Objetos tipo elevador.
        '''
        # Colision | Objetos dañinos
        damage_number = int
        self.damage_effect = False
        self.collision_score = False

        for obj in damage_objects:
            # Determinar si se colisiono con un objeto dañino y obtener el numero de daño.
            if self.rect.colliderect(obj.rect):
                self.damage_effect = True                
                damage_number = obj.damage
        
        if self.damage_effect == True and self.dead == False:
            #self.gravity_current = 0 # Cancelar gravedad
            #self.air_count = 0 # Cancelar gravedad
            self.jumping=False # Cancelar salto
            # Efecto de daño basado en el numero de daño recibido
            multipler = 1
            if isinstance(damage_number, int):
                if damage_number > 0:
                    multipler = damage_number*0.05

            xy_move = self.rect.height * multipler
            if random.choice( [False, True] ):
                self.moving_xy[1] -= xy_move*0.2
            else:
                self.moving_xy[1] -= xy_move
            if random.choice( [False, True] ):
                self.moving_xy[0] += xy_move
            else:
                self.moving_xy[0] -= xy_move
        if isinstance(damage_number, int):
            # Reducir HP
            if self.dead == False:
                if damage_number <= 0:
                    self.hp = -1
                else:
                    self.hp -= damage_number
        
        # Colision | Limite del mapa
        if not self.limit_xy == [0,0]:
            if self.rect.x > self.limit_xy[0] + self.rect.height or self.rect.x < 0:
               self.hp = -1
            elif self.rect.y > self.limit_xy[1] + self.rect.height or self.rect.y < 0:
               self.hp = -1
        
        
        # Colision | Objetos | Cambio de nivel
        if self.change_level == True:
            for level in level_objects:
                if self.rect.colliderect(level.rect):
                    level.change_level = True
                    self.hp = 100
                    self.rect.topleft = (level.rect.x+(self.rect.width//2), level.rect.y)
                    self.moving_xy = [0,0]
                

        # Colision | Objetos | Score-Monedas
        for score in score_objects:
            if self.rect.colliderect(score.rect):
                self.score += 1
                self.collision_score = True
                if (
                    self.hp < 100 and
                    (self.dead == False)
                ):
                    self.hp += 10
                score.remove_point()
                
        
        # Colision | Trampoline
        for obj in jumping_objects:
            if self.rect.colliderect(obj.rect):
                #if self.moving_xy[1] > 0:
                #    self.rect.bottom = obj.rect.top - obj.rect.height
                #    self.gravity_current = 0
                self.air_count=0
                self.jumping=True
                self.set_and_jump(multipler=2)
        

        # Colision | Solidos | Escalera
        if pygame.sprite.spritecollide(self, ladder_objects, False):
            if self.down == False:
                self.gravity_current = 0
                self.air_count = 0
                
        # Colision | Solidos | Elevador
        for obj in moving_objects:
            if self.rect.colliderect(obj.rect):
                self.gravity_current = 0
                self.air_count = 0
                
                if self.rect.y <= obj.rect.y:
                    self.rect.bottom = obj.rect.top+1
                    
                elif self.rect.y > obj.rect.y:
                    self.jumping=True
                    self.set_and_jump(multipler=0.5)
            
                if self.dead == False:
                    if obj.move_dimension == 1:
                        if obj.move_positive == True:   self.moving_xy[0] += obj.speed
                        else:                           self.moving_xy[0] -= obj.speed
                    if obj.move_dimension == 2:
                        if obj.move_positive == True:   self.moving_xy[1] += obj.speed
                        else:                           self.moving_xy[1] -= obj.speed

                if pygame.sprite.spritecollide(self, solid_objects, False):
                    self.hp = -1
                    self.not_move = True


    def anim_all(self, fall=False, speed_multipler=1):
        '''
        Animacion | sprites | surface | collider
        '''
        flip_image = False
        transform = False
        moving = False
        if self.left == True:
            flip_image = True
            moving = True
        elif self.right == True: moving = True
        if self.left == True and self.right == True: moving = False
        if moving == False or self.jumping == True or fall == True: self.step_count = 0
 
        if self.jumping == True:
            if moving == False:
                self.surf.fill( generic_colors('blue') )
                transform = False
                if self.anim_xy[1] == True:
                    self.sprite_layer.layer[0].surf = self.dict_sprite[ 'side-y' ][ 1 ]
            elif moving == True: 
                self.surf.fill( (0, 19, 63) )
                transform = True
                if self.anim_xy[0] == True:
                    self.sprite_layer.layer[0].surf = self.dict_sprite[ 'side-x' ][ 1 ]
        elif fall == True:
            if moving == False:
                self.surf.fill( generic_colors('sky_blue') )
                transform = False
                if self.anim_xy[1] == True:
                    self.sprite_layer.layer[0].surf = self.dict_sprite[ 'side-y' ][ 2 ]
            elif moving == True: 
                self.surf.fill( (0, 126, 255) )
                transform = True
                if self.anim_xy[0] == True:
                    self.sprite_layer.layer[0].surf = self.dict_sprite[ 'side-x' ][ 6 ]
        elif fall == False:
            if moving == False:
                self.surf.fill( generic_colors('green') )
                transform = False
                if self.anim_xy[1] == True:
                    self.sprite_layer.layer[0].surf = self.dict_sprite[ 'side-y' ][ 0 ]
            elif moving == True: 
                self.surf.fill( generic_colors('yellow') )
                self.step_count = ( 
                    (self.step_count +(1*speed_multipler)) % self.frames_xy[0]
                )
                transform = True
                if self.anim_xy[0] == True:
                    self.sprite_layer.layer[0].surf = self.dict_sprite[ 'side-x' ][ int(self.step_count) ]
        
        # Voltear sprite o no.
        if transform == True:
            self.sprite_layer.layer[0].surf = pygame.transform.flip( 
                self.sprite_layer.layer[0].surf, flip_image, False 
            )

        # Establecer trnasparencia, a collide y sprite.
        self.set_transparency()
        self.sprite_layer.layer[0].set_transparency()
    
    def sound(self):
        '''
        Sonido hits pasos, saltar y colision.
        '''
        # Sonido hits
        if self.damage_effect == True and self.dead == False: get_sound('hits').play()
        
        # Sonido | Pasos | Saltar | Colisionar con piso
        if (
            ( self.step_count == self.frames_xy[0] *0.5 ) or
            ( self.state_collide_in_floor == 'yes' )
        ):
            get_sound('steps').play()
            Particle( 
                size=[self.rect.height//4, self.rect.height//4], 
                position=[self.rect.x, self.rect.y-1+self.rect.height-pixel_space_to_scale//4], 
                transparency_collide=255, transparency_sprite=255, 
                color_collide=generic_colors('grey'), time_kill=data_CF.fps, sound=None
            )
        
        if self.jumping == True and self.jump_count == self.jump_power:
            get_sound('jump').play()
        
        # Score Monedas
        if self.collision_score == True:
            ( random.choice(sounds_score) ).play()
            
    def move(self):
        '''
        Moverse
        '''
        return True
    
    
    def gravity(self, old_gravity=False):
        self.moving_xy[1] += self.gravity_current
        if old_gravity == True:
            self.gravity_current = self.rect.height//4
        else:
            # Modo moderno
            if self.gravity_current < self.gravity_limit:
                self.gravity_current += self.gravity_power
            else:
                self.gravity_current = self.gravity_limit
    
    
    def gun_event(self):
        # Arma Gun | Disparo
        if self.action:
            bullet = Bullet(
               size=[self.rect.height//4, self.rect.height//4], position=self.rect.center, image=None,
               speed_xy=speed2d_with_angle( self.rect.height, self.sprite_layer.layer[1].angle ), time=90
            )
            bullet.rect.center = self.rect.center
        self.action = False
        
        # Arma Gun | Cambiar angulo
        if self.side_positive == True:
            speed_move_angle = 2
        else:
            speed_move_angle = -2

        if self.up == True:
            self.sprite_layer.layer[1].angle += speed_move_angle
        if self.down == True:
            self.sprite_layer.layer[1].angle -= speed_move_angle

        # Arma Gun | Bloquear rotación
        if self.side_positive == True:
            if self.sprite_layer.layer[1].angle > 90:
                self.sprite_layer.layer[1].angle = 90
            elif self.sprite_layer.layer[1].angle < -90:
                self.sprite_layer.layer[1].angle = -90
        else:
            if self.sprite_layer.layer[1].angle < -180-90:
                self.sprite_layer.layer[1].angle = -180-90
            elif self.sprite_layer.layer[1].angle > -180+90:
                self.sprite_layer.layer[1].angle = -180+90
                
        # Arma Gun | Rotar Sprite gun
        self.sprite_layer.layer[1].rotate()
    
    
    def update(self, old_gravity=False, old_jump=True):
        '''
        Actualizar eventos del jugador. Moverse y todo eso.
        '''
        # Moverse
        self.move()
        
        # HP | Determinar si el jugador esta vivo o muerto
        if self.hp <= 0:
            self.dead = True
            self.not_move = True
            self.jump_count = self.jump_max_height
            self.gravity_current = 0
            self.sprite_layer.layer[0].not_see=True
        else:
            self.sprite_layer.layer[0].not_see=False
            self.dead = False
            if self.hp > self.get_max_hp(multipler=1): self.hp = self.get_max_hp(multipler=1)
        
        # Dejar de moverse
        if self.not_move == True or self.damage_effect == True:
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.jump = False
            self.walk = False
            self.action = False
            
        # Detectar si esta en el piso o no
        # Esto se determina dependiendo la cantidad de frames en las que el jugador esta en el aire
        # Entre mas alto, major funciona en res bajas, y entre mas bajo mejor funciona en res altas.
        if self.air_count <= air_count_based_on_resolution:
            #print('En el piso')
            self.fall = False
            if self.state_collide_in_floor == 'wait':
                self.state_collide_in_floor = 'yes'
            elif self.state_collide_in_floor == 'yes':
                self.state_collide_in_floor = 'no'
        else:
            #print('Cayendo')
            self.fall = True
            self.state_collide_in_floor = 'wait'
        
        # Determinar velocidad del jugador
        if self.walk == True:
            # valores usados: 0.25 0.5 0.625
            speed_multipler = 0.5
        else:
            speed_multipler = 1
            self.step_count = int(self.step_count)
        speed = self.get_speed(multipler=speed_multipler)
        
        # Mover el jugador
        self.moving_xy = [0,0]
        if self.left == True:  
            self.moving_xy[0] -= speed
            self.sprite_layer.layer[1].angle = -180
            self.side_positive = False
        if self.right == True: 
            self.moving_xy[0] += speed
            self.sprite_layer.layer[1].angle = 0
            self.side_positive = True
        if self.jump == True:
            if self.fall == False:
                self.jumping = True
                #self.jump = False
        self.jump = False # Para que no puedas inicializar el salto en el aire.
        
        # Gravedad | Caida
        self.gravity(old_gravity=old_gravity)
                
        # Salto
        if self.jumping == True:
            if old_jump == True:
                self.gravity_current, self.moving_xy[1] = 0, 0
                self.jump_count += self.jump_power
                if self.jump_count <= self.jump_max_height:
                    self.moving_xy[1] -= self.jump_power
                    self.jumping = True
                else: self.jumping = False
            else:
                self.gravity_current = -self.jump_max_height*0.1125
                self.jumping=False
                self.jump_count = 0

        else: 
            self.jump_count = 0
        
        # Colisiones | Solidos | Primera pasada
        self.collision_solid = collide_and_move(obj=self, obj_movement=self.moving_xy, solid_objects=solid_objects)
        
        if self.collision_solid == 'bottom':
            self.gravity_current = 0
            self.air_count = 0
        else:
            self.air_count += 1
        
        if self.collision_solid == 'top':
            self.gravity_current = 0
            
            self.jumping = False
            self.jump_count = 0
            
        # Colision No solidos
        self.moving_xy = [0,0]
        if self.dead == False: self.collision_no_solid()
        
        # Colisiones | Solidos | Segunda pasada
        self.collision_solid = collide_and_move(obj=self, obj_movement=self.moving_xy, solid_objects=solid_objects)
        
        if self.collision_solid == 'bottom':
            self.gravity_current = 0
            #self.air_count = 0
        else:
            pass#self.air_count += 1
        
        if self.collision_solid == 'top':
            self.gravity_current = 0
            
            self.jumping = False
            self.jump_count = 0
            
        # Arma Gun | Disparos
        self.gun_event()
            
        # Anim
        self.anim_all(fall=self.fall, speed_multipler=speed_multipler)
        
        # Sound
        self.sound()





class Enemy(Character):
    def __init__(
        self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255, 
        dict_sprite={
            'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
            'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
        }, 
        position=[0,0], limit_xy=[0,0], color_sprite=[255,127,127], 
        sprite_difference_xy=[0,-(pixel_space_to_scale//2)]
    ):
        
        super().__init__( 
            size=size, 
            transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
            dict_sprite=dict_sprite, position=position, limit_xy=limit_xy, color_sprite=color_sprite,
            sprite_difference_xy=sprite_difference_xy
        )
        self.transparency=0

        self.init_wait = 10
        self.init_count = 0
        self.variation_xy = [None,None]
        self.variation_count = 0
        self.variation_time = air_count_based_on_resolution*2.5 #10
        
        self.time_change_direction = 8
        self.count_change_direction = 0
        self.direction_xy = [True, False]
        self.bool_direction = False
        
        #self.sprite_layer.layer[0].center_difference_xy = [0, -(self.rect.height//2)]
    
    def change_direction(self):
        if self.direction_xy[0] == True:
            self.direction_xy[0] = False
        else:
            self.direction_xy[0] = True
            
        if self.direction_xy[1] == True:
            self.direction_xy[1] = False
        else:
            self.direction_xy[1] = True
    
    def set_direction( self ):
        self.right = self.direction_xy[0] == True
        self.left = self.direction_xy[0] == False
        
        self.down = self.direction_xy[1] == True
        self.up = self.direction_xy[1] == False
    
    def move(self):
        if self.init_count < self.init_wait:
            self.init_count += 1
        if self.init_count >= self.init_wait:
            self.set_direction( )
            self.walk = False
            
            # Nomas detectar caida.
            if self.air_count > air_count_based_on_resolution*0.625:
                self.set_and_jump(1)
                
                #self.right = False
                #self.left = True
                #self.walk = True
            else:
                self.jump = False
                #self.right = True
                #self.left = False
                #self.walk = False
            
            if self.bool_direction == True:
                if self.count_change_direction == 0:
                    self.change_direction()
                    print('Cambiando')
                self.count_change_direction += 1
                if self.count_change_direction >= self.time_change_direction:
                    self.bool_direction = False
                    self.count_change_direction = 0
                    print('listo')
            
            if self.rect.x == self.variation_xy[0]:
                self.bool_direction = True
                #self.jump = True
        
        self.variation_count += 1
        if self.variation_count >= self.variation_time:
            self.variation_xy = [self.rect.x,self.rect.y]
            self.variation_count = 0




class Player(Character):
    def __init__(
        self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255, 
        dict_sprite={
            'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
            'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
        }, 
        position=[0,0], limit_xy=[0,0], color_sprite=[153,252,152], 
        sprite_difference_xy=[0,-(pixel_space_to_scale//2)]
    ):
        
        super().__init__( 
            size=size, 
            transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
            dict_sprite=dict_sprite, position=position, limit_xy=limit_xy, color_sprite=color_sprite,
            sprite_difference_xy=sprite_difference_xy
        )
        
        self.change_level = True
        
        # Transparencia
        #...
        
        # Teclas de movimiento
        self.pressed_jump       = player_key['jump']
        self.pressed_left       = player_key['left']
        self.pressed_right      = player_key['right']
        self.pressed_up         = player_key['up']
        self.pressed_down       = player_key['down']
        self.pressed_walk       = player_key['walk']
        self.pressed_action     = player_key['action']
        
        # Grupo de sprites
        player_objects.add(self)
    
    
    def move(self):
        # Movimiento | Funcion que se encarga de saber si se han percionado las Teclas de movimiento
        pressed_keys = pygame.key.get_pressed()

        self.left = pressed_keys[self.pressed_left]
        self.right = pressed_keys[self.pressed_right]
        self.up = pressed_keys[self.pressed_up]
        self.down = pressed_keys[self.pressed_down]
        self.walk = pressed_keys[self.pressed_walk]
        if pressed_keys[self.pressed_jump]:
            self.set_and_jump( multipler=1 )
        self.action = pressed_keys[self.pressed_action]
        
        



class Player_old(pygame.sprite.Sprite):
    def __init__( 
        self, position=[0, 0], size=pixel_space_to_scale, 
        transparency_collide=255, transparency_sprite=255,
        color_sprite=[153,252,152] 
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        size = [size//2, size]
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.surf.fill( generic_colors(color='green', transparency=self.transparency_collide ) )
        
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.x += size[0]//2
        layer_all_sprites.add(self, layer=3)
        player_objects.add(self) # Para que la lluvia colisione
        
        # Sprite GUN
        #self.sprite_gun = pygame.sprite.Sprite()
        self.gun_surf = pygame.Surface( [size[1], size[1]], pygame.SRCALPHA)
        palote = pygame.Surface( [size[1], size[1]//2 ], pygame.SRCALPHA )
        palote.fill( (127, 127, 127) )
        self.gun_surf.blit( palote, [0, size[1]//2 - size[1]//4 ] )

        puntito = pygame.Surface( [size[1]//4, size[1]//4], pygame.SRCALPHA )
        puntito.fill( [255,0,0] )
        self.gun_surf.blit( puntito, [ size[1] -size[1]//4, size[1]//2 - size[1]//8 ] )
        
        self.gun_surf.set_alpha(127)
        
        self.sprite_gun = SpritePasteRect( self.gun_surf, self.rect )
        update_objects.add( self.sprite_gun )
        layer_all_sprites.add( self.sprite_gun, layer=4 )
        
        # Sprite
        size_sprite = [pixel_space_to_scale*2, pixel_space_to_scale*2]
        self.sprite_player_not_move = get_image( 
            'player_not-move', size=size_sprite, color=color_sprite, colored_method='surface', transparency=self.transparency_sprite
        )
        self.sprite_player_move = get_image( 
            'player_move', size=size_sprite, color=color_sprite, colored_method='surface', transparency=self.transparency_sprite
        )
        self.sprite_player_move_invert = get_image( 
            'player_move', size=size_sprite, color=color_sprite, colored_method='surface', flip_x=True, transparency=self.transparency_sprite
        )
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = self.sprite_player_not_move[0]
        self.sprite.rect = self.sprite.surf.get_rect( topleft=self.get_position_for_sprite() )
        layer_all_sprites.add(self.sprite, layer=2)
        

        # Movimiento
        self.not_move = False
        self.damage_effect = False
        self.moving_xy = [0,0]
        self.hp = 100
        self.speed = size[1]*0.5
        self.collision_solid = None
        self.angle = 0
        self.side_positive = True
        
        # Valores de porcentaje para poder gravedad usados 
        # 0.0625 0.05 0.025 0.028125 0.03125 0.015625
        # Valores de porcentaje para limite gravedad usados 00.375 0.35 0.3125 0.03 0.306 0.25 
        self.gravity_power = size[1]*0.03125  #0.03125#0.0625
        self.gravity_limit = size[1]-1#*0.75#0.25
        self.gravity_current = -self.gravity_power # Para que empieze en 0 poder de gravedad
        self.air_count = 8 # Para que inicie en caida
        
        self.move_jump = False
        self.jump_power = size[1]*0.5
        self.jump_count = 0
        self.jump_max_height = size[1]*4
        self.jumping = False

        # Movimiento | Sonido contador de pasos
        self.step_count = 0
        self.state_collide_in_floor = 'wait'
        
        # Movimiento | Teclas de movimiento y variables de movimiento
        self.action = False
        self.pressed_jump       = player_key['jump']
        self.pressed_left       = player_key['left']
        self.pressed_right      = player_key['right']
        self.pressed_up         = player_key['up']
        self.pressed_down       = player_key['down']
        self.pressed_walk       = player_key['walk']
        self.pressed_action     = player_key['action']
        
        
    def get_position_for_sprite(self):
        return [self.rect.x -self.rect.width*1.5, self.rect.y -self.rect.height]

    def get_speed( self, multipler=1 ):
        return self.speed*multipler
    
    def get_max_hp( self, multipler=1 ):
        return int(100*multipler)
    
    
    def move(self):
        # Movimiento | Funcion que se encarga de saber si se han percionado las Teclas de movimiento
        pressed_keys = pygame.key.get_pressed()

        self.move_left = pressed_keys[self.pressed_left]
        self.move_right = pressed_keys[self.pressed_right]
        self.move_up = pressed_keys[self.pressed_up]
        self.move_down = pressed_keys[self.pressed_down]
        self.walking = pressed_keys[self.pressed_walk]
        self.action = pressed_keys[self.pressed_action]
        

    def jump(self, multipler=1):
        self.move_jump = True
        self.jump_max_height = (self.rect.height*4)*multipler
        
        
    def collision_no_solid(self):
        # Colision | Objetos dañinos
        damage_number = int
        self.damage_effect = False

        for obj in damage_objects:
            # Determinar si se colisiono con un objeto dañino y obtener el numero de daño.
            if self.rect.colliderect(obj.rect):
                self.damage_effect = True                
                damage_number = obj.damage
        
        if self.damage_effect == True and self.dead == False:
            #self.gravity_current = 0 # Cancelar gravedad
            #self.air_count = 0 # Cancelar gravedad
            self.jumping=False # Cancelar salto
            # Efecto de daño basado en el numero de daño recibido
            multipler = 1
            if isinstance(damage_number, int):
                if damage_number > 0:
                    multipler = damage_number*0.05

            xy_move = self.rect.height * multipler
            if random.choice( [False, True] ):
                self.moving_xy[1] -= xy_move*0.2
            else:
                self.moving_xy[1] -= xy_move
            if random.choice( [False, True] ):
                self.moving_xy[0] += xy_move
            else:
                self.moving_xy[0] -= xy_move
        if isinstance(damage_number, int):
            # Reducir HP
            if self.dead == False:
                if damage_number <= 0:
                    self.hp = -1
                else:
                    self.hp -= damage_number
        
        
        # Colision | Objetos | Cambio de nivel
        for level in level_objects:
            if self.rect.colliderect(level.rect):
                level.change_level = True
                self.hp = 100
                self.rect.topleft = (level.rect.x+(self.rect.width//2), level.rect.y)
                self.moving_xy = [0,0]
                # hp al 100, para si o si que el player este vivo
                

        # Colision | Objetos | Score-Monedas
        for score in score_objects:
            if self.rect.colliderect(score.rect):
                score.point = True
                ( random.choice(sounds_score) ).play()
                if (
                    self.hp < 100 and
                    (self.dead == False)
                ):
                    self.hp += 10
                
        
        # Colision | Trampoline
        for obj in jumping_objects:
            if self.rect.colliderect(obj.rect):
                if self.moving_xy[1] > 0:
                    self.rect.bottom = obj.rect.top - obj.rect.height
                    self.gravity_current = 0
                self.air_count = 0
                self.jump(multipler=2)
        

        # Colision | Solidos | Escalera
        if pygame.sprite.spritecollide(self, ladder_objects, False):
            if self.move_down == False:
                self.gravity_current = 0
                self.air_count = 0
                
        # Colision | Solidos | Elevador
        for obj in moving_objects:
            if self.rect.colliderect(obj.rect):
                self.gravity_current = 0
                self.air_count = 0

                if isinstance(self.collision_solid, str): 
                   if self.rect.y > obj.rect.y: self.jump(multipler=0.5)
                   if self.collision_solid == 'top' or self.collision_solid == 'bottom':
                       self.hp = -1
                       self.not_move = True
                   #self.hp = -1
                   #self.not_move = True

                else:
                    if self.rect.y <= obj.rect.y:
                        self.rect.bottom = obj.rect.top+1
                    elif self.rect.y > obj.rect.y:
                        self.jump(multipler=0.5)
            
                if self.dead == False:
                    if obj.move_dimension == 1:
                        if obj.move_positive == True:   self.moving_xy[0] += obj.speed
                        else:                           self.moving_xy[0] -= obj.speed
                    if obj.move_dimension == 2:
                        if obj.move_positive == True:   self.moving_xy[1] += obj.speed
                        else:                           self.moving_xy[1] -= obj.speed

                        


    def sprite_anim(self, fall=False, speed_multipler=1):    
        # Animacion | Sprites | Surface | Collider
        flip_image = False
        moving = False
        if self.move_left == True:
            flip_image = True
            moving = True
        elif self.move_right == True: moving = True
        if self.move_left == True and self.move_right == True: moving = False
        if moving == False or self.jumping == True or fall == True: self.step_count = 0
 
        if self.jumping == True:
            if moving == False:
                self.surf.fill( generic_colors('blue') )
                self.sprite.surf = self.sprite_player_not_move[1]
            elif moving == True: 
                self.surf.fill( (0, 19, 63) )
                self.sprite.surf = pygame.transform.flip( self.sprite_player_move[1], flip_image, False )
        elif fall == True:
            if moving == False:
                self.surf.fill( generic_colors('sky_blue') )
                self.sprite.surf = self.sprite_player_not_move[2]
            elif moving == True: 
                self.surf.fill( (0, 126, 255) )
                self.sprite.surf = pygame.transform.flip( self.sprite_player_move[6], flip_image, False )
        elif fall == False:
            if moving == False:
                self.surf.fill( generic_colors('green') )
                self.sprite.surf = self.sprite_player_not_move[0]
            elif moving == True: 
                self.surf.fill( generic_colors('yellow') )
                self.step_count = ( 
                    (self.step_count +(1*speed_multipler)) % len(self.sprite_player_move) 
                )
                self.sprite.surf = pygame.transform.flip( 
                    self.sprite_player_move[int(self.step_count)], flip_image, False 
                )

        self.surf.set_alpha(self.transparency_collide)
        self.sprite.surf.set_alpha(self.transparency_sprite)
        position = self.get_position_for_sprite() 
        self.sprite.rect.x = position[0]
        self.sprite.rect.y = position[1]
        
        
        
        
    def sound(self):
        # Sonido hits
        if self.damage_effect == True and self.dead == False: get_sound('hits').play()
        
        # Sonido | Pasos | Saltar | Colisionar con piso
        if (
            ( self.step_count == len(self.sprite_player_move) *0.5 ) or
            ( self.state_collide_in_floor == 'yes' )
        ):
            get_sound('steps').play()
            Particle( 
                size=[pixel_space_to_scale//4, pixel_space_to_scale//4], 
                position=[self.rect.x, self.rect.y-1+self.rect.height-pixel_space_to_scale//4], 
                transparency_collide=255, transparency_sprite=255, 
                color_collide=generic_colors('grey'), time_kill=data_CF.fps, sound=None
            )
        
        if self.jumping == True and self.jump_count == self.jump_power:
            get_sound('jump').play()
    
    
    
    
    def update(self, old_gravity=True):
        # Movimiento | Actualizar movimiento del jugador
        
        # HP | Determinar si el jugador esta vivo o muerto
        if self.hp <= 0:
            self.dead = True
            self.not_move = True
            self.jump_count = self.jump_max_height
            self.gravity_current = 0
        else:
            self.dead = False
            if self.hp > self.get_max_hp(multipler=1): self.hp = self.get_max_hp(multipler=1)

        # Dejar de moverse
        if self.not_move == True or self.damage_effect == True:
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = False
            self.move_jump = False
            self.walking = False
            self.action = False

        # Disparo
        if self.action:
            bullet = Bullet(
               size=[self.rect.height//4, self.rect.height//4], position=self.rect.center, image=None,
               speed_xy=speed2d_with_angle( self.rect.height, self.angle ), time=90
            )
            bullet.rect.center = self.rect.center
        self.action = False
        
        
        
        # Cambiar angulo
        if self.side_positive == True:
            speed_move_angle = 2
        else:
            speed_move_angle = -2

        if self.move_up == True:
            self.angle += speed_move_angle
        if self.move_down == True:
            self.angle -= speed_move_angle

        # Bloquear rotación
        if self.side_positive == True:
            if self.angle > 90:
                self.angle = 90
            elif self.angle < -90:
                self.angle = -90
        else:
            if self.angle < -180-90:
                self.angle = -180-90
            elif self.angle > -180+90:
                self.angle = -180+90
        #elif self.angle < 0:
        #    self.angle = 0



        # Detectar si esta en el piso o no
        # Esto se determina dependiendo la cantidad de frames en las que el jugador esta en el aire
        # Entre mas alto, major funciona en res bajas, y entre mas bajo mejor funciona en res altas.
        if self.air_count <= air_count_based_on_resolution:
            #print('En el piso')
            fall = False
            if self.state_collide_in_floor == 'wait':
                self.state_collide_in_floor = 'yes'
            elif self.state_collide_in_floor == 'yes':
                self.state_collide_in_floor = 'no'
        else:
            #print('Cayendo')
            fall = True
            self.state_collide_in_floor = 'wait'
        
        
        
        
        # Determinar velocidad del jugador
        if self.walking == True:
            # valores usados: 0.25 0.5 0.625
            speed_multipler = 0.5
        else:
            speed_multipler = 1
            self.step_count = int(self.step_count)
        speed = self.get_speed(multipler=speed_multipler)
        
        
        
        # Mover el jugador
        self.moving_xy = [0,0]
        if self.move_left == True:  
            self.moving_xy[0] -= speed
            self.angle = -180
            self.side_positive = False
        if self.move_right == True: 
            self.moving_xy[0] += speed
            self.angle = 0
            self.side_positive = True
        if self.move_jump == True:
            if fall == False:
                self.jumping = True
                self.move_jump = False
        self.move_jump = False # Para que no puedas inicializar el salto en el aire.
        
        
        
        
        # Gravedad | Caida
        self.moving_xy[1] += self.gravity_current
        if old_gravity == True:
            self.gravity_current = self.rect.height//4
        else:
            # Modo moderno
            if self.gravity_current < self.gravity_limit:
                self.gravity_current += self.gravity_power
            else:
                self.gravity_current = self.gravity_limit
        
        
        
        
        # Salto
        if self.jumping == True:
            self.gravity_current, self.moving_xy[1] = 0, 0
            self.jump_count += self.jump_power
            if self.jump_count <= self.jump_max_height:
                self.moving_xy[1] -= self.jump_power
                self.jumping = True
            else: self.jumping = False

        else: self.jump_count = 0
        
        # Colisiones | Solidos
        self.collision_solid = collide_and_move(obj=self, obj_movement=self.moving_xy, solid_objects=solid_objects)
        
        if self.collision_solid == 'bottom':
            self.gravity_current = 0
            self.air_count = 0
        else:
            self.air_count += 1
        
        if self.collision_solid == 'top':
            self.gravity_current = 0
            
            self.jumping = False
            self.jump_count = 0
        
        # Colision No solidos
        self.moving_xy = [0,0]
        if self.dead == False: self.collision_no_solid()
        
        # Colisiones | Solidos
        self.collision_solid = collide_and_move(obj=self, obj_movement=self.moving_xy, solid_objects=solid_objects)
        
        if self.collision_solid == 'bottom':
            self.gravity_current = 0
            #self.air_count = 0
        else:
            pass#self.air_count += 1
        
        if self.collision_solid == 'top':
            self.gravity_current = 0
            
            self.jumping = False
            self.jump_count = 0
        
        # Sprite gun
        self.sprite_gun.angle = self.angle
        self.sprite_gun.rotate()
        
        # Anim
        self.sprite_anim(fall=fall, speed_multipler=speed_multipler)
        
        # Sound
        self.sound()



class Anim_player_dead(pygame.sprite.Sprite):
    def __init__(
        self, position=[0,0], fps=data_CF.fps, 
        transparency_collide=255, transparency_sprite=255,
        color_sprite=(153, 252, 152) 
    ):
        super().__init__()

        # Transparencia        
        self.transparency_collide=transparency_collide
        self.transparency_sprite=transparency_sprite

        # Principal
        self.size = pixel_space_to_scale
        self.surf = pygame.Surface( (self.size, self.size), pygame.SRCALPHA )
        self.rect = self.surf.get_rect( topleft=position )
    
        self.fps = data_CF.fps*3
        self.__count = 0
        self.anim_fin = False
        anim_sprites.add( self )
        layer_all_sprites.add(self, layer=2)
        
        # Partes
        size_parts = self.size//2
        img = get_image( 
            'player_not-move', number=0, size=[pixel_space_to_scale*2, pixel_space_to_scale*2],
            colored_method='surface', color=color_sprite
        )
        img = Split_sprite(sprite_sheet=img, parts=8)
        self.part1 = Particle( 
            size=[size_parts, size_parts], position=[ self.rect.x, self.rect.y+size_parts ],
            image=img[13], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
            time_kill=self.fps, sound='player'
        )
        
        self.part2 = Particle( 
            size=[size_parts, size_parts], position=[self.rect.x+size_parts, self.rect.y+size_parts ],
            image=img[14], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
            time_kill=self.fps, sound='player'
        )
        
        self.part3 = Particle( 
            size=[size_parts, size_parts], position=[self.rect.x, self.rect.y],
            image=img[9], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
            time_kill=self.fps, sound='player'
        )

        self.part4 = Particle( 
            size=[size_parts, size_parts], position=[self.rect.x+size_parts, self.rect.y],
            image=img[10], transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
            time_kill=self.fps, sound='player'
        )
    
    def anim(self):
        # Contador 
        self.__count += 1
        if self.__count*5 <= 128:
            self.surf.fill( ( 255-(self.__count*5), 0, 0, self.transparency_collide)  )

        if self.__count == self.fps:
            # Animacion terminada, todos los objetos se eliminaran
            self.anim_fin = True
            self.kill()




class Particle(pygame.sprite.Sprite):
    def __init__(
        self, size=[pixel_space_to_scale//2, pixel_space_to_scale//2], position=[0,0],
        color_collide=generic_colors('green'), color_sprite=None,
        transparency_sprite=255, transparency_collide=255,
        time_kill=0, image=None, sound=None
    ):
        super().__init__()
        
        # 
        self.sounds_str = None
        if sound == 'player':
            self.sounds_str = ['steps', 'hits']
            
        
        # Transparencia de collider y imagen
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.surf.fill( color_collide )
        self.surf.set_alpha( self.transparency_collide )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=2)
        anim_sprites.add(self)
        particle_objects.add(self)
        
        # Imagen
        if type(image) == pygame.Surface:
            rect = image.get_rect()
            if rect.x != self.rect.x or rect.y != self.rect.y:
                image = pygame.transform.scale(image, size)
                
            self.image = pygame.sprite.Sprite()
            self.image.surf = image
            self.image.surf.set_alpha( self.transparency_sprite )
            self.image.rect = self.image.surf.get_rect( topleft=position )
            layer_all_sprites.add(self.image, leyer=1)
        else: self.image = None
        
        # Movimiento
        self.moving_xy = [0,0]
        
        self.gravity_power = random.choice( [size[0]*0.025, size[0]*0.05] )
        self.gravity_limit = size[0]*0.75
        self.gravity_current = -self.gravity_power # Para que inicie callendo
        self.air_count = 8 # 8 Para que inicie en caida
        self.gravity = True
        
        self.move_positive_x = random.choice( [False,True] )
        self.speed = random.randint( size[0]//4, size[0]//2 )

        self.jumping = random.choice( [False, True] )
        self.jump_power = random.choice( [size[0]*0.125, size[0]*0.25, size[0]*0.4] )
        
        # Tiempo para eliminar la particula
        self.time_kill = time_kill
        self.time_kill_count = 0
    
    def anim(self):
        # Movimiento en x
        if self.move_positive_x == True:    self.moving_xy[0] = self.speed
        else:                               self.moving_xy[0] = -self.speed
    
        # Detectar si esta callendo o no
        if self.air_count <= air_count_based_on_resolution: fall = False
        else:                                               fall = True
        
        # Salto
        if fall == False:
            self.gravity_current = -self.jump_power
        if self.jumping == True:
            self.jumping = False
            self.gravity_current = -self.jump_power
        
        # Gravedad
        if self.gravity == True:
            self.moving_xy[1] = self.gravity_current
            if self.gravity_current < self.gravity_limit:   self.gravity_current += self.gravity_power
            else:                                           self.gravity_current = self.gravity_limit
        
        
        # Colision objetos dañinos
        damage_effect=False
        for obj in damage_objects:
            if self.rect.colliderect(obj.rect):
                damage_effect=True
        if damage_effect == True:
            self.moving_xy[0] += self.rect.width * random.choice([1,-1])
            self.moving_xy[1] += self.rect.height * random.choice([1,-1])
        
        # Mover y colisionar Solidos
        collide_objects = []
        for obj in solid_objects: collide_objects.append(obj)
        for obj in particle_objects: 
            if not obj == self: 
                collide_objects.append(obj)
        for obj in jumping_objects: collide_objects.append(obj)
        collided_side = collide_and_move( 
            obj=self, obj_movement=self.moving_xy, solid_objects=collide_objects
        )
        self.air_count += 1
        if collided_side == 'bottom':
            self.gravity_current = 0
            self.air_count = 0
        elif collided_side == 'top': self.gravity_current = 0
        elif collided_side == 'right': self.move_positive_x = False
        elif collided_side == 'left': self.move_positive_x = True
        
        
        
        # Posicionear imagen
        if not self.image == None:
            self.image.rect.x = self.rect.x
            self.image.rect.y = self.rect.y
        
        
        # Sonido
        if isinstance(self.sounds_str, list):
            if damage_effect == True: get_sound(sound=self.sounds_str[1]).play()
            if isinstance(collided_side, str): get_sound(sound=self.sounds_str[0]).play()


        # Tiempo de vida
        if self.time_kill > 0:
            self.time_kill_count += 1
            if self.time_kill_count == self.time_kill:
                if not self.image == None: self.image.kill()
                self.kill()



class Floor( SpriteMultiLayer ):
    '''
    El piso del videojuego Cuadrado Feliz
    '''
    def __init__(
        self, size = [pixel_space_to_scale, pixel_space_to_scale], position = [0,0], 
        transparency_collide=255, transparency_sprite=255, color=None, limit=True, climate=None
    ):
        
        # Establecer color
        random_more_color = random.choice( [8, 16, 32] )

        if climate == 'alien':
            color = [0,random_more_color,random_more_color]#'sky_blue'

        elif climate == 'sunny':
            color = [random_more_color,0,0]#'red'

        elif climate == 'rain':
            color = [0,0,random_more_color]#'blue'

        elif climate == 'black':
            color = [
                (random_more_color//2),
                random_more_color,
                0
            ]#'Verde amarillento'
        else:
            color = generic_colors('grey')
        
        # Iniziar uso de SpriteMultiLayer
        super().__init__( 
            surf=pygame.Surface(size, pygame.SRCALPHA), transparency=transparency_collide, position=position,
            layer=[get_image( 'stone', size=size, color=color )], 
            layer_transparency=transparency_sprite, layer_difference_xy=[0,0]
        )
        
        # Cambiar color de collider
        #self.surf.fill( color )
        self.surf.fill( generic_colors('grey') )
        self.set_transparency()
        layer_all_sprites.add( self, layer=2 )
        solid_objects.add(self)
        
        # Agregar a grupos al Sprite
        self.sprite_layer.add_to_sprite_group( update_objects )
        self.sprite_layer.add_to_layer_group( layer_all_sprites, layer=1 )
        
        # Agregar o no limite
        self.limit_collision( limit )
    
    def limit_collision(self, limit=False):
        # Para agergar un objeto en medio del floor que mate por si traspasa el collider.
        pass




class Ladder(pygame.sprite.Sprite):
    def __init__(self, size=pixel_space_to_scale, position=[0,0],
        transparency_collide=255, transparency_sprite=255
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider y surface
        size_collide = round(size*0.75)
        self.surf = pygame.Surface( (size_collide, size_collide), pygame.SRCALPHA )
        self.surf.fill( (113,77,41, self.transparency_collide) )
        self.rect = self.surf.get_rect( 
            topleft=( position[0]+size_collide*0.25, position[1]+size_collide*0.25 ) 
        )
        layer_all_sprites.add(self, layer=2)
        ladder_objects.add(self)
        
        # Sprite
        sprite = pygame.sprite.Sprite()
        sprite.surf = get_image('ladder', size=[size, size], transparency=self.transparency_sprite)
        sprite.rect = sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add(sprite, layer=1)



class Trampoline(pygame.sprite.Sprite):
    def __init__(self, size=pixel_space_to_scale, position=[0,0],
        transparency_collide=255, transparency_sprite=255
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collide
        self.surf = pygame.Surface( (size, size//8), pygame.SRCALPHA )
        self.surf.fill( generic_colors('sky_blue', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.y += self.rect.height//2
        
        layer_all_sprites.add(self, layer=2)
        jumping_objects.add(self)
        
        # Sprite
        sprite = pygame.sprite.Sprite()
        sprite.surf = get_image( 'trampoline', size=(size, size), transparency=self.transparency_sprite )
        sprite.rect = sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add( sprite, layer=1 )




class Elevator(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=(0,0),
        transparency_collide=255, transparency_sprite=255, move_dimension=1
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        size_ready = (size*2, size)
        self.surf = pygame.Surface( size_ready, pygame.SRCALPHA)
        self.surf.fill( generic_colors('grey', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=2)
        moving_objects.add(self)
        anim_sprites.add(self)
        
        # Sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = get_image('elevator', size=size_ready, transparency=self.transparency_sprite)
        self.sprite.rect = self.sprite.surf.get_rect( topleft=(self.rect.x, self.rect.y) )
        layer_all_sprites.add(self.sprite, layer=1)
        
        # Velocidades
        self.move_dimension = move_dimension
        self.move_positive = True#bool(random.getrandbits(1))
        #self.speed = int( (size)*0.25 ) # Entero, funcional, pero demasiado rapido | 4
        #self.speed = int( (size)*0.125 ) # Entero, funcional, pero demasiado lento | 2

        # Decimal, funcinal pero en resoluciones inferiores a 960 irregular | 3
        # Por default; 4.5, no se redondea a 5, se rodondea a 4. 1.5 a 2.
        # Esto se debe a la Regla del redondeo. Se redondeara siempre al numero par mas cercano.
        self.speed = int( (size)*0.1875 )
        #if self.speed == 2:
        #    self.speed = 1

        #print(self.speed)
    
    def anim(self):
        # Si colisiona con algun objeto solido.
        #if pygame.sprite.spritecollide(self, solid_objects, False):
        for obj in solid_objects:
            #collision = obj_collision_sides_solid(obj_main=self, obj_collide=obj)
            #if not collision == None:
            #    self.move_positive = bool(random.getrandbits(1))
            if self.rect.colliderect(obj.rect):
                if self.rect.x > obj.rect.x: #- (self.speed/8):
                    self.move_positive = True
                elif self.rect.x < obj.rect.x: #+ (self.speed/8):
                    self.move_positive = False
                    
                if self.rect.y > obj.rect.y: #- (self.speed/8):
                    self.move_positive = True
                elif self.rect.y < obj.rect.y: #+ (self.speed/8):
                    self.move_positive = False
    
        # Moverse positivo o negativamente
        if self.move_dimension == 1:
            if self.move_positive == True:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
        elif self.move_dimension == 2:
            if self.move_positive == True:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
                
        # Sprite
        self.sprite.rect.x = self.rect.x
        self.sprite.rect.y = self.rect.y




class Spike( SpriteMultiLayer ):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0], transparency_collide=255, transparency_sprite=255,
        moving=False, instakill=False
    ):  
        # Establecer color y daño
        self.__color = (0, 0, 71)
        if instakill == True:
            self.__color = (71, 0, 0)
            self.damage = 0
        else:
            self.damage = 20
        
        # Inicializar SpriteMultiLayer
        super().__init__( 
            surf=pygame.Surface( (size/4, size/2), pygame.SRCALPHA ), transparency=transparency_collide,
            position=position, layer=[ 
                get_image(
                    'spike', colored_method='normal',  color=self.__color, size=[size,size]
                )
            ],
            layer_transparency=transparency_sprite, layer_difference_xy=[0,size*0.25]
        )
        
        # Añadir a los grupos de sprites
        # Daño
        if moving == True:
            anim_sprites.add(self)

        
        # Collider
        self.surf.fill( generic_colors(color='red') )
        self.set_transparency()
        self.rect.x += (size-self.rect.width)//2
        damage_objects.add(self)
        layer_all_sprites.add(self, layer=3)
        
        # Sprite
        self.sprite_layer.set_transparency_layer()
        self.sprite_layer.update_layer() # Establecer posición
        self.sprite_layer.add_to_layer_group( layer_all_sprites, layer=1 )
        
        # Cuadrados solidos
        square_size = self.rect.height
        floor_x = Floor(
            size = ( square_size, square_size ),
            position = [position[0], position[1]+square_size],
            transparency_collide=transparency_collide, transparency_sprite=0,
            limit = False
        )
        
        floor_y = Floor(
            size = ( square_size, square_size ),
            position = [position[0]+square_size, position[1]+square_size],
            transparency_collide=transparency_collide, transparency_sprite=0,
            limit = False
        )
        
        # Mover o no sprite
        self.size = size
        self.size_y = size
        self.moving = moving
        self.__move_count = 0
        self.__move_pixels = size*4
        self.__move_speed = size//2
        self.__move_type = 'UP'
    
    def anim(self):
        # Solo se activa esta función si se mueve el picote
        if self.moving == True:
            if self.__move_type == 'UP':
                self.__move_count += self.__move_speed                
                self.size_y += self.__move_speed

                self.surf = pygame.Surface( (self.rect.width, self.size_y), pygame.SRCALPHA )
                self.surf.fill( generic_colors(color='red', transparency=self.transparency) )
                position = (self.rect.x, self.rect.y)
                self.rect = self.surf.get_rect( topleft=position )
                self.rect.y -= self.__move_speed
                
                if not self.sprite_layer.layer[0] == None:
                    self.sprite_layer.layer[0].surf = pygame.transform.scale(
                        self.sprite_layer.layer[0].surf_base, (self.size, (self.size_y))
                    )
                    self.sprite_layer.layer[0].rect.y -= self.__move_speed
                
                if self.__move_count >= self.__move_pixels:
                    self.__move_type = 'DOWN'

            elif self.__move_type == 'DOWN':
                self.__move_count -= self.__move_speed//2
                self.size_y -= self.__move_speed//2

                self.surf = pygame.Surface( (self.rect.width, self.size_y), pygame.SRCALPHA )
                self.surf.fill( generic_colors(color='red', transparency=self.transparency) )
                position = (self.rect.x, self.rect.y)
                self.rect = self.surf.get_rect( topleft=position )
                self.rect.y += self.__move_speed//2
                
                if not self.sprite_layer.layer[0] == None:
                    self.sprite_layer.layer[0].surf = pygame.transform.scale(
                        self.sprite_layer.layer[0].surf_base, (self.size, (self.size_y))
                    )
                    self.sprite_layer.layer[0].rect.y += self.__move_speed//2
                
                if self.__move_count <= 0:
                    self.__move_type = 'UP'




class Star_pointed(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0], transparency_collide=255, transparency_sprite=255,
        moving=False, instakill=False
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Movimiento variables
        self.moving = moving
        self.instakill = instakill
        self.count_moving = 0
        self.moving_pixels = size*4
        self.moving_speed = size//4
        
        # Collider principal
        self.surf = pygame.Surface( ( size/2, size/2 ), pygame.SRCALPHA )
        self.surf.fill( generic_colors('green', self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.x += (size -self.rect.width)//2
        self.rect.y += (size -self.rect.height)//2
        
        layer_all_sprites.add(self, layer=2)
        anim_sprites.add(self)
        
        # Sprite
        self.__size = size
        if self.instakill == True:
            color = [95, 0, 0]
        else:
            color = [0, 0, 127]

        self.sprite = Anim_sprite(
            sprite_sheet=get_image(
                'star-pointed', size=[self.__size*7, self.__size], return_method='image', color=color,
                transparency=self.transparency_sprite
            )
        )
        self.sprite.rect.topleft = (
            self.rect.x-(self.__size//4),
            self.rect.y-(self.__size//4)
        )
        layer_all_sprites.add(self.sprite, layer=1)
        
        # Cuadrados dañinos
        size_square = self.rect.width/2
        
        self.square_x1 = self.square_damage(
            size=size_square, position=(self.rect.x, self.rect.y +(size_square//2) ),
            color=generic_colors('black', self.transparency_collide)
        )
        self.square_x2 = self.square_damage(
            size=size_square, position=(
                self.rect.x-size_square, self.rect.y +(size_square//2) 
            ),
            color=generic_colors('red', self.transparency_collide)
        )
        self.square_x3 = self.square_damage(
            size=size_square, position=(self.rect.x+size_square, self.rect.y +(size_square//2) ),
            color=generic_colors('grey', self.transparency_collide)
        )
        self.square_x4 = self.square_damage(
            size=size_square, position=(self.rect.x+(size_square*2), self.rect.y +(size_square//2) ),
            color=generic_colors('blue', self.transparency_collide)
        )
        
        # Animacion Variables
        self.__size_square = size_square
        self.__move = 0
        self.__size_square_percentage_50 = self.__size_square//2
        self.__size_square_percentage_150 = self.__size_square*1.5
        self.__size_square_percentage_300 = self.__size_square*3

    def square_damage(self, size=4, position=(0,0), color=generic_colors('green')):
        # Cuadrado de daño
        # Daño
        square = pygame.sprite.Sprite()
        square.surf = pygame.Surface( (size, size), pygame.SRCALPHA )
        square.surf.fill( color )
        square.rect = square.surf.get_rect( topleft=position)
        layer_all_sprites.add(square, layer=2)
        if self.instakill == True:
            square.damage = 0
        else:
            square.damage = 10
        damage_objects.add(square)
        return square
    
    def anim(self):
        # Animación del sprite
        self.sprite.anim()
        
        # Movimiento estandar del collider
        if self.__move == 0:
            self.__move = 0.1

        elif self.__move == 0.1:
            self.square_x2.rect.y -= self.__size_square_percentage_150
            self.square_x1.rect.y -= self.__size_square_percentage_50
            
            self.square_x4.rect.y += self.__size_square_percentage_150
            self.square_x3.rect.y += self.__size_square_percentage_50
            self.__move = 0.2

        elif self.__move == 0.2:
            self.square_x2.rect.x += self.__size_square_percentage_150
            self.square_x1.rect.x += self.__size_square_percentage_50
        
            self.square_x4.rect.x -= self.__size_square_percentage_150
            self.square_x3.rect.x -= self.__size_square_percentage_50
            self.__move = 0.3

        elif self.__move == 0.3:
            self.square_x2.rect.x += self.__size_square_percentage_150
            self.square_x1.rect.x += self.__size_square_percentage_50
        
            self.square_x4.rect.x -= self.__size_square_percentage_150
            self.square_x3.rect.x -= self.__size_square_percentage_50
            self.__move = 0.4

        elif self.__move == 0.4:
            self.square_x2.rect.y += self.__size_square_percentage_150
            self.square_x1.rect.y += self.__size_square_percentage_50
            self.square_x2.rect.x -= self.__size_square_percentage_300
            self.square_x1.rect.x -= self.__size_square
            
            self.square_x4.rect.y -= self.__size_square_percentage_150
            self.square_x3.rect.y -= self.__size_square_percentage_50
            self.square_x4.rect.x += self.__size_square_percentage_300
            self.square_x3.rect.x += self.__size_square
            self.__move = 0.1

        
        # Si la estrella se va a mover
        if self.moving == True:
            if self.count_moving < self.moving_pixels:
                self.count_moving += self.moving_speed
                self.rect.x += self.moving_speed

                self.square_x1.rect.x += self.moving_speed
                self.square_x2.rect.x += self.moving_speed
                self.square_x3.rect.x += self.moving_speed
                self.square_x4.rect.x += self.moving_speed

                self.sprite.rect.x += self.moving_speed
            elif self.count_moving >= self.moving_pixels:
                if self.count_moving < self.moving_pixels*1.5:
                    self.count_moving += self.moving_speed
                    self.rect.y -= self.moving_speed

                    self.square_x1.rect.y -= self.moving_speed
                    self.square_x2.rect.y -= self.moving_speed
                    self.square_x3.rect.y -= self.moving_speed
                    self.square_x4.rect.y -= self.moving_speed

                    self.sprite.rect.y -= self.moving_speed
                elif self.count_moving >= self.moving_pixels*1.5:
                    if self.count_moving < self.moving_pixels*2.5:
                        self.count_moving += self.moving_speed
                        self.rect.x -= self.moving_speed

                        self.square_x1.rect.x -= self.moving_speed
                        self.square_x2.rect.x -= self.moving_speed
                        self.square_x3.rect.x -= self.moving_speed
                        self.square_x4.rect.x -= self.moving_speed

                        self.sprite.rect.x -= self.moving_speed

                    elif self.count_moving >= self.moving_pixels*2.5:
                        if self.count_moving < self.moving_pixels*3:
                            self.count_moving += self.moving_speed
                            self.rect.y += self.moving_speed

                            self.square_x1.rect.y += self.moving_speed
                            self.square_x2.rect.y += self.moving_speed
                            self.square_x3.rect.y += self.moving_speed
                            self.square_x4.rect.y += self.moving_speed

                            self.sprite.rect.y += self.moving_speed
                        elif self.count_moving == self.moving_pixels*3:
                            self.count_moving = 0




class Stair(pygame.sprite.Sprite):
    def __init__( 
        self, size=pixel_space_to_scale, position=[0, 0], 
        transparency_collide=255, transparency_sprite=255, invert=False, climate=None
    ):
        super().__init__()
        
        # transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite


        # Tamaños y parametros de floor/partes de escalera
        size_part = size//2
        self.climate = climate
        
        # Para posicionar correctamente
        if invert == True:
            more_pixels1 = 0
            more_pixels2 = size_part
            more_pixels3 = -(size)
        else:
            more_pixels1 = size_part
            more_pixels2 = size_part
            more_pixels3 = size        

        # Colliders | Partes de escalera | objetos
        self.stair_part( 
            size=size_part, 
            position=[position[0]+more_pixels1, position[1]]
        )
        self.stair_part( 
            size=size_part, 
            position=[position[0], position[1]+more_pixels2]
        )
        self.stair_part( 
            size=size_part, 
            position=[position[0]+more_pixels2, position[1]+more_pixels2]
        )
        
        self.stair_part( # Parte necesaria para evitar bugs
            size=size, 
            position=(position[0]+more_pixels3, position[1])
        )
        
    def stair_part(self, size=4, position=(0,0) ):
        stair_part = Floor( 
            size=[size, size], position=position, 
            transparency_collide=self.transparency_collide, transparency_sprite=self.transparency_sprite, 
            limit=False, climate=self.climate
        )
        solid_objects.add(stair_part)




class Climate_rain(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=(scale_surface_size[0]//2, scale_surface_size[1]//2),
        transparency_collide=255, transparency_sprite=255, damage=False
    ):
        super().__init__()
        
        # Mostrar Collider o no
        self.transparency_sprite = transparency_sprite
        self.transparency_collide = transparency_collide
        
        # Sección de collider
        self.surf = pygame.Surface( (size//4, size//4), pygame.SRCALPHA )
        self.rect = self.surf.get_rect( topleft=position )
        self.speed_y = random.choice(
            [  
                size//2, 
                ( (size//2) -(size//16) ),
                ( (size//2) -(size//8) )
            ]
        )
        self.speed_x = self.speed_y//2
        self.move = True
        self.not_move = False
        self.spawn_xy = [self.rect.x, self.rect.y]
        
        layer_all_sprites.add(self, layer=1)
        climate_objects.add(self)
        # Establecer que es objeto dañino, con color y grupo de objetos
        if damage == True: 
            self.surf.fill( generic_colors('red', self.transparency_collide) )
            color_sprite = [0,255,0]
            self.damage = 1
            damage_objects.add(self)
        else: 
            self.surf.fill( generic_colors('sky_blue', self.transparency_collide) )
            self.damage = damage
            color_sprite = [0,0,127]
        
        # Sección de sprite
        self.fps = data_CF.fps//4
        self.fps_count = 0
        self.sprite_collide = None
        self.sprite = None
        self.size = size
        self.size_difference = (size//4)*3

        self.__image = get_image( 
            'rain', size=[size,size], color=color_sprite, transparency=self.transparency_sprite
        )
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = self.__image[0]
        self.sprite.rect = self.surf.get_rect( topleft=(self.rect.x,self.rect.y-self.size_difference) )
        layer_all_sprites.add(self.sprite, layer=3)
        
        # Tiempo
        self.time_respawn = 0 # Esta variable se usa en el loop del juego
        
    def update(self):            
        # Mover al jugador si el collider esta en false
        self.collide = False
        if (
            self.collide == False and 
            self.move == True and
            self.not_move == False
        ):
            self.rect.y += self.speed_y
            self.rect.x -= self.speed_x
        
        # Esta variable permite establecer si se quiere parar el movimiento de la lluvia o no.
        #self.not_move = False

        # Eventos | Si traspasa la pantalla
        '''
        transfer_disp = obj_not_see(
            disp_width=scale_surface_size[0], disp_height=scale_surface_size[1], obj=self, difference=(self.size*32)
        )
        if transfer_disp == 'height_positive':
            self.collide = True
        elif (
            transfer_disp == 'width_positive' or
            transfer_disp == 'width_negative'
        ):
            self.not_move = True
        '''

        # Eventos | Si toca objetos solidos
        for solid_object in solid_objects:
            if self.rect.colliderect(solid_object.rect):
                self.collide = True
                self.time_respawn = 1

        # Eventos | Si colisiona con el player        
        for player in player_objects:
            if self.rect.colliderect(player.rect):
                self.collide = True
                if self.damage == False: self.time_respawn = 1
        
        # Sección para mover sprite correctamente
        if not self.sprite == None:
            self.sprite.rect.topleft = (
                self.rect.x, self.rect.y-(self.size_difference)
            )
        
        # Sección para dibujar un sprite al colisionar con piso
        if self.collide == True:
            if self.sprite_collide == None and (not self.sprite == None):
                self.sprite_collide = pygame.sprite.Sprite()
                self.sprite_collide.surf = self.__image[1]
                self.sprite_collide.rect = self.sprite_collide.surf.get_rect()
                self.sprite_collide.rect.topleft = (
                    self.rect.x, self.rect.y-(self.size_difference)
                )
                layer_all_sprites.add(self.sprite_collide, layer=3)
        else:
            if not self.sprite_collide == None:
                self.fps_count += 1
                if self.fps_count == self.fps:
                    self.sprite_collide.kill()
                    self.sprite_collide = None
                    self.fps_count = 0






            
class Limit_indicator(pygame.sprite.Sprite):
    def __init__(self, 
        size=[pixel_space_to_scale, pixel_space_to_scale], transparency_collide=255, position = [0, 0]
    ):
        super().__init__()
        
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.transparency_collide = transparency_collide
        self.surf.fill( generic_colors(color='red', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )

        layer_all_sprites.add(self, layer=1)
        limit_objects.add(self)



class Level_change(pygame.sprite.Sprite):
    def __init__(
        self, level=None, dir_level=None, position=(0,0), gamecomplete=False,
        transparency_collide=255, transparency_sprite=255
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite

        # ...
        if dir_level == None:
            self.dir_level = ''
        else:
            self.dir_level = dir_level

        if level == None:
            self.name = 'cf_map_default.txt'
        else:
            self.name = f'cf_map_{level}.txt'
            if dir_level == '':
                pass
            else:
                self.dir_level = dir_level
        self.change_level = False
        self.level = None
        self.__gamecomplete = gamecomplete
        self.gamecomplete = False
        
        # Collider
        size = (pixel_space_to_scale, pixel_space_to_scale)

        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        if gamecomplete == True:
            self.surf.fill( generic_colors('green', transparency=self.transparency_collide) )
        else:
            self.surf.fill( generic_colors('black', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=2)
        level_objects.add(self)
        
        # Sprite
        sprite = pygame.sprite.Sprite()
        
        if gamecomplete == True:
            sprite.surf = get_image( 
                'level_change', size=size, color=[0, 48, 0], transparency=self.transparency_sprite
            )
        else:
            sprite.surf = get_image( 
                'level_change', size=size, color=[39, 28, 18], transparency=self.transparency_sprite
            )

        sprite.rect = sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add(sprite, layer=1)
    
    def update(self):
        if self.change_level == True:
            self.level = os.path.join( dir_maps, self.dir_level, self.name )
            if self.__gamecomplete == True:
                self.gamecomplete = True




class Score(pygame.sprite.Sprite):
    def __init__(
        self, size=pixel_space_to_scale, position=[0,0], transparency_collide=255, transparency_sprite=255
    ):
        super().__init__()
        
        # Transaparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        self.surf = pygame.Surface( ( size//2, size//2 ), pygame.SRCALPHA )
        self.surf.fill( generic_colors('yellow', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.x += ( size -self.rect.width)//2
        self.rect.y += ( size -self.rect.height)//2
        
        # Agregar collider
        layer_all_sprites.add(self, layer=3)
        score_objects.add(self)
        
        # Sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = get_image( 'coin', size=[size, size], transparency=self.transparency_sprite )
        self.sprite.rect = self.sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add(self.sprite, layer=3)
        
        
        # Variables principales
        self.point = False
    
    def remove_point(self):
        if not self.sprite == None:
            self.sprite.kill()
        self.kill()




class Cloud(pygame.sprite.Sprite):
    def __init__(
        self, size = (pixel_space_to_scale*4, pixel_space_to_scale*2),  position=(0,0),
        transparency_collide=255, transparency_sprite=255
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide=transparency_collide
        self.transparency_sprite=transparency_sprite
        
        # Seccion de imagen
        image_set = random.choice( [1, 2, 3] )
        
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.surf.fill( (191,191,191, self.transparency_collide) )
        self.rect = self.surf.get_rect(topleft=position)
        
        nocamera_back_sprites.add(self)
        anim_sprites.add(self)
        
        # Sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = get_image(
            f'cloud-{image_set}', size=size, transparency=self.transparency_sprite, return_method='image'
        )
        self.sprite.rect = self.sprite.surf.get_rect( topleft=position )
        nocamera_back_sprites.add(self.sprite)
        
        # Sección de velocidad
        self.speed = random.choice( 
            [-pixel_space_to_scale//4, pixel_space_to_scale//4] 
        )
        self.fps = (data_CF.fps*1.5)//( random.choice( [2, 3, 4] ) )
        self.count_fps = 0
        
    def anim(self):
        self.count_fps += 1
        if self.count_fps == self.fps:
            self.rect.x += self.speed
            self.count_fps = 0

        # Eventos | Si traspasa la pantalla
        if self.rect.x > scale_surface_size[0]+self.rect.width:
            # Si coordenada x es mayor a pantalla mas ancho de nube.
            self.rect.x = -self.rect.width
        elif self.rect.x < -self.rect.width:
            # Si coordenada x es menor a menos ancho de nube.
            self.rect.x = scale_surface_size[0]
        
        self.sprite.rect.x = self.rect.x
        self.sprite.rect.y = self.rect.y




class Sun( pygame.sprite.Sprite ):
    def __init__( 
        self, size=[16, 16], color=generic_colors('yellow'), divider=16, 
        start_with_max_power=True, time=0, display=[1920,1080]
    ):
        super().__init__()
        
        self.time = time
        self.count = 0
        self.divider = divider
        self.step = 0
        
        # Transparencia
        self.transparency_collide = False
        self.transparency_sprite = False
        
        # Colores | Colores a mostrar
        self.color = color # Color actual
        self.list_color = []
        r = stepped_number_sequence( [color[0], color[0]*0.2], divider, True, False, True )
        g = stepped_number_sequence( [color[1], color[1]*0.2], divider, True, False, True )
        b = stepped_number_sequence( [color[2], color[2]*0.2], divider, True, False, True )
        for x in range(divider):
            self.list_color.append( [r[x], g[x], b[x]] )
        
        # Movimiento de posición de la pantalla
        self.move_xy =[0,0]
        self.move_xy[0] = stepped_number_sequence(
            [display[0], 0], divider, most_to_least=False, from_zero=True
        )
        self.move_xy[1] = stepped_number_sequence(
            [display[1]//2, 0], divider, most_to_least=False, from_zero=False
        )
        position = [ self.move_xy[0][0], self.move_xy[1][0] ]
        
        # Superficie y collider
        self.surf = pygame.Surface(size)
        self.surf.fill( self.color ) 
        self.rect = self.surf.get_rect( topleft=position )
        
        # Agergar a grupos de sprites. Iluminación, background.
        anim_sprites.add( self )
        nocamera_back_sprites.add( self )
        lighting_objects.add( self )
    
    def anim(self):
        '''
        Metodo anim, mueve el sol solecito y lo cambia de color 
        Dependiendo su pos en pantalla cambia de color.
        Dependiendo el valor divider
        '''
        self.count += 1
        
        if self.count >= self.time:
            #print(self.step)
            self.count = 0
            
            position = [ self.move_xy[0][self.step], self.move_xy[1][self.step] ]
            self.color = self.list_color[self.step]

            self.rect.topleft = position
            self.surf.fill(self.color)
            
            self.step += 1
            if self.step >= self.divider:
                self.step = 0
    
    def restart(self):
        '''
        Restablece el bucle. Desde el comienzo.
        '''
        self.count = 0

        self.step = 0
        position = [ self.move_xy[0][self.step], self.move_xy[1][self.step] ]
        self.rect.topleft = position

        self.color = self.list_color[self.step]
        self.surf.fill(self.color)





class Bullet( SpriteStandar ):
    def __init__( self, size, position, image, speed_xy, time ):
        # Superficie de collider
        surf = pygame.Surface( size, pygame.SRCALPHA ) 
        surf.fill( [255, 255, 0] )
    
        # Establecer parametros para SpriteStandar
        super().__init__( 
            surf, transparency=255, position=position
        )
        
        self.moving_xy = speed_xy
        self.time = time
        
        # Agregar 
        layer_all_sprites.add( self, layer=3 )
        anim_sprites.add( self )
    
    def anim(self):
        # Mover bala
        self.time_count += 1

        self.movement()
        
        # Colisiones
        kill = False
        for solid_object in solid_objects:
            if self.rect.colliderect(solid_object.rect):
                kill = True
        
        # Eliminar
        if self.time_over() or kill == True:
            Particle( 
                size=[self.rect.height, self.rect.height], 
                position=[self.rect.x -self.moving_xy[0], self.rect.y-self.moving_xy[1]], 
                transparency_collide=255, transparency_sprite=255, 
                color_collide=generic_colors('grey'), time_kill=data_CF.fps*0.5, sound=None
            )
            self.kill()




# Grupos de sprites
layer_all_sprites = pygame.sprite.LayeredUpdates()
nocamera_back_sprites = pygame.sprite.Group()

player_objects = pygame.sprite.Group()
update_objects = pygame.sprite.Group()

solid_objects = pygame.sprite.Group()
ladder_objects = pygame.sprite.Group()
jumping_objects = pygame.sprite.Group()
moving_objects = pygame.sprite.Group()

damage_objects = pygame.sprite.Group()
limit_objects = pygame.sprite.Group()
level_objects = pygame.sprite.Group()
anim_sprites = pygame.sprite.Group()
climate_objects = pygame.sprite.Group()
score_objects = pygame.sprite.Group()
particle_objects = pygame.sprite.Group()

lighting_objects = pygame.sprite.Group()