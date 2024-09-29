from os import path
from sys import platform
from tkinter import Tk

from pygame import Surface, display, FULLSCREEN, RESIZABLE

from ..Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains the code responsible for the game settings.
"""


class SettingsKeeper(SingletonPattern):
    """
    Reading settings from "settings" file and keep it.
    """
    def __init__(self):
        # Path settings:
        script_root_path: str = path.abspath(__file__)\
            .replace(path.join(*[
                'Scripts', 'Application_layer', 'Settings_Keeper.py'
            ]), '')
        self._user_settings_path: str = f"{script_root_path}{path.join(*['user_settings'])}"

        # Default settings:
        self._game_settings: dict = {
            "system_type": self._system_type(),
            "screen_size": (1280, 720),
            "screen_type": "windowed",
            "general_volume": 100,
            "music_volume": 100,
            "sound_volume": 100,
            "text_language": "eng",
            "voice_acting_language": "eng",
            "frames_per_second": 60
        }

        # Read settings configuration file:
        resave: bool = False
        current_landed_file_game_settings: dict = {}
        try:
            with open(
                    file=self._user_settings_path,
                    mode='r',
                    encoding='utf-8'
            ) as game_settings:
                if game_settings.read().strip() == '':
                    resave: bool = True
                for row in game_settings:
                    try:

                        if "game_settings" in row:
                            continue
                        setting_type_name, setting_value = row.replace('\n', '').split('=')

                        # Windows settings:
                        if setting_type_name == 'screen_size':
                            screen_size_settings: list[str] = setting_value.split('x')
                            current_landed_file_game_settings["screen_size"]: tuple[int, int] = (
                                int(screen_size_settings[0]),
                                int(screen_size_settings[1])
                            )

                        # Sound settings:
                        elif setting_type_name in (
                                "general_volume",
                                "music_volume",
                                "sound_volume"
                        ):
                            current_landed_file_game_settings[setting_type_name]: int = int(setting_value)

                        # Other settings:
                        else:
                            current_landed_file_game_settings[setting_type_name]: str = setting_value

                    except ValueError:
                        resave: bool = True
                        continue

            for setting_type_name in self._game_settings:
                if setting_type_name in (
                        "system_type",
                        "frames_per_second"
                ):
                    continue
                if setting_type_name not in current_landed_file_game_settings:
                    resave: bool = True
                else:
                    self._game_settings[setting_type_name]: str | int | tuple = \
                        current_landed_file_game_settings[setting_type_name]

        except FileExistsError:
            resave: bool = True

        if resave is True:
            self._save_settings()

        # Display settings:
        self._screen: Surface = self._set_windows_settings()

    def get_voice_acting_language(self):
        """
        Used in SoundDirector.
        """
        return self._game_settings["voice_acting_language"]

    def get_text_language(self) -> str:
        """
        Used in StageDirector, ButtonFactory, MenuText, BaseButton
        """
        return self._game_settings["text_language"]

    def get_general_volume(self) -> int:
        """
        Used in SoundDirector.
        """
        return self._game_settings["general_volume"]

    def get_music_volume(self) -> int:
        """
        Used in SoundDirector.
        """
        return self._game_settings["music_volume"]

    def get_sound_volume(self) -> int:
        """
        Used in SoundDirector.
        """
        return self._game_settings["sound_volume"]

    def get_frames_per_second(self) -> int:
        """
        Used in GameMaster.
        """
        return self._game_settings["frames_per_second"]

    def get_system_type(self) -> str:
        """
        Used in program entry point.
        """
        return self._game_settings["system_type"]

    def get_window(self) -> Surface:
        """
        Get "display.set_mode(...)" pygame.Surface with actual settings.
        :return: pygame.Surface
        """
        return self._screen

    def _set_windows_settings(self) -> Surface:
        """
        Generate or set new display mode.
        :return: pygame.display.Surface
        """
        if self._game_settings["screen_type"] == 'full_screen':
            screen_size: Tk = Tk()
            screen_size_x, screen_size_y = \
                screen_size.winfo_screenwidth(), \
                screen_size.winfo_screenheight()
            screen: Surface = display.set_mode(
                (screen_size_x, screen_size_y),
                FULLSCREEN
            )
            return screen

        elif self._game_settings["screen_type"] == 'windowed':
            screen: Surface = display.set_mode(
                self._game_settings["screen_size"],
                RESIZABLE
            )
            return screen

    def update_settings(self):
        """
        Update game settings.
        """
        self._screen: Surface = self._set_windows_settings()
        self._save_settings()

    def _save_settings(self):
        """
        Save new settings to "user_settings" file.
        """
        with open(
                file=self._user_settings_path,
                mode='w',
                encoding='utf-8'
        ) as settings_file:
            settings_file.write(
                "# game_settings:"
            )
            for setting_name, setting_value in self._game_settings.items():
                if setting_name not in (
                        "screen_size",
                        "system_type",
                        "frames_per_second"
                ):
                    settings_file.write(
                        f"\n{setting_name}={str(setting_value)}"
                    )
                elif setting_name == "screen_size":
                    settings_file.write(
                        f"\n{setting_name}={str(setting_value[0])}x{str(setting_value[1])}"
                    )

    @staticmethod
    def _system_type() -> str:
        """
        Return String with system type.
        :return: str
        """
        if platform == "win32" or platform == "win64":
            return 'Windows'
        elif platform == "linux" or platform == "linux2":
            return 'linux'
        elif platform == "darwin":
            return 'Mac_OS'
