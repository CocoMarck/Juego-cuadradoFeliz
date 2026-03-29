from entities.pygame.object_with_physics import ObjectWithPhysics

class ObjectWithHappyPhysics(ObjectWithPhysics):
    '''
    La furza de gravedad, es por px's por segundo.
    Es decir, cada 1 segundos, el player se movera `x pixles`.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__( *args, vertical_force_hint=20, vertical_force_limit_hint=40, **kwargs )
