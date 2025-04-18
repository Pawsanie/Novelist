from pygame import Surface

from ..Game_objects.Character import characters_generator
from ..Game_objects.Background import Background
from ..User_Interface.UI_Text_Canvas import TextCanvas
from ..Game_objects.Dialogues import DialogueKeeper, DialoguesWords
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Settings_Keeper import SettingsKeeper
from ..Game_objects.Character import Character
from ..Application_layer.Sound_Director import SoundDirector
# Lazy import:
# from ..Render.Batch import Batch
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
        self.current_language: str = self._settings_keeper.get_text_language()
        self._text_canvas: TextCanvas = TextCanvas()
        self._dialog_controller: DialoguesWords = DialoguesWords()
        self._text_dialogues_data: dict[str, dict[str, dict]] = DialogueKeeper().get_dialogues_data()
        self._text_reading_dialogues_gameplay_data: dict[str, dict[str, dict]] = self._text_dialogues_data['reading']
        self._text_dict_reading_cash: dict = {}

    def set_scene(self, *, location: str):
        """
        Update background Image, for scene render.
        Use in StateMachine and Self.
        :param location: String with background location name.
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

    def vanishing_scene(self):
        """
        Delete all characters and background from scene.
        """
        self._background.devnull()
        for character in self._characters_collection.values():
            character.kill()

        self._text_canvas.status = False
        self._dialog_controller.status = False

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

        # Text canvas:
        if self._text_canvas.status is True:
            result.append(
                self._text_canvas.get_sprite()
            )
        if self._dialog_controller.status is True:
            # Speech:
            result.append(
                self._dialog_controller.make_words(
                    text_string=self._text_dict_reading_cash['what']['text'],
                    text_color=self._text_dict_reading_cash['what']['color'],
                    text_type='words'
                )
            )
            # Speaker:
            result.append(
                self._dialog_controller.make_words(
                    text_string=self._text_dict_reading_cash['who']['text'],
                    text_color=self._text_dict_reading_cash['who']['color'],
                    text_type='speaker'
                )
            )
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
            self._text_dict_reading_cash: dict[str, str] = \
                self._text_reading_dialogues_gameplay_data.get(
                    self.current_language
                )[
                    scene_data["current_scene_name"]
                ]
            self._text_canvas.status = True
            self._dialog_controller.status = True

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
