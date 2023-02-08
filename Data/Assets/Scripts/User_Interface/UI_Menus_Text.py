from pygame import Surface, font

from ..Assets_load import json_load, font_load
font.init()
"""
Contents code for menus text keeper.
"""


class MenuText:
    """
    Keep menus text.
    """
    def __init__(self, *, background_surface: Surface, menu_name: str, menu_text: str,
                 language_flag: str, menu_text_localization_dict: dict[str], menu_text_font: str or None,
                 menu_text_color: str, menu_text_coordinates: dict[str, int]):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface
        :param menu_name: The name of the menu the text is for.
        :type menu_name: str
        :param menu_text: Text of the menu.
        :type menu_text: str
        :param language_flag: String with language flag.
        :type language_flag: str
        :param menu_text_localization_dict: Dictionary with language flags as keys and localization text as values.
        :type menu_text_localization_dict: dict[str]
        :param menu_text_font: Font name for font asset load.
        :type menu_text_font: str | None
        :param menu_text_color: Text color.
        :type menu_text_color: str
        :param menu_text_coordinates: Dictionary with str(x|y) as key and int as value.
        :type menu_text_coordinates: dict[str, int]
        """
        # Arguments processing:
        self.background_surface: Surface = background_surface
        self.menu_name: str = menu_name
        self.language_flag: str = language_flag
        self.menu_text: str = menu_text
        self.localisation_menu_text: dict[str] = menu_text_localization_dict
        self.menu_text_coordinates_x = menu_text_coordinates['x']
        self.menu_text_coordinates_y = menu_text_coordinates['y']
        self.font_size: int = 0
        self.text_color: str = menu_text_color
        self.text_font: str or None = menu_text_font
        if self.text_font is not None:
            self.font_name: str = self.text_font
            self.set_button_font: font.Font = font_load(font_name=self.font_name, font_size=self.font_size)

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
                menu_text_localization_dict=menu_text_localization,
                menu_text_font=ui_menus_texts_json['font'],
                menu_text_color=ui_menus_texts_json['color'],
                menu_text_coordinates=ui_menus_texts_json['coordinates']
            )})

        result.update({file_name: ui_menus_texts})

    return result
