from data.Modulo_Language import get_text as Lang
from data.CF_info import *
from data.CF_data import *

from interface.interface_number import *
from interface.css_util import *

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


# Detectar si el juego esta completado
if get_gamecomplete() == None:
    gamecomplete = False
else:
    gamecomplete = True



# Ventana
class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle('Cuadrado Feliz')
        #self.setWindowIcon( QIcon('ruta') )
        self.resize(nums_win_main[0], nums_win_main[1])

        self.__gamecomplete = gamecomplete
        
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
        current_volume = round( (data_CF.volume)*self.__volume_multipler )
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
        
        label = QLabel( str( data_CF.fps ) )
        hbox.addWidget(label)
        
        
        # Sección Vertical - Boton alternable - Establecer escuchar musica o no
        self.button_bool_music = QPushButton()
        self.button_bool_music.setCheckable(True)

        self.evt_set_music( checked=data_CF.music )

        self.button_bool_music.clicked.connect( self.evt_set_music )
        vbox_main.addWidget( self.button_bool_music )
        
        # Sección Vertical - Boton alternable - Establecer sonido de fondo o no
        self.button_bool_climateSound = QPushButton()
        self.button_bool_climateSound.setCheckable(True)
        self.evt_set_climateSound( checked=data_CF.climate_sound )
        
        self.button_bool_climateSound.clicked.connect( self.evt_set_climateSound )
        vbox_main.addWidget( self.button_bool_climateSound )
        
        # Sección Vertical - Boton alternable - Ver nubes o no
        self.button_bool_show_clouds = QPushButton()
        self.button_bool_show_clouds.setCheckable(True)
        
        self.evt_set_show_clouds( checked=data_CF.show_clouds )
        self.button_bool_show_clouds.clicked.connect( self.evt_set_show_clouds )
        vbox_main.addWidget( self.button_bool_show_clouds )
        

        # Sección Vertical - Gamecomplete - Boton alternable - Establecer ver collider o no
        if gamecomplete == True:
            self.button_bool_show_collide = QPushButton()
            self.button_bool_show_collide.setCheckable(True)
        
            self.evt_set_show_collide( checked=data_CF.show_collide )
        
            self.button_bool_show_collide.clicked.connect( self.evt_set_show_collide )
            vbox_main.addWidget( self.button_bool_show_collide )
        
        
        # Seccion Vertical - Label - Nivel
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        label = QLabel( Lang('lvl') )
        hbox.addWidget( label )
        
        hbox.addStretch()
        
        current_level = data_CF.current_level
        if gamecomplete == False:
            label = QLabel( current_level.replace(dir_maps, '') )
            hbox.addWidget( label )
        else:
            # Seccion Vertical - Gamecomplete - Combobox - Nivel
            # Si el jugador ya completo el juego, se le permite seleccionar un nivel.
            # De lo contrario, no se le permite cambiar de nivel.
            self.combobox_set_level = QComboBox(self)
            self.combobox_set_level.addItem(
                 current_level.replace( 
                    dir_maps, ''
                 )
            )

            for level in get_level_list():
                if not level == current_level:
                    self.combobox_set_level.addItem( level.replace(dir_maps, '') )
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
        current_resolution = data_CF.disp
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
        

        # Separador
        vbox_main.addStretch()

        # Sección vertical | Gamecomplete | Boton | Información de juegos completados
        if gamecomplete == True:
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
        data_CF.volume=value/self.__volume_multipler
        save_CF( data_CF )
    
    def evt_set_music(self, checked):
        # Establecer sonido de musica o no
        self.button_bool_music.setChecked( checked )
        if checked == True:
            self.button_bool_music.setText( f'{Lang("on")} | {Lang("music")}' )
        else:
            self.button_bool_music.setText( f'{Lang("off")} | {Lang("music")}' )
        data_CF.music=checked
        save_CF( data_CF )
            
    def evt_set_climateSound(self, checked):
        # Establecer sonido de clima o no
        self.button_bool_climateSound.setChecked( checked )
        if checked == True:
            self.button_bool_climateSound.setText( f'{Lang("on")} | {Lang("climateSound")}' )
        else:
            self.button_bool_climateSound.setText( f'{Lang("off")} | {Lang("climateSound")}' )
        data_CF.climate_sound=checked
        save_CF( data_CF )
    
    def evt_set_show_clouds(self, checked):
        # Establecer ver nubes o no
        self.button_bool_show_clouds.setChecked( checked )
        if checked == True:
            self.button_bool_show_clouds.setText( f'{Lang("on")} | {Lang("show_clouds")}')
        else:
            self.button_bool_show_clouds.setText( f'{Lang("off")} | {Lang("show_clouds")}')
        data_CF.show_clouds=checked
        save_CF( data_CF )
    
    def evt_set_level(self):
        # Establecer nivel
        data_CF.current_level = f'{dir_maps}{self.combobox_set_level.currentText()}' 
        save_CF( data_CF )

    def evt_set_show_collide(self, checked):
        # Establecer si ver colliders o no
        self.button_bool_show_collide.setChecked( checked )
        if checked == True:
            self.button_bool_show_collide.setText( f'{Lang("on")} | {Lang("show_collide")}' )
        else:
            self.button_bool_show_collide.setText( f'{Lang("off")} | {Lang("show_collide")}' )
        data_CF.show_collide=checked
        save_CF( data_CF )
    
    def evt_set_disp(self):
        # Establecer la resolución seleccionada
        display = self.combobox_set_resolution.currentText().split('x')
        data_CF.disp = [ int(display[0]), int(display[1]) ]
        save_CF( data_CF )
    
    def evt_get_gamecomplete(self):
        # Mostrar el record de juegos completados

        # Obtener el record de score
        dict_gamecomplete = {}
        list_gamecomplete = get_gamecomplete()
        str_gamecomplete = ''
        for gamecomplete in list_gamecomplete:
            dict_gamecomplete.update( {gamecomplete[0]:None} )
            str_gamecomplete += (
                f'{Lang("lvl")}: {gamecomplete[0]} | {Lang("score")}: {gamecomplete[1]}\n'
            )
         
        for key in dict_gamecomplete.keys():
            list_number = []
            for gamecomplete in list_gamecomplete:
                if key == gamecomplete[0]:
                    list_number.append( gamecomplete[1] )
                    dict_gamecomplete.update( {key:list_number} )
        
        text_record = ''
        for key in dict_gamecomplete.keys():
            text_record += f'{Lang("lvl")}: {key} | {Lang("score")}: {max(dict_gamecomplete[key])}\n'
        
        # Mostrar los juegos completados y su record
        QMessageBox.information(
            self,
            Lang('completedGames'), #Titulo
            (
                f'{Lang("max_score")}:\n'
                f'{text_record}'
                #f'\n\n{str_gamecomplete}'
            ) # Texto
        )

    def evt_credits(self):
        # Creditos del juego
        QMessageBox.information(
            self,
            Lang('credits'), # Titulo
            credits( share=True,jump_lines=True ) # Texto
        )




# Bucle y estilo de programa
qss_style = ''
for widget in get_list_text_widget( 'Qt' ):
    qss_style += text_widget_style(
        widget=widget, font=None, font_size=num_font, 
        margin_xy=num_margin_xy, padding=num_space_padding, idented=4
    )
print(qss_style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss_style)
    window = Window_Main()
    sys.exit( app.exec() )