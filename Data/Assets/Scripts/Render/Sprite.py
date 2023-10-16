from pygame import Surface, time, SRCALPHA, transform

from .Sprite_animation_pause import SpriteAnimationPause
"""
Responsible for the code of a sprites used in rendering.
"""


class Sprite:
    """
    Spites uses in batch rendering.
    """
    def __init__(self, *, image: Surface, layer: int = 1, coordinates: tuple[int, int] = (0, 0),
                 name: str | None = None, sprite_sheet_data: dict[str, list[int, int]] | None = None):
        """
        :param image: Pygame.Surface for sprite render.
        :type image: Surface
        :param layer: Layer for sprite render.
                      1 as default.
        :type layer: int
        :param coordinates: Coordinates for sprite render.
                            (0, 0) as default.
        :type coordinates: tuple[int, int]
        :param name: Sprite name.
                     None as default.
        :type name: str | None
        :param sprite_sheet_data: Dict with sprite sheet animations coordinates.
                                  None as default.
        :type sprite_sheet_data: dict[str, list[int, int]] | None
        """
        # Program layers settings:
        self.frame_time: int = time.get_ticks()

        # Arguments processing:
        self.name: str | None = name
        self.image_safe: Surface = image
        self.image: Surface = image
        self.layer: int = layer
        self.coordinates: tuple[int, int] = coordinates

        self.frames: str = "frames"
        self.time_duration: str = "time_duration"
        self.sprite_sheet: dict[str, dict[str, list[Surface] | float | None]] | None = \
            self.make_sprite_sheet(sprite_sheet_data)
        self.animation_name: str | None = None

        self.statick_frame_key: int | None = None
        self.last_frame_number: int = -1

    def blit(self, any_surface: Surface):
        """
        Draw sprite on surface.
        :param any_surface: Any Surface.
        :type any_surface: Surface
        """
        self.image.blit(any_surface, self.coordinates)

    def sprite_sheet_next_frame(self):
        """
        Switch frames in Sprite 2d animation if possible.
        """
        if self.sprite_sheet is None:
            return

        if self.animation_name is None:
            self.animation_name: str = list(self.sprite_sheet.keys())[0]

        if self.statick_frame_key is None:
            sprite_sheet_frame: int = self.get_frame_number()
        else:
            sprite_sheet_frame: int = self.statick_frame_key - 1

        self.image: Surface = self.sprite_sheet[self.animation_name][self.frames][sprite_sheet_frame]

    @SpriteAnimationPause()
    def get_frame_number(self) -> int:
        """
        Get step for sprite sheet frame swap.
        :result: int
        """
        if (time.get_ticks() - self.frame_time) / 1000 >= (
                self.sprite_sheet[self.animation_name][self.time_duration]
                / len(self.sprite_sheet[self.animation_name][self.frames])
        ):
            self.frame_time: int = time.get_ticks()
            if self.last_frame_number + 1 <= len(
                    self.sprite_sheet[self.animation_name][self.frames]
            ) - 1:
                self.last_frame_number += 1
            else:
                self.last_frame_number: int = 0
        return self.last_frame_number

    def scale(self, size: tuple[int, int]):
        """
        Scale Sprite image to size.
        :param size: Tuple with x/y size data.
        :type size: tuple[int, int]
        """
        self.image: Surface = Surface(size, SRCALPHA)
        self.sprite_sheet_next_frame()
        self.image: Surface = transform.scale(self.image, size)

    def make_sprite_sheet(self, sprite_sheet_data) -> dict[str, list[Surface]] | None:
        """
        Make sprite sheet for Sprite if it`s possible.
        None or Dictionary with animation names as keys and Surfaces in lists as values as a result.
        :param sprite_sheet_data: Dictionary with animation names as keys and sprite sheet frame coordinates as values.
        :type sprite_sheet_data: dict
        :result: dict[str, list[Surface]] | None
        """
        if sprite_sheet_data is None:
            return None

        result: dict = {}
        for animation in sprite_sheet_data:
            animation_sprite_sheet: list = []
            for frame_name in sprite_sheet_data[animation][self.frames]:
                frame: dict = sprite_sheet_data[animation][self.frames][frame_name]
                frame_image: Surface = Surface(
                    (
                        frame['x'][1] - frame['x'][0],
                        frame['y'][1] - frame['y'][0]
                    ),
                    SRCALPHA
                )
                frame_image.blit(
                    self.image_safe,
                    (
                            - frame['x'][0],
                            - frame['y'][0],
                    )
                )
                animation_sprite_sheet.append(
                    frame_image
                )
            result.update({
                animation: {
                    self.frames: animation_sprite_sheet,
                    self.time_duration: sprite_sheet_data[animation][self.time_duration]
                }
            })
        return result

    def play_animation(self, animation_name: str):
        self.animation_name: str = animation_name
