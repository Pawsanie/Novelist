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
    def __init__(
            self, *,
            source_path: str,
            alternative_destination_path: str | None = None
    ):
        """
        :param source_path: Source path for reading ini screenplay scene files.
        :param alternative_destination_path: Alternative destination path for screenplay.json.
                                             If you need screenplay.json specific file path.
                                             As example if the utility is not in the directory
                                             with your copy of the game.
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
            "speaker_name_color",
            "speech_text_color",

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

        self._default_speaker_name_color: str = "#ffffff"
        self._default_speech_text_color: str = "#ffffff"
        self._default_choice_text_color: str = "#ffffff"

        self._scene_row_data_collection: dict = {}
        self._scene_settings_collection: dict = {}
        self._scene_name_collections: list = []

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
                except MissingSectionHeaderError:
                    print(
                        f"File {file_name} have no legal header, or this is no ini configuration. File ignored."
                    )
                except ParsingError:
                    print(
                        f"File {file_name} have no legal ini syntax. File ignored."
                    )

    def _get_row_data(self):
        """
        Get row data from scene config`s and parse it to dictionary.
        """
        # Get row data from configs:
        for scene_name in self._config_parser.sections():
            if scene_name in self._scene_name_collections:
                print(
                    "Critical parse error:\n"
                    f"Scene name {scene_name} already parsed.\n"
                    "Scenes must have unique names."
                )
                exit(1)
            else:
                self._scene_name_collections.append(scene_name)

            scene_settings: dict = {}
            for key, value in self._config_parser.items(scene_name):
                if value.lower() in ("false", "no", "off"):
                    value: bool = False
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
                "speaker_name_color": "#00ffff",
                "speech_text_color": "#ffffff",
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
                        "text_color": "#ffffff",
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

            # Reading gameplay:
            if scene_settings["scene_type"] == "reading":
                if "next_scene" not in scene_settings:
                    print(
                        f"Parsing critical error:\n"
                        f"Reading scene {scene_name} have no 'next_scene' key..."
                    )
                    exit(1)
                if "speaker_name_color" in scene_settings:
                    speaker_name_color: str = scene_settings["speaker_name_color"]
                else:
                    speaker_name_color: str = self._default_speaker_name_color
                if "speech_text_color" in scene_settings:
                    speech_text_color: str = scene_settings["speech_text_color"]
                else:
                    speech_text_color: str = self._default_speech_text_color
                self._scene_settings_collection[scene_name].update(
                    {
                        "next_scene": scene_settings["next_scene"],
                        "speaker_name_color": speaker_name_color,
                        "speech_text_color": speech_text_color,
                    }
                )

            for key, value in scene_settings.items():
                # Immutable keys:
                if key in self._parser_immutable_keys:
                    if key in (
                            "background_sprite_sheet",
                            "background_animation",
                            "past_scene",
                            "scene_type",
                            "next_scene",
                            "speaker_name_color",
                            "speech_text_color"
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
                                    "Fatal parsing error!:\n"
                                    f"Have no character key {error} in {scene_name}.\n"
                                    "But have any settings this character..."
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
                        elif type(value) is str:
                            self._scene_settings_collection[scene_name].update(
                                {
                                    "special_effects": value.split(",")
                                }
                            )

                # Scene choice targets:
                elif self._immutable_path_of_scene_choice_key in key:
                    if scene_settings["scene_type"] != "choice":
                        print(
                            "Parsing critical error:\n"
                            f"Not choice type scene {scene_name} have"
                            f"{self._immutable_path_of_scene_choice_key} key.\n"
                            f"Key name {key}"
                        )
                        exit(1)
                    if "choices" not in self._scene_settings_collection[scene_name]:
                        self._scene_settings_collection[scene_name].update(
                            {
                                "choices": {}
                            }
                        )
                    choice_name: str = key.split(".")[-1]
                    self._scene_settings_collection[scene_name]["choices"].update(
                        {
                            choice_name: {
                                "branching": value
                            }
                        }
                    )
                    try:
                        self._scene_settings_collection[scene_name]["choices"][choice_name].update(
                            {
                                "text_color": scene_settings[f"choice_text_color.{choice_name}"]
                            }
                        )
                    except KeyError:
                        self._scene_settings_collection[scene_name]["choices"][choice_name].update(
                            {
                                "text_color": self._default_choice_text_color
                            }
                        )
                # Independently not significant key:
                elif "choice_text_color" in key:
                    if scene_settings["scene_type"] == "choice":
                        continue
                    else:
                        print(
                            "Critical parsing error:\n"
                            f"Scene {scene_name}.\n"
                            "Choice text color key in not choice scene type detected."
                        )
                        exit(1)

                # Invalid keys:
                else:
                    print(
                        "Warning:\n"
                        f"Invalid configuration key detected: {key}"
                    )

    def _land_screenplay(self):
        """
        Land screenplay data to screenplay.json file.
        """
        if len(self._scene_settings_collection) > 0:
            with open(
                    file=self._destination_path,
                    mode='w',
                    encoding='utf-8'
            ) as file:
                json.dump(
                    obj=self._scene_settings_collection,
                    fp=file,
                    ensure_ascii=False,
                    indent=2
                )

            print(
                f"Successfully land screenplay data to path: {self._destination_path}"
            )
        else:
            print(
                "Have no data to landing."
            )

    def get_scenes(self):
        """
        Get scene names.
        """
        self._devnull()
        self._read_source()
        self._get_row_data()
        self._parse_scene_configs()
        return self._scene_settings_collection.keys()

    def execute(self):
        """
        Execute class destination.
        """
        self._devnull()
        self._read_source()
        self._get_row_data()
        self._parse_scene_configs()
        self._land_screenplay()

    def _devnull(self):
        """
        Devnull collections data.
        """
        self._scene_row_data_collection.clear()
        self._scene_settings_collection.clear()
        self._scene_name_collections.clear()


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
