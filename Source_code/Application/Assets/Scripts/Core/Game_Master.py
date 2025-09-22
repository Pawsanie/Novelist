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

        # Program layers settings:
        self._stage_director: StageDirector = StageDirector()
        self._sound_director: SoundDirector = SoundDirector()

        self._interface_controller: InterfaceController = InterfaceController()
        self._render: Render = Render()

        self._state_machine: StateMachine = StateMachine()
        self._reactions_to_input_commands: InputCommandsReactions = InputCommandsReactions()
        self._gameplay_administrator: GamePlayAdministrator = GamePlayAdministrator()

    async def _render_loop(self):
        """
        MVC pattern Model and View parts.
        """
        main_cycle_fps_clock: Clock = time.Clock()
        main_cycle_fps: int = SettingsKeeper().get_frames_per_second()

        while True:
            # Build scene:
            self._state_machine()
            self._stage_director.scale()
            # Sound control:
            self._sound_director.play()
            # Build interface:
            self._gameplay_administrator.set_gameplay_type()
            self._interface_controller.scale()
            # Image render:
            self._render.image_render()

            main_cycle_fps_clock.tick(main_cycle_fps)
            await sleep(0)

    async def _mvc_pattern(self):
        """
        MVC pattern main game loop.
        """
        try:
            await gather(
                    *[
                        self._render_loop(),
                        self._reactions_to_input_commands.input_commands_loop()
                    ]
                )
        except SystemExit as exit_statis:
            if exit_statis.code != 0:
                raise exit_statis

    @error_logger
    def __call__(self):
        """
        Main game loop call.
        """
        run(
            self._mvc_pattern()
        )
