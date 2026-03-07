import pygame
import random
from .background_sound import BackgroundSound

class PlayBackgroundSounds():
    '''
    Clase que necesita de un `pygame.mixer.music` para jalar.
    '''
    def __init__(
        self, sounds:[BackgroundSound], mixer: pygame.mixer.music,
        play_music_sound: bool = True, play_simple_sound: bool = True,
        music_possibility: float = 0.5
    ):
        self._sounds = sounds

        self.play_music_sound = play_music_sound
        self.play_simple_sound = play_simple_sound
        self._simple_sounds_played = []
        self._musics_played = []
        self._selected_sound = None
        self._count = 0
        self.mixer = mixer

        self.music_possibility = music_possibility

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
        # Nadota de sonido.
        if not (self.play_music_sound) and not(self.play_simple_sound):
            return

        # Establecer si buscar musica o no.
        search_music = self.play_music_sound
        if search_music:
            if self.play_simple_sound:
                search_music = random.random() > self.music_possibility

        # Establcer sonidos a seleccionar
        if search_music:
            sounds = self.get_music_sounds()
            sounds_played = self._musics_played
        else:
            sounds = self.get_simple_sounds()
            sounds_played = self._simple_sounds_played

        # Establecer sonido seleccionado
        if self._selected_sound == None:
            # Reiniciar cantidad de sonidos reproducidos
            if len(sounds) == len(sounds_played):
                sounds_played.clear()

            # Establcer sonidos no reproducidos
            sounds_not_played = []
            for sound in sounds:
                if not sound in sounds_played:
                    sounds_not_played.append( sound )

            # Sonido seleccionado
            if mode == "random":
                self._selected_sound = random.choice( sounds_not_played )
            elif mode == "sequential":
                self._selected_sound = sounds_not_played[0]

            # Agregar sonido a sonidos reproducidos
            sounds_played.append( self._selected_sound )


        # Reproducir sonido seleccionado
        if (self._selected_sound != None) and (not self.mixer.get_busy()):
            if self._count == self._selected_sound.repetitions:
                self._count = 0
                self._selected_sound = None
            else:
                self._count += 1
                self._selected_sound.play( self.mixer )
