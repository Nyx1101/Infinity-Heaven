from pathlib import Path
import pygame
from typing import Dict

class AudioManager:
    def __init__(self, audio_root: Path):
        pygame.mixer.init()
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_paused = False

        self.sounds_path = audio_root / "sounds"
        self.music_path = audio_root / "music"

    def load_sound(self, name: str, filename: str):
        path = self.sounds_path / filename
        try:
            self.sounds[name] = pygame.mixer.Sound(str(path))
        except pygame.error as e:
            print(f"[AudioManager] Failed to load sound '{name}': {e}")

    def play_sound(self, name: str, loops=0):
        sound = self.sounds.get(name)
        if sound:
            sound.play(loops=loops)
        else:
            print(f"[AudioManager] Sound '{name}' not found.")

    def set_sound_volume(self, name: str, volume: float):
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(max(0.0, min(1.0, volume)))

    def play_music(self, filename: str, loops=-1):
        path = self.music_path / filename
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play(loops)
            self.music_paused = False
        except pygame.error as e:
            print(f"[AudioManager] Failed to load or play music: {e}")

    def pause_music(self):
        if not self.music_paused:
            pygame.mixer.music.pause()
            self.music_paused = True

    def resume_music(self):
        if self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_paused = False

    def set_music_volume(self, volume: float):
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))