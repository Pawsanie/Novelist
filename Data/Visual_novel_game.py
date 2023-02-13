from os import path

from pygame import display

from Assets.Scripts.Assets_load import image_load
from Assets.Scripts.Settings_Keeper import SettingsKeeper
from Assets.Scripts.Game_Master import GameMaster
from Assets.Scripts.Logging_Config import logging_config
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
    # Path to icons:
    path_to_icons: str = path.join(*['User_Interface', 'Icons'])
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
    gameplay = GameMaster(start_settings=start_settings)
    gameplay()


if __name__ == '__main__':
    logging_config(
        log_path="logg_file.txt",
        log_level=30
    )
    run()
