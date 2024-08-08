from pygame import Surface

from ..Universal_computing.Surface_size import surface_size
from .Background import Background
"""
Contains the code for characters computing.
"""


def character_sprite_size(character_surface: Surface) -> tuple[int, int]:
    """
    Calculation character surface size.
    Formula: Character_Sprite[x] + Background_and_Character_Sprite[x]_difference percent:
    coefficient = x / 100 ->
    percent_difference = Character_Sprite / Background * 100 ->
    difference = coefficient * (100 - percent_difference) ->
    x = Character_Sprite[size] + difference
    Or: Character_Sprite[x] - Background_and_Character_Sprite[x]_difference percent:
    percent_difference = Background / Character_Sprite * 100 ->
    x = Character_Sprite[size] * (1 - (100 - percent_difference) / 100)
    Formula: Character_Sprite[Y]:
    Character_Sprite[Y] = Background[Y]

    :param character_surface: pygame.Surface of character.
    :return: Tuple with x and y sizes for character`s images.
             These sizes depends of main frame size.
    """
    background_surface: Background = Background()
    result_size_x, result_size_y = (0, 0)
    screen_size: tuple[int, int] = background_surface.get_size()
    sprite_size: tuple[int, int] = surface_size(character_surface)

    if sprite_size[1] != screen_size[1]:
        result_size_y: int = screen_size[1]
        if sprite_size[1] < screen_size[1]:
            percent_size_sprite_difference = int(sprite_size[1] / screen_size[1] * 100)
            coefficient: int | float = sprite_size[0] / 100
            percent_integer: int | float = coefficient * (100 - percent_size_sprite_difference)
            result_size_x = int(sprite_size[0] + percent_integer)
        if sprite_size[1] > screen_size[1]:
            percent_size_sprite_difference = int(screen_size[1] / sprite_size[1] * 100)
            result_size_x = int(sprite_size[0] * (1 - ((100 - percent_size_sprite_difference) / 100)))
    else:
        return sprite_size

    return result_size_x, result_size_y
