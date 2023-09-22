from pygame.mixer import Sound

from ..Universal_computing.Pattern_State_Machine import StateMachinePattern
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Scene_Validator import SceneValidator
from ..User_Interface.Interface_Controller import InterfaceController
from .Stage_Director import StageDirector
from .Sound_Director import SoundDirector
from .Assets_load import music_load, json_load
"""
Contend code for switch between gameplay and menu state.
"""


class MenuState(SingletonPattern):
    """
    Menu state for StateMachine.
    """
    def __init__(self):
        # Program layers settings:
        self.interface_controller: InterfaceController = InterfaceController()
        self.stage_director: StageDirector = StageDirector()
        self.sound_director: SoundDirector = SoundDirector()

        # Sound settings:
        self.menu_music_data: dict = json_load(
            ['Scripts', 'Json_data', 'menu_sound_settings']
        )

        # Specific name switcher:
        self.game_menu_name: str = 'game_menu'

    def __call__(self):
        # Scene settings:
        menu_name: str | None = self.interface_controller.menu_name
        self.stage_director.vanishing_scene()
        self.stage_director.set_scene(
            location=menu_name
        )
        if menu_name is None:
            menu_name: str = self.game_menu_name

        # Sound data:
        menu_data: dict = self.menu_music_data[menu_name]
        for sound_chanel in self.menu_music_data[menu_name]:
            sound_file_name: str | bool = menu_data[sound_chanel]
            if sound_file_name is not False:

                # Change soundtrack in sound chanel:
                if self.sound_director.channels_collection[sound_chanel]['sound_file_name'] != sound_file_name:
                    sound_file: Sound = music_load(
                        asset_type='Music',
                        file_name=sound_file_name
                    )
                    self.sound_director.channels_collection[sound_chanel]['sound_file'] = sound_file
                    self.sound_director.channels_collection[sound_chanel]['devnull_status'] = True

                # Keep current soundtrack in sound chanel:
                else:
                    self.sound_director.channels_collection[sound_chanel]['sound_file'] = None
                    self.sound_director.channels_collection[sound_chanel]['devnull_status'] = False


class StateMachine(StateMachinePattern, SingletonPattern):
    """
    Contend state machine for switch between menu and gameplay states.
    """
    state_collection = [
        MenuState(),
        SceneValidator()  # GamePlay state.
    ]

    def __init__(self):
        super().__init__(
            collection=self.state_collection
        )

    def __call__(self):
        self.state()
