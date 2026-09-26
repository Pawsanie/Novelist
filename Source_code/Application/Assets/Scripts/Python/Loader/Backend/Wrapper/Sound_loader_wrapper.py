"""
Contains code responsible for sound assets loader wrapper.
"""


def load_sound(path: str) -> bytes:
    """
    Load sound file from file system.
    :param path: Absolute path to file.
    """
    with open(
            file=path,
            mode='rb'
    ) as file:
        return file.read()
