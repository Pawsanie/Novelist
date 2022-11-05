from os import path
from sys import platform
from tkinter import Tk

from pygame import display, RESIZABLE, FULLSCREEN

from Assets.Scripts.Gameplay import gameplay_stage_director_initialization as gameplay
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


def read_settings() -> dict[str or int or tuple[int, int]]:
    """
    Reading settings from "settings" file.

    :return: Dict with game settings.
    """
    script_root_path = f"{path.abspath(__file__).replace(path.join(*['Visual_novel_game.py']), '')}"
    user_settings_path = f"{script_root_path}{path.join(*['Assets', 'user_settings'])}"
    start_settings = {}
    with open(user_settings_path) as game_settings:
        for row in game_settings:
            row = row.replace('\n', '').split('=')
            if row[0] == 'screen_size':
                screen_size_settings: list = row[1].split('x')
                screen_size: tuple[int, int] = (int(screen_size_settings[0]), int(screen_size_settings[1]))
                start_settings.update({'screen_size': screen_size})
            if row[0] == 'general_volume':
                start_settings.update({'general_volume': row[1]})
            if row[0] == 'music_volume':
                start_settings.update({'music_volume': row[1]})
            if row[0] == 'sound_volume':
                start_settings.update({'sound_volume': row[1]})
            if row[0] == 'screen_type':
                start_settings.update({'screen_type': row[1]})
            if row[0] == 'language':
                start_settings.update({'language': row[1]})
    return start_settings


def run():
    """
    Initialization.
    """
    # Set game settings:
    type_of_system: str = system_type()
    game_settings: dict = read_settings()
    screen = None
    # Display settings:
    screen_size_x, screen_size_y = game_settings['screen_size']
    if game_settings['screen_type'] == 'windowed':
        screen = display.set_mode((screen_size_x, screen_size_y), RESIZABLE)
    if game_settings['screen_type'] == 'full_screen':
        screen_size = Tk()
        screen_size_x, screen_size_y = screen_size.winfo_screenwidth(), screen_size.winfo_screenheight()
        screen = display.set_mode((screen_size_x, screen_size_y), FULLSCREEN)
    # Window settings:
    display.set_caption("Visual Novel")
    # if type_of_system == 'Windows':
    #     display.set_icon()
    # if type_of_system == 'Mac_OS':
    #     display.set_icon()
    # if type_of_system == 'linux':
    #     display.set_icon()
    # Start game:
    gameplay(display_screen=screen)


if __name__ == '__main__':
    run()
