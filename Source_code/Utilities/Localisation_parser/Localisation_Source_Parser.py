from argparse import ArgumentParser, Namespace
from os import path
from configparser import ConfigParser

from ..Universal_computing.Config_Parser_INI import ConfigParserINI
"""

"""


class LocalisationSourceParser(ConfigParserINI):
    def __init__(self, *, source_path: str):
        super().__init__(
            replace_path=[
                'Utilities', 'Localisation_parser', 'Localisation_Source_Parser.py'
            ],
            source_path=source_path
        )

    def execute(self):
        self._read_source()


if __name__ == "__main__":
    # Parse args:
    arguments_parser: ArgumentParser = ArgumentParser()
    arguments_parser.add_argument(
        "-sp",
        "--sp",
        default="./GamePlay_Localisation_source",
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
