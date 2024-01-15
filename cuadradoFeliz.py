import pygame, sys, random
from pygame.locals import *

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

# Colores genericos
color_black = (0, 0, 0)
color_white = (128, 128, 128)




# Objetos / Clases
class Player(pygame.sprite.Sprite):
    def __init__(self, position=(disp_width//2,disp_height//2) ):
        super().__init__()
        
        # Sprite
        self.surf = pygame.Surface( (disp_width//120, disp_width//60) )
        self.surf.fill( (0, 255, 0) )
        
        # Collider y posición
        self.rect = self.surf.get_rect(
            center=position
        )
        
        # Spawn
        self.spawn_xy = [self.rect.x, self.rect.y]
        
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
                    self.surf.fill( (255, 255, 0) )
    
            if self.pressed_right:
                self.moving = True
                self.rect.x += self.speed
                if self.jumping == False and self.gravity == False:
                    self.surf.fill( (255, 255, 0) )
    
    def jump(self):
        if (
            not self.gravity == True and
            self.not_move == False
        ):
            self.jumping = True
    
    def update(self):
        # Colisiones
        collide = False
        damage = False
        instakill = False
        
        # Colisiones Objetos
        if pygame.sprite.spritecollide(self, instakill_objects, False):
            collide = True
            damage = True
            instakill = True

        if pygame.sprite.spritecollide(self, damage_objects, False):
            damage = True
            
        if pygame.sprite.spritecollide(self, solid_objects, False):
            collide = True
            
        # Collisionar con el final vertical de la pantalla
        if self.rect.y >= disp_height:
            instakill = True
        
        # Boleanos daño y instakill
        if instakill == True:
            damage = True
        
        if damage == True:
            collide = True
        
        # Eventos | Colsiones con solidos
        self.not_move = False
        for solid_object in solid_objects:
            # Acomodar coliders, dependiendo de la dirección de colisión:
            # arriba, abajo, izquierda, o derecha
            if self.rect.colliderect(solid_object.rect):
                collide = True
                
                # Para detectar que la altura el solido y la del jugador sean correctas.
                # Formula x + (y - x) = y
                # Ejemplo 8 + (16 - 8) = 8
                if self.rect.height > solid_object.rect.height:
                    # Advertencia Altura de solido mas pequeña comparada con la del jugador
                    more_height = True
                else:
                    more_height = False
                
                # Arriba y abajo
                # Recuerda que no se puede colisionar dos veces, se eliguira una colision, y en este caso siempre tiene mas pioridad la colision arriba, debido a que esta arriba de la linea de colision de la derecha.
                if self.rect.y < solid_object.rect.y:
                    #print('arriba')
                    self.rect.y = solid_object.rect.y - self.rect.height+1
                    #self.jumping = False
                elif self.rect.y > solid_object.rect.y+(solid_object.rect.height//4):
                    # El "+(solid_object.rect.height//4)", es para evitar dos colisiones al mismo tiempo:
                    # Puede ser colisionar abajo y del lado izquierdo o derecho.
                    # Funciona, porque la colision del lado inferior, esta un poco mas abajo de lo normal.
                    #print('abajo')
                    self.jumping = False
                    self.rect.y = solid_object.rect.y + solid_object.rect.height

                # Izquierda y derecha
                # Collisionar de izquierda/derecha solo cuando el jugador no es mas pequeño en hight que el solido
                # El "self.not_move", ayuda a que no puedas mover de ninguna manera al jugador
                # Los "self.rect.x +-= self.speed" vistos aqui, redirecciónan al lado contrario al jugador dependiendo si colisiono del lado derecho o del lado izquierdo
                # Recuerda que no se puede colisionar dos veces, se eliguira una colision, y en este caso siempre tiene mas pioridad la colision izquirda, debido a que esta arriba de la linea de colision de la derecha.
                elif more_height == False:
                    if self.rect.x < solid_object.rect.x+self.speed/8:
                        #print('izquierda')
                        self.not_move = True
                        self.jumping = False
                        self.rect.x = solid_object.rect.x -self.rect.width -self.speed
                    elif self.rect.x > solid_object.rect.x-self.speed/8:
                        #print('derecha')
                        self.not_move = True
                        self.jumping = False
                        self.rect.x = solid_object.rect.x +solid_object.rect.width +self.speed
                
                # Cuando la altura "hight" del solido es mas baja que la del el jugador
                if more_height == True:
                    # Aqui agragar codigo futuro
                    #height_difference = self.rect.height - solid_object.rect.height
                    pass

        # Eventos al colisionar
        if collide == True:
            self.gravity = False
            self.surf.fill( (255, 0, 0) )

            if damage == True:
                #self.rect.x += random.randint(-1, 1)
                #self.rect.y += random.randint(-1, 1)
                self.hp -= 1

                if instakill == True:
                    self.hp = -1

                if self.hp <= 0:
                    # El player se murio
                    # Establecer al player al spawn
                    self.hp = 0

        else:
            self.gravity = True
        
        # Gravedad
        if (
            self.gravity == True and
            self.jumping == False
        ):
            self.surf.fill( (0, 255, 255) )

            self.rect.y += self.gravity_power

            #print( 
            #    self.rect.x, self.rect.y
            #)
        else:
            if self.jumping == True:
                self.surf.fill( (0, 0, 255) )
                if not self.__jump_max_height <= 0:
                    self.rect.y -= self.jump_power
                    self.__jump_max_height -= self.jump_power
                else:
                    self.jumping = False
            else:
                self.surf.fill( (0, 255, 0) )
                self.__jump_max_height = self.jump_power*8
            #print('sin gravedad')

            self.rect.y += 0



class Floor(pygame.sprite.Sprite):
    def __init__(
        self,
        size = (disp_width, disp_width//60),
        position = (disp_width//2, (disp_height-8)),
        color=color_white,
        limit = True
    ):
        super().__init__()
        
        # Sprite
        self.surf = pygame.Surface( size )
        self.surf.fill(color)
        
        # Collider y posición
        self.rect = self.surf.get_rect( 
            center = position
        )
        self.add_limit = limit
        solid_objects.add(self)
        
    
    def limit_collision(self):
        if self.add_limit == True:
            # Limite de colision, si toca este limite, el jugador muere.
            # Esto es demostrativo, aun no funcional
            limit = pygame.sprite.Sprite()
            limit_xy = [
                round(self.rect.width*0.5, 4), round(self.rect.height*0.5, 4)
            ]
            limit.surf = pygame.Surface( (limit_xy[0], limit_xy[1]) )
            limit.surf.fill( (255,0,0) )
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


class Limit_indicator(pygame.sprite.Sprite):
    def __init__(self, 
        size = (disp_width//480, disp_width//60), see = True, position = (0, 0)
    ):
        super().__init__()
        
        self.surf = pygame.Surface( size )
        if see == True:
            self.surf.fill( (255, 0, 0) )
        self.rect = self.surf.get_rect(
            center = ( position )
        )



class Spike(pygame.sprite.Sprite):
    def __init__(self, position=(0,0) ):
        super().__init__()
        
        # Pico
        self.surf = pygame.Surface( (disp_width//240, disp_width//120) )
        self.surf.fill( (255, 0, 0) )
        self.rect = self.surf.get_rect(
            center=position
        )
        self.rect.y -= self.rect.height//2
        
        # Cuadrados solidos
        square_size = self.rect.height
        floor_x = Floor(
            size = ( square_size, square_size ),
            position = position,
            limit = False
        )
        floor_x.rect.x -= square_size//2
        floor_x.rect.y += square_size//2
        all_sprites.add(floor_x)
        
        floor_y = Floor(
            size = ( square_size, square_size ),
            position = position,
            limit = False
        )
        floor_y.rect.x += square_size//2
        floor_y.rect.y += square_size//2
        all_sprites.add(floor_y)




# Grupos de sprites
all_sprites = pygame.sprite.Group()
solid_objects = pygame.sprite.Group()
instakill_objects = pygame.sprite.Group()
damage_objects = pygame.sprite.Group()
limit_objects = pygame.sprite.Group()


'''
for x in range(0, 20):
    floor = Floor()
    floor.surf = pygame.Surface( (32, 4) )
    floor.surf.fill(color_white)
    floor.rect = floor.surf.get_rect(
        center = (
            random.randint(18, disp_width-18),
            random.randint(18, disp_height-18)
        )
    )
    floor.add_limit = False
    all_sprites.add(floor)
    #solid_objects.add(floor)
'''





# Funciones
class Start_Map():
    def __init__(self,
        x_column = 0,
        y_column = 0,
        map_level = [
            '|....pppp.......................................................................|',
            '.....p...........................................................................',
            '.....pjpp........................................................................',
            '.....pppp.........p..............................................................',
            '.................................................................................',
            '.......................................ppp.......................................',
            '.......................................p.p.......................................',
            '................p......................p.p.......................................',
            '.......................................ppp.......................................',
            '.................................................................................',
            '.......................p...............ppp........................................',
            '.................................................................................',
            '.................................................................................',
            '..............................p.....p............................................',
            '.............................p...................................................',
            '............................p.............p......................................',
            '........................pppp...............p.....................................',
            '.......................p....................p....................................',
            '......................p......................p...................................',
            '..................pppp........................p..................................',
            '..................p..........^^^^^^^^^^^pppppppppppppppp...p......p..............',
            '..................p..............................................................',
            '..................p.....................................................p........',
            '.............pppppp..............................................................',
            '.............p...........ppppppppppppppppp.......................................',
            '.................................................................................',
            '.........p..........................................................p............',
            '.................................................................................',
            '.................................................................................',
            '.....p...........................................................p...............',
            '.................................................................................',
            '...........p.....................................................................',
            '.................................................................................',
            '.............................................................p...................',
            '...................p.............................................................',
            '.................................................................................',
            '............................p..............................p.....................',
            'ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp',
            'ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp',
            '|...............................................................................|',
        ],
    ):
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
        test = ''
        for column in map_level:
            y_column += 1
            x_space = 0 + x_column
            for space in column:
                position=( (x_space*pixel_space), (y_column*pixel_space) )
                if space == '.':
                    x_space += 1
                if space == 'p':
                    x_space += 1
                    plat = Floor(
                        size=(pixel_space, pixel_space),
                        position=position
                    )
                    all_sprites.add(plat)
                    #test += f'columna {y_column}. {x_space*pixel_space}plataforma\n'
                if space == '|':
                    x_space += 1
                    limit = Limit_indicator(
                        position=position,
                        see=True
                    )
                    all_sprites.add(limit)
                    limit_objects.add(limit)
                if space == 'j':
                    x_space += 1
                    self.player_spawn = position
                if space == '^':
                    x_space += 1
                    spike = Spike( position=position )
                    all_sprites.add(spike)
                    instakill_objects.add(spike)
start_map = Start_Map(0, 0)

for plat in solid_objects:
    plat.limit_collision()

#player = Player( position=(disp_width//2, disp_height//2) )
player = Player( position=start_map.player_spawn )
all_sprites.add(player)




# Bucle del juego
camera_x = 0
camera_y = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == player.pressed_jump:
                player.jump()
    
    # Fondo
    display.fill(color_black)
    
    # Objetos / Sprites
    player.update()
    player.move()

    for sprite in all_sprites:
        display.blit(sprite.surf, sprite.rect)

    
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
    if player.hp == 0:
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
        player.rect.x = player.spawn_xy[0]
        player.rect.y = player.spawn_xy[1]
        player.hp = 100

    
    # Fin
    clock.tick(fps)
    pygame.display.update()