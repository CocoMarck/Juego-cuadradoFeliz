import pygame, sys
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
        self.surf = pygame.Surface( (8, 16) )
        self.surf.fill( (0, 255, 0) )
        
        # Collider y posición
        self.rect = self.surf.get_rect(
            center=(8,8)
        )
        
        # Variables
        self.gravity_power = 4
        self.speed = 8
        
        self.jumping = False
        self.__jump_max_height = 64
        self.jump_power = 8
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_LEFT]:
            self.rect.x -= self.speed
            if self.jumping == False and self.gravity == False:
                self.surf.fill( (255, 255, 0) )
        
        if pressed_keys[K_RIGHT]:
            self.rect.x += self.speed
            if self.jumping == False and self.gravity == False:
                self.surf.fill( (255, 255, 0) )
    
    def jump(self):
        if not self.gravity == True:
            self.jumping = True
    
    def update(self):
        self.gravity = True

        # Colisiones
        collide = False
        if self.rect.y >= disp_height:
            self.gravity = False
            collide = True

        if pygame.sprite.spritecollide(self, solid_objects, False):
            self.gravity = False
            collide = True

        if collide == True:
            #self.rect.x += random.randint(-1, 1)
            #self.rect.y += random.randint(-1, 1)
            self.surf.fill( (255, 0, 0) )
        
        # Gravedad
        if (
            self.gravity == True and
            self.jumping == False
        ):
            self.surf.fill( (0, 255, 255) )

            self.rect.y += self.gravity_power

            print( 
                self.rect.x, self.rect.y
            )
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
            print('sin gravedad')

            self.rect.y += 0



class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Sprite
        self.surf = pygame.Surface( (disp_width, 16) )
        self.surf.fill(color_white)
        
        # Collider y posición
        self.rect = self.surf.get_rect( 
            center = (disp_width//2, (disp_height-8))
        )




# Grupos de sprites
all_sprites = pygame.sprite.Group()
solid_objects = pygame.sprite.Group()

floor_main = Floor()
player = Player()

all_sprites.add(floor_main)
all_sprites.add(player)
solid_objects.add(floor_main)

'''
for x in range(0, 64):
    import random
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
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
            '...................p........................................',
            '............................................................',
            '..............p.............................................',
            '.......p..............p..................p..................',
            '...p.................................................p......',
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
                plat = Floor()
                plat.surf = pygame.Surface( (pixel_space, pixel_space) )
                plat.surf.fill(color_white)
                plat.rect = plat.surf.get_rect(
                    center = ( (x_space*pixel_space), (y_column*pixel_space) )
                )
                all_sprites.add(plat)
                solid_objects.add(plat)
                #test += f'columna {y_column}. {x_space*pixel_space}plataforma\n'
    #input(test)
start_map()




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
    floor_main.update()
    player.update()
    player.move()

    for sprite in all_sprites:
        display.blit(sprite.surf, sprite.rect)
    
    # Fin
    clock.tick(fps)
    pygame.display.update()