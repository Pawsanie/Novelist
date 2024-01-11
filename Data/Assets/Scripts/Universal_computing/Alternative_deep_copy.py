"""
Contain alternative method for data deep copy code.
"""


def deep_copy_alternative(interesting_data: dict) -> dict:
    """
    Alternative for dict deepcopy, because it cant works with pygame.
    :param interesting_data: Dict with menus data.
    :type interesting_data: dict
    """
    result: dict = {}
    for key, value in interesting_data.items():
        result.update(
            {key: value}
        )
    return result
