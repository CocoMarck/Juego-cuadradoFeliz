class AnimationController:
    '''
    animations. Dict con keys de animacines. Almanecaran tupla, con frames y numero flotante.
    - list: Los items seran pygame.Surface
    - float: Representara la duración de cada frame.

    Ejemplo:
    { 'idle': ( [surf1, surf2, surf3], 0.1 ) }
    '''
    def __init__(self, animations: dict, state: str ):
        self.animations = animations
        self.current_state = state
        self.current_frame_index = 0
        self.time_accumulator = 0

    def update(self, dt: float, state: str ):
        # Cambiar animación si el estado cambíio
        if state != self.current_state:
            self.current_state = state
            self.current_frame_index = 0
            self.time_accumulator = 0

        # Avanzar frames solo si la animación tiene mas de un frame.
        frames, frame_duration = self.animations[state]
        if len(frames) > 1:
            self.time_accumulator += dt
            if self.time_accumulator >= frame_duration:
                self.current_frame_index = (self.current_frame_index + 1) % len(frames)
                self.time_accumulator = 0

    def get_current_frame(self):
        # Obtener imagen actual.
        frames, _ = self.animations[self.current_state]
        return frames[self.current_frame_index]
