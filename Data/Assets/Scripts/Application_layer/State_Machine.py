from ..Universal_computing.Pattern_State_Machine import StateMachinePattern
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..GamePlay.Scene_Validator import SceneValidator
from ..User_Interface.Interface_Controller import InterfaceController
from .Stage_Director import StageDirector
from .Sound_Director import SoundDirector
from ..Universal_computing.Assets_load import AssetLoader
"""
Contend code for switch between gameplay and menu state.
"""


class MenuState(SingletonPattern):
    """
    Menu state for StateMachine.
    """
    def __init__(self):
        # Program layers settings:
        self._interface_controller: InterfaceController = InterfaceController()
        self._stage_director: StageDirector = StageDirector()
        self._sound_director: SoundDirector = SoundDirector()

        # Sound settings:
        self._menu_music_data: dict = AssetLoader().json_load(
            ['Scripts', 'Json_data', 'menu_sound_settings']
        )

        # Specific name switcher:
        self._game_menu_name: str = 'game_menu'

    def __call__(self):
        # Scene settings:
        menu_name: str | None = self._interface_controller.menu_name
        self._stage_director.vanishing_scene()
        self._stage_director.set_scene(
            location=menu_name
        )
        if menu_name is None:
            menu_name: str = self._game_menu_name

        # Sound data:
        menu_data: dict = self._menu_music_data[menu_name]
        for sound_chanel in self._menu_music_data[menu_name]:
            sound_file_name: str | bool = menu_data[sound_chanel]

            self._sound_director.sound_chanel_controller(
                sound_file_name=sound_file_name,
                sound_chanel=sound_chanel
            )


class StateMachine(StateMachinePattern, SingletonPattern):
    """
    Contend state machine for switch between menu and gameplay states.
    """
    _state_collection = [
        MenuState(),
        SceneValidator()  # GamePlay state.
    ]

    def __init__(self):
        super().__init__(
            collection=self._state_collection
        )

    def __call__(self):
        """
        Call from GameMaster.
        """
        self.state()
