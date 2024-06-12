from pygame import transform, Surface

from ..Universal_computing.Assets_load import AssetLoader
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Application_layer.Settings_Keeper import SettingsKeeper
"""
Contains code responsible for rendering scenes.
"""


class Background:
    """
    Load scene image by name and update the scene.
    Can scale scene size to display size.
    """
    def __init__(self, *, scene_image: Surface):
        """
        Set background image.
        :param scene_image: Image for background.
        :type scene_image: Surface
        """
        # Program layers settings:
        self._settings_keeper: SettingsKeeper = SettingsKeeper()

        # Background settings:
        self._display_surface: Surface = self._settings_keeper.get_windows_settings()
        self.scene_image: Surface = scene_image
        self.background_coordinates: tuple[int, int] = (0, 0)

        # hold standard image for rescale:
        self.scene_image_safe: Surface = scene_image

    def scale(self):
        """
        Sets the size and coordinates of the background.
        Call from StageDirector.
        """
        # Calculate scale coefficient:
        coefficient: int | float = min(
            self._display_surface.get_width() / self.scene_image_safe.get_width(),
            self._display_surface.get_height() / self.scene_image_safe.get_height()
        )
        # Set background sprite size:
        scene_image: Surface = self.scene_image_safe
        self.scene_image: Surface = transform.scale(
            scene_image,
            (
                int(self.scene_image_safe.get_width() * coefficient),
                int(self.scene_image_safe.get_height() * coefficient)
            )
        )
        # Calculate coordinates:
        render_coordinates: tuple[int, int] = (
            (self._display_surface.get_width() - self.scene_image.get_width()) // 2,
            (self._display_surface.get_height() - self.scene_image.get_height()) // 2
        )
        # Set background sprite coordinates:
        self.background_coordinates: tuple[int, int] = render_coordinates


def backgrounds_generator() -> dict[str, Background]:
    """
    Generate dict with names of backgrounds and their sprites, for StageDirector.
    :return: Dict wth names of backgrounds and their sprites.
    """
    asset_loader: AssetLoader = AssetLoader()
    result: dict = {}
    backgrounds_list: dict = asset_loader.json_load(
        ['Scripts', 'Json_data', 'backgrounds_sprites']
    )
    for location in backgrounds_list:
        sprite: Surface = asset_loader.image_load(
            art_name=backgrounds_list[location],
            asset_type='Backgrounds'
        )
        result.update(
            {
                location: Background(
                    scene_image=sprite
                )
            }
        )
    return result


class BackgroundProxy(Background, SingletonPattern):
    """
    Proxy Pattern object:
    Blank for images surface scale.
    """
    def __init__(self):
        super().__init__(
            scene_image=Surface((100, 100))
        )

    def get_data(self) -> tuple[Surface, tuple[int, int]]:
        """
        Calculation background size and return it Surface object.
        Calculation background coordinates and return it too.
        Call from StageDirector.
        :return: Background surface and coordinates.
        """
        self.scale()
        return self.scene_image, self.background_coordinates

    def set_new_image(self, *, new_image: Surface):
        """
        Set new image to safe place for scale.
        Call from StageDirector.
        :param new_image: Surface with image.
        :type new_image: Surface
        """
        self.scene_image_safe: Surface = new_image
        self.scene_image: Surface = new_image
