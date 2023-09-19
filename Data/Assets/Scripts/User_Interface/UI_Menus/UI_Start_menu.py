from ..UI_Base_menu import BaseMenu
from ...Application_layer.Save_Keeper import SaveKeeper
from ...Universal_computing.Pattern_Singleton import SingletonPattern
"""
Contains Start menu code.
"""


class StartMenu(BaseMenu, SingletonPattern):
    """
    Controls reactions to user input commands from mouse or key bord in Start Menu.
    """
    def __init__(self):
        super(StartMenu, self).__init__()
        self.save_keeper: SaveKeeper = SaveKeeper()
        self.status: bool = True

    def start_game(self, scene_name: str):
        """
        Switch flags for correct game start.
        Start game from correct scene.
        :param scene_name: The name of the scene to start the game from.
        """
        self.scene_validator.scene_flag = scene_name
        self.status: bool = False

        self.interface_controller.gameplay_interface_hidden_status = False
        self.interface_controller.gameplay_interface_status = True
        self.interface_controller.start_menu_flag = False

        self.save_keeper.generate_save_slots_buttons()

        self.state_machine.next_state()

    def input_mouse(self, event):
        """
        Interface interaction in in-game start menu.
        :param event: pygame.event from main_loop.
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status(event)
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]

            if command == 'start_menu_new_game':
                self.start_game(
                    self.scene_validator.default_scene_name
                )

            if command == 'start_menu_continue':
                continue_game_scene: str | False = self.save_keeper.continue_game()
                if continue_game_scene is not False:
                    self.start_game(continue_game_scene)
                    self.save_keeper.reread = True

            if command == 'start_menu_load':
                from .UI_Load_menu import LoadMenu
                self.status: bool = False
                LoadMenu().status = True
                self.save_keeper.generate_save_slots_buttons()
                LoadMenu().vanish_menu_data()

            if command == 'start_menu_settings':
                from .UI_Settings_menu import SettingsMenu
                self.status: bool = False
                SettingsMenu().status = True

            if command == 'start_menu_creators':
                from .UI_Creators_menu import CreatorsMenu
                self.status: bool = False
                CreatorsMenu().status = True

            if command == 'start_menu_exit':
                from .UI_Exit_menu import ExitMenu
                self.status: bool = False
                ExitMenu().status = True
