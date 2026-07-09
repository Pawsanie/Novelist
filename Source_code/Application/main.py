from logging import critical

from pygame import display

from Source_code.Application.Assets.Scripts.Python.Universal_computing.Assets_load import AssetLoader
from Source_code.Application.Assets.Scripts.Python.Core.Settings_Keeper import SettingsKeeper
from Source_code.Application.Assets.Scripts.Python.Core.Game_Master import GameMaster
from Source_code.Application.Assets.Scripts.Python.Logging_Config import logging_config, text_for_logging
"""
Contains app shell code.
"""


def run():
    """
    Initialization.
    """
    app_name: str = "Visual Novel"

    icon_set: dict[str, str] = {
        "Windows": "win_icon",
        "Mac_OS": "mac_icon",
        "linux": "nix_icon"
    }

    # Set game settings:
    type_of_system: str = SettingsKeeper().get_system_type()
    # Application name in window:
    display.set_caption(app_name)
    # Icon settings:
    display.set_icon(
        AssetLoader()
        .image_load(
            art_name=icon_set[type_of_system],
            asset_type="User_Interface",
            file_catalog='Icons'
        )
    )
    # Start game:
    GameMaster()()


if __name__ == '__main__':
    logging_config(
        log_path="log_file.txt",
        log_level=30
    )
    try:
        run()
    except Exception as error:
        critical(
            text_for_logging(
                log_text="The program launch ended with an error!",
                log_error=error
            )
        )
        raise error
