from pygame import Surface
"""
Responsible for the code of a sprites used in rendering.
"""


class Sprite:
    """
    Spites uses in batch rendering.
    """
    def __init__(self, *, image: Surface, layer: int = 1, coordinates: tuple[int, int] = (0, 0),
                 name: str | None = None, sprite_sheet: list[Surface] | None = None):
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
        :param sprite_sheet: List with sprite sheet Surface frames.
                             None as default.
        :type sprite_sheet: list[Surface] | None
        """
        self.name: str | None = name
        self.image: Surface = image
        self.layer: int = layer
        self.coordinates: tuple[int, int] = coordinates

        self.sprite_sheet: list[Surface] | None = sprite_sheet
        self.current_frame: int = 0
        self.total_frames: int = self.get_sprite_sheet_frames_count()

    def blit(self, any_surface: Surface):
        """
        Draw sprite on surface.
        """
        self.image.blit(any_surface, self.coordinates)

    def get_sprite_sheet_frames_count(self) -> int:
        if self.sprite_sheet is None:
            return 0
        else:
            return len(self.sprite_sheet)

    def sprite_sheet_next_frame(self):
        """
        Switch frames in Sprite 2d animation if possible.
        """
        if self.sprite_sheet is None:
            return

        next_frame = self.current_frame + 1
        if next_frame > self.total_frames:
            self.current_frame = 0
        else:
            self.current_frame: int = next_frame
        self.image: Surface = self.sprite_sheet[self.current_frame]


def make_sprite_sheet(*, layer: int = 1, coordinates: tuple[int, int] = (0, 0),
                      name: str | None = None, sprite_sheet: list[Surface]) -> Sprite:
    """
    Generate Sprite from sprite sheet list.

    :param layer: Layer for sprite render.
                  1 as default.
    :type layer: int
    :param coordinates: Coordinates for sprite render.
                        (0, 0) as default.
    :type coordinates: tuple[int, int]
    :param name: Sprite name.
                 None as default.
    :type name: str | None
    :param sprite_sheet: List with sprite sheet Surface frames.
                         None as default.
    :type sprite_sheet: list[Surface] | None
    :return: Sprite
    """
    return Sprite(
        image=sprite_sheet[0],
        layer=layer,
        coordinates=coordinates,
        name=name,
        sprite_sheet=sprite_sheet
    )
