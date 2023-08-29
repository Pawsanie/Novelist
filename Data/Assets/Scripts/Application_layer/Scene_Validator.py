from .Stage_Director import StageDirector
from .Assets_load import json_load
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Sound_Director import SoundDirector
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

        # Directors settings:
        self.stage_director: StageDirector = StageDirector()
        # self.sound_director: SoundDirector = SoundDirector()

        # Scene FLAGS:
        # START as default!
        self.scene: str = 'START'
        # 'scene_01' as default!
        self.scene_flag: str = 'scene_01'
        self.next_scene: str = ''
        self.past_scene: str = ''
        self.scene_gameplay_type: str = ''
        self.default_scene_name: str = 'scene_01'

        self.status: bool = True

    def __call__(self):
        """
        Manages game scene selection and rendering.
        """
        # Keep current scene!:
        if all((
                self.status is False,
                self.scene_flag == self.scene
        )):
            return

        # Set new scene!:
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

        # Scene FLAG settings!:
        self.scene: str = self.scene_flag
        self.next_scene: str = scene['next_scene']
        self.past_scene: str = scene['past_scene']
        self.scene_gameplay_type: str = scene['gameplay_type']

        # Scene text settings!:
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

        # Special effects!:
        if scene['special_effects'] is not False:
            ...

    @staticmethod
    def autosave():
        """
        If current scene type is reading autosave it.
        """
        from .Save_Keeper import SaveKeeper
        SaveKeeper().save(auto_save=True)
