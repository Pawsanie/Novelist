from pygame import Surface

from .Assets_load import image_load
from .Render import text_canvas_render
"""
Contents code for user interface text canvas.
"""


class TextCanvas:
    """
    Generate text canvas surface and coordinates for render.

    :param background_surface: pygame.Surface of background.
    :type background_surface: Surface.
    """
    def __init__(self, *, background_surface: Surface):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface.
        """
        self.canvas_sprite: Surface = image_load(art_name='text_canvas',
                                                 file_format='png',
                                                 asset_type='UI')
        text_canvas: tuple[Surface, tuple[int, int]] = text_canvas_render(screen_surface=background_surface)
        self.text_canvas_surface: Surface = text_canvas[0]
        self.text_canvas_surface.blit(self.canvas_sprite, (0, 0))
        self.text_canvas_coordinates: tuple[int, int] = text_canvas[1]

    def generator(self):
        """
        Generate text canvas surface and coordinates for render.
        """
        return self.text_canvas_surface, self.text_canvas_coordinates

    def scale(self, *, background_surface):
        text_canvas: tuple[Surface, tuple[int, int]] = text_canvas_render(screen_surface=background_surface)
        self.text_canvas_surface: Surface = text_canvas[0]
        self.text_canvas_surface.blit(self.canvas_sprite, (0, 0))
        self.text_canvas_coordinates: tuple[int, int] = text_canvas[1]
