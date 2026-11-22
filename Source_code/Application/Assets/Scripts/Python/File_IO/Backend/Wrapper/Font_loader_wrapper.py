from pygame.font import Font
"""
Contains code responsible for Font assets loader wrapper.
"""


def load_font(
        *,
        path: str,
        size: int
) -> Font:
    """
    Load Text font from file system.
    :param path: Absolute path to file.
    :param size: The size at which the asset will be baked.
    """
    return Font(
        name=path,
        size=size
    )
