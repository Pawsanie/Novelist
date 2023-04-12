from pygame import font, Surface

from .Assets_load import json_load, font_load
from .Universal_computing import surface_size
font.init()
"""
Contains the code for text of dialogues.
"""


class DialoguesWords:
    """
    Control dialog scenes text and control font size.
    Load font asset and generate text coordinates.
    """

    def __init__(self, *, font_name: str | None, text_canvas: Surface):
        """
        :param font_name: String with font file name.
        :type font_name: str | None
        """
        self.font_size: int = 0
        self.font_name: str = font_name
        self.text_canvas: Surface = text_canvas
        self.used_font: font.Font | None = None
        self.set_font(font_name=font_name)
        self.font_coordinates: tuple[int, int] = (0, 0)

    def set_font(self, *, font_name: str | None):
        """
        :param font_name: String with font file name.
        :type font_name: str | None
        """
        self.font_name: str = font_name
        if self.font_name is None:
            self.used_font = font.Font(
                font.get_default_font(),
                self.font_size)
        else:
            self.used_font: font.Font = font_load(
                font_name=font_name,
                font_size=self.font_size)

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
            self.font_size: int = backgrounds_surface.get_height() // 40
            self.font_coordinates: tuple[int, int] = self.character_speech_text_coordinates(
                text_type='name'
            )
        if text_type == 'words':
            self.font_size: int = backgrounds_surface.get_height() // 50
            self.font_coordinates: tuple[int, int] = self.character_speech_text_coordinates(
                text_type='speech'
            )
        self.set_font(font_name=self.font_name)
        text_surface: Surface = self.used_font.render(text_string, True, text_color)

        return text_surface, self.font_coordinates

    def character_speech_text_coordinates(self, *, text_type: str) -> tuple[int, int]:
        """
        Generate coordinates of text for render.

        :param text_type: String: 'speech' or 'name'!
        :return: Tuple with x and y int coordinates for speech text render.
        """
        text_canvas_surface_size: tuple[int, int] = surface_size(self.text_canvas)
        text_canvas_size_x, text_canvas_size_y = text_canvas_surface_size
        x_result: int = (text_canvas_size_x // 100) * 15
        if text_type == 'speech':
            # x_result: int = (text_canvas_size_x // 100) * 15
            y_result: int = (self.font_size * 2) + ((text_canvas_size_y // 100) * 5)
            return x_result, y_result
        if text_type == 'name':
            # x_result: int = (text_canvas_size_x // 100) * 30
            y_result: int = (text_canvas_size_y // 100) * 5
            return x_result, y_result


def generate_dialogues():
    """
    Generate dict with dialogues.
    With keys as languages flags and json dictionary as value.
    """
    result: dict = {}
    language_flags: tuple = (json_load(
        [
            'Scripts',
            'Json_data',
            'Dialogues',
            'dialogues_localizations_data'
        ]
    )['language_flags'])

    for flag in language_flags:
        for dialogs_type in ['Reading', 'Choice']:
            json_values: dict = json_load(
                [
                    'Scripts',
                    'Json_data',
                    'Dialogues',
                    dialogs_type,
                    flag
                ]
            )
            result.setdefault(dialogs_type, {flag: json_values})
    return result
