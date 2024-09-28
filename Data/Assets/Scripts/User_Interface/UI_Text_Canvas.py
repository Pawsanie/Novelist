from pygame import Surface

from ..Game_objects.Background import Background
from ..Application_layer.Settings_Keeper import SettingsKeeper
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Render.Sprite import Sprite
"""
Contents code for user interface text canvas.
"""


class TextCanvas(SingletonPattern):
    """
    Generate text canvas surface and coordinates for render.
    """
    def __init__(self):
        # Program layers settings:
        self._background: Background = Background()
        self._screen: Surface = SettingsKeeper().get_window()

        # Text canvas settings:
        self._sprite_size: tuple[int, int] = (0, 0)
        self._text_canvas_coordinates: tuple[int, int] = (0, 0)
        self.status: bool = True

    def scale(self):
        """
        Generate text canvas surface with coordinates.
        """
        background_size: tuple[int, int] = self._background.get_size()
        background_width, background_height = background_size

        # Text canvas size:
        self._sprite_size: tuple[int, int] = (
            background_width,
            background_height // 5
        )

        # Text canvas coordinates:
        self._text_canvas_coordinates: tuple[int, int] = (
            self._background.get_coordinates()[0],

            (self._screen.get_height() // 2)
            + (background_height // 2)
            - (background_height // 5)
        )

    def get_size(self) -> tuple[int, int]:
        """
        Used in DialoguesWords.
        """
        return self._sprite_size

    def get_coordinates(self) -> tuple[int, int]:
        """
        Used in DialoguesWords.
        """
        return self._text_canvas_coordinates

    def get_sprite(self) -> Sprite:
        """
        Used in StageDirector.
        """
        return Sprite(
            name="Text_canvas",
            layer=3,
            coordinates=self._text_canvas_coordinates,
            texture_mame="text_canvas",
            sprite_sheet_data={
                "texture_type": "User_Interface",
                "sprite_sheet": False,
                "statick_frames": {
                    "text_canvas": {}
                }

            },
            sprite_size=self._sprite_size
        )
