from pygame import display, image, transform
"""
Contains code responsible for rendering scenes.
"""


class Background:
    """
    Load scene image by name and update the scene
    after the call "draw" method.
    """
    def __init__(self, *, screen_surface: display.set_mode, scene_image: image.load):
        """
        Set background image.
        Transform background to screen size.
        :param screen_surface: display.set_mode(...) surface.
        :param scene_image: pygame.image.load(...)
        """
        self.screen_surface = screen_surface
        self.display = display
        self.scene_image = scene_image

    def scale(self):
        scene_image = transform.scale(self.scene_image, (self.screen_surface.get_width(),
                                                         self.screen_surface.get_height()))
        return scene_image


class SceneText:
    """
    Ganerate text.
    """
