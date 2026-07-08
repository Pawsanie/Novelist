from pygame.event import Event

from ...Core.Settings_Keeper import SettingsKeeper
from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
# Lazy import:
# from .UI_Start_menu import StartMenu
# from .UI_Game_menu import GameMenu
"""
Contains settings menu code.
"""


class SettingsMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Settings Menu.
    """
    def __init__(self):
        super(SettingsMenu, self).__init__()
        self.settings_keeper: SettingsKeeper = SettingsKeeper()

    def _input_mouse(self, event: Event):
        """
        Interface interaction in in-game setting menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self._interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]

            if command == 'settings_menu_video':
                ...

            elif command == 'settings_menu_audio':
                ...

            elif command == 'settings_menu_localization':
                ...

            elif command == 'settings_menu_back':
                self.status: bool = False
                if self._interface_controller.start_menu_flag is True:
                    from .UI_Start_menu import StartMenu
                    StartMenu().status = True
                if self._interface_controller.start_menu_flag is False:
                    from .UI_Game_menu import GameMenu
                    GameMenu().status = True
