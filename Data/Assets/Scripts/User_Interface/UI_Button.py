from os import path

from pygame import Surface, SRCALPHA, transform, mouse, font, MOUSEBUTTONUP

from ..Application_layer.Assets_load import image_load, json_load, font_load
from ..Universal_computing.Surface_size import surface_size
from .UI_buttons_calculations import button_size
from ..Game_objects.Background import BackgroundProxy
from ..Application_layer.Settings_Keeper import SettingsKeeper
font.init()
"""
Contents code for user interface buttons.
Path of code of user interface buttons in 'UI_buttons_calculations.py' file...
"""


class Button:
    """
    Generate interface button surface and coordinates for render.

    Instances are created from button_generator function by InterfaceController class.
    """
    # Interface collections:
    yes_no_menus: tuple[str] = [
        'exit_menu',
        'settings_status_menu',
        'back_to_start_menu_status_menu'
    ]
    long_buttons_menus: tuple[str] = [
        'game_menu',
        'settings_menu',
        'start_menu',
        'creators_menu'
    ]
    save_load_menus: tuple[str] = [
        'save_menu',
        'load_menu',
    ]
    save_and_load_cell: tuple[str] = [
        'save_and_load_cell'
    ]
    gameplay_ui: tuple[str] = [
        'gameplay_ui'
    ]
    gameplay_dialogues_choice: tuple[str] = [
        'gameplay_dialogues_choice'
    ]

    # Tuple with RBG for button select render:
    button_selected_color: tuple[int] = (100, 0, 0)

    def __init__(self, *, button_name: str, button_text: str | None = None, button_image_data: dict[str, int],
                 button_text_localization_dict: dict[str] | None = None, have_real_path: bool = False,
                 text_offset_x: int | float | None = None, text_offset_y: int | float | None = None):
        """
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
        self.background: BackgroundProxy = BackgroundProxy()
        self.button_name: str = button_name
        self.button_text: str | None = button_text
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.language_flag: str = self.settings_keeper.text_language
        self.button_text_localization_dict: dict[str] | None = button_text_localization_dict
        if self.button_text_localization_dict is not None:
            self.localization_button_text()
        self.button_image_data: dict[str | int] = button_image_data

        self.text_offset_x: int | float = text_offset_x
        self.text_offset_y: int | float = text_offset_y

        # Generate button image:
        if have_real_path is False:
            self.button_sprite_standard: Surface = image_load(
                art_name=str(self.button_image_data['sprite_name']),
                file_format='png',
                asset_type=path.join(*['User_Interface', 'Buttons'])
            )
        else:  # TODO: Simplify this block...
            self.button_sprite_standard: Surface = image_load(
                art_name=str(self.button_image_data['sprite_name']),
                file_format='png',
                is_art_name_is_path=True
            )
        self.button_sprite: Surface = self.button_sprite_standard

        # Generate button surface:
        self.button_size: tuple[int, int] = button_size(
            place_flag=button_image_data['type'],
            background_surface=self.background.get_data()[0]
        )
        self.button_surface: Surface = Surface(self.button_size, SRCALPHA)

        # Generate button coordinates:
        self.button_coordinates: tuple[int, int] = (0, 0)

        # Button image render:
        self.button_sprite: Surface = transform.scale(self.button_sprite, self.button_size)
        self.button_surface.blit(self.button_sprite, (0, 0))

        # Button text:
        if self.button_text is not None:
            self.font_size: int = 0
            self.text_color: str = str(self.button_image_data['color'])
            if self.button_image_data['font'] is not None:
                self.font_name: str = str(self.button_image_data['font'])
                self.set_button_font: font.Font = font_load(font_name=self.font_name, font_size=self.font_size)
            else:
                self.font_name: None = None
                self.set_button_font: font.Font = font.Font(font.get_default_font(), self.font_size)

    def generator(self) -> tuple[Surface, tuple[int, int]]:
        """
        Generate button surface and coordinates for render.
        """
        return self.button_surface, self.button_coordinates

    def scale(self):
        """
        Scale button surface, with background context.
        """
        # Arg parse:
        background_surface: Surface = self.background.get_data()[0]

        # Devnull button_surface for new render:
        self.button_surface = Surface((0, 0), SRCALPHA)

        # Button size scale:
        self.button_sprite: Surface = self.button_sprite_standard
        self.button_size: tuple[int, int] = button_size(
            place_flag=self.button_image_data['type'],
            background_surface=background_surface
        )
        self.button_sprite: Surface = transform.scale(self.button_sprite, self.button_size)
        self.button_surface: Surface = transform.scale(self.button_surface, self.button_size)

        # Scale coordinates:
        self.coordinates()

        # Button text scale and render:
        if self.button_text is not None:
            self.button_text_render()

        # Default button render:
        if self.button_cursor_position_status() is False:
            self.button_surface.blit(self.button_sprite, (0, 0))
        # Button ready to be pressed:
        else:
            # Mask settings:
            screen_mask: Surface = Surface(
                [self.button_surface.get_width(), self.button_surface.get_height()]
            )
            screen_mask.fill(self.button_selected_color)
            screen_mask.set_alpha(150)
            # Button render:
            self.button_surface.blit(self.button_sprite, (0, 0))
            self.button_surface.blit(screen_mask, (0, 0))

    def reflect(self):
        """
        Reflect button sprite surface.
        Reflect methode must be after scale methode in prerender loop.
        """
        self.button_surface: Surface = transform.flip(
            self.button_surface,
            flip_x=True,
            flip_y=False
        )

    def menu_yes_no_coordinates(self):
        """
        Coordinates for exit menu and settings status menu buttons.
        """
        place_flag: int = self.button_image_data['index_number']
        button_middle_x, button_middle_y = self.button_middle_point_coordinates()
        background_y = self.background_surface_size()[1]

        # X:
        button_coordinates_x: int = int(
            button_middle_x
            - (self.button_size[0] // 2)
            + (self.button_size[0] * place_flag)
        )
        # Y:
        button_coordinates_y: int = (
                button_middle_y
                + (background_y // 4)
        )
        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def menu_long_buttons_coordinates(self, *, multiplier: int = 3):
        """
        Coordinates for start menu and settings menu buttons.
        """
        place_flag: int = self.button_image_data['index_number']
        button_middle_x, button_middle_y = self.button_middle_point_coordinates()

        # X:
        button_coordinates_x: int = (
                button_middle_x
                - (self.button_size[0] // 2)
        )
        # Y:
        button_coordinates_y: int = (
                button_middle_y
                - (self.button_size[1] // 2)
                + (self.button_size[1] * place_flag)
        )
        if multiplier != 0:
            button_coordinates_y: int = (
                button_coordinates_y
                - (self.button_size[1] * multiplier)
                )
        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def menu_save_and_load_coordinates(self):
        """
        Coordinates for save menu and load menu buttons.
        """
        place_flag: int = self.button_image_data['index_number']
        button_middle_x, button_middle_y = self.button_middle_point_coordinates()
        background_x, background_y = self.background_surface_size()

        # X:
        button_coordinates_x: int = int(
                button_middle_x
                + (self.button_size[0] * place_flag)
                + (background_x // 4)
        )
        # Y:
        button_coordinates_y: int = (
                button_middle_y
                + (background_y // 3)
        )
        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def menu_save_and_load_cell_coordinates(self):
        """
        Coordinates for save menu and load menu Save Cells buttons.
        """
        row, column = self.button_image_data['index_number']
        background: tuple[Surface, tuple[int, int]] = self.background.get_data()
        background_width, background_x = background[0].get_width(), background[1][0]
        background_height, background_y = background[0].get_height(), background[1][1]

        # X:
        button_coordinates_x: int = int(
            + background_x
            + (background_width // 4)
            + ((self.button_size[0] * 1.5) * column)
            - (self.button_size[0] // 2)
            - (self.button_size[0] * 2)
        )
        # Y:
        button_coordinates_y: int = int(
                + background_y
                + (background_height // 3)
                + ((self.button_size[1] * 1.5) * row)
                - (self.button_size[1] // 2)
                - (self.button_size[1] * 2.5)
        )

        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def gameplay_dialogues_choice_coordinates(self, *, multiplier: int = 2):
        """
        Coordinates for gameplay dialogues choice buttons.
        """
        place_flag: int = self.button_image_data['index_number']
        button_middle_x, button_middle_y = self.button_middle_point_coordinates()

        # X:
        button_coordinates_x: int = (
                button_middle_x
                - (self.button_size[0] // 2)
        )
        # Y:
        button_coordinates_y: int = (
                button_middle_y
                - (self.button_size[1] // 2)
                + ((self.button_size[1] * 2) * place_flag)
        )
        if multiplier != 0:
            button_coordinates_y: int = (
                    button_coordinates_y
                    - (self.button_size[1] * multiplier)
            )
        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def gameplay_reading_coordinates(self):
        """
        Coordinates for reading gameplay buttons.
        """
        place_flag: int = self.button_image_data['index_number']
        button_middle_x, button_middle_y = self.button_middle_point_coordinates()
        background_y = self.background_surface_size()[1]

        # X:
        button_coordinates_x: int = (
                button_middle_x
                - (self.button_size[0] // 2)
                + (self.button_size[0] * place_flag)
                )
        # Y:
        button_coordinates_y: int = (
                button_middle_y
                + (background_y // 2)
                - self.button_size[1]
        )
        # Result:
        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def button_middle_point_coordinates(self) -> tuple[int, int]:
        """
        Calculate button middle points coordinates.
        """
        screen_x = self.settings_keeper.screen.get_width()
        screen_y = self.settings_keeper.screen.get_height()

        button_middle_x: int = screen_x // 2
        button_middle_y: int = screen_y // 2

        return button_middle_x, button_middle_y

    def background_surface_size(self) -> list[int, int]:
        """
        Calculate background surface size.
        """
        background_data = self.background.get_data()
        background_surface: Surface = background_data[0]

        background_surface_size: list[int, int] = surface_size(interested_surface=background_surface)
        return background_surface_size

    def coordinates(self):
        """
        Generate coordinates.
        """
        menu_type: str = self.button_image_data['type']

        if menu_type in self.gameplay_ui:
            self.gameplay_reading_coordinates()
            return

        if menu_type in self.gameplay_dialogues_choice:
            self.gameplay_dialogues_choice_coordinates()
            return

        if menu_type in self.long_buttons_menus:
            self.menu_long_buttons_coordinates()
            return

        if menu_type in self.yes_no_menus:
            self.menu_yes_no_coordinates()
            return

        if menu_type in self.save_load_menus:
            self.menu_save_and_load_coordinates()
            return

        if menu_type in self.save_and_load_cell:
            self.menu_save_and_load_cell_coordinates()
            return

    def localization_button_text(self):
        """
        Localization text of button if it's necessary.

        """
        if self.button_text is not None:
            self.language_flag: str = self.settings_keeper.text_language
            self.button_text: str = self.button_text_localization_dict[self.language_flag]

    def button_text_render(self):
        """
        Generate text on button if it's necessary.
        """
        # Localization button text:
        if self.button_text_localization_dict is not None:
            self.localization_button_text()

        self.font_size: int = self.background.get_data()[0].get_height() // 50

        # Font reload for size scale:
        if self.font_name is None:
            self.set_button_font: font.Font = font.Font(
                font.get_default_font(),
                self.font_size
            )
        else:
            self.set_button_font: font.Font = font_load(
                font_name=self.font_name,
                font_size=self.font_size
            )
        text_surface: Surface = self.set_button_font.render(self.button_text, True, self.text_color)

        # Button text coordinates:
        button_text_coordinates: tuple[int, int] = self.button_text_coordinates(text_surface)
        # Button text render:
        self.button_sprite.blit(text_surface, button_text_coordinates)

    def button_text_coordinates(self, text_surface: Surface) -> tuple[int, int]:
        """
        Calculates the coordinates of the text on the button sprite.
        :param text_surface: Text Surface.
        :type text_surface: Surface
        :return: tuple[int, int]
        """
        if self.text_offset_x is None and self.text_offset_y is None:
            result: tuple[int, int] = (
                (self.button_surface.get_width() // 2) - (text_surface.get_width() // 2),
                (self.button_surface.get_height() // 2) - (text_surface.get_height() // 2)
            )
        else:
            if self.text_offset_x is None:
                text_offset_x: int = 0
            else:
                text_offset_x: int = self.text_offset_x
            if self.text_offset_y is None:
                text_offset_y: int = 0
            else:
                text_offset_y: int = self.text_offset_y

            result: tuple[int, int] = (
                int(
                 (self.button_surface.get_width() // 2)
                 - (text_surface.get_width() // 2)
                 + ((self.button_surface.get_width() // 10) * text_offset_x)
                ),
                int(
                    (self.button_surface.get_height() // 2)
                    - (text_surface.get_height() // 2)
                    + ((self.button_surface.get_height() // 10) * text_offset_y)
                )
            )
        return result

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.

        :return: True | False
        """
        # Mouse processing:
        cursor_position: tuple[int, int] = mouse.get_pos()
        # Button processing:
        button_x_size, button_y_size = surface_size(self.button_surface)
        button_coordinates_x, button_coordinates_y = self.button_coordinates

        # Drawing a button while hovering over:
        if button_coordinates_x < cursor_position[0] < button_coordinates_x + button_x_size and \
                button_coordinates_y < cursor_position[1] < button_coordinates_y + button_y_size:
            return True
        # Default Button Rendering:
        else:
            return False

    def button_click_hold(self) -> bool:
        """
        Check left click of mouse to button status.

        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()
            if button_clicked[0] is True:
                return True

    def button_clicked_status(self, event) -> bool:
        """
        Check left push out mouse left button status.

        :param event: pygame.event element.
        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            if event.type == MOUSEBUTTONUP and event.button == 1:  # event.button return int of button type.
                return True


