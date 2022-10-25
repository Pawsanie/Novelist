from pygame import transform, Surface, SRCALPHA

from .Render import character_sprite_size, meddle_point_for_character_render
from .Assets_load import image_load, json_load
"""
Contains code responsible for rendering character.
"""


class Character:
    """
    Super class for characters:
    """
    def __init__(self, *, surface: Surface, character_image: Surface, character_size: tuple,
                 coordinates_pixels: list[int], character_poses: dict, background_surface: Surface):
        """
        Load character image by name.
        Transform the art according to the screen size.
        :param surface: Must be pygame. Surface object.
        """
        self.surface = surface
        self.character_image = character_image
        self.coordinates_pixels = coordinates_pixels
        self.character_poses = character_poses
        self.background_surface = background_surface
        self.character_size = character_size
        surface.blit(character_image, (0, 0))

    def move(self, *, coordinates: list[int, int]):
        """
        Move character sprite to new point and update frame.
        :param coordinates: Tuple with x and y coordinates.
        """
        ald_coordinates = self.coordinates_pixels
        ald_coordinates[0], ald_coordinates[1] = coordinates[0], coordinates[1]

    def emotion(self):
        """
        Selects the correct part of the sprite to render on the surface.
        """
        self.surface.fill(None)

    def reflect(self):
        """
        Reflect character sprite surface
        """
        self.surface = transform.flip(self.surface, flip_x=True, flip_y=False)

    def scale(self):
        self.character_size = character_sprite_size(screen_surface=self.background_surface,
                                                    character_surface=self.surface)
        self.surface = transform.scale(self.surface, self.character_size)
        self.coordinates_pixels = meddle_point_for_character_render(screen_surface=self.background_surface,
                                                                    character_surface=self.surface)


def characters_generator(*, background_surface: Surface) -> dict[str, Character]:
    """
    Load data about characters and their sprites from json and make dict with Character class exemplars.
    :param background_surface: Background Surface.
    :return: Dictionary with 'character`s names as a keys and Character`s exemplar as values.
    """
    result = {}
    characters_list: dict = json_load(['Scripts',
                                       'Json_data',
                                       'characters_sprites.json'])
    for character_name in characters_list:
        character: dict = characters_list[character_name]
        sprite: Surface = image_load(art_name=character['sprite'],
                                     file_format='png',
                                     asset_type='Characters')
        character_poses: dict = character['poses']
        character_size_base: tuple[int, int] = (character_poses['1']['x'][1],
                                                character_poses['1']['y'][1])
        character_surface: Surface = Surface(character_size_base, SRCALPHA)
        coordinates_pixels: list[int] = meddle_point_for_character_render(screen_surface=background_surface,
                                                                          character_surface=character_surface)
        result.update({str(character_name): Character(surface=character_surface,
                                                      character_image=sprite,
                                                      character_size=character_size_base,
                                                      coordinates_pixels=coordinates_pixels,
                                                      character_poses=character_poses,
                                                      background_surface=background_surface)})

    return result
