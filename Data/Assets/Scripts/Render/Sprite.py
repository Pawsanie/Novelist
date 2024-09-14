from random import randint

from pygame import Surface, time, transform

from .Texture_Master import TexturesMaster
"""
Responsible for the code of a sprites used in rendering.
"""


class Sprite:
    """
    Spites uses in batch rendering.
    """
    def __init__(
            self, *, layer: int = 1,
            coordinates: tuple[int, int] = (0, 0),
            texture_mame: str,
            name: str | None = None,
            sprite_sheet_data: dict | None = None,
            sprite_size: tuple[int, int] = (0, 0)
    ):
        """
        Don't forget to specify the size of the "sprite_size" argument if it is not set in the loop by "scale" method!
        :param layer: Layer for sprite render.
                      1 as default.
        :type layer: int
        :param coordinates: Coordinates for sprite render.
                            (0, 0) as default.
        :type coordinates: tuple[int, int]
        :param name: Sprite name.
                     None as default.
        :type name: str | None
        :param sprite_sheet_data: As exemple:
                                  {
                                    "texture_type": "Characters"|"Backgrounds"|"User_Interface",
                                    "sprite_sheet": bool,
                                    "statick_frames"|"animations": {
                                        "any_animation_name": {  # The animation name only matters for animated sprites,
                                                                 # in the context of switching.
                                            {...},  # The data inside is irrelevant for statick sprites.
                                            "time_duration": float  # The only important value for animation sprites.
                                        }
                                    }
                                  }
        :type sprite_sheet_data: dict
        :param sprite_size: Sprite image Surface size.
        :type sprite_size: tuple[int, int]
        """
        # Program layers settings:
        self._texture_master: TexturesMaster = TexturesMaster()

        # Arguments processing:
        self._name: str | None = name
        self._layer: int = layer
        self._coordinates: tuple[int, int] = coordinates
        self._texture_id: str = texture_mame
        self._sprite_sheet_data: dict | None = sprite_sheet_data

        # Other settings:
        self._frame_time: int = time.get_ticks()
        self._image_size: tuple[int, int] = sprite_size

        # Sprite sheet animation data:
        self._animation_name: str = self._get_default_animation_name()
        self._sprite_sheet_frame: int | str = self._get_sprite_frame_name()
        self._pause_duration: int = 0

        # Render settings:
        self._scene_name: str | None = None
        self._recache_status: bool = True

    def _get_default_animation_name(self) -> str | None:
        """
        {
            "sprite_sheet": bool,
            "animation_name": {  # For statick is "statick_frames"
                any: dict
            }
        }
        """
        if self._sprite_sheet_data["sprite_sheet"] is False:
            return "statick_frames"
        else:
            return list(
                    self._sprite_sheet_data["animations"].keys()
                )[0]

    def _get_sprite_frame_name(self) -> int | str | None:
        """
        Sprite frame name can be any data types and values which can be keys in dictionaries.
        """
        if self._animation_name == "statick_frames":
            result: str = list(
                self._sprite_sheet_data[
                    "statick_frames"
                ].keys()
            )[0]
        else:
            result: int = 1
        return result

    def get_layer(self) -> int | str:
        """
        Use in Batch.
        """
        return self._layer

    def _recache_sprite(self):
        """
        Recache sprite in TextureMaster if necessary.
        """
        universal_parameters: dict = {
            "texture_type": self._sprite_sheet_data["texture_type"],
            "texture_name": self._texture_id,
            "animation_name": self._animation_name,
            "frame": self._sprite_sheet_frame
        }
        if self._texture_master.get_texture_size(
                **universal_parameters
        ) != self._image_size:
            if self._recache_status is False:
                temporary_texture: Surface = Surface(self._image_size)
                temporary_texture.blit(
                    transform.scale(
                        surface=self._texture_master.get_texture(**universal_parameters),
                        size=self._image_size
                    ),
                    (0, 0)
                )
                self._texture_master.set_temporary_texture(
                    texture_type=self._sprite_sheet_data["texture_type"],
                    texture_name=self._texture_id,
                    surface=temporary_texture
                )
                return
            self._texture_master.set_new_scale_frame(
                **universal_parameters,
                image_size=self._image_size
            )

    def blit_to(self, any_surface: Surface):
        """
        Draw sprite image on surface.
        Can be used in Render, Layer classes in context of render pipline.
        :param any_surface: Any Surface.
        :type any_surface: Surface
        """
        self._recache_sprite()
        any_surface.blit(
            self._texture_master.get_texture(
                texture_type=self._sprite_sheet_data["texture_type"],
                texture_name=self._texture_id,
                animation_name=self._animation_name,
                frame=self._sprite_sheet_frame
            ),
            self._coordinates
        )

    def blit(self, any_surface: Surface, coordinates: tuple[int, int]):
        """
        Draw surface image on Sprite texture and crate temporary texture for TextureMaster.
        Can be use in Buttons in context of UI image Render pipline.
        :param any_surface: Any Surface.
        :type any_surface: Surface
        :param coordinates: Render coordinates.
        :type coordinates: tuple[int, int]
        """
        self._recache_sprite()
        temporary_texture: Surface = self._texture_master.get_texture(
            texture_type=self._sprite_sheet_data["texture_type"],
            texture_name=self._texture_id,
            animation_name=self._animation_name,
            frame=self._sprite_sheet_frame
        )
        temporary_texture.blit(
            any_surface,
            coordinates
        )
        self._texture_master.set_temporary_texture(
            texture_type=self._sprite_sheet_data["texture_type"],
            texture_name=self._texture_id,
            surface=temporary_texture
        )

    def _sprite_sheet_next_frame(self):
        """
        Switch frames in Sprite 2d animation if possible.
        """
        if self._sprite_sheet_data is None:
            return

        if self._animation_name is None:
            self._animation_name: str = list(
                self._sprite_sheet_data.keys()
            )[0]

        if self._animation_name == "statick_frames":
            return

        self._sprite_sheet_frame: int = self.get_frame_number()

    @staticmethod
    def _get_scene_name() -> str:
        """
        Get scene name.
        """
        from ..GamePlay.Scene_Validator import SceneValidator
        return SceneValidator().get_current_scene_name()

    def get_animation_name(self) -> str:
        """
        Use in Character and Backgrounds.
        """
        return self._animation_name

    def get_frame_number(self) -> int:
        """
        Get step for sprite sheet frame swap.
        :result: int
        """
        # Statick frame:
        if self._animation_name == "statick_frames":
            return self._sprite_sheet_frame

        # Animation frame:
        current_time_frame: int = time.get_ticks()

        if (current_time_frame - self._frame_time) / 1000 >= self._pause_duration:
            self._frame_time: int = current_time_frame
            return self._sprite_sheet_frame

        if (current_time_frame - self._frame_time) / 1000 >= (
                self._sprite_sheet_data[self._animation_name]["time_duration"]
                / len(self._sprite_sheet_data[self._animation_name]["frames"])
        ):
            self._frame_time: int = current_time_frame
            if self._sprite_sheet_frame + 1 <= len(
                        self._sprite_sheet_data[self._animation_name]["frames"]
            ):
                self._sprite_sheet_frame += 1
            else:
                self._sprite_sheet_frame: int = 1
                self._pause_duration: int = randint(2, 5)
        return self._sprite_sheet_frame

    def set_recache_status(self, recache_status: bool = True):
        """
        :param recache_status: If there is no need to cache the sprite texture, a temporary image will be created.
        :type recache_status: bool
        """
        self._recache_status: bool = recache_status

    def scale(self, size: tuple[int, int]):
        """
        Scale Sprite image to size.
        :param size: Tuple with x/y size data.
        :type size: tuple[int, int]
        """
        self._image_size: tuple[int, int] = size

    def play_animation(self, animation_name: str):
        """
        Set new animation to play.
        """
        self._animation_name: str = animation_name

    def set_coordinates(self, current_coordinates: tuple[int, int]):
        self._coordinates: tuple[int, int] = current_coordinates
