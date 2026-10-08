from ..Wrapper import (
    create_window,
    screen_clear,
    draw_on_window,
    screen_flip,
    get_window_size,
    set_window_icon,
    set_window_name
)
from ..Protocol import SurfaceProtocol, WindowProtocol
"""
Contains code responsible for Window bridge.
"""


class WindowBridge:
    """
    Window bridge object for Render.
    """
    def __int__(
            self, *,
            window_name: str,
            window_icon: SurfaceProtocol
    ):
        """
        :param window_name: Name for application Window.
        :param window_icon: Window icon Surface image.
        """
        set_window_name(
            window_name
        )
        set_window_icon(
            window_icon
        )
        self._window: None or WindowProtocol = None

    def clear(self):
        """
        Clear the window by filling it with black.
        """
        screen_clear(
            self._window
        )

    @staticmethod
    def get_size() -> tuple[int, int]:
        """
        Get window X/Y size.
        """
        return get_window_size()

    @staticmethod
    def flip():
        """
        Render new image on window screen.
        """
        screen_flip()

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
        draw_on_window(
            window=self._window,
            surface=surface,
            coordinates=coordinates
        )

    def get_window(self) -> WindowProtocol | None:
        """
        Get Window Surface object.
        """
        return self._window

    def update(
            self, *,
            width: int,
            height: int,
            full_screen_status: bool
    ) -> WindowProtocol:
        """
        Update window properties.
        :param width: New window width.
        :param height: New window height.
        :param full_screen_status: Full screen bool status.
        """
        self._window: WindowProtocol = create_window(
                width=width,
                height=height,
                full_screen=full_screen_status
        )
        return self._window
