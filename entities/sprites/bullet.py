from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import *
from .general_use.standard_sprite import StandardSprite


class Bullet( StandardSprite ):
    def __init__( self, size, position, image, speed_xy, time, layer_all_sprites, anim_sprites ):
        # Superficie de collider
        surf = pygame.Surface( size, pygame.SRCALPHA ) 
        surf.fill( [255, 255, 0] )
    
        # Establecer parametros para SpriteStandar
        super().__init__( 
            surf, transparency=255, position=position
        )
        
        self.moving_xy = speed_xy
        self.time = time
        
        # Agregar 
        layer_all_sprites.add( self, layer=3 )
        anim_sprites.add( self )
    
    def anim(self):
        # Mover bala
        self.time_count += 1

        self.movement()
        
        # Colisiones
        kill = False
        for solid_object in solid_objects:
            if self.rect.colliderect(solid_object.rect):
                kill = True
        
        # Eliminar
        if self.time_over() or kill == True:
            Particle( 
                size=[self.rect.height, self.rect.height], 
                position=[self.rect.x -self.moving_xy[0], self.rect.y-self.moving_xy[1]], 
                transparency_collide=255, transparency_sprite=255, 
                color_collide=generic_colors('grey'), time_kill=data_CF.fps*0.5, sound=None
            )
            self.kill()