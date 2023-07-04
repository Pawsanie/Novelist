from pygame import Surface
"""
Contains a universal function for determining the size of surfaces.
"""


def surface_size(interested_surface: Surface) -> [int, int]:
    """
    Calculation surface size.

    :param interested_surface: pygame.Surface object.
    :return: Surface size with 2 init`s.
    """
    character_sprite_size_x: int = interested_surface.get_width()
    character_sprite_size_y: int = interested_surface.get_height()
    return character_sprite_size_x, character_sprite_size_y
