from pygame import transform, Surface, SRCALPHA

from .Render import character_sprite_size, meddle_point_for_character_render, surface_size
from .Assets_load import image_load, json_load
"""
Contains code responsible for rendering character.
"""


class Character:
    """
    Super class for characters.
    Control characters by a lot of methods.

    :param surface: Character surface object for render.
    :type surface: pygame.Surface
    :param character_image: Surface with image loaded.
    :type character_image: pygame.Surface
    :param character_size: Base character size.
    :type character_size: tuple[int, int]
    :param coordinates_pixels: Base coordinates for character render.
    :type coordinates_pixels: list[int, int]
    :param character_poses: All poses coordinates for sprite animation.
    :type character_poses: dict[dict[str, int]]
    :param background_surface: Surface with background.
    :type background_surface: pygame.Surface
    """
    def __init__(self, *, surface: Surface, character_image: Surface, character_size: tuple,
                 coordinates_pixels: list[int], character_poses: dict, background_surface: Surface):
        self.surface: Surface = surface
        self.character_image: Surface = character_image
        self.coordinates_pixels: list[int, int] = coordinates_pixels
        self.character_poses: dict = character_poses
        self.background_surface: Surface = background_surface
        self.character_size: tuple[int, int] = character_size
        self.position: str = 'middle'  # [middle/right/left/custom] as 'middle' as default
        self.plan: str = 'first_plan'  # [first_plan/background_plan] as 'first_plan' as default
        self.pose_number: str = '1'  # 1 as default
        self.surface.blit(character_image, (0, 0))
        # Render flag, for scale:
        self.scale_background_old_size_flag: tuple[int, int] = (0, 0)

    def move_custom(self, *, coordinates: list[int, int]):
        """
        Move character sprite to new point and update frame.
        :param coordinates: Tuple with x and y coordinates.
        """
        self.coordinates_pixels: list[int, int] = [coordinates[0], coordinates[1]]
        self.position = 'custom'

    def set_pose(self, *, pose_number: str):
        """
        Selects the correct part of the sprite to render on the surface.
        :param pose_number: Number of pose in character sprite, from character_poses dict key.
        """
        # Surface change:
        pose_coordinates: dict = self.character_poses.get(pose_number)
        surface_x: list[int, int] = pose_coordinates.get('x')
        surface_y: list[int, int] = pose_coordinates.get('y')
        x_line: int = (surface_x[1] - surface_x[0])
        y_line: int = (surface_y[1] - surface_y[0])
        self.surface: Surface = Surface((x_line, y_line), SRCALPHA)
        # Image pose change:
        sprite_coordinates: tuple[int, int] = (-surface_x[0], -surface_y[0])
        self.surface.blit(self.character_image, sprite_coordinates)
        self.pose_number: str = pose_number

    def reflect(self):
        """
        Reflect character sprite surface.
        """
        self.surface: Surface = transform.flip(self.surface, flip_x=True, flip_y=False)

    def scale(self, *, background_surface):
        """
        Scale characters surface, with background context.
        """
        self.background_surface = background_surface
        self.character_size: tuple[int, int] = character_sprite_size(background_surface=self.background_surface,
                                                                     character_surface=self.surface)
        if self.scale_background_old_size_flag != surface_size(self.background_surface):
            self.scale_background_old_size_flag: tuple[int, int] = surface_size(self.background_surface)
            # Size scale:
            if self.plan == 'background_plan':
                size: tuple[int, int] = self.character_size
                self.character_size = (int(size[0] * 0.8), int(size[1] * 0.8))
                self.surface: Surface = transform.scale(self.surface, self.character_size)
                self.surface.blit(self.character_image, self.character_size)
            if self.plan == 'first_plan':
                self.surface: Surface = transform.scale(self.surface, self.character_size)
                self.surface.blit(self.character_image, self.character_size)
            # Position correction:
            if self.position == 'middle':
                self.move_to_middle()
            if self.position == 'right':
                self.move_to_right()
            if self.position == 'left':
                self.move_to_left()
            if self.position == 'custom':
                ...

    def kill(self):
        """
        Remove the character from the stage.
        """
        self.surface = Surface((0, 0), SRCALPHA)

    def set_plan(self, *, plan: str):
        """
        Move character to first or background plan.
        :param plan: String [first_plan/background_plan].
        """
        self.plan: str = plan
        self.set_pose(pose_number=self.pose_number)

    def move_to_middle(self):
        """
        Move character to middle of scene.
        """
        if self.plan == 'background_plan':
            self.coordinates_pixels: list[int, int] = meddle_point_for_character_render(
                screen_surface=self.background_surface, character_surface=self.surface)
        if self.plan == 'first_plan':
            coordinates_pixels: list[int, int] = meddle_point_for_character_render(
                screen_surface=self.background_surface, character_surface=self.surface)
            coordinates_pixels_y: int = \
                self.background_surface.get_height() - int(self.background_surface.get_height() * 0.9)
            self.coordinates_pixels: list[int, int] = [coordinates_pixels[0], coordinates_pixels_y]
        self.position = 'middle'

    def move_to_left(self):
        """
        Move character to right of scene.
        """
        self.move_to_middle()
        coordinates_pixels: list[int, int] = self.coordinates_pixels
        self.coordinates_pixels = [coordinates_pixels[0] // 3, coordinates_pixels[1]]
        self.position = 'left'

    def move_to_right(self):
        """
        Move character to right of scene.
        """
        self.move_to_middle()
        coordinates_pixels: list[int, int] = self.coordinates_pixels
        self.coordinates_pixels = [int(coordinates_pixels[0] * 1.64), coordinates_pixels[1]]
        self.position = 'right'


def characters_generator(*, background_surface: Surface) -> dict[str, Character]:
    """
    Load data about characters and their sprites from json and make dict with Character class exemplars.

    :param background_surface: Background Surface.
    :return: Dictionary with 'character`s names as a keys and Character`s exemplar as values.
    """
    result = {}
    characters_list: dict = json_load(['Scripts',
                                       'Json_data',
                                       'characters_sprites'])
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
