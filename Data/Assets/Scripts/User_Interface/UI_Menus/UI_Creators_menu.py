from pygame import K_e, K_TAB, KEYDOWN, K_ESCAPE

from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains creators menu code.
"""


class CreatorsMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Creators Menu.
    """
    def __init__(self):
        super(CreatorsMenu, self).__init__()

    def creators_menu_back(self):
        """
        Back to start menu.
        """
        from .UI_Start_menu import StartMenu
        self.status: bool = False
        StartMenu().status = True

    def _key_bord_key_down(self, event):
        """
        Interface interaction in creators menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_TAB or event.key == K_e:
                self.creators_menu_back()

    def _input_mouse(self, event):
        """
        Interface interaction in creators menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self._interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            if gameplay_ui_buttons[0] == 'creators_menu_back':
                self.creators_menu_back()
