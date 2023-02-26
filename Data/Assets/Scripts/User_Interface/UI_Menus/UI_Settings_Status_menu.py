from ..UI_Base_menu import BaseMenu
"""
Contains Settings Status menu code.
"""


class SettingsStatusMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Settings Status Menu.
    """
    def __init__(self):
        super(SettingsStatusMenu, self).__init__()

    def setting_menu_input_mouse(self, event):
        """
        Interface interaction in in-game settings menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'save_menu_save':
                ...

    def settings_status_menu_input(self, event):
        """
        Settings status menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.setting_menu_input_mouse(event)
        self.input_wait_ready()
