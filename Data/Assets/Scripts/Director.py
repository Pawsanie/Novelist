from pygame import display, Surface, font

from .Character import Character, characters_generator
from .Scene import Background
"""
Contains stage director program code.
Stage director control scenes by class methods interfaces.
"""


class StageDirector:
    """
    Controls game scenes.
    """
    def __init__(self, *, characters: dict, protagonist: str, scenes: dict,
                 screen: Surface, background: Surface):
        """
        Init class params:
        :param characters: Tuple with dict which contains:
                           {character_name: {
                           str('surface'): PyGame.Surface(for_render),
                           str('character_art'): class_exemplar.Character(),
                           str('coordinates_pixels'): list[x, y]}}
        :param protagonist: String with protagonist name.
        :param scenes: Dict with scenes: contains {name_of_scene: PyGame.Surface(scene_image)}
        """
        self.background = background
        self.characters = characters
        # self.characters = characters_generator(characters_list=characters,
        #                                        background_surface=background)
        self.protagonist = protagonist
        self.scenes = scenes
        self.screen = screen
        self.background_interface = Background(screen_surface=screen,
                                               scene_image=None)
        # self.character_interface = Character(surface=None,
        #                                      character_image=None,
        #                                      character_size=None)

    def set_scene(self, *, location: str) -> Surface.blit:
        """
        Update background Image, for scene render.
        :param location: String with background location name.
        :return: Background for scene render.
        """
        scene = self.scenes.get(location)
        self.background_interface.scene_image = scene
        scene_image = self.background_interface.scale()
        # Update background surface:
        self.background.blit(scene_image, (0, 0))
        return self.screen.blit(self.background, (0, 0))

    def set_actor(self, *, character: str) -> Surface.blit:
        result = self.characters.get(character)
        return result

    def words(self, *, who: str, what: str):
        test = font.Font(font.get_default_font(), 36)

        # now print the text
        text_surface = test.render('Hello world', antialias=True, color=(0, 0, 0))
        # screen.blit(text_surface, dest=(0, 0))


