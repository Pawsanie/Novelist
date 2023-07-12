from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
from ...Application_layer.Save_Keeper import SaveKeeper
"""
Contains Load menu code.
"""


class LoadMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Load Menu.
    """
    def __init__(self):
        super(LoadMenu, self).__init__()
        self.save_keeper: SaveKeeper = SaveKeeper()

    def input_mouse(self, event):
        """
        Interface interaction in in-game load menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command: str = gameplay_ui_buttons[0]
            if command == 'load_menu_load':
                ...
            if command == 'load_menu_back':
                self.status: bool = False
                if self.interface_controller.start_menu_flag is True:
                    from .UI_Start_menu import StartMenu
                    StartMenu().status = True
                if self.interface_controller.start_menu_flag is False:
                    from .UI_Game_menu import GameMenu
                    GameMenu().status = True

