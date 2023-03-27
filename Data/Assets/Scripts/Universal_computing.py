from concurrent.futures import ThreadPoolExecutor

from pygame import Surface
"""
Contains universal computing for objects.
"""


class SingletonPattern:
    """
    Contain singleton design pattern code super class.
    """
    # Singleton instance flag:
    __singleton_instance: object or None = None
    # Singleton __init__ blocker callable function:
    __devnull_init: None = lambda self, *args, **kwargs: None

    def __new__(cls, *args, **kwargs) -> object:
        """
        Singleton design pattern class constructor part.
        Return Singleton instance.
        Blocking __init__ new instance dander method by callable function returning None.

        :result: Singleton instance.
        """
        if cls.__singleton_instance is None:
            try:
                cls.__singleton_instance = super(SingletonPattern, cls).__new__(cls)
            except TypeError:
                cls.__singleton_instance = super(SingletonPattern, cls).__new__(cls, *args, **kwargs)

        # Check default '__init__' value... is callable result None?
        elif cls.__dict__.get('__init__', None) is not cls.__devnull_init:
            cls.__init__: None = cls.__devnull_init

        return cls.__singleton_instance


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
