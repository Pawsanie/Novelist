from .UI_Base_menu import BaseMenu
"""
Contains Save menu code.
"""


class SaveMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Save Menu.

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
        super(SaveMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def save_menu_input(self, event):
        """
        Save menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.input_wait_ready()
