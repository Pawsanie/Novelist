from pygame import font, Surface

from ..Universal_computing.Assets_load import AssetLoader
from .Background import Background
from ..Core.Settings_Keeper import SettingsKeeper
from ..User_Interface.UI_Text_Canvas import TextCanvas
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Render.Texture_Master import TexturesMaster
from ..Render.Sprite import Sprite
# Lazy import:
# from ..GamePlay.Scene_Validator import SceneValidator
"""
Contains the code for text of dialogues.
"""
font.init()


class DialoguesWords(SingletonPattern):
    """
    Control dialog scenes text and control font size.
    Load font asset and generate text coordinates.
    """
    def __init__(self, *, font_name: str | None = None):
        """
        :param font_name: String with font file name.
        """
        # Program layers settings:
        self._background_surface: Background = Background()
        self._screen: Surface = SettingsKeeper().get_window()
        self._text_canvas: TextCanvas = TextCanvas()
        self._asset_loader: AssetLoader = AssetLoader()
        self._texture_master: TexturesMaster = TexturesMaster()

        # Dialogues attributes:
        self._font_size: int = 0
        self._font_name: str = font_name
        self._used_font: font.Font | None = None
        self._set_font(font_name=font_name)
        self._font_coordinates: tuple[int, int] = (0, 0)
        self.status: bool = True

    def _set_font(self, *, font_name: str | None):
        """
        :param font_name: String with font file name.
        """
        self._font_name: str = font_name
        if self._font_name is None:
            self._used_font = font.Font(
                font.get_default_font(),
                self._font_size
            )
        else:
            self._used_font: font.Font = self._asset_loader.font_load(
                font_name=font_name,
                font_size=self._font_size
            )

    def make_words(
            self, *,
            text_string: str,
            text_color: str,
            text_type: str
    ) -> Sprite:
        """
        Make text for text canvas surface.
        :param text_string: String from StageDirector.text_dict value.
        :param text_color: String with HTML color format.
        :param text_type: String 'speaker' or 'words'
        """
        background_size: tuple[int, int] = self._background_surface.get_size()
        background_height: int = background_size[1]
        if text_type == 'speaker':
            self._font_size: int = background_height // 40
            self._font_coordinates: tuple[int, int] = self._character_speech_text_coordinates(
                text_type='name'
            )
        if text_type == 'words':
            self._font_size: int = background_height // 50
            self._font_coordinates: tuple[int, int] = self._character_speech_text_coordinates(
                text_type='speech'
            )
        self._set_font(font_name=self._font_name)
        surface: Surface = self._used_font.render(
                text_string,
                True,
                text_color
            )

        universal_texture_data: dict = {
            "texture_type": text_type,
            "texture_name": text_type,
            "animation_name": "statick_frames",
            "frame": text_type
        }
        self._texture_master.devnull_temporary_texture(
            **universal_texture_data
        )
        self._texture_master.set_temporary_texture(
            **universal_texture_data | {"surface": surface}
        )
        return Sprite(
            layer=4,
            name=text_type,
            texture_mame=text_type,
            coordinates=self._font_coordinates,
            sprite_size=surface.get_size(),
            sprite_sheet_data={
                "texture_type": text_type,
                "sprite_sheet": False,
                "statick_frames": {
                    text_type: {}
                }
            }
        )

    def _character_speech_text_coordinates(self, *, text_type: str) -> tuple[int, int]:
        """
        Generate coordinates of text for render.
        :param text_type: String: 'speech' or 'name'!
        :return: Tuple with x and y int coordinates for speech text render.
        """
        text_canvas_surface_size: tuple[int, int] = self._text_canvas.get_size()
        text_canvas_size_x, text_canvas_size_y = text_canvas_surface_size

        text_canvas_y: int = self._text_canvas.get_coordinates()[1]

        x_result: int = (
                (text_canvas_size_x // 100) * 30
                + self._background_surface.get_coordinates()[0]
        )
        if text_type == 'speech':
            y_result: int = (
                    text_canvas_y
                    + (self._font_size * 2)
                    + ( (text_canvas_size_y // 100) * 5 )
            )
            return x_result, y_result
        if text_type == 'name':
            y_result: int = (
                    text_canvas_y
                    + ( (text_canvas_size_y // 100) * 5 )
            )
            return x_result, y_result


class DialogueKeeper(SingletonPattern):
    """
    Generate and keep dialogues data for gameplay.
    """
    def __init__(self):
        self._dialogues_dict: dict = {}
        self._generate_dialogues()

    def get_dialogues_data(self) -> dict:
        """
        Get dict with dialogues.
        With keys as languages flags and json dictionary as value.
        """
        return self._dialogues_dict

    def _generate_dialogues(self):
        """
        Generate dict with dialogues.
        With keys as languages flags and json dictionary as value.
        """
        from ..GamePlay.Scene_Validator import SceneValidator
        screenplay_data: dict = SceneValidator().get_screenplay_data()
        screenplay_localization_data: tuple[dict] = AssetLoader().csv_load(
            file_name="screenplay_localization"
        )
        language_flags: tuple = tuple(
            flag
            for flag in screenplay_localization_data[0]
            if flag not in (
                "scene_id",
                "scene_type",
                "choice_id"
            )
        )

        for flag in language_flags:
            for row in screenplay_localization_data:
                self._dialogues_dict.setdefault(
                    row["scene_type"], {}
                )
                self._dialogues_dict[row["scene_type"]].setdefault(
                        flag, {}
                )
                scene_data: dict = {}
                if row["scene_type"] == "reading":
                    scene_text: list[str] = row[flag].split("::")
                    scene_data.update(
                        {
                            "who": {
                                "text": scene_text[0],
                                "color": screenplay_data[row["scene_id"]]
                                ["speaker_name_color"]
                            },
                            "what": {
                                "text": scene_text[1],
                                "color": screenplay_data[row["scene_id"]]
                                ["speech_text_color"]
                            }
                        }
                    )

                elif row["scene_type"] == "choice":
                    scene_data.update(
                        {
                            row["choice_id"]: row[flag]
                        }
                    )

                if row["scene_id"] in self._dialogues_dict[row["scene_type"]][flag]\
                        and row["scene_type"] == "choice":
                    self._dialogues_dict[row["scene_type"]][flag][row["scene_id"]]\
                        .update(scene_data)
                else:
                    self._dialogues_dict[row["scene_type"]][flag].update(
                        {
                            row["scene_id"]: scene_data
                        }
                    )
