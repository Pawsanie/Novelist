from os import path
from sys import platform
from tkinter import Tk

from pygame import display, RESIZABLE, FULLSCREEN

from Assets.Scripts.Gameplay import gameplay_stage_director_initialization as gameplay
from Assets.Scripts.Assets_load import image_load
"""
Contains app shell code.
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


def read_settings() -> dict[str | int | tuple[int, int]]:
    """
    Reading settings from "settings" file.

    :return: Dict with game settings.
    """
    script_root_path = f"{path.abspath(__file__).replace(path.join(*['Visual_novel_game.py']), '')}"
    user_settings_path = f"{script_root_path}{path.join(*['Assets', 'user_settings'])}"
    start_settings = {}
    with open(user_settings_path) as game_settings:
        for row in game_settings:
            setting_type: list[str] = row.replace('\n', '').split('=')
            if setting_type[0] == 'screen_size':
                screen_size_settings: list[str] = setting_type[1].split('x')
                screen_size: tuple[int, int] = (int(screen_size_settings[0]), int(screen_size_settings[1]))
                start_settings.update({'screen_size': screen_size})
            if setting_type[0] == 'general_volume':
                start_settings.update({'general_volume': setting_type[1]})
            if setting_type[0] == 'music_volume':
                start_settings.update({'music_volume': setting_type[1]})
            if setting_type[0] == 'sound_volume':
                start_settings.update({'sound_volume': setting_type[1]})
            if setting_type[0] == 'screen_type':
                start_settings.update({'screen_type': setting_type[1]})
            if setting_type[0] == 'language':
                start_settings.update({'language': setting_type[1]})
    return start_settings


def run():
    """
    Initialization.
    """
    # Set game settings:
    type_of_system: str = system_type()
    game_settings: dict[str | int | tuple[int, int]] = read_settings()
    screen = None
    # Display settings:
    screen_size_x, screen_size_y = game_settings['screen_size']
    if game_settings['screen_type'] == 'windowed':
        screen = display.set_mode((screen_size_x, screen_size_y), RESIZABLE)
    if game_settings['screen_type'] == 'full_screen':
        screen_size = Tk()
        screen_size_x, screen_size_y = screen_size.winfo_screenwidth(), screen_size.winfo_screenheight()
        screen = display.set_mode((screen_size_x, screen_size_y), FULLSCREEN)
    # Path to icons:
    path_to_icons = path.join(*['UI', 'Icons'])
    # Window settings:
    display.set_caption("Visual Novel")
    if type_of_system == 'Windows':
        display.set_icon(image_load(art_name='win_icon',
                                    file_format='png',
                                    asset_type=path_to_icons))
    # Mac settings:
    if type_of_system == 'Mac_OS':
        display.set_icon(image_load(art_name='mac_icon',
                                    file_format='png',
                                    asset_type=path_to_icons))
    # Unix settings:
    if type_of_system == 'linux':
        display.set_icon(image_load(art_name='nix_icon',
                                    file_format='png',
                                    asset_type=path_to_icons))
    # Start game:
    gameplay(display_screen=screen)


if __name__ == '__main__':
    run()
