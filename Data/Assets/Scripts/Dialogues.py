from pygame import font, Surface

from .Assets_load import json_load, font_load
from .Render import character_speech_text_coordinates
font.init()
"""
Contains the code for text of dialogues.
"""


class DialoguesWords:
    """
    Control dialog scenes text and control font size.
    Load font asset and generate text coordinates.

    :param font_name: String with font file name.
    :type font_name: str | None
    """

    def __init__(self, *, font_name: str | None, text_canvas: Surface):
        self.font_size: int = 0
        self.font_name: str = font_name
        self.text_canvas: Surface = text_canvas
        if self.font_name is None:
            self.set_font = font.Font(font.get_default_font(), self.font_size)
        else:
            self.set_font = font_load(font_name=font_name, font_size=self.font_size)
        self.font_coordinates: tuple[int, int] = (0, 0)

    def swap_font(self, *, font_name: str | None):
        """
        :param font_name: String with font file name.
        :type font_name: str | None
        """
        self.font_name: str = font_name
        if self.font_name is None:
            self.set_font = font.Font(font.get_default_font(), self.font_size)
        else:
            self.set_font = font_load(font_name=font_name, font_size=self.font_size)

    def make_words(self, *, text_string: str, text_color: str, text_type: str,
                   backgrounds_surface: Surface) -> tuple[Surface, tuple[int, int]]:
        """
        Make text for text canvas surface.

        :param text_string: String from StageDirector.text_dict value.
        :type text_string: str
        :param text_color: String with HTML color format.
        :type text_color: str
        :param text_type: String 'speaker' or 'words'
        :type text_type: str
        :param backgrounds_surface: Background pygame.Surface
        :type backgrounds_surface: Surface
        :return: tuple[pygame.Rect, tuple[int, int]]
        """
        if text_type == 'speaker':
            self.font_size: int = backgrounds_surface.get_height() // 50
            self.font_coordinates: tuple[int, int] = character_speech_text_coordinates(
                text_canvas_surface=self.text_canvas,
                font_size=None,
                text_type='name')
        if text_type == 'words':
            self.font_size: int = backgrounds_surface.get_height() // 60
            self.font_coordinates: tuple[int, int] = character_speech_text_coordinates(
                text_canvas_surface=self.text_canvas,
                font_size=self.font_size,
                text_type='speech')

        self.swap_font(font_name=self.font_name)
        text_surface: Surface = self.set_font.render(text_string, True, text_color)

        return text_surface, self.font_coordinates


def generate_dialogues():
    """
    Generate dict with dialogues.
    With keys as languages flags and json dictionary as value.
    """
    result = {}
    language_flags = (
        'eng',
        'ru'
    )
    for flag in language_flags:
        json_values = json_load(['Scripts', 'Json_data', 'Dialogues', flag])
        result.update({flag: json_values})
    return result
