from pygame import Surface

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Application_layer.Settings_Keeper import SettingsKeeper
from ..Render.Sprite import Sprite
from ..Universal_computing.Assets_load import AssetLoader
from ..Render.Texture_Master import TexturesMaster
"""
Contains code responsible for rendering scenes.
"""


class Background(SingletonPattern):
    """
    Load scene image by name and update the scene.
    Can scale scene size to display size.
    """
    def __init__(self):
        # Program layers settings:
        self._settings_keeper: SettingsKeeper = SettingsKeeper()
        self._asset_loader: AssetLoader = AssetLoader()
        self._texture_master: TexturesMaster = TexturesMaster()
        self._display_surface: Surface = self._settings_keeper.get_window()

        # Background attributes:
        self._background_name: str | None = None
        self._background_coordinates: tuple[int, int] = (0, 0)
        self._background_size: tuple[int, int] = (0, 0)
        self._sprite: Sprite | None = None
        self._last_screen_size: tuple[int, int] = (0, 0)

        # Background settings:
        self._all_backgrounds_sprites_settings: dict = self._asset_loader.json_load(
            ["Scripts", "Json_data", "backgrounds_sprites"]
        )
        for background_name in self._all_backgrounds_sprites_settings:
            self._all_backgrounds_sprites_settings[background_name].update(
                {
                    "sprite_sheet_configuration": self._texture_master.get_texture_configs_data(
                        texture_type="Backgrounds",
                        texture_name=self._all_backgrounds_sprites_settings[background_name]["texture"]
                    ),
                    "texture_type": "Backgrounds"
                }
            )

    def set_background(self, new_background_name: str):
        """
        Set new animated ot statick Sprite name for TexturesMaster.
        :param new_background_name: Name of background for search texture in TexturesMaster.
        """
        if self._background_name != new_background_name:
            self._background_name: str = new_background_name
            self._sprite: Sprite = Sprite(
                coordinates=self._background_coordinates,
                name=self._background_name,
                texture_mame=self._all_backgrounds_sprites_settings[self._background_name]["texture"],
                sprite_sheet_data=self._all_backgrounds_sprites_settings[
                    self._background_name
                ]["sprite_sheet_configuration"] | {
                    "texture_type": "Backgrounds"
                },
                sprite_size=self._background_size
            )

    def devnull(self):
        self._background_name: None = None

    def get_sprite(self) -> Sprite:
        return self._sprite

    def get_coordinates(self) -> tuple[int, int]:
        return self._background_coordinates

    def get_size(self) -> tuple[int, int]:
        return self._background_size

    def scale(self):
        """
        Sets the size and coordinates of the background.
        Call from StageDirector.
        """
        background_texture_size: tuple[int, int] = self._texture_master.get_texture_size(
            texture_name=self._all_backgrounds_sprites_settings[self._background_name]["texture"],
            texture_type="Backgrounds",
            animation_name=self._sprite.get_animation_name(),
            frame=self._sprite.get_frame_number()
        )
        if self._background_size == background_texture_size \
                and self._last_screen_size == (
                    self._display_surface.get_width(),
                    self._display_surface.get_height()
                ):
            return
        background_texture_size_width, background_texture_size_height = background_texture_size
        self._last_screen_size: tuple[int, int] = (
                    self._display_surface.get_width(),
                    self._display_surface.get_height()
        )

        # Calculate scale coefficient:
        coefficient: int | float = min(
            self._last_screen_size[0] / background_texture_size_width,
            self._last_screen_size[1] / background_texture_size_height
        )

        # Set background sprite size:
        self._background_size: tuple[int, int] = (
                int(background_texture_size_width * coefficient),
                int(background_texture_size_height * coefficient)
            )
        self._sprite.scale(self._background_size)

        self._texture_master.set_new_scale_frame(
            texture_name=self._all_backgrounds_sprites_settings[self._background_name]['texture'],
            texture_type="Backgrounds",
            animation_name=self._sprite.get_animation_name(),
            frame=self._sprite.get_frame_number(),
            image_size=self._background_size
        )

        # Calculate coordinates:
        self._background_coordinates: tuple[int, int] = (
            (self._last_screen_size[0] - self._background_size[0]) // 2,
            (self._last_screen_size[1] - self._background_size[1]) // 2
        )
        self._sprite.set_coordinates(self._background_coordinates)
