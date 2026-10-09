from ..Bridge import WindowBridge
from ..Protocol import WindowProtocol, SurfaceProtocol
from ....Fundamentals.Patterns import SingletonPattern
"""
Contains code responsible for Window facade.
"""


class WindowFacade(SingletonPattern):
    """
    Window Facade object for Render.
    """
    def __init__(self):
        self._window_bridge: WindowBridge = WindowBridge(
            window_name=...,
            window_icon=...
        )
        self._window_bridge.update(
            width=...,
            height=...,
            full_screen_status=...
        )

    def clear(self):
        """
        Clear the window by filling it with black.
        """
        self._window_bridge.clear()

    def get_size(self) -> tuple[int, int]:
        """
        Get window X/Y size.
        """
        return self._window_bridge.get_size()

    def draw(
            self, *,
            surface: SurfaceProtocol,
            coordinates: tuple[int, int]
    ):
        """
        Render image in window.
        :param surface: Image for Render.
        :param coordinates: Coordinates for image render.
        """
        self._window_bridge.draw(
            surface=surface,
            coordinates=coordinates
        )

    def get_window(self) -> WindowProtocol:
        """
        Get Window low-level object.
        """
        return self._window_bridge.get_window()
