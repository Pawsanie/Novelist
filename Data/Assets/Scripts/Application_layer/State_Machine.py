from ..Universal_computing.Pattern_State_Machine import StateMachinePattern
from ..Universal_computing.Pattern_Singleton import SingletonPattern
from .Scene_Validator import SceneValidator
from ..User_Interface.Interface_Controller import InterfaceController
from .Stage_Director import StageDirector
"""
Contend code for switch between gameplay and menu state.
"""


class MenuState(SingletonPattern):
    """
    Menu state for StateMachine.
    """
    def __init__(self):
        self.interface_controller: InterfaceController = InterfaceController()
        self.stage_director: StageDirector = StageDirector()

    def __call__(self):
        menu_name: str = self.interface_controller.menu_name
        self.stage_director.vanishing_scene()
        self.stage_director.set_scene(
            location=menu_name
        )


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
