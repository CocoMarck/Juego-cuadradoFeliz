MAXIMUM_ROTATION_ANGLE = 360
MINIMUM_ROTATION_ANGLE = -360


def normalize_angle(angle: int):
    '''
    Función que normaliza valor de angulo, no mas de 360 grados, y no menos de la iversa de 360 grados.
    '''
    # Establecer limite valor minimo y maximo de angulo de rotación a: 360 y -360
    if angle > MAXIMUM_ROTATION_ANGLE or angle < MINIMUM_ROTATION_ANGLE:
        return 0

    return angle
