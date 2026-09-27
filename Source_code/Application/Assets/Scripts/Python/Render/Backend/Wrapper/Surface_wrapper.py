from pygame import Surface
from pygame.transform import scale, smoothscale
"""
Contains code responsible for Surface wrapper.
"""


def create_surface(
        *,
        width: int = 0,
        height: int = 0
) -> Surface:
    """
    Crate low-level Pygame Surface for Sprite.
    :param width: New Surface pixel width.
                  0 by default.
    :param height: New Surface pixel height.
                  0 by default.
    """
    return Surface(
        size=(
            width,
            height
        )
    )


def get_size(surface: Surface) -> [int, int]:
    """
    Calculation low-level Pygame Surface x/y size.
    :param surface: Pygame Surface object.
    """
    return (
        surface.get_width(),
        surface.get_height()
    )


def apply_texture(
        *,
        texture: Surface,
        surface: Surface,
        coordinates: tuple[int, int] = (0, 0)
):
    """
    Attach texture Surface to another Surface.
    :param texture: Pygame Surface object with texture.
    :param surface: Pygame Surface object for texture render.,
    :param coordinates: The x/y coordinates on the Surface from which the texture should be rendered in pixels.
                        (0, 0) ┌────────────────→ X
                               │
                               │   ┌──────────┐
                               │   │          │
                               │   │          │
                               │   └──────────┘
                               │
                               ↓
                               Y
    """
    surface.blit(
        source=texture,
        dest=coordinates
    )


def scale_surface(
        *,
        surface: Surface,
        size: tuple[int, int],
        fast: bool = False
) -> Surface:
    """
    Scale Surface to x/y size in pixels.
    :param surface: Pygame Surface object.
    :param size: Tuple with x/y size data.
    :param fast: If True a coarser and faster scaling method will be selected.
    """
    if not fast:
        return smoothscale(
            surface=surface,
            size=size
        )

    return scale(
        surface=surface,
        size=size
    )
