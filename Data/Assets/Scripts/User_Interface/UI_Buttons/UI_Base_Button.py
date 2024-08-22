from abc import ABC, abstractmethod
from os.path import sep

from pygame import Surface, SRCALPHA, transform, mouse, font, MOUSEBUTTONUP, draw, Rect

from ...Universal_computing.Assets_load import AssetLoader
from ...Universal_computing.Surface_size import surface_size
from ...Game_objects.Background import Background
from ...Application_layer.Settings_Keeper import SettingsKeeper
from ...Render.Sprite import Sprite
"""
Contents code for user interface buttons.
Path of code of user interface buttons in 'UI_buttons_calculations.py' file...
"""


class BaseButton(ABC):
    """
    Generate interface button surface and coordinates for render.
    Instances are created from button_generator function by InterfaceController class.
    """
    # Tuple with RBG for button select render:
    _button_selected_color: tuple[int] = (100, 0, 0)
    _select_frame_color: tuple[int] = (48, 213, 200)

    def __init__(self, *, button_name: str, button_text: str | None = None, button_image_data: dict[str, int],
                 button_text_localization_dict: dict[str] | None = None, have_real_path: bool = False,
                 text_offset_x: int | float | None = None, text_offset_y: int | float | None = None):
        """
        :param button_name: String with button image file name.
        :type button_name: str
        :param button_text: String with text of button.
                            None by default.
        :type button_text: str | None
        :param button_image_data: Nested dictionary with button name as key and dictionary with button type,
                                  index order position and sprite name as values.
        :type button_image_data: dict[str, dict[str, int]]
        :param button_text_localization_dict: Dictionary with language flags as keys and localization text as values.
                                              If this parameter is set to 'None', no localization occurs.
                                              None by default.
        :type button_text_localization_dict: dict[str] | None
        :param have_real_path: If this flag is True button_image_data['sprite_name'] will be real path to file.
                               Is not file name.
        :type have_real_path: bool
        :param text_offset_x: Offset of the text inside the button, along the X axis.
                              If set to None, then there will be no offset.
                              The factor to multiply by the parameter is 1/10 of the button size.
                              left -0 | Right +0
                              None by default.
        :type text_offset_x: int | float | None
        :param text_offset_y: Offset of the text inside the button, along the Y axis.
                              If set to None, then there will be no offset.
                              The factor to multiply by the parameter is 1/10 of the button size.
                              Up -0 | Down +0
                              None by default.
        :type text_offset_y: int | float | None
        """
        # Program layers settings:
        self._assets_loader: AssetLoader = AssetLoader()
        self._settings_keeper: SettingsKeeper = SettingsKeeper()

        # Game scene objects settings:
        self._background: Background = Background()

        # Button settings:
        self._button_name: str = button_name
        self.select: bool = False

        # Button Sprite:
        self._button_sprite_data: dict[str | int] = button_image_data
        self._button_coordinates: tuple[int, int] = (0, 0)
        self.button_size: tuple[int, int] = self.get_button_size()

        if have_real_path is False:
            self.button_sprite_standard: Surface = self._assets_loader.image_load(
                art_name=str(self._button_sprite_data['sprite_name']),
                asset_type='User_Interface',
                file_catalog='Buttons'
            )
        else:  # TODO: Simplify this block...
            self.button_sprite_standard: Surface = self._assets_loader.image_load(
                art_name=str(self._button_sprite_data['sprite_name']),
                asset_type=str(self._button_sprite_data['sprite_name']).split(sep)[-3],
                art_name_is_path=True

            )
        # self.button_sprite: Sprite = Sprite(
        #     layer=,
        #     coordinates=
        # )

        # Button text settings:
        self._language_flag: str = self._settings_keeper.text_language
        self._button_text_localization_dict: dict[str] | None = button_text_localization_dict

        if self._button_text_localization_dict is not None:
            self._localization_button_text()
        self._button_text: str | None = button_text
        self._text_offset_x: int | float = text_offset_x
        self._text_offset_y: int | float = text_offset_y

        if self._button_text is not None:
            self._font_size: int = 0
            self._text_color: str = str(self._button_sprite_data['color'])
            if self._button_sprite_data['font'] is not None:
                self._font_name: str = str(self._button_sprite_data['font'])
                self._set_button_font: font.Font = self._assets_loader.font_load(
                    font_name=self._font_name,
                    font_size=self._font_size
                )
            else:
                self._font_name: None = None
                self._set_button_font: font.Font = font.Font(
                    font.get_default_font(),
                    self._font_size
                )

    # self.button_surface: Surface = Surface(self.button_size, SRCALPHA)
    # Button image render:
    # self.button_sprite: Surface = transform.scale(self.button_sprite, self.button_size)
    # self.button_surface.blit(self.button_sprite, (0, 0))

    def get_coordinates(self) -> tuple[int, int]:
        """
        Get Button coordinates.
        """
        return self._button_coordinates

    def generator(self) -> tuple[Surface, tuple[int, int]]:
        """
        Generate button surface and coordinates for render.
        """
        return self.button_surface, self._button_coordinates

    def scale(self):
        """
        Scale button surface, with background context.
        """
        # Arg parse:
        # background_surface: Surface = self.background.get_data()[0]
        select_frame_fatness: int = max(
            int(
                min(
                    self._settings_keeper.screen.get_width(),
                    self._settings_keeper.screen.get_height()
                    ) / 500
                ) * 4,
            1
        )

        # Devnull button_surface for new render:
        self.button_surface = Surface((0, 0), SRCALPHA)

        # Button size scale:
        self.button_sprite: Surface = self.button_sprite_standard
        self.button_size: tuple[int, int] = self.get_button_size()
        self.button_sprite: Surface = transform.scale(self.button_sprite, self.button_size)
        self.button_surface: Surface = transform.scale(self.button_surface, self.button_size)

        # Scale coordinates:
        self.coordinates()

        # Button text scale and render:
        if self._button_text is not None:
            self.button_text_render()

        # Default button render:
        if self.button_cursor_position_status() is False:
            self.button_surface.blit(self.button_sprite, (0, 0))
        # Button ready to be pressed:
        else:
            # Mask settings:
            screen_mask: Surface = Surface(
                [self.button_surface.get_width(), self.button_surface.get_height()]
            )
            screen_mask.fill(self._button_selected_color)
            screen_mask.set_alpha(150)
            # Button render:
            self.button_surface.blit(self.button_sprite, (0, 0))
            self.button_surface.blit(screen_mask, (0, 0))
        if self.select is True:
            draw.rect(
                surface=self.button_surface,
                color=self._select_frame_color,
                rect=Rect(
                    0, 0,
                    self.button_size[0],
                    self.button_size[1]
                ),
                width=select_frame_fatness
            )

    def button_middle_point_coordinates(self) -> tuple[int, int]:
        """
        Calculate button middle points coordinates.
        """
        screen_x = self._settings_keeper.screen.get_width()
        screen_y = self._settings_keeper.screen.get_height()

        button_middle_x: int = screen_x // 2
        button_middle_y: int = screen_y // 2

        return button_middle_x, button_middle_y

    def background_surface_size(self) -> list[int, int]:
        """
        Calculate background surface size.
        """
        return list(self._background.get_size())

    def _localization_button_text(self):
        """
        Localization text of button if it's necessary.
        """
        if self._button_text is not None:
            self._language_flag: str = self._settings_keeper.text_language
            self._button_text: str = self._button_text_localization_dict[self._language_flag]

    def button_text_render(self):
        """
        Generate text on button if it's necessary.
        """
        # Localization button text:
        if self._button_text_localization_dict is not None:
            self._localization_button_text()

        self._font_size: int = self._background.get_size()[1] // 50

        # Font reload for size scale:
        if self._font_name is None:
            self._set_button_font: font.Font = font.Font(
                font.get_default_font(),
                self._font_size
            )
        else:
            self._set_button_font: font.Font = self._assets_loader.font_load(
                font_name=self._font_name,
                font_size=self._font_size
            )
        text_surface: Surface = self._set_button_font.render(self._button_text, True, self._text_color)

        # Button text coordinates:
        button_text_coordinates: tuple[int, int] = self.button_text_coordinates(text_surface)
        # Button text render:
        self.button_sprite.blit(text_surface, button_text_coordinates)

    def button_text_coordinates(self, text_surface: Surface) -> tuple[int, int]:
        """
        Calculates the coordinates of the text on the button sprite.
        :param text_surface: Text Surface.
        :type text_surface: Surface
        :return: tuple[int, int]
        """
        if self._text_offset_x is None and self._text_offset_y is None:
            result: tuple[int, int] = (
                (self.button_surface.get_width() // 2) - (text_surface.get_width() // 2),
                (self.button_surface.get_height() // 2) - (text_surface.get_height() // 2)
            )
        else:
            if self._text_offset_x is None:
                text_offset_x: int = 0
            else:
                text_offset_x: int = self._text_offset_x
            if self._text_offset_y is None:
                text_offset_y: int = 0
            else:
                text_offset_y: int = self._text_offset_y

            result: tuple[int, int] = (
                int(
                 (self.button_surface.get_width() // 2)
                 - (text_surface.get_width() // 2)
                 + ((self.button_surface.get_width() // 10) * text_offset_x)
                ),
                int(
                    (self.button_surface.get_height() // 2)
                    - (text_surface.get_height() // 2)
                    + ((self.button_surface.get_height() // 10) * text_offset_y)
                )
            )
        return result

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.
        :return: True | False
        """
        # Mouse processing:
        cursor_position: tuple[int, int] = mouse.get_pos()
        # Button processing:
        button_x_size, button_y_size = surface_size(self.button_surface)
        button_coordinates_x, button_coordinates_y = self._button_coordinates

        # Drawing a button while hovering over:
        if button_coordinates_x < cursor_position[0] \
                < button_coordinates_x + button_x_size \
                and button_coordinates_y < cursor_position[1] \
                < button_coordinates_y + button_y_size:
            return True
        # Default Button Rendering:
        else:
            return False

    def button_click_hold(self) -> bool:
        """
        Check left click of mouse to button status.
        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()
            if button_clicked[0] is True:
                return True

    def button_clicked_status(self, event) -> bool:
        """
        Check left push out mouse left button status.
        :param event: pygame.event element.
        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            if event.type == MOUSEBUTTONUP and event.button == 1:  # event.button return int of button type.
                return True

    @abstractmethod
    def coordinates(self):
        """
        Generate coordinates for menu`s buttons.
        """
        pass

    @abstractmethod
    def get_button_size(self) -> tuple[int, int]:
        """
        Calculate button size.
        :return: Tuple with x and y sizes of button`s surface.
        """
        pass
