from Modulos.pygame.Modulo_pygame import (
    generic_colors, obj_collision_sides_solid, obj_coordinate_multiplier,
    player_camera_prepare, player_camera_move,
    obj_collision_sides_rebound, obj_not_see,
    Anim_sprite, Anim_sprite_set, Split_sprite
)
from .CF_info import (
    disp_width,
    disp_height,
    dir_game,
    dir_data,
    dir_sprites,
    dir_maps,
    fps,
    game_title
)

import pygame, sys, os, random
from pygame.locals import *


# Objetos / Clases
class Player(pygame.sprite.Sprite):
    def __init__(self, position=(disp_width//2,disp_height//2), show_collide=False, show_sprite=True ):
        super().__init__()
        
        # Sprite
        self.show_sprite = show_sprite
        self.sprite = None

        self.surf = pygame.Surface( (disp_width//120, disp_width//60), pygame.SRCALPHA )
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
        self.surf.fill( generic_colors(color='green', transparency=self.transparency) )
        
        # Collider y posición
        self.rect = self.surf.get_rect(
            center=position
        )
        all_sprites.add(self)
        player_objects.add(self)
        
        # Movimeinto
        # Jump power, establece velocidad y alura de salto.
        # speed, establece velocidad izquierda/derecha, y rebote en paredes.
        self.gravity_power      =   self.rect.height//4
        self.speed              =   self.rect.height//2
        self.jump_power         =   self.rect.height//2
        self.jumping = False
        self.not_move = False
        self.x_move_type = None
        
        # Vida
        self.hp = 100
    
    
    def move(self):
        # Sección sprite
        self.x_move_type = None
    
        # Teclas de movimiento
        pressed_keys = pygame.key.get_pressed()
        self.pressed_left = pressed_keys[K_LEFT]
        self.pressed_right = pressed_keys[K_RIGHT]
        self.pressed_jump =  pygame.K_SPACE
        
        # Iniciar o no el movimiento
        # Si el not_move esta en false, entonces puede seguir.
        # Si se pide unicamente una dirección (derecha/izquierda), puedes eguir
        self.moving = False
        if (
            self.not_move == False and
            not (self.pressed_left == True and self.pressed_right == True)
        ):
            if self.pressed_left:
                self.moving = True
                self.rect.x -= self.speed
                if self.jumping == False and self.gravity == False:
                    self.surf.fill( generic_colors('yellow', transparency=self.transparency) )
                    self.x_move_type = 'left-anim'
                elif self.jumping == True:
                    self.surf.fill( (128, 0, 255, self.transparency) )
                    self.x_move_type = 'left-jump'
                else:
                    self.surf.fill( (0, 128, 255, self.transparency) )
                    self.x_move_type = 'left-fall'
    
            if self.pressed_right:
                self.moving = True
                self.rect.x += self.speed
                if self.jumping == False and self.gravity == False:
                    self.surf.fill( generic_colors('yellow', transparency=self.transparency) )
                    self.x_move_type = 'right-anim'
                elif self.jumping == True:
                    self.surf.fill( (128, 0, 255, self.transparency) )
                    self.x_move_type = 'right-jump'
                else:
                    self.surf.fill( (0, 128, 255, self.transparency) )
                    self.x_move_type = 'right-fall'
    
    def jump(self):
        if (
            not self.gravity == True and
            self.not_move == False
        ):
            self.jumping = True
    
    def update(self):
        # Mostrar o no el sprite
        if self.sprite == None:
            if self.show_sprite == True:
                self.sprite = pygame.sprite.Sprite()
                image = Anim_sprite_set(
                    sprite_sheet=pygame.image.load(
                        os.path.join(dir_sprites, 'player/player_not-move.png')
                    ),
                    current_frame=0
                )
                self.sprite.surf = pygame.transform.scale(
                    image, 
                    ( (disp_width//30), disp_width//30 )
                )
                self.sprite.rect = self.sprite.surf.get_rect()
                all_sprites.add(self.sprite)
        else:
            if self.show_sprite == False:
                self.sprite.kill()
                self.sprite = None

        # Colisiones
        collide = False
        damage = False
        instakill = False
        
        # Colisiones Objetos
        if pygame.sprite.spritecollide(self, instakill_objects, False):
            instakill = True

        if pygame.sprite.spritecollide(self, damage_objects, False):
            damage = True
            
        if pygame.sprite.spritecollide(self, solid_objects, False):
            collide = True
            
        # Collisionar con el final vertical/horizontal de la pantalla
        if (
            self.rect.y >= disp_height or   self.rect.y <= 0 or
            self.rect.x >= disp_width or    self.rect.x <= 0
        ):
            instakill = True
        
        # Boleanos daño y instakill
        if instakill == True:
            damage = True
        
        # Eventos | Colsiones con solidos
        self.not_move = False
        for solid_object in solid_objects:
            # Acomodar coliders, dependiendo de la dirección de colisión:
            # arriba, abajo, izquierda, o derecha
            collision = obj_collision_sides_solid(obj_main=self, obj_collide=solid_object)
            if not collision == None:
                #print(collision)
                collide = True
        
        # Colision con cambio de nivel
        for level in level_objects:
            if self.rect.colliderect(level.rect):
                level.change_level = True


        # Eventos al colisionar
        if collide == True:
            self.gravity = False
            self.surf.fill( generic_colors('red', transparency=self.transparency) )

        else:
            self.gravity = True

        # Eventos al colisionar Daño
        if damage == True:
            # Erectos de daño
            self.not_move = True
            self.gravity = False
            self.jumping = False
            self.rect.x += random.choice( [-(self.speed), (self.speed)] )
            self.rect.y += random.choice( [-self.gravity_power, self.gravity_power] )

            # Eventos principales
            self.hp -= 10

            if instakill == True:
                self.hp = -1

        if self.hp <= 0:
            # El player se murio
            # Establecer al player al spawn
            self.not_move = True
            self.gravity = False
            self.jumping = False
        
        # Gravedad
        if (
            self.gravity == True and
            self.jumping == False
        ):
            self.surf.fill( generic_colors('sky_blue', transparency=self.transparency) )

            self.rect.y += self.gravity_power
            
            # Sección sprite y
            if self.show_sprite == True and (not self.sprite == None):
                self.sprite.kill()
                self.sprite = pygame.sprite.Sprite()
                image = Anim_sprite_set(
                    sprite_sheet=pygame.image.load(
                        os.path.join(dir_sprites, 'player/player_not-move.png')
                    ),
                    current_frame=2
                )
                self.sprite.surf = pygame.transform.scale(
                    image, 
                    ( (disp_width//30), disp_width//30 )
                )
                self.sprite.rect = self.sprite.surf.get_rect()
                all_sprites.add(self.sprite)

            #print( 
            #    self.rect.x, self.rect.y
            #)
        else:
            if self.jumping == True:
                self.surf.fill( generic_colors('blue', transparency=self.transparency) )

                if not self.__jump_max_height <= 0:
                    self.rect.y -= self.jump_power
                    self.__jump_max_height -= self.jump_power
                else:
                    self.jumping = False
                    
                # Sección sprite y
                if self.show_sprite == True and (not self.sprite == None):
                    self.sprite.kill()
                    self.sprite = pygame.sprite.Sprite()
                    image = Anim_sprite_set(
                        sprite_sheet=pygame.image.load(
                            os.path.join(dir_sprites, 'player/player_not-move.png')
                        ),
                        current_frame=1
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)

            else:
                self.surf.fill( generic_colors('green', transparency=self.transparency) )
                self.__jump_max_height = self.jump_power*8
                
                # Sección sprite y
                if self.show_sprite == True and (not self.sprite == None):
                    self.sprite.kill()
                    self.sprite = pygame.sprite.Sprite()
                    image = Anim_sprite_set(
                        sprite_sheet=pygame.image.load(
                            os.path.join(dir_sprites, 'player/player_not-move.png')
                        ),
                        current_frame=0
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)
            #print('sin gravedad')

            self.rect.y += 0
            
        # Scción sprite y movimiento x
        if not self.x_move_type == None:
            image=pygame.image.load(
                os.path.join(dir_sprites, 'player/player_move.png')
            )
            if self.show_sprite == True and (not self.sprite == None):
                self.sprite.kill()
                if self.x_move_type == 'right-anim':
                    self.sprite = pygame.sprite.Sprite()
                    image = Anim_sprite_set(
                        sprite_sheet=image,
                        current_frame=0
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)

                elif self.x_move_type == 'right-jump':
                    self.sprite = pygame.sprite.Sprite()
                    image = Anim_sprite_set(
                        sprite_sheet=image,
                        current_frame=1
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)
                elif self.x_move_type == 'right-fall':
                    self.sprite = pygame.sprite.Sprite()
                    image = Anim_sprite_set(
                        sprite_sheet=image,
                        current_frame=6
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)
                    
                elif self.x_move_type == 'left-anim':
                    self.sprite = pygame.sprite.Sprite()
                    image = pygame.transform.flip(image, True, False)
                    image = Anim_sprite_set(
                        sprite_sheet=image,
                        current_frame=7
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)

                elif self.x_move_type == 'left-jump':
                    self.sprite = pygame.sprite.Sprite()
                    image = pygame.transform.flip(image, True, False)
                    image = Anim_sprite_set(
                        sprite_sheet=image,
                        current_frame=6
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)
                elif self.x_move_type == 'left-fall':
                    self.sprite = pygame.sprite.Sprite()
                    image = pygame.transform.flip(image, True, False)
                    image = Anim_sprite_set(
                        sprite_sheet=image,
                        current_frame=1
                    )
                    self.sprite.surf = pygame.transform.scale(
                        image, 
                        ( (disp_width//30), disp_width//30 )
                    )
                    self.sprite.rect = self.sprite.surf.get_rect()
                    all_sprites.add(self.sprite)
        

        # Actualizar sprite
        if not self.sprite == None:
            self.sprite.rect.x = self.rect.x -(self.rect.width+(self.rect.width//2))
            self.sprite.rect.y = self.rect.y -self.rect.height




class Floor(pygame.sprite.Sprite):
    def __init__(
        self,
        size = (disp_width, disp_width//60),
        position = (disp_width//2, (disp_height-8)),
        color='grey', show_collide=True, show_sprite=True,
        limit = True
    ):
        super().__init__()
        
        # Sprite
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
            
        if show_sprite == True:
            self.surf = pygame.transform.scale(
                pygame.image.load(os.path.join(dir_sprites, 'floor/stone.png')), size
            )
        else:
            self.surf = pygame.Surface( size, pygame.SRCALPHA )
            self.surf.fill( generic_colors(color=color, transparency=self.transparency) )
        
        # Collider y posición
        self.rect = self.surf.get_rect( 
            center = position
        )
        self.add_limit = limit
        all_sprites.add(self)
        solid_objects.add(self)
        
    
    def limit_collision(self):
        if self.add_limit == True:
            # Limite de colision, si toca este limite, el jugador muere.
            # Esto es demostrativo, aun no funcional
            limit = pygame.sprite.Sprite()
            limit_xy = [
                round(self.rect.width*0.5, 4), round(self.rect.height*0.5, 4)
            ]
            limit.surf = pygame.Surface( (limit_xy[0], limit_xy[1]), pygame.SRCALPHA )
            limit.surf.fill( generic_colors(color='red', transparency=self.transparency) )
            limit.rect = limit.surf.get_rect(
                center=(
                    self.rect.x+(self.rect.width -limit_xy[0]),
                    self.rect.y+(self.rect.height -limit_xy[1])
                )
            )
            all_sprites.add(limit)
            #instakill_objects.add(limit)
            #damage_objects.add(limit)
            #print(self.rect.width)
            #print(self.rect.height)
            #print(limit_xy)
            #print(self.rect.x+(self.rect.width -limit_xy[0]))
            #print(self.rect.y+(self.rect.height -limit_xy[1]))



class Spike(pygame.sprite.Sprite):
    def __init__(self, size=disp_width//60, position=(0,0), show_collide=True ):
        super().__init__()

        # Sprite
        self.surf = pygame.Surface( (size/4, size/2), pygame.SRCALPHA )
        if show_collide == True:
            self.transparency = 255
        else:
            self.transparency = 0
            sprite = pygame.sprite.Sprite()
            sprite.surf = pygame.transform.scale(
                pygame.image.load(os.path.join(dir_sprites, 'spikes/spike.png')), (size, size)
            )
            sprite.rect = sprite.surf.get_rect(center=position)
            all_sprites.add(sprite)

        self.surf.fill( generic_colors(color='red', transparency=self.transparency) )

        # Collider pico
        self.rect = self.surf.get_rect(
            center=position
        )
        self.rect.y -= self.rect.height//2
        all_sprites.add(self)
        instakill_objects.add(self)
        #damage_objects.add(self)
        
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



class Star_pointed(pygame.sprite.Sprite):
    def __init__(self, size=disp_width//60, position=(0,0) ):
        super().__init__()
        
        # Collider principal
        self.surf = pygame.Surface( ( size/2, size/2 ) )
        self.surf.fill( generic_colors('green') )
        self.rect = self.surf.get_rect( center=position )
        
        all_sprites.add(self)
        anim_sprites.add(self)
        
        # Cuadrados dañinos
        size_square = self.rect.width/2
        
        self.square_x1 = self.square_damage(
            size=size_square, position=(self.rect.x, self.rect.y +(size_square//2) ),
            color=generic_colors('black')
        )
        self.square_x2 = self.square_damage(
            size=size_square, position=(
                self.rect.x-size_square, self.rect.y +(size_square//2) 
            ),
            color=generic_colors('red')
        )
        self.square_x3 = self.square_damage(
            size=size_square, position=(self.rect.x+size_square, self.rect.y +(size_square//2) ),
            color=generic_colors('grey')
        )
        self.square_x4 = self.square_damage(
            size=size_square, position=(self.rect.x+(size_square*2), self.rect.y +(size_square//2) ),
            color=generic_colors('blue')
        )
        
        # Animacion Variables
        self.fps = size_square
        self.count = 0


    def square_damage(self, size=4, position=(0,0), color=generic_colors('green') ):
        square = pygame.sprite.Sprite()
        square.surf = pygame.Surface( (size, size) )
        square.surf.fill( color )
        square.rect = square.surf.get_rect( topleft=position)
        all_sprites.add(square)
        damage_objects.add(square)
        #instakill_objects.add(square)
        return square
    
    def anim(self):
        if self.count < self.fps:
            self.count += 1
            self.square_x2.rect.y -= 1
            
            self.square_x4.rect.y += 1

        elif self.count >= self.fps:
            if self.count < self.fps+(self.fps//2):
                self.count += 1
                self.square_x1.rect.y -= 1
                self.square_x2.rect.y -= 1
                self.square_x3.rect.y += 1
                self.square_x4.rect.y += 1
            if self.count >= self.fps+(self.fps//2):
                if self.count < self.fps*2:
                    self.count += 1
                    self.square_x1.rect.x += 1
                    self.square_x2.rect.x += 3
                    self.square_x3.rect.x -= 1
                    self.square_x4.rect.x -= 3
                elif self.count >= self.fps*2:
                    if self.count < self.fps*3:
                        self.count += 1
                        self.square_x2.rect.x += 1
                        
                        self.square_x4.rect.x -= 1
                    elif self.count >= self.fps*3:
                        if self.count < self.fps*3+(self.fps//2):
                            self.count += 1
                            self.square_x1.rect.x += 1
                            self.square_x2.rect.x += 1
                            self.square_x3.rect.x -= 1
                            self.square_x4.rect.x -= 1
                        elif self.count >= self.fps*3+(self.fps//2):
                            if self.count < self.fps*4:
                                self.count += 1
                                self.square_x1.rect.y += 1
                                self.square_x2.rect.y += 3
                                self.square_x3.rect.y -= 1
                                self.square_x4.rect.y -= 3
                            elif self.count >= self.fps*4:
                                self.count = 0
                                self.square_x1.rect.x -= self.fps

                                self.square_x2.rect.x -= (self.fps*3)

                                self.square_x3.rect.x += self.fps

                                self.square_x4.rect.x += (self.fps*3)




class Climate_rain(pygame.sprite.Sprite):
    def __init__(self, size=disp_width//60, position=(disp_width//2, disp_height//2) ):
        super().__init__()
        
        self.surf = pygame.Surface( (size//4, size//4) )
        self.surf.fill( generic_colors('blue') )
        self.rect = self.surf.get_rect( center=position )
        self.speed_y = size//2
        self.speed_x = self.speed_y//2
        self.move = False
        
        all_sprites.add(self)
        climate_objects.add(self)
        
    def update(self):            
        # Mover al jugador si el collider esta en false
        self.collide = False
        if self.collide == False and self.move == True:
            self.rect.y += self.speed_y
            self.rect.x -= self.speed_x

        # Si traspasar la pantalla
        transfer_disp = obj_not_see(disp_width=disp_width, disp_height=disp_height, obj=self)
        if (
            #transfer_disp == 'width_positive' or
            #transfer_disp == 'width_negative' or
           transfer_disp == 'height_positive'
        ):
            self.collide = True

        # Si toca objetos solidos
        for solid_object in solid_objects:
            if self.rect.colliderect(solid_object.rect):
                self.collide = True

        # Si colisiona con el player        
        for player in player_objects:
            if self.rect.colliderect(player.rect):
                self.collide = True




class Anim_player_dead(pygame.sprite.Sprite):
    def __init__(self, position=(0,0), fps=fps, show_collide=False ):
        super().__init__()
        
        self.transparent = 255
        if show_collide == False:
            self.transparent = 0

        # Principal
        self.size = disp_width//60
        self.surf = pygame.Surface( (self.size, self.size), pygame.SRCALPHA )
        self.rect = self.surf.get_rect( center=position )
    
        self.fps = fps*3
        self.__count = 0
        self.anim_fin = False
        all_sprites.add( self )
        anim_sprites.add( self )
        
        # Partes
        size_parts = self.size//2
        self.part1 = Player_part( 
            size=size_parts,
            position=(self.rect.x+size_parts//2, self.rect.y + (size_parts+size_parts//2) ),
            color=generic_colors('green', self.transparent), sprite=3
        )
        
        self.part2 = Player_part( 
            size=size_parts,
            position=(self.rect.x+(size_parts+size_parts//2), self.rect.y + (size_parts+size_parts//2) ),
            color=generic_colors('blue', self.transparent), sprite=4
        )
        
        self.part3 = Player_part( 
            size=size_parts,
            position=(self.rect.x+size_parts//2, self.rect.y+size_parts//2),
            color=generic_colors('yellow', self.transparent), sprite=1
        )

        self.part4 = Player_part( 
            size=size_parts,
            position=(self.rect.x+(size_parts+size_parts//2), self.rect.y+size_parts//2),
            color=generic_colors('sky_blue', self.transparent), sprite=2
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
    def __init__(self, size=disp_width//120, color=generic_colors('green'), position=(0,0), sprite=None ):
        super().__init__()
        
        # Collider y sprite
        self.size = size
        if not sprite == None:
            img = pygame.transform.scale(
                pygame.image.load( os.path.join(dir_sprites, 'player/player_not-move.png') ),
                (disp_width//30*3, disp_width//30)
            )
            img = Anim_sprite_set(
                sprite_sheet=img,
                current_frame=0
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
        all_sprites.add(self)
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


            
class Limit_indicator(pygame.sprite.Sprite):
    def __init__(self, 
        size = (disp_width//60, disp_width//60), see = True, position = (0, 0)
    ):
        super().__init__()
        
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        if see == True:
            self.transparency = 255
        else:
            self.transparency = 0
        self.surf.fill( generic_colors(color='red', transparency=self.transparency) )

        self.rect = self.surf.get_rect(
            center = ( position )
        )

        all_sprites.add(self)
        limit_objects.add(self)



class Level_change(pygame.sprite.Sprite):
    def __init__(self, level=None, dir_level=None, position=(0,0) ):
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
        
        # Collider y sprite
        self.surf = pygame.Surface( (disp_width//60, disp_width//60) )
        self.rect = self.surf.get_rect( center=position )
        all_sprites.add(self)
        level_objects.add(self)
    
    def update(self):
        if self.change_level == True:
            self.level = os.path.join( dir_maps, self.dir_level, self.name )




# Grupos de sprites
all_sprites = pygame.sprite.Group()

player_objects = pygame.sprite.Group()
solid_objects = pygame.sprite.Group()
instakill_objects = pygame.sprite.Group()
damage_objects = pygame.sprite.Group()
limit_objects = pygame.sprite.Group()
level_objects = pygame.sprite.Group()
anim_sprites = pygame.sprite.Group()
climate_objects = pygame.sprite.Group()