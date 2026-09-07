from json import loads
"""
Contains code responsible for json assets load.
"""


def json_load_internal(path: str) -> dict:
    """
    Load json for FileLoader.
    :param path: Absolute path to file as string.
    """
    with open(
            file=path,
            mode='r',
            encoding='utf-8'
    ) as json_file:
        return loads(
            json_file.read()
        )
