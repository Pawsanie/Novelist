from pygame import Surface
"""
Responsible for the code of a sprites used in rendering.
"""


class Sprite:
    """
    Spites uses in batch rendering.
    """
    def __init__(self, *, image: Surface, layer: int = 1, coordinates: tuple[int, int] = (0, 0)):
        """
        :param image: Pygame.Surface for sprite render.
        :type image: Surface
        :param layer: Layer for sprite render.
                      1 as default.
        :type layer: int
        :param coordinates: Coordinates for sprite render.
        :type coordinates: tuple[int, int]
        """
        self.image: Surface = image
        self.layer: int = layer
        self.coordinates: tuple[int, int] = coordinates

    def blit(self, any_surface: Surface):
        """
        Draw sprite on surface.
        """
        self.image.blit(any_surface, self.coordinates)
