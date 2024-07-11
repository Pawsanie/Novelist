from os import path
from csv import DictReader
import json

from pygame import image, font, mixer, Surface

from .Pattern_Singleton import SingletonPattern
"""
Contains code responsible for assets load.
"""


class AssetLoader(SingletonPattern):
    """
    Responsible for assets load.
    """
    def __init__(self):
        # Root path attributes:
        self.__replace_path_list = [
            'Scripts', 'Universal_computing', 'Assets_load.py'
        ]
        self.__root_path: str = f"{path.abspath(__file__).replace(path.join(*self.__replace_path_list), '')}"

        # Sound attributes:
        self.__sounds_formats: dict[str] = {
            "Voice": "mp3",
            "Music": "mp3",
            "Effects": "mp3"
        }

        # Font attributes:
        self.__font_format: str = "TTF"

        # Images attributes:
        self.__images_instructions: dict[str] = {
            "Characters":
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
        }

    def json_load(self, path_list: list[str]) -> dict:
        """
        :param path_list: list with strings of folders names and file name.
        :type path_list: list[str]
        :return: dict
        """
        with open(
                file=f"{self.__root_path}{path.join(*path_list)}.{'json'}",
                mode='r',
                encoding='utf-8'
        ) as json_file:
            return json.loads(
                json_file.read()
            )

    def image_load(self, *, art_name: str, asset_type: str,
                   file_catalog: str = "", root_path: str = 'Images',
                   art_name_is_path: bool = False) -> Surface:
        """
        Load image by name and return it as Surface for image rendering.
        :param asset_type: String.
                           Example: "Characters".
        :type asset_type: str
        :param art_name: must be string with file name without file format.
        :param file_catalog: Catalog in Asset_Type_Folder.
                             Null as default.
        :type file_catalog: str
        :param root_path: Root path for get image file. Images as default.
        :type root_path: str
        :param art_name_is_path: If True art_name will be art_path.
        :type art_name_is_path: bool
        :return: Surface
        """
        file_format: str = self.__images_instructions[asset_type]["file_format"]
        if art_name_is_path is False:
            art_additional_part: str = f"{path.join(*[root_path, asset_type, file_catalog, art_name])}"
            art_path: str = f"{self.__root_path}{art_additional_part}.{file_format}"
        else:
            art_path: str = f"{art_name}.{file_format}"

        if self.__images_instructions[asset_type]["alpha_chanel"] is True:
            return image.load(art_path).convert_alpha()
        else:
            return image.load(art_path).convert()

    def sound_load(self, *, asset_type: str, file_name: str) -> mixer.music.load:
        """
        Load sound by name.
        :param asset_type: String: 'Effects' or 'Music'.
        :param file_name: must be string with file name in '*/Sounds/*' folder.
        :return: Loaded sound.
        """
        file_format: str = self.__sounds_formats[asset_type]
        return mixer.music.load(
            f"{self.__root_path}{path.join(*['Sounds', asset_type, file_name])}.{file_format}"
        )

    def font_load(self, *, font_name: str, font_size: int) -> font.Font:
        """
        Load font by name.
        :param font_name: Must be string with file name in '*/Fonts/*' folder.
        :param font_size: Must be int type.
        :return: Loaded font.
        """
        return font.Font(
            name=f"{self.__root_path}{path.join(*['Fonts', font_name])}.{self.__font_format}",
            size=font_size
        )

    def csv_load(self, *, file_name: str, inner_path: str = "Main", delimiter: str = "\t") -> tuple:
        """
        Load csv table by name.
        :param file_name: File name without file extension.
        :param inner_path: Path string. 'Main' as default.
        :param delimiter: Table delimiter.
        """
        with open(
                file=f"{self.__root_path}{path.join(*['Localisation', inner_path, file_name])}.csv",
                mode="r",
                encoding="utf-8"
        ) as csvfile:
            return tuple(
                dict(row)
                for (row) in DictReader(
                    f=csvfile,
                    delimiter=delimiter
                )
            )
