from pygame import display, Surface
"""
Contains code for display image render.
"""


def text_canvas_render(*, screen_surface: Surface) -> tuple[Surface, tuple[int, int]]:
    """
    Generate text canvas surface with coordinates.
    :param screen_surface: pygame.Surface with background.
    :return: pygame.Surface with text_canvas coordinates.
    """
    # Render text canvas:
    screen_size = surface_size(screen_surface)
    text_canvas: Surface = Surface((screen_size[0], screen_size[1] // 5))
    text_canvas.set_alpha(128)
    # Text canvas coordinates:
    canvas_coordinates = (0, screen_size[1] - surface_size(text_canvas)[1])
    return text_canvas, canvas_coordinates


def meddle_point_for_character_render(*, screen_surface: Surface, character_surface: Surface) -> list[int]:
    """
    Calculation middle coordinates for character render.
    :param screen_surface: pygame.Surface of background.
    :param character_surface: pygame.Surface of character.
    :return: List with coordinates of meddle point for character render.
    """
    screen_size = surface_size(screen_surface)
    sprite_size = surface_size(character_surface)
    result = [(screen_size[0] // 2) - (sprite_size[0] // 2),
              (screen_size[1] - sprite_size[1])]
    return result


def surface_size(interested_surface: Surface) -> [int, int]:
    """
    Calculation surface size.
    :param interested_surface: pygame.Surface object.
    :return: Surface size with 2 init`s.
    """
    character_sprite_size_x = interested_surface.get_width()
    character_sprite_size_y = interested_surface.get_height()
    return character_sprite_size_x, character_sprite_size_y


def background_sprite_size(*, display_surface: Surface) -> tuple[int, int]:
    """
    :param display_surface: display.set_mode surface.
    :return: Tuple with x and y sizes for background image.
             These sizes depends display size.
    """
    _16x9: int = int(16 / 9 * 100)
    display_size = surface_size(display_surface)
    # background_size = surface_size(background_surface)
    ratio_of_sizes = int(display_size[0] / display_size[1] * 100)
    if ratio_of_sizes == _16x9:
        return display_size
    else:
        pass


def character_sprite_size(*, background_surface: Surface, character_surface: Surface) -> tuple[int, int]:
    """
    Calculation character surface size.
    Formula: Character_Sprite[x] + 85%_Background_and_Character_Sprite[x]_difference percent:
    x = Background * 85% / 100 ->
    x = Character_Sprite / x * 100 ->
    x = Character_Sprite * (1 + x / 100)
    Or Character_Sprite - 90%_Background_and_Character_Sprite[x]_difference percent:
    ... ->
    x = Character_Sprite * (1 - (100 - x) / 100)
    :param background_surface: pygame.Surface of background.
    :param character_surface: pygame.Surface of character.
    :return: Tuple with x and y sizes for character`s images.
             These sizes depends of main frame size.
    """
    def percentage_increase_or_reduction(sizes: tuple, percent: int, operator: str) -> list[int, int]:
        result = []
        for integer in sizes:
            coefficient = integer / 100
            percent_integer = coefficient * (100 - percent)
            if operator == '+':
                result.append(int(integer + percent_integer))
            if operator == '-':
                result.append(int(integer * (1 - ((100 - percent) / 100))))
        return result

    screen_size = surface_size(background_surface)
    sprite_size = surface_size(character_surface)

    # 95% from screen:
    real_screen_size_pixels_from_percent = int(screen_size[1] * 95 / 100)
    # Result calculation:
    if sprite_size[1] < real_screen_size_pixels_from_percent:
        # Percent sprite from screen:
        real_percent_size_sprite_difference = int(sprite_size[1] / real_screen_size_pixels_from_percent * 100)
        # Result calculation:
        result_size_x, result_size_y = percentage_increase_or_reduction(
            sprite_size, real_percent_size_sprite_difference, '+')
    elif sprite_size[1] > real_screen_size_pixels_from_percent:
        # Percent sprite from screen:
        real_percent_size_sprite_difference = int(real_screen_size_pixels_from_percent / sprite_size[1] * 100)
        # Result calculation:
        result_size_x, result_size_y = percentage_increase_or_reduction(
            sprite_size, real_percent_size_sprite_difference, '-')
    else:
        result_size_x, result_size_y = sprite_size
    return result_size_x, result_size_y


def render(*, screen: Surface, background: Surface, characters_dict: dict):
    """
    Render image on display.
    :param screen: Display.
    :param background: pygame.Surface with background.
    :param characters_dict: Dictionary with 'character`s surfaces',
                            'character`s arts' and character`s coordinates in pixels.
    """
    # characters_scale_for_render(characters_list=characters_dict)
    # Characters render:
    for character in characters_dict.values():
        character.scale()
        background.blit(character.surface,
                        character.coordinates_pixels)
    # Text canvas render:
    text_canvas = text_canvas_render(screen_surface=background)
    # text = text_canvas[0].blit()
    background.blit(text_canvas[0], text_canvas[1])
    # Background render:
    screen.blit(background, (0, 0))
    # Flip all surfaces:
    display.update()


# def characters_scale_for_render(*, characters_list: dict):
#     """
#     :param characters_list: Dictionary with 'character`s surfaces',
#                             'character`s arts' and character`s coordinates in pixels.
#     """
#     for character in characters_list.values():
#         character.scale()
