import pygame.mixer
from src.utils import *


class Mixer:
    """Class which manage all audios of the application."""

    # Section of the config file which this class manipulate.
    SECTION = 'Audio'

    # Determines if the audio is muted or not
    __is_muted = False

    # Volume of the musics.
    _musicVolume = settings('Audio', 'music_volume')

    # Volume of the sounds.
    _soundVolume = settings('Audio', 'sound_volume')

    # Dict which contains every musics path of the game.
    musics = {
        'main': asset("sounds/macgyver_theme_song.ogg"),
        'victory': asset("sounds/victory_fanfare.ogg"),
        'defeat': asset("sounds/defeat_theme.ogg")
    }

    # Dict which contains every sounds of the game.
    sounds = {
        'wilhelm_scream': asset("sounds/wilhelm_scream.ogg")
    }

    @property
    def music_volume(self):
        """Retrieve the volume of musics."""
        return self._musicVolume

    @music_volume.setter
    def music_volume(self, value):
        """Increment/decrement the volume of musics."""

        if self.__is_audio_value(self._musicVolume + value):
            self._musicVolume += value
            write_config(section=self.SECTION, key='music_volume', value=self._musicVolume)

            pygame.mixer.music.set_volume(self.music_volume)

    @property
    def sound_volume(self):
        """Increment/decrement the volume of sounds."""
        return self._soundVolume

    @sound_volume.setter
    def sound_volume(self, value):
        """Set a new volume for sounds."""
        if self.__is_audio_value(self._musicVolume + value):
            self._soundVolume += value
            write_config(section=self.SECTION, key='sound_volume', value=self._soundVolume)

    def __init__(self):
        """Initialize the game mixer."""

        pygame.mixer.pre_init(
            44100,  # Audio frequency.
            -1,  # Size.
            2,  # Channels. 1 means mono, 2 stereo.
            512  # Buffer. A low buffer makes sounds play (essentially) immediatly.
        )

        # Initialize sounds after the pre initialization of the mixer.
        for sound_name in self.sounds.keys():
            self.sounds[sound_name] = pygame.mixer.Sound(self.sounds[sound_name])

        # Music of the main menu.
        self.set_music('main')

    def set_music(self, music_slug, loops=-1):
        """Set a music to play."""

        # Fallback with the main theme.
        pygame.mixer.music.load(self.musics.get(music_slug, asset('sounds/macgyver_theme_song.ogg')))
        pygame.mixer.music.set_volume(self._musicVolume)
        pygame.mixer.music.play(loops)

    def toggle(self):
        """Toggle the mute state."""
        if self.__is_muted:
            self.__unmute()
        else:
            self.__mute()

    def __mute(self):
        """Mute audio."""
        pygame.mixer.music.fadeout(0)
        self.__is_muted = True

    def __unmute(self):
        """Unmute the audio."""
        pygame.mixer.music.play()
        self.__is_muted = False

    @staticmethod
    def __is_audio_value(value):
        """Verify if the given value is a correct value for an audio level. \n
            A valid value is greater or equal than 0 and less or equal than 1.
        """
        return 1 >= value >= 0
