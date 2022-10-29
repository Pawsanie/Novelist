from pygame import time, QUIT, quit
import pygame.event

from .Stage_Director import StageDirector
from .Assets_load import json_load
"""
Contains gameplay code.
"""


def main_coroutine(func):
    """
    MAIN Coroutine!:
    Decorator with the main loop of game.
    """
    def coroutine(*args, **kwargs):
        program_running = True
        main_cycle_fps_clock = time.Clock()
        main_cycle_fps = 30
        while program_running:
            func(*args, **kwargs)
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                    program_running = False
            main_cycle_fps_clock.tick(main_cycle_fps)
    return coroutine


def gameplay_stage_director_initialization(*, display_screen):
    """
    Set all settings for Stage Director and game.
    Entry point for gameplay.
    """
    # Stage Director settings:
    director = StageDirector(display_screen=display_screen)
    gameplay = SceneValidator(director=director)
    gameplay()
    # display_image_render_loop(director, gameplay)


class SceneValidator:
    """
    Controls in what order the scenes go and their settings.

    Do not add render loop in this class: pygame surface flip conflicts with it.
    :param director: Import StageDirector.
    :type director: StageDirector.
    """
    def __init__(self, *, director: StageDirector):
        # Screenplay loading:
        self.screenplay: dict = json_load(path_list=['Scripts', 'Json_data', 'screenplay'])
        # Stage Director settings:
        self.director: StageDirector = director
        # Scene FLAG:
        # START as default!
        self.scene: str = 'START'
        self.scene_flag: str = 'test'  # <------- TEST SCENE!
        self.next_scene: str = ''
        self.past_scene: str = ''

    @main_coroutine
    def __call__(self):
        # Set new scene!:
        if self.scene_flag != self.scene:
            self.director.vanishing_scene()
            scene = self.screenplay[self.scene_flag]
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
            self.scene = self.scene_flag
            self.next_scene = scene['next_scene']
            self.past_scene = scene['past_scene']
            # Special effects!:
            if scene['special_effects'] is not False:
                ...
        # Keep current scene!:
        else:
            pass
        self.director.action()
