from ..Universal_computing.Surface_size import surface_size
"""
Contains calculations for user interface buttons.
"""
# Interface collections:
yes_no_menus: list[str] = [
    'save_menu',
    'load_menu',
    'exit_menu',
    'settings_status_menu',
    'back_to_start_menu_status_menu'
]
long_buttons_menus: list[str] = [
    'game_menu',
    'settings_menu',
    'start_menu',
    'creators_menu'
]


def yes_no_menu_button_size(background_size_x, background_size_y):
    """
    Calculate button size.

    :param background_size_x: surface_size result.
    :type background_size_x: int
    :param background_size_y: surface_size result.
    :type background_size_y: int
    """
    # X:
    x_size: int = int(background_size_x / 100 * 15)
    # Y:
    y_size: int = int(background_size_y / 100 * 10)
    return x_size, y_size


def menu_long_button_size(background_size_x, background_size_y):
    """
    Calculate button size.

    :param background_size_x: surface_size result.
    :type background_size_x: int
    :param background_size_y: surface_size result.
    :type background_size_y: int
    """
    # X:
    x_size: int = int(background_size_x / 100 * 30)
    # Y:
    y_size: int = int(background_size_y / 100 * 10)
    return x_size, y_size


def dialogue_button_size(background_size_x, background_size_y):
    """
    Calculate dialogue button size.

    :param background_size_x: surface_size result.
    :type background_size_x: int
    :param background_size_y: surface_size result.
    :type background_size_y: int
    """
    # X:
    x_size: int = int(background_size_x / 100 * 66)
    # Y:
    y_size: int = int(background_size_y / 100 * 10)
    return x_size, y_size


def button_size(*, place_flag, background_surface) -> tuple[int, int]:
    """
    Calculate button size.

    :param background_surface: pygame.Surface of background.
    :param place_flag: String with flag type of button.
    :return: Tuple with x and y sizes of button`s surface.
    """
    background_surface_size: tuple[int, int] = surface_size(interested_surface=background_surface)
    background_size_x, background_size_y = background_surface_size
    x_size, y_size = (0, 0)

    if place_flag == 'gameplay_ui':
        side_of_the_square: int = int(background_size_y / 100 * 4.17)
        x_size, y_size = (side_of_the_square, side_of_the_square)

    if place_flag in long_buttons_menus:
        x_size, y_size = menu_long_button_size(background_size_x, background_size_y)

    if place_flag in yes_no_menus:
        x_size, y_size = yes_no_menu_button_size(background_size_x, background_size_y)

    if place_flag == 'gameplay_dialogues_choice':
        x_size, y_size = dialogue_button_size(background_size_x, background_size_y)

    return x_size, y_size
