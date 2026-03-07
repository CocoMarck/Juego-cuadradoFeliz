import pygame
import random
from .background_sound import BackgroundSound

class PlayBackgroundSounds():
    '''
    Clase que necesita de un `pygame.mixer.music` para jalar.
    '''
    def __init__(
        self, sounds:[BackgroundSound], mixer: pygame.mixer.music,
        play_music_sound: bool = True, play_simple_sound: bool = True
    ):
        self._sounds = sounds

        self.play_music_sound = play_music_sound
        self.play_simple_sound = play_simple_sound
        self._sounds_played = []
        self._selected_sound = None
        self._count = 0
        self.mixer = mixer

    def get_music_sounds(self):
        musics = []
        for sound in self._sounds:
            if sound.music:
                musics.append( sound )
        return musics

    def get_simple_sounds(self):
        simple_sounds = []
        for sound in self._sounds:
            if not sound.music:
                simple_sounds.append( sound )
        return simple_sounds


    def select_background_sound(self, mode="random"):
        # Establecer si buscar musica o no.
        search_music = False
        if self.play_music_sound:
            search_music = True
            if self.play_simple_sound:
                search_music = random.random() > 0.5 # 50% de no usar musica

        # Establcer sonidos a seleccionar
        if search_music:
            sounds = self.get_music_sounds()
        else:
            sounds = self.get_simple_sounds()

        # Establecer sonido seleccionado
        if self._selected_sound == None:
            # Reiniciar cantidad de sonidos reproducidos
            if len(self._sounds) == len(self._sounds_played):
                self._sounds_played = []

            # Establcer sonidos no reproducidos
            sounds_not_played = []
            for sound in sounds:
                if not sound in self._sounds_played:
                    sounds_not_played.append( sound )

            # Sonido seleccionado
            if mode == "random":
                self._selected_sound = random.choice( sounds_not_played )
            elif mode == "sequential":
                self._selected_sound = sounds_not_played[0]

            # Agregar sonido a sonidos reproducidos
            self._sounds_played.append( self._selected_sound )


        # Reproducir sonido seleccionado
        if self._selected_sound != None:
            if not self.mixer.get_busy():
                self._count += 1

                if self._count > self._selected_sound.repetitions:
                    self._count = 0
                    self._selected_sound = None
                else:
                    self._selected_sound.play( self.mixer )

