from .Interface_Controller import InterfaceController
from .Scene_Validator import SceneValidator
"""
Contains code for User Interface Master Class.
"""


class BaseMenu:
    """
    User Interface menu Master Class!

    :param interface_controller: InterfaceController exemplar.
                                 Responsible for user interface status and buttons.
    :type interface_controller: InterfaceController
    :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
    :type scene_validator: SceneValidator
    """
    def __init__(self, *, interface_controller: InterfaceController,
                 scene_validator: SceneValidator):
        """
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                                Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        """
        # Control in game scene order:
        self.scene_validator: SceneValidator = scene_validator
        # User Interface controller settings:
        self.interface_controller: InterfaceController = interface_controller

    def input_wait_ready(self):
        """
        Stop loop after user command and redraw image.
        """
        self.scene_validator.scene = 'redraw'
