from pygame.event import Event

from .Interface_Controller import InterfaceController
from ..GamePlay.Scene_Validator import SceneValidator
from ..Application_layer.State_Machine import StateMachine
"""
Contains code for User Interface Master Class.
"""


class BaseMenu:
    """
    User Interface menu Master Class!
    """
    def __init__(self):
        # Control in game scene order:
        self._scene_validator: SceneValidator = SceneValidator()
        self._state_machine: StateMachine = StateMachine()
        # User Interface controller settings:
        self._interface_controller: InterfaceController = InterfaceController()
        self.status: bool = False

    def _input_wait_ready(self):
        """
        Stop loop after user command and redraw image.
        """
        self._scene_validator.status = True

    def _input_mouse(self, event: Event):
        """
        Interface interaction in MasterClass menu.
        :param event: pygame.event from main_loop.
        """
        pass

    def _key_bord_key_down(self, event: Event):
        """
        Interface interaction in MasterClass menu.
        :param event: pygame.event from main_loop.
        """
        pass

    def handle(self):
        """
        Part of StateMachine pattern.
        """
        pass

    def menu_input(self, event: Event):
        """
        Menu conveyor.
        :param event: pygame.event from main_loop.
        """
        # Button game menu ui status:
        self._input_mouse(event)
        # Button game menu key bord status:
        self._key_bord_key_down(event)
        # Redraw screen image:
        self._input_wait_ready()
