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


class WindowBridge:
    def __int__(
            self, *,
            window_name: str,
            window_icon: SurfaceProtocol
    ):
        set_window_name(
            window_name
        )
        set_window_icon(
            window_icon
        )
        self._window: None or WindowProtocol = None

    def clear(self):
        screen_clear(
            self._window
        )

    @staticmethod
    def get_size() -> tuple[int, int]:
        return get_window_size()

    @staticmethod
    def flip():
        screen_flip()

    def draw(
            self, *,
            surface: SurfaceProtocol,
            coordinates: tuple[int, int]
    ):
        draw_on_window(
            window=self._window,
            surface=surface,
            coordinates=coordinates
        )

    def get_window(self) -> WindowProtocol | None:
        return self._window

    def update(
            self, *,
            width: int,
            height: int,
            full_screen_status: bool
    ):
        self._window: WindowProtocol = create_window(
                width=width,
                height=height,
                full_screen=full_screen_status
            )
