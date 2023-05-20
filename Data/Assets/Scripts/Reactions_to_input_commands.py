from pygame import time, QUIT, quit, VIDEORESIZE
from pygame import event as pygame_events

from .User_Interface.Interface_Controller import InterfaceController
from .Settings_Keeper import SettingsKeeper
from .Stage_Director import StageDirector
from .Scene_Validator import SceneValidator
from .User_Interface.UI_Menus.UI_Exit_menu import ExitMenu
from .User_Interface.UI_Menus.UI_Game_menu import GameMenu
from .User_Interface.UI_Menus.UI_Load_menu import LoadMenu
from .User_Interface.UI_Menus.UI_Save_menu import SaveMenu
from .User_Interface.UI_Menus.UI_Settings_menu import SettingsMenu
from .User_Interface.UI_Menus.UI_Settings_Status_menu import SettingsStatusMenu
from .User_Interface.UI_Menus.UI_Start_menu import StartMenu
from .User_Interface.UI_Menus.UI_Back_to_Start_menu_Status_menu import BackToStartMenuStatusMenu
from .User_Interface.UI_Menus.UI_Creators_menu import CreatorsMenu
from .GamePlay.GamePlay_Administrator import GamePlayAdministrator
"""
Contains code for reactions to input commands.
"""


def main_loop(func):
    """
    Decorator with the main loop of game.
    """
    def coroutine(*args, **kwargs):
        self = args[0]  # class method`s 'self.' for in class decorator.
        program_running: bool = True
        main_cycle_fps_clock = time.Clock()
        main_cycle_fps: int = 30
        while program_running:
            for event in pygame_events.get():
                # Quit by exit_icon.
                if event.type == QUIT:
                    quit()
                    program_running: bool = False
                    exit(0)
                # Set scene:
                if self.scene_validator.scene_flag != self.scene_validator.scene:
                    func(*args, **kwargs)
                # Window resize:
                if event.type == VIDEORESIZE:
                    self.scene_validator.scene = 'redraw'
                # User commands:
                self.reactions_to_input_commands.reactions_to_input_commands(event)
            # Set scene without events:
            if self.scene_validator.scene_flag != self.scene_validator.scene:
                func(*args, **kwargs)
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
            'tag': 'ui_setting_menu_buttons',
            'text': 'ui_exit_menu_text'
        },
        'settings_menu': {
            'object': SettingsMenu(),
            'tag': 'ui_exit_menu_buttons',
            'text': None
        },
        'load_menu': {
            'object': LoadMenu(),
            'tag': 'ui_load_menu_buttons',
            'text': None
        },
        None: {
            'object': GameMenu(),
            'tag': 'ui_game_menu_buttons',
            'text': None
        },
        'save_menu': {
            'object': SaveMenu(),
            'tag': 'ui_save_menu_buttons',
            'text': None
        },
        'settings_status_menu': {
            'object': SettingsStatusMenu(),
            'tag': 'ui_settings_status_buttons',
            'text': 'ui_settings_status_text'
        },
        'start_menu': {
            'object': StartMenu(),
            'tag': 'ui_start_menu_buttons',
            'text': None
        },
        'back_to_start_menu_status_menu': {
            'object': BackToStartMenuStatusMenu(),
            'tag': 'ui_back_to_start_menu_status_menu_buttons',
            'text': 'ui_back_to_start_menu_status_menu_text'
        },
        'creators_menu': {
            'object': CreatorsMenu(),
            'tag': 'ui_creators_menu_buttons',
            'text': 'ui_creators_menu_text'
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

        self.current_menu = StartMenu()
        self.interface_controller.menus_collection = self.menus_collection  # TODO: crutch?

    def __call__(self):
        """
        Need for calling by Game_Master class in main_loop.
        """
        pass

    def reactions_to_input_commands(self, event):
        """
        User commands conveyor:
        :param event: pygame.event from main_loop.
        """
        # Gameplay:
        if self.interface_controller.gameplay_interface_status is True:
            self.gameplay_administrator.gameplay_input(event)
            return
        # Game menus:
        if self.current_menu.status is True:
            self.current_menu.menu_input(event)
            return
