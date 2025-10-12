import pygame
from .standard_sprite import StandardSprite


class SpritePastedRect(StandardSprite):
    '''
    Este objeto es heredado de SpriteStandar

    Este objeto tiene un metodo update, este metodo hace que se quede centralizado en el rect indicado en los parametros.
    
    Parametros:
    rect_pasted=collider, coordenadas de objeto a pegarse
    update_group=grupo en donde se añadira (opcional)
    
    Tiene el un metodo update, el cual permite que el sprite se pege al rect, a la posición.
    '''
    def __init__( 
        self, surf, rect_pasted, difference_xy=[0,0]
    ):  
        # Establecer parametros para SpriteStandar
        super().__init__( surf, surf.get_alpha(), rect_pasted.center )

        # Superficie
        self.rect_pasted = rect_pasted
        
        # Diferencia de centrado.
        self.center_difference_xy = difference_xy
    
    def paste_a_rectangle(self):
        '''
        Función: Dependencia necesaria
        '''
        # Si cambia de tamaño surf, volver a obtener rect.
        self.sync_size()
        
        # Centrar rect en el rect_pasted
        self.rect.center = self.rect_pasted.center
        
        # Agregar diferencia.
        self.rect.x += self.center_difference_xy[0]
        self.rect.y += self.center_difference_xy[1]

    def update(self):
        # Funcion por defecto para mover sprite
        self.paste_a_rectangle()
