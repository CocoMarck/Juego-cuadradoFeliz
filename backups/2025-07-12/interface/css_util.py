'''
Modulo con funciones relacionadas con los estilos CSS.
'''
def get_list_text_widget( option='Qt' ) -> list:
    '''Listar los widgets de un determinado framework'''
    if option == 'Qt':
        list_text_widget = [
            'Label',
            'ComboBox',
            'LineEdit',
            'PushButton',
            'TextEdit',
            'CheckBox'
        ]
        number = 0
    elif option == 'Gtk':
        list_text_widget = [
            'button',
            'label',
            'combobox',
            'entry',
            'textview',
            'checkbutton'
        ]
        

    # Devolver la lista
    for index in range(0, len(list_text_widget) ):
        if option == 'Qt':
            list_text_widget[index] = f'Q{list_text_widget[index]}'
        elif option == 'Gtk':
            list_text_widget[index] = list_text_widget[index].lower()

    return list_text_widget




def text_widget_style( 
    widget=str, font=str, font_size=int, margin_based_font=bool, 
    margin_xy=list, padding=int, idented=0
    ) -> str:
    '''Obtener estido para el widget. Tipo CSS'''
    text = ''

    # Establecer si se pondran corchetes o no {}
    # Inicio de corchete (solo si shell esta en true)
    shell = False
    if type(widget) == str:
        shell = True
        text += widget
        text += ' {\n'

    # Establecer el espacio de indentado
    space = ''
    if idented > 0:
        for x in range(0, idented):
            space += ' '


    # Agregar o no parametros
    # Fuente de texto y su tamaño
    if isinstance(font, str):
        text += f'{space}font-family: {font};\n'

    if isinstance(font_size, int):
        text += f'{space}font-size: {font_size}px;\n'

    # Margen xy
    set_margin = False
    if type(margin_xy) == list:
        if len(margin_xy) == 2:
            if (
                (type(margin_xy[0]) == int or float) and
                (type(margin_xy[1]) == int or float)
            ):
                set_margin = True
                margin_xy = [int(margin_xy[0]), int(margin_xy[1])]

    elif type(margin_based_font) == bool:
        if type(font_size) == int:
            set_margin = True
            margin_xy = [int(font_size/2), int(font_size/4)]

    if set_margin == True:
        if margin_xy[0] <= 0:
            margin_xy[0] = 1
        if margin_xy[1] <= 0:
            margin_xy[1] = 1
            
        text += (
            f'{space}margin-left: {margin_xy[0]}px;\n'
            f'{space}margin-right: {margin_xy[0]}px;\n'
            f'{space}margin-top: {margin_xy[1]}px;\n'
            f'{space}margin-bottom: {margin_xy[1]}px;\n'
        )

    # Size adicional para el widget
    if isinstance(padding, int):
        text += f'{space}padding: {padding}px;\n' # Size adicional para el widget


    # Cierre de corchete
    if shell == True:
        text += '}\n'


    # Devolver texto
    return text
