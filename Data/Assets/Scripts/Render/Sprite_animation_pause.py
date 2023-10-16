from pygame import time

from ..Universal_computing.Pattern_Singleton import SingletonPattern
"""

"""


class SpriteAnimationPause(SingletonPattern):
    """
    Decorator class which hold self time for animation pause animation tipe switch.
    """
    def __init__(self):
        self.frame_time: int = time.get_ticks()
        self.animation_skip: bool = False
        self.animation_skip_time: int = 4
        self.sprite_name: str | None = None
        self.sprite_animation: str | None = None

    def __call__(self, func):
        def decorated(*args, **kwargs):
            # class method`s 'self.' for in class decorator:
            decorated_self = args[0]

            if self.sprite_name != decorated_self.name \
                    or self.sprite_animation != decorated_self.animation_name:
                self.sprite_name = decorated_self.name
                self.sprite_animation = decorated_self.animation_name
                self.animation_skip = False
                return func(*args, **kwargs)

            if decorated_self.statick_frame_key is None:
                sprite_sheet_len: int = len(
                            decorated_self.sprite_sheet[decorated_self.animation_name][decorated_self.frames]
                        )

                if decorated_self.last_frame_number == sprite_sheet_len - 1:
                    self.animation_skip = True
                    decorated_self.last_frame_number = - 1

                if self.animation_skip is True:
                    decorated_self.last_frame_number = - 1
                    if time.get_ticks() / 1000 >= self.frame_time / 1000 + self.animation_skip_time:
                        self.animation_skip = False
                        self.frame_time = time.get_ticks()

            return func(*args, **kwargs)
        return decorated
