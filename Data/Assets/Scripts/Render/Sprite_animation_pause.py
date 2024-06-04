from random import randint

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
        self.scene_name: str = ""
        self.sprite_collection: dict = {}

    def __call__(self, func):
        """
        Control animation frame to hold "0" frame between sprite animations.
        """
        def decorated(*args, **kwargs):
            # class method`s 'self.' for in class decorator:
            decorated_self = args[0]
            scene_name: str = self.get_scene_name()

            if self.scene_name != scene_name:
                self.scene_name = scene_name
                self.sprite_collection.clear()
                return func(*args, **kwargs)

            if decorated_self.statick_frame_key is None:
                sprite_sheet_len: int = len(
                            decorated_self.sprite_sheet
                            [decorated_self.animation_name]
                            [decorated_self.frames]
                        )
                if decorated_self.name is not None:
                    sprite_name: str = decorated_self.name
                else:
                    sprite_name: str = str(decorated_self)
                if any((
                        decorated_self.name,
                        str(decorated_self)
                )) not in self.sprite_collection.keys():
                    self.update_scene_sprites(
                        sprite=decorated_self,
                        sprite_name=sprite_name
                    )
                sprite: dict = self.sprite_collection[sprite_name]
                if sprite["sprite"].last_frame_number == sprite_sheet_len - 1:
                    sprite["animation_skip"]: bool = True
                    sprite["sprite"].last_frame_number = -1

                if sprite["animation_skip"] is True:
                    sprite["sprite"].last_frame_number = -1
                    if time.get_ticks() / 1000 >= sprite["frame_time"] / 1000 + sprite["pause_time"]:
                        sprite["animation_skip"]: bool = False
                        sprite["frame_time"]: int = time.get_ticks()

            return func(*args, **kwargs)
        return decorated

    @staticmethod
    def get_scene_name() -> str:
        """
        Get scene name.
        """
        from ..GamePlay.Scene_Validator import SceneValidator
        return SceneValidator().scene

    def update_scene_sprites(self, *, sprite, sprite_name: str):
        """
        Update scene animation sprite`s data.

        :param sprite: Sprite for "sprite_collection".
        :type sprite: Sprite
        :param sprite_name: Name of Sprite.
        :type sprite_name: str
        """
        self.sprite_collection.setdefault(
            sprite_name, {
                "sprite": sprite,
                "animation_skip": False,
                "pause_time": randint(2, 5),
                "frame_time": time.get_ticks()
                }
        )
