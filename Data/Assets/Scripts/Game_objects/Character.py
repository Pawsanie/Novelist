from pygame import transform, Surface

from .Characters_calculations import character_sprite_size
from ..Application_layer.Assets_load import image_load, json_load
from .Background import BackgroundProxy
from ..Universal_computing.Surface_size import surface_size
from ..Render.Sprite import Sprite
"""
Contains code responsible for rendering character.
"""


class Character:
    """
    Super class for characters.
    Control characters by a lot of methods.
    """
    def __init__(self, *, character_image: Surface, sprite_sheet_data: dict | None = None,
                 poses: dict, animation: bool = False, name: str | None = None):
        """
        :param character_image: pygame.Surface with image loaded.
        :type character_image: pygame.Surface
        :param sprite_sheet_data: All poses coordinates for sprite animation.
        :type sprite_sheet_data: dict[dict[str, int]]
        :param poses: For animation sprites hold pose name. For statick sprite hold coordination for pose switch.
        :type poses: dict[str] | dict[str, [int, int]
        :param animation: Animation status for Sprite.
        :type animation: bool
        :param name: Character name.
        :type name: str
        """
        self.sprite: Sprite = Sprite(
            image=character_image,
            layer=2,
            sprite_sheet_data=sprite_sheet_data,
            name=name
        )
        self.coordinates_pixels: list[int, int] = [0, 0]
        self.character_size: tuple[int, int] = self.sprite.image.get_size()
        self.sprite_sheet_data: dict[str, dict[str, dict[str, list[int, int]]]] = sprite_sheet_data
        self.poses: dict = poses
        self.animation: bool = animation

        self.background: BackgroundProxy = BackgroundProxy()

        # [middle|right|left|custom] with 'middle' as default
        self.position: str = 'middle'
        # [first_plan|background_plan] with 'first_plan' as default
        self.plan: str = 'first_plan'
        # 1 as default
        self.pose_number: str = '1'
        self.default_animation: str = 'static'

        self.hidden: bool = True

    def move_custom(self, *, coordinates: list[int, int]):
        """
        Move character sprite to new point and update frame.
        :param coordinates: Tuple with x and y coordinates.
        """
        self.coordinates_pixels: list[int, int] = [coordinates[0], coordinates[1]]
        self.position: str = 'custom'

    def set_pose(self, *, pose_number: str):
        """
        Set pose for character sprite sheet.
        :param pose_number: Number of pose in character sprite, from character_poses dict key.
        :type pose_number: str
        """
        self.pose_number: str = pose_number
        if self.animation is True:
            self.sprite.animation_name = self.poses[self.pose_number]
        else:
            self.sprite.animation_name = self.default_animation
            self.sprite.statick_frame_key = int(self.pose_number)

    def reflect(self):
        """
        Reflect character sprite surface.
        """
        self.sprite.image = transform.flip(
            self.sprite.image,
            flip_x=True,
            flip_y=False
        )

    def scale(self):
        """
        Scale characters surface, with background context.
        """
        if self.hidden is True:
            return

        # Initialization:
        self.character_size: tuple[int, int] = character_sprite_size(
            character_surface=self.sprite.sprite_sheet[self.sprite.animation_name][int(self.pose_number)]
        )

        # Size scale:
        if self.plan == 'background_plan':
            size: tuple[int, int] = self.character_size
            self.character_size: tuple[int, int] = (
                int(size[0] * 0.8),
                int(size[1] * 0.8)
            )
            self.sprite.scale(self.character_size)

        if self.plan == 'first_plan':
            background_surface: Surface = self.background.get_data()[0]
            coordinates_difference: int = \
                background_surface.get_height() \
                - int(background_surface.get_height() * 0.9)
            fp_size: tuple[int, int] = (
                self.character_size[0],
                self.character_size[1] - coordinates_difference
            )
            self.sprite.scale(fp_size)

        # Position correction:
        if self.position == 'middle':
            self.move_to_middle()
        if self.position == 'right':
            self.move_to_right()
        if self.position == 'left':
            self.move_to_left()
        if self.position == 'custom':
            ...
        self.sprite.coordinates = self.coordinates_pixels

    def kill(self):
        """
        Remove the character from the stage.
        """
        self.hidden: bool = True

    def set_plan(self, *, plan: str):
        """
        Move character to first or background plan.
        :param plan: String [first_plan/background_plan].
        :type plan: str
        """
        self.plan: str = plan

    def middle_point_for_character_render(self) -> list[int, int]:
        """
        Calculation middle coordinates for character render.
        :return: List with coordinates of meddle point for character render.
        """
        screen_size: tuple[int, int] = surface_size(self.background.get_data()[0])
        sprite_size: tuple[int, int] = surface_size(self.sprite.image)
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

        # Animated Sprite:
        if character['sprite_sheet'] is True:
            sprite_sheet_data: dict = json_load([
                'Scripts',
                'Json_data',
                'Sprite_Sheet_data',
                'Characters',
                character["sprite"]
            ])
            result.update({str(character_name): Character(
                character_image=sprite,
                sprite_sheet_data=sprite_sheet_data,
                poses=character['poses'],
                animation=True,
                name=character_name
            )})

        # Statick Sprite:
        else:
            result.update({str(character_name): Character(
                character_image=sprite,
                sprite_sheet_data={'static': character['poses']},
                poses=character['poses'],
                name=character_name
            )})

    return result
