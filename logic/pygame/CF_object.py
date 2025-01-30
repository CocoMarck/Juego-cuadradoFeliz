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
class Player(pygame.sprite.Sprite):
    def __init__(
        self, position=(data_CF.disp[0]//2,data_CF.disp[1]//2), show_collide=False,
        show_sprite=True, color_sprite=(153, 252, 152)
    ):
        super().__init__()

        # Mostrar o no collider
        self.surf = pygame.Surface( (data_CF.pixel_space//2, data_CF.pixel_space), pygame.SRCALPHA )
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
        self.surf.fill( generic_colors(color='green', transparency=self.transparency) )
        
        # Collider y posición
        self.rect = self.surf.get_rect(
            center=position
        )
        layer_all_sprites.add(self, layer=3)
        player_objects.add(self)
        
        # Movimeinto
        # Jump power, establece velocidad y alura de salto.
        # speed, establece velocidad izquierda/derecha, y rebote en paredes.
        self.gravity            = True
        self.gravity_power      = self.rect.height//4

        self.jump_power         = self.rect.height//2
        self.jumping            = False
        self.jump_max_height    = self.jump_power*8
        self.__current_max_height   = self.jump_max_height
        self.__jump_count           = 0

        self.speed_multipler    = 1
        self.speed_run          = self.rect.height//2
        self.speed              = self.rect.height//2
        self.not_move           = False
        self.x_move_type        = None
        self.move_down          = None
        
        # Vida
        self.hp = 100
        
        # Teclas de movimiento
        self.pressed_jump       = pygame.K_SPACE
        self.pressed_left       = pygame.K_LEFT
        self.pressed_right      = pygame.K_RIGHT
        self.pressed_down       = pygame.K_DOWN
        self.pressed_walk       = pygame.K_LSHIFT
        
        # Mostrar o no sprite
        self.show_sprite = show_sprite
        self.sprite = None
        
        # Sprite / Imagenes de sprite
        # Sprite / Cambiar color al de imagenes de sprite    
        # Sprite / Dividir fotogramas de los sprites animados        
        self.sprite_notmove = get_image(
            'player_not-move', size=[data_CF.pixel_space*2, data_CF.pixel_space*2], color=color_sprite,
            colored_method='surface'
        )
        self.sprite_move = get_image(
            'player_move', size=[data_CF.pixel_space*2, data_CF.pixel_space*2], color=color_sprite,
            colored_method='surface'
        )

        self.sprite_move_invert = get_image(
            'player_move', size=[data_CF.pixel_space*2, data_CF.pixel_space*2], color=color_sprite,
            flip_x=True, colored_method='surface'
        )
        self.count_fps = 0
        self.count_fps_invert = len(self.sprite_move_invert)
        
        # FPS | Variables del valor de Milisegundos
        #self.__decressed_fps_type1 = data_CF.fps//3.75
        self.__decressed_fps_type2 = round(data_CF.fps*0.1)#0.125)
        
        # Sonido
        self.__step_count = 0
        self.__sound_step_number = 5
        self.sound_step = 'wait'
        
        # Plataformas movibles
        self.__moving_fps_count = 0
    
    
    def move(self):
        # Sección sprite
        self.x_move_type = None
        self.move_down   = False
    
        # Teclas de movimiento
        pressed_keys = pygame.key.get_pressed()
        pressed_left = pressed_keys[self.pressed_left]
        pressed_right = pressed_keys[self.pressed_right]
        pressed_down = pressed_keys[self.pressed_down]
        pressed_walk = pressed_keys[self.pressed_walk]
        
        # Iniciar o no el movimiento
        # Si el not_move esta en false, entonces puede seguir.
        # Si se pide unicamente una dirección (derecha/izquierda), puedes eguir
        self.moving = False
        if (
            self.not_move == False and
            not (pressed_left == True and pressed_right == True)
        ):
            if pressed_left:
                self.moving = True
                self.rect.x -= self.speed
                if self.jumping == False and self.gravity == False:
                    self.x_move_type = 'left-anim'
                elif self.jumping == True:
                    self.x_move_type = 'left-jump'
                else:
                    self.x_move_type = 'left-fall'
    
            if pressed_right:
                self.moving = True
                self.rect.x += self.speed
                if self.jumping == False and self.gravity == False:
                    self.x_move_type = 'right-anim'
                elif self.jumping == True:
                    self.x_move_type = 'right-jump'
                else:
                    self.x_move_type = 'right-fall'
            
            if pressed_down:
                self.move_down = True
            
            if pressed_walk:
                self.speed_multipler = 0.5
            else:
                self.speed_multipler = 1
            self.speed = self.speed_run * self.speed_multipler
    
    def jump(self, multipler=1):
        if self.gravity == False and self.not_move == False:
            self.jumping = True

            self.__current_max_height = self.jump_max_height*multipler
    
    def update(self):    
        # Mostrar o no el sprite
        if self.sprite == None:
            if self.show_sprite == True:
                self.sprite = pygame.sprite.Sprite()
                self.sprite.surf = self.sprite_notmove[0]
                self.sprite.rect = self.sprite.surf.get_rect()
                layer_all_sprites.add(self.sprite, layer=2)
        else:
            if self.show_sprite == False:
                self.sprite.kill()
                self.sprite = None
        
        # Verificar si el jugador este muerto o no
        dead = False
        if self.hp <= 0:
            dead = True

        # Variables | Colisiones
        collide = False
        damage = False
        instakill = False
        
        # Colision | Objetos | Solidos-Plataforma / Piso / Floor
        self.not_move = False
        for solid_object in solid_objects:
            # Acomodar coliders, dependiendo de la dirección de colisión:
            # arriba, abajo, izquierda, o derecha
            collision = obj_collision_sides_solid(obj_main=self, obj_collide=solid_object)
            if not collision == None:
                #print(collision)
                collide = True
            
        # Colision | Objetos | Solidos-Escalera
        if pygame.sprite.spritecollide(self, ladder_objects, False):
            # Si el jugador no se mueve hacia abajo
            if self.move_down == False:
                collide = True
                
        # Colision | Objetos | Solidos-Trampolin
        if pygame.sprite.spritecollide(self, jumping_objects, False):
            collide = True
            self.jump(multipler=2)
            self.rect.y -= 1 # Esto es para evitar bugs de colision.
            
        # Colision | Objetos | Solidos-Elevador
        for obj in moving_objects:
            if self.rect.colliderect(obj.rect):
                if self.rect.y < obj.rect.y:
                    #if self.move_down == False:
                        collide = True
                elif self.rect.y > obj.rect.y:
                    self.jump()
                    #self.rect.y += self.gravity_power

                if dead == False:
                    if obj.move_dimension == 1:
                        if obj.move_positive == True:
                            self.rect.x += obj.speed
                        else:
                            self.rect.x -= obj.speed
                    elif obj.move_dimension == 2:
                        if obj.move_positive == True:
                            self.rect.y += obj.speed
                        else:
                            self.rect.y -= obj.speed
                    
                    self.__moving_fps_count += 1
                    if self.__moving_fps_count == self.__decressed_fps_type2:
                        self.__moving_fps_count = 0
                        self.moving = True
        
        # Colision | Objetos | Daño
        damage_number = 0
        for obj in damage_objects:
            if self.rect.colliderect(obj.rect):
                damage = True                

                if obj.damage <= 0:
                    instakill = True
                else:
                    damage_number = obj.damage
            
        # Colision | Pantalla | Daño
        if (
            self.rect.y >= data_CF.disp[1] or   self.rect.y <= 0 or
            self.rect.x >= data_CF.disp[0] or    self.rect.x <= 0
        ):
            instakill = True
        
        # Si esta el instakill es True, es porque hay daño
        # Boleanos daño y instakill
        if instakill == True:
            damage = True
        
        # Colision | Objetos | Cambio de nivel
        for level in level_objects:
            if self.rect.colliderect(level.rect):
                level.change_level = True
                self.hp = 100
                self.rect.topleft = (level.rect.x+(self.rect.width//2), level.rect.y)
                # hp al 100, para si o si que el player este vivo


        # Colision | Objetos | Score-Monedas
        for score in score_objects:
            if self.rect.colliderect(score.rect):
                score.point = True
                ( random.choice(sounds_score) ).play()
                if (
                    self.hp < 100 and
                    (dead == False)
                ):
                    self.hp += 10


        # Eventos al colisionar con solidos
        if collide == True:
            self.gravity = False
            self.surf.fill( generic_colors('red', transparency=self.transparency) )
            
            if self.sound_step == 'wait':
                self.sound_step = 'yes'
            elif self.sound_step == 'yes':
                self.sound_step = 'no'

        else:
            self.gravity = True
            self.sound_step = 'wait'

        # Eventos al morir y al recibir Daño
        # Colider de daño
        if dead == True:
            # El player se murio
            # Establecer al player al spawn
            self.not_move = True
            self.gravity = False
            self.jumping = False
        else:
            if damage == True:
                # Erectos de daño
                self.not_move = True
                self.gravity = False
                self.jumping = False
                self.rect.x += random.choice( [-(self.speed), (self.speed)] )
                self.rect.y += random.choice( [-self.gravity_power, self.gravity_power] )

                # Eventos principales
                self.hp -= damage_number

                if instakill == True:
                    self.hp = -1
        
        # Gravedad y salto | Sprites player not_move
        if (
            self.gravity == True and
            self.jumping == False
        ):
            # Gravedad
            self.surf.fill( generic_colors('sky_blue', transparency=self.transparency) )

            self.rect.y += self.gravity_power
            
            # Sección sprite y
            if self.show_sprite == True and (not self.sprite == None):
                self.sprite.surf = self.sprite_notmove[2]
        else:
            # Salto
            if self.jumping == True:
                self.surf.fill( generic_colors('blue', transparency=self.transparency) )

                if not self.__jump_count >= (self.__current_max_height):
                    self.rect.y -= self.jump_power
                    self.__jump_count += self.jump_power
                else:
                    self.jumping = False
                    
                # Sección sprite y
                if self.show_sprite == True and (not self.sprite == None):
                    self.sprite.surf = self.sprite_notmove[1]

            else:
                self.__jump_count = 0
                self.surf.fill( generic_colors('green', transparency=self.transparency) )
                
                # Sección sprite y
                if self.show_sprite == True and (not self.sprite == None):
                    self.sprite.surf = self.sprite_notmove[0]

        # Sin gravedad
        self.rect.y += 0
    
        # Sección de movimiento x | Sprites player moving
        if (
            self.x_move_type == 'right-anim' or self.x_move_type == 'left-anim'
        ):
            self.surf.fill( generic_colors('yellow', transparency=self.transparency) )
            self.__step_count += 1*self.speed_multipler
            if int(self.__step_count) == self.__sound_step_number:
                ( random.choice(sounds_step) ).play()
                self.__step_count = 0
        elif (
            self.x_move_type == 'right-jump' or self.x_move_type == 'left-jump'
        ):
            self.surf.fill( (127, 0, 255, self.transparency) )
        elif (
            self.x_move_type == 'right-fall' or self.x_move_type == 'left-fall'
        ):
            self.surf.fill( (0, 127, 255, self.transparency) )
        else:
            #if self.x_move_type == None:
            self.__step_count = 0

        # Scción sprite movimiento x
        if self.show_sprite == True and (not self.sprite == None):
            if self.x_move_type == 'right-anim':
                self.count_fps = (self.count_fps +(1*self.speed_multipler)) % len(self.sprite_move)
                self.sprite.surf = self.sprite_move[int(self.count_fps)]

            elif self.x_move_type == 'right-jump':
                self.sprite.surf = self.sprite_move[1]
            elif self.x_move_type == 'right-fall':
                self.sprite.surf = self.sprite_move[6]
                
            elif self.x_move_type == 'left-anim':
                self.count_fps_invert = (
                    (self.count_fps_invert -(1*self.speed_multipler) ) % len(self.sprite_move_invert)
                )
                self.sprite.surf = self.sprite_move_invert[int(self.count_fps_invert)]

            elif self.x_move_type == 'left-jump':
                self.sprite.surf = self.sprite_move_invert[6]
            elif self.x_move_type == 'left-fall':
                self.sprite.surf = self.sprite_move_invert[1]
        

        # Actualizar posición de sprite
        if not self.sprite == None:
            self.sprite.rect.x = self.rect.x -(self.rect.width+(self.rect.width//2))
            self.sprite.rect.y = self.rect.y -self.rect.height
            
        # Audio | Reproducción
        if self.sound_step == 'yes':
            # Cuando tocas el suelo de objetos solidos
            ( random.choice(sounds_step) ).play()

        if self.not_move == True and self.hp >= 1:
            if damage == False:
                # Cuando te pegas con algun objeto solido.
                if not self.sound_step == 'yes':
                    ( random.choice(sounds_step) ).play()
            else:
                # Cuando te pegas con algun objeto dañino
                ( random.choice(sounds_hit) ).play()

        if (
            self.__jump_count == self.jump_power and self.jumping == True
        ):
            # Salto
            sound_jump.play()


class Anim_player_dead(pygame.sprite.Sprite):
    def __init__(self, position=(0,0), fps=data_CF.fps, show_collide=False, color_sprite=(153, 252, 152) ):
        super().__init__()
        
        if show_collide == True:
            self.transparent = 255
            list_sprites = [None, None, None, None]
        else:
            self.transparent = 0
            list_sprites = [3, 4, 1, 2]

        # Principal
        self.size = data_CF.pixel_space
        self.surf = pygame.Surface( (self.size, self.size), pygame.SRCALPHA )
        self.rect = self.surf.get_rect( center=position )
    
        self.fps = data_CF.fps*3
        self.__count = 0
        self.anim_fin = False
        anim_sprites.add( self )
        layer_all_sprites.add(self, layer=2)
        
        # Partes
        size_parts = self.size//2
        self.part1 = Player_part( 
            size=size_parts,
            position=(self.rect.x+size_parts//2, self.rect.y + (size_parts+size_parts//2) ),
            color=generic_colors('green', self.transparent), sprite=list_sprites[0],
            color_sprite=color_sprite
        )
        
        self.part2 = Player_part( 
            size=size_parts,
            position=(self.rect.x+(size_parts+size_parts//2), self.rect.y + (size_parts+size_parts//2) ),
            color=generic_colors('blue', self.transparent), sprite=list_sprites[1],
            color_sprite=color_sprite
        )
        
        self.part3 = Player_part( 
            size=size_parts,
            position=(self.rect.x+size_parts//2, self.rect.y+size_parts//2),
            color=generic_colors('yellow', self.transparent), sprite=list_sprites[2],
            color_sprite=color_sprite
        )

        self.part4 = Player_part( 
            size=size_parts,
            position=(self.rect.x+(size_parts+size_parts//2), self.rect.y+size_parts//2),
            color=generic_colors('sky_blue', self.transparent), sprite=list_sprites[3],
            color_sprite=color_sprite
        )
    
    def anim(self):
        # Partes
        self.part1.update()
        self.part2.update()
        self.part3.update()
        self.part4.update()

        # Contador
        self.__count += 1
        if self.__count*5 <= 128:
            self.surf.fill( ( 255-(self.__count*5), 0, 0, self.transparent)  )

        if self.__count == self.fps:
            # Animacion terminada, todos los objetos se eliminaran
            self.anim_fin = True
            self.part1.kill()
            self.part2.kill()
            self.part3.kill()
            self.part4.kill()
            self.kill()




class Player_part(pygame.sprite.Sprite):
    def __init__(
        self, size=data_CF.pixel_space//2, color=generic_colors('green'), position=(0,0), 
        sprite=None, color_sprite=None
    ):
        super().__init__()
        
        # Collider y sprite
        self.size = size
        if not sprite == None:
            # Sprite / Imagen y cambiar su color
            # Sprite / Dividir el sprite y establecer su parte indicada
            img = get_image( 
                'player_not-move', number=0, size=[data_CF.pixel_space*2, data_CF.pixel_space*2],
                colored_method='surface', color=color_sprite
            )
            img = Split_sprite(sprite_sheet=img, parts=8)
            if sprite == 1:
                self.surf = img[9]
            elif sprite == 2:
                self.surf = img[10]
            elif sprite == 3:
                self.surf = img[13]
            elif sprite == 4:
                self.surf = img[14]
        else:
            self.surf = pygame.Surface( (self.size, self.size), pygame.SRCALPHA )
            self.surf.fill( color )

        self.rect = self.surf.get_rect( 
            center=position
        )
        layer_all_sprites.add(self, layer=2)
        player_objects.add(self)
        
        # Movimiento
        if random.randint(0, 1) == 1:
            self.move_positive_x = True
        else:
            self.move_positive_x = False

        if random.randint(0, 1) == 1:
            self.jumping = False
        else:
            self.jumping = True
        self.move_positive_y = False
        self.__jump_number = 0
        self.speedxy = random.randint(size//4, size//2)
    
    def update(self):
        self.gravity = True
        
        # Colisiones
        for solid_object in solid_objects:
            collide = obj_collision_sides_rebound(
                obj_main=self, obj_collide=solid_object
            )
            if not collide == None:
                self.gravity = False
        
        for damage_object in damage_objects:
            collide = obj_collision_sides_rebound(
                obj_main=self, obj_collide=damage_object
            )
            if not collide == None:
                self.gravity = False
                ( random.choice(sounds_hit) ).play()
        
        # Gravedad / Salto / Movimiento y
        if self.gravity == True:
            self.move_positive_y = True
            
        if self.jumping == True:
            self.move_positive_y = False
        else:
            self.move_positive_y = True
        
        if self.move_positive_y == True:
            self.rect.y += self.speedxy
        else:
            self.__jump_number += self.speedxy
            self.rect.y -= self.speedxy
            self.jumping = True
            if self.__jump_number >= self.speedxy*8:
                self.__jump_number = 0
                self.jumping = False
        
        # Movimiento x
        if self.move_positive_x == True:
            self.rect.x += self.speedxy
        else:
            self.rect.x -= self.speedxy




class Floor(pygame.sprite.Sprite):
    def __init__(
        self,
        size = (data_CF.pixel_space, data_CF.pixel_space),
        position = (data_CF.disp[0]//2, (data_CF.disp[1]-8)),
        color='grey', show_collide=False, show_sprite=True,
        limit = True, climate=None
    ):
        super().__init__()
        
        # Sprite
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
            
        if show_sprite == True:
            self.surf = get_image('stone', size=size)
            
            # Coloriar sprite
            # Solo si hay sprite y el clima no esta en None
            if (
                not climate == None
            ):
                color = None
                random_more_color = random.choice( [8, 16, 32] )

                if climate == 'alien':
                    color = (0,random_more_color,random_more_color)#'sky_blue'

                elif climate == 'sunny':
                    color = (random_more_color,0,0)#'red'

                elif climate == 'rain':
                    color = (0,0,random_more_color)#'blue'

                elif climate == 'black':
                    color = (
                        (random_more_color//2),
                        random_more_color,
                        0
                    )#'Verde amarillento'
                
                if not color == None:
                    self.surf.fill( color, special_flags=pygame.BLEND_RGB_ADD)
            
        else:
            self.surf = pygame.Surface( size, pygame.SRCALPHA )
            self.surf.fill( generic_colors(color=color, transparency=self.transparency) )
        
        # Collider y posición
        self.rect = self.surf.get_rect( 
            center = position
        )
        self.add_limit = limit
        layer_all_sprites.add(self, layer=1)
        solid_objects.add(self)
        
        # Variables Colorear
        self.size = size
        
    
    def limit_collision(self):
        if self.add_limit == True:
            # Limite de colision, si toca este limite, el jugador muere.
            # Funcional, pero no tan bien
            limit = pygame.sprite.Sprite()
            limit_xy = [
                round(self.rect.width*0.75, 4), round(self.rect.height*0.75, 4)
            ]
            limit.surf = pygame.Surface( (limit_xy[0], limit_xy[1]), pygame.SRCALPHA )
            limit.surf.fill( (191, 127, 127, self.transparency) )
            limit.rect = limit.surf.get_rect(
                topleft=(
                    self.rect.x,
                    self.rect.y
                )
            )
            limit.rect.x += (self.rect.width-limit.rect.width) //2
            limit.rect.y += (self.rect.height-limit.rect.height) //2
            layer_all_sprites.add(limit, layer=2)
            #limit.damage = 10
            #damage_objects.add(limit)
            #print(self.rect.width)
            #print(self.rect.height)
            #print(limit_xy)
            #print(self.rect.x+(self.rect.width -limit_xy[0]))
            #print(self.rect.y+(self.rect.height -limit_xy[1]))




class Ladder(pygame.sprite.Sprite):
    def __init__(self, size=data_CF.pixel_space, position=(0,0), show_collide=False, show_sprite=True):
        super().__init__()
        
        # Collider y surface
        transparency = 0
        if show_collide == True:
            transparency = 255
        
        size_collide = round(size*0.75)
        self.surf = pygame.Surface( (size_collide, size_collide), pygame.SRCALPHA )
        self.surf.fill( (113,77,41, transparency) )
        
        self.rect = self.surf.get_rect( center=position )
        
        layer_all_sprites.add(self, layer=2)
        ladder_objects.add(self)
        
        # Sprite
        if show_sprite == True:
            sprite = pygame.sprite.Sprite()
            sprite.surf = get_image('ladder', size=[size, size])
            sprite.rect = sprite.surf.get_rect( center=position )
            layer_all_sprites.add(sprite, layer=1)



class Trampoline(pygame.sprite.Sprite):
    def __init__(self, size=data_CF.pixel_space, position=(0,0), show_collide=False, show_sprite=True):
        super().__init__()
        
        # Collide
        transparency = 0
        if show_collide == True:
            transparency = 255
        
        self.surf = pygame.Surface( (size, size//8), pygame.SRCALPHA )
        self.surf.fill( generic_colors('sky_blue', transparency=transparency) )
        self.rect = self.surf.get_rect( center=position )
        self.rect.y -= size//4
        
        layer_all_sprites.add(self, layer=2)
        jumping_objects.add(self)
        
        # Sprite
        if show_sprite == True:
            sprite = pygame.sprite.Sprite()
            sprite.surf = get_image( 'trampoline', size=(size, size) )
            sprite.rect = sprite.surf.get_rect( center=position )
            layer_all_sprites.add( sprite, layer=1 )




class Elevator(pygame.sprite.Sprite):
    def __init__(
        self, size=data_CF.pixel_space, position=(0,0),
        show_collide=False, show_sprite=True, move_dimension=1
    ):
        super().__init__()
        
        # Collider
        transparency = 0
        if show_collide == True:
            transparency = 255

        size_ready = (size*2, size)
        self.surf = pygame.Surface( size_ready, pygame.SRCALPHA)
        self.surf.fill( generic_colors('grey', transparency=transparency) )
        self.rect = self.surf.get_rect( center=position )
        self.rect.x += size//2
        layer_all_sprites.add(self, layer=2)
        moving_objects.add(self)
        anim_sprites.add(self)
        
        # Sprite
        if show_sprite == True:
            self.sprite = pygame.sprite.Sprite()
            self.sprite.surf = get_image('elevator', size=size_ready)
            self.sprite.rect = self.sprite.surf.get_rect( topleft=(self.rect.x, self.rect.y) )
            layer_all_sprites.add(self.sprite, layer=1)
        else:
            self.sprite = None
        
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
        if not self.sprite == None:
            self.sprite.rect.x = self.rect.x
            self.sprite.rect.y = self.rect.y




class Spike(pygame.sprite.Sprite):
    def __init__(
        self, size=data_CF.pixel_space, position=(0,0), show_collide=False, show_sprite=True,
        moving=False, instakill=False
    ):
        super().__init__()
        
        # Collider
        self.surf = pygame.Surface( (size/4, size/2), pygame.SRCALPHA )
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0

        self.surf.fill( generic_colors(color='red', transparency=self.transparency) )

        # Collider pico
        self.rect = self.surf.get_rect(
            center=position
        )
        self.rect.y -= self.rect.height//2
        
        # Añadir a los grupos de sprites
        # Daño
        layer_all_sprites.add(self, layer=2)
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
        self.image = get_image( 'spike' )
        if show_sprite == True:
            self.sprite = pygame.sprite.Sprite()
            self.sprite.surf = pygame.transform.scale(
                self.image, (size, size)
            )
            self.sprite.rect = self.sprite.surf.get_rect(center=position)
            layer_all_sprites.add(self.sprite, layer=1)
            self.sprite.surf.fill( self.__color, special_flags=pygame.BLEND_ADD )
        else:
            self.sprite = None
        
        # Cuadrados solidos
        square_size = self.rect.height
        floor_x = Floor(
            size = ( square_size, square_size ),
            position = position,
            show_collide = show_collide,
            show_sprite = False,
            limit = False
        )
        floor_x.rect.x -= square_size//2
        floor_x.rect.y += square_size//2
        
        floor_y = Floor(
            size = ( square_size, square_size ),
            position = position,
            show_collide = show_collide,
            show_sprite = False,
            limit = False
        )
        floor_y.rect.x += square_size//2
        floor_y.rect.y += square_size//2
        
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
                
                if not self.sprite == None:
                    self.sprite.surf = pygame.transform.scale(
                        self.image, (self.size, (self.size_y))
                    )
                    self.sprite.surf.fill( self.__color, special_flags=pygame.BLEND_ADD )
                    self.sprite.rect.y -= self.__move_speed
                
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
                
                if not self.sprite == None:
                    self.sprite.surf = pygame.transform.scale(
                        self.image, (self.size, (self.size_y))
                    )
                    self.sprite.surf.fill( self.__color, special_flags=pygame.BLEND_ADD )
                    self.sprite.rect.y += self.__move_speed//2
                
                if self.__move_count <= 0:
                    self.__move_type = 'UP'



class Star_pointed(pygame.sprite.Sprite):
    def __init__(
        self, size=data_CF.pixel_space, position=(0,0), show_collide=False, show_sprite=True,
        moving=False, instakill=False
    ):
        super().__init__()
        
        # Movimiento variables
        self.moving = moving
        self.instakill = instakill
        self.count_moving = 0
        self.moving_pixels = size*4
        self.moving_speed = size//4
        
        # Mostrar o no collider
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
        
        # Collider principal
        self.surf = pygame.Surface( ( size/2, size/2 ), pygame.SRCALPHA )
        self.surf.fill( generic_colors('green', self.transparency) )
        self.rect = self.surf.get_rect( center=position )
        
        layer_all_sprites.add(self, layer=2)
        anim_sprites.add(self)
        
        # Mostrar o no sprite
        self.show_sprite = show_sprite
        self.__size = size
        if self.show_sprite == True:
            if self.instakill == True:
                color = [95, 0, 0]
            else:
                color = [0, 0, 127]

            self.sprite = Anim_sprite(
                sprite_sheet=get_image(
                    'star-pointed', size=[self.__size*7, self.__size], return_method='image', color=color
                )
            )
            self.sprite.rect.topleft = (
                self.rect.x-(self.__size//4),
                self.rect.y-(self.__size//4)
            )
            layer_all_sprites.add(self.sprite, layer=1)
        else:
            self.sprite = None
        
        # Cuadrados dañinos
        size_square = self.rect.width/2
        
        self.square_x1 = self.square_damage(
            size=size_square, position=(self.rect.x, self.rect.y +(size_square//2) ),
            color=generic_colors('black', self.transparency)
        )
        self.square_x2 = self.square_damage(
            size=size_square, position=(
                self.rect.x-size_square, self.rect.y +(size_square//2) 
            ),
            color=generic_colors('red', self.transparency)
        )
        self.square_x3 = self.square_damage(
            size=size_square, position=(self.rect.x+size_square, self.rect.y +(size_square//2) ),
            color=generic_colors('grey', self.transparency)
        )
        self.square_x4 = self.square_damage(
            size=size_square, position=(self.rect.x+(size_square*2), self.rect.y +(size_square//2) ),
            color=generic_colors('blue', self.transparency)
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
        if self.show_sprite == True:
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

                if self.show_sprite == True:
                    self.sprite.rect.x += self.moving_speed
            elif self.count_moving >= self.moving_pixels:
                if self.count_moving < self.moving_pixels*1.5:
                    self.count_moving += self.moving_speed
                    self.rect.y -= self.moving_speed

                    self.square_x1.rect.y -= self.moving_speed
                    self.square_x2.rect.y -= self.moving_speed
                    self.square_x3.rect.y -= self.moving_speed
                    self.square_x4.rect.y -= self.moving_speed

                    if self.show_sprite == True:
                        self.sprite.rect.y -= self.moving_speed
                elif self.count_moving >= self.moving_pixels*1.5:
                    if self.count_moving < self.moving_pixels*2.5:
                        self.count_moving += self.moving_speed
                        self.rect.x -= self.moving_speed

                        self.square_x1.rect.x -= self.moving_speed
                        self.square_x2.rect.x -= self.moving_speed
                        self.square_x3.rect.x -= self.moving_speed
                        self.square_x4.rect.x -= self.moving_speed

                        if self.show_sprite == True:
                            self.sprite.rect.x -= self.moving_speed

                    elif self.count_moving >= self.moving_pixels*2.5:
                        if self.count_moving < self.moving_pixels*3:
                            self.count_moving += self.moving_speed
                            self.rect.y += self.moving_speed

                            self.square_x1.rect.y += self.moving_speed
                            self.square_x2.rect.y += self.moving_speed
                            self.square_x3.rect.y += self.moving_speed
                            self.square_x4.rect.y += self.moving_speed

                            if self.show_sprite == True:
                                self.sprite.rect.y += self.moving_speed
                        elif self.count_moving == self.moving_pixels*3:
                            self.count_moving = 0




class Stair(pygame.sprite.Sprite):
    def __init__( 
        self, size=data_CF.pixel_space, position=(0, 0), show_collide=False,
        invert=False, climate=None
    ):
        super().__init__()
        
        # Ayuda necesaria
        self.surf = pygame.Surface( (size, size), pygame.SRCALPHA )
        self.rect = self.surf.get_rect( center=position )
        layer_all_sprites.add(self, layer=1)
        
        # Mostrar o no collider
        self.show_collide = show_collide
        if self.show_collide == True:
            self.surf.fill( generic_colors('white') )
        else:
            pass
        
        # Posicion aumeto/disminución de pixeles de coordenadas portes
        size_part = size//2
        if invert == True:
            more_pixels1 = 0
            more_pixels2 = size_part
            more_pixels3 = -(size)
        else:
            more_pixels1 = size_part
            more_pixels2 = size_part
            more_pixels3 = size
        
        # Partes de escalera
        self.climate = climate
        self.stair_part( 
            size=size_part, 
            position=(self.rect.x+more_pixels1, self.rect.y)
        )
        self.stair_part( 
            size=size_part, 
            position=(self.rect.x, self.rect.y+more_pixels2)
        )
        self.stair_part( 
            size=size_part, 
            position=(self.rect.x+more_pixels2, self.rect.y+more_pixels2)
        )
        
        # Parte necesaria para evitar bugs
        self.stair_part( 
            size=size, 
            position=(self.rect.x+more_pixels3, self.rect.y)
        )
        
    def stair_part(self, size=4, position=(0,0) ):
        stair_part = Floor( 
            size=(size, size), limit=False, climate=self.climate
        )
        if self.show_collide == True:
            stair_part.surf.fill( generic_colors('blue') )
        stair_part.rect.topleft = position
        solid_objects.add(stair_part)




class Climate_rain(pygame.sprite.Sprite):
    def __init__(
        self, size=data_CF.pixel_space, position=(data_CF.disp[0]//2, data_CF.disp[1]//2),
        show_collide=False, show_sprite=True
    ):
        super().__init__()
        
        # Mostrar Collider o no
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
        
        # Sección de collider
        self.surf = pygame.Surface( (size//4, size//4), pygame.SRCALPHA )
        self.surf.fill( generic_colors('sky_blue', self.transparency) )
        self.rect = self.surf.get_rect( center=position )
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
        
        layer_all_sprites.add(self, layer=1)
        climate_objects.add(self)
        
        # Sección de sprite
        self.fps = data_CF.fps//4
        self.fps_count = 0
        self.sprite_collide = None
        self.sprite = None
        self.size = size
        self.size_difference = (size//4)*3
        if show_sprite == True:
            self.__image = get_image( 'rain', size=[size,size], color=[0,0,127], transparency=127 )

            self.sprite = pygame.sprite.Sprite()
            self.sprite.surf = self.__image[0]
            self.sprite.rect = self.surf.get_rect()
            layer_all_sprites.add(self.sprite, layer=3)
        
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
        self.not_move = False

        # Eventos | Si traspasa la pantalla
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

        # Eventos | Si toca objetos solidos
        for solid_object in solid_objects:
            if self.rect.colliderect(solid_object.rect):
                self.collide = True

        # Eventos | Si colisiona con el player        
        for player in player_objects:
            if self.rect.colliderect(player.rect):
                self.collide = True
        
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
        size = (data_CF.pixel_space, data_CF.pixel_space), show_collide = True, position = (0, 0)
    ):
        super().__init__()
        
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
        self.surf.fill( generic_colors(color='red', transparency=self.transparency) )

        self.rect = self.surf.get_rect(
            center = ( position )
        )

        layer_all_sprites.add(self, layer=1)
        limit_objects.add(self)



class Level_change(pygame.sprite.Sprite):
    def __init__(
        self, level=None, dir_level=None, position=(0,0), gamecomplete=False,
        show_collide=False, show_sprite=True
    ):
        super().__init__()

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
        self.__transparency = 0
        if show_collide == True:
            self.__transparency = 255

        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        if gamecomplete == True:
            self.surf.fill( generic_colors('green', transparency=self.__transparency) )
        else:
            self.surf.fill( generic_colors('black', transparency=self.__transparency) )
        self.rect = self.surf.get_rect( center=position )
        layer_all_sprites.add(self, layer=2)
        level_objects.add(self)
        
        # Sprite
        if show_sprite == True:
            sprite = pygame.sprite.Sprite()
            
            if gamecomplete == True:
                sprite.surf = get_image( 'level_change', size=size, color=[0, 48, 0] )
            else:
                sprite.surf = get_image( 'level_change', size=size, color=[39, 28, 18] )

            sprite.rect = sprite.surf.get_rect( center=position )
            layer_all_sprites.add(sprite, layer=1)
    
    def update(self):
        if self.change_level == True:
            self.level = os.path.join( dir_maps, self.dir_level, self.name )
            if self.__gamecomplete == True:
                self.gamecomplete = True




class Score(pygame.sprite.Sprite):
    def __init__(self, size=data_CF.pixel_space, position=(0, 0), show_collide=False, show_sprite=True ):
        super().__init__()
        
        # Collider
        self.surf = pygame.Surface( ( size//2, size//2 ), pygame.SRCALPHA )
        if show_collide == True:
            self.surf.fill( generic_colors('yellow') )
        else:
            self.surf.fill( (0, 0, 0, 0) )
        self.rect = self.surf.get_rect( center=position )
        
        # Agregar collider
        layer_all_sprites.add(self, layer=3)
        score_objects.add(self)
        
        # Sprite
        if show_sprite == True:
            self.sprite = pygame.sprite.Sprite()
            self.sprite.surf = get_image( 'coin', size=[size, size] )
            self.sprite.rect = self.sprite.surf.get_rect(
                center=position
            )
            layer_all_sprites.add(self.sprite, layer=3)
        else:
            self.sprite = None
        
        
        # Variables principales
        self.point = False
    
    def remove_point(self):
        if not self.sprite == None:
            self.sprite.kill()
        self.kill()




class Cloud(pygame.sprite.Sprite):
    def __init__(
        self, size = (data_CF.pixel_space*4, data_CF.pixel_space*2),  position=(0,0),
        show_collide=False
    ):
        super().__init__()
        
        # Seccion de imagen
        image_set = random.choice( [1, 2, 3] )
        transparency = random.choice( [8, 16, 32] )
        
        if show_collide == False:
            self.surf = get_image(
                f'cloud-{image_set}', size=size, transparency=transparency, return_method='image'
            )
        else:
            self.surf = pygame.Surface( size, pygame.SRCALPHA )
            self.surf.fill( (191,191,191, transparency) )
        self.rect = self.surf.get_rect(topleft=position)
        
        nocamera_back_sprites.add(self)
        anim_sprites.add(self)
        
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
        transfer_disp = obj_not_see(
            disp_width=data_CF.disp[0], disp_height=data_CF.disp[1], obj=self, difference=self.rect.width,
            reduce_positive=True
        )
        if (
            transfer_disp == 'width_positive'
        ):
            self.rect.x = 0
        elif (
            transfer_disp == 'width_negative'
        ):
            self.rect.x = data_CF.disp[0]-(self.rect.width)


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