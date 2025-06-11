from pathlib import Path
import pygame


class AudioManager:
    def __init__(self, audio_root: Path):
        pygame.mixer.init()
        self.current_music = None
        self.music_paused = False

        self.music_path = audio_root / "music"

    def play_music(self, filename: str, loops=-1):
        path = self.music_path / filename
        if self.current_music == filename:
            return

        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play(loops)
            self.music_paused = False
            self.current_music = filename
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

    @staticmethod
    def set_music_volume(volume: float):
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
