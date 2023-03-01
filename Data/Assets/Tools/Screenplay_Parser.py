import logging
from os import path, walk, sep
import json
from configparser import ConfigParser

from ..Scripts.Logging_Config import text_for_logging, logging_config
"""
Contains code responsible for ScreenplayParser.
"""


class ScreenplayParser:
    """
    Brings the outline of the script to the desired form and saves it to the correct json dictionaries.
    """
    def __init__(self):
        # Arguments processing:
        logging_config(
            log_path="Screenplay_Logg.txt",
            log_level=30
        )
        self.root_game_path: str = path.abspath(__file__)\
            .replace(path.join(
                *['Tools', 'Screenplay_Parser.py']
            ), '')
        self.path_to_json_data: str = path.join(
            *[self.root_game_path, 'Scripts', 'Json_data']
        )
        # Json paths:
        self.path_to_screenplay: str = path.join(
            *[self.path_to_json_data, 'screenplay.json']
        )
        self.path_to_choices_data: str = path.join(
            *[self.path_to_json_data, 'Dialogues', 'choices_data.json']
        )

        # Parsing path:
        self.parsing_root_path: str = ""
        # Files collection:
        self.file_list: list = []
        self.data_for_parsing: ConfigParser = ConfigParser(
            allow_no_value=True,
            empty_lines_in_values=True
        )

        # Data flags:
        self.screenplay_header: str = '#####Screenplay#####'
        self.reading_header: str = '#####Reading#####'
        self.choice_header: str = '#####Choice#####'

        # Result Collection:
        self.screenplay: dict[str] = {}

    def set_parsing_root_path(self, parsing_root_path: str):
        """
        Set path for game screenplay parsing.
        """
        self.parsing_root_path: str = parsing_root_path

    def get_data_for_screenplay(self):
        """
        Looks for files in a directory and recursively in the folders
        that are inside it in order to extract screenplay data from them.
        """
        self.file_list.clear()
        for dirs, folders, files in walk(self.parsing_root_path):
            for file in files:
                path_to_file: str = path.join(dirs, file)
                if path.isfile(path_to_file):
                    self.file_list.append(path_to_file)

    def extract_data_for_screenplay(self):
        """
        Extract data from files.
        """
        for file_path in self.file_list:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_data: list[str] = file.readlines()

                    if file_data[0].replace('\n', '') == self.screenplay_header:
                        pass
                    elif file_data[0].replace('\n', '') == self.reading_header:
                        self.extract_text_for_reading(file_data)
                        continue
                    elif file_data[0].replace('\n', '') == self.choice_header:
                        self.extract_text_for_choice(file_data)
                        continue
                    else:
                        continue
                self.data_for_parsing.read(file_path, encoding='utf-8')

            except Exception as error:
                logging.warning(
                    text_for_logging(
                        log_text=
                        "Problems with file:\n"
                        f"{file_path}",
                        log_error=error
                    ))

    def extract_text_for_reading(self, file_data):
        ...

    def extract_text_for_choice(self, file_data):
        ...

    def extract_screenplay_instructions(self):
        for scene in self.data_for_parsing:
            if scene != 'DEFAULT':
                try:
                    print(self.data_for_parsing.get(scene, 'text'))

                except Exception as error:
                    logging.warning(
                        text_for_logging(
                            log_text=
                            "Problems with cfg file data:",
                            log_error=error
                        ))
