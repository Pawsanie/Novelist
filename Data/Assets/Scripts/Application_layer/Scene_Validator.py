from os import sep

from .Stage_Director import StageDirector
from .Assets_load import json_load, sound_load, music_load
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Sound_Director import SoundDirector
from .Settings_Keeper import SettingsKeeper
"""
Contains SceneValidator code.
"""


class SceneValidator(SingletonPattern):
    """
    Controls in what order the scenes go and their settings.
    """
    def __init__(self):
        # Screenplay loading:
        self.screenplay: dict = json_load(
            path_list=[
                'Scripts', 'Json_data', 'screenplay'
            ]
        )
        self.choices_data: dict = json_load(
            path_list=[
                'Scripts', 'Json_data', 'Dialogues', 'choices_data'
            ]
        )

        # Program layers settings:
        self.stage_director: StageDirector = StageDirector()
        self.sound_director: SoundDirector = SoundDirector()
        self.settings_keeper: SettingsKeeper = SettingsKeeper()

        # Scene FLAGS:
        # START as default!
        self.scene: str = 'START'
        # 'scene_01' as default!
        self.scene_flag: str = 'scene_01'
        self.next_scene: str = ''
        self.past_scene: str = ''
        self.scene_gameplay_type: str = ''
        self.default_scene_name: str = 'scene_01'

        # Other settings:
        self.status: bool = True

    def __call__(self):
        """
        Manages game scene selection and rendering.
        """
        # Keep current scene:
        if all((
                self.status is False,
                self.scene_flag == self.scene
        )):
            return

        # Set new scene:
        self.stage_director.vanishing_scene()
        scene: dict = self.screenplay[self.scene_flag]
        self.stage_director.set_scene(location=scene['background'])
        for name in scene['actors']:
            character: dict[str, dict] = scene['actors'][name]
            self.stage_director.set_actor(character=name)\
                .set_pose(pose_number=character['character_pose'])
            self.stage_director.set_actor(character=name)\
                .set_plan(plan=character['character_plan'])

            if character['character_start_position'] == 'middle':
                self.stage_director.set_actor(character=name)\
                    .move_to_middle()
            if character['character_start_position'] == 'right':
                self.stage_director.set_actor(character=name)\
                    .move_to_right()
            if character['character_start_position'] == 'left':
                self.stage_director.set_actor(character=name)\
                    .move_to_left()

        # Scene FLAG settings:
        self.scene: str = self.scene_flag
        self.next_scene: str = scene['next_scene']
        self.past_scene: str = scene['past_scene']
        self.scene_gameplay_type: str = scene['gameplay_type']

        # Scene text settings:
        if self.scene_gameplay_type is not False:  # TODO: Remake?
            if self.scene_gameplay_type == 'reading':
                self.stage_director.text_canvas.text_canvas_status = True
                self.stage_director.set_reading_words(
                    script=self.stage_director.text_dict_reading.get(
                        self.stage_director.language_flag
                    )[self.scene]
                )
                self.autosave()
            if self.scene_gameplay_type == 'choice':
                self.stage_director.text_canvas.text_canvas_status = False
        else:
            self.stage_director.text_canvas.text_canvas_status = False  # TODO: Remake?

        # Special effects:
        if scene['special_effects'] is not False:
            ...

        # Sounds settings:
        for key, value in scene['sounds'].items():
            if value is not False:
                asset_type: str = ''

                # Music:
                if key == 'music_channel':
                    asset_type: str = 'Music'

                # Sound effects:
                if key == 'sound_channel':
                    asset_type: str = 'Effects'

                # Character Speach:
                if key == 'voice_channel':
                    if self.sound_director.single_voiceover_language is True:
                        asset_type: str = 'Voice'
                    else:
                        asset_type: str = f"Voice{sep}{self.settings_keeper.voice_acting_language}"

                self.sound_chanel_controller(
                    asset_type=asset_type,
                    sound_chanel=key,
                    sound_file_name=value
                )

    def sound_chanel_controller(self, asset_type: str, sound_file_name: str, sound_chanel: str):
        """
        Send soundtrack to sound chanel if necessary.

        :param asset_type: Asset "Sounds" sub folder.
        :type asset_type: str
        :param sound_file_name: Sound file name.
        :type sound_file_name: str
        :param sound_chanel: Sound chanel type.
        :type sound_chanel: str
        """
        # Change soundtrack in sound chanel:
        if self.sound_director.channels_collection[sound_chanel]['sound_file_name'] != sound_file_name:
            self.sound_director.status = True
            if asset_type == 'Music':
                sound_file = music_load(
                    asset_type=asset_type,
                    file_name=sound_file_name
                )
            else:
                sound_file = sound_load(
                    asset_type=asset_type,
                    file_name=sound_file_name
                )
            self.sound_director.channels_collection[sound_chanel]['sound_file'] = sound_file
            self.sound_director.channels_collection[sound_chanel]['sound_file_name'] = sound_file_name
            self.sound_director.channels_collection[sound_chanel]['devnull_status'] = True

        # Keep current soundtrack in sound chanel:
        else:
            self.sound_director.channels_collection[sound_chanel]['sound_file'] = None
            self.sound_director.channels_collection[sound_chanel]['devnull_status'] = False

    @staticmethod
    def autosave():
        """
        If current scene type is reading autosave it.
        """
        from .Save_Keeper import SaveKeeper
        SaveKeeper().save(auto_save=True)
