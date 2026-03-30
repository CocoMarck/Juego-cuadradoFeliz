from .object_with_happy_physics import ObjectWithHappyPhysics

class Character(ObjectWithHappyPhysics):
    def __init__( self, *args, hp=100, speed_hint: int=None, jump_force_hint:int=None,  **kwargs ):
        super().__init__( *args, **kwargs )

        self._SPANW_HP = hp
        self._SPAWN_JUMP_FORCE = (
            max(self.rect.size)*jump_force_hint if jump_force_hint else max(self.rect.size)*10
        )
        self._SPAWN_SPEED = (
            max(self.rect.size)*speed_hint if speed_hint else max(self.rect.size)*16
        )

        self.hp = self._SPANW_HP
        self.jump_force = self._SPAWN_JUMP_FORCE
        self.speed = self._SPAWN_SPEED
        self._WALKING_SPEED_MULTIPLIER = 0.5

        # Para moverse
        self.move_walk = False
        self.move_left = False
        self.move_right = False
        self.move_jump = False

    def get_speed(self, multiplier:float ):
        return self.speed * multiplier

    def get_running_speed(self):
        return self.get_speed(1)

    def get_walking_speed(self):
        return self.get_speed(self._WALKING_SPEED_MULTIPLIER)

    def jump_multiplier(self, multiplier=1 ):
        self.jump( self.jump_force*multiplier )

    def jump_on_the_ground(self, multiplier=1):
        if self.on_the_ground():
            self.jump_multiplier( multiplier=multiplier )

    def move(self):
        if self.move_walk:
            speed = self.get_walking_speed()
        else:
            speed = self.get_running_speed()

        if self.move_left:
            self.flip_x = True
            self.moving_xy[0] = -speed
        elif self.move_right:
            self.flip_x = False
            self.moving_xy[0] = speed
        else:
            self.moving_xy[0] = 0

        if self.move_jump:
            self.jump_on_the_ground()

    def update_state(self):
        '''
        Character move states
        '''
        move = self.moving_xy[0] != 0
        prefix = "idle"
        if move:
            prefix = 'move'
        self.state = prefix
        if move and self.move_walk:
            self.state += '-walk'

        if self.moving_xy[1] < 0:
            self.state = f'jumping-{prefix}'
        elif not self.on_the_ground():
            self.state = f'falling-{prefix}'
