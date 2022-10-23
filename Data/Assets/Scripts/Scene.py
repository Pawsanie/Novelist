from pygame import display, image, transform
"""
Contains code responsible for rendering scenes.
"""


class Background:
    """
    Load scene image by name and update the scene
    after the call "draw" method.
    """
    def __init__(self, *, surface: display.set_mode, scene_image: image.load):
        """
        Set background image.
        Transform background to screen size.
        :param surface: display.set_mode(...) surface.
        :param scene_image: pygame.image.load(...)
        """
        scene_image = transform.scale(scene_image, (surface.get_width(), surface.get_height()))
        surface.blit(scene_image, (0, 0))


class SceneText:
    """
    Ganerate text.
    """
