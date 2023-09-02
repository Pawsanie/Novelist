from pygame.mixer import Channel, Sound, music
from pygame import mixer

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Settings_Keeper import SettingsKeeper
"""
Contains the code responsible for play sounds.
"""
mixer.init()


class SoundDirector(SingletonPattern):
    """
    Controls the sounds within the scene.
    """
    def __init__(self):
        # Program layers settings:
        self.settings_keeper: SettingsKeeper = SettingsKeeper()

        self.music_channel: Channel = Channel(0)
        self.sound_channel: Channel = Channel(1)
        self.voice_channel: Channel = Channel(2)

    def vanish_channels(self):
        ...

    def play_sound(self, sound_file: Sound):
        """
        Play sound file.
        :param sound_file: Sound file.
        :type sound_file: Sound
        """
        self.set_sound_volume(
            sound_file=sound_file,
            sound_type_volume=self.settings_keeper.sound_volume
        )
        self.sound_channel.play(sound_file)

    def play_music(self, music_file: Sound):
        """
        Play music file.
        :param music_file: Music file.
        :type music_file: Sound | music
        """
        self.set_sound_volume(
            sound_file=music_file,
            sound_type_volume=self.settings_keeper.music_volume
        )
        self.music_channel.play(music_file)

    def play_voice(self, voice_sound_file: Sound):
        """
        Play music file.
        :param voice_sound_file: Character speech sound file.
        :type voice_sound_file: Sound
        """
        self.set_sound_volume(
            sound_file=voice_sound_file,
            sound_type_volume=self.settings_keeper.sound_volume
        )
        self.voice_channel.play(voice_sound_file)

    def set_sound_volume(self, *, sound_file: Sound, sound_type_volume: int):
        """
        Set sound volume.
        :param sound_file: Sound or music for volume changing.
        :type sound_file: Sound | music
        :param sound_type_volume: SettingsKeeper volume type.
        :type sound_type_volume: int
        """
        sound_file.set_volume(
            float(
                self.settings_keeper.general_volume /
                sound_type_volume
            )
        )
