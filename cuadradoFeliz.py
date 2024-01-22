from Modulos.Modulo_Text import (
    Text_Read, Ignore_Comment, Only_Comment
)
from Modulos.pygame.Modulo_pygame import (
    generic_colors, obj_collision_sides_solid, obj_coordinate_multiplier,
    player_camera_prepare, player_camera_move,
    obj_collision_sides_rebound
)

import pygame, sys, os, random
from pygame.locals import *


# Directorio del juego
dir_game = os.path.dirname(__file__)

dir_data = os.path.join(dir_game, 'data')

# Sub directorios Data
dir_sprites = os.path.join(dir_data, 'sprites')
dir_maps = os.path.join(dir_data, 'maps')


# Inicalizar pygame
pygame.init()

# Resolución de pantalla de juego
disp_width = 960
disp_height = 540
disp_resolution = ( disp_width, disp_height )
display = pygame.display.set_mode( disp_resolution )

# Fotogramas del juego
fps = 30
clock = pygame.time.Clock()

# Titulo del juego
pygame.display.set_caption('El cuadrado Feliz')




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
        
        # Movimeinto
        # Jump power, establece velocidad y alura de salto.
        # speed, establece velocidad izquierda/derecha, y rebote en paredes.
        self.gravity_power      =   self.rect.height//4
        self.speed              =   self.rect.height//2
        self.jump_power         =   self.rect.height//2
        self.jumping = False
        self.not_move = False
        
        # Vida
        self.hp = 100
    
    
    def move(self):
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
                elif self.jumping == True:
                    self.surf.fill( (128, 0, 255, self.transparency) )
                else:
                    self.surf.fill( (0, 128, 255, self.transparency) )
    
            if self.pressed_right:
                self.moving = True
                self.rect.x += self.speed
                if self.jumping == False and self.gravity == False:
                    self.surf.fill( generic_colors('yellow', transparency=self.transparency) )
                elif self.jumping == True:
                    self.surf.fill( (128, 0, 255, self.transparency) )
                else:
                    self.surf.fill( (0, 128, 255, self.transparency) )
    
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
                self.sprite.surf = pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(dir_sprites, 'player/player_not-move.png')), 
                        (disp_width//60, disp_width//60
                    )
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


        # Eventos al colisionar
        if collide == True:
            self.gravity = False
            self.surf.fill( generic_colors('red', transparency=self.transparency) )

        else:
            self.gravity = True

        if damage == True:
            #self.rect.x += random.randint(-1, 1)
            #self.rect.y += random.randint(-1, 1)
            self.hp -= 1

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
            else:
                self.surf.fill( generic_colors('green', transparency=self.transparency) )
                self.__jump_max_height = self.jump_power*8
            #print('sin gravedad')

            self.rect.y += 0
        
        # Actualizar sprite
        if not self.sprite == None:
            self.sprite.rect.x = self.rect.x -(self.rect.width/2)
            self.sprite.rect.y = self.rect.y




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




