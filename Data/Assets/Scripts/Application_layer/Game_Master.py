from asyncio import run, sleep, gather

from pygame import time
from pygame.time import Clock

from .Reactions_to_input_commands import InputCommandsReactions
from .Stage_Director import StageDirector
from ..Render.Render import Render
from ..User_Interface.Interface_Controller import InterfaceController
from ..Logging_Config import error_logger
from .Sound_Director import SoundDirector
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .State_Machine import StateMachine
from .Initialization import initialization
from ..GamePlay.GamePlay_Administrator import GamePlayAdministrator
from .Settings_Keeper import SettingsKeeper
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

    async def _render_loop(self):
        """
        MVC Model and View.
        """
        main_cycle_fps_clock: Clock = time.Clock()
        main_cycle_fps: int = SettingsKeeper().frames_per_second

        while True:
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

            main_cycle_fps_clock.tick(main_cycle_fps)
            await sleep(0)

    async def _mvc_pattern(self):
        """
        MVC pattern main game loop.
        """
        await gather(
                *[
                    self._render_loop(),
                    self.reactions_to_input_commands.input_commands_loop()
                ]
            )

    @error_logger
    def __call__(self):
        """
        Main game loop call.
        """
        run(
            self._mvc_pattern()
        )
