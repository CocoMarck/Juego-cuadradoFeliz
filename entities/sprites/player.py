from .cf_sounds import *
from controllers.cf_info import pixel_space_to_scale
from core.pygame.cf_util import get_image, player_key
from .character import Character




class Player(Character):
    def __init__(
     self, size=pixel_space_to_scale, transparency_collide=255, transparency_sprite=255, 
     dict_sprite={
        'side-x' : get_image( 'player_move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] ),
        'side-y' : get_image( 'player_not-move', size=[pixel_space_to_scale*2,pixel_space_to_scale*2] )
     },  position=[0,0], limit_xy=[0,0], color_sprite=[153,252,152], 
     sprite_difference_xy=[0,-(pixel_space_to_scale//2)], player_objects:object=None, 
     solid_objects=None, damage_objects=None, level_objects=None, score_objects=None, jumping_objects=None,
     moving_objects=None, ladder_objects=None, particle_objects=None, anim_sprites=None,
     update_objects=None, layer_all_sprites=None
    ):
        
        super().__init__( 
         size=size, transparency_collide=transparency_collide, transparency_sprite=transparency_sprite,
         dict_sprite=dict_sprite, position=position, limit_xy=limit_xy, color_sprite=color_sprite,
         sprite_difference_xy=sprite_difference_xy, solid_objects=solid_objects, damage_objects=damage_objects, 
         level_objects=level_objects, score_objects=score_objects, jumping_objects=jumping_objects,
         moving_objects=moving_objects, ladder_objects=ladder_objects, particle_objects=particle_objects,
         anim_sprites=anim_sprites, update_objects=update_objects, layer_all_sprites=layer_all_sprites
        )
        
        self.change_level = True
        
        # Transparencia
        #...
        
        # Teclas de movimiento
        self.pressed_jump       = player_key['jump']
        self.pressed_left       = player_key['left']
        self.pressed_right      = player_key['right']
        self.pressed_up         = player_key['up']
        self.pressed_down       = player_key['down']
        self.pressed_walk       = player_key['walk']
        self.pressed_action     = player_key['action']
        
        # Grupo de sprites
        player_objects.add(self)
    
    
    def move(self):
        # Movimiento | Funcion que se encarga de saber si se han percionado las Teclas de movimiento
        pressed_keys = pygame.key.get_pressed()

        self.left = pressed_keys[self.pressed_left]
        self.right = pressed_keys[self.pressed_right]
        self.up = pressed_keys[self.pressed_up]
        self.down = pressed_keys[self.pressed_down]
        self.walk = pressed_keys[self.pressed_walk]
        if pressed_keys[self.pressed_jump]:
            self.set_and_jump( multipler=1 )
        self.action = pressed_keys[self.pressed_action]