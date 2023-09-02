from pygame import font, Surface

from ..Application_layer.Assets_load import json_load, font_load
from ..Universal_computing.Surface_size import surface_size
from .Background import BackgroundProxy
from ..Application_layer.Settings_Keeper import SettingsKeeper
from ..User_Interface.UI_Text_Canvas import TextCanvas
from ..Universal_computing.Pattern_Singleton import SingletonPattern
font.init()
"""
Contains the code for text of dialogues.
"""


class DialoguesWords(SingletonPattern):
    """
    Control dialog scenes text and control font size.
    Load font asset and generate text coordinates.
    """

    def __init__(self, *, font_name: str | None = None):
        """
        :param font_name: String with font file name.
        :type font_name: str | None
        """
        self.background_surface: BackgroundProxy = BackgroundProxy()
        self.screen: Surface = SettingsKeeper().screen
        self.font_size: int = 0
        self.font_name: str = font_name
        self.text_canvas: TextCanvas = TextCanvas()
        self.used_font: font.Font | None = None
        self.set_font(font_name=font_name)
        self.font_coordinates: tuple[int, int] = (0, 0)
        self.status: bool = True

    def set_font(self, *, font_name: str | None):
        """
        :param font_name: String with font file name.
        :type font_name: str | None
        """
        self.font_name: str = font_name
        if self.font_name is None:
            self.used_font = font.Font(
                font.get_default_font(),
                self.font_size
            )
        else:
            self.used_font: font.Font = font_load(
                font_name=font_name,
                font_size=self.font_size
            )

    def make_words(self, *, text_string: str, text_color: str, text_type: str) -> tuple[Surface, tuple[int, int]]:
        """
        Make text for text canvas surface.

        :param text_string: String from StageDirector.text_dict value.
        :type text_string: str
        :param text_color: String with HTML color format.
        :type text_color: str
        :param text_type: String 'speaker' or 'words'
        :type text_type: str
        :return: tuple[pygame.Rect, tuple[int, int]]
        """
        backgrounds_surface: Surface = self.background_surface.get_data()[0]
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
        text_canvas_surface_size: tuple[int, int] = surface_size(
            self.text_canvas.text_canvas_surface
        )
        text_canvas_size_x, text_canvas_size_y = text_canvas_surface_size

        text_canvas_y: int = self.text_canvas.text_canvas_coordinates[1]

        x_result: int = (
                (text_canvas_size_x // 100) * 30
                + self.background_surface.background_coordinates[0]
        )
        if text_type == 'speech':
            y_result: int = (
                    text_canvas_y
                    + (self.font_size * 2)
                    + ((text_canvas_size_y // 100) * 5)
            )
            return x_result, y_result
        if text_type == 'name':
            y_result: int = (
                    text_canvas_y
                    + ((text_canvas_size_y // 100) * 5)
            )
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
