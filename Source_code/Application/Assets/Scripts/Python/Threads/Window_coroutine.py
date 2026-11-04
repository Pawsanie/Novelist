from asyncio import sleep

from ..Fundamentals.Patterns import SingletonPattern
from ..Stage_Director.Stage_Director import StageDirector
from ..Render import Render
from ..User_Interface.Interface_Controller import InterfaceController
from ..Stage_Director.State_Machine import StateMachine
from ..GamePlay.GamePlay_Administrator import GamePlayAdministrator
from ..Audio_system.Sound_Director import SoundDirector
from ..Core import SettingsKeeper
from ..Render.Backend import Clock
"""
Contain game window thread code.
"""


class WindowThread(SingletonPattern):
    """
    Object responsible for window loop and image render.
    """
    def __init__(self):
        self._stage_director: StageDirector = StageDirector()
        self._sound_director: SoundDirector = SoundDirector()

        self._interface_controller: InterfaceController = InterfaceController()
        self._render: Render = Render()

        self._state_machine: StateMachine = StateMachine()
        self._gameplay_administrator: GamePlayAdministrator = GamePlayAdministrator()

    async def coroutine(self):
        """
        MVC pattern Model and View parts.
        """
        main_cycle_fps_clock: Clock = Clock(
            SettingsKeeper().get_frames_per_second()
        )

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

            main_cycle_fps_clock.tick()
            await sleep(0)
