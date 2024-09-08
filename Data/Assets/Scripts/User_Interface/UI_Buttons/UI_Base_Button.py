from abc import ABC, abstractmethod

from pygame import Surface, mouse, font, MOUSEBUTTONUP, draw, Rect, transform
from pygame.event import Event

from ...Universal_computing.Assets_load import AssetLoader
from ...Game_objects.Background import Background
from ...Application_layer.Settings_Keeper import SettingsKeeper
from ...Render.Sprite import Sprite
from ...Render.Texture_Master import TexturesMaster
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
    # Other settings:
    _button_layer: int = 4

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
        self._button_size: tuple[int, int] = self._get_button_size()
        sprite_attributes: dict = {
            "layer": self._button_layer,
            "coordinates": self._button_coordinates,
            "name": self._button_name,
            "texture_mame": self._button_sprite_data["sprite_name"],
            "sprite_sheet_data": {
                "texture_type": "User_Interface",
                "sprite_sheet": False,
                "statick_frames": {
                    self._button_sprite_data["sprite_name"]: {}
                }
            },
            "sprite_size": self._button_size
        }
        if have_real_path is None:
            self._load_real_path_button_static_texture()
        self._button_sprite: Sprite = Sprite(**sprite_attributes)

        # Button text settings:
        self._language_flag: str = self._settings_keeper.text_language
        self._button_text_localization_dict: dict[str] | None = button_text_localization_dict
        self._button_text: str | None = button_text

        if self._button_text_localization_dict is not None:
            self._localization_button_text()
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

    def _load_real_path_button_static_texture(self):
        """
        Load texture for SaveLoad buttons.
        """
        TexturesMaster().load_static_texture_from_path(
            texture_path=self._button_sprite_data["sprite_name"],
            texture_type="User_Interface",
            asset_type="Saves"
        )

    def _cache_temporary_image(self, surface: Surface):
        """
        Used for specific button states.
        For example, mouse cursor hover.
        """
        TexturesMaster().set_temporary_texture(
            texture_type="User_Interface",
            texture_name=self._button_name,
            surface=surface
        )

    def get_coordinates(self) -> tuple[int, int]:
        """
        Get Button coordinates.
        """
        return self._button_coordinates

    def get_sprite(self) -> Sprite:
        """
        Use in InterfaceController.
        """
        TexturesMaster().devnull_temporary_texture(
            texture_type="User_Interface",
            texture_name=self._button_name
        )

        # Standard UI button:
        if self._button_text is None and self.select is False:
            return self._button_sprite

        # Surface for specific buttons:
        button_surface: Surface = transform.scale(
            TexturesMaster().get_texture(
                texture_type="User_Interface",
                texture_name=self._button_sprite._texture_id,
                animation_name=self._button_sprite.get_animation_name(),
                frame=self._button_sprite._sprite_sheet_frame
            ),
            self._button_size
        )

        # Button text scale and render:
        if self._button_text is not None:
            button_surface: Surface = self._button_text_render(button_surface)

        # Button ready to be pressed:
        if self.button_cursor_position_status() is True:
            # Mask settings:
            screen_mask: Surface = Surface(self._button_size)
            screen_mask.fill(self._button_selected_color)
            screen_mask.set_alpha(150)
            # Button render:
            button_surface.blit(
                screen_mask,
                (0, 0)
            )

        # Button selected after pressed:
        if self.select is True:
            select_frame_fatness: int = max(
                int(
                    min(
                        self._settings_keeper.screen.get_width(),
                        self._settings_keeper.screen.get_height()
                    ) / 500
                ) * 4,
                1
            )
            draw.rect(
                surface=button_surface,
                color=self._select_frame_color,
                rect=Rect(
                    0, 0,
                    self._button_size[0],
                    self._button_size[1]
                ),
                width=select_frame_fatness
            )

        self._cache_temporary_image(button_surface)
        return Sprite(
            layer=self._button_layer,
            coordinates=self._button_coordinates,
            texture_mame=self._button_name,
            name=self._button_name,
            sprite_sheet_data=self._button_sprite._sprite_sheet_data,
            sprite_size=self._button_size
        )

    def scale(self):
        """
        Scale button surface, with background context.
        """
        # Button size scale:
        self._button_size: tuple[int, int] = self._get_button_size()
        self._button_sprite.scale(
            self._button_size
        )

        # Scale coordinates:
        self._calculate_coordinates()
        self._button_sprite.set_coordinates(
            self._button_coordinates
        )

    def _button_middle_point_coordinates(self) -> tuple[int, int]:
        """
        Calculate button middle points coordinates.
        """
        screen_x: int = self._settings_keeper.screen.get_width()
        screen_y: int = self._settings_keeper.screen.get_height()

        button_middle_x: int = screen_x // 2
        button_middle_y: int = screen_y // 2

        return button_middle_x, button_middle_y

    def _background_surface_size(self) -> tuple[int, int]:
        """
        Calculate background surface size.
        """
        return self._background.get_size()

    def _localization_button_text(self):
        """
        Localization text of button if it's necessary.
        """
        if self._button_text is not None:
            self._language_flag: str = self._settings_keeper.text_language
            self._button_text: str = self._button_text_localization_dict[self._language_flag]

    def _button_text_render(self, input_surface) -> Surface:
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
        text_surface: Surface = self._set_button_font.render(
            self._button_text, True, self._text_color
        )

        # Button text coordinates:
        button_text_coordinates: tuple[int, int] = self._button_text_coordinates(text_surface)
        # Button text render:
        input_surface.blit(
            text_surface,
            button_text_coordinates
        )
        return input_surface

    def _button_text_coordinates(self, text_surface: Surface) -> tuple[int, int]:
        """
        Calculates the coordinates of the text on the button sprite.
        :param text_surface: Text Surface.
        :type text_surface: Surface
        :return: tuple[int, int]
        """
        button_sprite_width, button_sprite_height = self._button_size
        if self._text_offset_x is None and self._text_offset_y is None:
            result: tuple[int, int] = (
                (button_sprite_width // 2) - (text_surface.get_width() // 2),
                (button_sprite_height // 2) - (text_surface.get_height() // 2)
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
                 (button_sprite_width // 2)
                 - (text_surface.get_width() // 2)
                 + (
                         (button_sprite_width // 10) * text_offset_x
                 )
                ),
                int(
                    (button_sprite_height // 2)
                    - (text_surface.get_height() // 2)
                    + (
                            (button_sprite_height // 10) * text_offset_y
                    )
                )
            )
        return result

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.
        Use in InterfaceController and another button calculation.
        :return: True | False
        """
        # Mouse processing:
        cursor_position: tuple[int, int] = mouse.get_pos()
        # Button processing:
        button_x_size, button_y_size = self._button_size
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
        Use in InterfaceController.
        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()
            if button_clicked[0] is True:
                return True

    def button_clicked_status(self, event: Event) -> bool:
        """
        Check left push out mouse left button status.
        Use in InterfaceController.
        :param event: pygame.event element.
        :type event: Event
        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            if event.type == MOUSEBUTTONUP and event.button == 1:  # event.button return int of button type.
                return True

    @abstractmethod
    def _calculate_coordinates(self):
        """
        Generate coordinates for menu`s buttons.
        """
        pass

    @abstractmethod
    def _get_button_size(self) -> tuple[int, int]:
        """
        Calculate button size.
        :return: Tuple with x and y sizes of button`s surface.
        """
        pass
