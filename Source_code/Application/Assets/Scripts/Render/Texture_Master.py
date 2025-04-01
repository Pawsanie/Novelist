from typing import Callable

from pygame import Surface, SRCALPHA, transform

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Universal_computing.Assets_load import AssetLoader
"""
Contains code responsible for collecting and storing textures.
"""


class TexturesMaster(SingletonPattern):
    """
    Storing textures data for image calculation.
    """
    def __init__(self):
        # Program layers settings:
        self._asset_loader: AssetLoader = AssetLoader()

        # TexturesMaster attributes:
        self._texture_sources: dict = {
            "Characters": "characters_sprites",
            "Backgrounds": "backgrounds_sprites"
        }
        self._texture_configs_catalog: dict = {}
        self._raw_images_catalog: dict = {}
        self._raw_textures_catalog: dict = {
            "User_Interface": {}
        }
        self._texture_catalog: dict = {}
        self._image_memory_pool_bytes: int = 262144000  # 250mb as default
        self._temporary_textures: dict = {}

        # TexturesMaster settings:
        self.__initialisation()

    def get_texture_configs_data(self, *, texture_name: str, texture_type: str) -> dict:
        """
        Get texture configuration data.
        Use in Sprites.
        :param texture_name: Name of texture which data you want to get.
        :param texture_type: Type of texture which data you want to get.
        """
        return self._texture_configs_catalog[texture_type][texture_name]

    def __initialisation(self):
        """
        Collect raw texture data and create sprite sheets.
        """
        # Collect raw textures:
        self._collect_texture_configurations()
        self._collect_raw_images()
        self._create_raw_sprite_sheet_frames()
        self._raw_images_catalog.clear()

        # Create technical textures:
        self._create_void_background()
        self._create_screen_mask_for_background_in_menu()

        # Collect raw UI textures:
        self._collect_raw_ui_images()

        # Create texture catalog:
        deep_copy_surfaces: Callable = lambda dict_to_copy: {
            key: (
                value.copy() if isinstance(value, Surface)
                else deep_copy_surfaces(value) if isinstance(value, dict)
                else value
            )
            for key, value in dict_to_copy.items()
        }
        self._texture_catalog: dict = deep_copy_surfaces(self._raw_textures_catalog)

    def _collect_raw_ui_images(self):
        """
        Collect raw User Interface texture image surfaces for _raw_textures_catalog.
        """
        raw_ui_data: dict = self._asset_loader.json_load(
            [
                "Scripts", "Json_data", "User_Interface", "ui_sprites"
            ]
        )
        for catalog_name in raw_ui_data:
            for texture_image_name in raw_ui_data[catalog_name]:
                raw_image_surface: Surface = self._asset_loader.image_load(
                    art_name=texture_image_name,
                    asset_type="User_Interface",
                    file_catalog=catalog_name
                )
                self._raw_textures_catalog["User_Interface"].update(
                    {
                        texture_image_name: {
                            "statick_frames": {
                                texture_image_name: raw_image_surface
                            }
                        }
                    }
                )

    def load_static_texture_from_path(
            self, *,
            texture_path: str,
            texture_type: str,
            asset_type: str
    ):
        """
        Load texture without configuration.
        Use in BaseButton.
        :param texture_path: Path to image file.
        :param texture_type: Characters|Backgrounds|User_Interface
        :param asset_type: As example - "Characters":
                {
                    "file_format": "png",
                    "alpha_chanel": True
                },
            "User_Interface": {
                    "file_format": "png",
                    "alpha_chanel": True
                },
            "Backgrounds": {
                    "file_format": "jpg",
                    "alpha_chanel": False
                },
            "Saves": {
                "file_format": "png",
                "alpha_chanel": False
                }
        """
        self._raw_textures_catalog[texture_type].update(
            {
                texture_path: {
                    "statick_frames": {
                        texture_path: self._asset_loader.image_load(
                            art_name=texture_path,
                            asset_type=asset_type,
                            art_name_is_path=True
                        )
                    }
                }
            }
        )

        if texture_type not in self._texture_catalog:
            self._texture_catalog.update(
                {
                    texture_type: {}
                }
            )

        if texture_path not in self._texture_catalog[texture_type]:
            self._texture_catalog[texture_type].update(
                {
                    texture_path: {}
                }
            )

        self._texture_catalog[texture_type][texture_path].update(
            {
                "statick_frames": {
                    texture_path: self._raw_textures_catalog[
                        texture_type
                    ][
                        texture_path
                    ][
                        "statick_frames"
                    ][
                        texture_path
                    ].copy()
                }
            }
        )

    def _create_void_background(self):
        """
        generate Void for screen cleaning.
        """
        void_surface: Surface = Surface(
            (720, 480)
        )
        void_surface.fill(
            (0, 0, 0)
        )
        self._raw_textures_catalog["Backgrounds"].update(
            {
                None: {
                    "statick_frames": {
                        "void_texture": void_surface
                    }
                }
            }
        )

    def _create_screen_mask_for_background_in_menu(self):
        """
        Generate filter for backgrounds when the in-game menu is called.
        """
        screen_mask: Surface = Surface(
            (720, 480),
            SRCALPHA
        )
        screen_mask.fill(
            (0, 0, 0)
        )
        screen_mask.set_alpha(210)
        self._raw_textures_catalog["Backgrounds"].update(
            {
                "ui#screen_mask": {
                    "statick_frames": {
                        "screen_mask": screen_mask
                    }
                }
            }
        )

    def get_texture(
            self, *,
            texture_type: str,
            texture_name: str,
            animation_name: str,
            frame: int | str
    ) -> Surface:
        """
        Get texture Surface from TexturesMaster storage.
        :param texture_type: Characters|Backgrounds|User_Interface
        :param texture_name: Name of texture.
        :param animation_name: Animation name of sprite sheet.
        :param frame: Animation frame number, or frame name for statick images.
        """
        try:
            return self._temporary_textures[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ]
        except KeyError:
            return self._texture_catalog[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ]

    def _collect_texture_configurations(self):
        """
        Get texture configurations for Sprites creation.
        """
        for texture_source_folder, game_play_texture_config_file in self._texture_sources.items():
            if texture_source_folder not in self._texture_configs_catalog:
                self._texture_configs_catalog.update(
                    {
                        texture_source_folder: {}
                    }
                )

            # Get texture configs names:
            sprite_configs_names_collection: list = []
            sprites_raw_data: dict = self._asset_loader.json_load(
                [
                    "Scripts", "Json_data", game_play_texture_config_file,
                ]
            )

            for sprite_type_name_key, sprite_data_value in sprites_raw_data.items():
                sprite_config_name: str = sprite_data_value["texture"]
                if sprite_config_name not in sprite_configs_names_collection:
                    sprite_configs_names_collection.append(sprite_config_name)

            # Get texture configs data:
            for config_name in sprite_configs_names_collection:
                config_data: dict = self._asset_loader.json_load(
                    [
                        "Scripts", "Json_data", "Texture_data", texture_source_folder, config_name
                    ]
                )
                self._texture_configs_catalog[texture_source_folder].update(
                    {
                        config_name: config_data
                    }
                )

    def _collect_raw_images(self):
        """
        Collect row texture images for scale.
        """
        for texture_type, texture_collection in self._texture_configs_catalog.items():
            if texture_type not in self._raw_images_catalog:
                self._raw_images_catalog.update(
                    {
                        texture_type: {}
                    }
                )

            for texture_name in texture_collection:
                texture_image: Surface = self._asset_loader.image_load(
                    art_name=texture_name,
                    asset_type=texture_type,
                )
                self._raw_images_catalog[texture_type].update(
                    {
                        texture_name: texture_image
                    }
                )

    def _create_raw_sprite_sheet_frames(self):
        """
        Create raw sprite sheet.
        Frames of this sprite sheet are not scale from raw state.
        They will be scale when loading a game map or video clip into a separate collection.
        """
        def __get_frames(*, texture_type_name: str, frames: dict) -> dict:
            """
            Get sprite sheet frame from texture image.
            :param texture_type_name: Asset type for raw image getting.
            :param frames: Dictionary with frame coordinates data.
            """
            result: dict = {}
            for frame in frames:
                top_left_corner: dict = frames[frame]["top_left_corner"]
                bottom_right_corner: dict = frames[frame]["bottom_right_corner"]

                bounding_box: tuple[int, int] = (
                    bottom_right_corner["x"] - top_left_corner["x"],
                    bottom_right_corner["y"] - top_left_corner["y"]
                )

                frame_surface: Surface = Surface(
                    bounding_box,
                    SRCALPHA
                )

                frame_blit_coordinates: tuple[int, int] = (
                    - top_left_corner["x"],
                    - top_left_corner["y"]
                )

                texture: Surface = self._raw_images_catalog[texture_type_name][texture_name]
                frame_surface.blit(
                    texture, frame_blit_coordinates
                )

                result.update(
                    {
                        frame: frame_surface
                    }
                )
            return result

        # Create sprites:
        for texture_type, texture_catalog in self._texture_configs_catalog.items():
            if texture_type not in self._raw_textures_catalog:
                self._raw_textures_catalog.update(
                    {
                        texture_type: {}
                    }
                )

            for texture_name, texture_data in texture_catalog.items():
                self._raw_textures_catalog[texture_type].update(
                    {
                        texture_name: {}
                    }
                )

                # Animation sprites:
                if texture_data["sprite_sheet"]:
                    for animation in texture_data["animations"]:
                        self._raw_textures_catalog[texture_type][texture_name].update(
                            {
                                animation: __get_frames(
                                    texture_type_name=texture_type,
                                    frames=texture_data["animations"][animation]["frames"]
                                )
                            }
                        )

                # Statick sprites:
                else:
                    self._raw_textures_catalog[texture_type][texture_name].update(
                        {
                            "statick_frames": __get_frames(
                                texture_type_name=texture_type,
                                frames=texture_data["statick_frames"]
                            )
                        }
                    )

    def set_new_scale_frame(
            self, *,
            texture_name: str,
            texture_type: str,
            frame: int | str,
            image_size: tuple[int, int],
            animation_name: str = "statick_frames"
    ):
        """
        Cash new frame size.
        :param texture_name: Name of texture image frame.
        :param texture_type: Characters|Backgrounds|User_Interface
        :param frame: Number of frame or statick frame name.
        :param image_size: Frame image surface.
        :param animation_name: Name of animation for non statick textures.
        """
        try:
            image_surface: Surface = transform.scale(

                self._temporary_textures[
                    texture_type
                ][
                    texture_name
                ][
                    animation_name
                ][
                    str(frame)
                ],

                image_size
            )
            self._temporary_textures[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ]: Surface = image_surface

        except KeyError:
            self._texture_catalog[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ]: Surface = \
                transform.scale(
                self._raw_textures_catalog[
                    texture_type
                ][
                    texture_name
                ][
                    animation_name
                ][
                    str(frame)
                ].copy(),
                image_size
            )

    def set_temporary_texture(
            self, *,
            texture_type: str,
            texture_name: str,
            surface: Surface,
            animation_name: str,
            frame: int | str
    ):
        """
        Set temporary texture.
        These are specific textures generated using on-the-fly calculations.
        Can be used for UI buttons as exemple.
        :param texture_name: Name of texture image frame.
        :param texture_type: Type of texture image.
        :param animation_name: Name of animation for non statick textures.
        :param frame: Number of frame or statick frame name.
        :param surface: Pygame.Surface object.
        """
        if texture_type not in self._temporary_textures:
            self._temporary_textures.update(
                {
                    texture_type: {}
                }
            )

        if texture_name not in self._temporary_textures[texture_type]:
            self._temporary_textures[texture_type].update(
                {
                    texture_name: {}
                }
            )

        if animation_name not in self._temporary_textures[texture_type][texture_name]:
            self._temporary_textures[texture_type][texture_name].update(
                {
                    animation_name: {}
                }
            )

        if str(frame) not in self._temporary_textures[
            texture_type
        ][
            texture_name
        ][
            animation_name
        ]:
            self._temporary_textures[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ].update(
                {
                    str(frame): surface
                }
            )

        else:
            self._temporary_textures[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ]: Surface = surface

    def devnull_temporary_texture(
            self, *, texture_type: str,
            texture_name: str,
            animation_name: str,
            frame: int | str
    ):
        """
        Devnull temporary texture.
        These are specific textures generated using on-the-fly calculations.
        Can be used for UI buttons as exemple.
        :param texture_name: Name of texture image frame.
        :param texture_type: Type of texture image.
        :param frame: Number of frame or statick frame name.
        :param animation_name: Name of animation for non statick textures.
        """
        try:
            del self._temporary_textures[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ]
        except KeyError:
            pass

    def get_temporary_texture(
            self, texture_type: str,
            texture_name: str,
            animation_name: str,
            frame: int | str
    ) -> Surface:
        """
        Get cyclically recache texture.
        Can be used for UI buttons.
        :param texture_name: Name of texture image frame.
        :param texture_type: Type of texture image.
        :param frame: Number of frame or statick frame name.
        :param animation_name: Name of animation for non statick textures.
        """
        return self._temporary_textures[
            texture_type
        ][
            texture_name
        ][
            animation_name
        ][
            str(frame)
        ]

    def get_texture_size(
            self, *,
            texture_type: str,
            texture_name: str,
            animation_name: str = "statick_frames",
            frame: int | str = 0
    ) -> tuple[int, int]:
        """
        Get texture size from catalog.
        :param texture_name: Name of texture image frame.
        :param texture_type: Characters|Backgrounds|User_Interface
        :param frame: Number of frame or statick frame name.
        :param animation_name: Name of animation for non statick textures.
        """
        try:
            texture_surface: Surface = self.get_temporary_texture(
                texture_type=texture_type,
                texture_name=texture_name,
                animation_name=animation_name,
                frame=str(frame)
            )
            return texture_surface.get_width(), \
                texture_surface.get_height()
        except KeyError:
            return self._texture_catalog[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ].get_width(), \
                self._texture_catalog[
                    texture_type
                ][
                    texture_name
                ][
                    animation_name
                ][
                    str(frame)
                ].get_height()
