from pygame import display, Surface, font

from .Character import characters_generator
from .Background import backgrounds_generator
"""
Contains stage director program code.
Stage director control scenes by class methods interfaces.
"""


class StageDirector:
    """
    Controls game scenes and assets loads.
    StageDirector used in "Gameplay.py" for gameplay programming.
    """
    def __init__(self, *, screen: display, background_surface: Surface):
        """
        Initializes class params and assets loads.
        :param screen: pygame.display surface.
        :param background_surface: pygame.Surface.
        """
        """Assets loading:"""
        # Characters load:
        self.characters_dict: dict = characters_generator(background_surface=background_surface)
        # Backgrounds load:
        self.backgrounds_dict: dict = backgrounds_generator(screen_surface=screen)

        """Arguments processing:"""
        self.background_surface: Surface = background_surface
        self.screen: display = screen
        # self.protagonist: str = protagonist

    def set_scene(self, *, location: str) -> Surface.blit:
        """
        Update background Image, for scene render.
        :param location: String with background location name.
        :return: Background for scene render.
        """
        scene = self.backgrounds_dict.get(location)
        scene.scale()
        scene_image = scene.scene_image
        # Update background surface:
        self.background_surface.blit(scene_image, (0, 0))
        return self.screen.blit(self.background_surface, (0, 0))

    def set_actor(self, *, character: str) -> Surface.blit:
        return self.characters_dict.get(character)

    def words(self, *, who: str, what: str):
        test = font.Font(font.get_default_font(), 36)

        # now print the text
        text_surface = test.render('Hello world', antialias=True, color=(0, 0, 0))
        # screen.blit(text_surface, dest=(0, 0))
