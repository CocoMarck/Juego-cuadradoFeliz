from data.Modulo_Language import get_text as Lang
from data.CF_info import data_CF
from data.CF_data import *
#import subprocess, sys

from interface.interface_number import *
from interface.css_util import *

import threading
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk




# Detectar si se completo el juego o no
if not get_gamecomplete() == None:
    gamecomplete = True
else:
    gamecomplete = False




# Ventana principal
class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__( title='El Cuadrado Feliz' )
        
        self.set_resizable(True)
        self.set_default_size(nums_win_main[0], nums_win_main[1])
        #self.set_icon_from_file( 'Icon.png' )
        
        # Contenedor principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        
        # Sección Vertical - Boton - Inicio, Controles
        button_play = Gtk.Button( label=Lang('start') )
        button_play.connect('clicked', self.evt_start_game )
        vbox_main.pack_start( button_play, True, True, 0 )
        
        button_controls = Gtk.Button( label=Lang('ctrls') )
        button_controls.connect('clicked', self.evt_get_controls)
        vbox_main.pack_start( button_controls, True, True, 0 )
        

        # Sección Vertical - SpinBox - Establecer volumen
        self.__volume_multipler = 100
        current_volume = round( (data_CF.volume )*self.__volume_multipler )
        
        hbox = Gtk.Box(spacing=0)
        vbox_main.pack_start(hbox, True, False, 0)
        
        label = Gtk.Label( label=Lang('volume') )
        hbox.pack_start(label, False, False, 0)
        
        self.spinbutton_volume = Gtk.SpinButton()
        self.spinbutton_volume.set_adjustment(
            Gtk.Adjustment(
                upper=self.__volume_multipler, step_increment=1, page_increment=10,
                value=current_volume
            )
        )
        self.spinbutton_volume.connect('value-changed', self.evt_set_volume)
        hbox.pack_end(self.spinbutton_volume, False, False, 0)
        

        # Sección Vertical - Label - Fps establecidos
        hbox = Gtk.Box(spacing=0)
        vbox_main.pack_start(hbox, True, False, 0)
        
        label = Gtk.Label( label=Lang('fps') )
        hbox.pack_start(label, False, False, 0)
        
        label = Gtk.Label( label=f'{ data_CF.fps }' )
        hbox.pack_end(label, False, False, 0)
        

        # Sección Vertical - Switch Button -  Establecer escuchar musica o no
        hbox = Gtk.Box(spacing=0)
        vbox_main.pack_start(hbox, True, False, 0)
        
        label = Gtk.Label( label=Lang('music') )
        hbox.pack_start(label, False, False, 0)
        
        switch = Gtk.Switch()
        switch.connect('notify::active', self.evt_set_music)
        switch.set_active( data_CF.music )
        hbox.pack_end( switch, False, False, 0)
                
        # Sección Vertical - Switch Button - Establecer escuchar sonido de fondo o no
        hbox = Gtk.Box(spacing=0)
        vbox_main.pack_start(hbox, True, False, 0)
        
        label = Gtk.Label( label=Lang('climateSound') )
        hbox.pack_start(label, False, False, 0)
        
        switch = Gtk.Switch()
        switch.connect('notify::active', self.evt_set_climateSound)
        switch.set_active( data_CF.climate_sound )
        hbox.pack_end( switch, False, False, 0 )


        # Sección Vertical - Switch Button - Establecer ver nubes o no
        hbox = Gtk.Box(spacing=0)
        vbox_main.pack_start(hbox, True, False, 0)
        
        label = Gtk.Label( label=Lang('show_clouds') )
        hbox.pack_start( label, False, False, 0 )
        
        switch = Gtk.Switch()
        switch.connect('notify::active', self.evt_set_show_clouds)
        switch.set_active( data_CF.show_clouds )
        hbox.pack_end(switch, False, False, 0)
        
        # Sección vertical - Gamecomplete - Switch button - Establecer ver collider o no
        if gamecomplete == True:
            hbox = Gtk.Box(spacing=0)
            vbox_main.pack_start(hbox, True, False, 0)
            
            label = Gtk.Label( label=Lang('show_collide') )
            hbox.pack_start(label, False, False, 0)
        
            switch = Gtk.Switch()
            switch.connect('notify::active', self.evt_set_show_collide )
            switch.set_active( data_CF.show_collide )
            hbox.pack_end( switch, False, False, 0 )
            
            # Mostrar sprite
            hbox = Gtk.Box(spacing=0)
            vbox_main.pack_start(hbox, True, False, 0 )
            label = Gtk.Label( label=Lang('show_sprite') )
            hbox.pack_start(label, False, False, 0)
            switch = Gtk.Switch()
            switch.connect('notify::active', self.evt_set_show_sprite)
            switch.set_active( data_CF.show_sprite )
            hbox.pack_end(switch, False, False, 0)
            

        # Sección vertical - Label - Ver Nivel
        hbox = Gtk.Box(spacing=0)
        vbox_main.pack_start(hbox, True, False, 0)
        
        label = Gtk.Label( label=Lang('lvl') )
        hbox.pack_start(label, False, False, 0)

        current_level = data_CF.current_level
        if gamecomplete == False:
            label = Gtk.Label( label=current_level.replace(dir_maps, '') )
            hbox.pack_end( label, False, False, 0 )
            
        # Sección vertical - Gamecomplete - Comobobox - Seleccionar nivel
        else:
            # Lista de niveles
            # El indice del nivel actual seria el numero '0"
            list_level = Gtk.ListStore(str)
            list_level.append( [ current_level.replace(dir_maps, '') ] )
            for level in get_level_list():
                if not level == current_level:
                    list_level.append( [ level.replace(dir_maps, '') ] )
            
            # Combobox
            rendertext = Gtk.CellRendererText()
            self.combobox_set_level = Gtk.ComboBox.new_with_model( list_level )
            self.combobox_set_level.pack_start(rendertext, True)
            self.combobox_set_level.add_attribute(
                rendertext, 'text', 0
            )
            self.combobox_set_level.set_active( 0 )
            self.combobox_set_level.connect("changed", self.evt_set_level)
            hbox.pack_end( self.combobox_set_level, False, False, 0 )

        
        # Sección vertical - Combobox - Seleccionar resolución
        hbox = Gtk.Box(spacing=0)
        vbox_main.pack_start(hbox, True, False, 0)
        
        label = Gtk.Label( label=Lang('resolution') )
        hbox.pack_start(label, False, False, 0 )
        
        current_resolution = 3
        list_resolution = (
            [1920, 1080],
            [1440, 810],
            [960, 540],
            [480, 270]
        )
        listStore_resolution = Gtk.ListStore(str)
        count_resolution = 0
        for resolution in list_resolution:
            listStore_resolution.append( [f'{resolution[0]}x{resolution[1]}'] ) 
            if resolution == data_CF.disp :
                current_resolution = count_resolution
            count_resolution += 1

        rendertext = Gtk.CellRendererText()
        combobox_set_resolution = Gtk.ComboBox.new_with_model( listStore_resolution )
        combobox_set_resolution.pack_start(rendertext, True)
        combobox_set_resolution.add_attribute(
            rendertext, 'text', 0
        )
        combobox_set_resolution.set_active( current_resolution )
        combobox_set_resolution.connect( 'changed', self.evt_set_disp )
        hbox.pack_end( combobox_set_resolution, False, False, 0 )
        

        # Sección Vertical - Gamecomplete - Button - Información de juegos completados
        if gamecomplete == True:
            button_get_gamecomplete = Gtk.Button( label=Lang('completedGames') )
            button_get_gamecomplete.connect('clicked', self.evt_get_gamecomplete)
            vbox_main.pack_start(button_get_gamecomplete, True, True, 0 )
        
        
        # Sección Vertical - Button - Creditos
        button_credits = Gtk.Button( label=Lang('credits') )
        button_credits.connect('clicked', self.evt_credits)
        vbox_main.pack_end(button_credits, True, True, 0)
        

        # Mostrar todo y agregar contenedor principal
        self.add(vbox_main)
        self.show_all()
    
    def evt_start_game(self, button):
        # Cerrar cliente, y comenzar juego.
        self.thread = threading.Thread(target=self.thread_start_game)
        self.thread.start()
        
        self.destroy()
        #self.hide()
    
    def thread_start_game(self):
        import cuadradoFeliz
    #    GLib.idle_add(self.thread_fin_game)
    #def thread_fin_game(self):
    #    self.show_all()
        
    def evt_get_controls(self, button):
        # Obtener los controles default
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            title=Lang('ctrls'),
            text=Lang('default_ctrls')
        )
        dialog.run()
        dialog.destroy()
        

    def evt_set_volume(self, scroll):
        # Establecer volumen
        # Valor actual del spinbutton, dividido entre self.__volume_multipler
        # Ejemplo: 50/100 = 0.5
        data_CF.volume = self.spinbutton_volume.get_value_as_int()/self.__volume_multipler 
        save_CF( data_CF )
        

    def evt_set_music(self, switch, gparam):
        # Establecer el escuchar musica o no.
        data_CF.music=switch.get_active()
        save_CF( data_CF )

    def evt_set_climateSound(self, switch, gparam):
        # Establecer el escuchar sonido de clima o no.
        data_CF.climate_sound=switch.get_active()
        save_CF( data_CF )
    

    def evt_set_show_clouds(self, switch, gparam):
        # Establecer mostrar nubes o no
        data_CF.show_clouds=switch.get_active()
        save_CF( data_CF )
    
    def evt_set_show_collide(self, switch, gparam):
        # Establecer el mostrar collider o no
        data_CF.show_collide=switch.get_active()
        save_CF( data_CF )

    def evt_set_show_sprite(self, switch, gparam):
        # Establecer el mostrar sprite o no
        data_CF.show_sprite=switch.get_active()
        save_CF( data_CF )
    
    
    
    def evt_set_level(self, combo):
        # Establecer nivel
        combo_iter = combo.get_active_iter()
        combo_model = combo.get_model()
        data_CF.current_level = f'{dir_maps}{combo_model[combo_iter][0]}'
        save_CF( data_CF )
    

    def evt_set_disp(self, combo):
        # Establecer la resolución seleccionada
        combo_iter = combo.get_active_iter()
        combo_model = combo.get_model()
        disp_xy = combo_model[combo_iter][0].split('x')
        data_CF.disp = [ int(disp_xy[0]), int(disp_xy[1]) ]
        save_CF( data_CF )
    
    
    def evt_get_gamecomplete(self, button):
        # Mostrar el record de juegos completados

        # Obtener el record de score
        dict_gamecomplete = {}
        list_gamecomplete = get_gamecomplete()
        for gamecomplete in list_gamecomplete:
             dict_gamecomplete.update( {gamecomplete[0]:None} )
         
        for key in dict_gamecomplete.keys():
            list_number = []
            for gamecomplete in list_gamecomplete:
                if key == gamecomplete[0]:
                    list_number.append( gamecomplete[1] )
                    dict_gamecomplete.update( {key:list_number} )
        
        text_record = ''
        for key in dict_gamecomplete.keys():
            text_record += f'{Lang("lvl")}: {key} | {Lang("score")}: {max(dict_gamecomplete[key])}\n'

        # Dialog
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            title=Lang('completedGames'),
            text=(
                f'{Lang("max_score")}:\n'
                f'{text_record}'
            )
        )
        dialog.run()
        dialog.destroy()
    

    def evt_credits(self, button):
        # Mostrar los creditos
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            title=Lang('credits'),
            text=credits( share=True,jump_lines=True )
        )
        dialog.run()
        dialog.destroy()




# Bucle y estilo de programa
css_style = ''
for widget in get_list_text_widget( 'Gtk' ):
    if widget == 'textview':
        css_style += text_widget_style(
            widget=widget, font=None, font_size=num_font,
            padding=None, margin_xy=None, idented=4
        )
    else:
        css_style += text_widget_style(
            widget=widget, font=None, font_size=num_font,
            padding=num_space_padding, margin_xy=None, idented=4
        )
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
style_context = Gtk.StyleContext()
style_context.add_provider_for_screen(
    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
provider.load_from_data( str.encode(css_style) )
print( css_style )


win = Window_Main()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()