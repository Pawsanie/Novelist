from pygame import time, QUIT, quit
import pygame.event

from .Stage_Director import StageDirector
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
        main_cycle_fps = 20
        while program_running:
            func(*args, **kwargs)
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                    program_running = False
            main_cycle_fps_clock.tick(main_cycle_fps)
    return coroutine


@main_coroutine
def test_scene_01(director):
    director.set_scene(location='back_ground_01')
    director.set_actor(character='Nurse').set_pose(pose_number='2')
    director.set_actor(character='Nurse').set_plan(plan='background_plan')
    # director.set_actor(character='Nurse').move_to_right()
    # director.set_actor(character='Nurse').reflect()
    director.set_actor(character='Nurse').move_to_left()

    director.set_actor(character='Test').set_pose(pose_number='1')
    director.set_actor(character='Test').set_plan(plan='first_plan')

    director.set_actor(character='Test2').set_pose(pose_number='3')
    director.set_actor(character='Test2').set_plan(plan='background_plan')
    director.set_actor(character='Test2').move_to_right()

    director.action()


def vanishing_scene(director):
    for character in director.characters_dict.values():
        character.kill()


def gameplay_stage_director_initialization(*, display_screen):
    """
    Set all settings for Stage Director and game.
    Entry point for gameplay.
    """
    # Stage Director settings:
    director = StageDirector(screen=display_screen)
    vanishing_scene(director)
    test_scene_01(director)
    # director.action()


def scene_validator():
    ...

# ['Scripts', 'Scenes_Scripts', 'screenplay.json']
