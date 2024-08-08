from .UI_Base_Button import BaseButton
"""
Contents code for user interface 'Yes | No' buttons.
"""


class YesNoButton(BaseButton):
    """
    Generate interface button surface and it`s coordinates for render.
    Yes | No buttons.
    """
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
        super().__init__(
            button_name=button_name,
            button_text=button_text,
            button_image_data=button_image_data,
            button_text_localization_dict=button_text_localization_dict,
            have_real_path=have_real_path,
            text_offset_x=text_offset_x,
            text_offset_y=text_offset_y
        )

    def coordinates(self):
        """
        Generate coordinates for exit menu and settings status menu buttons.
        """
        place_flag: int = self.button_image_data['index_number']
        button_middle_x, button_middle_y = self.button_middle_point_coordinates()
        background_y: int = self.background_surface_size()[1]

        # X:
        button_coordinates_x: int = int(
            button_middle_x
            - (self.button_size[0] // 2)
            + (self.button_size[0] * place_flag)
        )
        # Y:
        button_coordinates_y: int = (
                button_middle_y
                + (background_y // 4)
        )
        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def get_button_size(self) -> tuple[int, int]:
        """
        Calculate button size.

        :return: Tuple with x and y sizes of button`s surface.
        """
        background_surface_size: tuple[int, int] = self.background.get_size()
        background_size_x, background_size_y = background_surface_size

        # X:
        x_size: int = int(background_size_x / 100 * 15)
        # Y:
        y_size: int = int(background_size_y / 100 * 10)
        return x_size, y_size
