from pygame import transform, Surface, SRCALPHA

from .Characters_calculations import character_sprite_size
from ..Application_layer.Assets_load import image_load, json_load
from .Background import BackgroundProxy
from ..Universal_computing.Surface_size import surface_size
"""
Contains code responsible for rendering character.
"""


class Character:
    """
    Super class for characters.
    Control characters by a lot of methods.
    """
    def __init__(self, *, surface: Surface, character_image: Surface, character_size: tuple, character_poses: dict):
        """
        :param surface: Character surface object for render.
        :type surface: pygame.Surface
        :param character_image: pygame.Surface with image loaded.
        :type character_image: pygame.Surface
        :param character_size: Base character size.
        :type character_size: tuple[int, int]
        :param character_poses: All poses coordinates for sprite animation.
        :type character_poses: dict[dict[str, int]]
        """
        self.surface: Surface = surface
        self.character_image_safe: Surface = character_image
        self.character_image: Surface | None = None
        self.coordinates_pixels: list[int, int] = [0, 0]

        self.character_poses: dict = character_poses
        self.background: BackgroundProxy = BackgroundProxy()
        self.character_size: tuple[int, int] = character_size
        # [middle|right|left|custom] with 'middle' as default
        self.position: str = 'middle'
        # [first_plan|background_plan] with 'first_plan' as default
        self.plan: str = 'first_plan'
        # 1 as default
        self.pose_number: str = '1'

        self.hidden: bool = True

    def move_custom(self, *, coordinates: list[int, int]):
        """
        Move character sprite to new point and update frame.
        :param coordinates: Tuple with x and y coordinates.
        """
        self.coordinates_pixels: list[int, int] = [coordinates[0], coordinates[1]]
        self.position: str = 'custom'

    def get_pose(self):
        """
        Selects the correct part of the sprite to render on the surface.
        """
        # Surface change:
        pose_coordinates: dict = self.character_poses.get(self.pose_number)
        surface_x: list[int, int] = pose_coordinates.get('x')
        surface_y: list[int, int] = pose_coordinates.get('y')
        x_line: int = (surface_x[1] - surface_x[0])
        y_line: int = (surface_y[1] - surface_y[0])
        self.character_image: Surface = Surface((x_line, y_line), SRCALPHA)

        # Image pose change:
        sprite_coordinates: tuple[int, int] = (-surface_x[0], -surface_y[0])
        self.character_image.blit(self.character_image_safe, sprite_coordinates)

    def set_pose(self, *, pose_number: str):
        """
        Set pose for character sprite sheet.
        :param pose_number: Number of pose in character sprite, from character_poses dict key.
        """
        self.pose_number: str = pose_number

    def reflect(self):
        """
        Reflect character sprite surface.
        """
        self.surface: Surface = transform.flip(
            self.surface,
            flip_x=True,
            flip_y=False
        )

    def scale(self):
        """
        Scale characters surface, with background context.
        """
        # Initialization:
        self.get_pose()
        self.character_size: tuple[int, int] = character_sprite_size(
            character_surface=self.character_image
        )

        # Size scale:
        if self.plan == 'background_plan':
            size: tuple[int, int] = self.character_size
            self.character_size: tuple[int, int] = (
                int(size[0] * 0.8),
                int(size[1] * 0.8)
            )
            self.surface: Surface = transform.scale(self.character_image, self.character_size)

        if self.plan == 'first_plan':
            background_surface: Surface = self.background.get_data()[0]
            coordinates_difference: int = \
                background_surface.get_height() \
                - int(background_surface.get_height() * 0.9)
            fp_size: tuple[int, int] = (
                self.character_size[0],
                self.character_size[1] - coordinates_difference
            )
            self.surface: Surface = Surface(fp_size, SRCALPHA)
            self.character_image: Surface = transform.scale(self.character_image, self.character_size)
            self.surface.blit(self.character_image, (0, 0))

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
        self.hidden: bool = True

    def set_plan(self, *, plan: str):
        """
        Move character to first or background plan.
        :param plan: String [first_plan/background_plan].
        """
        self.plan: str = plan

    def middle_point_for_character_render(self) -> list[int, int]:
        """
        Calculation middle coordinates for character render.
        :return: List with coordinates of meddle point for character render.
        """
        screen_size: tuple[int, int] = surface_size(self.background.get_data()[0])
        sprite_size: tuple[int, int] = surface_size(self.surface)
        background_y_coordinate: int = self.background.background_coordinates[1]

        # X:
        x_coordinate: int = int(
            (screen_size[0] // 2)
            - (sprite_size[0] // 2)
        )

        # Y:
        y_coordinate: int = int(
            (screen_size[1] - sprite_size[1])
            + background_y_coordinate
        )

        return [x_coordinate, y_coordinate]

    def move_to_middle(self):
        """
        Move character to middle of scene.
        """
        x_coordinate, y_coordinate = self.middle_point_for_character_render()
        self.coordinates_pixels: list[int, int] = [
            int(
                x_coordinate
                + self.background.background_coordinates[0]
            ),
            y_coordinate
        ]
        self.position: str = 'middle'

    def move_to_left(self):
        """
        Move character to right of scene.
        """
        x_coordinate, y_coordinate = self.middle_point_for_character_render()
        self.coordinates_pixels: list[int, int] = [
            int(
                x_coordinate // 3
                + self.background.background_coordinates[0]
            ),
            y_coordinate
        ]
        self.position: str = 'left'

    def move_to_right(self):
        """
        Move character to right of scene.
        """
        x_coordinate, y_coordinate = self.middle_point_for_character_render()
        self.coordinates_pixels: list[int, int] = [
            int(
                x_coordinate * 1.64
                + self.background.background_coordinates[0]
            ),
            y_coordinate
        ]
        self.position: str = 'right'


def characters_generator() -> dict[str, Character]:
    """
    Load data about characters and their sprites from json and make dict with Character class exemplars.

    :return: Dictionary with character`s names as a keys and Character`s exemplar as values.
    """
    result: dict = {}
    characters_list: dict = json_load([
        'Scripts',
        'Json_data',
        'characters_sprites'
    ])
    for character_name in characters_list:
        character: dict = characters_list[character_name]
        sprite: Surface = image_load(
            art_name=character['sprite'],
            file_format='png',
            asset_type='Characters'
        )
        character_poses: dict = character['poses']
        character_size_base: tuple[int, int] = (
            character_poses['1']['x'][1],
            character_poses['1']['y'][1]
        )
        character_surface: Surface = Surface(character_size_base, SRCALPHA)
        result.update({str(character_name): Character(
            surface=character_surface,
            character_image=sprite,
            character_size=character_size_base,
            character_poses=character_poses
        )})

    return result
