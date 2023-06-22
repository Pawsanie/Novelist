from pygame import display, Surface

from ..Game_objects.Character import characters_generator
from ..Game_objects.Background import backgrounds_generator, Background, BackgroundMock
from ..User_Interface.UI_Text_Canvas import TextCanvas
from ..Game_objects.Dialogues import generate_dialogues, DialoguesWords
from ..Universal_computing import SingletonPattern
from .Settings_Keeper import SettingsKeeper
from ..Game_objects.Character import Character
from ..Render.Sprite import Sprite
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
        self.text_canvas: TextCanvas = TextCanvas()
        self.text_canvas_surface: Surface = self.text_canvas.text_canvas_surface
        # Text generation:
        self.text_controller = DialoguesWords()
        self.text_dict_all: dict[str] = generate_dialogues()
        # Text Reading gameplay:
        self.text_dict_reading: dict[str] = self.text_dict_all['Reading']
        self.text_string_reading: str = ''  # Blank as default.
        self.text_speaker_reading: str = ''  # Blank as default.
        self.speech: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        self.speaker: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        # Text Choice gameplay:
        self.scene_name: str = ''
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

    def set_actor(self, *, character: str) -> Surface.blit:
        """
        :param character: String with character name.
        :return: pygame.Surface of character.
        """
        self.characters_dict.get(character).hidden = False
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

        self.text_canvas.status = False
        self.text_controller.status = False

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
        self.text_canvas.status = True
        self.text_controller.status = True

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

    def generate_characters_batch(self):
        """
        Generate batch with characters sprites for display image render.

        :return: Batch
        """
        from ..Render.Batch import Batch
        result: Batch = Batch()

        for character in self.characters_dict.values():
            if character.hidden is False:
                character_coordinates: tuple[int, int] = (
                    character.coordinates_pixels[0],
                    character.coordinates_pixels[1]
                )
                result.append(
                    Sprite(
                        image=character.surface,
                        layer=2,
                        coordinates=character_coordinates,
                    )
                )

        return result

    def generate_background_batch(self):
        """
        Generate batch with background sprite for display image render.

        :return: Batch
        """
        from ..Render.Batch import Batch
        result: Batch = Batch()
        result.append(
            Sprite(
                image=self.background_surface,
                layer=1,
                coordinates=self.background_coordinates,
            )
        )
        return result

    def generate_speech(self):
        """
        Generate batch with speech text sprites for display image render.

        :return: Batch
        """
        from ..Render.Batch import Batch
        result: Batch = Batch()

        # Text canvas:
        if self.text_canvas.status is True:
            result.append(
                Sprite(
                    image=self.text_canvas.text_canvas_surface,
                    layer=3,
                    coordinates=self.text_canvas.text_canvas_coordinates,
                )
            )
        if self.text_controller.status is True:
            # Speech:
            result.append(
                Sprite(
                    image=self.speech[0],
                    layer=4,
                    coordinates=self.speech[1],
                )
            )
            # Speaker:
            result.append(
                Sprite(
                    image=self.speaker[0],
                    layer=4,
                    coordinates=self.speaker[1],
                )
            )
        return result
