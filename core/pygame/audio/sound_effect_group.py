from .sound_effect import SoundEffect

class SoundEffectGroup():
    def __init__(self):
        self._sounds = []

    def add(self, sound: SoundEffect) -> bool:
        if not sound in self._sounds:
            self._sounds.append(sound)
            return True
        return False

    def remove(self, sound: SoundEffect) -> bool:
        if sound in self._sounds:
            self._sounds.remove(sound)
            return True
        return False

    def clear(self):
        self._sounds.clear()

    def sounds(self) -> list:
        return self._sounds
