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
color_white = (255, 255, 255)




# Objetos / Clases
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Sprite
        self.surf = pygame.Surface( (disp_width//120, disp_width//60) )
        self.surf.fill( (0, 255, 0) )
        
        # Collider y posición
        self.rect = self.surf.get_rect(
            center=(8,8)
        )
        
        # Variables
        self.not_move = False
        self.hp = 100
        self.gravity_power = 4
        self.speed = 8
        
        self.jumping = False
        self.__jump_max_height = 64
        self.jump_power = 8
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.not_move == False:
            if pressed_keys[K_LEFT]:
                self.rect.x -= self.speed
                if self.jumping == False and self.gravity == False:
                    self.surf.fill( (255, 255, 0) )
    
            if pressed_keys[K_RIGHT]:
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
        
        # Colisiones Objetos dañinos
        if pygame.sprite.spritecollide(self, instakill_objects, False):
            collide = True
            damage = True
            instakill = True

        if pygame.sprite.spritecollide(self, damage_objects, False):
            collide = True
            damage = True
        
        # Colsiones objetos solidos
        self.not_move = False
        for solid_object in solid_objects:
            # Acomodar coliders, dependiendo de la dirección de colisión:
            # arriba, abajo, izquierda, o derecha
            if self.rect.colliderect(solid_object.rect):
                collide = True
                
                # Arriba y abajo
                if self.rect.y < solid_object.rect.y:
                    #print('arriba')
                    self.rect.y = solid_object.rect.y - self.rect.height+1
                    #self.jumping = False
                elif self.rect.y > solid_object.rect.y+(solid_object.rect.height//4):
                    #print('abajo')
                    # El "+(solid_object.rect.height//4)", es para evitar dos colisiones al mismo tiempo:
                    # Puede ser colisionar abajo y del lado izquierdo o derecho.
                    # Funciona, porque la colision del lado inferior, esta un poco mas abajo de lo normal.
                    self.jumping = False
                    self.rect.y = solid_object.rect.y + solid_object.rect.height

                # Izquierda y derecha
                # El "self.not_move", ayuda a que no puedas mover de ninguna manera al jugador
                # Los for vistos aqui, redirecciónan al lado contrario al jugador dependiendo si colisiono del lado derecho o del lado izquierdo
                elif self.rect.x < solid_object.rect.x:
                    #print('izquierda')
                    self.not_move = True
                    self.rect.x = solid_object.rect.x - self.rect.width
                    for x in range(0, 10):
                        self.rect.x -= 1
                elif self.rect.x > solid_object.rect.x:
                    #print('derecha')
                    self.not_move = True
                    self.rect.x = solid_object.rect.x + solid_object.rect.width
                    for x in range(0, 10):
                        self.rect.x += 1
        
        if self.rect.y >= disp_height:
            collide = True

        if pygame.sprite.spritecollide(self, solid_objects, False):
            collide = True

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
                    self.kill()
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
                self.__jump_max_height = 64
            #print('sin gravedad')

            self.rect.y += 0



class Floor(pygame.sprite.Sprite):
    def __init__(
        self,
        size = (disp_width, disp_width//60),
        position = (disp_width//2, (disp_height-8)),
        color=color_white
    ):
        super().__init__()
        
        # Sprite
        self.surf = pygame.Surface( size )
        self.surf.fill(color)
        
        # Collider y posición
        self.rect = self.surf.get_rect( 
            center = position
        )
        
    
    def limit_collision(self):
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




# Grupos de sprites
all_sprites = pygame.sprite.Group()
solid_objects = pygame.sprite.Group()
instakill_objects = pygame.sprite.Group()
damage_objects = pygame.sprite.Group()

#floor_main = Floor()
#all_sprites.add(floor_main)
#solid_objects.add(floor_main)

'''
for x in range(0, 64):
    floor = Floor()
    floor.surf = pygame.Surface( (16, 2) )
    floor.rect = floor.surf.get_rect(
        center = (
            random.randint(18, disp_width-18),
            random.randint(18, disp_height-18)
        )
    )
    all_sprites.add(floor)
    solid_objects.add(floor)
'''




# Funciones
def start_map(
        default_map = [
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', ''
            '...................p.................................pp.....',
            '.....................................................pp.....',
            '...p..........p................................p.....pp.....',
            '...p....p.............p..................p..................',
            '...p.................................................pp......',
            'pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp',
            'pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp',
        ]
    ):
    y_column = 0
    x_space = 0
    plat_number = 0
    pixel_space = disp_width//60
    test = ''
    for column in default_map:
        y_column += 1
        x_space = 0
        for space in column:
            if space == '.':
                x_space += 1
            if space == 'p':
                x_space += 1
                plat = Floor(
                    size=(pixel_space, pixel_space),
                    position=( (x_space*pixel_space), (y_column*pixel_space) )
                )
                all_sprites.add(plat)
                solid_objects.add(plat)
                #test += f'columna {y_column}. {x_space*pixel_space}plataforma\n'
    #input(test)
start_map()

for plat in solid_objects:
    plat.limit_collision()

player = Player()
all_sprites.add(player)




# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    # Fondo
    display.fill(color_black)
    
    # Objetos / Sprites
    #floor_main.update()
    player.update()
    player.move()

    for sprite in all_sprites:
        display.blit(sprite.surf, sprite.rect)
    
    # Fin
    clock.tick(fps)
    pygame.display.update()