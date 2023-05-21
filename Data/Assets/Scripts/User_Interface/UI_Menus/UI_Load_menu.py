from ..UI_Base_menu import BaseMenu
from ...Universal_computing import SingletonPattern
"""
Contains Load menu code.
"""


class LoadMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Load Menu.
    """
    def __init__(self):
        super(LoadMenu, self).__init__()

    def input_mouse(self, event):
        """
        Interface interaction in in-game load menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'load_menu_load':
                ...
            if command == 'load_menu_back':
                self.status: bool = False
                if self.interface_controller.start_menu_flag is True:
                    from .UI_Start_menu import StartMenu
                    StartMenu().status = True
                if self.interface_controller.start_menu_flag is False:
                    from UI_Game_menu import GameMenu
                    GameMenu().status = True

