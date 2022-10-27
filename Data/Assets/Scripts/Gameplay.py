from .Stage_Director import StageDirector


def test_scene_01(director):
    director.set_scene(location='back_ground_01')
    director.set_actor(character='Nurse').set_pose(pose_number='2')


def vanishing_scene(director):
    for character in director.characters_dict.values():
        character.kill()


def gameplay_stage_director_initialization(*, display_screen):
    # Stage Director settings:
    director = StageDirector(screen=display_screen)
    vanishing_scene(director)
    test_scene_01(director)
    director.action()


def scene_validator():
    ...

# ['Scripts', 'Scenes_Scripts', 'screenplay.json']
