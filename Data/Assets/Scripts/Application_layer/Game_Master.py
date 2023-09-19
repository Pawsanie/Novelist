from .Reactions_to_input_commands import main_loop, InputCommandsReactions
from .Stage_Director import StageDirector
from ..Render.Render import Render
from ..User_Interface.Interface_Controller import InterfaceController
from ..Logging_Config import error_logger
from .Sound_Director import SoundDirector
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .State_Machine import StateMachine
from .Initialization import initialization
from ..GamePlay.GamePlay_Administrator import GamePlayAdministrator
"""
Contains code for GameMaster.
Control gameplay, menus and display image render.
"""


class GameMaster(SingletonPattern):
    """
    Set all settings for Stage Director and game.
    Entry point for gameplay.
    """
    def __init__(self):
        initialization()
        # Stage Director settings:
        self.stage_director: StageDirector = StageDirector()
        # Sound Director settings:
        self.sound_director: SoundDirector = SoundDirector()
        # Interface Controller settings:
        self.interface_controller: InterfaceController = InterfaceController()
        # User input commands processing:
        self.reactions_to_input_commands: InputCommandsReactions = InputCommandsReactions()
        # Render settings:
        self.render: Render = Render()
        # StateMachine:
        self.state_machine: StateMachine = StateMachine()
        # Settings for gameplay:
        self.gameplay_administrator: GamePlayAdministrator = GamePlayAdministrator()

    @error_logger
    @main_loop
    def __call__(self):
        """
        Main game loop call.
        """
        # Build scene:
        self.state_machine()
        self.stage_director.scale()
        # Sound control:
        self.sound_director.play()
        # Build interface:
        self.gameplay_administrator.set_gameplay_type()
        self.interface_controller.scale()
        # Image render:
        self.render.image_render()
