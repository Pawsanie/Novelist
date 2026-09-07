from pygame import image, Surface
"""
Contains code responsible for 2D assets loader wrapper.
"""


def load_texture(
        *,
        path: str,
        alpha_chanel: bool
) -> Surface:
    """
    Load 2D texture from file system.
    :param path: Absolute path to file.
    :param alpha_chanel: Alpha channel processing required.
    """
    if alpha_chanel is True:
        return image.load(
            path
        ).convert_alpha()
    else:
        return image.load(
            path
        ).convert()
