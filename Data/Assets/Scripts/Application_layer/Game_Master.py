from pygame import Surface

from .Reactions_to_input_commands import main_loop, InputCommandsReactions
from .Stage_Director import StageDirector
from ..Render.Render import Render
from .Scene_Validator import SceneValidator
from ..User_Interface.Interface_Controller import InterfaceController
from .Settings_Keeper import SettingsKeeper
from .Save_Keeper import SaveKeeper
from ..Logging_Config import error_logger
"""
Contains code for GameMaster.
Control gameplay, menus and display image render.
"""


class GameMaster:
    """
    Set all settings for Stage Director and game.
    Entry point for gameplay.
    """
    def __init__(self):
        # Collect base game settings:  # TODO: remove?
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.display_screen: Surface = self.settings_keeper.get_windows_settings()
        self.language_flag: str = self.settings_keeper.text_language

        # Stage Director settings:
        self.stage_director: StageDirector = StageDirector()
        # Scene Validator settings:
        self.scene_validator: SceneValidator = SceneValidator()
        # Interface Controller settings:
        self.interface_controller: InterfaceController = InterfaceController()
        # Render settings:
        self.render: Render = Render()
        # User input commands processing:
        self.reactions_to_input_commands: InputCommandsReactions = InputCommandsReactions()

        # Save and load system:  # TODO: remove?
        self.save_keeper: SaveKeeper = SaveKeeper()

    def set_gameplay_type(self):  # TODO: DEVNULL
        """
        Set gameplay type.
        """
        if self.scene_validator.scene_gameplay_type == 'reading':
            self.interface_controller.gameplay_type_choice = False
            self.interface_controller.gameplay_type_reading = True
            return
        if self.scene_validator.scene_gameplay_type == 'choice':
            self.interface_controller.gameplay_type_reading = False
            self.interface_controller.gameplay_type_choice = True
            # Push dialogue buttons to 'InterfaceController':
            self.interface_controller.gameplay_choice_buttons = \
                self.reactions_to_input_commands.gameplay_administrator\
                .gameplay_dialogues_choice\
                .dialogues_buttons[self.scene_validator.scene]
            return

    @error_logger
    @main_loop
    def __call__(self):
        """
        Main game loop call.
        """
        # User input commands processing:
        self.reactions_to_input_commands()
        # Build scene:
        self.scene_validator()
        self.stage_director.scale()
        # Chose gameplay settings:
        self.set_gameplay_type()
        # Build interface:
        self.interface_controller.scale()
        # Image render:
        self.render.image_render()