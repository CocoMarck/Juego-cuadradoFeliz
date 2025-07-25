'''
Este modulo, es para funciones relacionadas con la los valores xy de la resolucion de pantalla.
'''
from .system_util import get_display_resolution

display=get_display_resolution()

def get_display_number(multipler=0, divisor=0, based='width', display=display) -> int:
    '''Obtener un numero basado en la resolución de pantalla'''
    if based == 'width':
        base = display[0]
    else:
        base = display[1]

    lim_max = int( max(display)*0.75 )
    lim_min = 8

    number = None
    if multipler > 0:
        number = base*multipler
    else:
        if divisor > 0:
            number = base/divisor

    if not number == None:
        if number > lim_max:
            return lim_max
        elif number < lim_min:
            return lim_min
        else:
            return int(number)