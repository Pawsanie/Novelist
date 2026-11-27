from os.path import join

from ..Fundamentals.Patterns import SingletonPattern
from .Internal import get_root_path, ini_output_internal
"""
Contains code responsible for file output.
"""


class FileLoader(SingletonPattern):
    """
    Responsible for file output.
    """
    def __init__(self):
        # Path attributes:
        self.__root_path: str = get_root_path()

    def ini_load(
            self,
            file_name: str,
            data: dict
    ) -> dict:
        """
        Land INI config file.
        :param file_name: File name without file format.
        :param data: New INI config for writing.
                 As exemple: {
                    "section_name": {
                        "comment": str,
                        "fields": {
                            "field_name": {
                                    "comment": str,
                                    "value": value_data
                                },
                            ...
                        }
                    },
                    ...
                }
        """
        return ini_output_internal(

            path=f"{self.__root_path}"
            f"{
                join(
                    *[
                        "Scripts",
                        "INI",
                        file_name
                    ]
                )
            }"
            f".{self.__ini_format}",
            data=data

        )