class Anim_player_dead(pygame.sprite.Sprite):
    def __init__(self, position=(0,0), fps=fps ):
        super().__init__()

        # Principal
        self.size = disp_width//60
        self.surf = pygame.Surface( (self.size, self.size) )
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
            color=generic_colors('green') 
        )
        
        self.part2 = Player_part( 
            size=size_parts,
            position=(self.rect.x+(size_parts+size_parts//2), self.rect.y + (size_parts+size_parts//2) ),
            color=generic_colors('blue') 
        )
        
        self.part3 = Player_part( 
            size=size_parts,
            position=(self.rect.x+size_parts//2, self.rect.y+size_parts//2),
            color=generic_colors('yellow') 
        )

        self.part4 = Player_part( 
            size=size_parts,
            position=(self.rect.x+(size_parts+size_parts//2), self.rect.y+size_parts//2),
            color=generic_colors('sky_blue') 
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
            self.surf.fill( ( 255-(self.__count*5), 0, 0)  )

        if self.__count == self.fps:
            # Animacion terminada, todos los objetos se eliminaran
            self.anim_fin = True
            self.part1.kill()
            self.part2.kill()
            self.part3.kill()
            self.part4.kill()
            self.kill()



class Player_part(pygame.sprite.Sprite):
    def __init__(self, size=disp_width//120, color=generic_colors('green'), position=(0,0) ):
        super().__init__()
        
        # Collider y sprite
        self.size = size
        self.surf = pygame.Surface( (self.size, self.size) )
        self.surf.fill( color  )
        self.rect = self.surf.get_rect( 
            center=position
        )
        all_sprites.add(self)
        
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
    def __init__(self, level=None, position=(0,0) ):
        super().__init__()

        if level == None:
            self.name = '_default'
        else:
            self.name = f'_{level}'
        self.level = None
        
        # Collider y sprite
        self.surf = pygame.Surface( (disp_width//60, disp_width//60) )
        self.rect = self.surf.get_rect( center=position )
        all_sprites.add(self)
        level_objects.add(self)
    
    def update(self):
        if self.rect.colliderect(player.rect):
            self.level = os.path.join( dir_maps, f'cf_map{self.name}.txt' )




# Grupos de sprites
all_sprites = pygame.sprite.Group()
solid_objects = pygame.sprite.Group()
instakill_objects = pygame.sprite.Group()
damage_objects = pygame.sprite.Group()
limit_objects = pygame.sprite.Group()
level_objects = pygame.sprite.Group()
anim_sprites = pygame.sprite.Group()


'''
for x in range(0, 10):
    floor = Floor(
        size=(disp_width//30, disp_width//60),
        position=(
            random.randint(disp_width//60, disp_width-disp_width//60),
            random.randint(disp_width//60, disp_height-disp_width//60)            
        ),
        limit=False,
        show_collide=False
    )
'''




# Funciones
class Start_Map():
    def __init__(self,
        x_column = 0,
        y_column = 0,
        map_level = Text_Read(os.path.join(dir_maps, 'cf_map_level-test.txt'), 'ModeText')
    ):
        #cf_map_default.txt
        #cf_map.txt
        #cf_map_level-test.txt
        #cf_map_level-test1.txt
        '''
        Funcion que permite crear niveles de una forma visual y sencilla.
        "." para un espacio de el "ancho sobre 60" del juego
        "p" para una plataforma con un espacio del "ancho sobre 60" del juego
        "|" para establecer el limite de la camara, con un espacio del ancho sobre el juego"
        
        "x, y" column son para establecer el pixel de inicio basado en la resolucion del juego. Por defecto inician en 0, 0.
        '''
        self.player_spawn = None
        plat_number = 0
        pixel_space = disp_width//60
        
        # Establecer la información del mapa
        change_level = None
        map_info = Only_Comment(
            text=map_level,
            comment='$$'
        )
        info = None
        if not map_info == None:
            info = []
            for line in map_info.split('\n'):
                info.append(line)
            change_level = info[0]

        # Establecer objetos en su posición inidaca
        map_level = Ignore_Comment(text=map_level, comment='//')
        map_level = Ignore_Comment(text=map_level, comment='$$')
        test = ''
        for column in map_level.split('\n'):
            y_column += 1
            x_space = x_column
            for space in column:
                position=( (x_space*pixel_space), (y_column*pixel_space) )
                if space == '.' or space == '#':
                    x_space += 1

                elif space == 'p':
                    x_space += 1
                    plat = Floor(
                        size=(pixel_space, pixel_space),
                        position=position,
                        show_collide=False
                    )
                
                elif space == 'P':
                    x_space += 1

                    # Para acomodar los objetos de forma adecuada.
                    multipler = obj_coordinate_multiplier(
                        multipler=2,
                        pixel=pixel_space,
                        x=x_space,
                        y=y_column
                    )
                    size=multipler[0]
                    position=multipler[1]

                    plat = Floor(
                        size=size,
                        position=position,
                        show_collide=False
                    )

                elif space == '|':
                    x_space += 1
                    limit = Limit_indicator(
                        position=position,
                        see=False
                    )

                elif space == 'j':
                    x_space += 1
                    self.player_spawn = position

                elif space == '^':
                    x_space += 1
                    spike = Spike( position=position, show_collide=False )
                    
                elif space == 'A':
                    x_space += 1

                    # Para acomodar los objetos de forma adecuada.
                    multipler = obj_coordinate_multiplier(
                        multipler=2,
                        pixel=pixel_space,
                        x=x_space,
                        y=y_column
                    )
                    for x in multipler[0]:
                        size = x
                    position=multipler[1]

                    spike = Spike(
                        size=size,
                        position=position,
                        show_collide=False
                    )

                elif space == '0':
                    x_space += 1

                    level = Level_change(
                        level=change_level,
                        position=position
                    )




# Iniciar Funciones y contantes necesarias
start_map = Start_Map(0, 0)

for plat in solid_objects:
    plat.limit_collision()

player = Player( position=start_map.player_spawn )

player_spawn_hp = player.hp
player_spawn_xy = player_camera_prepare(
    disp_width=disp_width, disp_height=disp_height, more_pixels=disp_width//30,
    all_sprites=all_sprites, player=player, show_coordenades=True
)
player_show_sprite = player.show_sprite
player_anim_dead = None

camera_x = 0
camera_y = 0




# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == player.pressed_jump:
                player.jump()
    
    # Fondo
    display.fill( (155, 168, 187) )
    
    # Objetos para cambiar de nivel
    for sprite in level_objects:
        sprite.update()
        if not sprite.level == None:
            level = sprite.level

            for other_sprite in all_sprites:
                other_sprite.kill()

            start_map = Start_Map(
                 0, 0,
                 map_level = Text_Read(level, 'ModeText')
            )

            for plat in solid_objects:
                plat.limit_collision()

            player = Player( position=start_map.player_spawn )
            player.hp = player_spawn_hp

            #player_spawn_hp = player_spawn_hp
            player_spawn_xy = player_camera_prepare(
                disp_width=disp_width, disp_height=disp_height, more_pixels=disp_width//30,
                all_sprites=all_sprites, player=player, show_coordenades=True
            )
            #player_show_sprite = player_show_sprite
            player_anim_dead = None

            camera_x = 0
            camera_y = 0
    
    # Objetos / Sprites Normales  
    player.update()
    player.move()

    for sprite in all_sprites:
        if not sprite == player:
            display.blit(sprite.surf, sprite.rect)
        
    for sprite in all_sprites:
        if sprite == player:
            display.blit(sprite.surf, sprite.rect)
    
    for sprite in anim_sprites:
        sprite.anim()

    # Camara
    camera = player_camera_move(
        disp_width=disp_width, disp_height=disp_height,
        camera_x=camera_x, camera_y=camera_y, 
        all_sprites=all_sprites,
        limit_objects=limit_objects,
        player=player,
    )
    camera_x=camera[0]
    camera_y=camera[1]
    dead = camera[2]
    if dead == True:
        if player_anim_dead == None:
            player_anim_dead = Anim_player_dead(
                position=(
                    (player.rect.x +(player.rect.width/2)),
                    player.rect.y+(player.rect.height//2)
                )
            )
            player.show_sprite = False
        else:
            if player_anim_dead.anim_fin == True:
                player_anim_dead = None
                # Establecer todos los objetos como al inicio del juego
                # Con base al valor xy actual de la camara, sus valores xy se invierten y se suman a las coordenadas actuales de los sprites.
                # Recuerda que esto es posible: "x+ -x = 0"
                for sprite in all_sprites:
                    sprite.rect.x += (camera_x*-1)
                    sprite.rect.y += (camera_y*-1)
            
                # Establecer camara en la posición inicial
                camera_x = 0
                camera_y = 0
            
                # Establecer player como al inicio del juego
                player.rect.x = player_spawn_xy[0]
                player.rect.y = player_spawn_xy[1]
                player.hp = player_spawn_hp
                player.show_sprite = player_show_sprite
        

    
    # Fin
    clock.tick(fps)
    pygame.display.update()