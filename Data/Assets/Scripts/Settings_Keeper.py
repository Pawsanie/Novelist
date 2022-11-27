from os import path
from sys import platform
"""
Contains the code responsible for the game settings.
"""


def system_type() -> str:
    """
    :return: String with system type.
    """
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'Mac_OS'
    elif platform == "win32" or platform == "win64":
        return 'Windows'


class SettingsKeeper:
    """
    Reading settings from "settings" file.
    """
    def __init__(self):
        script_root_path: str = f"{path.abspath(__file__).replace(path.join(*['Scripts', 'Settings_Keeper.py']), '')}"
        user_settings_path: str = f"{script_root_path}{path.join(*['user_settings'])}"
        with open(user_settings_path) as game_settings:
            for row in game_settings:
                setting_type: list[str] = row.replace('\n', '').split('=')
                if setting_type[0] == 'screen_size':
                    screen_size_settings: list[str] = setting_type[1].split('x')
                    screen_size: tuple[int, int] = (int(screen_size_settings[0]), int(screen_size_settings[1]))
                    self.screen_size: tuple[int, int] = screen_size
                if setting_type[0] == 'general_volume':
                    self.general_volume: int = int(setting_type[1])
                if setting_type[0] == 'music_volume':
                    self.music_volume: int = int(setting_type[1])
                if setting_type[0] == 'sound_volume':
                    self.sound_volume: int = int(setting_type[1])
                if setting_type[0] == 'screen_type':
                    self.screen_type: str = setting_type[1]
                if setting_type[0] == 'text_language':
                    self.text_language: str = setting_type[1]
                if setting_type[0] == 'voice_acting_language':
                    self.voice_acting_language: str = setting_type[1]
        self.system_type: str = system_type()
