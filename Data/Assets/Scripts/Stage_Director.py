from pygame import display, Surface, font

from .Character import characters_generator
from .Background import backgrounds_generator
from .Render import background_sprite_size, render
"""
Contains stage director program code.
Stage director control scenes by class methods interfaces.
"""


class StageDirector:
    """
    Controls game scenes and assets loads.
    StageDirector used in "Gameplay.py" for gameplay programming.
    """
    def __init__(self, *, screen: display):
        """
        Initializes class params and assets loads.
        :param screen: pygame.display surface.
        """
        # Make background surface:
        self.background_surface: Surface = Surface(background_sprite_size(display_surface=screen))
        """Assets loading:"""
        # Characters load:
        self.characters_dict: dict = characters_generator(background_surface=self.background_surface)
        # Backgrounds load:
        self.backgrounds_dict: dict = backgrounds_generator(screen_surface=screen)
        """Arguments processing:"""
        self.display_screen: display = screen

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
        return self.display_screen.blit(self.background_surface, (0, 0))

    def set_actor(self, *, character: str) -> Surface.blit:
        """
        :param character: String with character name.
        :return: pygame.Surface of character.
        """
        return self.characters_dict.get(character)

    def action(self):
        """
        Render image.
        """
        render(screen=self.display_screen,
               background=self.background_surface,
               characters_dict=self.characters_dict)

    def words(self, *, who: str, what: str):
        test = font.Font(font.get_default_font(), 36)

        # now print the text
        text_surface = test.render('Hello world', antialias=True, color=(0, 0, 0))
        # screen.blit(text_surface, dest=(0, 0))
