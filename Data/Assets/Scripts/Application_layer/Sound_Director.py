from os import sep

from pygame.mixer import Channel, Sound, music
from pygame import mixer

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Settings_Keeper import SettingsKeeper
from ..Universal_computing.Assets_load import AssetLoader
mixer.init()
"""
Contains the code responsible for play sounds.
"""


class SoundDirector(SingletonPattern):
    """
    Controls the sounds within the scene.
    """
    def __init__(self):
        # Program layers settings:
        self._settings_keeper: SettingsKeeper = SettingsKeeper()
        self._asset_loader: AssetLoader = AssetLoader()

        # Sound attributes:
        self._channels_collection: dict = {
            "music_channel": {
                "sound_channel": Channel(0),
                "sound_file": None,
                "sound_type_volume": self._settings_keeper.music_volume,
                "devnull_status": False,
                "sound_file_name": None
            },
            "sound_channel": {
                "sound_channel": Channel(1),
                "sound_file": None,
                "sound_type_volume": self._settings_keeper.sound_volume,
                "devnull_status": False,
                "sound_file_name": None
            },
            "voice_channel": {
                "sound_channel": Channel(2),
                "sound_file": None,
                "sound_type_volume": self._settings_keeper.sound_volume,
                "devnull_status": False,
                "sound_file_name": None
            }
        }

        self._status: bool = True
        self._single_voiceover_language: bool = True
        # self.default_language: str = 'eng'
        # music.set_endevent(constants.USEREVENT)  # TODO: music use low RAM.

    def _vanish_channels(self):
        """
        Devnull sounds from all sound channels.
        """
        for chanel in self._channels_collection:
            if self._channels_collection[chanel]["devnull_status"] is True:
                self._channels_collection[chanel]["sound_channel"].fadeout(1600)

    def _play_sound(self, sound_file: Sound, sound_channel: Channel, sound_type_volume: int, sound_chanel_name: str):
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
        self._set_sound_volume(
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

    def _set_sound_volume(self, *, sound_file: Sound, sound_type_volume: int):
        """
        Set sound volume.
        :param sound_file: Sound or music for volume changing.
        :type sound_file: Sound | music
        :param sound_type_volume: SettingsKeeper volume type.
        :type sound_type_volume: int
        """
        sound_file.set_volume(
            float(
                self._settings_keeper.general_volume
                / sound_type_volume
            )
        )

    def play(self):
        """
        Play soundtracks if it possibly.
        Call from GameMaster.
        """
        if self._status is True:
            self._vanish_channels()

            for channel_name in self._channels_collection:
                channel: dict = self._channels_collection[channel_name]
                sound_file: Sound | None = channel['sound_file']

                if sound_file is not None:
                    self._play_sound(
                        sound_file=sound_file,
                        sound_channel=channel['sound_channel'],
                        sound_type_volume=channel['sound_type_volume'],
                        sound_chanel_name=channel_name
                    )

            self._status: bool = False

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
        if self._channels_collection[sound_chanel]['sound_file_name'] != sound_file_name:
            self._status: bool = True

            # Devnull sound in chanel:
            if sound_file_name is False:
                self._channels_collection[sound_chanel]['sound_file_name'] = sound_file_name
                self._channels_collection[sound_chanel]['sound_file'] = None
                self._channels_collection[sound_chanel]['devnull_status'] = True
                return

            # Music:
            if sound_chanel == 'music_channel':
                asset_type: str = 'Music'

            # Sound effects:
            elif sound_chanel == 'sound_channel':
                asset_type: str = 'Effects'

            # Character Speach:
            elif sound_chanel == 'voice_channel':
                if self._single_voiceover_language is True:
                    asset_type: str = 'Voice'
                else:
                    asset_type: str = f"Voice{sep}{self._settings_keeper.voice_acting_language}"

            # Install sound in chanel:
            sound_file = self._asset_loader.sound_load(
                    asset_type=asset_type,
                    file_name=sound_file_name
                )
            self._channels_collection[sound_chanel]['sound_file'] = sound_file
            self._channels_collection[sound_chanel]['sound_file_name'] = sound_file_name
            self._channels_collection[sound_chanel]['devnull_status'] = True

        # Keep current soundtrack in sound chanel:
        else:
            self._channels_collection[sound_chanel]['sound_file'] = None
            self._channels_collection[sound_chanel]['devnull_status'] = False
