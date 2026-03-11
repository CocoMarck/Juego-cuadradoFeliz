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




def calculate_aspect_ratio( resolution_xy:tuple ):
    width, height = resolution_xy
    x_integer_divisors = []
    y_integer_divisors = []
    for divisor in range(1, width):
        value = float(width / divisor)
        if value.is_integer():
            x_integer_divisors.append( value )

    for divisor in range(1, height):
        value = float(height / divisor)
        if value.is_integer():
            y_integer_divisors.append( value )

    # Obtener coincidencia entre divisores en xy.
    good_divisors = []
    for x in x_integer_divisors:
        if x in y_integer_divisors:
            good_divisors.append( x )

    # Obtener el divisor mas grande coincidente.
    if len(good_divisors) > 0:
        divisor_for_aspect_ratio = max(good_divisors)

        aspect_ratio_x = width / divisor_for_aspect_ratio
        aspect_ratio_y = height / divisor_for_aspect_ratio

        return (aspect_ratio_x, aspect_ratio_y)
    else:
        return (width, height)
