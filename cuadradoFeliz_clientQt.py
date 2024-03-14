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
        
        button_controls = QPushButton( 'Controles' )
        button_controls.clicked.connect( self.evt_get_controls )
        vbox_main.addWidget( button_controls )
        

        # Seccion Vertical - SpinBox - Establecer volumen
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
        
        label = QLabel( 'Nivel' )
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
        button_get_gamecomplete = QPushButton( 'Juegos completados' )
        button_get_gamecomplete.clicked.connect( self.evt_get_gamecomplete )
        vbox_main.addWidget( button_get_gamecomplete )
        
        
        # Sección vertical | Boton | Creditos
        vbox_main.addStretch()
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
            'Controles', # Titulo
            'Flechas y espacio' # Información
        )
    
    def evt_set_volume(self, value):
        # Establecer volumen en el archivo CF_data
        # Preparar el valor entero a decimal. Dividiendolo entre 100
        CF_data.set_volume( volume=value/self.__volume_multipler )
    
    def evt_set_music(self, checked):
        # Establecer sonido de musica o no
        self.button_bool_music.setChecked( checked )
        if checked == True:
            self.button_bool_music.setText( 'Activada | Musica ' )
        else:
            self.button_bool_music.setText( 'Desactivado | Musica' )
        CF_data.set_music( music=checked )
            
    def evt_set_climateSound(self, checked):
        # Establecer sonido de clima o no
        self.button_bool_climateSound.setChecked( checked )
        if checked == True:
            self.button_bool_climateSound.setText( 'Activado | Sonido de Fondo ' )
        else:
            self.button_bool_climateSound.setText( 'Desactivado | Sonido de Fondo ' )
        CF_data.set_climate_sound( climate_sound=checked )
    
    def evt_set_level(self):
        # Establecer nivel
        CF_data.set_level( 
            level=f'{CF_data.dir_maps}{self.combobox_set_level.currentText()}' 
        )
    
    def evt_set_disp(self):
        # Establecer la resolución seleccionada
        disp_xy = self.combobox_set_resolution.currentText().split('x')
        CF_data.set_disp( width=disp_xy[0], height=disp_xy[1] )
    
    def evt_get_gamecomplete(self):
        # Mostrar todos los juegos completados
        # Si no existen juegos completados, se indicare mediante un mensaje.
        text_ready = ''
        if self.__gamecomplete == True:
            for gamecomplete in CF_data.get_gamecomplete():
                text_ready += (
                    f'Nivel: {gamecomplete[0]} | {Lang("score")}: {gamecomplete[1]}\n'
                )
        else:
            text_ready = 'No hay juegos completados'
        
        QMessageBox.information(
            self,
            'Juegos completados', #Titulo
            text_ready # Texto
        )

    def evt_credits(self):
        QMessageBox.information(
            self,
            Lang('credits'), # Titulo
            'Jean Abraham Chacón Candanosa @CocoMarck' # Texto
        )



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Main()
    sys.exit( app.exec() )