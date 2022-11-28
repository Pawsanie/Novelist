from pygame import display, Surface, SRCALPHA
"""
Contains code for display image render.
"""


def character_speech_text_coordinates(*, text_canvas_surface: Surface, font_size: int | None, text_type: str
                                      ) -> tuple[int, int]:
    """
    Generate coordinates of text for render.

    :param text_canvas_surface: pygame.Surface with text canvas.
    :param font_size: Size of font like int ore None ('speech' must have int parameter!).
    :param text_type: String: 'speech' or 'name'!
    :return: Tuple with x and y int coordinates for speech text render.
    """
    text_canvas_surface_size: tuple[int, int] = surface_size(text_canvas_surface)
    text_canvas_size_x, text_canvas_size_y = text_canvas_surface_size
    x_result: int = (text_canvas_size_x // 100) * 15
    if text_type == 'speech':
        y_result: int = (font_size * 2) + ((text_canvas_size_y // 100) * 5)
        return x_result, y_result
    if text_type == 'name':
        y_result: int = (text_canvas_size_y // 100) * 5
        return x_result, y_result


def text_canvas_render(*, screen_surface: Surface) -> tuple[Surface, tuple[int, int]]:
    """
    Generate text canvas surface with coordinates.

    :param screen_surface: pygame.Surface with background.
    :return: pygame.Surface with text_canvas coordinates.
    """
    # Render text canvas:
    screen_size: tuple[int, int] = surface_size(screen_surface)
    text_canvas: Surface = Surface((screen_size[0], screen_size[1] // 5), SRCALPHA)
    # text_canvas.set_alpha(128)
    # Text canvas coordinates:
    canvas_coordinates: tuple[int, int] = (0, screen_size[1] - surface_size(text_canvas)[1])
    return text_canvas, canvas_coordinates


def meddle_point_for_character_render(*, screen_surface: Surface, character_surface: Surface) -> list[int]:
    """
    Calculation middle coordinates for character render.

    :param screen_surface: pygame.Surface of background.
    :param character_surface: pygame.Surface of character.
    :return: List with coordinates of meddle point for character render.
    """
    screen_size: tuple[int, int] = surface_size(screen_surface)
    sprite_size: tuple[int, int] = surface_size(character_surface)
    result = [(screen_size[0] // 2) - (sprite_size[0] // 2),
              (screen_size[1] - sprite_size[1])]
    return result


def surface_size(interested_surface: Surface) -> [int, int]:
    """
    Calculation surface size.

    :param interested_surface: pygame.Surface object.
    :return: Surface size with 2 init`s.
    """
    character_sprite_size_x: int = interested_surface.get_width()
    character_sprite_size_y: int = interested_surface.get_height()
    return character_sprite_size_x, character_sprite_size_y


def background_sprite_data(*, display_surface: Surface) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Make size of background and it coordinates.

    :param display_surface: display.set_mode surface.
    :return: Tuple with x and y sizes for background image.
             These sizes depends display size.
             And tuple with coordinates of rendering.
    """
    def scale_y(display_ratio) -> int:
        """
        Calculate background Y size.
        :return: int
        """
        size_x, size_y = display_size
        if size_x > size_y:
            while display_ratio != _16x9:
                if display_ratio > _16x9:
                    size_y += 1
                    display_ratio = int(background_size_x / size_y * 100)
                else:
                    size_y -= 1
                    display_ratio = int(background_size_x / size_y * 100)
        else:
            while display_ratio != _16x9:
                size_y -= 1
                display_ratio = int(background_size_x / size_y * 100)
        return size_y

    # Display resolution:
    # _5x4: int = int(5 / 4 * 100)  # Dinosaurs
    _16x9: int = int(16 / 9 * 100)  # Movie, game, text and art.
    # _21x9: int = int(21 / 9 * 100)  # Video montage and code.
    # _32x9: int = int(32 / 9 * 100)  # 27 inches or more.

    display_size: tuple[int, int] = surface_size(display_surface)
    ratio_of_sizes = int(display_size[0] / display_size[1] * 100)
    if ratio_of_sizes == _16x9:
        return display_size, (0, 0)
    else:
        background_size_x, background_size_y = display_size
        display_aspect_ratio = int(background_size_x / background_size_y * 100)
        # Scale Y size!:
        if background_size_x // 2 <= background_size_y:
            background_size_y = scale_y(display_aspect_ratio)
        # Scale X size!:
        else:
            while background_size_x // 2 > background_size_y:
                background_size_x -= 1
            background_size_y = scale_y(int(background_size_x / background_size_y * 100))
        # Result:
        background_surface_size = (background_size_x, background_size_y)
        render_coordinates = ((display_size[0] // 2) - (background_size_x // 2),
                              (display_size[1] // 2) - (background_size_y // 2))
        # display.set_mode(display_size)
        return background_surface_size, render_coordinates


def character_sprite_size(*, background_surface: Surface, character_surface: Surface) -> tuple[int, int]:
    """
    Calculation character surface size.
    Formula: Character_Sprite[x] + Background_and_Character_Sprite[x]_difference percent:
    coefficient = x / 100 ->
    percent_difference = Character_Sprite / Background * 100 ->
    difference = coefficient * (100 - percent_difference) ->
    x = Character_Sprite[size] + difference
    Or: Character_Sprite[x] - Background_and_Character_Sprite[x]_difference percent:
    percent_difference = Background / Character_Sprite * 100 ->
    x = Character_Sprite[size] * (1 - (100 - percent_difference) / 100)
    Formula: Character_Sprite[Y]:
    Character_Sprite[Y] = Background[Y]

    :param background_surface: pygame.Surface of background.
    :param character_surface: pygame.Surface of character.
    :return: Tuple with x and y sizes for character`s images.
             These sizes depends of main frame size.
    """
    result_size_x, result_size_y = (0, 0)
    screen_size: tuple[int, int] = surface_size(background_surface)
    sprite_size: tuple[int, int] = surface_size(character_surface)

    if sprite_size[1] != screen_size[1]:
        result_size_y: int = screen_size[1]
        if sprite_size[1] < screen_size[1]:
            percent_size_sprite_difference = int(sprite_size[1] / screen_size[1] * 100)
            coefficient: int | float = sprite_size[0] / 100
            percent_integer: int | float = coefficient * (100 - percent_size_sprite_difference)
            result_size_x = int(sprite_size[0] + percent_integer)
        if sprite_size[1] > screen_size[1]:
            percent_size_sprite_difference = int(screen_size[1] / sprite_size[1] * 100)
            result_size_x = int(sprite_size[0] * (1 - ((100 - percent_size_sprite_difference) / 100)))
    else:
        return sprite_size

    return result_size_x, result_size_y


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

    if place_flag == 'settings_menu':
        # X:
        # Y:
        ...

    if place_flag == 'start_menu':
        # X:
        # Y:
        ...

    if place_flag == 'save_menu':
        # X:
        # Y:
        ...

    if place_flag == 'load_menu':
        # X:
        # Y:
        ...

    if place_flag == 'exit_menu':
        # X:
        # Y:
        ...

    if place_flag == 'change_settings':
        # X:
        # Y:
        ...
    return x_size, y_size


class Render:
    """
    Render image on display.

    :param screen: Display surface for image render.
    :type screen: pygame.Surface
    :param interface_controller: InterfaceController for access to user interface.
    :type interface_controller: InterfaceController
    :param stage_director: StageDirector for access to scenes data.
    :type stage_director: StageDirector
    """
    def __init__(self, *, screen: Surface, interface_controller, stage_director):
        """
        :param screen: Display surface for image render.
        :type screen: pygame.Surface
        :param interface_controller: InterfaceController for access to user interface.
        :type interface_controller: InterfaceController
        :param stage_director: StageDirector for access to scenes data.
        :type stage_director: StageDirector
        """
        self.screen: Surface = screen
        self.stage_director = stage_director
        self.interface_controller = interface_controller

    def screen_clear(self):
        """
        Clear scene before scene render.
        """
        self.screen.fill((0, 0, 0))

    def gameplay_text_render(self):
        # Get data from StageDirector:
        background: Surface = self.stage_director.get_background()[0]
        text_canvas: tuple[Surface, tuple[int, int]] = self.stage_director.text_canvas.generator()  # Remake
        speaker: tuple[Surface, tuple[int, int]] = self.stage_director.speaker
        speech: tuple[Surface, tuple[int, int]] = self.stage_director.speech
        # Render:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            text_canvas[0].blit(speaker[0], speaker[1])
            text_canvas[0].blit(speech[0], speech[1])
            background.blit(text_canvas[0], text_canvas[1])

    def ui_buttons_render(self):
        """
        User interface render.
        """
        # Get data from StageDirector and InterfaceController:
        background: Surface = self.stage_director.get_background()[0]
        get_ui_buttons_dict = self.interface_controller.get_ui_buttons_dict()
        # Render:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            for button_key in get_ui_buttons_dict:
                button = get_ui_buttons_dict[button_key]
                button_surface, button_coordinates = button.generator()
                background.blit(button_surface, button_coordinates)

    def characters_render(self):
        """
        Scene characters render.
        """
        # Get data from StageDirector:
        background = self.stage_director.get_background()[0]
        characters_dict = self.stage_director.characters_dict
        # Render:
        for character in characters_dict.values():
            background.blit(character.surface,
                            character.coordinates_pixels)

    def background_render(self):
        """
        Background render.
        """
        # Get data from StageDirector:
        get_background_data: tuple[Surface, tuple[int, int]] = self.stage_director.get_background()
        background, background_coordinates = get_background_data
        # Render:
        self.screen.blit(background, background_coordinates)

    def gameplay_read_scene(self):
        """
        Render reading scene.
        """
        # Clear old screen for not 16x9 display render:
        self.screen_clear()
        # Characters render:
        self.characters_render()
        # Text render:
        self.gameplay_text_render()
        # Gameplay ui render:
        self.ui_buttons_render()
        # Background render:
        self.background_render()
        # Flip all surfaces:
        display.update()

    def image_render(self):
        """
        Display image render.
        """
        if self.interface_controller.gameplay_interface_status is True:
            self.gameplay_read_scene()
        if self.interface_controller.game_menu_status is True:
            self.game_menu()
        if self.interface_controller.settings_menu_status is True:
            ...
        if self.interface_controller.exit_menu_status is True:
            ...
        if self.interface_controller.load_menu_status is True:
            ...
        if self.interface_controller.save_menu_status is True:
            ...
        if self.interface_controller.settings_status_menu_status is True:
            ...
        if self.interface_controller.start_menu_status is True:
            ...

    def game_menu(self):
        """
        Render game menu scene.
        """
        # Clear old screen for not 16x9 display render:
        self.screen_clear()
        # Characters render:
        self.characters_render()
        # Gameplay ui render:
        self.ui_buttons_render()
        # Background render:
        self.background_render()
        # Flip all surfaces:
        display.update()
