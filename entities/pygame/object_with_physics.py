import pygame
from .game_object import GameObject
from core.pygame.physics_utils import collide_and_move

class ObjectWithPhysics(GameObject):
    '''
    La furza de gravedad, es por px's por segundo.
    Es decir, cada 1 segundos, el player se movera `x pixles`.
    '''
    def __init__(self, *args, vertical_force_hint: int=None, vertical_force_limit_hint: int=None, **kwargs):
        super().__init__( *args, **kwargs )

        # Constantes
        self._SPAWN_VERTICAL_FORCE = max(self.rect.size)*vertical_force_hint if vertical_force_hint else max(self.rect.size)*60
        self._SPAWN_VERTICAL_FORCE_LIMIT = max(self.rect.size)*vertical_force_limit_hint if vertical_force_limit_hint else max(self.rect.size)*120

        # Gravedad
        self.vertical_force_limit = self._SPAWN_VERTICAL_FORCE_LIMIT
        self.vertical_force = self._SPAWN_VERTICAL_FORCE

        # Detección de colision en el piso.
        self.air_dt_count = 1
        self.collision_side = {}


    def apply_gravity(self, dt:float):
        '''
        En dalta time.
        Cada segundo se mueve `self.current_vertical_force` pixeles.
        `vertical_force` se acumula; Es relativo, por lo que la fuerza debe medirse en cada acumulación por segundo.

        # Recomendación.
        Cada 1 segundo se mueva: 10 rect max(size). Y como maximo 30 max(size)
        '''
        self.moving_xy[1] += self.vertical_force*dt
        if self.moving_xy[1] > self.vertical_force_limit:
            self.moving_xy[1] = self.vertical_force_limit


    def collide_and_move(self, dt: float, solid_objects: list):
        '''
        Colisionar con objeto solido y moverse.
        '''
        move_x = round(self.moving_xy[0] * dt)
        move_y = round(self.moving_xy[1] * dt)
        return collide_and_move(
            self.rect, (move_x, move_y), solid_objects
        )

    def on_the_ground(self):
        return (
            self.air_dt_count <= 0.1 and
            self.moving_xy[1] >= 0
        )

    def jump(self, force):
        self.moving_xy[1] = -force

    def update_state(self):
        '''
        Defaults states.
        '''
        move = self.moving_xy[0] != 0
        prefix = "idle"
        if move:
            prefix = 'move'
        self.state = prefix

        if self.moving_xy[1] < 0:
            self.state = f'jumping-{prefix}'
        elif not self.on_the_ground():
            self.state = f'falling-{prefix}'

    def update(self, dt=1, solid_objects: pygame.sprite.Group=[] ):
        self.apply_gravity(dt)

        self.air_dt_count += dt

        self.collision_side = self.collide_and_move( dt=dt, solid_objects=solid_objects )

        #if not (self.collision_side['left'] or self.collision_side['right']):
        if self.collision_side['bottom']:
            self.moving_xy[1] = 0
            self.air_dt_count = 0
        if self.collision_side['top']:
            self.moving_xy[1] = 0

        self.update_state()




