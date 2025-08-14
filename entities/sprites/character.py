# General
from core.pygame.pygame_util import generic_colors

import pygame, random
from pygame.locals import *

# CF
from controllers.cf_info import (
    data_CF, scale_surface_size, pixel_space_to_scale
)
from core.pygame.cf_util import *

from .cf_sounds import *
from .general_use.standard_sprite import StandardSprite
from .general_use.sprite_layer_pasted_rect import SpriteLayerPastedRect
from .bullet import Bullet
from .particle import Particle
from .anim_dead_character import AnimDeadCharacter




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




class Character( StandardSprite ):
    '''
    Objeto Personaje, para Player, y para NPC.
    '''
    def __init__(
     self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255, 
     dict_sprite={
        'side-x' : pygame.Surface( [pixel_space_to_scale,pixel_space_to_scale] ),
        'side-y' : pygame.Surface( [pixel_space_to_scale,pixel_space_to_scale] )
     }, position=[0,0], limit_xy=[0,0], color_sprite=[153,252,152], sprite_difference_xy=[0,0],
     solid_objects=None, damage_objects=None, level_objects=None, score_objects=None, jumping_objects=None,
     moving_objects=None, ladder_objects=None, particle_objects=None, anim_sprites=None,
     update_objects=None, layer_all_sprites=None
    ):
        # grupos
        self.__damage_objects=damage_objects
        self.__solid_objects=solid_objects
        self.__level_objects=level_objects
        self.__score_objects=score_objects
        self.__jumping_objects=jumping_objects
        self.__moving_objects=moving_objects
        self.__ladder_objects=ladder_objects
        self.__particle_objects=particle_objects
        self.__anim_sprites=anim_sprites
        
        self.__update_objects = update_objects
        self.__layer_all_sprites = layer_all_sprites
        
        # Parametros para Sprite Standar
        surf = pygame.Surface( [size*0.5,size] )
        surf.fill( [0,0,0] )
        
        # Establecer parametros
        super().__init__( 
            surf, transparency=transparency_collide, position=position
        )
        self.rect.x += size*0.25
        
        # Transparencia
        #self.transparency
        self.color_sprite = color_sprite
        
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
        self.with_gun = True
        
        self.can_shot = True
        self.count_shot = 0
        self.time_to_shot = data_CF.fps*0.25
        
        # Capas | Sprites | Apariencia de player
        self.sprite_layer = SpriteLayerPastedRect(
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
        self.initial_hp = 100
        self.hp = self.initial_hp
        self.dead = False
        self.anim_dead_count = 0
        self.anim_dead = None
        self.anim_fin = False
        
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

        for obj in self.__damage_objects:
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
            for level in self.__level_objects:
                if self.rect.colliderect(level.rect):
                    level.change_level = True
                    self.hp = self.initial_hp
                    self.rect.topleft = (level.rect.x+(self.rect.width//2), level.rect.y)
                    self.moving_xy = [0,0]
                

        # Colision | Objetos | Score-Monedas
        for score in self.__score_objects:
            if self.rect.colliderect(score.rect):
                self.score += 1
                self.collision_score = True
                if (
                    self.hp < self.initial_hp and
                    (self.dead == False)
                ):
                    self.hp += 10
                score.remove_point()
                
        
        # Colision | Trampoline
        for obj in self.__jumping_objects:
            if self.rect.colliderect(obj.rect):
                #if self.moving_xy[1] > 0:
                #    self.rect.bottom = obj.rect.top - obj.rect.height
                #    self.gravity_current = 0
                self.air_count=0
                self.jumping=True
                self.set_and_jump(multipler=2)
        

        # Colision | Solidos | Escalera
        if pygame.sprite.spritecollide(self, self.__ladder_objects, False):
            if self.down == False:
                self.gravity_current = 0
                self.air_count = 0
                
        # Colision | Solidos | Elevador
        for obj in self.__moving_objects:
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

                if pygame.sprite.spritecollide(self, self.__solid_objects, False):
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
        self.sprite_layer.layer[1].set_transparency()
    
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
                color_collide=generic_colors('grey'), time_kill=data_CF.fps, sound=None,
                particle_objects=self.__particle_objects, solid_objects=self.__solid_objects,
                damage_objects=self.__damage_objects, jumping_objects=self.__jumping_objects,
                anim_sprites=self.__anim_sprites, layer_all_sprites=self.__layer_all_sprites
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
        # Establecer arma
        if self.with_gun:
            # Speed
            speed_xy = speed2d_with_angle( self.rect.height*2, self.sprite_layer.layer[1].angle )
        
            # Arma Gun | Disparo
            if self.action and self.can_shot:
                bullet = Bullet(
                 size=[self.rect.height*2, self.rect.height//4], position=self.rect.topleft, image=None,
                 speed_xy=speed_xy, time=data_CF.fps*2,
                 particle_objects=self.__particle_objects, solid_objects=self.__solid_objects,
                 damage_objects=self.__damage_objects, jumping_objects=self.__jumping_objects, 
                 anim_sprites=self.__anim_sprites, layer_all_sprites=self.__layer_all_sprites,
                 particle_size=[self.rect.height//4, self.rect.height//4], damage=20
                )
                #bullet.angle = self.sprite_layer.layer[1].angle
                #bullet.rotate()
                '''
                bullet.rect.y += self.rect.width*0.75
                if self.side_positive:
                    bullet.rect.x += self.rect.width
                else:
                    bullet.rect.x -= bullet.rect.width
                if self.left:
                    bullet.rect.x -= self.speed
                if self.right:
                    bullet.rect.x += self.speed
                '''
                bullet.angle = self.sprite_layer.layer[1].angle
                bullet.rotate()
                bullet.rect.center = self.rect.center
                

                self.can_shot = False
                random.choice(sounds_shot).play()

            # Limitar generacion de balasos
            if self.can_shot == False:
                self.count_shot += 1
                if self.count_shot >= self.time_to_shot:
                    self.count_shot = 0
                    self.can_shot = True

            # Reiniciar estado de disparo
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
        
        # Cambiar dirección del arma
        if self.left:  
            self.sprite_layer.layer[1].angle = -180
        if self.right: 
            self.sprite_layer.layer[1].angle = 0
            
        # Arma Gun | Rotar Sprite gun
        self.sprite_layer.layer[1].rotate()

        # Para que no se vea si es que no se tiene arma
        if self.dead == False:
            self.sprite_layer.layer[1].not_see = not self.with_gun
            self.sprite_layer.layer[1].set_transparency()
    
    
    def update(self, old_gravity=False, old_jump=True):
        '''
        Actualizar eventos del jugador. Moverse y todo eso.
        '''
        # Moverse
        if self.dead == False:
            self.move()
        
        # HP | Determinar si el jugador esta vivo o muerto
        if self.hp <= 0:
            self.dead = True
            self.not_move = True
            self.jump_count = self.jump_max_height
            self.gravity_current = 0
            self.sprite_layer.layer[0].not_see=True
            self.sprite_layer.layer[1].not_see=True
        else:
            self.sprite_layer.layer[0].not_see=False
            self.sprite_layer.layer[1].not_see=False
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
        
        # Animacion de kill
        if self.dead:
            # Si el contador de animaaciones de kill esta en cero.
            if self.anim_dead_count <= 0:
                self.anim_dead_count += 1
                self.anim_dead = AnimDeadCharacter(
                 position=[ self.rect.x -self.rect.width//2, self.rect.y ], 
                 transparency_collide=self.transparency, 
                 transparency_sprite=self.sprite_layer.transparency_layer, color_sprite=self.color_sprite,
                 particle_objects=self.__particle_objects, solid_objects=self.__solid_objects, 
                 damage_objects=self.__damage_objects, jumping_objects=self.__jumping_objects,
                 anim_sprites=self.__anim_sprites, layer_all_sprites=self.__layer_all_sprites
                )
                ( random.choice(sounds_dead) ).play()
        else:
            self.anim_dead_count = 0
        
        if not (self.anim_dead == None):
            if self.anim_dead.anim_fin:
                self.anim_fin = True
                self.anim_dead = None
        else:
            self.anim_fin = False
                
            
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
            self.side_positive = False
        if self.right == True: 
            self.moving_xy[0] += speed
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
        self.collision_solid = collide_and_move(
         obj=self, obj_movement=self.moving_xy, solid_objects=self.__solid_objects
        )
        
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
        self.collision_solid = collide_and_move(
         obj=self, obj_movement=self.moving_xy, solid_objects=self.__solid_objects
        )
        
        if self.collision_solid == 'bottom':
            self.gravity_current = 0
            #self.air_count = 0
        else:
            pass#self.air_count += 1
        
        if self.collision_solid == 'top':
            self.gravity_current = 0
            
            self.jumping = False
            self.jump_count = 0
            
        # Anim
        self.anim_all(fall=self.fall, speed_multipler=speed_multipler)
        
       # Arma Gun | Disparos
        self.gun_event()
        
        # Sound
        self.sound()
