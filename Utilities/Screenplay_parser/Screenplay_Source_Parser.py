from configparser import ConfigParser, MissingSectionHeaderError, ParsingError
from os import path, walk
import json
from argparse import ArgumentParser, Namespace
"""
The utility for building a screenplay.
"""


class ScreenplaySourceParser:
    """
    Parse scene configs to screenplay json.
    """
    def __init__(self, *, source_path: str, alternative_destination_path: str | None = None):
        """
        :param source_path: Source path for reading ini screenplay scene files.
        :type source_path: str
        :param alternative_destination_path: Alternative destination path for screenplay.json.
                                             If you need screenplay.json specific file path.
                                             As example if the utility is not in the directory
                                             with your copy of the game.
        :type alternative_destination_path: str
        """
        # Path Settings:
        self.__replace_path: str = path.join(
            *[
                'Utilities', 'Screenplay_parser', 'Screenplay_Source_Parser.py'
            ]
        )
        self.__root_path: str = f"{path.abspath(__file__).replace(self.__replace_path, '')}"
        self.__screenplay_add_path: str = path.join(
            *[
                "Data", "Assets", "Scripts", "Json_data", "screenplay.json"
            ]
        )
        self.__screenplay_path: str = path.join(
            *[
                self.__root_path, self.__screenplay_add_path
            ]
        )
        self._source_path: str = source_path
        if alternative_destination_path is not None:
            self._destination_path: str = alternative_destination_path
        else:
            self._destination_path: str = self.__screenplay_path

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

    def _land_screenplay(self):
        """
        Land screenplay data to screenplay.json file.
        """
        ...

    def execute(self):
        """
        Execute class destination.
        """
        self._read_source()
        self._get_row_data()
        self._parse_scene_configs()
        self._land_screenplay()


if __name__ == "__main__":
    """
    Get path from scrypt run argument and run screenplay parser.
    """
    # Parse args:
    arguments_parser: ArgumentParser = ArgumentParser()
    arguments_parser.add_argument(
        "-sp",
        "--sp",
        default="./Screenplay_source",
        type=str,
        help="This is a scene`s configs Source Path flag. Example: python ./*.py -sp ./example/path"
    )
    arguments_parser.add_argument(
        "-dp",
        "--dp",
        type=str or None,
        default=None,
        help="This is a scene`s screenplay Destination Path flag. Example: python ./*.py -dp ./example/path"
    )
    arguments: Namespace = arguments_parser.parse_args()
    screenplay_data_source_path: str = arguments.sp
    screenplay_destination_path: str | None = arguments.dp

    # Execute:
    ScreenplaySourceParser(
        source_path=screenplay_data_source_path,
        alternative_destination_path=screenplay_destination_path
    ).execute()
