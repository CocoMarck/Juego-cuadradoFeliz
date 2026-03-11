import pygame

from core.pygame.angle_utils import normalize_angle

class GameObject(pygame.sprite.Sprite):
    '''
    Objeto de juego con los atributos necesarios para eventos básicos del juego.
    Evitar wrappers, para esto tendremos que tener claro que funciones tienen los objetos: `pygame.Surface` `pygame.Rect`.

    `self.surf` tiene pa:
        - `get_alpha()`, `set_alpha()`
    `set_spawn_alpha()`

    `get_volume`, `set_volume`, `set_spawn_volume`. Volumen de objeto.
    '''
    def __init__(
        self, name='object', group="generic", 
        surf: pygame.Surface = None, alpha=255, flip_x=False, flip_y=False, position=(0,0),
        volume=float(1), angle=int(0), state='idle'
    ):
        # Evitar hacer wrappers al surface o al rect, nada de eso.
        super().__init__()

        # Constantes
        self._SPAWN_POSITION = position
        self._SPAWN_VOLUME = volume
        self._SPAWN_ANGLE = angle
        self._SPAWN_ALPHA = alpha
        self._SURF_BASE = surf.copy()
        self._SPAWN_SIZE = surf.get_rect().size

        # Variables | Para sonido
        self._volume = volume

        # Variables | Relacionado con movimiento
        self.angle = angle
        self.moving_xy = [0,0]
        self.flip_x = flip_x
        self.flip_y = flip_y

        # Varialbes | Releciondas con herencia, o tipo de objeto
        self.name = name
        self.group = group

        # Estado
        self.state = state

        # Superficie
        self.surf = surf.copy()
        self.surf.set_alpha( alpha )
        self.rect = surf.get_rect( topleft=self._SPAWN_POSITION )

    def get_spawn_size(self):
        return self._SPAWN_SIZE

    def flip_surf(self):
        self.surf = pygame.transform.flip( self.surf, self.flip_x, self.flip_y )

    def build_surf(self):
        self.resize_surf()
        self.flip_surf()
        self.set_spawn_alpha()

    def build_rect( self, size ):
        self.rect.size = (size[0], size[1])

    def resize_surf(self):
        '''
        Escalar surf respecto a rect
        '''
        if self.surf.get_size() != self.rect.size:
            self.surf = pygame.transform.scale( self._SURF_BASE, self.rect.size )

    def resize_rect(self):
        '''
        Escalar rect respecto a surf.
        '''
        if self.surf.get_size() != self.rect.size:
            position = (self.rect.x, self.rect.y)
            self.rect = self.surf.get_rect( topleft=position )

    def set_spawn_position(self):
        self.rect.topleft = self._SPAWN_POSITION

    def set_spawn_alpha(self):
        self.surf.set_alpha( self._SPAWN_ALPHA )

    def set_spawn_rect(self):
        self.rect = self.get_rect( self._SPAWN_SIZE )

    def resize_with_multiplier( self, multiplier ):
        self.build_rect(
            (self._SPAWN_SIZE[0]*multiplier[0], self._SPAWN_SIZE[1]*multiplier[1])
        )
        self.build_surf()

    def set_spawn_state(self):
        self.set_spawn_position()
        self.set_spawn_rect()
        self.set_spawn_alpha()
        self.resize_surf()

    def rotate_surf(self):
        '''
        Rotar superficie
        '''
        self.angle = normalize_angle( self.angle )
        if self.angle != 0:
            self.build_surf()
            self.surf = pygame.transform.rotate( self.surf, self.angle )
            self.resize_rect()

    # Sonido
    def get_volume(self):
        return self._volume

    def set_volume(self, volume: float):
        if volume > 1:
            volume = float(1)
        elif volume < 0:
            volume = float(0)

        if isinstance(volume, float):
            self._volume = volume

    def set_spawn_volume(self):
        self.update_volume( self._SPAWN_VOLUME )


    def update(self, dt=1):
        # Update por defecto.
        self.rect.x += self.moving_xy[0]*dt
        self.rect.y += self.moving_xy[1]*dt

