from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Universal_computing.Assets_load import AssetLoader
from ..Application_layer.Settings_Keeper import SettingsKeeper
from .UI_Buttons.UI_Base_Button import BaseButton
from .UI_Buttons.UI_Yes_No_Button import YesNoButton
from .UI_Buttons.UI_Long_Button import LongButton
from .UI_Buttons.UI_Save_Load_Menu_Button import SaveLoadMenuButton
from .UI_Buttons.UI_GamePlay_Reading_Button import GamePlayReadingButton
"""
Contents code for user interface buttons generation.
"""


class ButtonFactory(SingletonPattern):
    """
    Generate interface button surface and coordinates for render as Factory.
    Instances are created from button_generator function by InterfaceController class.
    """
    # Interface collections:
    yes_no_menus: tuple[str] = (
        'exit_menu',
        'settings_status_menu',
        'back_to_start_menu_status_menu'
    )
    long_buttons_menus: tuple[str] = (
        'game_menu',
        'settings_menu',
        'start_menu',
        'creators_menu'
    )
    save_load_menus: tuple[str] = (
        'save_menu',
        'load_menu'
    )
    gameplay_reading: tuple[str] = (
        'gameplay_ui',
    )

    # Buttons collection:
    button_collections: dict[dict[str, BaseButton]] = {
        'yes_no_menus': {
            'button_object': YesNoButton,
            'allowable_menus': yes_no_menus
        },
        'long_buttons_menus': {
            'button_object': LongButton,
            'allowable_menus': long_buttons_menus
        },
        'save_load_menus': {
            'button_object': SaveLoadMenuButton,
            'allowable_menus': save_load_menus
        },
        'gameplay_reading': {
            'button_object': GamePlayReadingButton,
            'allowable_menus': gameplay_reading
        }
    }

    def produce(self, *, button_name: str, button_text: str | None = None, button_image_data: dict[str, int],
                button_text_localization_dict: dict[str] | None = None, have_real_path: bool = False,
                text_offset_x: int | float | None = None, text_offset_y: int | float | None = None) -> BaseButton:
        """
        Generate new Button object.

        :param button_name: String with button image file name.
        :type button_name: str
        :param button_text: String with text of button.
                            None by default.
        :type button_text: str | None
        :param button_image_data: Nested dictionary with button name as key and dictionary with button type,
                                  index order position and sprite name as values.
        :type button_image_data: dict[str, dict[str, int]]
        :param button_text_localization_dict: Dictionary with language flags as keys and localization text as values.
                                              If this parameter is set to 'None', no localization occurs.
                                              None by default.
        :type button_text_localization_dict: dict[str] | None
        :param have_real_path: If this flag is True button_image_data['sprite_name'] will be real path to file.
                               Is not file name.
        :type have_real_path: bool
        :param text_offset_x: Offset of the text inside the button, along the X axis.
                              If set to None, then there will be no offset.
                              The factor to multiply by the parameter is 1/10 of the button size.
                              left -0 | Right +0
                              None by default.
        :type text_offset_x: int | float | None
        :param text_offset_y: Offset of the text inside the button, along the Y axis.
                              If set to None, then there will be no offset.
                              The factor to multiply by the parameter is 1/10 of the button size.
                              Up -0 | Down +0
                              None by default.
        :type text_offset_y: int | float | None
        """
        for value in self.button_collections.values():
            if button_image_data['type'] in value['allowable_menus']:
                new_button: BaseButton = value['button_object'](
                    button_name=button_name,
                    button_text=button_text,
                    button_image_data=button_image_data,
                    button_text_localization_dict=button_text_localization_dict,
                    have_real_path=have_real_path,
                    text_offset_x=text_offset_x,
                    text_offset_y=text_offset_y
                )
                return new_button


def button_generator() -> dict[str, dict[str, BaseButton]]:
    """
    Generate dict with buttons for user interface.
    Use by InterfaceController.
    :return: A nested dictionary of button`s group and an instance of the Button class.
    """
    language_flag: str = SettingsKeeper().text_language
    result: dict = {}
    factory: ButtonFactory = ButtonFactory()
    asset_loader: AssetLoader = AssetLoader()

    # Buttons data:
    ui_buttons_files: tuple[str] = tuple(
        asset_loader.json_load(
            ['Scripts', 'Json_data', 'User_Interface', 'UI_Buttons', 'ui_buttons_data']
        )
    )
    # localizations data:
    localizations_data: tuple[dict] = asset_loader.csv_load(
            file_name='button_menu_localization'
        )
    localizations: tuple = tuple(
            flag
            for flag in localizations_data[0]
            if flag != "button_id"
        )

    # All buttons text localizations:
    all_buttons_text_localizations_dict: dict = {}
    for language in localizations:
        all_buttons_text_localizations_dict.update(
            {
                language: {}
            }
        )
        for row in localizations_data:
            all_buttons_text_localizations_dict[language].update(
                {
                    row["button_id"]: row[language]
                }
            )

    # User Interface buttons:
    for file_name in ui_buttons_files:
        ui_buttons_json: dict[str] = asset_loader.json_load(
            ['Scripts', 'Json_data', 'User_Interface', 'UI_Buttons', "Buttons_config_files", file_name]
        )
        ui_buttons: dict = {}
        for key in ui_buttons_json:

            # Generate text localizations for button:
            button_text_localization: dict = {}
            try:
                for language in all_buttons_text_localizations_dict:
                    button_text_localization.update(
                        {
                            language: all_buttons_text_localizations_dict[language][key]
                        }
                    )
                button_text: str = all_buttons_text_localizations_dict[language_flag][key]
            except KeyError:
                button_text: None = None

            # Generate button:
            ui_buttons.update(
                {
                    key: factory.produce(
                        button_name=key,
                        button_text=button_text,
                        button_image_data=ui_buttons_json[key],
                        button_text_localization_dict=button_text_localization
                    )
                }
            )

        result.update({file_name: ui_buttons})
    return result
