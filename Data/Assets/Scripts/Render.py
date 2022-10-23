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


def character_sprite_size(*, screen_surface: Surface, character_surface: Surface) -> tuple[int]:
    """
    Calculation character surface size.
    Formula: Character_Sprite[x] + 85%_Background_and_Character_Sprite[x]_difference percent:
    x = Background * 85% / 100 ->
    x = Character_Sprite / x * 100 ->
    x = Character_Sprite * (1 + x / 100)
    Or Character_Sprite - 90%_Background_and_Character_Sprite[x]_difference percent:
    ... ->
    x = Character_Sprite * (1 - (x-90) / 100)
    :param screen_surface: pygame.Surface of background.
    :param character_surface: pygame.Surface of character.
    :return: Tuple with x and y sizes for character`s images.
             These sizes depends of main frame size.
    """
    result = []
    screen_size = surface_size(screen_surface)
    sprite_size = surface_size(character_surface)
    for x, y in zip(screen_size, sprite_size):
        # 85% from screen:
        real_screen_size_percent = int(x * 85 / 100)
        # Percent sprite from screen:
        real_size_sprite_difference = int(y / real_screen_size_percent * 100)
        # Result calculation:
        if y < real_screen_size_percent:
            result_size = int(y * (1 + (real_size_sprite_difference / 100)))
            result.append(result_size)
        else:
            result_size = int(y * (1 - ((real_size_sprite_difference - 90) / 100)))
            result.append(result_size)
    return tuple(result)


def render(*, screen: Surface, background: Surface, characters_list: dict):
    """
    Render image on display.
    :param screen: Display.
    :param background: pygame.Surface with background.
    :param characters_list: Dictionary with 'character`s surfaces',
                            'character`s arts' and character`s coordinates in pixels.
    """
    # Characters render:
    print(characters_list)
    for character in characters_list.values():
        background.blit(character.get('surface'),
                        tuple(character.get('coordinates_pixels')))
    # Text canvas render:
    text_canvas = text_canvas_render(screen_surface=background)
    background.blit(text_canvas[0], text_canvas[1])
    # Background render:
    screen.blit(background, (0, 0))
    # Flip all surfaces:
    display.update()
