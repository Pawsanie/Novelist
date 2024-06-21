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
            "scene_text_file",
            "past_scene",

            # Background:
            "background_sprite_sheet",
            "background_animation",

            # Reading gameplay:
            "next_scene",

            # Left Character:
            "left_character_animation",
            "left_character_sprite_sheet",
            "left_character_plan",
            "left_character_position",
            "left_character_start_animation",

            # Middle Character:
            "middle_character_animation",
            "middle_character_sprite_sheet",
            "middle_character_plan",
            "middle_character_position",
            "middle_character_start_animation",

            # Right Character:
            "right_character_animation",
            "right_character_sprite_sheet",
            "right_character_plan",
            "right_character_position",
            "right_character_start_animation",
            
            # Scene optional settings:
            "scene_special_effects",
            "music",
            "sound",
            "voice"
        )
        self._immutable_path_of_scene_choice_key: str = "scene_choice"
        self._reading_scene_type: str = "reading"
        self._scene_type: str = "scene_type"

        self._scene_row_data_collection: dict = {}
        self._scene_settings_collection: dict = {}

    def _read_source(self):
        """
        Read ini screenplays files.
        """
        for target_path, path_folders, catalog_filenames in walk(self._source_path):
            for file_name in catalog_filenames:
                if file_name == "example_scene_config.ini":
                    continue
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
        Scene settings result example:
        {
            "reading_scene_name": {
                "background": {
                    background_sprite_sheet: "back_ground_01",
                    background_animation: "animation_1"
                    },
                "actors": {
                  "character_sprite_sheet_id": {
                    "character_start_position": "right",
                    "character_animation": "animation_3",
                    "character_scene_start_animation: "animation_10",
                    "character_plan": "background_plan"
                  },
                  ...
                },
                "special_effects": false | [str, ...],
                "gameplay_type": "reading",
                "past_scene": "scene_name",
                "next_scene": "scene_name_02",
                "sounds": {
                  "music_channel": false,
                  "sound_channel": "blank",
                  "voice_channel": false
                }
            },

            "choice_scene_name": {
                "background": {
                    background_sprite_sheet: "back_ground_01",
                    background_animation: "animation_1"
                    },
                "actors": {
                  "character_sprite_sheet_id": {
                    "character_start_position": "right",
                    "character_animation": "animation_3",
                    "character_scene_start_animation: "animation_10",
                    "character_plan": "background_plan"
                  },
                  ...
                },
                "special_effects": false | [str, ...],
                "gameplay_type": "choice",
                "choices": {
                    "choice_01": {
                        "branching": "scene_name",
                        "counter_change": {
                            "counter_name": 1
                        }
                    },
                    ...
                }
                "past_scene": "scene_name",
                "sounds": {
                  "music_channel": false,
                  "sound_channel": "blank",
                  "voice_channel": false
                }
            },
        }
        """
        for scene_name, scene_settings in self._scene_row_data_collection.items():
            # Default keys:
            self._scene_settings_collection.update(
                {
                    scene_name: {
                        "gameplay_type": scene_settings["scene_type"],
                        "background": {
                            "background_sprite_sheet": scene_settings["background_sprite_sheet"],
                            "background_animation": scene_settings["background_animation"]
                        },
                        "past_scene": scene_settings["past_scene"],
                        "actors": {}
                    }
                }
            )
            for key, value in scene_settings.items():
                # Immutable keys:
                if key in self._parser_immutable_keys:
                    if key in (
                            "background_sprite_sheet",
                            "background_animation",
                            "past_scene",
                            "scene_type"
                    ):
                        continue

                    # Scene Actors:
                    elif "character" in key:
                        for position in (
                                "left",
                                "middle",
                                "right"
                        ):
                            if key != f"{position}_character_sprite_sheet":
                                continue
                            try:
                                self._scene_settings_collection[scene_name]["actors"].update(
                                    {
                                        value: {}
                                    }
                                )
                                self._scene_settings_collection[scene_name]["actors"][value].update(
                                    {
                                        "character_animation":  scene_settings[
                                            f"{position}_character_animation"
                                        ],
                                        "character_plan": scene_settings[
                                            f"{position}_character_plan"
                                        ],
                                        "character_start_position": position
                                    }
                                )
                            except KeyError as error:
                                print(
                                    f"Fatal parsing error!:\n"
                                    f"Have no character key {error} in {scene_name}.\n"
                                    f"But have any settings this character..."
                                )
                                exit(1)
                            try:
                                for optional_key, optional_value in {
                                    "character_position": [
                                                f"{position}_character_start_position"
                                            ],
                                    "character_scene_start_animation": scene_settings[
                                        f"{position}_character_start_animation"
                                    ]
                                }.items():
                                    self._scene_settings_collection[scene_name]["actors"][value].update(
                                        {
                                            optional_key: optional_value
                                        }
                                    )
                            except KeyError:
                                pass

                    # Sound optional scene settings:
                    elif key in (
                        "music",
                        "sound",
                        "voice"
                    ):
                        if "sounds" not in self._scene_settings_collection[scene_name].keys():
                            self._scene_settings_collection[scene_name].update(
                                {
                                    "sounds": {}
                                }
                            )
                        self._scene_settings_collection[scene_name]["sounds"].update(
                            {
                                f"{key}_channel": value
                            }
                        )

                    # Special effects optional settings:
                    elif key == "scene_special_effects":
                        if value is False:
                            self._scene_settings_collection[scene_name].update(
                                {
                                    "special_effects": value
                                }
                            )
                        elif value is str:
                            self._scene_settings_collection[scene_name].update(
                                {
                                    "special_effects": value.split(",")
                                }
                            )

                # Scene choice targets:
                elif self._immutable_path_of_scene_choice_key in key:
                    if scene_settings[self._scene_type] == self._reading_scene_type:
                        print(
                            f"Scene {scene_name}: "
                            f"{self._immutable_path_of_scene_choice_key} key "
                            f"in {self._reading_scene_type} detected."
                        )
                        continue
                    scene_choose_name, scene_choose_target = key.split(".")
                    self._scene_settings_collection[scene_name].update(
                        {
                            "choices": {
                                scene_choose_name: {
                                    "branching": scene_choose_target
                                }
                            }
                        }
                    )
                else:
                    print(
                        f"Invalid configuration key detected: {key}"
                    )

    def _land_screenplay(self):
        """
        Land screenplay data to screenplay.json file.
        """
        if len(self._scene_settings_collection) > 0:
            ...

            print(
                f"Successfully land screenplay data to path: {self._destination_path}"
            )
        else:
            print(
                f"Have no data to landing."
            )

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
