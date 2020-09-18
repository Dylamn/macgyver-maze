import pygame.mixer

from pygame.locals import K_F1, K_KP_PLUS, K_KP_MINUS

from src.UI.notification import Notification
from src.utils import settings, asset, write_config


class Mixer:
    """Class which manage all audios of the application."""

    # Section of the config file which this class manipulate.
    SECTION = 'Audio'

    # Determines if the audio is muted or not
    __is_muted = bool(settings('Audio', 'muted'))

    # Volume of the musics.
    _musicVolume = settings('Audio', 'music_volume')

    # TODO:
    #  replace by # settings('Audio', 'sound_volume') when sound is handled.
    # Volume of the sounds.
    _soundVolume = settings('Audio', 'music_volume')

    # Dict which contains every musics path of the game.
    musics = {
        'main': asset("sounds/macgyver_theme_song.ogg"),
        'victory': asset("sounds/victory_fanfare.ogg"),
        'defeat': asset("sounds/defeat_theme.ogg"),
    }

    # Dict which contains every sounds of the game.
    sounds = {
        'dummy_sound': asset("sounds/dummy_sound.ogg"),
        'wilhelm_scream': asset("sounds/wilhelm_scream.ogg"),
    }

    @property
    def is_muted(self):
        """Return the boolean which determine if the audio is muted or not."""
        return self.__is_muted

    @is_muted.setter
    def is_muted(self, value: int):
        """Set a new state for the mute status and save it to the config."""
        self.__is_muted = bool(value)
        write_config(section=self.SECTION, key='muted', value=value)

    @property
    def music_volume(self):
        """Retrieve the volume of musics."""
        return self._musicVolume

    @music_volume.setter
    def music_volume(self, value):
        """Increment/decrement the volume of musics."""
        new_volume = self._musicVolume + value

        if self.__is_audio_value(new_volume):
            self._musicVolume += value
        elif new_volume > 1:
            self._musicVolume = 1
        else:
            self._musicVolume = 0.00

        write_config(self.SECTION, key='music_volume', value=self._musicVolume)

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
            write_config(self.SECTION, 'sound_volume', self._soundVolume)

    def __init__(self, notification: Notification = None):
        """Initialize the game mixer."""

        pygame.mixer.pre_init(
            # The audio frequency.
            frequency=44100,

            # How many bits used for audio samples.
            # negative value means that the signed sample values will be used.
            size=-1,

            # 1 for mono, 2 for stereo.
            channels=2,

            # A low buffer makes sounds play (essentially) immediatly.
            buffer=512
        )

        # Initialize sounds after the pre initialization of the mixer.
        for path in self.sounds.keys():
            self.sounds[path] = pygame.mixer.Sound(self.sounds[path])

        self.notification = notification

        # Music of the main menu.
        self.set_music('main')

    def set_music(self, music_slug, loops=-1):
        """Set a music to play."""
        # Fallback with the main theme.
        pygame.mixer.music.load(
            self.musics.get(
                music_slug, asset('sounds/macgyver_theme_song.ogg')
            )
        )
        pygame.mixer.music.set_volume(self._musicVolume)

        if self.is_muted:
            return
        else:
            pygame.mixer.music.play(loops)

    def play_sound(self, sound_slug):
        """Play a sound. Fallback with a dummy sound if given doesn't exist."""
        if self.is_muted:
            return

        # Retrieve the sound
        sound = self.sounds.get(sound_slug, self.sounds['dummy_sound'])
        # Set the volume based on the local settings.
        sound.set_volume(self.sound_volume)
        # Play the sound
        sound.play()

    def toggle(self):
        """Toggle the mute state."""
        if self.is_muted:
            self.__unmute()
        else:
            self.__mute()

    def keys_interaction(self, keys):
        """Handle keys which interact with the audio"""
        if keys[K_F1]:
            self.toggle()

            # String representation of mute status
            mute_status = 'muted' if self.is_muted else 'unmuted'

            self.notification.active('volume', mute_status).set_timer(1)

        if keys[K_KP_PLUS] or keys[K_KP_MINUS]:
            step = 0.1 if keys[K_KP_PLUS] else -0.1

            # Decrement/increment the volume by 0.1 (10%)
            self.music_volume = step

            # A volume "human readable" representation as %
            percent = int(self.music_volume * 100)

            self.notification.active('volume', percent).set_timer(1)

    def __mute(self):
        """Mute audio."""
        pygame.mixer.music.fadeout(0)
        self.is_muted = 1

    def __unmute(self):
        """Unmute the audio."""
        pygame.mixer.music.play()
        self.is_muted = 0

    @staticmethod
    def __is_audio_value(value):
        """Verify if the given value is a correct value for an audio level.

        A valid value is greater or equal than 0 and less or equal than 1.
        """
        return 1 >= value >= 0
