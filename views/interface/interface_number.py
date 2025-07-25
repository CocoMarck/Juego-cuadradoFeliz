'''
Este modulo es para información numerica relacionada con la interfaz.
Por ejemplo:
Valores xy de dimenciónes de ventana.
Valores xy de para fuente de texto.
Valores xy de para iconos.
'''
from core.display_number import *


# Establecer dimenciones de windegts y ventana
# Limite de resolucion: Anchura y altura de 480px como minimo.
num_font = get_display_number(divisor=120)
num_space_padding = int(num_font/4)
num_margin_xy = [num_font//4, num_font//8]

nums_win_main = [
    get_display_number(multipler=0.275, based='width'),
    get_display_number(multipler=0.5, based='height')
]

nums_win_dialog = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.15, based='height')
]