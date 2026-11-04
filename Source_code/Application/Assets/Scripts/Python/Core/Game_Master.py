from asyncio import run, gather

from ..Fundamentals.Logging import error_logger
from ..Fundamentals.Patterns import SingletonPattern
from .Initialization import initialization
from ..Threads import WindowThread, InputThread
"""
Contains code for GameMaster.
"""


class GameMaster(SingletonPattern):
    """
    Set all settings for Stage Director and game.
    Entry point for gameplay.
    Control gameplay, menus and display image render.
    """
    def __init__(self):
        initialization()

        # Threads:
        self._window_thread: WindowThread = WindowThread()
        self._input_thread: InputThread = InputThread()

    async def _mvc_pattern(self):
        """
        MVC pattern main loop.
        """
        try:
            await gather(
                    *[
                        self._window_thread.coroutine(),
                        self._input_thread.coroutine()
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
