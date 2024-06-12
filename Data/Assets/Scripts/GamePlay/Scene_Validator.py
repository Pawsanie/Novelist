from ..Application_layer.Stage_Director import StageDirector
from ..Universal_computing.Assets_load import AssetLoader
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Application_layer.Sound_Director import SoundDirector
from ..Application_layer.Settings_Keeper import SettingsKeeper
"""
Contains SceneValidator code.
"""


class SceneValidator(SingletonPattern):
    """
    Controls in what order the scenes go and their settings.
    """
    def __init__(self):
        # Program layers settings:
        self._asset_loader: AssetLoader = AssetLoader()
        self.stage_director: StageDirector = StageDirector()
        self.sound_director: SoundDirector = SoundDirector()
        self.settings_keeper: SettingsKeeper = SettingsKeeper()

        # Screenplay loading:
        self.screenplay: dict = self._asset_loader.json_load(
            path_list=[
                'Scripts', 'Json_data', 'screenplay'
            ]
        )
        self.choices_data: dict = self._asset_loader.json_load(
            path_list=[
                'Scripts', 'Json_data', 'Dialogues', 'choices_data'
            ]
        )

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
            self.stage_director.set_actor(character=name).position = \
                character['character_start_position']

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
            self.sound_director.sound_chanel_controller(
                sound_chanel=key,
                sound_file_name=value
            )

    @staticmethod
    def autosave():
        """
        If current scene type is reading autosave it.
        """
        from ..Application_layer.Save_Keeper import SaveKeeper
        SaveKeeper().save(auto_save=True)
