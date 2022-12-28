from pygame import Surface

from ..User_Interface.UI_Button import button_generator
"""
Contents code for user interface controller.
"""


class InterfaceController:
    """
    Generate user interface: buttons, menu and control it.
    InterfaceController used in "GamePlay_Administrator.py" for gameplay programming.
    Created in GameMaster class in Game_Master.py.
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
        # In game user interface:
        # "True/False" and "False" as default.
        self.gameplay_interface_hidden_status: bool = False
        self.gameplay_interface_status: bool = False
        # Menu interface:
        # "True/False" and "False" as default.
        self.game_menu_status: bool = False
        self.settings_menu_status: bool = False
        self.exit_menu_status: bool = False
        self.load_menu_status: bool = False
        self.save_menu_status: bool = False
        self.settings_status_menu_status: bool = False
        # Start Menu:
        # "True/False" and "True" as default.
        self.start_menu_status: bool = True
        # Exit menu "from called" flag:
        # "True/False" and "start_menu_flag - True" as default.
        self.exit_from_start_menu_flag: bool = True
        self.exit_from_game_menu_flag: bool = False
        # Setting menu "from called" flag:
        # "True/False" and "start_menu_flag - True" as default.
        self.settings_from_start_menu_flag: bool = True
        self.settings_from_game_menu_flag: bool = False
        # Load menu "from called" flag:
        # "True/False" and "start_menu_flag - True" as default.
        self.load_from_start_menu_flag: bool = True
        self.load_from_game_menu_flag: bool = False

    def get_ui_buttons_dict(self) -> dict[str]:
        """
        Generate user interface buttons.

        :return: Dict with buttons names strings as values.
        """
        if self.gameplay_interface_status is True:
            return self.buttons_dict['ui_gameplay_buttons']
        if self.game_menu_status is True:
            return self.buttons_dict['ui_game_menu_buttons']
        if self.settings_menu_status is True:
            return self.buttons_dict['ui_setting_menu_buttons']
        if self.exit_menu_status is True:
            return self.buttons_dict['ui_exit_menu_buttons']
        if self.load_menu_status is True:
            return self.buttons_dict['ui_load_menu_buttons']
        if self.save_menu_status is True:
            return self.buttons_dict['ui_save_menu_buttons']
        if self.settings_status_menu_status is True:
            return self.buttons_dict['ui_settings_status_buttons']
        if self.start_menu_status is True:
            return self.buttons_dict['ui_start_menu_buttons']

    def scale(self, *, background_surface):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface
        """
        ui_buttons_dict = self.get_ui_buttons_dict()
        for key in ui_buttons_dict:
            button = ui_buttons_dict[key]
            button.scale(background_surface=background_surface)

    def button_clicked_status(self) -> tuple[str | None, bool]:
        """
        Check left click of mouse to button status.

        :return: tuple[str | None, True | False]
        """
        if self.gameplay_interface_hidden_status is False:
            gameplay_ui_dict = self.get_ui_buttons_dict()
            for button in gameplay_ui_dict:
                click_status = gameplay_ui_dict[button].button_clicked_status()
                if click_status is True:
                    return button, True
        return None, False

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.

        :return: True | False
        """
        gameplay_ui_dict: dict = self.get_ui_buttons_dict()
        for button in gameplay_ui_dict:
            cursor_position_status = gameplay_ui_dict[button].button_cursor_position_status()
            if cursor_position_status is True:
                return True
            else:
                return False
