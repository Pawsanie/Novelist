from configparser import ConfigParser
"""
Contains code responsible for INI assets I/O.
"""


def ini_load_internal(path: str) -> dict:
    """
    Load INI for FileLoader.
    :param path: Absolute path to file as string.
    :return: As exemple: {
                "Section": {
                    "field": value,
                    ...
                },
                ...
            }
    """
    with open(
            file=path,
            mode='r',
            encoding='utf-8'
    ) as ini_file:

        config_data: ConfigParser = ConfigParser(
            inline_comment_prefixes=(
                "#",
                ";"
            )
        ).read_file(
            ini_file
        )

        return {
            section: dict(
                config_data[section]
            )
            for section in config_data.sections()
        }


def ini_output_internal(
    path: str,
    data: dict
):
    ...
