from .Interface_Controller import InterfaceController
from ..Application_layer.Scene_Validator import SceneValidator
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
        self.scene_validator: SceneValidator = SceneValidator()
        self.state_machine: StateMachine = StateMachine()
        # User Interface controller settings:
        self.interface_controller: InterfaceController = InterfaceController()
        self.status: bool = False

    def input_wait_ready(self):
        """
        Stop loop after user command and redraw image.
        """
        self.scene_validator.status = True

    def input_mouse(self, event):
        """
        Interface interaction in MasterClass menu.
        :param event: pygame.event from main_loop.
        """
        pass

    def key_bord_key_down(self, event):
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

    def menu_input(self, event):
        """
        Menu conveyor.
        :param event: pygame.event from main_loop.
        """
        # Button game menu ui status:
        self.input_mouse(event)
        # Button game menu key bord status:
        self.key_bord_key_down(event)
        # Redraw screen image:
        self.input_wait_ready()
