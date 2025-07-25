import os
import shutil
import subprocess
from pathlib import Path as pathlib
from glob import glob
from .system_util import (
    get_system,
    view_echo
)


def get_path(path='', system=get_system()):
    '''Comprobar o hacer que una carpeta termine con su slash correspondiente.'''
    path_fin = ''
    if system == 'linux':
        path_fin = '/'

    elif system == 'win':
        path_fin = '\\'

    if path == '':
        if system == 'win':
            path = (
                os.path.join( os.path.join(os.environ['USERPROFILE']), 'Desktop' )
            )
        elif system == 'linux': 
            path = view_echo( "$HOME" )
        else: pass

    try: path_laststr = path[-1]
    except: path_laststr = path_fin
    if path_laststr == path_fin: pass
    else:        
        path = path + path_fin

    return path


def get_name(name=''):
    '''Elegir el nombre de un archivo'''
    if name == '':
        name ='No_name'
    else: pass

    return name


def list_files(files='*', path='./', remove_path=False):
    '''Te lista los archivos existentes en una ruta espaficada'''
    # Buscar archivos
    search_files = sorted(
        pathlib(path)
        .glob(files)
    )
    
    # Agregar los archivos buscados a una lista
    files_list = []
    for file_text in search_files:
        # Convertir el objeto pathlib a str
        file_text = str( pathlib(file_text) )

        # Remplazar o no el path
        if remove_path == True:
            file_text = file_text.replace(path, '')
        else:
            pass
        
        # Agregar el archivo a la lista de archivos
        files_list.append( file_text )
    
    return files_list
    
    


def create_directory(file_dir='') -> bool:
    '''Crear una carpeta o varias carpetas'''

    if os.path.isdir(file_dir):
        # Carpeta ya existente, por lo tanto no se creara.
        return True
    
    else:
        # Intentar Crear carpeta, porque no existe
        try:
            # Separador de slash
            if get_system() == 'linux':
                slash = '/'
            elif get_system() == 'win':
                slash = '\\'
            else:
                pass
            
            # Separar Carpetas basado en los slash
            dir_ready = ''
            for text_dir in file_dir.split(slash):
                dir_ready += f'{text_dir}{slash}'
                
                if os.path.isdir(dir_ready):
                    # Si existe la carpeta
                    pass
                else:
                    # Si no existe la carpeta
                    os.mkdir(dir_ready)

            return True
        except:
            return False




def copy_files(source='', destiny='') -> bool:
    from distutils.dir_util import copy_tree # Por files copy
    '''Copia archivos a una ruta especificada'''
    
    return_value = False
    
    # Detectar si es una carpeta
    if os.path.isdir(source):
        destiny = f'{get_path(destiny)}{source}'
        create_directory(file_dir=destiny)
        copy_tree(source, destiny)
    # Detectar si es un archivo
    elif os.path.isfile(source):
        shutil.copy(source, destiny)
    else:
        return_value = False
    
    return return_value



