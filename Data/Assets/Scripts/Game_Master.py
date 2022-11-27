from .Gameplay import main_loop, GamePlay
from .Stage_Director import StageDirector
# from .Render import Render
from .Scene_Validator import SceneValidator
from .Interface_Controller import InterfaceController


class GameMaster:
    def __init__(self, *, display_screen, start_settings):
        """
        Set all settings for Stage Director and game.
        Entry point for gameplay.

        :param display_screen: pygame.display.Surface
        """
        # Collect base game settings:
        self.settings_keeper = start_settings
        # Stage Director settings:
        self.stage_director: StageDirector = StageDirector(display_screen=display_screen)
        self.scene_validator: SceneValidator = SceneValidator(director=self.stage_director)
        # Interface Controller settings:
        self.language_flag: str = self.settings_keeper.text_language
        self.interface_controller = InterfaceController(
            background_surface=self.stage_director.background_surface,
            language_flag=self.language_flag)
        # Gameplay input controller:
        self.gameplay = GamePlay(stage_director=self.stage_director,
                                 interface_controller=self.interface_controller,
                                 scene_validator=self.scene_validator)
        # Render settings:
        # self.render: Render = Render()

    @main_loop
    def __call__(self):
        self.gameplay()
        self.scene_validator()
