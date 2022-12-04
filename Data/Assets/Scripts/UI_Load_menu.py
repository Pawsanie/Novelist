from .UI_Base_menu import BaseMenu
"""
Contains Load menu code.
"""


class LoadMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Load Menu.

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
        super(LoadMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)

    def load_menu_input(self, event):
        """
        Load menu conveyor:
        :param event: pygame.event from main_loop.
        """
        if self.interface_controller.load_from_start_menu_flag is True:
            ...
        if self.interface_controller.load_from_game_menu_flag is True:
            ...
        self.input_wait_ready()
