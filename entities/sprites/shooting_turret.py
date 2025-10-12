from controllers.cf_info import pixel_space_to_scale
from .general_use.multi_layer_sprite import MultiLayerSprite


class ShootingTurret(MultiLayerSprite):
    '''
    `aim`: determina a que disparar.
    `detection_multipler`: dtermina la distancia `xy` a la que se detecta un objetivo. Si esta en -1, lo detecta en cualquier lado.
    '''
    def __init__(
     self, size=pixel_space_to_scale, positon=[0,0], aim="all", detection_multipler=1,
     npc_objects, player_objects
    ):
        super().__init__( 
         surf=pygame.Surface( (size, size), pygame.SRCALPHA ), position=position,
         transparency=255, layer=[], layer_transparency=255, layer_difference_xy=[0,0]
        )
        
        self.objects_to_shoot = player_objects
        self.current_focus = None
        
        
    def set_current_approach(self):
        if self.current_focus == None:
            for obj in self.objects_to_shoot:
                self.current_focus = obj
                break