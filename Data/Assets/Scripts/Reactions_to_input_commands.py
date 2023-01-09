from pygame import time, QUIT, quit, VIDEORESIZE
from pygame import event as pygame_events

from .User_Interface.Interface_Controller import InterfaceController
from .Settings_Keeper import SettingsKeeper
from .Stage_Director import StageDirector
from .Scene_Validator import SceneValidator
from .User_Interface.UI_Exit_menu import ExitMenu
from .User_Interface.UI_Game_menu import GameMenu
from .User_Interface.UI_Load_menu import LoadMenu
from .User_Interface.UI_Save_menu import SaveMenu
from .User_Interface.UI_Settings_menu import SettingsMenu
from .User_Interface.UI_Settings_Status_menu import SettingsStatusMenu
from .User_Interface.UI_Start_menu import StartMenu
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
                    self.scene = 'redraw'
                # User commands:
                self.reactions_to_input_commands.reactions_to_input_commands(event)
            main_cycle_fps_clock.tick(main_cycle_fps)
    return coroutine


class InputCommandsReactions:
    """
    Controls reactions to user input commands from mouse or key bord by conveyor
    in 'reactions_to_input_commands' method from 'main_loop'.
    """
    def __init__(self, *, interface_controller, settings_keeper, stage_director, scene_validator):
        """
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        :param settings_keeper: Settings controller class.
        :type settings_keeper: SettingsKeeper
        :param stage_director: Stage Director class exemplar.
                               Responsible for stage production.
        :type stage_director: StageDirector
        """
        # Arguments processing:
        self.interface_controller: InterfaceController = interface_controller
        self.settings_keeper: SettingsKeeper = settings_keeper
        self.stage_director: StageDirector = stage_director
        self.scene_validator: SceneValidator = scene_validator

        # Settings for UI menus:
        self.exit_menu: ExitMenu = ExitMenu(
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )
        self.game_menu: GameMenu = GameMenu(
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )
        self.load_menu: LoadMenu = LoadMenu(
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )
        self.save_menu: SaveMenu = SaveMenu(
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )
        self.settings_menu: SettingsMenu = SettingsMenu(
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator,
            settings_keeper=self.settings_keeper
        )
        self.settings_status_menu: SettingsStatusMenu = SettingsStatusMenu(
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )
        self.start_menu: StartMenu = StartMenu(
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )
        # Settings for gameplay:
        self.gameplay_administrator: GamePlayAdministrator = GamePlayAdministrator(
            stage_director=self.stage_director,
            interface_controller=self.interface_controller,
            scene_validator=self.scene_validator
        )

    def __call__(self):
        """
        Need for calling by Game_Master class in main_loop.
        """
        # Get settings for 'reactions_to_input_commands' 'Gameplay':
        # Associated with the main loop.
        self.gameplay_administrator.set_gameplay_type()
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
