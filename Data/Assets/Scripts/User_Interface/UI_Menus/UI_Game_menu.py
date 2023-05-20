from pygame import KEYDOWN, K_ESCAPE

from ..UI_Base_menu import BaseMenu
from ...Universal_computing import SingletonPattern
"""
Contains game menu code.
"""


class GameMenu(SingletonPattern, BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Game Menu.
    """
    def __init__(self):
        super(GameMenu, self).__init__()

    def input_mouse(self, event):
        """
        Interface interaction in in-game menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'game_menu_continue':
                self.interface_controller.game_menu_status = False
                self.interface_controller.gameplay_interface_status = True
            if command == 'game_menu_save':
                self.interface_controller.game_menu_status = False
                self.interface_controller.save_menu_status = True
            if command == 'game_menu_load':
                self.interface_controller.game_menu_status = False
                self.interface_controller.load_menu_status = True
            if command == 'game_menu_settings':
                self.interface_controller.game_menu_status = False
                self.interface_controller.settings_menu_status = True
            if command == 'game_menu_start_menu':
                self.interface_controller.game_menu_status = False
                self.interface_controller.back_to_start_menu_status = True
            if command == 'game_menu_exit':
                self.interface_controller.game_menu_status = False
                self.interface_controller.exit_menu_status = True

    def key_bord_key_down(self, event):
        """
        Interface interaction in in-game menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.interface_controller.game_menu_status = False
                self.interface_controller.gameplay_interface_status = True

    def menu_input(self, event):
        """
        Game menu input conveyor:
        :param event: pygame.event from main_loop.
        """
        # Exit menu "from called" status flag:
        self.interface_controller.exit_from_start_menu_flag = False
        self.interface_controller.exit_from_game_menu_flag = True
        # Load menu "from called" status flag:
        self.interface_controller.load_from_start_menu_flag = False
        self.interface_controller.load_from_game_menu_flag = True
        # Setting menu "from called" status flag:
        self.interface_controller.settings_from_start_menu_flag = False
        self.interface_controller.settings_from_game_menu_flag = True
        # Button game menu ui status:
        self.input_mouse(event)
        # Button game menu key bord status:
        self.key_bord_key_down(event)
        self.input_wait_ready()