def button_generator() -> dict[str, dict[str, Button]]:
    """
    Generate dict with buttons for user interface.
    Used by InterfaceController.

    :return: A nested dictionary of button`s group and an instance of the Button class.
    """
    language_flag: str = SettingsKeeper().text_language
    result: dict = {}

    # localizations instructions from 'ui_buttons_localizations_data.json': UI files and languages for UI.
    localizations_data: dict[str] = json_load(
        ['Scripts', 'Json_data', 'User_Interface', 'UI_Buttons', 'Localization', 'ui_buttons_localizations_data']
    )

    # localizations data:
    ui_buttons_files: tuple[str] = (
        localizations_data['ui_buttons_files']
    )
    localizations: tuple[str] = (
        localizations_data['localizations']
    )

    # All buttons text localizations:
    all_buttons_text_localizations_dict: dict = {}
    for language in localizations:
        all_buttons_text_localizations_dict.update(
            {language: json_load(
                ['Scripts', 'Json_data', 'User_Interface', 'UI_Buttons', 'Localization', language]
            )}
        )

    # User Interface buttons:
    for file_name in ui_buttons_files:
        ui_buttons_json: dict[str] = json_load(
            ['Scripts', 'Json_data', 'User_Interface', 'UI_Buttons', file_name]
        )
        ui_buttons: dict = {}
        for key in ui_buttons_json:

            # Generate text localizations for button:
            button_text_localization: dict = {}
            try:
                for language in all_buttons_text_localizations_dict:
                    button_text_localization.update(
                        {language: all_buttons_text_localizations_dict[language][key]}
                    )
                button_text: str = all_buttons_text_localizations_dict[language_flag][key]
            except KeyError:
                button_text: None = None

            # Generate button:
            ui_buttons.update(
                {key: Button(
                    button_name=key,
                    button_text=button_text,
                    button_image_data=ui_buttons_json[key],
                    button_text_localization_dict=button_text_localization
                )})

        result.update({file_name: ui_buttons})
    return result
