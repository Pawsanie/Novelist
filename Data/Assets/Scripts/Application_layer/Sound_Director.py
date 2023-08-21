from pygame.mixer import music, Channel, Sound

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Settings_Keeper import SettingsKeeper
"""
Contains the code responsible for play sounds.
"""


class SoundDirector(SingletonPattern):
    """
    Controls the sounds within the scene.
    """
    def __init__(self):
        # Program layers settings:
        self.settings_keeper: SettingsKeeper = SettingsKeeper()

        self.music_channel: Channel = Channel(0)
        self.sound_channel: Channel = Channel(1)

    def vanish_channels(self):
        ...

    def play_sound(self, sound_file: Sound):
        """
        Play sound file.
        """
        self.sound_volume(sound_file)
        self.sound_channel.play(sound_file)

    def play_music(self, music_file: Sound):
        """
        Play music file.
        """
        self.music_volume(music_file)
        self.music_channel.play(music_file)

    def music_volume(self, music_file: Sound):
        """
        Set music volume.
        """
        music_file.set_volume(
            float(
                self.settings_keeper.general_volume /
                self.settings_keeper.music_volume
            )
        )

    def sound_volume(self, sound_file: Sound):
        """
        Set sound volume.
        """
        sound_file.set_volume(
            float(
                self.settings_keeper.general_volume /
                self.settings_keeper.sound_volume
            )
        )
