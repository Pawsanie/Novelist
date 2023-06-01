from pygame import Surface

from ..Settings_Keeper import SettingsKeeper
"""
Contains code for batch rendering.
"""


class Batch:
    """
    An entity that allows you to draw all objects, inside yourself, at a time.
    """
    def __init__(self):
        self.sprite_collection: list = []
        self.sprite_to_render: dict = {}
        self.screen: Surface = SettingsKeeper().screen

    def append(self, sprite: Surface):
        """
        Add new sprite in batch.
        """
        self.sprite_collection.append(sprite)

    def initialization(self):
        """
        Prepares images in a batch for rendering.
        """
        if len(self.sprite_collection) > 0:
            for sprite in self.sprite_collection:
                sprite_layer: int = sprite.layer

                if sprite_layer not in self.sprite_to_render:
                    self.sprite_to_render.update(
                        {sprite_layer: [sprite]}
                    )

                else:
                    self.sprite_to_render[sprite_layer].append(sprite)

        self.sprite_collection.clear()

    def draw(self):
        """
        Draw all layers in batch.
        """
        self.initialization()
        if len(self.sprite_to_render) > 0:
            sorted_layers: list = sorted(
                self.sprite_to_render.items()
            )
            self.sprite_to_render: dict = {
                key: value for key, value in sorted_layers
            }

            for layer in self.sprite_to_render:
                for sprite in self.sprite_to_render[layer]:
                    self.screen.blit(
                        source=sprite,
                        dest=sprite.coordinates
                    )

        self.sprite_to_render.clear()
