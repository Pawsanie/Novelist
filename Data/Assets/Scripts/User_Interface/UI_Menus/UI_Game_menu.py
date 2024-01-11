from pygame import KEYDOWN, K_ESCAPE

from ..UI_Base_menu import BaseMenu
from ...Universal_computing.Pattern_Singleton import SingletonPattern
from ...Application_layer.Save_Keeper import SaveKeeper
"""
Contains game menu code.
"""


class GameMenu(SingletonPattern, BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Game Menu.
    """
    def __init__(self):
        super(GameMenu, self).__init__()
        self.save_keeper: SaveKeeper = SaveKeeper()

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
                self.status: bool = False
                self.interface_controller.gameplay_interface_status = True
                self.state_machine.next_state()

            elif command == 'game_menu_save':
                self.status: bool = False
                from .UI_Save_menu import SaveMenu
                SaveMenu().status = True
                self.save_keeper.generate_save_slots_buttons()
                SaveMenu().vanish_menu_data()

            elif command == 'game_menu_load':
                self.status: bool = False
                from .UI_Load_menu import LoadMenu
                LoadMenu().status = True
                self.save_keeper.generate_save_slots_buttons()
                LoadMenu().vanish_menu_data()

            elif command == 'game_menu_settings':
                self.status: bool = False
                from .UI_Settings_menu import SettingsMenu
                SettingsMenu().status = True

            elif command == 'game_menu_start_menu':
                self.status: bool = False
                from .UI_Back_to_Start_menu_Status_menu import BackToStartMenuStatusMenu
                BackToStartMenuStatusMenu().status = True

            elif command == 'game_menu_exit':
                self.status: bool = False
                from .UI_Exit_menu import ExitMenu
                ExitMenu().status = True

    def key_bord_key_down(self, event):
        """
        Interface interaction in in-game menu.
        :param event: pygame.event from main_loop.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.status: bool = False
                self.interface_controller.gameplay_interface_status = True
