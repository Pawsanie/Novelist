from pygame import Surface, time

from .Sprite_animation_pause import SpriteAnimationPause
from .Texture_Master import TexturesMaster
"""
Responsible for the code of a sprites used in rendering.
"""


class Sprite:
    """
    Spites uses in batch rendering.
    """
    def __init__(self, *, layer: int = 1, coordinates: tuple[int, int] = (0, 0), texture_mame: str,
                 name: str | None = None, sprite_sheet_data: dict | None = None):
        """
        :param layer: Layer for sprite render.
                      1 as default.
        :type layer: int
        :param coordinates: Coordinates for sprite render.
                            (0, 0) as default.
        :type coordinates: tuple[int, int]
        :param name: Sprite name.
                     None as default.
        :type name: str | None
        """
        # Program layers settings:
        self._texture_master: TexturesMaster = TexturesMaster()

        # Arguments processing:
        self._name: str | None = name
        self._layer: int = layer
        self._coordinates: tuple[int, int] = coordinates
        self._texture_id: str = texture_mame

        # Other settings:
        self._frame_time: int = time.get_ticks()

        self._sprite_sheet_data: dict | None = sprite_sheet_data
        self._image_size: tuple[int, int] = (0, 0)

        # Sprite sheet animation data:
        self._animation_name: str | None = None
        self._statick_frame_key: int | None = None
        self._last_frame_number: int = -1
        self._sprite_sheet_frame: int = 0

    def blit(self, any_surface: Surface):
        """
        Draw sprite on surface.
        :param any_surface: Any Surface.
        :type any_surface: Surface
        """
        self._sprite_sheet_next_frame()
        if self._texture_master.get_texture_size(
                texture_type=self._sprite_sheet_data["texture_type"],
                texture_name=self._texture_id,
                frame=self._sprite_sheet_frame
        ) != self._image_size:
            self._texture_master.set_new_scale_frame(
                texture_type=self._sprite_sheet_data["texture_type"],
                texture_name=self._texture_id,
                frame=self._sprite_sheet_frame,
                image_size=self._image_size
            )

        self._texture_master.get_texture(
            texture_type=self._sprite_sheet_data["texture_type"],
            texture_name=self._texture_id,
            animation=self._animation_name,
            frame=self._sprite_sheet_frame
        ).blit(any_surface, self._coordinates)

    def _sprite_sheet_next_frame(self):
        """
        Switch frames in Sprite 2d animation if possible.
        """
        if self._sprite_sheet_data is None:
            return

        if self._animation_name is None:
            self._animation_name: str = list(
                self._sprite_sheet_data.keys()
            )[0]

        if self._statick_frame_key is None:
            self._sprite_sheet_frame: int = self.get_frame_number()
        else:
            self._sprite_sheet_frame: int = self._statick_frame_key - 1

    @SpriteAnimationPause()
    def get_frame_number(self) -> int:
        """
        Get step for sprite sheet frame swap.
        :result: int
        """
        if (time.get_ticks() - self._frame_time) / 1000 >= (
                self._sprite_sheet_data[self._animation_name]["time_duration"]
                / len(self._sprite_sheet_data[self._animation_name]["frames"])
        ):
            self._frame_time: int = time.get_ticks()
            if self._last_frame_number + 1 <= len(
                    self._sprite_sheet_data[self._animation_name]["frames"]
            ) - 1:
                self._last_frame_number += 1
            else:
                self._last_frame_number: int = 0

        # TODO: SpriteAnimationPause call "-1" frame stabilisation:
        # TODO: Think about how to move it to SpriteAnimationPause class...
        if self._last_frame_number < 0:
            self._last_frame_number: int = 0

        return self._last_frame_number

    def scale(self, size: tuple[int, int]):
        """
        Scale Sprite image to size.
        :param size: Tuple with x/y size data.
        :type size: tuple[int, int]
        """
        self._image_size: tuple[int, int] = size

    def play_animation(self, animation_name: str):
        """
        Set new animation to play.
        """
        self._animation_name: str = animation_name
