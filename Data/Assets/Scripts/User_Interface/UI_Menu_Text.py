from os import path

from pygame import Surface, font, SRCALPHA, transform

from ..Assets_load import json_load, font_load, image_load
font.init()
"""
Contents code for menus text keeper.
"""


class MenuText:
    """
    Generate menus text surface and coordinates for render.

    Instances are created from menus_text_generator function by InterfaceController class.
    """
    def __init__(self, *, background_surface: Surface, menu_name: str, menu_text: str,
                 language_flag: str, menu_text_localization_dict: dict[str], menu_text_font: str or None,
                 menu_text_color: str, menu_text_coordinates: dict[str, int], menu_text_substrate: str or None):
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
        :param menu_text_substrate: Menu text image substrate.
        :type menu_text_substrate: str | None
        """
        # Arguments processing:
        self.background_surface: Surface = background_surface
        self.menu_name: str = menu_name
        self.language_flag: str = language_flag
        self.menu_text: str = menu_text
        self.localisation_menu_text: dict[str] = menu_text_localization_dict
        self.menu_text_coordinates_x: int = menu_text_coordinates['x']
        self.menu_text_coordinates_y: int = menu_text_coordinates['y']
        self.font_size: int = 0
        self.text_color: str = menu_text_color
        if menu_text_font is not None:
            self.font_name: str = menu_text_font
            self.set_text_font: font.Font = font_load(font_name=self.font_name, font_size=self.font_size)
        else:
            self.font_name: None = None
            self.set_text_font: font.Font = font.Font(font.get_default_font(), self.font_size)
        if menu_text_substrate is not None:
            self.menu_text_substrate_standard: Surface = image_load(
                art_name=menu_text_substrate,
                file_format='png',
                asset_type=path.join(
                    *['User_Interface', 'Menu_Substrate']
                ))
            self.menu_text_substrate_sprite: Surface = self.menu_text_substrate_standard
        else:
            self.menu_text_substrate_sprite: None = None

        self.menu_text_surface: Surface = Surface((0, 0), SRCALPHA)
        self.menu_text_coordinates: tuple[int, int] = (0, 0)
        self.menu_text_surface_size: tuple[int, int] = (0, 0)

    def scale(self, *, background_surface):
        """
        Scale menu text for render.
        """
        # Devnull interesting data:
        self.background_surface = background_surface
        self.menu_text_surface_size: tuple[int, int] = (0, 0)
        self.menu_text_coordinates: tuple[int, int] = (0, 0)
        # Set menu lists:
        yes_no_menu_text_list: list = [
            'back_to_start_menu_status_menu',
            'exit_menu',
            'settings_status_menu',
            'creators_menu'
        ]

        # Calculating surface size and text coordinates:
        if self.menu_name in yes_no_menu_text_list:
            self.menu_text_surface_size: tuple[int, int] = (
                (self.background_surface.get_width() // 3),
                (self.background_surface.get_height() // 3)
            )
            self.menu_text_coordinates: tuple[int, int] = (
                (self.background_surface.get_width() // 2) - (self.menu_text_surface_size[0] // 2),
                (self.background_surface.get_height() // 2) - (self.menu_text_surface_size[1] // 2)
            )

        # Surface scale:
        if self.menu_text_substrate_sprite is not None:
            menu_text_substrate_standard: Surface = self.menu_text_substrate_standard
            menu_text_substrate_standard: Surface = transform.scale(
                menu_text_substrate_standard, self.menu_text_surface_size
            )
            self.menu_text_substrate_sprite: Surface = Surface(self.menu_text_surface_size, SRCALPHA)
            self.menu_text_substrate_sprite.blit(menu_text_substrate_standard, (0, 0))
        self.menu_text_surface: Surface = Surface(self.menu_text_surface_size, SRCALPHA)

    def get_text(self) -> tuple[Surface, tuple[int, int]]:
        """
        :return: menu`s object and text coordinates.
        """
        self.text_render()
        return self.menu_text_surface, self.menu_text_coordinates

    def localization_menu_text(self, *, language_flag):
        """
        Localization menu text if it's necessary.

        :param language_flag: String with language flag.
        :type language_flag: str
        """
        self.language_flag: str = language_flag
        self.menu_text: str = self.localisation_menu_text[self.language_flag]

    def text_render(self):
        """
        Render text on text surface, for display image render.
        """
        # Localization menu text:
        self.localization_menu_text(language_flag=self.language_flag)
        self.font_size: int = self.background_surface.get_height() // 50

        # Font reload for size scale:
        if self.font_name is not None:
            self.set_text_font: font.Font = font_load(font_name=self.font_name, font_size=self.font_size)
        else:
            self.set_text_font: font.Font = font.Font(font.get_default_font(), self.font_size)

        # Generate text:
        rows_list: list = []
        for index, row in enumerate(self.menu_text.split('\n')):
            text_surface: Surface = self.set_text_font.render(row, True, self.text_color)
            # Menu surface text coordinates:
            text_coordinates: tuple[int, int] = (
                ((self.menu_text_surface.get_width() // 2) - (text_surface.get_width() // 2))
                * self.menu_text_coordinates_x,

                (((self.menu_text_surface.get_height() // 2) - (text_surface.get_height() // 2))
                 - ((text_surface.get_height() // 2) * (index - 1) * 2))
                * self.menu_text_coordinates_y
            )
            rows_list.append((text_surface, text_coordinates))

        # Render text on substrate if it possible:
        if self.menu_text_substrate_sprite is not None:
            for row in rows_list:
                self.menu_text_substrate_sprite.blit(row[0], row[1])
            self.menu_text_surface.blit(self.menu_text_substrate_sprite, (0, 0))
        else:
            for row in rows_list:
                self.menu_text_surface.blit(row[0], row[1])

    def devnull_text(self):
        self.menu_text_surface: Surface = Surface((0, 0))


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
                menu_text_coordinates=ui_menus_texts_json['coordinates'],
                menu_text_substrate=ui_menus_texts_json['substrate']
            )})

        result.update({file_name: ui_menus_texts})

    return result