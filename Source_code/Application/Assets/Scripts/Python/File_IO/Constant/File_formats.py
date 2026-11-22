from copy import deepcopy
"""
Contains code responsible for file formats code.
"""


# Text formats:
JSON_FORMAT: str = "json"
FONT_FORMAT: str = "TTF"
TABLE_FORMAT: str = "csv"

# Sound formats:
MPEG3_FORMAT: str = "mp3"

# Image formats:
PNG_FORMAT: str = "png"
JPG_FORMAT: str = "jpg"

__all__: tuple[str] = (
    name
    for name in globals().copy().keys()
)


def __getattr__(name: str):
    """
    :param name: The Constant`s name.
    """
    if name not in __all__:
        raise AttributeError(name)

    return deepcopy(
        globals()[name]
    )
