import pygame

# Objetos para uso general
class StandardSprite(pygame.sprite.Sprite):
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
        Si cambia de tamaño surf, volver a obtener rect. Volver a establecer posición
        '''
        old_position = (self.rect.x, self.rect.y)
        if self.surf.get_size() != self.rect.size:
            self.rect = self.surf.get_rect( topleft=old_position )
    
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
        self.set_transparency()
        
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
