from ..UI_Base_menu import BaseMenu
"""
Contains Save menu code.
"""


class SaveMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Save Menu.
    """
    def __init__(self):
        super(SaveMenu, self).__init__()

    def save_menu_input_mouse(self, event):
        """
        Interface interaction in in-game save menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'save_menu_save':
                ...
            if command == 'save_menu_back':
                self.interface_controller.save_menu_status = False
                self.interface_controller.game_menu_status = True

    def save_menu_input(self, event):
        """
        Save menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.save_menu_input_mouse(event)
        self.input_wait_ready()
