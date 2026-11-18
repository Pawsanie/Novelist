from copy import deepcopy


# Text formats:
JSON_FORMAT: str = "json"
FONT_FORMAT: str = "TTF"
TABLE_FORMAT: str = "csv"


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
