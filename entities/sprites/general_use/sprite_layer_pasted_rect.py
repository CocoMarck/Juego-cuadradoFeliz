import pygame
from .sprite_pasted_rect import SpritePastedRect




class SpriteLayerPastedRect( ):
    '''
    Un objeto que contiene varios objetos SpritePastedRect
    Su función es tener entre una capa/layer a muchos capas/layers de sprites.
    
    rect_pasted, es un pygame.Rect, obtiene sus coordenadas xy
    layer, es una lista de SpritePastedRect
    '''
    def __init__(
        self, rect_pasted, transparency=255, layer=[], difference_xy=[0,0]
    ):  
        # Atributos necesarios
        self.transparency_layer = transparency
        self.difference_xy = difference_xy
        self.rect_pasted = rect_pasted

        # Atributos de las capas | Agregar capas
        self.surf_layer = layer
        self.layer = []
        self.set_layer()

        # Rotar
        self.angle = 0
        self.flip_x = False
        self.flip_y = False


    def set_layer(self):
        '''
        Establecer capas
        '''
        self.layer = []
        for surf in self.surf_layer:
            sprite = SpritePastedRect(
             surf=surf, rect_pasted=self.rect_pasted, difference_xy=self.difference_xy
            )
            sprite.transparency = self.transparency_layer
            sprite.set_transparency()
            self.layer.append( sprite )

    def set_attributes_to_layer(self):
        '''
        Establecer atibutos a todas las capas
        '''
        for sprite in self.layer:
            sprite.flip_x = self.flip_x
            sprite.flip_y = self.flip_y
            sprite.angle = self.angle

    def set_surf(self):
        '''
        Establecer superficie a todas las capas
        '''
        self.set_attributes_to_layer()
        for sprite in self.layer:
            sprite.set_surf()

    def rotate(self):
        '''
        Rotar todas las capas
        '''
        self.set_attributes_to_layer()
        for sprite in self.layer:
            sprite.rotate()
    
    def add_to_sprite_group(self, group):
        '''
        Agregar a grupo de sprites
        '''
        for sprite in self.layer:
            group.add(sprite)
    
    def add_to_layer_group(self, group, layer=0):
        '''
        Agregar a grupo de layer
        '''
        for sprite in self.layer:
            group.add(sprite, layer=layer)
    
    def rm_layer(self):
        '''
        Eliminar todos los layer
        '''
        for sprite in self.layer:
            sprite.kill()
        

    def set_transparency_layer(self):
        '''
        Establecer transparencia a todos los layers. Todas las capas
        '''
        for sprite in self.layer:
            sprite.transparency = self.transparency_layer
    
    def update_layer(self):
        '''
        Acomodar todos los layer
        '''
        for layer in self.layer:
            layer.update()
