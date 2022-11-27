from .Stage_Director import StageDirector
from .Assets_load import json_load
"""
Contains SceneValidator code.
"""


class SceneValidator:
    """
    Controls in what order the scenes go and their settings.

    :param director: Import StageDirector.
    :type director: StageDirector.
    """
    def __init__(self, *, director: StageDirector):
        """
        :param director: Import StageDirector.
        :type director: StageDirector.
        """
        # Screenplay loading:
        self.screenplay: dict = json_load(path_list=['Scripts', 'Json_data', 'screenplay'])
        # Stage Director settings:
        self.director: StageDirector = director
        # Scene FLAG:
        self.scene: str = 'START'  # START as default!
        self.scene_flag: str = 'test'  # <------- TEST SCENE!
        self.next_scene: str = ''
        self.past_scene: str = ''

    def __call__(self):
        """
        Manages game scene selection and rendering.
        """
        # Set new scene!:
        if self.scene_flag != self.scene:
            self.director.vanishing_scene()
            scene: dict = self.screenplay[self.scene_flag]
            self.director.set_scene(location=scene['background'])
            for name in scene['actors']:
                character = scene['actors'][name]
                self.director.set_actor(character=name).set_pose(pose_number=character['character_pose'])
                self.director.set_actor(character=name).set_plan(plan=character['character_plan'])
                if character['character_start_position'] == 'middle':
                    self.director.set_actor(character=name).move_to_middle()
                if character['character_start_position'] == 'right':
                    self.director.set_actor(character=name).move_to_right()
                if character['character_start_position'] == 'left':
                    self.director.set_actor(character=name).move_to_left()
            # Scene FLAG settings!:
            self.scene: str = self.scene_flag
            self.next_scene: str = scene['next_scene']
            self.past_scene: str = scene['past_scene']
            # Scene text settings!:
            self.director.set_words(script=self.director.text_dict.get(self.director.language_flag)[self.scene])
            # Special effects!:
            if scene['special_effects'] is not False:
                ...
        # Keep current scene!:
        else:
            pass
        self.director.action()
