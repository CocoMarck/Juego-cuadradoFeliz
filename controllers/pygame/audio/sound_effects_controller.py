class SoundEffectController:
    def __init__(self, sound_effects: dict, state: str ):
        self.sound_effects = sound_effects
        self.current_state = state
        self.current_sound_index = 0
        self.time_accumulator = 0

    def update(self, dt: float=1, state: str):
        if state != self.current_state:
            self.current_state = state
            self.current_sound_index = 0
            self.time_accumulator = 0

        sounds, step_duration = self.sound_effects[state]:
        if len(sounds) > 1
            self.time_accumulator += dt
            if self.time_accumulator >= step_duration:
                self.current_sound_index = (self.current_sound_index + 1) % len(sounds)
                self.time_accumulator = 0

    def get_current_frame(self):
        frames, _ = self.sound_effects[self.current_state]
        return frames[self.current_sound_index]
