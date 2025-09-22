from pygame import Surface, SRCALPHA

from ..Core.Settings_Keeper import SettingsKeeper
from ..Render.Sprite import Sprite
"""
Contains code for Layers.
"""


class Layer:
    """
    Layer keep sprites and draw it on oneself.
    """
    def __init__(self, key: int):
        self._screen = SettingsKeeper().get_window()
        self._name: str | int = key
        self.sprite_collection: list = []
        self._layer_canvas: Surface | None = None

    def initialization(self):
        """
        Render sprites in layer canvas.
        """
        self._layer_canvas: Surface = Surface(
            (
                self._screen.get_width(),
                self._screen.get_height()
            ),
            SRCALPHA
        )

        for sprite in self.sprite_collection:
            sprite.blit_to(
                self._layer_canvas
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
        self._screen.blit(
            self._layer_canvas,
            (0, 0)
        )
