from pathlib import Path
import pygame


class AudioManager:
    def __init__(self, audio_root: Path):
        """
        Initialize the audio manager, set up the pygame mixer and audio paths.
        """
        pygame.mixer.init()  # Initialize the mixer module for audio playback
        self.current_music = None  # Track currently playing music filename
        self.music_paused = False  # Track if music is currently paused

        self.music_path = audio_root / "music"  # Path to the music directory

    def play_music(self, filename: str, loops=-1):
        """
        Play background music from the specified file, optionally looping.
        """
        path = self.music_path / filename
        if self.current_music == filename:
            # Already playing this track, no need to reload
            return

        try:
            pygame.mixer.music.load(str(path))  # Load music file
            pygame.mixer.music.play(loops)     # Start playback with looping
            self.music_paused = False
            self.current_music = filename
        except pygame.error as e:
            print(f"[AudioManager] Failed to load or play music: {e}")

    def pause_music(self):
        """
        Pause the currently playing music if it is not already paused.
        """
        if not self.music_paused:
            pygame.mixer.music.pause()
            self.music_paused = True

    def resume_music(self):
        """
        Resume the music playback if it is currently paused.
        """
        if self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False

    def stop_music(self):
        """
        Stop the music playback completely.
        """
        pygame.mixer.music.stop()
        self.music_paused = False

    @staticmethod
    def set_music_volume(volume: float):
        """
        Set the volume level for music playback.
        """
        # Clamp volume between 0.0 and 1.0
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
