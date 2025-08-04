from core.pygame.pygame_util import generic_colors
from core.pygame.cf_util import *
from .general_use.standard_sprite import StandardSprite
from .particle import Particle


class Bullet( StandardSprite ):
    def __init__( 
        self, size, position, image, speed_xy, time,
        particle_objects, solid_objects, damage_objects, jumping_objects, anim_sprites, layer_all_sprites, 
        particle_size=[0,0], damage=20
    ):
        # Grupos
        self.__particle_objects = particle_objects
        self.__solid_objects = solid_objects
        self.__damage_objects = damage_objects
        self.__jumping_objects = jumping_objects
        self.__anim_sprites = anim_sprites
        self.__layer_all_sprites = layer_all_sprites
        
        # Superficie de collider
        surf = pygame.Surface( size, pygame.SRCALPHA ) 
        surf.fill( [255, 255, 0] )
        self.damage = damage
    
        # Establecer parametros para SpriteStandar
        super().__init__( 
            surf, transparency=255, position=position
        )
        
        self.moving_xy = speed_xy
        self.time = time
        self.particle_size = particle_size
        
        # Agregar 
        layer_all_sprites.add( self, layer=3 )
        damage_objects.add(self)
        anim_sprites.add( self )
    
    def anim(self):
        # Mover bala
        self.time_count += 1

        self.movement()
        
        # Colisiones
        kill = False
        for solid_object in self.__solid_objects:
            if self.rect.colliderect(solid_object.rect):
                kill = True
        
        # Eliminar
        if self.time_over():
            self.kill()
        if kill:
            # Tamaño de particula
            if self.particle_size == [0,0]:
                size = [self.rect.height, self.rect.height]
            else:
                size = self.particle_size
            
            # Posicion correcta de particula
            if self.angle >= 0:
                position=[self.rect.x+self.rect.width -self.moving_xy[0], self.rect.y]
            else:
                position=[self.rect.x -self.moving_xy[0], self.rect.y]
            if self.moving_xy[1] < 0:
                position[1] -= self.moving_xy[1]
            if self.moving_xy[1] > 0:
                if self.moving_xy[0] > 0:
                    position[0] += self.moving_xy[0]
            
            # Generar particula
            Particle( 
                size=size, position=position, 
                transparency_collide=255, transparency_sprite=255, 
                color_collide=generic_colors('grey'), time_kill=data_CF.fps*0.5, sound=None,
                particle_objects=self.__particle_objects, solid_objects=self.__solid_objects,
                damage_objects=self.__damage_objects, jumping_objects=self.__jumping_objects, 
                anim_sprites=self.__anim_sprites, layer_all_sprites=self.__layer_all_sprites
            )
            self.kill()