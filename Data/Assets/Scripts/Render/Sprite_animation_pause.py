from pygame import time

from ..Universal_computing.Pattern_Singleton import SingletonPattern
"""
Responsible for the code of a pauses between sprite animations.
"""


class SpriteAnimationPause(SingletonPattern):
    """
    Decorator class which hold self time for animation pause animation tipe switch.
    """
    def __init__(self):
        self.frame_time: int = time.get_ticks()
        self.animation_skip: bool = False
        self.animation_skip_time: int = 4

        self.scene_name: str = ""

    def __call__(self, func):
        """
        Control animation frame to hold "0" frame between sprite animations.
        """
        def decorated(*args, **kwargs):
            # class method`s 'self.' for in class decorator:
            decorated_self = args[0]
            scene_name: str = self.get_scene_name()

            if any((
                self.scene_name != scene_name,
            )):
                self.scene_name = scene_name
                self.animation_skip = False
                return func(*args, **kwargs)

            if decorated_self.statick_frame_key is None:
                sprite_sheet_len: int = len(
                            decorated_self.sprite_sheet[decorated_self.animation_name]
                            [decorated_self.frames]
                        )

                if decorated_self.last_frame_number == sprite_sheet_len - 1:
                    self.animation_skip = True
                    decorated_self.last_frame_number = -1

                if self.animation_skip is True:
                    decorated_self.last_frame_number = -1
                    if time.get_ticks() / 1000 >= self.frame_time / 1000 + self.animation_skip_time:
                        self.animation_skip = False
                        self.frame_time = time.get_ticks()

            return func(*args, **kwargs)
        return decorated

    @staticmethod
    def get_scene_name() -> str:
        """
        Get scene name.
        """
        from ..Application_layer.Scene_Validator import SceneValidator
        return SceneValidator().scene
