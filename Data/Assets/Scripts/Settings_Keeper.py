from os import path
from sys import platform
from tkinter import Tk

from pygame import Surface, display, FULLSCREEN, RESIZABLE
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
        # Path settings:
        script_root_path: str = path.abspath(__file__)\
            .replace(path.join(*['Scripts', 'Settings_Keeper.py']), '')
        self.user_settings_path: str = f"{script_root_path}{path.join(*['user_settings'])}"
        # Read settings configuration file:
        with open(self.user_settings_path, 'r') as game_settings:
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
        # Get system type:
        self.system_type: str = system_type()
        # Display settings:
        self.screen = self.set_windows_settings()

    def get_windows_settings(self):
        return self.screen

    def set_windows_settings(self) -> Surface:
        """
        Generate or set new display mode.
        :result: pygame.display.Surface
        """
        if self.screen_type == 'full_screen':
            screen_size = Tk()
            screen_size_x, screen_size_y = \
                screen_size.winfo_screenwidth(), \
                screen_size.winfo_screenheight()
            screen: Surface = display.set_mode((screen_size_x, screen_size_y), FULLSCREEN)
            return screen
        if self.screen_type == 'windowed':
            screen: Surface = display.set_mode(self.screen_size, RESIZABLE)
            return screen

    def update_settings(self):
        """
        Update game settings.
        """
        self.screen = self.set_windows_settings()
        self.save_settings()

    def save_settings(self):
        """
        Save new settings to "user_settings" file.
        """
        with open(self.user_settings_path, 'w') as settings_file:
            settings_file.write(
                f"# game_settings:\n"
                f"screen_size={self.screen_size[0]}x{self.screen_size[1]}\n"
                f"screen_type={self.screen_type}\n"
                f"general_volume={self.general_volume}\n"
                f"music_volume={self.music_volume}\n"
                f"sound_volume={self.sound_volume}\n"
                f"text_language={self.text_language}\n"
                f"voice_acting_language={self.voice_acting_language}"
            )