def create_shortcut(
        name='',
        version=1.0,
        execute='',
        path_base='',
        categories=[''],
        comment='',
        icon='',
        terminal=False,
        path_shortcut=''
    ) -> bool:
    '''Para crear un acceso directo.'''
    
    '''Recuerda que el parametro execute, se refiere a la aplicación que quieras ejecutar, por medio del acceso directo.
    
    Y path_shortcut, se refiere a la ruta de cración del acceso directo. Podriamos decir que es un parametro opcional, ya que la mayoria de veces, es mejor dejarlo sin llenar.

    Pide como parametros:
        version=float,
        name=str,
        execute=str,
        path=str,
        categories=list[str],
        comment=str,
        icon=str,
        terminal=bool,
        path_shortcut=str
    '''
    return_value = False

    # Si existe el path y entonces se seguira
    if pathlib(path_base).exists():
        # Si existe la aplicación, entonces se sigue
        go = True
        
        # Verificar la existencia del nombre
        if name == '':
            name = 'NoName'
        else:
            pass
            
        # Verificar que la version sea un float
        if type(version) is float:
            pass
        else:
            version=1.0
        
        # Verificar que el icono exista
        if pathlib(icon).exists():
            pass
        else:
            icon = icon#''
            
        # Verificar que las categorias sean una lista
        if type(categories) is list:
            pass
        else:
            categories = ['']
            
        # Verificar que el parametro terminal sea un boleano
        if type(terminal) is bool:
            if get_system() == 'linux':
                # Solo en linux
                if terminal == True:
                    terminal = 'true'
                else:
                    terminal = 'false'
            else:
                pass
        else:
            terminal = False

    else:
        # Si no existe el path y el app no se seguira
        go = False

    
    # Si se cumplen los requisitos, para crear el acceso directo
    if go == True:
        # Poner la lista de categorias en una variable tipo str
        categories_ready = ''
        for categorie in categories:
            categorie = str(categorie)
            categories_ready += categorie
            if categorie == '':
                pass
            else:
                categories_ready += ';'
        categories_ready = categories_ready.replace('\n','')
        
        # Verificar o establecer el path necesario para el acceso directo
        if path_shortcut == '':
            if get_system() == 'linux':
                path_shortcut = view_echo(
                    text='$HOME/.local/share/applications/'
                )
            elif get_system() == 'win':
                path_shortcut = view_echo(
                    '%USERPROFILE%'
                    '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\'
                )
            else:
                pass
        else:
            pass
        if pathlib(path_shortcut).exists():
            pass
        else:
            create_directory( path_shortcut )

        # Texto necesario para el acceso directo
        if get_system() == 'linux':
            type_shortcut = '.desktop'
        
            text_shortcut = (
                '[Desktop Entry]\n'
                'Encoding=UTF-8\n'
                'Type=Application\n'
                f'Version={version}\n'
                f'Name={name}\n'
                f'Comment={comment}\n'
                f'Icon={path_base}{icon}\n'
                f'Exec={execute}\n'
                f'Path={path_base}\n'
                f'Terminal={terminal}\n'
                f'Categories={categories_ready}'
            )
        elif get_system() == 'win':
            type_shortcut = '.vbs'

            if terminal == True:
                with open(f'{get_path(path_base)}{name}.bat', 'w') as text_exec:
                    text_exec.write(
                        '@echo off\n'
                        f'{execute}\n'
                        'pause'
                    )
                execute = f'{name}.bat'

            else:
                pass
        
            text_shortcut = (
                # Objeto para acceder a la shell
                'Set objShell = WScript.CreateObject("WScript.SHell")\n\n'

                # Objeto shortcut - Crear acceso directo
                'Set objshortcut = objShell.CreateShortcut'
                f'("{path_shortcut}{name}.Lnk")\n'
                
                # Objeto shortcut - Aplicacion a ejecutar
                '    objshortcut.TargetPath = '
                f'"{get_path(path_base)}{execute}"\n'
                
                # shortcut - Parametro de carpeta de trabajo
                f'    objshortcut.WorkingDirectory = "{path_base}"\n'
                
                # DierctAccess - Parametro de comentario
                f'    objshortcut.Description = "{comment}"\n'
                
                # shortcut - Parametro de icono
                '    objshortcut.IconLocation = '
                f'"{get_path(path_base)}{icon}"\n\n'
                
                # Fin, para guardar el acceso directo
                'objshortcut.Save'
            )
        else: pass
            
        
        # Establecer el acceso directo, con el path y el name indicados
        # Tambien darle permisos de ejecución
        shortcut = name + type_shortcut
        
        if get_system() == 'linux':
            with open(
                path_shortcut + shortcut,
                'w'
            ) as shortcut_ready:
                shortcut_ready.write(text_shortcut)

            os.system(f'chmod +x "{path_shortcut + shortcut}"')
            
            return_value = True

        elif get_system() == 'win':
            with open(shortcut, 'w') as shortcut_ready:
                shortcut_ready.write(text_shortcut)
        
            os.system(f'"{shortcut}"')
            #os.remove(shortcut)
            
            return_value = True
        else:
            pass
        
    # Si no se cumple los requisitos, entonces no se hace nada
    else:
        pass
    
    
    return return_value