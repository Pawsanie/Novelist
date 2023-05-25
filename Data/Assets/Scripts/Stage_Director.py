from pygame import display, Surface

from .Character import characters_generator
from .Background import backgrounds_generator, Background, BackgroundMock
from .User_Interface.UI_Text_Canvas import TextCanvas
from .Dialogues import generate_dialogues, DialoguesWords
from .Universal_computing import SingletonPattern
from .Settings_Keeper import SettingsKeeper
from .Character import Character
"""
Contains stage director program code.
Stage director control scenes by class methods interfaces.
"""


class StageDirector(SingletonPattern):
    """
    Controls game scenes and assets loads.
    StageDirector used in "GamePlay_Administrator.py" for gameplay programming.
    Created in GameMaster class in Game_Master.py.
    """
    def __init__(self):
        # Arguments processing:
        self.settings_keeper: SettingsKeeper = SettingsKeeper()
        self.display_screen: display = self.settings_keeper.get_windows_settings()
        # Make background surface:
        self.background_mock: BackgroundMock = BackgroundMock()
        self.background_surface: Surface = self.background_mock.get_data()[0]
        self.background_coordinates: tuple[int, int] = self.background_mock.get_data()[1]

        """Assets loading:"""
        # Characters load:
        self.characters_dict: dict[str, Character] = characters_generator()
        # Backgrounds load:
        self.backgrounds_dict: dict[str, Background] = backgrounds_generator()
        self.location: Background | None = None

        """Make UI:"""
        # Set language:
        self.language_flag: str = self.settings_keeper.text_language
        # Text canvas:
        self.text_canvas = TextCanvas()
        self.text_canvas_surface: Surface = self.text_canvas.get()[0]
        # Text generation:
        self.text_controller = DialoguesWords(
            font_name=None,
            text_canvas=self.text_canvas_surface
        )
        self.text_dict_all: dict[str] = generate_dialogues()
        # Text Reading gameplay:
        self.text_dict_reading: dict[str] = self.text_dict_all['Reading']
        self.text_string_reading: str = ''  # Blank as default.
        self.text_speaker_reading: str = ''  # Blank as default.
        self.speech: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        self.speaker: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        # Text Choice gameplay:
        # self.text_dict_choice: dict[str] = self.text_dict_all['Choice']

    def set_scene(self, *, location: str) -> Surface.blit:
        """
        Update background Image, for scene render.

        :param location: String with background location name.
        :return: Background for scene render.
        """
        if location is not None:  # In game menu.
            scene: Background = self.backgrounds_dict.get(location)
            self.location: Background = scene
        else:
            scene = self.location

        scene.scale()
        scene_image: Surface = scene.scene_image
        # Update background surface:
        self.background_mock.set_new_image(new_image=scene_image)
        self.background_surface: Surface = self.background_mock.get_data()[0]
        self.background_surface.blit(scene_image, (0, 0))
        return self.display_screen.blit(self.background_surface, self.background_coordinates)

    def set_actor(self, *, character: str) -> Surface.blit:
        """
        :param character: String with character name.
        :return: pygame.Surface of character.
        """
        return self.characters_dict.get(character)

    def scale(self):
        """
        Render image scale.
        """
        # Scale:
        self.location.scale()
        self.text_canvas.scale()
        for character in self.characters_dict.values():
            character.scale()

    def vanishing_scene(self):
        """
        Delete all characters and background from scene.
        """
        background_data: tuple = self.background_mock.get_data()
        self.background_surface: Surface = background_data[0]
        self.background_surface.fill((0, 0, 0))
        self.background_coordinates: tuple[int, int] = background_data[1]
        for character in self.characters_dict.values():
            character.kill()
        self.text_string_reading: str = ''
        self.text_speaker_reading: str = ''

    def set_reading_words(self, *, script: dict):
        """
        Set a speaker and his words and these text colors.
        Get data from self.text_dict.

        :param script: Dict with scene words and speaker.
        """
        speaker: str = script['who']['text']
        speaker_color: str = script['who']['color']
        text: str = script['what']['text']
        text_color: str = script['what']['color']
        self.text_string_reading: str = text
        self.text_speaker_reading: str = speaker
        self.speech: tuple[Surface, tuple[int, int]] = \
            self.text_controller.make_words(
                text_string=self.text_string_reading,
                text_color=text_color,
                text_type='words'
            )
        self.speaker: tuple[Surface, tuple[int, int]] = \
            self.text_controller.make_words(
                text_string=self.text_speaker_reading,
                text_color=speaker_color,
                text_type='speaker'
            )

    def get_speech(self) -> tuple[Surface, tuple[int, int]]:
        """
        Get character speech text and coordinates in tuple[int, int].

        :return: tuple[Surface, tuple[int, int]]
        """
        return self.speech

    def get_speaker(self) -> tuple[Surface, tuple[int, int]]:
        """
        Get character speaker name text and coordinates in tuple[int, int].

        :return: tuple[Surface, tuple[int, int]]
        """
        return self.speaker

    def get_background(self) -> tuple[Surface, tuple[int, int]]:
        """
        Get tuple with background surface and background coordinates in tuple[int, int].

        :return: tuple[Surface, tuple[int, int]]
        """
        return self.background_surface, self.background_coordinates
