from configparser import ConfigParser
from os import sep, path
"""
The utility for building a screenplay.
"""


class ScreenplaySourceParser:
    """
    Parse scene configs to screenplay json.
    """
    def __init__(self, source_path: str):
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
            "scene_reading_gameplay_text_file",
            "scene_choice_gameplay_text_file",

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
        self._scene_settings_collection: dict = {}

    def read_source(self, path_to_file: str):
        """
        Read ini screenplays files.
        """
        scene_config = self._config_parser.read(
            path_to_file
        )


