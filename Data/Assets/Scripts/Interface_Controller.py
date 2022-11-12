from pygame import Surface

from .UI_Button import button_generator
# from .UI_Text_Canvas import TextCanvas
from .Render import surface_size
"""
Contents code for user interface controller.
"""


class InterfaceController:
    """
    Generate user interface: text canvas, buttons, menu and control it.

    :param background_surface: pygame.Surface of background.
    :type background_surface: Surface
    :param language_flag: String with language flag for button text localization..
    :type language_flag: str
    """
    def __init__(self, *, background_surface: Surface, language_flag: str):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface
        :param language_flag: String with language flag for button text localization..
        :type language_flag: str
        """
        # Parse args:
        self.background_surface: Surface = background_surface
        self.language_flag: str = language_flag
        # Generate buttons:
        self.buttons_dict: dict = button_generator(
            language_flag=language_flag,
            background_surface=self.background_surface)
        # Text canvas:
        # self.text_canvas = TextCanvas(background_surface=self.background_surface)
        # self.text_canvas_surface: Surface = self.text_canvas.generator()[0]
        # Game settings menu:
        self.settings_menu_background = Surface(surface_size(self.background_surface))
        self.settings_menu_background.set_alpha(128)
        self.settings_menu_canvas = ...
        # In game user interface:
        self.active_game_interface_flag = 'on'  # "on/off" and "on" as default.

    def ui_gameplay_generator(self):
        """
        Generate user interface gameplay buttons.
        """
        return self.buttons_dict['ui_gameplay_buttons']

    def scale(self, *, background_surface, ui_type_flag: str):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface
        :param ui_type_flag: String with type of scale need.
        :type ui_type_flag: str
        """
        if ui_type_flag == 'gameplay_ui':
            if self.active_game_interface_flag == 'on':
                for key in self.buttons_dict['ui_gameplay_buttons']:
                    button = self.buttons_dict['ui_gameplay_buttons'][key]
                    button.scale(background_surface=background_surface)

    def button_clicked_status(self) -> tuple[str | None, bool]:
        """
        Check left click of mouse to button status.

        :return: tuple[str | None, True | False]
        """
        if self.active_game_interface_flag == 'on':
            gameplay_ui_dict = self.ui_gameplay_generator()
            for button in gameplay_ui_dict:
                click_status = gameplay_ui_dict[button].button_clicked_status()
                if click_status is True:
                    return button, True
            return None, False
        ...

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.

        :return: True | False
        """
        gameplay_ui_dict = self.ui_gameplay_generator()
        for button in gameplay_ui_dict:
            cursor_position_status = gameplay_ui_dict[button].button_cursor_position_status()
            if cursor_position_status is True:
                return True
            else:
                return False
