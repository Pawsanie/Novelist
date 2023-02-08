from pygame import Surface

from ..Assets_load import json_load
"""
Contents code for menus text keeper.
"""


class MenuText:
    """
    Keep menus text.
    """
    def __init__(self, *, background_surface: Surface, menu_name: str, menu_text: str,
                 language_flag: str, menu_text_localization_dict: dict[str]):
        # Arguments processing:
        self.background_surface: Surface = background_surface
        self.menu_name: str = menu_name
        self.language_flag: str = language_flag
        self.menu_text: str = menu_text
        self.localisation_menu_text: dict[str] = menu_text_localization_dict

    def get_text(self) -> str:
        """
        :return: menu`s str
        """
        return self.localisation_menu_text[self.language_flag]


def menus_text_generator(language_flag: str, background_surface: Surface) -> dict[str, dict[str]]:
    """
    Generate all menus text for MenusTextKeeper.

    :param language_flag: String with language flag.
    :type language_flag: str
    :param background_surface: Surface of background.
    :type background_surface: pygame.Surface

    :return: dict with text.
    """
    result: dict = {}

    # localizations instructions from 'ui_menu_text_localizations_data.json': Menus text files and localisation data.
    localizations_data: dict[str] = json_load(
        ['Scripts', 'Json_data', 'User_Interface', 'UI_Menu_texts', 'Localization', 'ui_menu_text_localizations_data']
    )

    # localizations data:
    ui_menus_text_files: tuple[str] = (
        localizations_data['ui_menus_text_files']
    )
    localizations: tuple[str] = (
        localizations_data['localizations']
    )

    # All menus text localizations:
    all_menus_text_localizations_dict: dict = {}
    for language in localizations:
        all_menus_text_localizations_dict.update(
            {language: json_load(
                ['Scripts', 'Json_data', 'User_Interface', 'UI_Menu_texts', 'Localization', language]
            )}
        )

    # Menu`s texts:
    for file_name in ui_menus_text_files:
        ui_menus_texts_json: dict[str] = json_load(
            ['Scripts', 'Json_data', 'User_Interface', 'UI_Menu_texts', file_name]
        )
        ui_menus_texts: dict = {}

        # Generate text localizations for menu text:
        text_name: str = ui_menus_texts_json['text']
        text_type: str = ui_menus_texts_json['type']
        menu_text_localization: dict = {}
        for language in all_menus_text_localizations_dict:
            menu_text_localization.update(
                {language: all_menus_text_localizations_dict[language][text_name]}
            )
        menu_text: str = all_menus_text_localizations_dict[language_flag][text_name]

        # Generate menu text:
        ui_menus_texts.update(
            {text_type: MenuText(
                background_surface=background_surface,
                menu_name=text_type,
                menu_text=menu_text,
                language_flag=language_flag,
                menu_text_localization_dict=menu_text_localization
            )})

        result.update({file_name: ui_menus_texts})

    return result
