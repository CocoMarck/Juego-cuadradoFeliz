#from .modulo_files import Path, Name
from core.system_util import (
    clean_screen, command_output, get_system
)




def get_text( text: str ):
    return text




DEFAULT_CONSOLE = True



def print_and_return( text: str = "", console: bool = DEFAULT_CONSOLE ):
    final_text = f"{text}\n"
    if console:
        print( final_text[:-1] )
    
    return final_text


def title(
    text=get_text('title'),
    character='#',
    space=4,
    console=DEFAULT_CONSOLE,
):
    '''
    Mostrar un Titulo
    
    Parametros:
    text=str
    # Texto titular
    
    character=str
    # Caracter, con la funcion de simbolo
    
    space=int
    # Numero de espacios, es decir:
    #   4 = '    '
    
    console=bool
    # False, Modo imprimir titulo sin devolver texto.
    # True, Devolver texto.
    '''
    
    
    # Establecer variables
    space = ' '*space
    text = f'{character}{space}{text}{space}{character}\n'
    
    # Print o String mode
    if console == True:
        # Imprimir texto
        print( text[:-1] )
    
    return text


def input_continue(
    text=f'¿{get_text("continue")}?',
    yes_no=[ get_text("y"), get_text("n") ],
    message_error=False
) -> bool | None:
    '''
    Mostrar un masaje para continuar o no.
    
    Parametros:
    text = str
    # Es el mensaje ¿Continuar?

    yes_no = list
    # Una lista así ['y', 'n']

    message_error = bool
    # Muestra un input de error, que se quita precionando enter.
    '''
    
    
    # Declarar variable, option
    option = None
    
    # Mostrar o no mensaje de error
    if message_error == True:
        # Se cancelara el continue loop
        loop = False

        # Se mostrara un input, que se quitara, precionando enter.
        #CleanScreen()
        print()
        if text == '':
            input(get_text('continue_enter') + '...')
        else:
            input(
                f'[ERROR] {text}\n' +
                get_text('continue_enter') + '...'
            )
        print()
        return None

    else:
        # Se activa el loop e continue
        loop = True

    # input_continue - Loop
    while loop == True:
        # Visual input, si o no
        # [:1] Es el primer caracter
        # lower() modo minusculas, upper() Modo Mayusculas
        option = input(
            f'{text} {yes_no[0]}/{yes_no[1]}: '
        )
        
        # Eleccion de opcion
        # lower() modo minusculas, upper() Modo Mayusculas
        if option == yes_no[0]:
            loop = False
            return True
        elif option == yes_no[1]:
            # Si la opcion es si o no, el loop para
            loop = False
            return False
        
        else:
            # Si la opcion es erronea, el loop sigue
            input_continue(text=option, message_error=True)


def separator(
    character = '-',
    number = 128,
    console = DEFAULT_CONSOLE
):
    '''
    Separador
    Muestra una serie de un solo caracter, tiene la funcion de separar textos.
    Te devuele un str.


    Parametros:
    character = str
    # Un simbolo/caracter, que se repetira por number
    
    number = int
    # Catidad de simbolos/caracteres.
    
    console = bool
    # Mostrar con print o no.
    '''
    separator = f'\n\n{character*number}\n\n'
    if console == True:
        print( separator[:-1] )

    return separator


def archive_path(text='Archivo'):
    title(f'{get_text("dir")} - {text}')
    cfg = Path(input(f'{get_text("set_dir")}: '))
    
    title(f'{get_text("name")} - {text}')
    cfg = cfg + Name(input(f'{get_text("name")}: '))
    
    return cfg




def text_box( text: str, character: str, text_type: str, console: bool = DEFAULT_CONSOLE):
    '''
    Muestra texto encerrado en ``` (character)
    '''
    final_text = f"\n{character}{text_type}\n{text}\n{character}\n\n"
    if console:
        print( final_text[:-1] )

    return final_text


def code_box( text: str = "Nothing", text_type: str = None, console: bool = DEFAULT_CONSOLE ):
    '''
    Muestra texto encerrado en ``` o en ~~~, dependiendo de text_type.
    '''
    character = "```"
    if text_type == None:
        text_type = ""
        character = "~~~"
    
    return text_box( text=text, character=character, text_type=text_type, console=console )


def command_box( command: str, show_entry: bool = True, console: bool = DEFAULT_CONSOLE ):
    '''
    Encierra en un `text_box`, la salida de un comando.
    '''
    final_text = ""
    if show_entry == True:
        final_text = f"**Command:** `{command}`"

    output = command_output( command )
    
    text_type = "bash"
    if get_system() == "win":
        text_type = "powershell"

    final_text += text_box( text=output, character="```", text_type=text_type, console=False)

    if console:
        print(final_text)

    return final_text