from pygame.mixer import Sound
from pygame.rect import Rect

class SoundEffect( Sound ):
    def __init__(self, *args, volume: float=1.0, rect: Rect, **kwargs):
        super().__init__(*args, **kwargs)

        self._INIT_VOLUME = volume
        self.set_volume( self._INIT_VOLUME )
        self.rect = rect

    def get_multiply_init_volume(self, multiplier=1.0, channel="left"):
        return self._INIT_VOLUME * multiplier

    def set_multiply_init_volume(self, multiplier=1.0, channel="left"):
        new_volume = self.get_multiply_init_volume(multiplier, channel)
        if new_volume != self.get_volume():
            self.set_volume( new_volume )
