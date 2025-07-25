from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import *


class Sun( pygame.sprite.Sprite ):
    def __init__( 
        self, size=[16, 16], color=generic_colors('yellow'), divider=16, 
        start_with_max_power=True, time=0, display=[1920,1080], 
        anim_sprites=None, lighting_objects=None, nocamera_back_sprites=None
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
