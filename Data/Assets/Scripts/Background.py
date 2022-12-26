from pygame import display, image, transform, Surface

from .Assets_load import image_load, json_load
from .Universal_computing import surface_size
"""
Contains code responsible for rendering scenes.
"""


def background_sprite_data(*, display_surface: Surface) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Make size of background and it coordinates.

    :param display_surface: display.set_mode surface.
    :return: Tuple with x and y sizes for background image.
             These sizes depends display size.
             And tuple with coordinates of rendering.
    """

    def scale_y(display_ratio) -> int:
        """
        Calculate background Y size.
        :return: int
        """
        size_x, size_y = display_size
        if size_x > size_y:
            while display_ratio != _16x9:
                if display_ratio > _16x9:
                    size_y += 1
                    display_ratio = int(background_size_x / size_y * 100)
                else:
                    size_y -= 1
                    display_ratio = int(background_size_x / size_y * 100)
        else:
            while display_ratio != _16x9:
                size_y -= 1
                display_ratio = int(background_size_x / size_y * 100)
        return size_y

    # Display resolution:
    # _5x4: int = int(5 / 4 * 100)  # Dinosaurs
    _16x9: int = int(16 / 9 * 100)  # Movie, game, text and art.
    # _21x9: int = int(21 / 9 * 100)  # Video montage and code.
    # _32x9: int = int(32 / 9 * 100)  # 27 inches or more.

    display_size: tuple[int, int] = surface_size(display_surface)
    ratio_of_sizes = int(display_size[0] / display_size[1] * 100)
    if ratio_of_sizes == _16x9:
        return display_size, (0, 0)
    else:
        background_size_x, background_size_y = display_size
        display_aspect_ratio = int(background_size_x / background_size_y * 100)
        # Scale Y size!:
        if background_size_x // 2 <= background_size_y:
            background_size_y = scale_y(display_aspect_ratio)
        # Scale X size!:
        else:
            while background_size_x // 2 > background_size_y:
                background_size_x -= 1
            background_size_y = scale_y(int(background_size_x / background_size_y * 100))
        # Result:
        background_surface_size = (background_size_x, background_size_y)
        render_coordinates = ((display_size[0] // 2) - (background_size_x // 2),
                              (display_size[1] // 2) - (background_size_y // 2))
        # display.set_mode(display_size)
        return background_surface_size, render_coordinates


class Background:
    """
    Load scene image by name and update the scene.
    Can scale scene size to display size.
    """
    def __init__(self, *, display_surface: display.set_mode, scene_image: image.load):
        """
        Set background image.
        Transform background to screen size.

        :param display_surface: Display surface object.
        :type display_surface: display.set_mode
        :param scene_image: Image for background.
        :type scene_image: pygame.image.load
        """
        self.display_surface: Surface = display_surface
        self.scene_image: Surface = scene_image
        self.scene_image_safe: Surface = scene_image  # hold standard image for rescale.
        self.background_coordinates: tuple[int, int] = (0, 0)

    def scale(self):
        scene_image: Surface = self.scene_image_safe
        new_background_surface_size: tuple = background_sprite_data(display_surface=self.display_surface)
        self.scene_image: Surface = transform.scale(scene_image, new_background_surface_size[0])
        self.background_coordinates: tuple[int, int] = new_background_surface_size[1]


def backgrounds_generator(*, display_surface: Surface) -> dict[str, Background]:
    """
    Generate dict with names of backgrounds and their sprites, for StageDirector.

    :param display_surface: pygame.Surface of pygame.display.set_mode.
    :return: Dict wth names of backgrounds and their sprites.
    """
    result: dict = {}
    backgrounds_list: dict = json_load(['Scripts',
                                       'Json_data',
                                        'backgrounds_sprites'])
    for location in backgrounds_list:
        sprite: Surface = image_load(art_name=backgrounds_list[location],
                                     file_format='jpg',
                                     asset_type='Backgrounds')
        result.update({location: Background(display_surface=display_surface,
                                            scene_image=sprite)})
    return result
