from pygame import Surface, SRCALPHA, transform

from ..Assets_load import image_load
from ..Universal_computing import surface_size
"""
Contents code for user interface text canvas.
"""


class TextCanvas:
    """
    Generate text canvas surface and coordinates for render.
    """
    def __init__(self, *, background_surface: Surface):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface.
        """
        self.canvas_sprite: Surface = image_load(
            art_name='text_canvas',
            file_format='png',
            asset_type='User_Interface'
        )
        self.text_canvas_surface: Surface = Surface((0, 0))
        self.text_canvas_coordinates: tuple[int, int] = (0, 0)
        self.text_canvas_status: bool = True
        # Calculate:
        self.scale(background_surface=background_surface)

    def get(self):
        """
        Generate text canvas surface and coordinates for render.
        """
        if self.text_canvas_status is True:
            return self.text_canvas_surface, self.text_canvas_coordinates
        if self.text_canvas_status is False:
            return Surface((0, 0)), (0, 0)

    def scale(self, *, background_surface):
        self.text_canvas_generator(background_surface=background_surface)
        canvas_sprite: Surface = transform.scale(self.canvas_sprite, surface_size(self.text_canvas_surface))
        self.text_canvas_surface.blit(canvas_sprite, (0, 0))

    def text_canvas_generator(self, *, background_surface: Surface):
        """
        Generate text canvas surface with coordinates.

        :param background_surface: pygame.Surface with background.
        :return: pygame.Surface with text_canvas coordinates.
        """
        # Render text canvas:
        screen_size: tuple[int, int] = surface_size(background_surface)
        self.text_canvas_surface: Surface = Surface((screen_size[0], screen_size[1] // 5), SRCALPHA)
        # text_canvas.set_alpha(128)
        # Text canvas coordinates:
        self.text_canvas_coordinates: tuple[int, int] = (
            0,
            screen_size[1] - surface_size(self.text_canvas_surface)[1]
        )
