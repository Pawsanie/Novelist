from pygame import Surface

from .Assets_load import image_load
from .Render import text_canvas_render
"""
Contents code for user interface.
"""


def text_canvas_generator(*, background_surface: Surface):
    """
    Generate text canvas surface and coordinates for render.

    :param background_surface: pygame.Surface of background.
    :type background_surface: Surface.
    """
    canvas_sprite = image_load(art_name='text_canvas',
                               file_format='png',
                               asset_type='UI')
    text_canvas: tuple[Surface, tuple[int, int]] = text_canvas_render(screen_surface=background_surface)
    text_canvas_surface: Surface = text_canvas[0]
    text_canvas_surface.blit(canvas_sprite, (0, 0))
    text_canvas_coordinates: tuple[int, int] = text_canvas[1]
    return text_canvas_surface, text_canvas_coordinates


class Button:
    def __init__(self):
        ...

