from os.path import abspath, join
"""
Contains code responsible for FileLoader files root path.
"""


def get_root_path() -> str:
    """
    Get root path for FileLoader.
    """
    return abspath(__file__) \
        .replace(
        join(
            *(
                'Scripts', 'Python', 'Loader', 'Internal', 'Assets_root_path.py'
            )
        ), ''
    )
