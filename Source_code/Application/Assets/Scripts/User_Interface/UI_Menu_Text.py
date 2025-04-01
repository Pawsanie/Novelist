from pygame import Surface, font, SRCALPHA, transform

from ..Universal_computing.Assets_load import AssetLoader
from ..Application_layer.Settings_Keeper import SettingsKeeper
from ..Game_objects.Background import Background
from ..Render.Texture_Master import TexturesMaster
from ..Render.Sprite import Sprite
"""
Contents code for menus text keeper.
"""


class MenuText:
    """
    Generate menus text surface and coordinates for render.
    Instances are created from menus_text_generator function by InterfaceController class.
    """
    # Set menu lists:
    _yes_no_menu_text_list: list[str] = [
        'back_to_start_menu_status_menu',
        'exit_menu',
        'settings_status_menu',
    ]
    _back_menu_text_list: list[str] = [
        'creators_menu'
    ]
    _save_and_load_menu_text_list: list[str] = [
        'load_menu',
        'save_menu'
    ]

    def __init__(
            self, *,
            menu_name: str,
            menu_text: str,
            menu_text_localization_dict: dict[str, str] | None,
            menu_text_font: str | None,
            menu_text_color: str,
            menu_text_coordinates: dict[str, int],
            menu_text_substrate: str | None,
            menu_text_factor: int | float = 1
    ):
        """
        :param menu_name: The name of the menu the text is for.
        :param menu_text: Text of the menu.
        :param menu_text_localization_dict: Dictionary with language flags as keys and localization text as values.
                                            If this parameter is None localization will not be made.
        :param menu_text_font: Font name for font asset load.
        :param menu_text_color: Text color.
        :param menu_text_coordinates: Dictionary with str(x|y) as key and int as value.
        :param menu_text_substrate: Menu text image substrate.
        :param menu_text_factor: Scale symbol factor. 1 as default.
        """
        # Program layers settings:
        self._asset_loader: AssetLoader = AssetLoader()
        self._background: Background = Background()
        self._settings_keeper: SettingsKeeper = SettingsKeeper()
        self._texture_master: TexturesMaster = TexturesMaster()

        # Arguments processing:
        self._menu_name: str = menu_name
        self._language_flag: str = self._settings_keeper.get_text_language()
        self._menu_text: str = menu_text
        self._localisation_menu_text: dict[str, str] = menu_text_localization_dict
        self._menu_text_coordinates_x: int = menu_text_coordinates['x']
        self._menu_text_coordinates_y: int = menu_text_coordinates['y']
        self._font_size: int = 0
        self._text_color: str = menu_text_color
        self._menu_text_scale_factor: int = menu_text_factor
        self._menu_text_substrate: str | None = menu_text_substrate

        if menu_text_font is not None:
            self._font_name: str = menu_text_font
            self._set_text_font: font.Font = self._asset_loader.font_load(
                font_name=self._font_name,
                font_size=self._font_size
            )
        else:
            self._font_name: None = None
            self._set_text_font: font.Font = font.Font(
                font.get_default_font(),
                self._font_size
            )

        # Other attributes:
        self._menu_text_coordinates: tuple[int, int] = (0, 0)
        self._menu_text_surface_size: tuple[int, int] = (0, 0)

    def _set_text_surface_size(self):
        """
        Set text Surface size.
        """
        background_size: tuple[int, int] = self._background.get_size()
        background_width, background_height = background_size

        self._menu_text_surface_size: tuple[int, int] = (
            (background_width // 3),
            (background_height // 3)
        )

    def _yes_no_menu_text_coordinates(self):
        """
        Set yes/no menu text coordinates.
        """
        self._set_text_surface_size()
        self._menu_text_coordinates: tuple[int, int] = (
            (self._settings_keeper.get_window().get_width() // 2)
            - (self._menu_text_surface_size[0] // 2),

            (self._settings_keeper.get_window().get_height() // 2)
            - (self._menu_text_surface_size[1] // 2)
        )

    def _back_menu_text_coordinates(self):
        """
        Set menu text coordinates for menus with back button.
        """
        self._set_text_surface_size()
        self._menu_text_coordinates: tuple[int, int] = (
            (self._settings_keeper.get_window().get_width() // 2)
            - (self._menu_text_surface_size[0] // 2),

            (self._settings_keeper.get_window().get_height() // 2)
            - self._menu_text_surface_size[1]
        )

    def _save_and_load_menu_text_coordinates(self):
        """
        Set save/load menu text coordinates.
        Generate text for current save slots page.
        """
        self._set_text_surface_size()
        self._menu_text_coordinates: tuple[int, int] = (

            + (self._settings_keeper.get_window().get_width() // 2)
            - (self._menu_text_surface_size[0] // 2),

            + (self._settings_keeper.get_window().get_height() // 2)
            + (self._menu_text_surface_size[1])
            - (self._menu_text_surface_size[1] // 5)

        )

    def scale(self):
        """
        Scale menu text for render.
        """
        # Calculating surface size and text coordinates:
        if self._menu_name in self._yes_no_menu_text_list:
            self._yes_no_menu_text_coordinates()
        elif self._menu_name in self._back_menu_text_list:
            self._back_menu_text_coordinates()
        elif self._menu_name in self._save_and_load_menu_text_list:
            self._save_and_load_menu_text_coordinates()

    def get_sprite(self) -> Sprite:
        """
        Used in InterfaceController.
        :return: Sprite
        """
        universal_parameters: dict = {
            "texture_type": "User_Interface",
            "texture_name": "Menu_Text",
            "animation_name": "statick_frames",
            "frame": "Menu_Text"
        }
        self._texture_master.devnull_temporary_texture(
            **universal_parameters
        )
        self._texture_master.set_temporary_texture(
            **universal_parameters,
            surface=self._text_render()
        )

        return Sprite(
            name="Menu_Text",
            texture_mame="Menu_Text",
            layer=6,
            coordinates=self._menu_text_coordinates,
            sprite_size=self._menu_text_surface_size,
            sprite_sheet_data={
                "texture_type": "User_Interface",
                "sprite_sheet": False,
                "statick_frames": {
                    "Menu_Text": {}
                }
            }
        )

    def _localization_menu_text(self):
        """
        Localization menu text if it's necessary.
        """
        if self._localisation_menu_text is not None:
            self._language_flag: str = self._settings_keeper.get_text_language()
            self._menu_text: str = self._localisation_menu_text[self._language_flag]

    def _text_render(self) -> Surface:
        """
        Render text on text surface, for display image render.
        """
        # Localization menu text:
        self._localization_menu_text()
        self._font_size: int = int(
            self._background.get_size()[1] // 50
            * self._menu_text_scale_factor
        )

        # Font reload for size scale:
        if self._font_name is not None:
            self._set_text_font: font.Font = self._asset_loader.font_load(
                font_name=self._font_name,
                font_size=self._font_size
            )
        else:
            self._set_text_font: font.Font = font.Font(
                font.get_default_font(),
                self._font_size
            )

        # Generate text:
        menu_text_surface: Surface = Surface(
            self._menu_text_surface_size,
            SRCALPHA
        )
        menu_text_surface_width, menu_text_surface_height = self._menu_text_surface_size
        rows_list: list = []

        for index, row in enumerate(self._menu_text.split('\n')):
            text_surface: Surface = self._set_text_font.render(
                row, True, self._text_color
            )
            # Menu surface text coordinates:
            text_coordinates: tuple[int, int] = (
                (
                        (menu_text_surface_width // 2)
                        - (text_surface.get_width() // 2)
                )
                * self._menu_text_coordinates_x,

                (
                        (
                                (menu_text_surface_height // 2)
                                - (text_surface.get_height() // 2)
                         )
                        - ((text_surface.get_height() // 2) * (index - 1) * 2)
                )
                * self._menu_text_coordinates_y
            )
            rows_list.append(
                (text_surface, text_coordinates)
            )

        # Render text on substrate if it`s possible:
        if self._menu_text_substrate is not None:
            menu_text_substrate_sprite: Surface = Surface(
                self._menu_text_surface_size,
                SRCALPHA
            )
            menu_text_substrate_sprite.blit(
                transform.scale(
                    self._texture_master.get_texture(
                        texture_type="User_Interface",
                        texture_name=self._menu_text_substrate,
                        animation_name="statick_frames",
                        frame=self._menu_text_substrate
                    ),
                    self._menu_text_surface_size
                ),
                (0, 0)
            )
            for text_surface, text_coordinates in rows_list:
                menu_text_substrate_sprite.blit(
                    text_surface,
                    text_coordinates
                )
            menu_text_surface.blit(
                menu_text_substrate_sprite,
                (0, 0)
            )

        # Render text without substrate:
        else:
            for text_surface, text_coordinates in rows_list:
                menu_text_surface.blit(
                    text_surface,
                    text_coordinates
                )

        return menu_text_surface


def menus_text_generator() -> dict[str, dict[str]]:
    """
    Generate all menus text for MenusTextKeeper.
    :return: dict with text.
    """
    language_flag = SettingsKeeper().get_text_language()
    result: dict = {}
    asset_loader: AssetLoader = AssetLoader()

    # Menu`s text files instructions:
    ui_menus_text_files: dict[str, str] = asset_loader.json_load(
        [
            'Scripts', 'Json_data', 'User_Interface', 'UI_Menu_texts', 'ui_menu_text_data'
        ]
    )

    # localizations data:
    localizations_data: tuple[dict] = asset_loader.csv_load(
        file_name="text_menu_localization"
    )
    localizations: tuple = tuple(
        flag
        for flag in localizations_data[0]
        if flag != "text_id"
    )

    # All menus text localizations:
    all_menus_text_localizations_dict: dict = {}
    for language in localizations:
        all_menus_text_localizations_dict.update(
            {
                language: {}
            }
        )
        for row in localizations_data:
            all_menus_text_localizations_dict[language].update(
                {
                    row["text_id"]: row[language]
                }
            )

    # Menu`s texts:
    for file_name in ui_menus_text_files:
        ui_menus_texts_json: dict[str, str | int | dict] = asset_loader.json_load(
            [
                'Scripts', 'Json_data', 'User_Interface', 'UI_Menu_texts', "Text_config_files", file_name
            ]
        )
        ui_menus_texts: dict = {}

        # Generate text localizations for menu text:
        text_name: str = ui_menus_texts_json['text']
        text_type: str = ui_menus_texts_json['type']
        menu_text_localization: dict = {}
        for language in all_menus_text_localizations_dict:
            menu_text_localization.update(
                {
                    language: all_menus_text_localizations_dict[language][text_name]
                }
            )
        menu_text: str = all_menus_text_localizations_dict[language_flag][text_name]

        # Generate menu text:
        ui_menus_texts.update(
            {
                text_type: MenuText(
                    menu_name=text_type,
                    menu_text=menu_text,
                    menu_text_localization_dict=menu_text_localization,
                    menu_text_font=ui_menus_texts_json['font'],
                    menu_text_color=ui_menus_texts_json['color'],
                    menu_text_coordinates=ui_menus_texts_json['coordinates'],
                    menu_text_substrate=ui_menus_texts_json['substrate']
                )
            }
        )

        result.update({file_name: ui_menus_texts})

    return result
