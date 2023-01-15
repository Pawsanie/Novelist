from concurrent.futures import ThreadPoolExecutor

from pygame import Surface
"""
Contains universal computing for objects.
"""


def surface_size(interested_surface: Surface) -> [int, int]:
    """
    Calculation surface size.

    :param interested_surface: pygame.Surface object.
    :return: Surface size with 2 init`s.
    """
    character_sprite_size_x: int = interested_surface.get_width()
    character_sprite_size_y: int = interested_surface.get_height()
    return character_sprite_size_x, character_sprite_size_y


def coroutine_decorator(func):
    """
    Decorator with asynchronous results.
    """
    def coroutine(*args, **kwargs):
        with ThreadPoolExecutor(max_workers=1) as executor:
            task = func(*args, **kwargs)
            try:
                callback = executor.submit(task)
                try:
                    return callback.result()
                except Exception as error:
                    ...
            except Exception as error:
                ...
    return coroutine
