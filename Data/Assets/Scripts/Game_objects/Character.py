from ..Universal_computing.Assets_load import AssetLoader
from ..Render.Sprite import Sprite
from .Background import Background
from ..Render.Texture_Master import TexturesMaster
"""
Contains code responsible for rendering character.
"""


class Character:
    """
    Super class for characters.
    Control characters by a lot of methods.
    """
    def __init__(self, *, character_texture_mame: str, sprite_sheet_data: dict | None = None,
                 poses: dict, animation: bool = False, name: str | None = None):
        """
        :param character_texture_mame: Texture name for TextureMaster.
        :type character_texture_mame: str
        :param sprite_sheet_data: All poses coordinates for sprite animation.
        :type sprite_sheet_data: dict[dict[str, int]]
        :param poses: For animation sprites hold pose name. For statick sprite hold coordination for pose switch.
        :type poses: dict[str] | dict[str, [int, int]
        :param animation: Animation status for Sprite.
        :type animation: bool
        :param name: Character name.
        :type name: str
        """
        # Program layers settings:
        self._texture_master: TexturesMaster = TexturesMaster()

        # Game scene objects settings:
        self._background: Background = Background()

        # Sprite settings:
        self._sprite_sheet_data: dict[str, dict[str, dict[str, list[int, int]]]] = sprite_sheet_data | {
            "texture_type": "Characters"
        }
        self._texture_name: str = character_texture_mame
        self._sprite: Sprite = Sprite(
            texture_mame=self._texture_name,
            layer=2,
            sprite_sheet_data=self._sprite_sheet_data,
            name=name
        )
        self._character_sprite_size: tuple[int, int] = (0, 0)  # self._get_character_sprite_size()

        # Character settings:
        self._sprite_coordinates: tuple[int, int] = (0, 0)
        self._poses: dict = poses
        self.animation: bool = animation

        # [middle|right|left] with 'middle' as default
        self._position: str = 'middle'
        # [first_plan|background_plan] with 'first_plan' as default
        self._plan: str = 'first_plan'
        # 1 as default
        self.pose_number: str = '1'
        self.default_animation: str = 'statick_frames'

        self.hidden: bool = True

    def set_position(self, position: str):
        """
        Use in Stage Director.
        :param position: middle|right|left
        :param position: str
        """
        self._position: str = position

    def _get_character_sprite_size(self) -> tuple[int, int]:
        return self._texture_master.get_texture_size(
            texture_name=self._texture_name,
            texture_type="Characters",
            animation_name=self._sprite.get_animation_name(),
            frame=self._sprite.get_frame_number()
        )

    def _scale_character_sprite_size(self):
        """
        Scale size for screen image.
        """
        self._texture_master.devnull_temporary_texture(
            texture_type="Characters",
            texture_name=self._texture_name,
            animation_name=self._sprite.get_animation_name(),
            frame=self._sprite.get_frame_number()
        )
        screen_size_x, screen_size_y = self._background.get_size()
        sprite_size_x, sprite_size_y = self._get_character_sprite_size()

        if sprite_size_y == screen_size_y:
            self._character_sprite_size: tuple[int, int] = (
                sprite_size_x,
                sprite_size_y
            )
            return
        result_size_y: int = screen_size_y
        result_size_x: int = 0
        if sprite_size_y < screen_size_y:
            percent_size_sprite_difference: int = int(
                sprite_size_y / screen_size_y * 100
            )
            coefficient: int | float = sprite_size_x / 100
            percent_integer: int | float = coefficient * (100 - percent_size_sprite_difference)
            result_size_x: int = int(
                sprite_size_x + percent_integer
            )
        elif sprite_size_y > screen_size_y:
            percent_size_sprite_difference: int = int(screen_size_y / sprite_size_y * 100)
            result_size_x: int = int(
                sprite_size_x * (1 - ((100 - percent_size_sprite_difference) / 100))
            )
        self._character_sprite_size: tuple[int, int] = result_size_x, result_size_y

    def get_sprite(self) -> Sprite:
        """
        Use in StageDirector.
        """
        return self._sprite

    def set_pose(self, *, pose_number: str):
        """
        Set pose for character sprite sheet.
        :param pose_number: Number of pose in character sprite, from character_poses dict key.
        :type pose_number: str
        """
        self.pose_number: str = pose_number
        if self.animation is True:
            self._sprite.animation_name = self._poses[self.pose_number]
        else:
            self._sprite.animation_name = self.default_animation
            self._sprite.statick_frame_key = int(self.pose_number)

    def scale(self):
        """
        Scale characters surface, with background context.
        """
        if self.hidden is True:
            return

        # Initialization:
        self._scale_character_sprite_size()

        # Size scale:
        if self._plan == 'background_plan':
            size: tuple[int, int] = self._character_sprite_size
            self._character_sprite_size: tuple[int, int] = (
                int(size[0] * 0.8),
                int(size[1] * 0.8)
            )
            self._sprite.scale(self._character_sprite_size)

        if self._plan == 'first_plan':
            background_surface: tuple[int, int] = self._background.get_size()
            background_height: int = background_surface[1]
            coordinates_difference: int = \
                background_height - int(background_height * 0.9)
            fp_size: tuple[int, int] = (
                self._character_sprite_size[0],
                self._character_sprite_size[1] - coordinates_difference
            )
            self._sprite.scale(fp_size)
        self._sprite.set_recache_status(False)

        # Position correction:
        if self._position == 'middle':
            self._move_to_middle()
        elif self._position == 'right':
            self._move_to_right()
        elif self._position == 'left':
            self._move_to_left()

        self._sprite.set_coordinates(
            self._sprite_coordinates
        )

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
        self._plan: str = plan

    def _middle_point_for_character_render(self) -> tuple[int, int]:
        """
        Calculation middle coordinates for character render.
        :return: List with coordinates of meddle point for character render.
        """
        screen_size_x, screen_size_y = self._background.get_size()
        sprite_size_x, sprite_size_y = self._sprite._image_size
        background_y_coordinate: int = self._background.get_coordinates()[1]

        # X:
        x_coordinate: int = int(
            (screen_size_x // 2)
            - (sprite_size_x // 2)
        )

        # Y:
        y_coordinate: int = int(
            (screen_size_y - sprite_size_y)
            + background_y_coordinate
        )

        return x_coordinate, y_coordinate

    def _move_to_middle(self):
        """
        Move character to middle of scene.
        """
        x_coordinate, y_coordinate = self._middle_point_for_character_render()
        self._sprite_coordinates: tuple[int, int] = (
            int(
                x_coordinate
                + self._background.get_coordinates()[0]
            ),
            y_coordinate
        )
        self._position: str = 'middle'

    def _move_to_left(self):
        """
        Move character to right of scene.
        """
        x_coordinate, y_coordinate = self._middle_point_for_character_render()
        self._sprite_coordinates: tuple[int, int] = (
            int(
                x_coordinate // 3
                + self._background.get_coordinates()[0]
            ),
            y_coordinate
        )
        self._position: str = 'left'

    def _move_to_right(self):
        """
        Move character to right of scene.
        """
        x_coordinate, y_coordinate = self._middle_point_for_character_render()
        self._sprite_coordinates: tuple[int, int] = (
            int(
                x_coordinate * 1.64
                + self._background.get_coordinates()[0]
            ),
            y_coordinate
        )
        self._position: str = 'right'


def characters_generator() -> dict[str, Character]:
    """
    Load data about characters and their sprites from json and make dict with Character class exemplars.
    :return: Dictionary with character`s names as a keys and Character`s exemplar as values.
    """
    asset_loader: AssetLoader = AssetLoader()
    result: dict = {}
    characters_list: dict = asset_loader.json_load(
        [
            'Scripts',
            'Json_data',
            'characters_sprites'
        ]
    )

    for character_name in characters_list:
        character: dict = characters_list[character_name]
        sprite_sheet_data: dict = asset_loader.json_load(
            [
                'Scripts',
                'Json_data',
                'Texture_data',
                'Characters',
                character["texture"]
            ]
        )
        result.update(
            {
                str(character_name): Character(
                    character_texture_mame=character['texture'],
                    sprite_sheet_data=sprite_sheet_data,
                    poses=character['animations'],
                    animation=sprite_sheet_data["sprite_sheet"],
                    name=character_name
                )
            }
        )
    return result
