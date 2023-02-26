from ..UI_Base_menu import BaseMenu
"""
Contains creators menu code.
"""


class CreatorsMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Creators Menu.
    """
    def __init__(self):
        super(CreatorsMenu, self).__init__()

    def creators_menu_back(self):
        self.interface_controller.creator_menu = False
        self.interface_controller.start_menu_status = True

    def creators_menu_input_mouse(self, event):
        """
        Interface interaction in in-game setting menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            if gameplay_ui_buttons[0] == 'creators_menu_back':
                self.creators_menu_back()

    def creators_menu_input(self, event):
        """
        Save menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.creators_menu_input_mouse(event)
        self.input_wait_ready()
