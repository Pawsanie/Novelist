from os.path import join

from ..Fundamentals.Patterns import SingletonPattern
from .Backend import (
    FontProtocol,
    TextureProtocol,
    load_font,
    load_texture,
    load_sound
)
from .Internal import (
    get_root_path,
    json_load_internal,
    csv_load_internal
)
"""
Contains code responsible for assets load.
"""


class FileLoader(SingletonPattern):
    """
    Responsible for assets load.
    """
    def __init__(self):
        # Path attributes:
        self.__root_path: str = get_root_path()

        # File formats settings:
        self.__json_format: str = "json"
        self.__font_format: str = "TTF"
        self.__table_format: str = "csv"

        self.__sound_formats: dict[str, str] = {
            "Voice": "mp3",
            "Music": "mp3",
            "Effects": "mp3"
        }

        self.__image_formats: dict[str, dict[str, str | bool]] = {
            "Characters": {
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
        }

    def json_load(
            self,
            path_list: list[str] | tuple[str] | None = None,
            *,
            absolute_path: str | None = None
    ) -> dict:
        """
        Load json config file.
        :param path_list: list with strings of folders names and file name without file format.
        :param absolute_path: Absolute path to file as string without file format.
        """
        return json_load_internal(

            f"{self.__root_path}"
            f"{join(*path_list)}"
            f".{self.__json_format}"
            if type(absolute_path) is not str

            else
            f"{absolute_path}"
            f".{self.__json_format}"

        )

    def csv_load(
            self,
            path: list[str] | tuple[str]
    ) -> tuple[
        list[str],
        list[list[str]]
    ]:
        """
        Load csv table file from file system.
        :param path: list with strings of folders names and file name without file format.
                     Or path to file without root path as string.
        """
        return csv_load_internal(
            f"{
                self.__root_path
            }{
                join(
                    *[
                        "Localisation", 
                        self._convert_path(
                            path
                        )
                    ]
                )
            }.{
                self.__table_format
            }"
        )

    def image_load(
            self, *,
            asset_type: str,
            path: list[str] | tuple[str] | str
    ) -> TextureProtocol:
        """
        Load image from file system and return it as raw Texture for image rendering.
        :param asset_type: "Characters|User_Interface|Backgrounds|Saves"
        :param path: list with strings of folders names and file name without file format.
                     Or path to file without root path as string.
        """
        return load_texture(
            path=f"{
                    self.__root_path
                }{
                    join(
                        *[
                            "Images" if type(path) is not str 
                            else "", 
                            self._convert_path(
                                path
                            )
                          ]
                    )
                 }.{
                    self.__image_formats[
                        asset_type
                    ][
                        'file_format'
                    ]
                 }",
            alpha_chanel=self.__image_formats[
                asset_type
            ][
                "alpha_chanel"
            ]
        )

    def sound_load(
            self, *,
            asset_type: str,
            path: list[str] | tuple[str] | str
    ) -> bytes:
        """
        Load sound from file system and return it as bytes for sound system.
        :param asset_type: "Voice|Music|Effects".
        :param path: list with strings of folders names and file name without file format.
                     Or path to file without root path as string.
        """
        return load_sound(
            path=f"{
                    self.__root_path
                }{
                    join(
                        *[
                            "Sounds" if type(path) is not str 
                            else "", 
                            self._convert_path(path)
                        ]
                    )
                 }.{
                    self.__sound_formats[
                        asset_type
                    ]
                 }"
        )

    def font_load(
            self, *,
            path: list[str] | tuple[str] | str,
            size: int
    ) -> FontProtocol:
        """
        Load font from file system.
        :param path: Must be collection of font family and font file name, without format.
        :param size: The size at which the Font will be baked.
        """
        return load_font(
            path=f"{
                    self.__root_path
                }{
                    join(
                        *[
                            'Fonts', 
                            self._convert_path(
                                path
                            )
                        ]
                    )
                }.{
                    self.__font_format
                }",
            size=size
        )

    @staticmethod
    def _convert_path(path: list[str] | tuple[str] | str):
        """
        Provides a file path to the contract for loading.
        :param path: String or file name strings collection.
        """
        if type(path) is str:
            return path

        return join(*path)
