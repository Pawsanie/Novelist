from pygame import transform, Surface, SRCALPHA

from .Render import render, character_sprite_size, meddle_point_for_character_render
"""
Contains code responsible for rendering character.
"""


class Character:
    """
    Super class for characters:
    """
    def __init__(self, *, surface: Surface, character_image: Surface, character_size: tuple):
        """
        Load character image by name.
        Transform the art according to the screen size.
        :param surface: Must be pygame. Surface object.
        """
        self.surface = surface
        # character_image = transform.scale(character_image, character_size)
        self.character_image = character_image
        surface.blit(character_image, (0, 0))

    def move(self, *, characters_list, coordinates: list[int, int]):
        """
        Move character sprite to new point and update frame.
        :param characters_list: Tuple with variables which loaded character`s_images.
                            As the rule variable names must be character`s names
        :param coordinates: Tuple with x and y coordinates.
        """
        character_image = self.character_image
        # surface = self.surface
        character_name = f"{character_image=}".split('=')[0]
        ald_coordinates = characters_list.get(character_name).get('coordinates_pixels')
        ald_coordinates[0], ald_coordinates[1] = coordinates[0], coordinates[1]

    def emotion(self):
        """
        Selects the correct part of the sprite to render on the surface.
        """
        surface = self.surface

    def reflect(self):
        """
        Reflect character sprite surface
        """
        surface = self.surface


def characters_generator(*, characters_list: tuple, background_surface: Surface, character_name: str)\
        -> dict[str, dict[str, Surface, Character, list[int, int]]]:
    """
    :param characters_list: Tuple with variables which loaded character`s_images.
                            As the rule variable names must be character`s names
    :param background_surface: Background Surface.
    :param character_name: String from variable name as the rule.
    :return: Dictionary with 'character`s surfaces', 'character`s arts' and character`s coordinates in pixels.
    """
    result = {}
    for character in characters_list:
        character_size: tuple[int] = character_sprite_size(screen_surface=background_surface,
                                                           character_surface=character)
        character: Surface = transform.scale(character, character_size)
        coordinates_pixels: list[int] = meddle_point_for_character_render(screen_surface=background_surface,
                                                                          character_surface=character)

        # character_name = '%(character)s' % locals()
        character_surface = Surface(character_size, SRCALPHA)
        result.update({character_name: {'surface': character_surface,
                                        'character_art': Character(surface=character_surface,
                                                                   character_image=character,
                                                                   character_size=character_size),
                                        'coordinates_pixels': coordinates_pixels}})

    return result

