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
from .Logging_Config import logger
"""
Contains code for reactions to input commands.
"""


@logger
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
    def __init__(self):
        # Arguments processing:
        self.interface_controller: InterfaceController = InterfaceController()
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.stage_director: StageDirector = StageDirector()
        self.scene_validator: SceneValidator = SceneValidator()

        # Settings for UI menus:
        self.exit_menu: ExitMenu = ExitMenu()
        self.game_menu: GameMenu = GameMenu()
        self.load_menu: LoadMenu = LoadMenu()
        self.save_menu: SaveMenu = SaveMenu()
        self.settings_menu: SettingsMenu = SettingsMenu()
        self.settings_status_menu: SettingsStatusMenu = SettingsStatusMenu()
        self.start_menu: StartMenu = StartMenu()
        self.back_to_start_menu_status_menu: BackToStartMenuStatusMenu = BackToStartMenuStatusMenu()
        self.creators_menu: CreatorsMenu = CreatorsMenu()
        # Settings for gameplay:
        self.gameplay_administrator: GamePlayAdministrator = GamePlayAdministrator()

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
        # Game menu:
        if self.interface_controller.game_menu_status is True:
            self.game_menu.game_menu_input(event)
            return
        # Exit menu:
        if self.interface_controller.exit_menu_status is True:
            self.exit_menu.exit_menu_input(event)
            return
        # Setting menu:
        if self.interface_controller.settings_menu_status is True:
            self.settings_menu.setting_menu_input(event)
            return
        # Load menu:
        if self.interface_controller.load_menu_status is True:
            self.load_menu.load_menu_input(event)
            return
        # Save menu:
        if self.interface_controller.save_menu_status is True:
            self.save_menu.save_menu_input(event)
            return
        # Settings status menu:
        if self.interface_controller.settings_status_menu_status is True:
            self.settings_status_menu.settings_status_menu_input(event)
            return
        # Start menu:
        if self.interface_controller.start_menu_status is True:
            self.start_menu.start_menu_input(event)
            return
        # Back to "Start menu" status menu:
        if self.interface_controller.back_to_start_menu_status is True:
            self.back_to_start_menu_status_menu.back_to_start_menu_status_menu_input(event)
            return
        # Creators menu:
        if self.interface_controller.creators_menu_status is True:
            self.creators_menu.creators_menu_input(event)
            return
