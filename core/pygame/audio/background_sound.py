import pygame
import pathlib

class BackgroundSound():
    '''
    Sonido de fondo.
    '''
    def __init__(self, source: pathlib.Path, volume: float, music: bool, repetitions: int):
        self.source = source
        self.music = music
        self._volume = volume
        self.repetitions = repetitions

    def set_volume(self, volume):
        if volume > 1:
            volume = 1
        if volume < 0:
            volume = 0
        self._volume = float(volume)

    def get_volume(self):
        return self._volume

    def play(self, mixer: pygame.mixer.music):
        mixer.set_volume( self.get_volume() )
        mixer.load( self.source )
        mixer.play()
