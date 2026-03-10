from .sticky_sprite import StickySprite
from controllers.pygame.animation_controller import AnimationController
import pygame

class AnimatedStickySprite(StickySprite):
    '''
    Usando un controller, establece el cambio de frames, remplazando surf dependiendo del parametro `state` de update.

    > Se supone que ya deben estar los estados left, right, etc. Con images ya con flip.
    '''
    def __init__(
        self, *args,
        animation_controller: AnimationController = None,
        states_to_rotate_x: list = [], states_to_rotate_y: list = [],
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.animation_controller = animation_controller

        self.states_to_rotate_x = states_to_rotate_x
        self.states_to_rotate_y = states_to_rotate_y



    def update(self, dt):
        self.animation_controller.update(dt, self.game_object.state)

        frame = self.animation_controller.get_current_frame().copy()
        self.surf = pygame.transform.flip( frame, self.game_object.flip_x, self.game_object.flip_y)
