from .Interface_Controller import InterfaceController
from ..Scene_Validator import SceneValidator
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
        # User Interface controller settings:
        self.interface_controller: InterfaceController = InterfaceController()

    def input_wait_ready(self):
        """
        Stop loop after user command and redraw image.
        """
        self.scene_validator.scene = 'redraw'
