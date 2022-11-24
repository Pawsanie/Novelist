from os import path

from pygame import Surface, SRCALPHA, transform, mouse

from .Assets_load import image_load, json_load
from .Render import surface_size, button_size
"""
Contents code for user interface buttons.
"""


class Button:
    """
    Generate interface button surface and coordinates for render.

    :param background_surface: pygame.Surface of background.
    :type background_surface: Surface
    :param button_name: String with button image file name.
    :type button_name: str
    :param button_text: String with text of button.
    :type button_text: str | None
    :param place_flag: Dictionary with button type string as a key and order int as value.
    :type place_flag: dict[str, dict[str, int]]
    """
    def __init__(self, *, background_surface: Surface, button_name: str,
                 button_text: str | None, place_flag: dict[str, int],
                 language_flag: str, button_text_localization_dict: dict[str]):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface
        :param button_name: String with button image file name.
        :type button_name: str
        :param button_text: String with text of button.
        :type button_text: str | None
        :param place_flag: Dictionary with button type string as a key and order int as value.
        :type place_flag: dict[str, int]
        :param language_flag:
        :type language_flag:
        :param button_text_localization_dict:
        :type button_text_localization_dict:
        """
        self.background_surface: Surface = background_surface
        self.button_name: str = button_name
        self.button_text: str | None = button_text
        self.language_flag = language_flag
        self.button_text_localization_dict = button_text_localization_dict

        # Generate button image:
        self.button_sprite_standard: Surface = image_load(
            art_name=self.button_name,
            file_format='png',
            asset_type=path.join(*['UI', 'Buttons']))
        self.button_sprite: Surface = self.button_sprite_standard

        # Generate button surface:
        self.button_size: tuple[int, int] = button_size(
            place_flag=place_flag['type'],
            background_surface=self.background_surface)
        self.button_surface: Surface = Surface(self.button_size, SRCALPHA)

        # Generate button coordinates:
        self.button_coordinates: tuple[int, int] = (0, 0)
        self.place_flag: dict[str, int] = place_flag
        self.coordinates(background_surface=self.background_surface)

        # Button image render:
        self.button_sprite = transform.scale(self.button_sprite, self.button_size)
        self.button_surface.blit(self.button_sprite, (0, 0))

    def generator(self):
        """
        Generate button surface and coordinates for render.
        """
        return self.button_surface, self.button_coordinates

    def scale(self, *, background_surface):
        """
        Scale button surface, with background context.

        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface.
        """
        # Arg parse:
        self.background_surface = background_surface

        # Button size scale:
        self.button_sprite: Surface = self.button_sprite_standard
        self.button_size: tuple[int, int] = button_size(
            place_flag=self.place_flag['type'],
            background_surface=self.background_surface)
        self.button_sprite = transform.scale(self.button_sprite, self.button_size)
        self.button_surface: Surface = transform.scale(self.button_surface, self.button_size)

        # Scale coordinates:
        self.coordinates(background_surface=self.background_surface)

        # Default button render:
        if self.button_cursor_position_status() is False:
            self.button_surface.blit(self.button_sprite, (0, 0))

        # Button ready to be pressed:
        else:
            # self.button_surface.blit(self.button_sprite, (0, 0))
            self.button_surface.fill((0, 0, 0))  # <---------------- Remake after tests

    def reflect(self):
        """
        Reflect button sprite surface.
        Reflect methode must be after scale methode in prerender loop.
        """
        self.button_surface: Surface = transform.flip(
            self.button_surface,
            flip_x=True,
            flip_y=False)

    def coordinates(self, *, background_surface: Surface):
        """
        Generate coordinates.

        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface.
        """
        self.background_surface = background_surface
        place_flag = self.place_flag
        button_coordinates_x, button_coordinates_y = (0, 0)
        background_surface_size: list[int, int] = surface_size(interested_surface=self.background_surface)
        background_surface_size_x_middle = background_surface_size[0]//2
        background_surface_size_y_middle = background_surface_size[1]//2

        if place_flag['type'] == 'gameplay_ui':
            # X:
            button_coordinates_x: int = \
                (background_surface_size_x_middle - (self.button_size[0]//2)) + \
                (self.button_size[0] * place_flag['index_number'])
            # Y:
            button_coordinates_y: int = background_surface_size[1] - self.button_size[1]

        if place_flag['type'] == 'game_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'start_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'save_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'load_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'exit_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'settings_menu':
            # X:
            # Y:
            ...

        self.button_coordinates = (button_coordinates_x, button_coordinates_y)

    def button_text(self, language_flag: str):
        """
        Generate text on button if it's necessary.
        """
        if self.button_text is not None:
            ...

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

    def button_clicked_status(self) -> bool:
        """
        Check left click of mouse to button status.

        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()
            if button_clicked[0] is True:
                return True


def button_generator(language_flag: str, background_surface: Surface) -> dict[str, dict[str, Button]]:
    """
    Generate dict with buttons for user interface.

    :return: A nested dictionary of buttons group and an instance of the Button class.
    """
    result, ui_buttons_json = {}, {}
    # Tuple with user interface button`s json file`s names:
    ui_buttons_files: tuple = (
        'ui_exit_menu_buttons',
        'ui_game_menu_buttons',
        'ui_gameplay_buttons',
        'ui_load_menu_buttons',
        'ui_save_menu_buttons',
        'ui_setting_menu_buttons',
        'ui_setting_status',
        'ui_start_menu_buttons')

    localizations: tuple = (
        'eng',
        'ru')

    # Buttons text:
    buttons_text_localization_dict = {}
    for localization in localizations:
        buttons_text_localization_dict.update(
            {localization: json_load(['Scripts', 'Json_data', 'UI', 'Localization', language_flag])})
    # Remake key sort for buttons to {"Lang": text} in localization dict.

    # User Interface buttons:
    for file_name in ui_buttons_files:
        ui_buttons_json: dict = json_load(['Scripts', 'Json_data', 'UI', file_name])
        ui_buttons = {}
        for key in ui_buttons_json:
            ui_buttons.update(
                {key: Button(
                    background_surface=background_surface,
                    button_name=key,
                    button_text=None,
                    place_flag=ui_buttons_json[key],
                    language_flag=language_flag,
                    button_text_localization_dict=buttons_text_localization_dict
                )})
        result.update({file_name: ui_buttons})
    return result
