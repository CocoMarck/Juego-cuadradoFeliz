from Modulos.Modulo_Language import get_text as Lang
from Modulos.pygame import CF_data

import sys
from PyQt6.QtWidgets import(
    QApplication,
    QWidget,
    QDialog,
    QMessageBox,

    QLineEdit,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,

    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle('Cuadrado Feliz')
        #self.setWindowIcon( QIcon('ruta') )
        self.resize(384, -1)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        
        # Secciones Vertical - Boton - Inicio, Controles
        button_play = QPushButton( Lang('start') )
        button_play.clicked.connect( self.evt_start_game )
        vbox_main.addWidget( button_play )
        
        button_controls = QPushButton( Lang('ctrls') )
        button_controls.clicked.connect( self.evt_get_controls )
        vbox_main.addWidget( button_controls )
        

        # Seccion Vertical - SpinBox - Establecer volumen
        vbox_main.addStretch()

        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        label = QLabel('Volumen')
        hbox.addWidget(label)
        
        hbox.addStretch()
        
        self.__volume_multipler = 100
        current_volume = round( (CF_data.get_volume())*self.__volume_multipler )
        spinbox_volume = QSpinBox( 
            minimum=1, maximum=self.__volume_multipler,
            value=current_volume
        )
        spinbox_volume.valueChanged.connect( self.evt_set_volume )
        hbox.addWidget( spinbox_volume )
        
        
        # Seccion Vertical - Label - Fps establecidos
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)

        label = QLabel( Lang('fps') )
        hbox.addWidget(label)
        
        hbox.addStretch()
        
        label = QLabel( str(CF_data.get_fps()) )
        hbox.addWidget(label)
        
        
        # Sección Vertical - Boton alternable - Establecer escuchar musica o no
        self.button_bool_music = QPushButton()
        self.button_bool_music.setCheckable(True)

        self.evt_set_music( checked=CF_data.get_music() )

        self.button_bool_music.clicked.connect( self.evt_set_music )
        vbox_main.addWidget( self.button_bool_music )
        
        # Sección Vertical - Boton alternable - Establecer sonido de fondo o no
        self.button_bool_climateSound = QPushButton()
        self.button_bool_climateSound.setCheckable(True)
        
        self.evt_set_climateSound( checked=CF_data.get_climate_sound() )
        
        self.button_bool_climateSound.clicked.connect( self.evt_set_climateSound )
        vbox_main.addWidget( self.button_bool_climateSound )
        
        
        # Seccion Vertical - ComboBox - Nivel
        # Si el jugador ya completo el juego, se le permite seleccionar un nivel.
        # De lo contrario, no se le permite cambiar de nivel.
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        label = QLabel( Lang('lvl') )
        hbox.addWidget( label )
        
        hbox.addStretch()
        
        current_level = CF_data.get_level()
        self.combobox_set_level = QComboBox(self)
        self.combobox_set_level.addItem(
             current_level.replace( 
                CF_data.dir_maps, ''
             )
        )
        self.__gamecomplete = False
        if not CF_data.get_gamecomplete() == None:
            self.__gamecomplete = True
            for level in CF_data.get_level_list():
                if not level == current_level:
                    self.combobox_set_level.addItem( level.replace(CF_data.dir_maps, '') )
        self.combobox_set_level.activated.connect( self.evt_set_level )
        hbox.addWidget( self.combobox_set_level )
                

        # Sección Vertical - Boton alternable - Establecer ver collider o no
        if self.__gamecomplete == True:
            self.button_bool_show_collide = QPushButton()
            self.button_bool_show_collide.setCheckable(True)
        
            self.evt_set_show_collide( checked=CF_data.get_show_collide() )
        
            self.button_bool_show_collide.clicked.connect( self.evt_set_show_collide )
            vbox_main.addWidget( self.button_bool_show_collide )
        
        
        # Seccion Vertical - Combobox - Resolución
        # Establecer la resolución actual.
        # Y establecer resoluciones optimizadas para el juego.
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        label = QLabel( Lang('resolution') )
        hbox.addWidget( label )
        
        hbox.addStretch()

        self.combobox_set_resolution = QComboBox(self)
        current_resolution = CF_data.get_disp()
        self.combobox_set_resolution.addItem( f'{current_resolution[0]}x{current_resolution[1]}' )
        list_resolution_ready = [
            [1920, 1080],
            [1440, 810],
            [960, 540],
            [480, 270]
        ]
        for resolution in list_resolution_ready:
            if not resolution == current_resolution:
                self.combobox_set_resolution.addItem( f'{resolution[0]}x{resolution[1]}' )
        self.combobox_set_resolution.activated.connect(self.evt_set_disp)
        hbox.addWidget( self.combobox_set_resolution )
        

        # Sección vertical | Boton | Información de juegos completados
        vbox_main.addStretch()
        button_get_gamecomplete = QPushButton( Lang('completedGames') )
        button_get_gamecomplete.clicked.connect( self.evt_get_gamecomplete )
        vbox_main.addWidget( button_get_gamecomplete )
        
        
        # Sección vertical | Boton | Creditos
        button_credits = QPushButton( Lang('credits') )
        button_credits.clicked.connect( self.evt_credits )
        vbox_main.addWidget( button_credits )
        
        
        # Fin, Mostrar ventana y los widgets agregados en ella
        self.show()
    
    def evt_start_game(self):
        # Cerrar cliente, y abrir videojuego
        self.close()
        import cuadradoFeliz

    def evt_get_controls(self):
        # Mostrar los controles
        QMessageBox.information(
            self,
            Lang('ctrls'), # Titulo
            Lang('default_ctrls') # Información
        )
    
    def evt_set_volume(self, value):
        # Establecer volumen en el archivo CF_data
        # Preparar el valor entero a decimal. Dividiendolo entre 100
        CF_data.set_volume( volume=value/self.__volume_multipler )
    
    def evt_set_music(self, checked):
        # Establecer sonido de musica o no
        self.button_bool_music.setChecked( checked )
        if checked == True:
            self.button_bool_music.setText( f'{Lang("on")} | {Lang("music")}' )
        else:
            self.button_bool_music.setText( f'{Lang("off")} | {Lang("music")}' )
        CF_data.set_music( music=checked )
            
    def evt_set_climateSound(self, checked):
        # Establecer sonido de clima o no
        self.button_bool_climateSound.setChecked( checked )
        if checked == True:
            self.button_bool_climateSound.setText( f'{Lang("on")} | {Lang("climateSound")}' )
        else:
            self.button_bool_climateSound.setText( f'{Lang("off")} | {Lang("climateSound")}' )
        CF_data.set_climate_sound( climate_sound=checked )
    
    def evt_set_level(self):
        # Establecer nivel
        if self.__gamecomplete == True:
            CF_data.set_level( 
                level=f'{CF_data.dir_maps}{self.combobox_set_level.currentText()}' 
            )
    def evt_set_show_collide(self, checked):
        # Establecer si ver colliders o no
        self.button_bool_show_collide.setChecked( checked )
        if checked == True:
            self.button_bool_show_collide.setText( f'{Lang("on")} | {Lang("show_collide")}' )
        else:
            self.button_bool_show_collide.setText( f'{Lang("off")} | {Lang("show_collide")}' )
        CF_data.set_show_collide( show_collide=checked )
    
    def evt_set_disp(self):
        # Establecer la resolución seleccionada
        disp_xy = self.combobox_set_resolution.currentText().split('x')
        CF_data.set_disp( width=disp_xy[0], height=disp_xy[1] )
    
    def evt_get_gamecomplete(self):
        # Mostrar todos los juegos completados
        # Si no existen juegos completados, se indicare mediante un mensaje.
        
        # Establecer información de juegos completados
        # Establecer nombre del nivel en el diccionario
        text_ready = ''
        dict_gamecomplete = {}
        list_gamecomplete = CF_data.get_gamecomplete()
        if self.__gamecomplete == True:
            for gamecomplete in list_gamecomplete:
                text_ready += (
                    f'{Lang("lvl")}: {gamecomplete[0]} | {Lang("score")}: {gamecomplete[1]}\n'
                )
                dict_gamecomplete.update( {gamecomplete[0]:None} )
        else:
            text_ready = 'No hay juegos completados'
        
        # Record | Establecer en una lista los valores de score en el diccionario
        for key in dict_gamecomplete.keys():
            list_number = []
            for gamecomplete in list_gamecomplete:
                if key == gamecomplete[0]:
                    list_number.append( gamecomplete[1] )
                    dict_gamecomplete.update( {key:list_number} )

        # Record | Establecer el texto del record
        text_record = ''
        for key in dict_gamecomplete.keys():
            '''
            # Acomodar valores del record
            # Ordenar valores con el Metodo burbuja.
            # El valor mas alto sera el ultimo indice de la lista de valores.
            list_number = dict_gamecomplete[key]
            len_list_number = len(list_number)
            for index in range(len_list_number):
                for current_number in range(len_list_number-1):
                    next_number = current_number+1
                    
                    if list_number[current_number] > list_number[next_number]:
                        go_prev = list_number[current_number]
                        go_next = list_number[next_number]
                        list_number[current_number] = go_next
                        list_number[next_number] = go_prev
            print( key, dict_gamecomplete[key] )
            '''
            text_record += f"{Lang('lvl')}: {key} | {Lang('score')}: {max(dict_gamecomplete[key])}\n"

        if not text_record == '':
            text_ready = (
                f'{Lang("max_score")}:\n'
                f'{text_record}\n\n\n{text_ready}'
            )
        
        # Mostrar los juegos completados y su record
        QMessageBox.information(
            self,
            Lang('completedGames'), #Titulo
            text_ready # Texto
        )

    def evt_credits(self):
        # Creditos del juego
        QMessageBox.information(
            self,
            Lang('credits'), # Titulo
            CF_data.credits( share=True,jump_lines=True ) # Texto
        )



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Main()
    sys.exit( app.exec() )