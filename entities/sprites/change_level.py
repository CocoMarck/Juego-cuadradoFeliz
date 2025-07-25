import pygame, os
from core.pygame.pygame_util import generic_colors
from controllers.cf_info import pixel_space_to_scale, dir_maps
from core.pygame.cf_util import get_image

class ChangeLevel(pygame.sprite.Sprite):
    def __init__(
        self, level=None, dir_level=None, position=(0,0), gamecomplete=False,
        transparency_collide=255, transparency_sprite=255, layer_all_sprites=None, level_objects=None
    ):
        super().__init__()
        
        # Transparencia
        self.transparency_collide = transparency_collide
        self.transparency_sprite = transparency_sprite

        # ...
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
        size = (pixel_space_to_scale, pixel_space_to_scale)

        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        if gamecomplete == True:
            self.surf.fill( generic_colors('green', transparency=self.transparency_collide) )
        else:
            self.surf.fill( generic_colors('black', transparency=self.transparency_collide) )
        self.rect = self.surf.get_rect( topleft=position )
        layer_all_sprites.add(self, layer=2)
        level_objects.add(self)
        
        # Sprite
        sprite = pygame.sprite.Sprite()
        
        if gamecomplete == True:
            sprite.surf = get_image( 
                'level_change', size=size, color=[0, 48, 0], transparency=self.transparency_sprite
            )
        else:
            sprite.surf = get_image( 
                'level_change', size=size, color=[39, 28, 18], transparency=self.transparency_sprite
            )

        sprite.rect = sprite.surf.get_rect( topleft=position )
        layer_all_sprites.add(sprite, layer=1)
    
    def update(self):
        if self.change_level == True:
            self.level = os.path.join( dir_maps, self.dir_level, self.name )
            if self.__gamecomplete == True:
                self.gamecomplete = True