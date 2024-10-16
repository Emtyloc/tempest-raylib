import os
from pyray import load_sound, unload_sound, set_sound_volume

class SoundManager:
    def __init__(self, volume: float):
        self.sounds = {}
        self.volume = volume

    def load_sounds(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/sounds"))
        self.sounds['shot'] = load_sound(os.path.join(base_path, "shot.wav"))
        self.sounds['blaster_move'] = load_sound(os.path.join(base_path, "tick.wav"))
        self.sounds['enemy_bullet'] = load_sound(os.path.join(base_path, "bullet.wav"))
        self.sounds['enemy_death'] = load_sound(os.path.join(base_path, "flippershot.wav"))
        self.sounds['super_zapper'] = load_sound(os.path.join(base_path, "zap.wav"))

        self.set_sounds_volume()
    
    def set_sounds_volume(self):
        for sound in self.sounds.values():
            set_sound_volume(sound, self.volume)

    def get_sound(self, sound_name):
        return self.sounds.get(sound_name)

    def unload_sounds(self):
        for sound in self.sounds.values():
            unload_sound(sound)
        self.sounds.clear()
