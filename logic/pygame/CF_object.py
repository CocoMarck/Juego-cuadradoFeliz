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
    
    data_CF
)
from logic.pygame.CF_function import *

import pygame, sys, os, random
from pygame.locals import *




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
air_count_based_on_resolution = round( 1920 / ( data_CF.disp[0] * 0.4) ) #round(data_CF.pixel_space*0.3125) 
if air_count_based_on_resolution < 0:
    air_count_based_on_resolution = 0
elif air_count_based_on_resolution > 5:
    air_count_based_on_resolution = 5
print( round( 1920 / (data_CF.pixel_space*20) ) )

# Basado en las dimenciones del ancho de la resolución maxima, entre el 26% de la resolución de ancho seelccionada.
# Resolución base 1920, resolucion seleccionada llamemosla res_current (res_current*/)
air_count_based_on_resolution = round( 1920 / (data_CF.disp[0]*0.26) )

class Player(pygame.sprite.Sprite):
    def __init__( 
        self, position=[0, 0], size=data_CF.pixel_space, 
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
        
        # Sprite
        size_sprite = [data_CF.pixel_space*2, data_CF.pixel_space*2]
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
        self.pressed_jump       = player_key['jump']
        self.pressed_left       = player_key['left']
        self.pressed_right      = player_key['right']
        self.pressed_up         = player_key['up']
        self.pressed_down       = player_key['down']
        self.pressed_walk       = player_key['walk']
        
        
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
                size=[data_CF.pixel_space//4, data_CF.pixel_space//4], 
                position=[self.rect.x, self.rect.y-1+self.rect.height-data_CF.pixel_space//4], 
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
        if self.move_left == True:  self.moving_xy[0] -= speed
        if self.move_right == True: self.moving_xy[0] += speed
        if self.move_jump == True:
            if fall == False:
                self.jumping = True
                self.move_jump = False
        
        
        
        
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
            self.air_count = 0
        else:
            self.air_count += 1
        
        if self.collision_solid == 'top':
            self.gravity_current = 0
            
            self.jumping = False
            self.jump_count = 0
        
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
        self.size = data_CF.pixel_space
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
            'player_not-move', number=0, size=[data_CF.pixel_space*2, data_CF.pixel_space*2],
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
        self, size=[data_CF.pixel_space//2, data_CF.pixel_space//2], position=[0,0],
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




class Floor(pygame.sprite.Sprite):
    def __init__(
        self, size = [data_CF.pixel_space, data_CF.pixel_space], position = [0,0], 
        transparency_collide=255, transparency_sprite=255, color=None, limit=True, climate=None
    ):
        super().__init__()
        
        # Transparensia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
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
        
        # Collider
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.surf.fill( color )
        self.surf.set_alpha( self.transparency_collide )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add( self, layer=2 )
        solid_objects.add(self)
        
        # Sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = get_image( 'stone', size=size, color=color )
        self.sprite.surf.set_alpha( self.transparency_sprite )
        self.sprite.rect = self.sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add( self.sprite, layer=1 )
        
        # Agregar o no limite
        self.limit_collision( limit )
    
    def limit_collision(self, limit=False):
        # Para agergar un objeto en medio del floor que mate por si traspasa el collider.
        pass




class Ladder(pygame.sprite.Sprite):
    def __init__(self, size=data_CF.pixel_space, position=[0,0],
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
    def __init__(self, size=data_CF.pixel_space, position=[0,0],
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
        self, size=data_CF.pixel_space, position=(0,0),
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




class Spike(pygame.sprite.Sprite):
    def __init__(
        self, size=data_CF.pixel_space, position=[0,0], transparency_collide=255, transparency_sprite=255,
        moving=False, instakill=False
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite
        
        # Collider
        self.surf = pygame.Surface( (size/4, size/2), pygame.SRCALPHA )
        self.surf.fill( generic_colors(color='red', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.x += (size-self.rect.width)//2
        layer_all_sprites.add(self, layer=2)
        
        # Añadir a los grupos de sprites
        # Daño
        if moving == True:
            anim_sprites.add(self)
            
        self.__color = (0, 0, 71)
        if instakill == True:
            self.__color = (71, 0, 0)
            self.damage = 0
        else:
            self.damage = 20
        damage_objects.add(self)
        
        # Sprite
        self.image = get_image( 
            'spike', colored_method='normal', color=self.__color,
            transparency=self.transparency_sprite 
        )
        self.sprite = pygame.sprite.Sprite()
        self.sprite.surf = pygame.transform.scale( self.image, (size, size) )
        self.sprite.rect = self.sprite.surf.get_rect(topleft=position)
        layer_all_sprites.add(self.sprite, layer=1)
        
        # Cuadrados solidos
        square_size = self.rect.height
        floor_x = Floor(
            size = ( square_size, square_size ),
            position = [position[0], position[1]+square_size],
            transparency_collide=self.transparency_collide, transparency_sprite=0,
            limit = False
        )
        
        floor_y = Floor(
            size = ( square_size, square_size ),
            position = [position[0]+square_size, position[1]+square_size],
            transparency_collide=self.transparency_collide, transparency_sprite=0,
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
                self.surf.fill( generic_colors(color='red', transparency=self.transparency_collide) )
                position = (self.rect.x, self.rect.y)
                self.rect = self.surf.get_rect( topleft=position )
                self.rect.y -= self.__move_speed
                
                if not self.sprite == None:
                    self.sprite.surf = pygame.transform.scale(
                        self.image, (self.size, (self.size_y))
                    )
                    self.sprite.rect.y -= self.__move_speed
                
                if self.__move_count >= self.__move_pixels:
                    self.__move_type = 'DOWN'

            elif self.__move_type == 'DOWN':
                self.__move_count -= self.__move_speed//2
                self.size_y -= self.__move_speed//2

                self.surf = pygame.Surface( (self.rect.width, self.size_y), pygame.SRCALPHA )
                self.surf.fill( generic_colors(color='red', transparency=self.transparency_collide) )
                position = (self.rect.x, self.rect.y)
                self.rect = self.surf.get_rect( topleft=position )
                self.rect.y += self.__move_speed//2
                
                if not self.sprite == None:
                    self.sprite.surf = pygame.transform.scale(
                        self.image, (self.size, (self.size_y))
                    )
                    self.sprite.rect.y += self.__move_speed//2
                
                if self.__move_count <= 0:
                    self.__move_type = 'UP'



class Star_pointed(pygame.sprite.Sprite):
    def __init__(
        self, size=data_CF.pixel_space, position=[0,0], transparency_collide=255, transparency_sprite=255,
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
        self, size=data_CF.pixel_space, position=[0, 0], 
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
        self, size=data_CF.pixel_space, position=(data_CF.disp[0]//2, data_CF.disp[1]//2),
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
            disp_width=data_CF.disp[0], disp_height=data_CF.disp[1], obj=self, difference=(self.size*32)
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
        size=[data_CF.pixel_space, data_CF.pixel_space], transparency_collide=255, position = [0, 0]
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
        size = (data_CF.pixel_space, data_CF.pixel_space)

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
        self, size=data_CF.pixel_space, position=[0,0], transparency_collide=255, transparency_sprite=255
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
        self, size = (data_CF.pixel_space*4, data_CF.pixel_space*2),  position=(0,0),
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
            [-data_CF.pixel_space//4, data_CF.pixel_space//4] 
        )
        self.fps = (data_CF.fps*1.5)//( random.choice( [2, 3, 4] ) )
        self.count_fps = 0
        
    def anim(self):
        self.count_fps += 1
        if self.count_fps == self.fps:
            self.rect.x += self.speed
            self.count_fps = 0

        # Eventos | Si traspasa la pantalla
        if self.rect.x > data_CF.disp[0]+self.rect.width:
            # Si coordenada x es mayor a pantalla mas ancho de nube.
            self.rect.x = -self.rect.width
        elif self.rect.x < -self.rect.width:
            # Si coordenada x es menor a menos ancho de nube.
            self.rect.x = data_CF.disp[0]
        
        self.sprite.rect.x = self.rect.x
        self.sprite.rect.y = self.rect.y


# Grupos de sprites
layer_all_sprites = pygame.sprite.LayeredUpdates()
nocamera_back_sprites = pygame.sprite.Group()

player_objects = pygame.sprite.Group()

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