from pygame import Surface

from ..Game_objects.Character import characters_generator
from ..Game_objects.Background import Background
from ..User_Interface.UI_Text_Canvas import TextCanvas
from ..Game_objects.Dialogues import DialogueKeeper, DialoguesWords
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Settings_Keeper import SettingsKeeper
from ..Game_objects.Character import Character
from ..Render.Sprite import Sprite
from ..Application_layer.Sound_Director import SoundDirector
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
        # Program layers settings:
        self._settings_keeper: SettingsKeeper = SettingsKeeper()
        self._sound_director: SoundDirector = SoundDirector()

        # Game scene objects settings:
        self._background: Background = Background()
        self._characters_collection: dict[str, Character] = characters_generator()
        self._location: str | None = None

        # Text Reading gameplay settings:
        self.current_language: str = self._settings_keeper.text_language
        self._text_canvas: TextCanvas = TextCanvas()
        self._dialog_controller: DialoguesWords = DialoguesWords()
        self._text_dialogues_data: dict[str] = DialogueKeeper().get_dialogues_data()

        # Text Reading gameplay:
        self._text_reading_dialogues_gameplay_data: dict[str] = self._text_dialogues_data['reading']
        self.text_string_reading: str = ''  # Blank as default.
        self.text_speaker_reading: str = ''  # Blank as default.
        self.speech: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        self.speaker: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        self.text_dict_reading_cash: dict[str] = {}

    def set_scene(self, *, location: str) -> Surface.blit:
        """
        Update background Image, for scene render.
        Use in StateMachine and Self.
        :param location: String with background location name.
        :return: Background for scene render.
        """
        if location is not None:  # In game menu.
            self._background.set_background(location)

    def scale(self):
        """
        Render image scale.
        """
        # Scale:
        self._background.scale()
        self._text_canvas.scale()
        for character in self._characters_collection.values():
            character.scale()

        # Set words again (cant be scaled):
        if self._dialog_controller.status is True:
            self.set_reading_words(script=self.text_dict_reading_cash)

    def vanishing_scene(self):
        """
        Delete all characters and background from scene.
        """
        self._background.devnull()
        for character in self._characters_collection.values():
            character.kill()

        self._text_canvas.status = False
        self._dialog_controller.status = False

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

        self.text_dict_reading_cash: dict[str] = script

        # TODO: Refactor?:
        self._text_canvas.status = True
        self._dialog_controller.status = True

        self.speech: tuple[Surface, tuple[int, int]] = \
            self._dialog_controller.make_words(
                text_string=self.text_string_reading,
                text_color=text_color,
                text_type='words'
            )
        self.speaker: tuple[Surface, tuple[int, int]] = \
            self._dialog_controller.make_words(
                text_string=self.text_speaker_reading,
                text_color=speaker_color,
                text_type='speaker'
            )

    def generate_characters_batch(self):
        """
        Generate batch with characters sprites for display image render.
        Call from Render class.
        :return: Batch
        """
        from ..Render.Batch import Batch
        result: Batch = Batch()

        for character in self._characters_collection.values():
            if character.hidden is False:
                result.append(character.get_sprite())

        return result

    def generate_background_batch(self):
        """
        Generate batch with background sprite for display image render.
        Call from Render class.
        :return: Batch
        """
        from ..Render.Batch import Batch
        result: Batch = Batch()
        result.append(
            self._background.get_sprite()
        )
        return result

    def generate_speech(self):
        """
        Generate batch with speech text sprites for display image render.
        Call from Render class.
        :return: Batch
        """
        from ..Render.Batch import Batch
        result: Batch = Batch()

        # # Text canvas:
        # if self._text_canvas.status is True:
        #     result.append(
        #         Sprite(
        #             image=self._text_canvas.text_canvas_surface,
        #             layer=3,
        #             coordinates=self._text_canvas.text_canvas_coordinates,
        #         )
        #     )
        # if self._dialog_controller.status is True:
        #     # Speech:
        #     result.append(
        #         Sprite(
        #             image=self.speech[0],
        #             layer=4,
        #             coordinates=self.speech[1],
        #         )
        #     )
        #     # Speaker:
        #     result.append(
        #         Sprite(
        #             image=self.speaker[0],
        #             layer=4,
        #             coordinates=self.speaker[1],
        #         )
        #     )
        return result

    def build_a_scene(self, scene_data: dict):
        """
        Call from SceneValidator.
        """
        self.vanishing_scene()

        # Set a new background:
        self.set_scene(
            location=scene_data['background']['background_sprite_sheet']
        )

        # Set new actors:
        for name in scene_data['actors']:
            character_scene_data: dict = scene_data['actors'][name]
            character: Character = self._characters_collection.get(name)

            character.hidden = False
            character.set_pose(
                pose_number=character_scene_data['character_animation']
            )
            character.set_plan(
                plan=character_scene_data['character_plan']
            )
            character.set_position(
                position=character_scene_data['character_start_position']
            )

        # Scene text settings:
        if scene_data['gameplay_type'] == 'reading':
            self._text_canvas.text_canvas_status = True
            self.set_reading_words(
                script=self._text_reading_dialogues_gameplay_data.get(
                    self.current_language
                )[scene_data["current_scene_name"]]
            )
        elif scene_data['gameplay_type'] == 'choice':
            self._text_canvas.text_canvas_status = False

        # Special effects:
        if scene_data['special_effects'] is not False:
            ...

        # Sounds settings:
        for key, value in scene_data['sounds'].items():
            self._sound_director.sound_chanel_controller(
                sound_chanel=key,
                sound_file_name=value
            )
