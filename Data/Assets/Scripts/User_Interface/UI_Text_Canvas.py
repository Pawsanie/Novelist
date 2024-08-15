from pygame import Surface, SRCALPHA, transform

from ..Universal_computing.Assets_load import AssetLoader
from ..Universal_computing.Surface_size import surface_size
from ..Game_objects.Background import Background
from ..Application_layer.Settings_Keeper import SettingsKeeper
from ..Universal_computing.Pattern_Singleton import SingletonPattern
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
        self.screen: Surface = SettingsKeeper().screen

        # Text canvas settings:
        self.canvas_safe: Surface = AssetLoader().image_load(
            art_name='text_canvas',
            asset_type='User_Interface'
        )
        self.text_canvas_surface: Surface = Surface((0, 0))
        self.text_canvas_coordinates: tuple[int, int] = (0, 0)
        self.status: bool = True

    def scale(self):
        """
        Generate text canvas surface with coordinates.
        """
        background_size: tuple[int, int] = self._background.get_size()
        background_width, background_height = background_size
        # Text canvas surface:
        self.text_canvas_surface: Surface = Surface(
            (background_width, background_height // 5), SRCALPHA
        )
        canvas_sprite: Surface = transform.scale(
            self.canvas_safe, surface_size(self.text_canvas_surface)
        )
        self.text_canvas_surface.blit(canvas_sprite, (0, 0))

        # Text canvas coordinates:
        self.text_canvas_coordinates: tuple[int, int] = (
            self._background.get_coordinates()[0],

            (self.screen.get_height() // 2)
            + (background_height // 2)
            - surface_size(self.text_canvas_surface)[1]
        )
