from pygame import display, image, transform, Surface

from .Assets_load import image_load, json_load
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
        self.scene_image = scene_image

    def scale(self):
        self.scene_image = transform.scale(self.scene_image, (self.screen_surface.get_width(),
                                           self.screen_surface.get_height()))


def backgrounds_generator(*, screen_surface: Surface) -> dict[str, Background]:
    """
    Generate dict with names of backgrounds and their sprites, for StageDirector.
    :param screen_surface: pygame.Surface of pygame.display.set_mode.
    :return: Dict wth names of backgrounds and their sprites.
    """
    result = {}
    backgrounds_list: dict = json_load(['Scripts',
                                       'Json_data',
                                        'backgrounds_sprites'])
    for location in backgrounds_list:
        sprite: Surface = image_load(art_name=backgrounds_list[location],
                                     file_format='jpg',
                                     asset_type='Backgrounds')
        result.update({location: Background(screen_surface=screen_surface,
                                            scene_image=sprite)})
    return result

