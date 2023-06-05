from pygame import Surface, SRCALPHA, transform

from ..Application_layer.Assets_load import image_load
from ..Universal_computing import surface_size
from ..Game_objects.Background import BackgroundMock
"""
Contents code for user interface text canvas.
"""


class TextCanvas:
    """
    Generate text canvas surface and coordinates for render.
    """
    def __init__(self):
        self.canvas_sprite: Surface = image_load(
            art_name='text_canvas',
            file_format='png',
            asset_type='User_Interface'
        )
        self.background_surface: BackgroundMock = BackgroundMock()
        self.text_canvas_surface: Surface = Surface((0, 0))
        self.text_canvas_coordinates: tuple[int, int] = (0, 0)
        self.text_canvas_status: bool = True
        # Calculate:
        self.scale()

    def get(self):
        """
        Generate text canvas surface and coordinates for render.
        """
        if self.text_canvas_status is True:
            return self.text_canvas_surface, self.text_canvas_coordinates
        if self.text_canvas_status is False:
            return Surface((0, 0)), (0, 0)

    def scale(self):
        self.text_canvas_generator()
        canvas_sprite: Surface = transform.scale(self.canvas_sprite, surface_size(self.text_canvas_surface))
        self.text_canvas_surface.blit(canvas_sprite, (0, 0))

    def text_canvas_generator(self):
        """
        Generate text canvas surface with coordinates.

        :return: pygame.Surface with text_canvas coordinates.
        """
        # Render text canvas:
        screen_size: Surface = self.background_surface.get_data()[0]
        self.text_canvas_surface: Surface = Surface(
            (screen_size.get_width(), screen_size.get_height() // 5), SRCALPHA
        )
        # text_canvas.set_alpha(128)
        # Text canvas coordinates:
        self.text_canvas_coordinates: tuple[int, int] = (
            0,
            screen_size.get_height() - surface_size(self.text_canvas_surface)[1]
        )
