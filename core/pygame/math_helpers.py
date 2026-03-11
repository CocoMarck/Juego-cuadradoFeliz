def resolution_scale_ratio( first_res: list, second_res: list, dividend="min" ):
    '''
    Cálcula la proporcion de escalado entre dos resoluciones. Obtener porcentaje de diferencia respecto a dos resoluciones. Sirve para escalar render a size de view/window. Y aun mantener click events.
    '''
    max_res = [ max( first_res[0], second_res[0] ), max( first_res[1], second_res[1] ) ]
    min_res = [ min( first_res[0], second_res[0] ), min( first_res[1], second_res[1] ) ]
    if dividend == "min":
        return [
            (min_res[0] / max_res[0]),
            (min_res[1] / max_res[1])
        ]
    elif dividend == "max":
        return [
            (max_res[0] / min_res[0]),
            (max_res[1] / min_res[1])
        ]


def axis_coord_porcentage( size, negative_start_counted, positive_start_counted, coord ):
    '''
    Calcula el porcentaje de una coordenada respecto al eje dado. Porcentaje de coordenada respecto a valor de eje.

    x: Distancia total.
    y: Coordenada actual.

    if x > y:
        (x -y) / x
    if y > x:
        ( (x -y) / x ) * -1
    '''
    multiplier = (size -(coord - positive_start_counted)) / size
    if coord < 0:
        multiplier = (-size - (coord +negative_start_counted) ) / -size
    return multiplier
