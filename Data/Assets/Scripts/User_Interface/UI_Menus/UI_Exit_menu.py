from pygame import quit, KEYDOWN, K_ESCAPE, K_TAB, K_e

from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains exit menu code.
"""


class ExitMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Exit Menu.
    """
    def __init__(self):
        super(ExitMenu, self).__init__()

    def exit_menu_back(self):
        """
        Back from exit menu.
        """
        self.status: bool = False

        if self.interface_controller.start_menu_flag is True:
            from .UI_Start_menu import StartMenu
            StartMenu().status = True

        if self.interface_controller.start_menu_flag is False:
            from .UI_Game_menu import GameMenu
            GameMenu().status = True

    def input_mouse(self, event):
        """
        Interface interaction in in-game exit menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]

            if command == 'exit_menu_yes':
                quit()
                exit(0)

            if command == 'exit_menu_no':
                self.exit_menu_back()

    def key_bord_key_down(self, event):
        """
        Interface interaction in in-game exit menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_TAB:
                self.exit_menu_back()
            if event.key == K_e:
                quit()
                exit(0)
