from pygame import Surface

from ..Application_layer.Settings_Keeper import SettingsKeeper
from ..Render.Sprite import Sprite
"""
Contains code for Layers.
"""


class Layer:
    """
    Layer keep sprites and draw it on oneself.
    """
    def __init__(self, key: int):
        self.screen = SettingsKeeper().screen
        self.name: str | int = key
        self.sprite_collection: list = []
        self.layer_canvas: Surface | None = None

    def initialization(self):
        """
        Render sprites in layer canvas.
        """
        self.layer_canvas: Surface = Surface(
            (self.screen.get_width(), self.screen.get_height())
        )

        for sprite in self.sprite_collection:
            self.layer_canvas.blit(
                sprite.image, sprite.coordinates
            )

    def append(self, sprite: Sprite):
        """
        Add new sprite in to layer.
        """
        self.sprite_collection.append(sprite)

    def clear(self):
        """
        Clear layer from sprites.
        """
        self.sprite_collection.clear()

    def draw(self):
        """
        Render layer on display screen
        """
        self.initialization()
        self.screen.blit(self.layer_canvas, (0, 0))
