from pygame import Surface, display, FULLSCREEN, RESIZABLE
"""
Contains code responsible for Window wrapper.
"""


def create_window(
        *,
        width: int,
        height: int,
        full_screen: bool = True
) -> Surface:
    """
    Create low-level Pygame Window Surface.
    :param width: Window width in pixels.
    :param height: Window height in pixels.
    :param full_screen: Should the window fill the entire screen or be resizable?
    """
    def set_window_settings(
            constant: FULLSCREEN | RESIZABLE
    ) -> Surface:
        return display.set_mode(
            (width, height),
            constant
        )

    return set_window_settings(
        constant=\
        FULLSCREEN if full_screen
        else RESIZABLE
    )


def set_window_name(window_name: str):
    """
    Sets the name for a Window that can be created later.
    To ensure correct operation, this action must be performed to create the Window.
    :param window_name: Application window name string.
    """
    display.set_caption(
        window_name
    )


def set_window_icon(icon_surface: Surface):
    """
    Sets the icon for a Window that can be created later.
    To ensure correct operation, this action must be performed to create the Window.
    :param icon_surface: Pygame Surface object.
    """
    display.set_icon(
        icon_surface
    )


def screen_clear(window: Surface):
    """
    Clear low-level Window.
    """
    window.fill(
        (
            0,  # R
            0,  # G
            0  # B
        )
    )


def draw_on_window(
        *,
        window: Surface,
        surface: Surface,
        coordinates: tuple[int, int] = (0, 0)
):
    """
    Attach low-level Surface to Window Surface.
    :param window: Screen Pygame display Surface object.
    :param surface: Pygame Surface object.
    :param coordinates: The x/y coordinates at which the Surface is to be drawn on the Window in pixels.
                        As example:
                        Window coordinate axes.
                        (0, 0) ┌────────────────→ X
                               │  (X/Y)
                               │   ┌───────────┐
                               │   │           │
                               │   │  Surface  │
                               │   │           │
                               │   └───────────┘
                               ↓
                               Y
    """
    window.blit(
        source=surface,
        dest=coordinates
    )


def screen_flip():
    """
    Flip low-level window and render new image.
    """
    display.update()


def get_window_size() -> tuple[int, int]:
    """
    Get Window size in pixels.
    """
    return display.get_window_size()
