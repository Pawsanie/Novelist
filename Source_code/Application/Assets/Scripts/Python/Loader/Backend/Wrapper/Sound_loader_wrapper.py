"""
Contains code responsible for sound assets loader wrapper.
"""


def sound_load(path: str) -> bytes:
    """
    Load sound file from file system.
    :param path: Absolute path to file.
    """
    with open(
            file=path,
            mode='rb'
    ) as file:
        return file.read()
