from controllers.language_controller import get_text
from controllers.cf_info import *
from controllers.cf_controller import *
from core.pygame.cf_util import all_images

from views.interface.interface_number import *
from views.interface.css_util import *
import main_map

import sys, os
from functools import partial
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QMessageBox,
    QInputDialog,

    QLineEdit,
    QLabel,
    QPushButton,
    QComboBox,

    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt




class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle('Cuadarado Feliz')
        self.setWindowIcon( QIcon( str(all_images['icon']) ) )
        self.resize( nums_win_dialog[0], nums_win_dialog[1] )
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout( vbox_main )
        
        # Sección Vertical seleccion de mapa
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
       

        self.combobox_map = QComboBox(self)
        self.update_list_of_maps()
        hbox.addWidget(self.combobox_map)
        
        hbox.addStretch()
        
        button = QPushButton( 'del' )
        button.clicked.connect( partial(self.select_map, 'del' ) )
        hbox.addWidget(button)

        button = QPushButton( 'edit' )
        button.clicked.connect( partial(self.select_map, 'edit' ) )
        hbox.addWidget(button)
        
        # Sección vertical editline botones | Editar Mapa | Crear mapa
        hbox = QHBoxLayout()
        
        label = QLabel("path")
        hbox.addWidget(label)
        self.combobox_path = QComboBox(self)
        for path in ["custom"]:
            self.combobox_path.addItem( path )
        hbox.addWidget(self.combobox_path)
        
        label = QLabel("name")
        hbox.addWidget(label)
        self.entry_name = QLineEdit()
        hbox.addWidget(self.entry_name)
        
        label = QLabel("size-xy")
        hbox.addWidget(label)
        self.combobox_size_xy = QComboBox()
        for size in [ "64x32", "64x64", "72x72", "128x128" ]:
            self.combobox_size_xy.addItem( str(size) )
        hbox.addWidget(self.combobox_size_xy)
        
        button = QPushButton( 'create_map' )
        button.clicked.connect( self.create_map )
        hbox.addWidget( button )
        
        vbox_main.addLayout(hbox)
        
        # Mostrar todo
        self.show()
    
    def update_list_of_maps(self):
        self.combobox_map.clear()
        for level in get_level_list():
            item_level = level.replace(dir_maps, '' )
            if ( item_level.replace('/', '') ).startswith( 'custom' ):
                self.combobox_map.addItem( item_level )
            else:
                self.combobox_map.addItem( item_level )
    



    def select_map( self, option='edit' ):
        print( f'Mapa seleccionado: {self.combobox_map.currentText()}' )
        
        YesNo = QMessageBox.question(
            self,
            'Continuar', # Titulo de mensaje
            
            '¿Quieres continuar?',
            
            QMessageBox.StandardButton.Yes |    # Boton si
            QMessageBox.StandardButton.No       # Boton no
        )
        if YesNo == QMessageBox.StandardButton.Yes:
            level = dir_maps + self.combobox_map.currentText()
            if option == 'edit':
                print("edit")
                print(level)

                main_map.run( level=level )
                self.update_list_of_maps()
                self.close()
            elif option == 'del':
                print("del")
                #os.remove( level )
                self.update_list_of_maps()
            
        else:
            pass




    def create_map(self):
        name = self.entry_name.text()
        path = self.combobox_path.currentText()
        
        size_xy = self.combobox_size_xy.currentText().split('x')
        for x in range( 0, len(size_xy) ):
            size_xy[x] = int( size_xy[x] )
        
        # Crear mapa
        if isinstance(name, str) and (not name == ''):
            main_map.run( 
                level=self.entry_name.text(), path=self.combobox_path.currentText(), size_xy=size_xy,
                with_limit=True, create_map=True
            )
            self.update_list_of_maps()
        else:
            # Mensaje de que no se pudo crear el mapa por falta de parametros
            pass




# Bucle y Estilo de programa
qss_style = ''
for widget in get_list_text_widget( 'Qt' ):
    qss_style += text_widget_style(
        widget=widget, font=None, font_size=num_font,
        margin_xy=num_margin_xy, padding=num_space_padding, idented=4
    )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss_style)
    window = Window_Main()
    sys.exit( app.exec() )