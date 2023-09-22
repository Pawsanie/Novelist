from os import sep

from pygame.mixer import Channel, Sound, music
from pygame import mixer \
 # , constants

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Settings_Keeper import SettingsKeeper
from .Assets_load import sound_load, music_load
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
                "sound_type_volume": self.settings_keeper.music_volume,
                "devnull_status": False,
                "sound_file_name": None
            },
            "sound_channel": {
                "sound_channel": Channel(1),
                "sound_file": None,
                "sound_type_volume": self.settings_keeper.sound_volume,
                "devnull_status": False,
                "sound_file_name": None
            },
            "voice_channel": {
                "sound_channel": Channel(2),
                "sound_file": None,
                "sound_type_volume": self.settings_keeper.sound_volume,
                "devnull_status": False,
                "sound_file_name": None
            }
        }

        self.status: bool = True
        self.single_voiceover_language: bool = True
        self.default_language: str = 'eng'
        # music.set_endevent(constants.USEREVENT)  # TODO: music use low RAM.

    def vanish_channels(self):
        """
        Devnull sounds from all sound channels.
        """
        for chanel in self.channels_collection:
            if self.channels_collection[chanel]["devnull_status"] is True:
                self.channels_collection[chanel]["sound_channel"].fadeout(1600)

    def play_sound(self, sound_file: Sound, sound_channel: Channel, sound_type_volume: int, sound_chanel_name: str):
        """
        Play sound file.
        :param sound_file: Sound file.
        :type sound_file: Sound
        :param sound_channel: Channel for soundtrack playing.
        :type sound_channel: Channel
        :param sound_type_volume: Link to SettingsKeeper sound volume type.
        :type sound_type_volume: int
        :param sound_chanel_name: Name of sound chanel.
        :type sound_chanel_name: str
        """
        self.set_sound_volume(
            sound_file=sound_file,
            sound_type_volume=sound_type_volume
        )
        loops: int = 0
        if sound_chanel_name == "music_channel":
            loops -= 1
        sound_channel.play(
            sound_file,
            loops=loops
        )

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

            for channel_name in self.channels_collection:
                channel: dict = self.channels_collection[channel_name]
                sound_file: Sound | None = channel['sound_file']

                if sound_file is not None:
                    self.play_sound(
                        sound_file=sound_file,
                        sound_channel=channel['sound_channel'],
                        sound_type_volume=channel['sound_type_volume'],
                        sound_chanel_name=channel_name
                    )

            self.status: bool = False

    def sound_chanel_controller(self, *, asset_type: str = '', sound_file_name: str | bool, sound_chanel: str):
        """
        Send soundtrack to sound chanel if necessary.

        :param asset_type: Asset "Sounds" sub folder.
                           Controlled by default.
        :type asset_type: str
        :param sound_file_name: Sound file name. Must be "string" or "False".
        :type sound_file_name: str | False
        :param sound_chanel: Sound chanel type.
        :type sound_chanel: str
        """
        # Change soundtrack in sound chanel:
        if self.channels_collection[sound_chanel]['sound_file_name'] != sound_file_name:
            self.status = True

            # Devnull sound in chanel:
            if sound_file_name is False:
                self.channels_collection[sound_chanel]['sound_file_name'] = sound_file_name
                self.channels_collection[sound_chanel]['sound_file'] = None
                self.channels_collection[sound_chanel]['devnull_status'] = True
                return

            # Music:
            if sound_chanel == 'music_channel':
                asset_type: str = 'Music'

            # Sound effects:
            if sound_chanel == 'sound_channel':
                asset_type: str = 'Effects'

            # Character Speach:
            if sound_chanel == 'voice_channel':
                if self.single_voiceover_language is True:
                    asset_type: str = 'Voice'
                else:
                    asset_type: str = f"Voice{sep}{self.settings_keeper.voice_acting_language}"

            # Install sound in chanel:
            if asset_type == 'Music':
                sound_file = music_load(
                    asset_type=asset_type,
                    file_name=sound_file_name
                )
            else:
                sound_file = sound_load(
                    asset_type=asset_type,
                    file_name=sound_file_name
                )
            self.channels_collection[sound_chanel]['sound_file'] = sound_file
            self.channels_collection[sound_chanel]['sound_file_name'] = sound_file_name
            self.channels_collection[sound_chanel]['devnull_status'] = True

        # Keep current soundtrack in sound chanel:
        else:
            self.channels_collection[sound_chanel]['sound_file'] = None
            self.channels_collection[sound_chanel]['devnull_status'] = False
