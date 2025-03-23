from configparser import ConfigParser, MissingSectionHeaderError, ParsingError
from os import walk
from os.path import join, abspath
"""

"""


class ConfigParserINI:
    def __init__(self, *, replace_path: list[str], source_path: str):
        # Path Settings:
        self._replace_path: str = join(
            *replace_path
        )
        self._root_path: str = f"{abspath(__file__).replace(self._replace_path, '')}"
        self._source_path: str = source_path

        # Parser settings:
        self._config_parser: ConfigParser = ConfigParser()

    def _read_source(self):
        """
        Read ini screenplays files.
        """
        for target_path, path_folders, catalog_filenames in walk(self._source_path):
            for file_name in catalog_filenames:
                if file_name == "example_scene_config.ini":
                    continue
                target_file: str = join(
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
