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

        self.channels_collection: dict = {
            "music_channel": {
                "sound_channel": Channel(0),
                "sound_file": None,
                "sound_type_volume": self.settings_keeper.music_volume
            },
            "sound_channel": {
                "sound_channel": Channel(1),
                "sound_file": None,
                "sound_type_volume": self.settings_keeper.sound_volume
            },
            "voice_channel": {
                "sound_channel": Channel(2),
                "sound_file": None,
                "sound_type_volume": self.settings_keeper.sound_volume
            }
        }

        self.status: bool = True

    def vanish_channels(self):
        """
        Devnull sounds from all sound channels.
        """
        for chanel in self.channels_collection:
            self.channels_collection[chanel]["sound_channel"].fadeout(300)

    def play_sound(self, sound_file: Sound, sound_channel: Channel, sound_type_volume: int):
        """
        Play sound file.
        :param sound_file: Sound file.
        :type sound_file: Sound
        :param sound_channel: Channel for soundtrack playing.
        :type sound_channel: Channel
        :param sound_type_volume: Link to SettingsKeeper sound volume type.
        :type sound_type_volume: int
        """
        self.set_sound_volume(
            sound_file=sound_file,
            sound_type_volume=sound_type_volume
        )
        sound_channel.play(sound_file)

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

    def play(self):
        """
        Play soundtracks if it possibly.
        """
        if self.status is True:
            self.vanish_channels()

            for channel in self.channels_collection:
                channel: dict = self.channels_collection[channel]
                sound_file: Sound | None = channel['sound_file']

                if channel['sound_file'] is not None:
                    self.play_sound(
                        sound_file=sound_file,
                        sound_channel=channel['sound_channel'],
                        sound_type_volume=channel['sound_type_volume']
                    )

            self.status: bool = False
