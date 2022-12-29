from os import path
from tkinter import Tk

from pygame import display, RESIZABLE, FULLSCREEN, Surface

from Assets.Scripts.Assets_load import image_load
from Assets.Scripts.Settings_Keeper import SettingsKeeper
from Assets.Scripts.Game_Master import GameMaster
"""
Contains app shell code.
"""

app_name: str = "Visual Novel"


def run():
    """
    Initialization.
    """
    # Set game settings:
    start_settings: SettingsKeeper = SettingsKeeper()
    type_of_system: str = start_settings.system_type
    screen: None = None
    # Display settings:
    screen_size_x, screen_size_y = start_settings.screen_size
    if start_settings.screen_type == 'windowed':
        screen: Surface = display.set_mode((screen_size_x, screen_size_y), RESIZABLE)
    if start_settings.screen_type == 'full_screen':
        screen_size = Tk()
        screen_size_x, screen_size_y = screen_size.winfo_screenwidth(), screen_size.winfo_screenheight()
        screen: Surface = display.set_mode((screen_size_x, screen_size_y), FULLSCREEN)
    # Path to icons:
    path_to_icons: str = path.join(*['UI', 'Icons'])
    # Application name in window:
    display.set_caption(app_name)
    # Window settings:
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
    gameplay = GameMaster(display_screen=screen, start_settings=start_settings)
    gameplay()


if __name__ == '__main__':
    run()
