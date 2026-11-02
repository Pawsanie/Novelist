from pygame import time
from pygame.time import Clock

from ....Fundamentals.Patterns import SingletonPattern
"""
Contains the global clock wrapper code.
"""


class ClockWrapper(SingletonPattern):
    """
    Pygame global cloack wrapper.
    """
    def __init__(self, main_cycle_fps: int):
        """
        :param main_cycle_fps: The frequency at which the simulation should be updated.
        """
        self._clock: Clock = time.Clock()
        self._main_cycle_fps: int = main_cycle_fps

    def set_fps(self, fps: int):
        """
        Set the frames per second rate for updating the simulation.
        :param fps: The frequency at which the simulation should be updated.
        """
        self._main_cycle_fps: int = fps

    @staticmethod
    def get_real_time() -> int:
        """
        Get real unix time from the counts the moment of time subsystem initialization.
        """
        return time.get_ticks()

    def tick(self) -> int:
        """
        Updates the time of the C++ cloack and returns the time since the previous call, including the delay.
        """
        return self._clock.tick(
            self._main_cycle_fps
        )
