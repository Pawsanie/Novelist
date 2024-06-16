from configparser import ConfigParser, MissingSectionHeaderError, ParsingError
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

        self._scene_row_data_collection: dict = {}
        self._scene_settings_collection: dict = {}

    def _read_source(self):
        """
        Read ini screenplays files.
        """
        for target_path, path_folders, catalog_filenames in walk(self._source_path):
            for file_name in catalog_filenames:
                target_file: str = path.join(
                    *[
                        target_path, file_name
                    ]
                )
                try:
                    self._config_parser.read(
                        target_file
                    )
                except MissingSectionHeaderError as exception:
                    ...
                except ParsingError as exception:
                    ...

    def _get_row_data(self):
        """
        Get row data from scene config`s and parse it to dictionary.
        """
        # Get row data from configs:
        for scene_name in self._config_parser.sections():
            scene_settings: dict = {}
            for key, value in self._config_parser.items(scene_name):
                scene_settings.update(
                    {
                        key: value
                    }
                )
            self._scene_row_data_collection.update(
                {
                    scene_name: scene_settings
                }
            )

    def _parse_scene_configs(self):
        """
        Parse row data to dictionary for easy landing in screenplay.json.
        """
        ...

    def execute(self):
        """
        Execute class destination.
        """
        self._read_source()
        self._get_row_data()
        self._parse_scene_configs()


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
