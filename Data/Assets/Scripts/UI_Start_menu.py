from .UI_Base_menu import BaseMenu
"""
Contains Start menu code.
"""


class StartMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Start Menu.

    :param interface_controller: InterfaceController exemplar.
                                 Responsible for user interface status and buttons.
    :type interface_controller: InterfaceController
    :param scene_validator: SceneValidator exemplar.
                        Responsible for scene order and scene construction.
    :type scene_validator: SceneValidator
    """
    def __init__(self, *, interface_controller, scene_validator):
        """
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        """
        super(StartMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def start_menu_input(self, event):
        """
        Start menu conveyor:
        :param event: pygame.event from main_loop.
        """
        ...
