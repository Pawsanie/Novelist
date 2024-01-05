import logging
from os import path

from pygame import display

from Assets.Scripts.Application_layer.Assets_load import image_load
from Assets.Scripts.Application_layer.Settings_Keeper import SettingsKeeper
from Assets.Scripts.Application_layer.Game_Master import GameMaster
from Assets.Scripts.Logging_Config import logging_config, text_for_logging
"""
Contains app shell code.
"""


def run():
    """
    Initialization.
    """
    app_name: str = "Visual Novel"

    icon_set: dict[str] = {
        "Windows": "win_icon",
        "Mac_OS": "mac_icon",
        "linux": "nix_icon"
    }

    # Set game settings:
    start_settings: SettingsKeeper = SettingsKeeper()
    type_of_system: str = start_settings.system_type
    # Path to icons:
    path_to_icons: str = path.join(*[
        'User_Interface', 'Icons'
    ])
    # Application name in window:
    display.set_caption(app_name)
    # Icon settings:
    display.set_icon(image_load(
        art_name=icon_set[type_of_system],
        file_format='png',
        asset_type=path_to_icons
    ))
    # Start game:
    gameplay: GameMaster = GameMaster()
    gameplay()


if __name__ == '__main__':
    logging_config(
        log_path="logg_file.txt",
        log_level=30
    )
    try:
        run()
    except Exception as error:
        logging.critical(
            text_for_logging(
                log_text="The program launch ended with an error!",
                log_error=error
            )
        )
        raise error
