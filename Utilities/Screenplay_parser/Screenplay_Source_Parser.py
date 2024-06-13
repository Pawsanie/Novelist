from configparser import ConfigParser
from os import sep, path, walk
import json
from argparse import ArgumentParser, Namespace
"""
The utility for building a screenplay.
"""


class ScreenplaySourceParser:
    """
    Parse scene configs to screenplay json.
    """
    def __init__(self, *, source_path: str):
        """
        :param source_path: Source path for reading ini screenplay scene files.
        :type source_path: str
        """
        # Path Settings:
        self.__replace_path_list: list[str] = [
            'Scripts', 'Utilities', 'Source_parser.py'
        ]
        self.__root_path: str = f"{path.abspath(__file__).replace(path.join(*self.__replace_path_list), '')}"
        self.__screenplay_add_path: str = path.join(
            *[
                "Scripts", "Json_data" "screenplay.json"
            ]
        )
        self.__screenplay_path: str = f"{self.__root_path}{sep}{self.__screenplay_add_path}"
        self._source_path: str = source_path

        # Parser settings:
        self._config_parser: ConfigParser = ConfigParser()
        self._parser_immutable_keys: tuple = (
            # Scene Settings:
            "scene_type",
            "scene_special_effects"
            "scene_text_file",

            # Background:
            "background_sprite_sheet",
            "background_animation",

            # Left Character:
            "left_character_name",
            "left_character_animation",
            "left_character_sprite_sheet",

            # Middle Character:
            "middle_character_name",
            "middle_character_animation",
            "middle_character_sprite_sheet",

            # Right Character:
            "right_character_name",
            "right_character_animation",
            "right_character_sprite_sheet"
        )
        self._immutable_path_of_scene_choice_key: str = "scene_choice"
        self._valid_scene_types: tuple = (
            "reading",
            "choice"
        )

        self._scene_settings_collection: dict = {}

    def _read_source(self):
        """
        Read ini screenplays files.
        """
        for root_path, folders, filenames in walk(self._source_path):
            ...

        # scene_config = self._config_parser.read(
        #     path_to_file
        # )

    def execute(self):
        self._read_source()


if __name__ == "__main__":
    """
    Get path from scrypt run argument and run screenplay parser.
    """
    # Parse args:
    arguments_parser: ArgumentParser = ArgumentParser()
    arguments_parser.add_argument(
        "-sp",
        "--sp",
        type=str,
        help="This is a scene`s configs source path flag. Example ./*.py -ps ./example/path"
    )
    arguments: Namespace = arguments_parser.parse_args()

    if any(
            vars(arguments).values()
    ):
        if arguments.sp:
            screenplay_data_source_path: str = arguments.sp
        else:
            raise "Have no -sp flag: please use flag -h for help"
    else:
        screenplay_data_source_path: str = "./Screenplay_source"

    # Execute:
    ScreenplaySourceParser(
        source_path=screenplay_data_source_path
    ).execute()
