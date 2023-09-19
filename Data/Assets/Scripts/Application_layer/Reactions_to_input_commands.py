from pygame import time, QUIT, quit
from pygame import event as pygame_events

from ..User_Interface.Interface_Controller import InterfaceController
from .Settings_Keeper import SettingsKeeper
from .Stage_Director import StageDirector
from .Scene_Validator import SceneValidator
from ..User_Interface.UI_Menus.UI_Exit_menu import ExitMenu
from ..User_Interface.UI_Menus.UI_Game_menu import GameMenu
from ..User_Interface.UI_Menus.UI_Load_menu import LoadMenu
from ..User_Interface.UI_Menus.UI_Save_menu import SaveMenu
from ..User_Interface.UI_Menus.UI_Settings_menu import SettingsMenu
from ..User_Interface.UI_Menus.UI_Settings_Status_menu import SettingsStatusMenu
from ..User_Interface.UI_Menus.UI_Start_menu import StartMenu
from ..User_Interface.UI_Menus.UI_Back_to_Start_menu_Status_menu import BackToStartMenuStatusMenu
from ..User_Interface.UI_Menus.UI_Creators_menu import CreatorsMenu
from ..GamePlay.GamePlay_Administrator import GamePlayAdministrator
"""
Contains code for reactions to input commands.
"""


def main_loop(func):
    """
    Decorator with the main loop of game.
    """
    def coroutine(*args, **kwargs):
        # class method`s 'self.' for in class decorator:
        self = args[0]

        program_running: bool = True
        main_cycle_fps_clock = time.Clock()
        main_cycle_fps: int = SettingsKeeper().frames_per_second

        while program_running:
            # Set scene:
            func(*args, **kwargs)
            for event in pygame_events.get():
                # Quit by exit_icon:
                if event.type == QUIT:
                    quit()
                    exit(0)
                # User commands:
                self.reactions_to_input_commands.reactions_to_input_commands(event)

            pygame_events.clear()
            main_cycle_fps_clock.tick(main_cycle_fps)

    return coroutine


class InputCommandsReactions:
    """
    Controls reactions to user input commands from mouse or key bord by conveyor
    in 'reactions_to_input_commands' method from 'main_loop'.
    """
    menus_collection: dict = {
        'exit_menu': {
            'object': ExitMenu(),
            'menu_file': 'ui_exit_menu_buttons',
            'text_file': 'ui_exit_menu_text'
        },
        'settings_menu': {
            'object': SettingsMenu(),
            'menu_file': 'ui_settings_menu_buttons',
            'text_file': None
        },
        'load_menu': {
            'object': LoadMenu(),
            'menu_file': 'ui_load_menu_buttons',
            'text_file': None
        },
        None: {
            'object': GameMenu(),
            'menu_file': 'ui_game_menu_buttons',
            'text_file': None
        },
        'save_menu': {
            'object': SaveMenu(),
            'menu_file': 'ui_save_menu_buttons',
            'text_file': None
        },
        'settings_status_menu': {
            'object': SettingsStatusMenu(),
            'menu_file': 'ui_settings_status_buttons',
            'text_file': 'ui_settings_status_text'
        },
        'start_menu': {
            'object': StartMenu(),
            'menu_file': 'ui_start_menu_buttons',
            'text_file': None
        },
        'back_to_start_menu_status_menu': {
            'object': BackToStartMenuStatusMenu(),
            'menu_file': 'ui_back_to_start_menu_status_menu_buttons',
            'text_file': 'ui_back_to_start_menu_status_menu_text'
        },
        'creators_menu': {
            'object': CreatorsMenu(),
            'menu_file': 'ui_creators_menu_buttons',
            'text_file': 'ui_creators_menu_text'
        }
    }

    def __init__(self):
        # Arguments processing:
        self.interface_controller: InterfaceController = InterfaceController()
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.stage_director: StageDirector = StageDirector()
        self.scene_validator: SceneValidator = SceneValidator()

        # Settings for gameplay:
        self.gameplay_administrator: GamePlayAdministrator = GamePlayAdministrator()
        # Itself data proxy:
        self.interface_controller.menus_collection = self.menus_collection

    def __call__(self):
        """
        Need for calling by Game_Master class in main_loop.
        """
        pass

    def reactions_to_input_commands(self, event):
        """
        User commands conveyor:
        :param event: 'pygame.event' from main_loop.
        """
        # Gameplay:
        if self.interface_controller.gameplay_interface_status is True:
            self.gameplay_administrator.gameplay_input(event)
            return
        # Game menus:
        for key in self.menus_collection:
            menu = self.menus_collection[key]['object']
            if menu.status is True:
                menu.menu_input(event)
                return
