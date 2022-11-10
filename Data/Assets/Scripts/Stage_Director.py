from pygame import display, Surface

from .Character import characters_generator
from .Background import backgrounds_generator
from .Render import background_sprite_data, render
from .UI_Text_Canvas import TextCanvas
from .Dialogues import generate_dialogues, DialoguesWords
"""
Contains stage director program code.
Stage director control scenes by class methods interfaces.
"""


class StageDirector:
    """
    Controls game scenes and assets loads.
    StageDirector used in "Gameplay.py" for gameplay programming.

    :param display_screen: Display surface.
    :type display_screen: pygame.display.Surface
    """
    def __init__(self, *, display_screen: display):
        """
        Initializes class params and assets loads.
        """
        # Make background surface:
        background_data: tuple = background_sprite_data(display_surface=display_screen)
        self.background_surface: Surface = Surface(background_data[0])
        self.background_coordinates: tuple[int, int] = background_data[1]
        """Assets loading:"""
        # Characters load:
        self.characters_dict: dict = characters_generator(background_surface=self.background_surface)
        # Backgrounds load:
        self.backgrounds_dict: dict = backgrounds_generator(display_surface=display_screen)
        self.location = None
        """Make UI:"""
        # Text canvas:
        self.text_canvas = TextCanvas(background_surface=self.background_surface)
        self.text_canvas_surface: Surface = self.text_canvas.generator()[0]
        # Text generation:
        self.text_controller = DialoguesWords(font_name=None,
                                              text_canvas=self.text_canvas_surface)
        self.language_flag = 'eng'  # ENG as default.
        self.text_dict: dict[str] = generate_dialogues()
        self.text_string: str = ''  # Blank as default.
        self.text_speaker: str = ''  # Blank as default.
        self.speech: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        self.speaker: tuple[Surface, tuple[int, int]] = (Surface((0, 0)), (0, 0))
        """Arguments processing:"""
        self.display_screen: display = display_screen

    def set_scene(self, *, location: str) -> Surface.blit:
        """
        Update background Image, for scene render.

        :param location: String with background location name.
        :return: Background for scene render.
        """
        scene = self.backgrounds_dict.get(location)
        self.location = scene
        scene.scale()
        scene_image: Surface = scene.scene_image
        # Update background surface:
        self.background_surface.blit(scene_image, (0, 0))
        return self.display_screen.blit(self.background_surface, self.background_coordinates)

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
        self.location.scale()
        self.text_canvas.scale(background_surface=self.background_surface)
        for character in self.characters_dict.values():
            character.scale(background_surface=self.background_surface)
        render(screen=self.display_screen,
               background=self.background_surface,
               characters_dict=self.characters_dict,
               text_canvas=self.text_canvas.generator(),
               speech=self.speech,
               speaker=self.speaker,
               background_coordinates=self.background_coordinates)

    def vanishing_scene(self):
        """
        Delete all characters and background from scene.
        """
        background_data: tuple = background_sprite_data(display_surface=self.display_screen)
        self.background_surface: Surface = Surface(background_data[0])
        self.background_coordinates: tuple[int, int] = background_data[1]
        for character in self.characters_dict.values():
            character.kill()
        self.text_string: str = ''
        self.text_speaker: str = ''

    def set_words(self, *, script: dict):
        """
        Set a speaker and his words and these text colors.
        Get data from self.text_dict.

        :param script:
        """
        speaker: str = script['who'][0]
        speaker_color: str = script['who'][1]
        text: str = script['what'][0]
        text_color: str = script['what'][1]
        self.text_string: str = text
        self.text_speaker: str = speaker
        self.speech: tuple[Surface, tuple[int, int]] = \
            self.text_controller.make_words(text_string=self.text_string,
                                            text_color=text_color,
                                            text_type='words',
                                            backgrounds_surface=self.background_surface)
        self.speaker: tuple[Surface, tuple[int, int]] = \
            self.text_controller.make_words(text_string=self.text_speaker,
                                            text_color=speaker_color,
                                            text_type='speaker',
                                            backgrounds_surface=self.background_surface)
