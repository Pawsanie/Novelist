from .Render import Render
from .Layer import Layer
from .Sprite import Sprite
"""
Contains code for batch rendering.
"""


class Batch:
    """
    An entity that allows you to draw all objects, inside yourself, at a time.
    """
    def __init__(self):
        self.sprite_collection: list = []
        self.sprite_to_render: dict = Render().layers_collection
        self.active: bool = True

    def append(self, sprite: Sprite):
        """
        Add new sprite in batch.
        """
        if sprite not in self.sprite_collection:
            self.sprite_collection.append(sprite)

    def initialization(self):
        """
        Prepares images in a batch for rendering.
        """
        if len(self.sprite_collection) > 0:
            for sprite in self.sprite_collection:
                sprite_layer: int = sprite.get_layer()

                if sprite_layer not in self.sprite_to_render:
                    layer_object: Layer = Layer(sprite_layer)
                    layer_object.append(sprite)
                    self.sprite_to_render.update(
                        {sprite_layer: layer_object}
                    )

                else:
                    if sprite not in self.sprite_to_render[sprite_layer].sprite_collection:
                        self.sprite_to_render[sprite_layer].append(sprite)

    def clear(self):
        """
        Clear batch.
        """
        self.sprite_collection.clear()
