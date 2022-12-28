from pygame import Surface

from .Reactrions_to_input_commands import main_loop, InputCommandsReactions
from .Stage_Director import StageDirector
from .Render import Render
from .Scene_Validator import SceneValidator
from .User_Interface.Interface_Controller import InterfaceController
from .Settings_Keeper import SettingsKeeper
"""
Contains code for GameMaster.
Control gameplay, menus and display image render.
"""


class GameMaster:
    """
    Set all settings for Stage Director and game.
    Entry point for gameplay.
    """
    def __init__(self, *, display_screen, start_settings):
        """
        :param display_screen: pygame.display.Surface
        :param start_settings: SettingsKeeper
        """
        # Collect base game settings:
        self.settings_keeper: SettingsKeeper = start_settings
        self.display_screen: Surface = display_screen
        self.language_flag: str = self.settings_keeper.text_language

        # Stage Director settings:
        self.stage_director: StageDirector = StageDirector(
            display_screen=self.display_screen,
            language_flag=self.language_flag
        )
        self.scene_validator: SceneValidator = SceneValidator(
            stage_director=self.stage_director
        )
        # Interface Controller settings:
        self.interface_controller: InterfaceController = InterfaceController(
            background_surface=self.stage_director.background_surface,
            language_flag=self.language_flag
        )
        # Render settings:
        self.render: Render = Render(
            screen=self.display_screen,
            interface_controller=self.interface_controller,
            stage_director=self.stage_director
        )
        # User input commands processing:
        self.reactions_to_input_commands: InputCommandsReactions = InputCommandsReactions(
            interface_controller=self.interface_controller,
            settings_keeper=self.settings_keeper,
            stage_director=self.stage_director,
            scene_validator=self.scene_validator
        )

    @main_loop
    def __call__(self):
        """
        Main game loop call.
        """
        self.reactions_to_input_commands()
        self.scene_validator()
        self.stage_director.scale(self.interface_controller)
        self.render.image_render()
