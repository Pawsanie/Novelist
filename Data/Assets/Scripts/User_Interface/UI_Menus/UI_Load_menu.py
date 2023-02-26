from ..UI_Base_menu import BaseMenu
"""
Contains Load menu code.
"""


class LoadMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Load Menu.
    """
    def __init__(self):
        super(LoadMenu, self).__init__()

    def load_menu_input_mouse(self, event):
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
                self.interface_controller.load_menu_status = False
                if self.interface_controller.load_from_start_menu_flag is True:
                    self.interface_controller.start_menu_status = True
                if self.interface_controller.load_from_game_menu_flag is True:
                    self.interface_controller.game_menu_status = True

    def load_menu_input(self, event):
        """
        Load menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.load_menu_input_mouse(event)
        self.input_wait_ready()
