from .UI_Base_Button import BaseButton
"""
Contents code for user interface 'gameplay reading' buttons.
"""


class GamePlayReadingButton(BaseButton):
    """
    Generate interface button surface and it`s coordinates for render.
    GamePlay reading buttons.
    """
    def __init__(
            self, *,
            button_name: str,
            button_text: str | None = None,
            button_image_data: dict[str, int],
            button_text_localization_dict: dict[str] | None = None,
            have_real_path: bool = False,
            text_offset_x: int | float | None = None,
            text_offset_y: int | float | None = None
    ):
        """
        :param button_name: String with button image file name.
        :param button_text: String with text of button.
                            None by default.
        :param button_image_data: Nested dictionary with button name as key and dictionary with button type,
                                  index order position and sprite name as values.
        :param button_text_localization_dict: Dictionary with language flags as keys and localization text as values.
                                              If this parameter is set to 'None', no localization occurs.
                                              None by default.
        :param have_real_path: If this flag is True button_image_data['sprite_name'] will be real path to file.
                               Is not file name.
        :param text_offset_x: Offset of the text inside the button, along the X axis.
                              If set to None, then there will be no offset.
                              The factor to multiply by the parameter is 1/10 of the button size.
                              left -0 | Right +0
                              None by default.
        :param text_offset_y: Offset of the text inside the button, along the Y axis.
                              If set to None, then there will be no offset.
                              The factor to multiply by the parameter is 1/10 of the button size.
                              Up -0 | Down +0
                              None by default.
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

    def _calculate_coordinates(self):
        """
        Coordinates for reading gameplay buttons.
        """
        place_flag: int = self._button_sprite_data['index_number']
        button_middle_x, button_middle_y = self._button_middle_point_coordinates()
        background_y = self._background_surface_size()[1]

        # X:
        button_coordinates_x: int = (
                button_middle_x
                - (self._button_size[0] // 2)
                + (self._button_size[0] * place_flag)
                )
        # Y:
        button_coordinates_y: int = (
                button_middle_y
                + (background_y // 2)
                - self._button_size[1]
        )
        # Result:
        self._button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def _get_button_size(self) -> tuple[int, int]:
        """
        Calculate button size.
        :return: Tuple with x and y sizes of button`s surface.
        """
        background_surface_size: tuple[int, int] = self._background.get_size()
        background_size_x, background_size_y = background_surface_size

        side_of_the_square: int = int(background_size_y / 100 * 4.17)
        x_size, y_size = side_of_the_square, side_of_the_square

        return x_size, y_size
