from pygame import KEYDOWN, K_ESCAPE, K_TAB, K_e

from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
"""
Back to start menu status menu code.
"""


class BackToStartMenuStatusMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in "Back to 'Start menu' status menu".
    """
    def __init__(self):
        super(BackToStartMenuStatusMenu, self).__init__()

    def back_to_start_menu_status_menu_yes(self):
        """
        Switch to start menu.
        """
        self.status: bool = False
        from .UI_Start_menu import StartMenu
        self._interface_controller.start_menu_flag = True
        StartMenu().status = True

    def back_to_start_menu_status_menu_no(self):
        """
        Back from back to start menu status menu.
        """
        self.status: bool = False
        from .UI_Game_menu import GameMenu
        GameMenu().status = True

    def _input_mouse(self, event):
        """
        Interface interaction in in-game back to start menu status menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self._interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]

            if command == 'back_to_start_menu_yes':
                self.back_to_start_menu_status_menu_yes()

            if command == 'back_to_start_menu_no':
                self.back_to_start_menu_status_menu_no()

    def _key_bord_key_down(self, event):
        """
        Interface interaction in in-game back to start menu status menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_TAB:
                self.back_to_start_menu_status_menu_no()
            if event.key == K_e:
                self.back_to_start_menu_status_menu_yes()
